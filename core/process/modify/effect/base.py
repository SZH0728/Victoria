# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any

from core.process.modify.base import ModifyBase, DataType


class EffectModifyBase(ModifyBase):
    def abstract_modify(self) -> tuple[DataType, Any]:
        return DataType.effect, self.modify()

if __name__ == '__main__':
    pass
