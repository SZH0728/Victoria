# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package analysis.definition
@brief 国家定义分析模块
@details 提供国家定义数据的解析和分析功能，包括国家标签、颜色、等级、文化、首都等信息的提取
"""

from typing import Type

from .base import DefinitionAnalysisBase
from .default import DefinitionAnalysisDefault

__all__ = [
    'DefinitionAnalysisBase',
    'DefinitionAnalysisDefault',
    'DEFINITION_ANALYSIS_LIST',
]

DEFINITION_ANALYSIS_LIST: dict[str, Type[DefinitionAnalysisBase]] = {
    'default': DefinitionAnalysisDefault,
}

if __name__ == '__main__':
    pass