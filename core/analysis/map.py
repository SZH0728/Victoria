# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from pyradox import Tree, parse

from core.datatype import Map
from core.analysis import KeyExtractionMixin

logger = getLogger(__name__)


class MapAnalysis(KeyExtractionMixin):
    def __init__(self):
        self.map: Map[int] = Map()

    def main(self, manager: FileManager, group: str):
        for _, content in manager.read_files_in_range(group):
            tree: Tree = parse(content)

            for state_name, state_definition in tree.items():
                state_name = self.extract_state_name_from_key(state_name)

                for key, value in state_definition.items():
                    if key == 'id':
                        self.map[state_name] = int(value)


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('map', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\map_data\state_regions'))
    manager.collect_file('map', '.txt')

    analysis = MapAnalysis()
    analysis.main(manager, 'map')

    print(analysis.map)
