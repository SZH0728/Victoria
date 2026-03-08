# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from abc import ABC, abstractmethod
from logging import getLogger

from pyradox import Tree, parse

from core.file import FileManager

logger = getLogger(__name__)


class AnalysisBase(ABC):
    def __init__(self):
        self.result: dict[str, Any] = {}
        self.ignore: set[str] = set()

    @staticmethod
    def get_stringify_value_from_tree(value: Any) -> Any:
        if isinstance(value, Tree):
            return str(value)

        return value

    @staticmethod
    def add_value_to_list_in_dict(dictionary: dict[str, Any], key: str, value: Any):
        if key not in dictionary:
            dictionary[key] = []

        dictionary[key].append(value)

    @staticmethod
    def add_value_to_dict_in_dict(dictionary: dict[str, Any], key: str, sub_key: Any, value: Any):
        if key not in dictionary:
            dictionary[key] = {}

        dictionary[key][sub_key] = value

    @staticmethod
    def verify_key_in_dictionary(dictionary: dict[str, Any], key: str, value: Any = None):
        if key not in dictionary:
            dictionary[key] = value

    def should_skip_file(self, filename: str) -> bool:
        """Check if the file should be skipped based on ignore list."""
        return filename in self.ignore

    def add_ignore_file(self, filename: str):
        """Add a filename to the ignore list."""
        self.ignore.add(filename)

    def remove_ignore_file(self, filename: str):
        """Remove a filename from the ignore list."""
        self.ignore.discard(filename)

    @abstractmethod
    def analysis(self, filename: str, tree: Tree):
        pass

    @staticmethod
    def modify_context(context: str) -> str:
        return context

    def main(self, manager: FileManager, group: str):
        for file, context in manager.read_files_in_range(group):
            if self.should_skip_file(file.name):
                logger.info(f"Skipping ignored file: {file.name}")
                continue

            tree: Tree = parse(self.modify_context(context))
            self.analysis(file.name, tree)


if __name__ == '__main__':
    pass
