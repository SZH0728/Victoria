# -*- coding:utf-8 -*-
# AUTHOR: Sun

from abc import ABC, abstractmethod
from logging import getLogger

from pyradox import Tree, parse

from core.file import FileManager
from core.datatype import Map, RegionPopulation
from core.analysis.extract import KeyExtractionMixin

logger = getLogger(__name__)


class PopulationAnalysisBase(KeyExtractionMixin, ABC):
    """!
    @brief 人口分析抽象基类
    @details 提供人口分析的通用框架，子类需实现具体的分析逻辑
    """
    STATE_KEY_PREFIX = 's:STATE_'
    COUNTRY_TAG_KEY_PREFIX = 'region_state:'

    def __init__(self):
        """!
        @brief 初始化人口分析器
        """
        self.population: Map[RegionPopulation] = Map()
        logger.info("Population analysis base initialized")


    @abstractmethod
    def analysis(self, tree: Tree, state_name: str) -> RegionPopulation:
        """!
        @brief 分析人口树，提取人口数据
        @details 子类必须实现此方法，解析pyradox树结构并返回人口对象
        @param tree pyradox解析的树结构
        @param state_name 州名称
        @return 人口对象
        """
        pass

    def main(self, manager: FileManager, group: str):
        """!
        @brief 主分析流程，读取文件组并进行分析
        @details 遍历文件组中的所有文件，解析内容并调用analysis方法提取人口数据，
                 将结果存储到population容器中
        @param manager 文件管理器实例
        @param group 文件组名称
        """
        logger.info(f"Starting population analysis for group '{group}'")

        for file_path, content in manager.read_files_in_range(group):
            logger.debug(f"Processing file: {file_path}")
            tree = parse(content)

            logger.debug(f"Analyzing populations in tree")
            for state_name, building_definition in tree['POPS'].items():
                state_name = self.get_state_name_by_key(state_name)
                logger.debug(f"Analyzing population for state '{state_name}'")
                population = self.analysis(building_definition, state_name)

                self.population[state_name] = population
                logger.debug(f"Population for state '{state_name}' added to container")

        logger.info(f"Completed population analysis for group '{group}'")

if __name__ == '__main__':
    pass
