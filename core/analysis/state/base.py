# -*- coding:utf-8 -*-
# AUTHOR: Sun

from abc import ABC, abstractmethod
from logging import getLogger

from pyradox import Tree, parse

from core.file import FileManager
from core.datatype import Map, State
from core.analysis.extract import KeyExtractionMixin

logger = getLogger(__name__)


class StateAnalysisBase(KeyExtractionMixin, ABC):
    """!
    @brief 州分析抽象基类
    @details 提供州分析的通用框架，子类需实现具体的分析逻辑
    """
    STATE_KEY_PREFIX = 's:STATE_'
    COUNTRY_TAG_KEY_PREFIX = 'c:'
    CULTURE_KEY_PREFIX = 'cu:'

    def __init__(self):
        """!
        @brief 初始化州分析器
        """
        self.state: Map[State] = Map()
        logger.info("State analysis base initialized")


    @abstractmethod
    def analysis(self, tree: Tree, state_name: str) -> State:
        """!
        @brief 分析州树，提取州数据
        @details 子类必须实现此方法，解析pyradox树结构并返回州对象
        @param tree pyradox解析的树结构
        @param state_name 州名称
        @return 州对象
        """
        pass

    def main(self, manager: FileManager, group: str):
        """!
        @brief 主分析流程，读取文件组并进行分析
        @details 遍历文件组中的所有文件，解析内容并调用analysis方法提取州数据，
                 将结果存储到state容器中
        @param manager 文件管理器实例
        @param group 文件组名称
        """
        logger.info(f"Starting state analysis for group '{group}'")

        for file_path, content in manager.read_files_in_range(group):
            logger.debug(f"Processing file: {file_path}")
            tree = parse(content)

            logger.debug(f"Analyzing states in tree")
            for state_name, state_definition in tree['STATES'].items():
                state_name = self.get_state_name_by_key(state_name)
                logger.debug(f"Analyzing state '{state_name}'")
                state = self.analysis(state_definition, state_name)

                self.state[state_name] = state
                logger.debug(f"State '{state_name}' added to container")

        logger.info(f"Completed state analysis for group '{group}'")


if __name__ == '__main__':
    pass
