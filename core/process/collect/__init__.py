# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Type

from .base import CollectBase
from .plot import StatePlotCollect
from .population import PopulationMergeCollect

__all__ = [
    'CollectBase',
    'StatePlotCollect',
    'PopulationMergeCollect',
    'COLLECT_LIST',
    'COLLECT_DEPENDENCY',
]

COLLECT_LIST: dict[str, Type[CollectBase]] = {
    'state_plot': StatePlotCollect,
    'population_merge': PopulationMergeCollect,
}

COLLECT_DEPENDENCY: dict[str, tuple[str, ...]] = {
    'state_plot': (),
    'population_merge': (),
}

if __name__ == '__main__':
    pass
