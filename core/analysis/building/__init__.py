# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package building
@brief 建筑分析子模块
@details 提供建筑数据的解析和分析功能
"""

from typing import Type

from .base import BuildingAnalysisBase
from .default import BuildingAnalysisDefault

__all__ = [
    'BuildingAnalysisBase',
    'BuildingAnalysisDefault',
    'BUILDING_ANALYSIS_LIST',
]

BUILDING_ANALYSIS_LIST: dict[str, Type[BuildingAnalysisBase]] = {
    'default': BuildingAnalysisDefault,
}

if __name__ == '__main__':
    pass
