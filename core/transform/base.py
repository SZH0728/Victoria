# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from abc import ABC, abstractmethod
from logging import getLogger

from pyradox import Tree

from core.file import FileManager

logger = getLogger(__name__)


class TransformBase(ABC):
    def __init__(self):
        self.result: dict[str, Any] = {}

    @abstractmethod
    def transform(self, target: Any) -> Tree:
        pass

    def main(self, manager: FileManager, group: str, target: dict[str, Any]):
        for key, value in target.items():
            tree = self.transform(value)
            manager.write_file(group, key, str(tree))


if __name__ == '__main__':
    pass