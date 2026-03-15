# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Type

from .base import TransformBase
from .building import TransformBuildingDefault
from .definition import TransformDefinitionDefault
from .effect import TransformEffectDefault
from .map import TransformMapDefault
from .population import TransformPopulationDefault
from .region import TransformRegionDefault
from .state import TransformStateDefault
from .translate import TransformTranslationDefault


TRANSFORM_REGISTER: dict[str, Type[TransformBase]] = {
    "TransformRegionDefault": TransformRegionDefault,
    "TransformMapDefault": TransformMapDefault,
    "TransformStateDefault": TransformStateDefault,
    "TransformPopulationDefault": TransformPopulationDefault,
    "TransformBuildingDefault": TransformBuildingDefault,
    "TransformEffectDefault": TransformEffectDefault,
    "TransformDefinitionDefault": TransformDefinitionDefault,
    "TransformTranslationDefault": TransformTranslationDefault,
}


if __name__ == '__main__':
    pass
