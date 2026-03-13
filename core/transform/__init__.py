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


TRANSFORM_REGISTER: dict[str, tuple[int, Type[TransformBase]]] = {
    "TransformRegionDefault": (1000, TransformRegionDefault),
    "TransformMapDefault": (2000, TransformMapDefault),
    "TransformStateDefault": (3000, TransformStateDefault),
    "TransformPopulationDefault": (4000, TransformPopulationDefault),
    "TransformBuildingDefault": (5000, TransformBuildingDefault),
    "TransformEffectDefault": (6000, TransformEffectDefault),
    "TransformDefinitionDefault": (7000, TransformDefinitionDefault),
    "TransformTranslationDefault": (8000, TransformTranslationDefault)
}


if __name__ == '__main__':
    pass
