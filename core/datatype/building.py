# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.datatype.building
@brief 建筑数据类模块
@details 定义游戏建筑所有权和层级结构的数据类
"""

from dataclasses import dataclass


@dataclass
class BuildingCountryOwnership(object):
    """!
    @brief 建筑国家所有权数据类
    @details 记录建筑由国家直接拥有的信息
    """
    country: str                     #!< 国家标签（3字母代码）
    level: int                       #!< 建筑等级


@dataclass
class BuildingPrivateOwnership(object):
    """!
    @brief 建筑私人所有权数据类
    @details 记录建筑由私人（资本家）拥有的信息
    """
    building: str                    #!< 建筑类型
    country: str                     #!< 国家标签（3字母代码）
    level: int                       #!< 建筑等级
    region: str                      #!< 所属区域


@dataclass
class BuildingCompanyOwnership(object):
    """!
    @brief 建筑公司所有权数据类
    @details 记录建筑由公司拥有的信息
    """
    company: str                     #!< 公司名称
    country: str                     #!< 国家标签（3字母代码）
    level: int                       #!< 建筑等级


@dataclass
class BuildingItem(object):
    """!
    @brief 建筑项数据类
    @details 存储单个建筑的完整信息，包括所有权、补贴、储备和生产方法
    """
    building: str                    #!< 建筑类型
    ownership: tuple[BuildingCountryOwnership|BuildingPrivateOwnership|BuildingCompanyOwnership, ...]  #!< 所有权列表
    subsidized: str | None           #!< 补贴状态（如"yes"，可选）
    reserve: int | None              #!< 建筑储备（可选）
    methods: tuple[str, ...]         #!< 生产方法列表


@dataclass
class BuildingNoOwnerItem(object):
    """!
    @brief 无所有者建筑项数据类
    @details 记录没有明确所有者的建筑信息
    """
    building: str                    #!< 建筑类型
    level: int                       #!< 建筑等级


@dataclass
class CountryBuilding(object):
    """!
    @brief 国家建筑数据类
    @details 存储单个国家拥有的所有建筑信息
    """
    country_tag: str                     #!< 国家标签（3字母代码）
    buildings: tuple[BuildingItem|BuildingNoOwnerItem, ...]  #!< 建筑项列表


@dataclass
class StateBuilding(object):
    """!
    @brief 州建筑数据类
    @details 存储单个州中所有国家的建筑信息
    """
    state: str                         #!< 州名称
    country: tuple[CountryBuilding, ...]  #!< 国家建筑列表


if __name__ == '__main__':
    pass