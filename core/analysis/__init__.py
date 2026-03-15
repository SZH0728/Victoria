# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Type

from .base import AnalysisBase
from .building import AnalysisBuildingDefault
from .definition import AnalysisDefinitionDefault
from .effect import AnalysisEffectDefault
from .map import AnalysisMapDefault
from .population import AnalysisPopulationDefault
from .region import AnalysisRegionDefault
from .state import AnalysisStateDefault
from .translate import AnalysisTranslationDefault


ANALYSIS_REGISTER: dict[str, Type[AnalysisBase]] = {
    "AnalysisRegionDefault": AnalysisRegionDefault,
    "AnalysisMapDefault": AnalysisMapDefault,
    "AnalysisStateDefault": AnalysisStateDefault,
    "AnalysisPopulationDefault": AnalysisPopulationDefault,
    "AnalysisBuildingDefault": AnalysisBuildingDefault,
    "AnalysisEffectDefault": AnalysisEffectDefault,
    "AnalysisDefinitionDefault": AnalysisDefinitionDefault,
    "AnalysisTranslationDefault": AnalysisTranslationDefault,
}


if __name__ == '__main__':
    pass
