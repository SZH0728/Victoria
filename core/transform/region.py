# -*- coding:utf-8 -*-
# AUTHOR: Sun

from pyradox import Tree

from core.datatype.region import RegionFile, RegionItem
from core.transform.base import TransformBase


class TransformRegionDefault(TransformBase):

    def transform_region_item(self, region_item: RegionItem) -> Tree:
        tree = Tree()

        if region_item.graphical_culture is not None:
            tree['graphical_culture'] = region_item.graphical_culture

        if region_item.capital_province is not None:
            tree['capital_province'] = region_item.capital_province

        if region_item.map_color:
            for color_value in region_item.map_color:
                tree.append('map_color', color_value, in_group=True)

        if region_item.states:
            for state in region_item.states:
                tree.append('states', state.prefix_string, in_group=True)

        return tree

    def transform(self, target: RegionFile) -> Tree:
        tree = Tree()

        for region_name_prefix, region_item in target.region_item_dict.items():
            tree[region_name_prefix.prefix_string] = self.transform_region_item(region_item)

        return tree


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager
    from core.analysis.region import AnalysisRegionDefault

    manager = FileManager()
    manager.create_group('region', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\strategic_regions'))
    manager.collect_file('region', '.txt')

    manager.create_group('new_region', Path(r'C:\Users\User\Documents\Paradox Interactive\Victoria 3\mod\Alternate World\common\strategic_regions'))

    analysis = AnalysisRegionDefault()
    analysis.main(manager, 'region')

    transform = TransformRegionDefault()
    transform.main(manager, 'new_region', analysis.result)