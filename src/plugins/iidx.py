from collections import defaultdict

from nonebot import on_command, on_regex
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from nonebot.adapters.cqhttp import Message

from src.libraries.tool import hash
from src.libraries.iidx_music import *
from src.libraries.image import *

import re
import os


def song_txt(music: Music):
    sid = music.id
    
    
    return Message([
        {
            "type": "text",
            "data": {
                "text": f"{sid}. {music.title}\nSP:{'/'.join(music.difficulty[0:5])}\nDP:{'/'.join(music.difficulty[5:9])}\nBPM:{music.bpm}\nGenre：{music.genre}\n版本：{music.version}\n曲师：{music.artist}"}}])
    

spec_rand = on_regex(r"^(?i)iidx随个(?:dx|sd|标准)?[绿蓝黄红黑dps]*[0-9]+\+?")


@spec_rand.handle()
async def _(bot: Bot, event: Event, state: T_State):
    level_labels = ['绿', '蓝', '黄', '红', '黑','dp蓝', 'dp黄', 'dp红', 'dp黑','sp绿', 'sp蓝', 'sp黄', 'sp红', 'sp黑','sp','dp']

    regex = "iidx随个((?:dx|sd|标准))?([绿蓝黄红黑dps]*)([0-9]+\+?)"
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
            if level_index > 8:
                level_index = level_index - 9
            music_data = total_list.filter(level=level, diff=[level_index])
            if res.groups()[1] == 'dp':
                music_data = total_list.filter(level=level, diff=[5,6,7,8])
            elif res.groups()[1] == 'sp':
                music_data = total_list.filter(level=level, diff=[0,1,2,3,4])
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



sr = on_regex(r".*(?i)iidx.*什么")


@sr.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if random.randint(0,100) == 7:
        svcdnd = ['影子此时在打永劫无间因此拒绝了你的随机请求','这都要我随机是不是懒B','我随机出来了，但我不想告诉你','随机结果：向轮椅奔去 -1/-1/-1/-1','随机结果：冰！！！！！','Result:_EmpErr0R 获取结果失败','不知道','我没空，能不能自己随','猪B吧','影子绝赞溜冰中，故此决定拒绝你此次的请求，再求我一次我就告诉你']
        await sr.send(f"{random.choice(svcdnd)}")
    else:
        await sr.finish(song_txt(total_list.random())) 



search_music = on_regex(r"^(?i)iidx查歌.+")


@search_music.handle()
async def _(bot: Bot, event: Event, state: T_State):
    regex = "(?i)iidx查歌(.+)"
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
        
        
query_chart = on_regex(r"^([绿蓝黄红黑dps]*)iidx([0-9]+)")


@query_chart.handle()
async def _(bot: Bot, event: Event, state: T_State):
    regex = "([绿蓝黄红黑dps]*)iidx([0-9]+)"
    groups = re.match(regex, str(event.get_message())).groups()
    level_labels = ['绿', '蓝', '黄', '红', '黑','dp蓝', 'dp黄', 'dp红', 'dp黑','sp绿', 'sp蓝', 'sp黄', 'sp红', 'sp黑']
    if groups[0] != "":
        try:
            level_index = level_labels.index(groups[0])
            
            type = 'SP'
            name = groups[1]
            music = total_list.by_id(name)
            level = music['difficulty'][level_index]
            version = music['version']
            level_name_alt = ['BEGINNER', 'NORMAL', 'HYPER', 'ANOTHER', 'LEGGENDARIA']
            sid = name
            if level_index > 8:
                level_index = level_index - 9
            if level_index > 4:
                level_index_1 = level_index - 4
                type = 'DP'
            else:
                level_index_1 = level_index
            zero_note = ['-','-','-','-','-','-','-','-','-','-']
            if music['hell_charge_notes'] == []:
                music['hell_charge_notes'] = zero_note.copy()
            if music['charge_notes'] == []:
                music['charge_notes'] = zero_note.copy()
            if music['hell_backspin_scratches'] == []:
                music['hell_backspin_scratches'] = zero_note.copy()
            if music['backspin_scratches'] == []:
                music['backspin_scratches'] = zero_note.copy()
            await query_chart.send(f"{music['id']}.{music['title']} \n{type} {level_name_alt[level_index_1]} \n总物量：{music['notecounts'][level_index]}\nCS：{music['charge_notes'][level_index]}\nHCS：{music['hell_charge_notes'][level_index]}\nBS：{music['backspin_scratches'][level_index]}\nHBS：{music['hell_backspin_scratches'][level_index]}")
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


query_score = on_command('iidx分数线')


@query_score.handle()
async def _(bot: Bot, event: Event, state: T_State):
    r = "([绿蓝黄红黑dps]*)(iidx)?([0-9]+)"
    argv = str(event.get_message()).strip().split(" ")
    if len(argv) == 1 and argv[0] == '帮助':
        s = '''有他妈笨b
命令格式：iidx分数线 <难度+歌曲id> <分数线>
例如：iidx分数线 紫iidx799 AAA
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
            level_labels = ['绿', '蓝', '黄', '红', '黑','dp蓝', 'dp黄', 'dp红', 'dp黑','sp绿', 'sp蓝', 'sp黄', 'sp红', 'sp黑']

            level_index = level_labels.index(grp[0])
            if level_index > 8:
                level_index = level_index - 9
            chart_id = grp[2]
            if argv[1] == 'AAA' or argv[1] == 'aaa':
                line = float(8/9)
            elif argv[1] == 'AA' or argv[1] == 'aa':
                line = float(7/9)
            elif argv[1] == 'A' or argv[1] == 'a':
                line = float(6/9)
            elif argv[1] == 'B' or argv[1] == 'b':
                line = float(5/9)
            elif argv[1] == 'C' or argv[1] == 'c':
                line = float(4/9)
            elif argv[1] == 'D' or argv[1] == 'd':
                line = float(3/9)
            elif argv[1] == 'E' or argv[1] == 'e':
                line = float(2/9)
            elif argv[1] == 'F' or argv[1] == 'f':
                line = float(0)

            
            music = total_list.by_id(chart_id)

            level_name_alt = ['BEGINNER', 'NORMAL', 'HYPER', 'ANOTHER', 'LEGGENDARIA']
            type = 'SP'
            if level_index > 4:
                level_index_1 = level_index - 4
                type = 'DP'
            else:
                level_index_1 = level_index
                

            
            
            total_score = float(music.notecounts[level_index])
            
            


            await query_chart.send(f'''{music['title']} {type} {level_name_alt[level_index_1]}
分数线 {argv[1].upper()} 允许的最多 GREAT 数量为 {int(total_score * (1.0 - line) * 2)}(向下取整)，允许的最多GOOD和BAD以及POOR数量为 {int(total_score * (1.0 - line))}(向下取整)''')
        except Exception as e:
            print(e)
            await query_chart.send("快几把看看帮助吧哥哥（如果正常歌曲分数线出现错误，你的命令格式没出错并且你很确定bot的数据库中记录了这首歌的这个难度，请私聊作者）")

