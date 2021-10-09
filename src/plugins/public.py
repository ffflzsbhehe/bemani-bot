import random
import re

from PIL import Image
from nonebot import on_command, on_message, on_notice, require, get_driver, on_regex
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Message, Event, Bot
from src.libraries.image import *
from random import randint


help = on_command('help')


@help.handle()
async def _(bot: Bot, event: Event, state: T_State):
    help_str = '''哥你都在这个群多久了还能不知道这个啊.jpg
千雪回来之前就让影子来帮助你推进你的卖〇事业吧！
今日溜冰 查看今天的溜冰指导
今日舞萌 查看今天的舞萌运势
XXXmaimaiXXX什么 随机一首maimai的歌
XXXsdvxXXX什么 随机一首SDVX的歌
随个[dx/标准][绿黄红紫白]<难度> 随机一首指定条件的maimai乐曲
SDVX随个[紫黄红彩白]<难度> 随机一首指定条件的SDVX乐曲
查歌<乐曲标题的一部分> 查询符合条件的maimai乐曲
SDVX查歌<乐曲标题的一部分或者作者名称的一部分> 查询符合条件的SDVX乐曲
[绿黄红紫白]id<歌曲编号> 查询maimai乐曲信息或谱面信息
[紫黄红彩白]sdvx<歌曲编号> 查询SDVX乐曲信息或谱面信息
<歌曲别名>是什么歌 查询乐曲别名对应的maimai乐曲
定数查歌 <定数>  查询定数对应的乐曲
定数查歌 <定数下限> <定数上限>
分数线 <难度+歌曲id> <分数线> 详情请输入“分数线 帮助”查看
SDVX分数线 <难度+歌曲id> <分数线> 详情请输入“SDVX分数线 帮助”查看
以上SDVX相关功能把SDVX替换成iidx或者popn就是二寺和破盆的功能，使用方式完全一样，除了难度标志不同
chiwaht，吃嘛，吃什么等... 获取在天津随机出勤地点干饭的建议
地名/机厅名chiwaht 获取该地点/机厅准确的干饭情报
没有想要的地名请整理好该地区有什么吃的,因为作者认识的地方基本都加了
bot管它喊燒餅静蓝SB影子炎勠骚冰或者你喜欢的名字都好'''

    await help.send(Message([{
        "type": "image",
        "data": {
            "file": f"base64://{str(image_to_base64(text_to_image(help_str)), encoding='utf-8')}"
        }
    }]))


async def _group_poke(bot: Bot, event: Event, state: dict) -> bool:
    value = (event.notice_type == "notify" and event.sub_type == "poke" and event.target_id == int(bot.self_id))
    return value


poke = on_notice(rule=_group_poke, priority=10, block=True)


@poke.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if event.__getattribute__('group_id') is None:
        event.__delattr__('group_id')
    await poke.send(Message([{
        "type": "poke",
        "data": {
            "qq": f"{event.sender_id}"
        }
    }]))

