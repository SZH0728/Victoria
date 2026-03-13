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


ANALYSIS_REGISTER: dict[str, tuple[int, Type[AnalysisBase]]] = {
    "AnalysisRegionDefault": (1000, AnalysisRegionDefault),
    "AnalysisMapDefault": (2000, AnalysisMapDefault),
    "AnalysisStateDefault": (3000, AnalysisStateDefault),
    "AnalysisPopulationDefault": (4000, AnalysisPopulationDefault),
    "AnalysisBuildingDefault": (5000, AnalysisBuildingDefault),
    "AnalysisEffectDefault": (6000, AnalysisEffectDefault),
    "AnalysisDefinitionDefault": (7000, AnalysisDefinitionDefault),
    "AnalysisTranslationDefault": (8000, AnalysisTranslationDefault)
}

ANALYSIS_GROUP_NAME: dict[Type[AnalysisBase], str] = {
    AnalysisRegionDefault: "region",
    AnalysisMapDefault: "map",
    AnalysisStateDefault: "state",
    AnalysisPopulationDefault: "population",
    AnalysisBuildingDefault: "building",
    AnalysisEffectDefault: "effect",
    AnalysisDefinitionDefault: "definition",
    AnalysisTranslationDefault: "translation"
}


if __name__ == '__main__':
    pass
