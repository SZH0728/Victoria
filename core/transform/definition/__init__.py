# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package definition
@brief 国家定义转换子模块
@details 提供国家定义数据的序列化和转换功能
"""

from typing import Type

from .base import DefinitionTransformBase
from .default import DefinitionTransformDefault

__all__ = [
    'DefinitionTransformBase',
    'DefinitionTransformDefault',
    'DEFINITION_TRANSFORM_LIST',
]

DEFINITION_TRANSFORM_LIST: dict[str, Type[DefinitionTransformBase]] = {
    'default': DefinitionTransformDefault,
}

if __name__ == '__main__':
    pass
