# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package state
@brief 州转换子模块
@details 提供州数据的序列化和转换功能
"""

from typing import Type

from .base import StateTransformBase
from .default import StateTransformDefault

__all__ = [
    'StateTransformBase',
    'StateTransformDefault',
    'STATE_TRANSFORM_LIST'
]

STATE_TRANSFORM_LIST: dict[str, Type[StateTransformBase]] = {
    'default': StateTransformDefault,
}

if __name__ == '__main__':
    pass
