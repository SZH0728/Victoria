# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package state
@brief 州数据修改子模块
@details 提供州数据的修改功能
"""

from typing import Type

from .base import StateModifyBase
from .state import StateModifySingleStateCountry
from .merge import StateModifyRegionMerge
from .adjacent import StateModifyRegionAdjacent

__all__ = [
    'StateModifyBase',
    'StateModifySingleStateCountry',
    'StateModifyRegionMerge',
    'StateModifyRegionAdjacent',
    'STATE_MODIFY_LIST',
    'STATE_MODIFY_DEPENDENCY',
]

STATE_MODIFY_LIST: dict[str, Type[StateModifyBase]] = {
    'single_state_country': StateModifySingleStateCountry,
    'region_merge_country': StateModifyRegionMerge,
    'region_adjacent_country': StateModifyRegionAdjacent,
}

STATE_MODIFY_DEPENDENCY: dict[str, tuple[str, ...]] = {
    'default': (),
    'single_state_country': ('state_plot',),
    'region_merge_country': ('state_plot',),
    'region_adjacent_country': ('state_in_region_order',),
}

if __name__ == '__main__':
    pass
