# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief middleware模块
@details 提供数据结构的双向转换功能，包括structure（源数据→结构化数据）和destructure（结构化数据→源数据）两个子模块
"""

from . import structure, destructure
from .base import StructureBase, DestructureBase
from .structure import STRUCTURE_REGISTER
from .destructure import DESTRUCTURE_REGISTER


MIDDLEWARE_REGISTER: dict[str, dict[str, type]] = {
    "structure": STRUCTURE_REGISTER,
    "destructure": DESTRUCTURE_REGISTER,
}


if __name__ == '__main__':
    pass
