# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any

from core.process.modify.building.base import BuildingModifyBase


class BuildingModifyDefault(BuildingModifyBase):
    def modify(self) -> Any:
        return self.origin.building

if __name__ == '__main__':
    pass
