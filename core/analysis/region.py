# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from pyradox import Tree

from core.datatype.prefix import RegionNamePrefix, StateNamePurePrefix
from core.datatype.source.region import RegionFile, RegionItem
from core.analysis.base import AnalysisBase

logger = getLogger(__name__)


class AnalysisRegionDefault(AnalysisBase):
    """
    @brief 战略区域数据分析类
    @details 分析维多利亚3游戏中的战略区域数据文件，提取区域相关信息
    """
    def __init__(self):
        """
        @brief 初始化战略区域数据分析类
        @details 调用父类初始化方法，添加默认忽略文件，设置结果字典类型
        """
        super().__init__()
        self.add_ignore_file('water_strategic_regions.txt')
        self.result: dict[str, RegionFile] = {}
        logger.debug(f"AnalysisRegionDefault initialized with empty result dict")

    def analysis_region_item(self, tree: Tree) -> RegionItem:
        """
        @brief 分析区域项数据
        @details 从Tree对象中提取战略区域相关信息，包括图形文化、首府省份、地图颜色和包含的州
        @param tree 包含区域项数据的Tree对象
        @return 解析后的RegionItem对象
        """
        result: dict[str, Any] = {}
        logger.debug(f"Starting analysis of region item")

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'graphical_culture':
                result['graphical_culture'] = value
                logger.debug(f"Found graphical_culture: {value}")
            elif key == 'capital_province':
                result['capital_province'] = value
                logger.debug(f"Found capital_province: {value}")
            elif key == 'map_color':
                self.add_value_to_list_in_dict(result, 'map_color', value)
                logger.debug(f"Added map_color value: {value}")
            elif key == 'states':
                self.add_value_to_list_in_dict(result, 'states', StateNamePurePrefix(str_with_prefix=value))
                logger.debug(f"Added state to region: {value}")
            else:
                logger.warning(f"Unknown key '{key}' when analyzing region")

        self.verify_key_in_dictionary(result, 'graphical_culture')
        self.verify_key_in_dictionary(result, 'capital_province')
        logger.debug(f"Region item analysis completed")
        return RegionItem(**result)


    def analysis(self, filename: str, tree: Tree):
        """
        @brief 分析战略区域数据文件
        @details 从Tree对象中提取所有区域数据，构建RegionFile对象
        @param filename 正在分析的文件名
        @param tree 解析后的Tree对象
        """
        logger.debug(f"Starting region analysis for file '{filename}'")

        region_item_dict: dict[RegionNamePrefix, RegionItem] = {}
        for name, context in tree.items():
            logger.debug(f"Analyzing region: {name}")
            name = RegionNamePrefix(str_with_prefix=name)
            region_item_dict[name] = self.analysis_region_item(context)

        self.result[filename] = RegionFile(root_key=None, region_item_dict=region_item_dict)
        logger.info(f"Region analysis completed for file '{filename}'")


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('region', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\strategic_regions'))
    manager.collect_file('region', '.txt')

    analysis = AnalysisRegionDefault()
    analysis.main(manager, 'region')
    print(analysis.result)
