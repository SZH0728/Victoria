# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package core
@brief 维多利亚3数据分析和转换核心模块
@details 提供游戏数据结构的类型定义、文件管理和分析转换框架
"""

from .datatype import (
    Map,
    RegionItem,
    Region,
    CountryState,
    State,
    BuildingCountryOwnership,
    BuildingPrivateOwnership,
    BuildingCompanyOwnership,
    BuildingItem,
    BuildingNoOwnerItem,
    CountryBuilding,
    StateBuilding,
    PopulationItem,
    CountryPopulation,
    RegionPopulation,
    CountryDefinition,
    CountryEffect,
    DataCombination,
)

from .file import FileManager, GroupType, GroupItem, Group

__all__ = [
    # 容器类
    'Map',
    # 区域相关
    'RegionItem',
    'Region',
    # 州相关
    'CountryState',
    'State',
    # 建筑相关
    'BuildingCountryOwnership',
    'BuildingPrivateOwnership',
    'BuildingCompanyOwnership',
    'BuildingItem',
    'BuildingNoOwnerItem',
    'CountryBuilding',
    'StateBuilding',
    # 人口相关
    'PopulationItem',
    'CountryPopulation',
    'RegionPopulation',
    # 国家定义
    'CountryDefinition',
    # 国家效果
    'CountryEffect',
    # 数据组合
    'DataCombination',
    # 文件管理
    'FileManager',
    'GroupType',
    'GroupItem',
    'Group',
]

if __name__ == '__main__':
    pass
