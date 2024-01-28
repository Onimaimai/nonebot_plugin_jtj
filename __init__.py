import json
import re
from nonebot import require
from datetime import datetime
from nonebot import on_message
from nonebot import on_command
from nonebot import get_driver
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Event, MessageEvent, PrivateMessageEvent
from nonebot.rule import to_me

SUPERUSERS = get_driver().config.superusers

__zx_plugin_name__ = "jtj [Hidden]"

reset_handler = on_command("重置机厅", priority=10, block=True)
@reset_handler.handle()
async def handle_reset(bot: Bot, event: Event):
    user_id = event.get_user_id()
    if user_id not in SUPERUSERS:
        await reset_handler.send("您没有权限执行此操作。")
    else:
        reset_state()
        await reset_handler.send("机厅人数已重置。")

def reset_state():
    with open(STATE_FILE, 'w', encoding='utf-8') as file:
        json.dump(EMPTY_STATE, file, ensure_ascii=False, indent=2)
	
    print("机厅人数已重置")
        
# 获取 APScheduler 定时器
scheduler = require("nonebot_plugin_apscheduler").scheduler

# 设置每天0点执行的定时任务
@scheduler.scheduled_job("cron", hour=0, minute=0)
async def scheduled_task():
    reset_state()  # 调用重置状态的函数
    

STATE_FILE = "state.json"
EMPTY_STATE = [
    {
      	"primary_keyword": "工位",
        "keywords": ["工位", "gw"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
  	{
      	"primary_keyword": "机房",
        "keywords": ["机房", "jf"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
  	{
      	"primary_keyword": "超市",
        "keywords": ["超市", "cs"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
  	{
      	"primary_keyword": "驿站",
        "keywords": ["驿站", "yz"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
  	{
      	"primary_keyword": "餐厅",
        "keywords": ["餐厅", "ct"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
  	{
      	"primary_keyword": "食堂",
        "keywords": ["食堂", "st"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
  	{
      	"primary_keyword": "望湖轩",
        "keywords": ["望湖轩", "whx", "wh"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
  	{
      	"primary_keyword": "图书馆",
        "keywords": ["图书馆", "tsg"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
  	{
      	"primary_keyword": "实验室",
        "keywords": ["实验室", "sys"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
  	{
      	"primary_keyword": "海底捞",
        "keywords": ["捞", "hdl"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
	{
      	"primary_keyword": "萨莉亚",
        "keywords": ["萨", "sly"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
  	{
      	"primary_keyword": "星巴克",
        "keywords": ["星巴克", "xbk"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
  	{
      	"primary_keyword": "瑞幸咖啡",
        "keywords": ["瑞幸咖啡", "瑞幸", "rx"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
  	{
      	"primary_keyword": "库迪咖啡",
        "keywords": ["库迪咖啡", "库迪", "kd"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
    {
      	"primary_keyword": "杭州丁桥天街菲游乐",
        "keywords": ["菲游乐","fyl"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
    {
      	"primary_keyword": "杭州新天地风云再起",
        "keywords": ["新天地", "xtd"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
  	{
      	"primary_keyword": "杭州工联CC卡通尼",
        "keywords": ["卡通尼", "cc"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
  	{
      	"primary_keyword": "杭州延安天空之城mai",
        "keywords": ["天空mai", "tkmai"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
    {
      	"primary_keyword": "杭州延安天空之城chu",
        "keywords": ["天空chu", "tkchu"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
  	{
      	"primary_keyword": "杭州东站量子空间",
        "keywords": ["dz", "东站"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
  	{
      	"primary_keyword": "杭州滨银in77第一回合mai",
        "keywords": ["77mai"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
    {
      	"primary_keyword": "杭州滨银in77第一回合chu",
        "keywords": ["77chu"],
        "peopleCount": 0,
        "updatedBy": "无",
        "lastUpdatedAt": "00:00:00",
    },
  	
]
  
  
jtj_handler = on_command("jtj", priority=10, block=True)
@jtj_handler.handle()
async def handle_jtj(bot: Bot, event: Event):
    user_id = event.get_user_id()
    full_command = str(event.get_message()).strip()
    prefix = full_command[3:] if full_command.startswith("jtj") else ""

    # 需要超级用户权限的情况
    if not prefix and user_id not in SUPERUSERS:
        return  # 如果没有前缀且用户不是超级用户，直接返回

    arcades = read_state()  # 读取机厅数据
    message = format_arcades_message(arcades, prefix)  # 格式化消息
    if message:
      	await jtj_handler.send(message)  # 发送消息


def read_state():
    try:
        with open('state.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # 如果文件不存在，返回空列表

def format_arcades_message(arcades, prefix):
    message_lines = []
    
    for arcade in arcades:
        if prefix in arcade['primary_keyword']:
            line = f"{arcade['primary_keyword']}：{arcade['peopleCount']}人"
            message_lines.append(line)
    return "\n".join(message_lines)
  	
  
arcade_handler = on_message(priority=999)
@arcade_handler.handle()
async def handle_arcade(bot: Bot, event: Event):
    arcades = read_state()
    message = event.get_message().extract_plain_text()
    if isinstance(event, GroupMessageEvent):
        user_id = event.user_id
        group_id = event.group_id
        user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
        user_nickname = user_info.get('nickname', '') + "(" + event.get_user_id() + ")"  # 获取群昵称
    else:
        user_nickname = event.get_user_id()  # 对于非群消息，使用用户 ID

    response = get_response(message, user_nickname, arcades)
    if response:
        await arcade_handler.send(response)
    save_state(arcades)


def get_response(message, user_nickname, arcades):
    for arcade in arcades:
        for keyword in arcade["keywords"]:
            primary_keyword = arcade["primary_keyword"]
            if keyword in message:
                updated = update_arcade_people_count(message, user_nickname, arcade, keyword)
                if updated:
                    # 如果发生了更新，保存状态并返回更新信息
                    save_state(arcades)
                    return f"更新成功！\n{primary_keyword}\n当前：{arcade['peopleCount']}人"
                elif keyword + "几" in message or keyword + "j" in message:
                    return f"{primary_keyword}\n当前：{arcade['peopleCount']}人\n\n上报：{arcade['updatedBy']}\n时间：{arcade['lastUpdatedAt']}"
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

        
