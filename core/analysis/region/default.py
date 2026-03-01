# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@file default.py
@brief 默认区域分析实现
@details 提供基于pyradox树解析的具体区域分析实现
"""

from logging import getLogger

from pyradox import Tree

from core.datatype import RegionItem
from core.analysis.region.base import RegionAnalysisBase

logger = getLogger(__name__)


class RegionAnalysisDefault(RegionAnalysisBase):
    """!
    @brief 默认区域分析器
    @details 实现具体的区域分析逻辑，解析战略区域树结构
    """
    def analysis(self, tree: Tree, region_name: str) -> RegionItem:
        """!
        @brief 分析战略区域树，提取区域项
        @details 遍历树中的每个区域节点，提取图形文化、首府省份、地图颜色和州列表信息
        @param tree pyradox解析的树结构
        @param region_name 区域名称
        @return 区域项
        """
        logger.debug(f"Analyzing region '{region_name}'")
        graphical_culture: str = ''
        capital_province: str = ''
        map_color: list[int] = []
        states: list[str] = []

        for key, value in tree.items():
            if isinstance(value, Tree):
                value = str(value)

            if key == 'graphical_culture':
                graphical_culture = value
            elif key == 'capital_province':
                capital_province = value
            elif key == 'map_color':
                map_color.append(value)
            elif key == 'states':
                states.append(self.extract_state_name_from_key(value))
            else:
                logger.warning(f"Unknown key '{key}' in region '{region_name}'")

        logger.debug(f"Created region item for '{region_name}'")
        region_item = RegionItem(
            region_name=region_name,
            graphical_culture=graphical_culture,
            capital_province=capital_province,
            map_color=tuple(map_color),
            states=tuple(states)
        )

        return region_item


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('region', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\strategic_regions'))
    manager.collect_file('region', '.txt')

    analysis = RegionAnalysisDefault()
    analysis.main(manager, 'region')
    print(analysis.region)
