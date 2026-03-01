# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any

from core.process.modify.population.base import PopulationModifyBase


class PopulationModifyDefault(PopulationModifyBase):
    def modify(self) -> Any:
        return self.origin.population

if __name__ == '__main__':
    pass
