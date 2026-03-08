# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from pyradox import Tree

from core.datatype.prefix import StateNamePurePrefix
from core.datatype.map import MapFile, MapRegion, MapResource
from core.analysis.base import AnalysisBase

logger = getLogger(__name__)


class AnalysisMapDefault(AnalysisBase):
    def __init__(self):
        super().__init__()
        self.add_ignore_file('99_seas.txt')

        self.result: dict[str, MapFile] = {}

    def analysis_map_undiscovered_resource(self, tree: Tree) -> MapResource:
        result: dict[str, Any] = {}

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'type':
                result['type'] = value
            elif key == 'depleted_type':
                result['depleted_type'] = value
            elif key == 'undiscovered_amount':
                result['undiscovered_amount'] = value
            elif key == 'discovered_amount':
                result['discovered_amount'] = value
            else:
                logger.warning(f"Unknown key '{key}' when analyzing map resource")

        self.verify_key_in_dictionary(result, 'depleted_type')
        self.verify_key_in_dictionary(result, 'undiscovered_amount')
        self.verify_key_in_dictionary(result, 'discovered_amount')

        return MapResource(**result)

    @staticmethod
    def analysis_map_resources(tree: Tree) -> dict[str, int]:
        result: dict[str, int] = {}

        for key, value in tree.items():
            result[key] = int(value)

        return result

    def analysis_map_region(self, tree: Tree) -> MapRegion:
        result: dict[str, Any] = {}

        for key, value in tree.items():
            if key == 'capped_resources':
                result['capped_resources'] = self.analysis_map_resources(value)
                continue

            if key == 'resource':
                self.add_value_to_list_in_dict(result, 'resource', self.analysis_map_undiscovered_resource(value))
                continue

            value = self.get_stringify_value_from_tree(value)

            if key == 'id':
                result['id'] = value

            elif key == 'subsistence_building':
                result['subsistence_building'] = value
            elif key == 'provinces':
                self.add_value_to_list_in_dict(result, 'provinces', value)
            elif key == 'traits':
                self.add_value_to_list_in_dict(result, 'traits', value)

            elif key == 'city':
                result['city'] = value
            elif key == 'port':
                result['port'] = value
            elif key == 'farm':
                result['farm'] = value
            elif key == 'mine':
                result['mine'] = value
            elif key == 'wood':
                result['wood'] = value

            elif key == 'arable_land':
                result['arable_land'] = value
            elif key == 'arable_resources':
                self.add_value_to_list_in_dict(result, 'arable_resources', value)

            elif key == 'naval_exit_id':
                result['naval_exit_id'] = value

        self.verify_key_in_dictionary(result, 'traits', [])
        self.verify_key_in_dictionary(result, 'port')
        self.verify_key_in_dictionary(result, 'capped_resources', {})
        self.verify_key_in_dictionary(result, 'resource', [])
        self.verify_key_in_dictionary(result, 'naval_exit_id')

        return MapRegion(**result)

    def analysis(self, filename: str, tree: Tree):
        map_region_dict: dict[StateNamePurePrefix, MapRegion] = {}

        for state_name, state_context in tree.items():
            state_name = StateNamePurePrefix(str_with_prefix=state_name)
            map_region_dict[state_name] = self.analysis_map_region(state_context)

        self.result[filename] = MapFile(root_key='MAP', map_region_dict=map_region_dict)

if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('map', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\map_data\state_regions'))
    manager.collect_file('map', '.txt')

    analysis = AnalysisMapDefault()
    analysis.main(manager, 'map')
    print(analysis.result)
