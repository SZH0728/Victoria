# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package definition
@brief 国家定义修改子模块
@details 提供国家定义数据的修改功能
"""

from typing import Type

from .base import DefinitionModifyBase
from .generate import DefinitionModifyGenerate

__all__ = [
    'DefinitionModifyBase',
    'DefinitionModifyGenerate',
    'DEFINITION_MODIFY_LIST',
    'DEFINITION_MODIFY_DEPENDENCY',
]

DEFINITION_MODIFY_LIST: dict[str, Type[DefinitionModifyBase]] = {
    'generate': DefinitionModifyGenerate,
}

DEFINITION_MODIFY_DEPENDENCY: dict[str, tuple[str, ...]] = {
    'generate': (),
}

if __name__ == '__main__':
    pass
