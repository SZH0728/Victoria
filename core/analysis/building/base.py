# -*- coding:utf-8 -*-
# AUTHOR: Sun

from abc import ABC, abstractmethod
from logging import getLogger

from pyradox import Tree, parse

from core.file import FileManager
from core.datatype import Map, StateBuilding
from core.analysis.extract import KeyExtractionMixin

logger = getLogger(__name__)


class BuildingAnalysisBase(KeyExtractionMixin, ABC):
    """!
    @brief 建筑分析抽象基类
    @details 提供建筑分析的通用框架，子类需实现具体的分析逻辑
    """

    def __init__(self):
        """!
        @brief 初始化建筑分析器
        """
        self.building: Map[StateBuilding] = Map()
        logger.info("Building analysis base initialized")


    @abstractmethod
    def analysis(self, tree: Tree, state_name: str) -> StateBuilding:
        """!
        @brief 分析建筑树，提取建筑数据
        @details 子类必须实现此方法，解析pyradox树结构并返回建筑对象
        @param tree pyradox解析的树结构
        @param state_name 州名称
        @return 建筑对象
        """
        pass

    def main(self, manager: FileManager, group: str):
        """!
        @brief 主分析流程，读取文件组并进行分析
        @details 遍历文件组中的所有文件，解析内容并调用analysis方法提取建筑数据，
                 将结果存储到building容器中
        @param manager 文件管理器实例
        @param group 文件组名称
        """
        logger.info(f"Starting building analysis for group '{group}'")

        for file_path, content in manager.read_files_in_range(group):
            logger.debug(f"Processing file: {file_path}")
            tree = parse(content)

            logger.debug(f"Analyzing buildings in tree")
            for state_name, building_definition in tree['BUILDINGS'].items():
                state_name = self.extract_state_name_from_key(state_name)
                logger.debug(f"Analyzing building for state '{state_name}'")
                building = self.analysis(building_definition, state_name)

                self.building[state_name] = building
                logger.debug(f"Building for state '{state_name}' added to container")

        logger.info(f"Completed building analysis for group '{group}'")

if __name__ == '__main__':
    pass
