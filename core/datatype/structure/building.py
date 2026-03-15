# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 结构化建筑数据模块
@details 提供建筑数据类的结构化版本别名和州建筑数据结构
"""

from dataclasses import dataclass

from core.datatype.prefix import StateNamePrefix
from core.datatype.source.building import BuildingItem, BuildingNoOwnerItem


StructuredBuildingItem = BuildingItem
"""
@brief 结构化建筑项目数据类
@details 建筑数据的结构化版本别名，与原始 BuildingItem 相同
"""

StructuredBuildingNoOwnerItem = BuildingNoOwnerItem
"""
@brief 结构化无主建筑项目数据类
@details 无主建筑数据的结构化版本别名，与原始 BuildingNoOwnerItem 相同
"""


@dataclass(frozen=True)
class StructuredBuildingState(object):
    """
    @brief 结构化州建筑数据类
    @details 表示一个州内的建筑信息，以州为键映射到建筑列表的字典结构

    @note 此数据结构用于按州组织建筑数据，便于按州进行建筑信息查询和分析
    """
    state_building_dict: dict[StateNamePrefix, list[StructuredBuildingItem | StructuredBuildingNoOwnerItem]]  # 区域建筑字典


if __name__ == '__main__':
    pass
