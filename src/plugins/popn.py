from collections import defaultdict

from nonebot import on_command, on_regex
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from nonebot.adapters.cqhttp import Message

from src.libraries.tool import hash
from src.libraries.popn_music import *
from src.libraries.image import *

import re
import os


def song_txt(music: Music):
    sid = music.id
    
    
    return Message([
        {
            "type": "text",
            "data": {
                "text": f"{sid}. {music.title}\nStandard:{'/'.join(music.difficulty[0:4])}\nBattle:{'/'.join(music.difficulty[4:6])}\nBPM:{music.bpm}\n角色：{music.chara}\n版本：{music.version}\n曲师：{music.artist}"}}])
    

spec_rand = on_regex(r"^(?i)popn随个(?:dx|sd|标准)?[蓝绿黄红对战]*[0-9]+\+?")


@spec_rand.handle()
async def _(bot: Bot, event: Event, state: T_State):
    level_labels = ['蓝','绿','黄','红','对战绿','对战黄']

    regex = "popn随个((?:dx|sd|标准))?([蓝绿黄红对战]*)([0-9]+\+?)"
    res = re.match(regex, str(event.get_message()).lower())
    
    
        
    try:
        if res.groups()[0] == "dp":
            tp = ["dp"]
        elif res.groups()[0] == "dp" or res.groups()[0] == "标准":
            tp = ["sp"]
        else:
            tp = ["sp", "dp"]
        level = res.groups()[2]
        if res.groups()[1] == "":
            music_data = total_list.filter(level=level)
        else:
            level_index = level_labels.index(res.groups()[1])
            music_data = total_list.filter(level=level, diff=[level_index])
            if res.groups()[1] == '对战':
                music_data = total_list.filter(level=level, diff=[4,5])
        if len(music_data) == 0:
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



sr = on_regex(r".*(?i)popn.*什么")


@sr.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if random.randint(0,100) == 7:
        svcdnd = ['影子此时在打永劫无间因此拒绝了你的随机请求','这都要我随机是不是懒B','我随机出来了，但我不想告诉你','随机结果：向轮椅奔去 -1/-1/-1/-1','随机结果：冰！！！！！','Result:_EmpErr0R 获取结果失败','不知道','我没空，能不能自己随','猪B吧','影子绝赞溜冰中，故此决定拒绝你此次的请求，再求我一次我就告诉你']
        await sr.send(f"{random.choice(svcdnd)}")
    else:
        await sr.finish(song_txt(total_list.random())) 



search_music = on_regex(r"^(?i)popn查歌.+")


@search_music.handle()
async def _(bot: Bot, event: Event, state: T_State):
    regex = "(?i)popn查歌(.+)"
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
            search_result += f"{music['id']}. {music['title']}\n"
        await search_music.finish(Message([
            {"type": "text",
                "data": {
                    "text": search_result.strip()
                }}]))
    else:
        await search_music.send(f"结果过多（{len(res)} 条），影子怀疑你用一个字当搜索条件，是不是A手粉丝啊")
        
        
query_chart = on_regex(r"^([蓝绿黄红对战]*)popn([0-9]+)")


@query_chart.handle()
async def _(bot: Bot, event: Event, state: T_State):
    regex = "([蓝绿黄红对战]*)popn([0-9]+)"
    groups = re.match(regex, str(event.get_message())).groups()
    level_labels = ['蓝','绿','黄','红','对战绿','对战黄']
    if groups[0] != "":
        try:
            level_index = level_labels.index(groups[0])
            
            
            name = groups[1]
            music = total_list.by_id(name)
            level = music['difficulty'][level_index]
            version = music['version']
            level_name_alt = ['EASY', 'NORMAL', 'HYPER', 'EX', 'Battle NORMAL','Battle HYPER']
            sid = name

            level_index_1 = level_index
            zero_note = ['-','-','-','-','-','-','-','-','-','-']
            if music['long'] == []:
                music['long'] = zero_note.copy()
            await query_chart.send(f"{music['id']}.{music['title']} \n{level_name_alt[level_index_1]} \n总物量：{music['notecounts'][level_index]}\nLong pop-kun：{music['long'][level_index]}")
        except Exception as e:
            print(e)
            await query_chart.send("找不到批")
    else:
        name = groups[1]
        music = total_list.by_id(name)
        try:
            await query_chart.send(song_txt(music)) 
        except Exception as e:
            print(e)
            await query_chart.send("是不是他妈的嘉心糖，找不到嘉然唱的曲子别搜了")


query_score = on_command('popn分数线')


@query_score.handle()
async def _(bot: Bot, event: Event, state: T_State):
    r = "([蓝绿黄红对战]*)(popn)?([0-9]+)"
    argv = str(event.get_message()).strip().split(" ")
    if len(argv) == 1 and argv[0] == '帮助':
        s = '''有他妈笨b
命令格式：popm分数线 <难度+歌曲id> <分数线>
例如：popn分数线 紫popn799 AA
命令将返回分数线允许的容错。'''

        await query_score.send(Message([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(text_to_image(s)), encoding='utf-8')}"
            }
        }]))
    elif len(argv) == 2:
        try:
            grp = re.match(r, argv[0]).groups()
            level_labels = ['蓝','绿','黄','红','对战绿','对战黄']

            level_index = level_labels.index(grp[0])
            chart_id = grp[2]
            if argv[1] == 'S' or argv[1] == 's':
                line = float(98000)
            elif argv[1] == 'AAA' or argv[1] == 'aaa':
                line = float(95000)
            elif argv[1] == 'AA' or argv[1] == 'aa':
                line = float(90000)
            elif argv[1] == 'AA' or argv[1] == 'aa':
                line = float(82000) 
            elif argv[1] == 'B' or argv[1] == 'b':
                line = float(72000)
            elif argv[1] == 'C' or argv[1] == 'c':
                line = float(62000)
            elif argv[1] == 'D' or argv[1] == 'd':
                line = float(50000)
            elif argv[1] == 'E' or argv[1] == 'e':
                line = float(0)
            else:
                line = float(argv[1])

            
            music = total_list.by_id(chart_id)

            level_name_alt = ['EASY', 'NORMAL', 'HYPER', 'EX', 'Battle NORMAL','Battle HYPER']

            
            
            
            
            total_score = float(100000)


            note = float(music.notecounts[level_index])
            fract = total_score / note
            


            await query_chart.send(f'''{music['title']} {level_name_alt[level_index]}
分数线 {argv[1].upper()} 允许的最多 GREAT 数量为 {int((total_score - line) / (fract * 0.3))}(向下取整)，允许的最多GOOD数量为 {int((total_score - line) / (fract * 0.6))}(向下取整)，允许的最多MISS数量为 {int((total_score - line) / fract)}(向下取整)''')
        except Exception as e:
            print(e)
            await query_chart.send("快几把看看帮助吧哥哥（如果正常歌曲分数线出现错误，你的命令格式没出错并且你很确定bot的数据库中记录了这首歌的这个难度，请私聊作者）")

