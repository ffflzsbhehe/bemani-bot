from collections import defaultdict

from nonebot import on_command, on_regex
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from nonebot.adapters.cqhttp import Message

from src.libraries.tool import hash
from src.libraries.sdvx_music import *
from src.plugins.sdvx_cover import *
from src.libraries.image import *

import re
import os



def song_txt(music: Music):
    sid = music.id.zfill(4)
    level: List[str] = []
    placeholder: [str] = '-'
    for i in range(0,len(music.difficulty)):
        if music.difficulty[i]['difnum'] == '0':
            level.append(placeholder)
        else:
            level.append(music.difficulty[i]['difnum'])
    jkid: [str] = '1'
    jkid = get_cover(sid)
    return Message([
        {
            "type": "text",
            "data": {
                "text": f"{sid}. {music.title_name}\n"
            }
        },
        {
            "type": "image",
            "data": {
                "file": f"file:///C:/Users/Administrator/Desktop/bot/src/static/sdvx/jk_{sid}_{jkid}.jpg"
            }
        },
        {
            "type": "text",
            "data": {
                "text": f"\n{'/'.join(level)}"
            }
        }
    ])


def randomjrmw(h):
    h1 = h+7
    music = total_list[h1 % len(total_list)]
    
    return Message([
        {"type": "text", "data": {"text": f"\n今日SDVX金曲：\n"}}
    ] + song_txt(music))

spec_rand = on_regex(r"^(?i)SDVX随个(?:dx|sd|标准)?[紫黄红彩白]?[0-9]+\+?")


@spec_rand.handle()
async def _(bot: Bot, event: Event, state: T_State):
    level_labels = ['紫', '黄', '红', '彩', '白']

    regex = "sdvx随个((?:dx|sd|标准))?([紫黄红彩白]?)([0-9]+\+?)"
    res = re.match(regex, str(event.get_message()).lower())
    try:
        level = res.groups()[2]
        if res.groups()[1] == "":
            music_data = total_list.filter(level=level)
        else:
            music_data = total_list.filter(level=level, diff=['紫黄红彩白'.index(res.groups()[1])])
            
        if len(music_data) == 0:
            if res.groups()[2] == "21":
                rand_result = song_txt(total_list.by_id('1103'))
            else:
                rand_result = "你动动奶子想想我能随出来你妈个狗愣子五花逼"
        elif res.groups()[2] == "1":
            rand_result = "有1吗"
        else:
            rand_result = song_txt(music_data.random())
        if random.randint(0,100) == 7:
            svcdnd = ['影子此时在打永劫无间因此拒绝了你的随机请求','这都要我随机是不是懒B','我随机出来了，但我不想告诉你','随机结果：向轮椅奔去 -1/-1/-1/-1','随机结果：冰！！！！！','Result:_EmpErr0R 获取结果失败','不知道','我没空，能不能自己随','猪B吧','影子绝赞溜冰中，故此决定拒绝你此次的请求，再求我一次我就告诉你']
            await spec_rand.send(f"{random.choice(svcdnd)}")
        else:
            await spec_rand.send(rand_result)
    except Exception as e:
        print(e)
        await spec_rand.finish("随歌儿都几把随不明白了")



sr = on_regex(r".*(?i)SDVX.*什么")


@sr.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if random.randint(0,100) == 7:
        svcdnd = ['影子此时在打永劫无间因此拒绝了你的随机请求','这都要我随机是不是懒B','我随机出来了，但我不想告诉你','随机结果：向轮椅奔去 -1/-1/-1/-1','随机结果：冰！！！！！','Result:_EmpErr0R 获取结果失败','不知道','我没空，能不能自己随','猪B吧','影子绝赞溜冰中，故此决定拒绝你此次的请求，再求我一次我就告诉你']
        await sr.send(f"{random.choice(svcdnd)}")
    else:
        await sr.finish(song_txt(total_list.random())) 



search_music = on_regex(r"^(?i)SDVX查歌.+")


@search_music.handle()
async def _(bot: Bot, event: Event, state: T_State):
    regex = "(?i)sdvx查歌(.+)"
    name = re.match(regex, str(event.get_message())).groups()[0].strip()
    if name == "":
        return
    res = total_list.filter(title_search=name)
    res += total_list.filter(author_search=name)
    if len(res) == 0:
        await search_music.send("你爹找不到，爬")
    elif len(res) < 50:
        search_result = ""
        for music in sorted(res, key = lambda i: int(i['id'])):
            print(music)
            search_result += f"{music['id']}. {music.info['title_name']}\n"
        await search_music.finish(Message([
            {"type": "text",
                "data": {
                    "text": search_result.strip()
                }}]))
    else:
        await search_music.send(f"结果过多（{len(res)} 条），影子怀疑你用一个字当搜索条件，是不是A手粉丝啊")
        
        
query_chart = on_regex(r"^([紫黄红彩白]?)sdvx([0-9]+)")


@query_chart.handle()
async def _(bot: Bot, event: Event, state: T_State):
    regex = "([紫黄红彩白]?)sdvx([0-9]+)"
    groups = re.match(regex, str(event.get_message())).groups()
    level_labels = ['紫', '黄', '红', '彩', '白']
    if groups[0] != "":
        try:
            level_index = level_labels.index(groups[0])
            

            name = groups[1]
            music = total_list.by_id(name)
            level = music.difficulty[level_index]['difnum']
            version = music.info['inf_ver']
            effect = music.difficulty[level_index]['effected_by']
            illu = music.difficulty[level_index]['illustrator']
            verinf = '该难度不存在'
            if version == '2':
                verinf = 'INFINITY'
            elif version == '3':
                verinf = 'GRAVITY'
            elif version == '4':
                verinf = 'HEAVENLY'
            elif version == '5':
                verinf = 'VIVID'
            level_name = ['NOVICE', 'ADVANCED', 'EXHAUST', f'{verinf}', 'MAXIMUM']
            level_name_alt = ['NOVICE', 'ADVANCED', 'EXHAUST', 'infinity', 'MAXIMUM']
            sid = name.zfill(4)
            version_d = '代码错误'
            version_r = music.info['version']
            if version_r == '1':
                version_d = 'Sound Voltex Booth'
            elif version_r == '2':
                version_d = 'Sound Voltex II: Infinite Infection'
            elif version_r == '3':
                version_d = 'Sound Voltex III: Gravity Wars'
            elif version_r == '4':
                version_d = 'Sound Voltex IV: Heavenly Haven'
            elif version_r == '5':
                version_d = 'Sound Voltex: Vivid Wave'
            cover_id = get_cover_s(sid,level_index)
            
            chain_level = level_name_alt[level_index].lower()
            chain = chain_list.by_title(music.info['title_name'],chain_level)
            file = f"file:///C:/Users/Administrator/Desktop/bot/src/static/sdvx/jk_{sid}_{cover_id}.jpg"
            
            msg = f'''{level_name[level_index]} {level}
MAX CHAIN: {chain}
版本: {version_d}
封面画师： {illu}
Effected By: {effect}'''
            await query_chart.send(Message([
                {
                    "type": "text",
                    "data": {
                        "text": f"{music['id']}. {music.info['title_name']}\n"
                    }
                },
                {
                    "type": "image",
                    "data": {
                        "file": f"{file}"
                    }
                },
                {
                    "type": "text",
                    "data": {
                        "text": msg
                    }
                }
            ]))
        except Exception as e:
            print(e)
            await query_chart.send("找不到批")
    else:
        name = groups[1]
        music = total_list.by_id(name)
        try:

            artist = music.info['artist_name']
            sid = name.zfill(4)
            bpm_max = float(music.info['bpm_max'])
            bpm_min = float(music.info['bpm_min'])
            bpmmax = bpm_max / 100
            bpmmin = bpm_min / 100
            version_d = '代码错误'
            version_r = music.info['version']
            if version_r == '1':
                version_d = 'Sound Voltex Booth'
            elif version_r == '2':
                version_d = 'Sound Voltex II: Infinite Infection'
            elif version_r == '3':
                version_d = 'Sound Voltex III: Gravity Wars'
            elif version_r == '4':
                version_d = 'Sound Voltex IV: Heavenly Haven'
            elif version_r == '5':
                version_d = 'Sound Voltex: Vivid Wave'
            level: List[str] = []
            placeholder: [str] = '-'
            for i in range(0,len(music.difficulty)):
                if music.difficulty[i]['difnum'] == '0':
                    level.append(placeholder)
                else:
                    level.append(music.difficulty[i]['difnum'])
            jkid: [str] = '1'
            jkid = get_cover(sid)
            level: List[str] = []
            placeholder: [str] = '-'
            for i in range(0,len(music.difficulty)):
                if music.difficulty[i]['difnum'] == '0':
                    level.append(placeholder)
                else:
                    level.append(music.difficulty[i]['difnum'])
            file = f"file:///C:/Users/Administrator/Desktop/bot/src/static/sdvx/jk_{sid}_{jkid}.jpg"
            await query_chart.send(Message([
                {
                    "type": "text",
                    "data": {
                        "text": f"{music['id']}. {music.info['title_name']}\n"
                    }
                },
                {
                    "type": "image",
                    "data": {
                        "file": f"{file}"
                    }
                },
                {
                    "type": "text",
                    "data": {
                        "text": f"艺术家: {artist}\n最大BPM: {bpmmax}\n最小BPM: {bpmmin}\n版本: {version_d}\n难度: {'/'.join(level)}"
                    }
                }
            ]))
        except Exception as e:
            print(e)
            await query_chart.send("是不是他妈的嘉心糖，找不到嘉然唱的曲子别搜了")

query_score = on_command('大图')

@query_score.handle()
async def _(bot: Bot, event: Event, state: T_State):
    r = "([紫黄红彩白])(sdvx)?([0-9]+)"
    argv = str(event.get_message()).strip().split(" ")
    grp = re.match(r, argv[0]).groups()
    level_labels = ['紫', '黄', '红', '彩', '白']
    level_index = level_labels.index(grp[0])
    chart_id = grp[2]
    sid = chart_id.zfill(4)
    cover_id = get_cover_s(sid,level_index)

    file = f"file:///C:/Users/Administrator/Desktop/bot/src/static/sdvx/JPEG/jk_{sid}_{cover_id}_b.jpg"
    await query_chart.send(Message([
    {
        "type": "image",
        "data": {
            "file": f"{file}"
        }
    }
    ]))

query_score = on_command('SDVX分数线' , aliases={'sdvx分数线'})


@query_score.handle()
async def _(bot: Bot, event: Event, state: T_State):
    r = "([紫黄红彩白])(sdvx)?([0-9]+)"
    argv = str(event.get_message()).strip().split(" ")
    if len(argv) == 1 and argv[0] == '帮助':
        s = '''有他妈笨b
命令格式：SDVX分数线 <难度+歌曲id> <分数线>
例如：分数线 紫sdvx799 10000000
命令将返回分数线允许的 NEAR 容错以及 ERROR容错。
2 NEAR = 1 ERROR
分数线支持直接输入PUC，S，鸟，鸟加
输入二位数或三位数会自动补全后面的零'''

        await query_score.send(Message([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(text_to_image(s)), encoding='utf-8')}"
            }
        }]))
    elif len(argv) == 2:
        try:
            grp = re.match(r, argv[0]).groups()
            level_labels = ['紫', '黄', '红', '彩', '白']

            level_index = level_labels.index(grp[0])
            chart_id = grp[2]
            if argv[1] == 'puc' or argv[1] == 'PUC':
                line = float(10000000)
            elif argv[1] == 'S' or argv[1] == 's':
                line = float(9900000)
            elif argv[1] == '鸟+' or argv[1] == '鸟加':
                line = float(9800000)
            elif argv[1] == '鸟':
                line = float(9700000)
            elif len(argv[1]) == 2:
                line = float(f"{argv[1]}00000")
            elif len(argv[1]) == 3:
                line = float(f"{argv[1]}0000")
            else:
                line = float(argv[1])
            music = total_list.by_id(chart_id)
            version = music.info['inf_ver']
            verinf = '该难度不存在'
            if version == '2':
                verinf = 'INFINITY'
            elif version == '3':
                verinf = 'GRAVITY'
            elif version == '4':
                verinf = 'HEAVENLY'
            elif version == '5':
                verinf = 'VIVID'
            level_labels2 = ['NOVICE', 'ADVANCED', 'EXHAUST', f'{verinf}', 'MAXIMUM']
            
            level_labels3 = ['NOVICE', 'ADVANCED', 'EXHAUST', 'infinity', 'MAXIMUM']
            chain_level = level_labels3[level_index].lower()
            max_chain = float(chain_list.by_title(music.info['title_name'],chain_level))
            print(chain_list.by_title(music.info['title_name'],'infinity'))
            total_score = float(10000000)
            reduce = 10000000 - line
            near_score = total_score / (max_chain * 2)
            if reduce <= 0 or reduce >= 10000000:
                raise ValueError
            await query_chart.send(f'''{music.info['title_name']} {level_labels2[level_index]}
分数线 {int(line)} 允许的最多 NEAR 数量为 {int(reduce / near_score)}(向下取整)，允许的最多 ERROR 数量为 {int(reduce / (near_score * 2))}(向下取整)''')
        except Exception as e:
            print(e)
            await query_chart.send("快几把看看帮助吧哥哥（如果正常歌曲分数线出现错误，你的命令格式没出错并且你很确定bot的数据库中记录了这首歌的这个难度，请私聊作者）")

wm_list = ['背诵吉吉国圣经','调戏bot','溜冰塔罗牌','溜冰', '拆机', '越级', '下埋', '出警', '游玩永劫无间', '溜iidx', '打拼机的人', '看电棍', '看A手', '看然然','游玩Apex','登顶国服百强']
info_list = ['哈比下！奥利安费，all in！！！','你白银说让我随机今日运势，我就是给你随机今日运势，你知道为什么吗？（后略）','很难说没有大','MY NAME IS MR. 冰 冰 冰！！！！！','千雪在的话想必一定会说：千雪提醒您：打机时不要大力拍打或滑动哦，呜呜，千冰，我的雪','拆机有风险，小心被线下solo喔','新手溜冰一次要控制好量','嘟嘟嘟嘟嘟，给你妈愉悦送走','喵喵喵喵 喵喵喵喵 喵喵 喵喵喵喵喵喵 喵喵喵喵 喵喵喵喵 喵喵 喵喵喵']


jrwm = on_command('今日运势', aliases={'今日溜冰'})


@jrwm.handle()
async def _(bot: Bot, event: Event, state: T_State):
    qq = int(event.get_user_id())
    h = hash(qq)
    rp = h % 100
    wm_value = []
    for i in range(11):
        wm_value.append(h & 3)
        h >>= 2
    s = f"今日人品值：{rp}\n"
    for i in range(11):
        if wm_value[i] == 3:
            s += f'宜 {wm_list[i]}\n'
        elif wm_value[i] == 0:
            s += f'忌 {wm_list[i]}\n'
    s += f"影子提醒您：{random.choice(info_list)}\n今日推荐歌曲："
    music = total_list[h % len(total_list)]
    await jrwm.finish(Message([
        {"type": "text", "data": {"text": s}}
    ] + song_txt(music)))