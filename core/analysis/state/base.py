# -*- coding:utf-8 -*-
# AUTHOR: Sun

from abc import ABC, abstractmethod
from logging import getLogger

from pyradox import Tree, parse

from core.file import FileManager
from core.datatype import StateMap, State

logger = getLogger(__name__)


class StateAnalysisBase(ABC):
    def __init__(self):
        self.state = StateMap()

    @staticmethod
    def get_state_name_by_key(name: str):
        return name.replace('s:STATE_', '').lower()

    @staticmethod
    def get_country_tag_by_key(tag: str):
        return tag.replace('c:', '')

    @abstractmethod
    def analysis(self, tree: Tree, state_name: str) -> State:
        pass

    def main(self, manager: FileManager, group: str):
        for _, content in manager.read_files_in_range(group):
            tree = parse(content)

            for state_name, state_definition in tree['STATES'].items():
                state_name = self.get_state_name_by_key(state_name)
                state = self.analysis(state_definition, state_name)

                self.state[state_name] = state


if __name__ == '__main__':
    pass
