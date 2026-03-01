# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package building
@brief 建筑数据修改子模块
@details 提供建筑数据的修改功能
"""

from typing import Type

from .base import BuildingModifyBase
from .default import BuildingModifyDefault
from .empty import BuildingModifyEmpty

__all__ = [
    'BuildingModifyBase',
    'BuildingModifyDefault',
    'BUILDING_MODIFY_LIST',
    'BUILDING_MODIFY_DEPENDENCY',
]

BUILDING_MODIFY_LIST: dict[str, Type[BuildingModifyBase]] = {
    'default': BuildingModifyDefault,
    'empty': BuildingModifyEmpty,
}

BUILDING_MODIFY_DEPENDENCY: dict[str, tuple[str, ...]] = {
    'default': (),
    'empty': (),
}

if __name__ == '__main__':
    pass
