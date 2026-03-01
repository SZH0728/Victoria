# -*- coding:utf-8 -*-
# AUTHOR: Sun

from abc import ABC, abstractmethod
from logging import getLogger

from pyradox import Tree

from core.file import FileManager
from core.datatype import Map, StateBuilding
from core.transform.combine import KeyCombinationMixin

logger = getLogger(__name__)


class BuildingTransformBase(KeyCombinationMixin, ABC):
    """!
    @brief 建筑转换抽象基类
    @details 提供建筑数据转换的通用框架，子类需实现具体的转换逻辑
    """


    @abstractmethod
    def transform(self, state_building: StateBuilding) -> Tree:
        """!
        @brief 转换州建筑对象为pyradox树
        @param state_building 州建筑对象
        @return 转换后的树
        """
        pass

    def main(self, manager: FileManager, group: str, filename: str, building_map: Map[StateBuilding]):
        """!
        @brief 主转换流程，将建筑映射写入文件
        @details 构建BUILDINGS顶层结构，转换每个州建筑并写入文件
        @param manager 文件管理器实例
        @param group 文件组名称
        @param filename 输出文件名
        @param building_map 州建筑映射
        """
        tree = Tree()

        tree['BUILDINGS'] = Tree()

        for state_building in building_map.values():
            state_name = self.combine_state_key(state_building.state)
            tree['BUILDINGS'][state_name] = self.transform(state_building)

        manager.write_file(group, filename, str(tree))


if __name__ == '__main__':
    pass