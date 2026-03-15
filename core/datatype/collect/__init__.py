# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 收集数据类模块包
@details 提供收集模块的数据类定义

此模块包含所有收集结果的数据类，用于存储建筑、人口、州等数据类型的收集统计结果。
"""

from core.datatype.collect.building import CollectBuildingStateItem, CollectBuildingStateResult
from core.datatype.collect.population import CollectPopulationStateItem, CollectPopulationResult
from core.datatype.collect.state import CollectStateItem, CollectStateResult

__all__ = [
    'CollectBuildingStateItem',
    'CollectBuildingStateResult',
    'CollectPopulationStateItem',
    'CollectPopulationResult',
    'CollectStateItem',
    'CollectStateResult',
]


if __name__ == '__main__':
    pass