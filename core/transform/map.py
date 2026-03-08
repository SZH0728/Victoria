# -*- coding:utf-8 -*-
# AUTHOR: Sun

from pyradox import Tree

from core.datatype.map import MapFile, MapRegion, MapResource
from core.transform.base import TransformBase


class TransformMapDefault(TransformBase):

    def transform_map_region(self, region: MapRegion) -> Tree:
        tree = Tree()

        # 必需字段
        tree['id'] = region.id
        tree['subsistence_building'] = region.subsistence_building
        tree['city'] = region.city
        tree['farm'] = region.farm
        tree['mine'] = region.mine
        tree['wood'] = region.wood
        tree['arable_land'] = region.arable_land

        # 可选字段（如果存在则添加）
        if region.port is not None:
            tree['port'] = region.port
        if region.naval_exit_id is not None:
            tree['naval_exit_id'] = region.naval_exit_id

        # 列表字段（使用in_group=True）
        for province in region.provinces:
            tree.append('provinces', province, in_group=True)
        for trait in region.traits:
            tree.append('traits', trait, in_group=True)
        for resource in region.arable_resources:
            tree.append('arable_resources', resource, in_group=True)

        # 嵌套字典字段：capped_resources
        if region.capped_resources:
            capped_tree = Tree()
            for resource_key, resource_value in region.capped_resources.items():
                capped_tree[resource_key] = resource_value
            tree['capped_resources'] = capped_tree

        if region.resource:
            for map_resource in region.resource:
                map_resource: MapResource
                resource_tree = Tree()

                resource_tree['type'] = map_resource.type

                if map_resource.depleted_type is not None:
                    resource_tree['depleted_type'] = map_resource.depleted_type

                if map_resource.undiscovered_amount is not None:
                    resource_tree['undiscovered_amount'] = map_resource.undiscovered_amount

                if map_resource.discovered_amount is not None:
                    resource_tree['discovered_amount'] = map_resource.discovered_amount

                tree.append('resource', resource_tree)

        return tree

    def transform(self, target: MapFile) -> Tree:
        tree = Tree()

        for state_prefix, region in target.map_region_dict.items():
            tree[state_prefix.prefix_string] = self.transform_map_region(region)

        return tree


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager
    from core.analysis.map import AnalysisMapDefault

    manager = FileManager()
    manager.create_group('map', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\map_data\state_regions'))
    manager.collect_file('map', '.txt')

    manager.create_group('new_map', Path(r'C:\Users\User\Documents\Paradox Interactive\Victoria 3\mod\Alternate World\map_data\state_regions'))

    analysis = AnalysisMapDefault()
    analysis.main(manager, 'map')

    transform = TransformMapDefault()
    transform.main(manager, 'new_map', analysis.result)