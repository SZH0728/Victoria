# -*- coding:utf-8 -*-
# AUTHOR: Sun

from dataclasses import dataclass


@dataclass
class CountryState(object):
    """!
    @brief 州-国家关系数据类
    @details 记录单个州中国家所有权和管辖信息
    """
    state_name: str                     #!< 州名称
    country_tag: str                    #!< 国家标签（3字母代码）
    provinces: tuple[str, ...]          #!< 所属省份ID列表
    state_type: str | None              #!< 州类型（如"incorporated"、"unincorporated"等，可选）


@dataclass
class State(object):
    """!
    @brief 州数据容器类
    @details 存储州的基本信息和多国所有权关系
    """
    state_name: str                     #!< 州名称
    country: list[CountryState]         #!< 国家所有权列表（一个州可能有多个国家拥有）
    homeland: tuple[str, ...]           #!< 本土文化列表
    claim: tuple[str, ...]              #!< 宣称文化列表


@dataclass
class StatePlot(object):
    """!
    @brief 州绘图数据类
    @details 用于地图绘制的州数据，包含省份和文化信息
    """
    state_name: str                     #!< 州名称
    provinces: list[str]                #!< 省份ID列表
    homeland: list[str]                 #!< 本土文化列表
    claim: list[str]                    #!< 宣称文化列表


@dataclass
class StateAdjacency(object):
    """!
    @brief 州相邻关系数据类
    @details 记录一个州的所有相邻州，基于省份编号的临近性判断
    """
    state_name: str                     #!< 州名称
    adjacent_states: list[str]          #!< 相邻州名称列表


if __name__ == '__main__':
    pass