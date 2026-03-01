# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any

from core.process.modify.effect.base import EffectModifyBase


class EffectModifyDefault(EffectModifyBase):
    def modify(self) -> Any:
        return self.origin.effect

if __name__ == '__main__':
    pass
