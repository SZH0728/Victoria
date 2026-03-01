# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package transform
@brief 维多利亚3数据转换模块
@details 提供游戏数据结构的序列化与转换功能，将分析结果转换回游戏可读的格式
"""

# 导入子模块中的转换器基类和默认实现
from .population import PopulationTransformBase, PopulationTransformDefault
from .building.base import BuildingTransformBase
from .building.default import BuildingTransformDefault
from .state.base import StateTransformBase
from .state.default import StateTransformDefault

__all__ = [
    # 人口转换
    'PopulationTransformBase',
    'PopulationTransformDefault',
    # 建筑转换
    'BuildingTransformBase',
    'BuildingTransformDefault',
    # 州转换
    'StateTransformBase',
    'StateTransformDefault',
]

if __name__ == '__main__':
    pass
