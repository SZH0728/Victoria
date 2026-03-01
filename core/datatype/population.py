# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.datatype.population
@brief 人口数据类模块
@details 定义游戏人口数据结构，包括人口项、国家人口和区域人口
"""

from dataclasses import dataclass


@dataclass
class PopulationItem(object):
    """!
    @brief 人口项数据类
    @details 存储单个人口群体的基本信息
    """
    size: int                       #!< 人口数量

    culture: str | None             #!< 文化（可选）
    religion: str | None            #!< 宗教（可选）
    population_type: str | None     #!< 人口类型（如"laborers"、"farmers"等，可选）


@dataclass
class CountryPopulation(object):
    """!
    @brief 国家人口数据类
    @details 存储单个国家的人口信息
    """
    country_tag: str                     #!< 国家标签（3字母代码）
    population: tuple[PopulationItem, ...]  #!< 人口项列表


@dataclass
class RegionPopulation(object):
    """!
    @brief 区域人口数据类
    @details 存储单个区域（战略区域）的人口信息
    """
    region: str                         #!< 区域名称
    population: tuple[CountryPopulation, ...]  #!< 国家人口列表


if __name__ == '__main__':
    pass