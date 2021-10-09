import json
import random
from typing import Dict, List, Optional, Union, Tuple, Any
from copy import deepcopy

import requests


def cross(checker: List[Any], elem: Optional[Union[Any, List[Any]]], diff):
    ret = False
    diff_ret = []
    if not elem or elem is Ellipsis:
        return True, diff
    if isinstance(elem, List):
        for _j in (range(len(checker)) if diff is Ellipsis else diff):
            if _j >= len(checker):
                continue
            __e = checker[_j]
            if __e in elem:
                diff_ret.append(_j)
                ret = True
    elif isinstance(elem, Tuple):
        for _j in (range(len(checker)) if diff is Ellipsis else diff):
            if _j >= len(checker):
                continue
            __e = checker[_j]
            if elem[0] <= __e <= elem[1]:
                diff_ret.append(_j)
                ret = True
    else:
        for _j in (range(len(checker)) if diff is Ellipsis else diff):
            if _j >= len(checker):
                continue
            __e = checker[_j]
            if elem == __e:
                return True, [_j]
    return ret, diff_ret


def in_or_equal(checker: Any, elem: Optional[Union[Any, List[Any]]]):
    if elem is Ellipsis:
        return True
    if isinstance(elem, List):
        return checker in elem
    elif isinstance(elem, Tuple):
        return elem[0] <= checker <= elem[1]
    else:
        return checker == elem






class Music(Dict):
    id: Optional[str] = None
    title: Optional[str] = None
    bpm: Optional[str] = None
    version: Optional[str] = None
    difficulty: Optional[List] = None
    artist: Optional[str] = None
    long: Optional[List] = None
    chara: Optional[str] = None
    diff: List[int] = []
    

    def __getattribute__(self, item):
        if item in self:
            return self[item]
        return super().__getattribute__(item)
    




class MusicList(List[Music]):
    def by_id(self, music_id: str) -> Optional[Music]:
        for music in self:
            if str(music.id) == music_id:
                return music
        return None

    def by_title(self, music_title: str) -> Optional[Music]:
        for music in self:
            if music.title == music_title:
                return music
        return None
        
    def by_author(self, music_author: str) -> Optional[Music]:
        for music in self:
            if music.artist == music_author:
                return music
        return None

    def random(self):
        return random.choice(self)
    
    
    def filter(self,
               *,
               level: Optional[Union[str, List[str]]] = ...,
               title_search: Optional[str] = ...,
               author_search: Optional[str] = ...,
               type: Optional[Union[str, List[str]]] = ...,
               diff: List[int] = ...,
               ):
        new_list = MusicList()
        for music in self:
            diff2 = diff
            music = deepcopy(music)
            placeholder: [str] = '-'
            level_temp = music.difficulty
            #if type == 'sp':
            #    level_temp = music.difficulty[0,5]
            #elif type == 'dp':
            #    level_temp = music.difficulty[5,]
            #    diff2 = diff2 - 1
            ret, diff2 = cross(level_temp, level, diff2)
            if not ret:
                continue
            if title_search is not Ellipsis and title_search.lower() not in music.title.lower():
                continue
            if author_search is not Ellipsis and author_search.lower() not in music.artist.lower():
                continue
            music.diff = diff2
            new_list.append(music)
        return new_list




with open("popn.json",'rb') as iidx:
    obj = json.load(iidx)
total_list: MusicList = MusicList(obj)
try:
    for __i in range(len(total_list)):
        total_list[__i] = Music(total_list[__i])

except KeyError: 
        print(total_list[__i].difficulty)
