# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package region
@brief 区域分析模块
@details 提供战略区域分析功能，包括基础数据结构和分析器实现
"""

from typing import Type

from .base import RegionAnalysisBase
from .default import RegionAnalysisDefault

__all__ = [
    'RegionAnalysisBase',
    'RegionAnalysisDefault',
    'REGION_ANALYSIS_LIST'
]

REGION_ANALYSIS_LIST: dict[str, Type[RegionAnalysisBase]] = {
    'default': RegionAnalysisDefault,
}

if __name__ == '__main__':
    pass
