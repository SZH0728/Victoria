# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any

from core.process.modify.definition.base import DefinitionModifyBase


class DefinitionModifyDefault(DefinitionModifyBase):
    def modify(self) -> Any:
        return self.origin.definition

if __name__ == '__main__':
    pass
