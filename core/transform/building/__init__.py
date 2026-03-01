# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package building
@brief 建筑转换子模块
@details 提供建筑数据的序列化和转换功能
"""

from typing import Type

from .base import BuildingTransformBase
from .default import BuildingTransformDefault

__all__ = [
    'BuildingTransformBase',
    'BuildingTransformDefault',
    'BUILDING_TRANSFORM_LIST'
]

BUILDING_TRANSFORM_LIST: dict[str, Type[BuildingTransformBase]] = {
    'default': BuildingTransformDefault,
}

if __name__ == '__main__':
    pass
