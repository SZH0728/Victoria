# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package state
@brief 州数据修改子模块
@details 提供州数据的修改功能
"""

from typing import Type

from .base import StateModifyBase
from .default import StateModifyDefault
from .state import StateModifySingleStateCountry
from .merge import StateModifyRegionMerge

__all__ = [
    'StateModifyBase',
    'StateModifyDefault',
    'StateModifySingleStateCountry',
    'StateModifyRegionMerge',
    'STATE_MODIFY_LIST',
    'STATE_MODIFY_DEPENDENCY',
]

STATE_MODIFY_LIST: dict[str, Type[StateModifyBase]] = {
    'default': StateModifyDefault,
    'single_state_country': StateModifySingleStateCountry,
    'region_merge_country': StateModifyRegionMerge,
}

STATE_MODIFY_DEPENDENCY: dict[str, tuple[str, ...]] = {
    'default': (),
    'single_state_country': ('state_plot',),
    'region_merge_country': ('state_plot',),
}

if __name__ == '__main__':
    pass
