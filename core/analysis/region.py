# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from pyradox import Tree

from core.datatype.prefix import RegionNamePrefix, StateNamePurePrefix
from core.datatype.region import RegionFile, RegionItem
from core.analysis.base import AnalysisBase

logger = getLogger(__name__)


class AnalysisRegionDefault(AnalysisBase):
    def __init__(self):
        super().__init__()
        self.add_ignore_file('water_strategic_regions.txt')

        self.result: dict[str, RegionFile] = {}

    def analysis_region_item(self, tree: Tree) -> RegionItem:
        result: dict[str, Any] = {}

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'graphical_culture':
                result['graphical_culture'] = value
            elif key == 'capital_province':
                result['capital_province'] = value
            elif key == 'map_color':
                self.add_value_to_list_in_dict(result, 'map_color', value)
            elif key == 'states':
                self.add_value_to_list_in_dict(result, 'states', StateNamePurePrefix(str_with_prefix=value))
            else:
                logger.warning(f"Unknown key '{key}' when analyzing region")

        self.verify_key_in_dictionary(result, 'graphical_culture')
        self.verify_key_in_dictionary(result, 'capital_province')

        return RegionItem(**result)


    def analysis(self, filename: str, tree: Tree):
        region_item_dict: dict[RegionNamePrefix, RegionItem] = {}

        for name, context in tree.items():
            name = RegionNamePrefix(str_with_prefix=name)
            region_item_dict[name] = self.analysis_region_item(context)

        self.result[filename] = RegionFile(root_key=None, region_item_dict=region_item_dict)


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('region', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\strategic_regions'))
    manager.collect_file('region', '.txt')

    analysis = AnalysisRegionDefault()
    analysis.main(manager, 'region')
    print(analysis.result)
