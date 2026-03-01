# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package core.datatype
@brief 维多利亚3游戏数据类型定义模块
@details 提供游戏数据结构的类型定义，按类别组织在不同子模块中
"""

from .map import Map
from .region import RegionItem, Region
from .state import CountryState, State, StatePlot, StateAdjacency
from .building import (
    BuildingCountryOwnership,
    BuildingPrivateOwnership,
    BuildingCompanyOwnership,
    BuildingItem,
    BuildingNoOwnerItem,
    CountryBuilding,
    StateBuilding,
)
from .population import PopulationItem, CountryPopulation, RegionPopulation
from .definition import CountryDefinition
from .effect import CountryEffect
from .combination import DataCombination

__all__ = [
    # 容器类
    'Map',
    # 区域相关
    'RegionItem',
    'Region',
    # 州相关
    'CountryState',
    'State',
    'StatePlot',
    'StateAdjacency',
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
]

if __name__ == '__main__':
    pass