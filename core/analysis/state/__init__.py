# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package state
@brief 州分析子模块
@details 提供州数据的解析和分析功能
"""

from typing import Type

from .base import StateAnalysisBase
from .default import StateAnalysisDefault

__all__ = [
    'StateAnalysisBase',
    'StateAnalysisDefault',
    'STATE_ANALYSIS_LIST'
]

STATE_ANALYSIS_LIST: dict[str, Type[StateAnalysisBase]] = {
    'default': StateAnalysisDefault,
}

if __name__ == '__main__':
    pass
