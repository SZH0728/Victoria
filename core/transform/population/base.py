# -*- coding:utf-8 -*-
# AUTHOR: Sun

from abc import ABC, abstractmethod
from logging import getLogger

from pyradox import Tree

from core.file import FileManager
from core.datatype import Map, RegionPopulation
from core.transform.combine import KeyCombinationMixin

logger = getLogger(__name__)


class PopulationTransformBase(KeyCombinationMixin, ABC):
    """!
    @brief 人口转换抽象基类
    @details 提供人口数据转换的通用框架，子类需实现具体的转换逻辑
    """


    @abstractmethod
    def transform(self, region_population: RegionPopulation) -> Tree:
        """!
        @brief 转换区域人口对象为pyradox树
        @param region_population 区域人口对象
        @return 转换后的树
        """
        pass

    def main(self, manager: FileManager, group: str, filename: str, population_map: Map[RegionPopulation]):
        """!
        @brief 主转换流程，将人口映射写入文件
        @details 构建POPS顶层结构，转换每个区域人口并写入文件
        @param manager 文件管理器实例
        @param group 文件组名称
        @param filename 输出文件名
        @param population_map 区域人口映射
        """
        tree = Tree()

        tree['POPS'] = Tree()

        for region_population in population_map.values():
            state_name = self.combine_state_key(region_population.region)
            tree['POPS'][state_name] = self.transform(region_population)

        manager.write_file(group, filename, str(tree))


if __name__ == '__main__':
    pass