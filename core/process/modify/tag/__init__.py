# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package tag
@brief 标签数据修改子模块
@details 提供标签数据的修改功能
"""

from typing import Type

from .default import TagModifyDefault
from .base import TagModifyBase

__all__ = [
    'TagModifyBase',
    'TagModifyDefault',
    'TAG_MODIFY_LIST',
    'TAG_MODIFY_DEPENDENCY',
]

TAG_MODIFY_LIST: dict[str, Type[TagModifyBase]] = {
    'default': TagModifyDefault,
}

TAG_MODIFY_DEPENDENCY: dict[str, tuple[str, ...]] = {
    'default': (),
}

if __name__ == '__main__':
    pass