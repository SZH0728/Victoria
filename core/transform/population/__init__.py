# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package population
@brief 维多利亚3人口转换模块
@details 提供人口数据转换功能，包括抽象基类和默认实现
"""

from typing import Type

from .base import PopulationTransformBase
from .default import PopulationTransformDefault

__all__ = [
    'PopulationTransformBase',
    'PopulationTransformDefault',
    'POPULATION_TRANSFORM_LIST',
]

POPULATION_TRANSFORM_LIST: dict[str, Type[PopulationTransformBase]] = {
    'default': PopulationTransformDefault,
}

if __name__ == '__main__':
    pass
