import json
import re
from nonebot import require
from datetime import datetime
from nonebot import on_message
from nonebot import on_command
from nonebot import get_driver
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Event, MessageEvent, PrivateMessageEvent
from nonebot.rule import to_me
from .arcade_data import EMPTY_STATE, get_all_regions

SUPERUSERS = get_driver().config.superusers

__zx_plugin_name__ = "机厅 help"


help_handler = on_command("机厅 help", priority=10, block=True)

@help_handler.handle()
async def handle_help(bot: Bot, event: GroupMessageEvent):
    help_message = (
        "地区列表\n"
        "绑定机厅 <地区>\n"
        "解绑机厅\n"
        "jtj\n"
        "<机厅>几/j\n"
        "<机厅>数字/+-数字\n"
    )
    await help_handler.send(help_message)

    
region_list_handler = on_command("地区列表", priority=10, block=True)

@region_list_handler.handle()
async def handle_region_list(bot: Bot, event: GroupMessageEvent):
    # 获取所有可用地区
    regions = get_all_regions()
    
    if not regions:
        await region_list_handler.send("当前没有可用的地区")
        return
    
    # 格式化地区列表
    region_list = "、".join(regions)
    message = f"地区列表：\n{region_list}"
    
    await region_list_handler.send(message)


reset_handler = on_command("重置机厅", priority=10, block=True)
@reset_handler.handle()
async def handle_reset(bot: Bot, event: Event):
    user_id = event.get_user_id()
    if user_id not in SUPERUSERS:
        await reset_handler.send("您没有权限执行此操作")
    else:
        reset_state()
        await reset_handler.send("机厅人数已重置")

def reset_state():
    updated_data = []

    # 遍历 arcade_data.py 中的所有机厅
    for arcade in EMPTY_STATE:
        # 初始化机厅的状态，人数设置为 0，更新时间为 04:00:00
        reset_arcade = {
            "primary_keyword": arcade["primary_keyword"],
            "keywords": arcade["keywords"],
            "peopleCount": 0,
            "updatedBy": "无",
            "lastUpdatedAt": "04:00:00",
            "region": arcade["region"]
        }
        updated_data.append(reset_arcade)

    # 将初始化后的数据写入 state.json 文件
    with open(STATE_FILE, 'w', encoding='utf-8') as file:
        json.dump(updated_data, file, ensure_ascii=False, indent=2)

    print("机厅人数已重置")

        
# 获取 APScheduler 定时器
scheduler = require("nonebot_plugin_apscheduler").scheduler

@scheduler.scheduled_job("cron", hour=4, minute=0)
async def scheduled_task():
    reset_state()  # 调用重置状态的函数
    

STATE_FILE = "state.json"
  	
    
jtj_handler = on_command("jtj", priority=10, block=True)

@jtj_handler.handle()
async def handle_jtj(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id
    group_region = read_group_region()

    # 检查群组是否有绑定地区
    if str(group_id) not in group_region:
        await jtj_handler.send("请发送 绑定机厅 <地区> 进行绑定")
        return
    
    region_name = group_region[str(group_id)]
    
    # 从 state.json 中读取机厅数据
    arcades = read_state()

    # 筛选出属于该地区的机厅
    region_arcades = [arcade for arcade in arcades if arcade['region'] == region_name]

    if not region_arcades:
        await jtj_handler.send(f"未找到地区 '{region_name}' 的机厅数据。")
        return

    # 格式化机厅信息并发送
    response_message = format_arcades_message(region_arcades, region_name)
    await jtj_handler.send(response_message)

# 保持原来的格式化方法不变
def format_arcades_message(arcades, region):
    message_lines = []
    
    for arcade in arcades:
        if region == arcade['region']:
            line = f"{arcade['primary_keyword']}：{arcade['peopleCount']}人"
            message_lines.append(line)
    return "\n".join(message_lines)

    
  
arcade_handler = on_message(priority=999)
@arcade_handler.handle()
async def handle_arcade(bot: Bot, event: GroupMessageEvent):
    arcades = read_state()
    group_id = event.group_id
    group_region = read_group_region().get(str(group_id))

    message = event.get_message().extract_plain_text().strip()
    user_info = await bot.get_group_member_info(group_id=group_id, user_id=event.user_id)
    user_nickname = user_info.get('nickname', '') + "(" + event.get_user_id() + ")"
    
    response = get_response(message, user_nickname, arcades, group_region)
    if response:
        await arcade_handler.send(response)
    save_state(arcades)


def get_response(message, user_nickname, arcades, group_region):
    
    # 如果绑定了地区，过滤出绑定地区的机厅
    region_arcades = [arcade for arcade in arcades if arcade["region"] == group_region]

    for arcade in region_arcades:
        for keyword in arcade["keywords"]:
            if message.startswith(keyword):
                updated = update_arcade_people_count(message, user_nickname, arcade, keyword)
                if updated:
                    save_state(arcades)
                    return f"更新成功！\n{arcade['primary_keyword']}\n当前：{arcade['peopleCount']}人"
                elif keyword + "几" in message or keyword + "j" in message:
                    return f"{arcade['primary_keyword']}\n当前：{arcade['peopleCount']}人\n\n上报：{arcade['updatedBy']}\n时间：{arcade['lastUpdatedAt']}"
    return None


def update_arcade_people_count(message, user_nickname, arcade, keyword):
    # 使用正则表达式来匹配消息中的数字
    match = re.search(f"{keyword}(\+|\-)?(\d+)", message)
    if not match:
        return False
    # 提取操作符和数字
    operator, number_str = match.groups()
    number = int(number_str)
    if operator == "+":
        arcade["peopleCount"] += number
    elif operator == "-":
        arcade["peopleCount"] -= number
    else:
        arcade["peopleCount"] = number
    arcade["updatedBy"] = user_nickname
    arcade["lastUpdatedAt"] = datetime.now().strftime("%H:%M:%S")
    return True  # 表示更新成功
  

def read_state():
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        with open(STATE_FILE, 'w', encoding='utf-8') as file:
            json.dump(EMPTY_STATE, file, ensure_ascii=False, indent=2)
        return EMPTY_STATE

def save_state(arcades):
    with open(STATE_FILE, 'w', encoding='utf-8') as file:
        json.dump(arcades, file, ensure_ascii=False, indent=2)
        
        
# 将新的机厅数据与已有的人数数据合并，并删除不在 arcade_data.py 中的机厅
def sync_arcade_data():
    # 读取当前 state.json 的数据
    current_data = read_state()

    # 构建一个以 "primary_keyword" 为键的字典，便于后续合并
    current_data_map = {arcade["primary_keyword"]: arcade for arcade in current_data}

    # 用来存储同步后的数据
    updated_data = []

    # 从 arcade_data.py 中获取所有的机厅关键词列表
    arcade_primary_keywords = [arcade["primary_keyword"] for arcade in EMPTY_STATE]

    # 遍历 arcade_data.py 中的 ARCADES 列表
    for arcade in EMPTY_STATE:
        primary_keyword = arcade["primary_keyword"]
        # 如果 state.json 中有这个机厅，保留它的人数数据
        if primary_keyword in current_data_map:
            existing_arcade = current_data_map[primary_keyword]
            arcade["peopleCount"] = existing_arcade.get("peopleCount", 0)
            arcade["updatedBy"] = existing_arcade.get("updatedBy", "无")
            arcade["lastUpdatedAt"] = existing_arcade.get("lastUpdatedAt", "04:00:00")
        else:
            # 如果是新的机厅，初始化人数数据
            arcade["peopleCount"] = 0
            arcade["updatedBy"] = "无"
            arcade["lastUpdatedAt"] = "04:00:00"

        updated_data.append(arcade)

    # 删除 state.json 中不再存在于 arcade_data.py 的机厅
    # 遍历 current_data，保留在 arcade_primary_keywords 中的机厅
    updated_data = [arcade for arcade in updated_data if arcade["primary_keyword"] in arcade_primary_keywords]

    # 将合并后的数据写回到 state.json 文件
    with open(STATE_FILE, 'w', encoding='utf-8') as file:
        json.dump(updated_data, file, ensure_ascii=False, indent=2)

    print("同步成功，已将机厅数据更新到 state.json")

# 定义同步指令
sync_handler = on_command("更新机厅", priority=10, block=True)

@sync_handler.handle()
async def handle_sync(bot: Bot, event: GroupMessageEvent):
    user_id = event.get_user_id()

    # 如果用户不是超级用户，禁止同步
    if user_id not in SUPERUSERS:
        await sync_handler.send("您没有权限执行此操作")
        return

    # 调用同步函数
    sync_arcade_data()

    await sync_handler.send("机厅数据已更新！")
        
        
GROUP_REGION_FILE = "group_region.json"

def read_group_region():
    try:
        with open(GROUP_REGION_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_group_region(group_region):
    with open(GROUP_REGION_FILE, 'w', encoding='utf-8') as file:
        json.dump(group_region, file, ensure_ascii=False, indent=2)

# 命令用于绑定地区
bind_region_handler = on_command("绑定机厅", priority=10, block=True)

@bind_region_handler.handle()
async def handle_bind_region(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id
    message = event.get_message().extract_plain_text().strip()
    region_name = message.replace("绑定机厅", "").strip()  # 去掉命令部分，提取地区名
    
    if not region_name:
        await bind_region_handler.send("请输入地区，如：绑定机厅 杭州")
        return
    
    # 获取所有有效的地区
    valid_regions = get_all_regions()
    # 检查用户输入的地区是否有效
    if region_name not in valid_regions:
        # 将有效地区列表格式化为字符串
        available_regions = "、".join(valid_regions)
        await bot.send(event, f"绑定失败：地区 '{region_name}' 不存在！\n可用地区有：{available_regions}")
        return
    
    group_region = read_group_region()
    group_region[str(group_id)] = region_name  # 将群组与地区绑定
    save_group_region(group_region)

    await bind_region_handler.send(f"已绑定机厅地区：{region_name}")

    
unbind_region_handler = on_command("解绑机厅", priority=10, block=True)

@unbind_region_handler.handle()
async def handle_unbind_region(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id
    group_region = read_group_region()

    if str(group_id) not in group_region:
        await unbind_region_handler.send("本群无需解绑")
        return

    del group_region[str(group_id)]  # 删除该群的绑定记录
    save_group_region(group_region)

    await unbind_region_handler.send("本群机厅已解绑")

    
    
