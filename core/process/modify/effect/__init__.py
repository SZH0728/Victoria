# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@package effect
@brief 国家效果修改子模块
@details 提供国家效果数据的修改功能
"""

from typing import Type

from .base import EffectModifyBase
from .default import EffectModifyDefault
from .empty import EffectModifyEmpty
from .randomize import EffectModifyRandomize

__all__ = [
    'EffectModifyBase',
    'EffectModifyDefault',
    'EffectModifyEmpty',
    'EffectModifyRandomize',
    'EFFECT_MODIFY_LIST',
    'EFFECT_MODIFY_DEPENDENCY',
]

EFFECT_MODIFY_LIST: dict[str, Type[EffectModifyBase]] = {
    'default': EffectModifyDefault,
    'empty': EffectModifyEmpty,
    'randomize': EffectModifyRandomize,
}

EFFECT_MODIFY_DEPENDENCY: dict[str, tuple[str, ...]] = {
    'default': (),
    'empty': (),
    'randomize': (),
}

if __name__ == '__main__':
    pass
