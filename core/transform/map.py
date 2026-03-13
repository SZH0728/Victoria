# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from pyradox import Tree

from core.datatype.source.map import MapFile, MapRegion, MapResource
from core.transform.base import TransformBase

logger = getLogger(__name__)


class TransformMapDefault(TransformBase):
    """
    @brief 地图数据转换类
    @details 将MapFile对象转换回pyradox Tree对象，用于写入游戏数据文件
    """
    @staticmethod
    def transform_map_resource(map_resource: MapResource) -> Tree:
        """
        @brief 转换地图资源数据
        @details 将MapResource对象转换为pyradox Tree对象
        @param map_resource 地图资源数据对象
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of map resource")
        tree = Tree()

        tree['type'] = map_resource.type
        logger.debug(f"Set resource type: {map_resource.type}")

        if map_resource.depleted_type is not None:
            tree['depleted_type'] = map_resource.depleted_type
            logger.debug(f"Set depleted_type: {map_resource.depleted_type}")

        if map_resource.undiscovered_amount is not None:
            tree['undiscovered_amount'] = map_resource.undiscovered_amount
            logger.debug(f"Set undiscovered_amount: {map_resource.undiscovered_amount}")

        if map_resource.discovered_amount is not None:
            tree['discovered_amount'] = map_resource.discovered_amount
            logger.debug(f"Set discovered_amount: {map_resource.discovered_amount}")

        logger.debug(f"Map resource transformation completed")
        return tree

    @staticmethod
    def transform_capped_resources(capped_resources: dict[str, int]) -> Tree:
        """
        @brief 转换限制资源字典
        @details 将capped_resources字典转换为pyradox Tree对象
        @param capped_resources 限制资源字典，键为资源类型，值为资源数量
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of capped resources")
        tree = Tree()

        for resource_key, resource_value in capped_resources.items():
            tree[resource_key] = resource_value
            logger.debug(f"Added capped_resource {resource_key}: {resource_value}")

        logger.debug(f"Capped resources transformation completed, total items: {len(capped_resources)}")
        return tree

    def transform_map_region(self, region: MapRegion) -> Tree:
        """
        @brief 转换地图区域数据
        @details 将MapRegion对象转换为pyradox Tree对象
        @param region 地图区域数据对象
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of map region")
        tree = Tree()

        tree['id'] = region.id
        logger.debug(f"Set id: {region.id}")

        tree['subsistence_building'] = region.subsistence_building
        logger.debug(f"Set subsistence_building: {region.subsistence_building}")

        # 列表字段（使用in_group=True）
        for province in region.provinces:
            tree.append('provinces', province, in_group=True)
            logger.debug(f"Added province: {province}")

        for trait in region.traits:
            tree.append('traits', trait, in_group=True)
            logger.debug(f"Added trait: {trait}")

        tree['city'] = region.city
        logger.debug(f"Set city: {region.city}")

        # 可选字段（如果存在则添加）
        if region.port is not None:
            tree['port'] = region.port
            logger.debug(f"Set port: {region.port}")

        tree['farm'] = region.farm
        logger.debug(f"Set farm: {region.farm}")

        tree['mine'] = region.mine
        logger.debug(f"Set mine: {region.mine}")

        tree['wood'] = region.wood
        logger.debug(f"Set wood: {region.wood}")

        tree['arable_land'] = region.arable_land
        logger.debug(f"Set arable_land: {region.arable_land}")

        for resource in region.arable_resources:
            tree.append('arable_resources', resource, in_group=True)
            logger.debug(f"Added arable_resource: {resource}")

        # 嵌套字典字段：capped_resources
        if region.capped_resources:
            tree['capped_resources'] = self.transform_capped_resources(region.capped_resources)
            logger.debug(f"Set capped_resources with {len(region.capped_resources)} items")

        if region.resource:
            for map_resource in region.resource:
                map_resource: MapResource
                tree.append('resource', self.transform_map_resource(map_resource))
                logger.debug(f"Added resource tree")

        if region.naval_exit_id is not None:
            tree['naval_exit_id'] = region.naval_exit_id
            logger.debug(f"Set naval_exit_id: {region.naval_exit_id}")

        logger.debug(f"Map region transformation completed")
        return tree

    def transform(self, target: MapFile) -> Tree:
        """
        @brief 转换地图数据文件
        @details 将MapFile对象转换为完整的pyradox Tree对象，包含所有地图区域
        @param target 地图数据文件对象
        @return 转换后的Tree对象
        @throws TypeError 如果target不是MapFile类型
        """
        logger.debug(f"Starting transformation of map file")

        self.raise_for_incorrect_type(target, MapFile)
        tree, inner_tree = self.create_tree(target.root_key)

        for state_prefix, region in target.map_region_dict.items():
            logger.debug(f"Transforming map region for key: {state_prefix.prefix_string}")
            inner_tree[state_prefix.prefix_string] = self.transform_map_region(region)

        logger.info(f"Map file transformation completed, total regions: {len(target.map_region_dict)}")
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
