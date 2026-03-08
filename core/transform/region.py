# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from pyradox import Tree

from core.datatype.region import RegionFile, RegionItem
from core.transform.base import TransformBase

logger = getLogger(__name__)


class TransformRegionDefault(TransformBase):
    """
    @brief 区域数据转换类
    @details 将RegionFile对象转换回pyradox Tree对象，用于写入游戏数据文件
    """
    @staticmethod
    def transform_region_item(region_item: RegionItem) -> Tree:
        """
        @brief 转换区域项数据
        @details 将RegionItem对象转换为pyradox Tree对象
        @param region_item 区域项数据对象
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of region item")
        tree = Tree()

        if region_item.graphical_culture is not None:
            tree['graphical_culture'] = region_item.graphical_culture
            logger.debug(f"Set graphical_culture: {region_item.graphical_culture}")

        if region_item.capital_province is not None:
            tree['capital_province'] = region_item.capital_province
            logger.debug(f"Set capital_province: {region_item.capital_province}")

        if region_item.map_color:
            for color_value in region_item.map_color:
                tree.append('map_color', color_value, in_group=True)
                logger.debug(f"Added map_color value: {color_value}")

        if region_item.states:
            for state in region_item.states:
                tree.append('states', state.prefix_string, in_group=True)
                logger.debug(f"Added state: {state.prefix_string}")

        logger.debug(f"Region item transformation completed")
        return tree

    def transform(self, target: RegionFile) -> Tree:
        """
        @brief 转换区域数据文件
        @details 将RegionFile对象转换为完整的pyradox Tree对象，包含所有区域项
        @param target 区域数据文件对象
        @return 转换后的Tree对象
        @throws TypeError 如果target不是RegionFile类型
        """
        logger.debug(f"Starting transformation of region file")

        self.raise_for_incorrect_type(target, RegionFile)
        tree, inner_tree = self.create_tree(target.root_key)

        for region_name_prefix, region_item in target.region_item_dict.items():
            logger.debug(f"Transforming region item for key: {region_name_prefix.prefix_string}")
            inner_tree[region_name_prefix.prefix_string] = self.transform_region_item(region_item)

        logger.info(f"Region file transformation completed, total regions: {len(target.region_item_dict)}")
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