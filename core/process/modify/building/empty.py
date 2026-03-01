# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.process.modify.building.empty
@brief 建筑清空修改器模块
@details 清空所有州的建筑数据，创建空的建筑结构
"""

from typing import Any

from core.datatype.map import Map
from core.datatype.building import StateBuilding
from core.process.modify.building.base import BuildingModifyBase


class BuildingModifyEmpty(BuildingModifyBase):
    """!
    @brief 建筑清空修改器
    @details 创建空的建筑数据结构，用于移除所有原始建筑信息
    """
    def modify(self) -> Any:
        """!
        @brief 执行建筑清空修改
        @details 创建空的建筑数据结构：
                 1. 遍历原始数据中的所有州
                 2. 为每个州创建空的StateBuilding对象（country字段为空元组）
                 3. 存储到建筑映射中

        @return 空的建筑映射 Map[StateBuilding]
        """
        building: Map[StateBuilding] = Map()

        for state in self.origin.state.keys():
            state_building = StateBuilding(
                state=state,
                country=()
            )

            building[state] = state_building

        return building

if __name__ == '__main__':
    pass
