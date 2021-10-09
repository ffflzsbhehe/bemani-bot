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



class Chart(Dict):
   
    effected_by: Optional[str] = None
    illustrator: Optional[str] = None
    difnum: Optional[str] = None

    def __getattribute__(self, item):
        if item == 'illustrator':
            return self['illustrator']
        elif item == 'effected_by':
            return self['effected_by']
        elif item == 'difnum':
            return self['difnum']
        return super().__getattribute__(item)


class Music(Dict):
    id: Optional[str] = None
    title_name: Optional[str] = None
    bpm_max: Optional[float] = None
    bpm_min: Optional[float] = None
    version: Optional[str] = None
    difficulty: Optional[Chart] = None
    distribution_date: Optional[str] = None
    artist_name: Optional[str] = None
    inf_ver: Optional[str] = None
    diff: List[int] = []
    

    def __getattribute__(self, item):
        if item in {'artist_name', 'title_name','distribution_date', 'bpm_max','bpm_min', 'version','inf_ver'}:
            return self['info'][item]
        elif item in self:
            return self[item]
        return super().__getattribute__(item)
    




class MusicList(List[Music]):
    def by_id(self, music_id: str) -> Optional[Music]:
        for music in self:
            if music.id == music_id:
                return music
        return None

    def by_title(self, music_title: str) -> Optional[Music]:
        for music in self:
            if music.title_name == music_title:
                return music
        return None
        
    def by_author(self, music_author: str) -> Optional[Music]:
        for music in self:
            if music.artist_name == music_author:
                return music
        return None

    def random(self):
        return random.choice(self)
    
    
    def filter(self,
               *,
               level: Optional[Union[str, List[str]]] = ...,
               title_search: Optional[str] = ...,
               author_search: Optional[str] = ...,
               diff: List[int] = ...,
               ):
        new_list = MusicList()
        for music in self:
            diff2 = diff
            music = deepcopy(music)
            leveltemp: List[str] = []
            placeholder: [str] = '-'
            for i in range(0,len(music.difficulty)):
                if music.difficulty[i]['difnum'] == '0':
                    leveltemp.append(placeholder)
                else:
                    leveltemp.append(music.difficulty[i]['difnum'])
            ret, diff2 = cross(leveltemp, level, diff2)
            if not ret:
                continue
            if title_search is not Ellipsis and title_search.lower() not in music.title_name.lower():
                continue
            if author_search is not Ellipsis and author_search.lower() not in music.artist_name.lower():
                continue
            music.diff = diff2
            new_list.append(music)
        return new_list


class Chain(Dict):
    title_name: Optional[str] = None
    novice: Optional[str] = None
    advanced: Optional[str] = None
    exhaust: Optional[str] = None
    maximum: Optional[str] = None
    infinity: Optional[str] = None
    
    def __getattribute__(self, item):
        if item in self:
            return self[item]
        return super().__getattribute__(item)

class ChainList(List[Chain]):
    
    def by_title(self, music_title: str,difnum: str) -> Optional[Chain]:
        music_title = music_title.replace(" ", "_")
        for chain in self:
            if chain['title_name'] == music_title:
                if difnum == 'novice':
                    return chain['novice']
                elif difnum == 'advanced':
                    return chain['advanced']
                elif difnum == 'exhaust':
                    return chain['exhaust']
                elif difnum == 'infinity':
                    return chain['infinity']
                elif difnum == 'maximum':
                    return chain['maximum']
                
        return None

with open("sdvx.json",'rb') as sdvx:
    obj = json.load(sdvx)
with open("sdvx_chain.json",'rb') as sdvx_chain:
    obj_c = json.load(sdvx_chain)
chain_list: ChainList = ChainList(obj_c)
total_list: MusicList = MusicList(obj)
try:
    for __i in range(len(total_list)):
        total_list[__i] = Music(total_list[__i])
        for __j in range(len(total_list[__i].difficulty)):
            total_list[__i].difficulty[__j] = Chart(total_list[__i].difficulty[__j])
except KeyError: 
        print(total_list[__i].difficulty)
