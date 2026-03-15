# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief destructure模块
@details 结构化数据→源数据转换模块，将结构化数据转换回transform模块可处理的源数据格式
"""

from typing import Type

from ..base import DestructureBase
from .building import DestructureBuildingDefault
from .definition import DestructureDefinitionDefault
from .effect import DestructureEffectDefault
from .map import DestructureMapDefault
from .population import DestructurePopulationDefault
from .region import DestructureRegionDefault
from .state import DestructureStateDefault


DESTRUCTURE_REGISTER: dict[str, Type[DestructureBase]] = {
    "DestructureRegionDefault": DestructureRegionDefault,
    "DestructureMapDefault": DestructureMapDefault,
    "DestructureStateDefault": DestructureStateDefault,
    "DestructurePopulationDefault": DestructurePopulationDefault,
    "DestructureBuildingDefault": DestructureBuildingDefault,
    "DestructureEffectDefault": DestructureEffectDefault,
    "DestructureDefinitionDefault": DestructureDefinitionDefault,
}


if __name__ == '__main__':
    pass
