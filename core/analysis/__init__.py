# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package analysis
@brief 维多利亚3数据分析模块
@details 提供游戏数据的解析、提取和分析功能，包括州、区域、建筑和人口等数据的分析
"""

from .extract import KeyExtractionMixin
from .translate import TranslateAnalysis

# 导入子模块中的分析器基类和默认实现
from .state.base import StateAnalysisBase
from .state.default import StateAnalysisDefault
from .region.base import RegionAnalysisBase
from .region.default import RegionAnalysisDefault
from .building.base import BuildingAnalysisBase
from .building.default import BuildingAnalysisDefault
from .population.base import PopulationAnalysisBase
from .population.default import PopulationAnalysisDefault
from .definition.base import DefinitionAnalysisBase
from .definition.default import DefinitionAnalysisDefault
from .effect.base import EffectAnalysisBase
from .effect.default import EffectAnalysisDefault

__all__ = [
    # 工具类
    'KeyExtractionMixin',
    'TranslateAnalysis',
    # 州分析
    'StateAnalysisBase',
    'StateAnalysisDefault',
    # 区域分析
    'RegionAnalysisBase',
    'RegionAnalysisDefault',
    # 建筑分析
    'BuildingAnalysisBase',
    'BuildingAnalysisDefault',
    # 人口分析
    'PopulationAnalysisBase',
    'PopulationAnalysisDefault',
    # 国家定义分析
    'DefinitionAnalysisBase',
    'DefinitionAnalysisDefault',
    # 国家效果分析
    'EffectAnalysisBase',
    'EffectAnalysisDefault',
]

if __name__ == '__main__':
    pass
