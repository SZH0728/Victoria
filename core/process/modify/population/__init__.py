# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package population
@brief 人口数据修改子模块
@details 提供人口数据的修改功能
"""

from typing import Type

from .base import PopulationModifyBase
from .merge import PopulationModifyMerge
from .generate import PopulationModifyGenerate

__all__ = [
    'PopulationModifyBase',
    'PopulationModifyMerge',
    'PopulationModifyGenerate',
    'POPULATION_MODIFY_LIST',
    'POPULATION_MODIFY_DEPENDENCY',
]

POPULATION_MODIFY_LIST: dict[str, Type[PopulationModifyBase]] = {
    'merge': PopulationModifyMerge,
    'generate': PopulationModifyGenerate,
}

POPULATION_MODIFY_DEPENDENCY: dict[str, tuple[str, ...]] = {
    'merge': ('population_merge',),
    'generate': ('population_merge',),
}

if __name__ == '__main__':
    pass
