# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief structure模块
@details 源数据→结构化数据转换模块，将analysis模块的输出重新组织为以国家/标识符为键的结构化数据
"""

from typing import Type

from ..base import StructureBase
from .building import StructureBuildingDefault
from .definition import StructureDefinitionDefault
from .effect import StructureEffectDefault
from .map import StructureMapDefault
from .population import StructurePopulationDefault
from .region import StructureRegionDefault
from .state import StructureStateDefault


STRUCTURE_REGISTER: dict[str, Type[StructureBase]] = {
    "StructureRegionDefault": StructureRegionDefault,
    "StructureMapDefault": StructureMapDefault,
    "StructureStateDefault": StructureStateDefault,
    "StructurePopulationDefault": StructurePopulationDefault,
    "StructureBuildingDefault": StructureBuildingDefault,
    "StructureEffectDefault": StructureEffectDefault,
    "StructureDefinitionDefault": StructureDefinitionDefault,
}


if __name__ == '__main__':
    pass
