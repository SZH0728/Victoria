# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package analysis.effect
@brief 国家效果分析模块
@details 提供国家效果数据的解析和分析功能，包括国家标签、国家名称、效果和特殊效果信息的提取
"""

from typing import Type

from .base import EffectAnalysisBase
from .default import EffectAnalysisDefault

__all__ = [
    'EffectAnalysisBase',
    'EffectAnalysisDefault',
    'EFFECT_ANALYSIS_LIST',
]

EFFECT_ANALYSIS_LIST: dict[str, Type[EffectAnalysisBase]] = {
    'default': EffectAnalysisDefault,
}

if __name__ == '__main__':
    pass