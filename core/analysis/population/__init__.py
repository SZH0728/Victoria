# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package population
@brief 人口分析子模块
@details 提供人口数据的解析和分析功能
"""

from typing import Type

from .base import PopulationAnalysisBase
from .default import PopulationAnalysisDefault

__all__ = [
    'PopulationAnalysisBase',
    'PopulationAnalysisDefault',
    'POPULATION_ANALYSIS_LIST'
]

POPULATION_ANALYSIS_LIST: dict[str, Type[PopulationAnalysisBase]] = {
    'default': PopulationAnalysisDefault,
}

if __name__ == '__main__':
    pass
