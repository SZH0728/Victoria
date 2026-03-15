# -*- coding:utf-8 -*-
# AUTHOR: Sun

from core.args import ArgsManager

if __name__ == '__main__':
    arg: ArgsManager = ArgsManager()

    arg.add('frame.analysis', 'enabled_analysis_type', ('building', 'definition', 'effect', 'map', 'population', 'region', 'state', 'translation'))

    arg.add('frame.analysis.map', 'name', 'AnalysisMapDefault')
    arg.add('frame.analysis.map', 'index', 1000)

    arg.add('frame.analysis.region', 'name', 'AnalysisRegionDefault')
    arg.add('frame.analysis.region', 'index', 2000)

    arg.add('frame.analysis.state', 'name', 'AnalysisStateDefault')
    arg.add('frame.analysis.state', 'index', 3000)

    arg.add('frame.analysis.population', 'name', 'AnalysisPopulationDefault')
    arg.add('frame.analysis.population', 'index', 4000)

    arg.add('frame.analysis.building', 'name', 'AnalysisBuildingDefault')
    arg.add('frame.analysis.building', 'index', 5000)

    arg.add('frame.analysis.definition', 'name', 'AnalysisDefinitionDefault')
    arg.add('frame.analysis.definition', 'index', 6000)

    arg.add('frame.analysis.effect', 'name', 'AnalysisEffectDefault')
    arg.add('frame.analysis.effect', 'index', 7000)

    arg.add('frame.analysis.translation', 'name', 'AnalysisTranslationDefault')
    arg.add('frame.analysis.translation', 'index', 8000)
