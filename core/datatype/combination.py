# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.datatype.combination
@brief 数据组合容器模块
@details 定义游戏所有数据的统一容器类，用于存储分析、转换过程中的数据
"""

from dataclasses import dataclass
from enum import Enum

from .map import Map
from .building import StateBuilding
from .definition import CountryDefinition
from .effect import CountryEffect
from .population import RegionPopulation
from .region import Region
from .state import State


@dataclass
class DataCombination(object):
    """!
    @brief 数据组合容器类
    @details 存储游戏所有类型数据的统一容器，用于框架各个阶段的数据传递
    """
    building: Map[StateBuilding] | None = None                #!< 建筑数据映射
    definition: Map[CountryDefinition] | None = None          #!< 国家定义数据映射
    effect: Map[CountryEffect] | None = None                  #!< 国家效果数据映射
    population: Map[RegionPopulation] | None = None           #!< 人口数据映射
    region: Region | None = None                              #!< 区域数据
    state: Map[State] | None = None                           #!< 州数据映射

    english_translation: Map[str] | None = None               #!< 英文翻译映射
    chinese_translation: Map[str] | None = None               #!< 中文翻译映射
    map: Map[int] | None = None
    tag: Map[str] | None = None                               #!< 标签映射（用于翻译更新）


class DataGenerateType(Enum):
    default = 0
    randomize = 1
    fix = 2


if __name__ == '__main__':
    pass