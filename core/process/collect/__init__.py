# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Type

from .base import CollectBase
from .plot import StatePlotCollect
from .region import StateInRegionOrder
from .population import PopulationMergeCollect

__all__ = [
    'CollectBase',
    'StatePlotCollect',
    'StateInRegionOrder',
    'PopulationMergeCollect',
    'COLLECT_LIST',
    'COLLECT_DEPENDENCY',
]

COLLECT_LIST: dict[str, Type[CollectBase]] = {
    'state_plot': StatePlotCollect,
    'state_in_region_order': StateInRegionOrder,
    'population_merge': PopulationMergeCollect,
}

COLLECT_DEPENDENCY: dict[str, tuple[str, ...]] = {
    'state_plot': (),
    'state_in_region_order': (),
    'population_merge': (),
}

if __name__ == '__main__':
    pass
