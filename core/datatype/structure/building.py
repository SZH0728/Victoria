# -*- coding:utf-8 -*-
# AUTHOR: Sun

from dataclasses import dataclass

from core.datatype.prefix import StateNamePrefix
from core.datatype.source.building import BuildingItem, BuildingNoOwnerItem


StructuredBuildingItem = BuildingItem
StructuredBuildingNoOwnerItem = BuildingNoOwnerItem


@dataclass(frozen=True)
class StructuredBuildingState(object):
    """
    @brief 州建筑项目数据类
    @details 表示一个州内的建筑信息，包含区域到区域建筑的映射
    """
    state_building_dict: dict[StateNamePrefix, list[StructuredBuildingItem | StructuredBuildingNoOwnerItem]]  # 区域建筑字典


if __name__ == '__main__':
    pass
