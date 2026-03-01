# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package population
@brief 人口数据修改子模块
@details 提供人口数据的修改功能
"""

from typing import Type

from .base import PopulationModifyBase
from .default import PopulationModifyDefault
from .merge import PopulationModifyMerge

__all__ = [
    'PopulationModifyBase',
    'PopulationModifyDefault',
    'PopulationModifyMerge',
    'POPULATION_MODIFY_LIST',
    'POPULATION_MODIFY_DEPENDENCY',
]

POPULATION_MODIFY_LIST: dict[str, Type[PopulationModifyBase]] = {
    'default': PopulationModifyDefault,
    'merge': PopulationModifyMerge,
}

POPULATION_MODIFY_DEPENDENCY: dict[str, tuple[str, ...]] = {
    'default': (),
    'merge': ('population_merge',),
}

if __name__ == '__main__':
    pass
