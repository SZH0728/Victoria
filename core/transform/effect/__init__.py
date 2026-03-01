# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package effect
@brief 维多利亚3效果转换模块
@details 提供效果数据转换功能，包括抽象基类和默认实现
"""

from typing import Type

from .base import EffectTransformBase
from .default import EffectTransformDefault

__all__ = [
    'EffectTransformBase',
    'EffectTransformDefault',
    'EFFECT_TRANSFORM_LIST',
]

EFFECT_TRANSFORM_LIST: dict[str, Type[EffectTransformBase]] = {
    'default': EffectTransformDefault,
}

if __name__ == '__main__':
    pass
