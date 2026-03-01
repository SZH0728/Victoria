# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@file base.py
@brief 国家定义分析基础模块，定义国家定义数据结构和分析基类
@details 提供国家定义数据类、容器类以及国家定义分析的抽象基类
"""

from abc import ABC, abstractmethod
from logging import getLogger

from pyradox import Tree, parse

from core.file import FileManager
from core.datatype import Map, CountryDefinition
from core.analysis.extract import KeyExtractionMixin

logger = getLogger(__name__)


class DefinitionAnalysisBase(KeyExtractionMixin, ABC):
    """!
    @brief 国家定义分析抽象基类
    @details 提供国家定义分析的通用框架，子类需实现具体的分析逻辑
    """

    def __init__(self):
        """!
        @brief 初始化国家定义分析器
        """
        self.definition: Map[CountryDefinition] = Map()
        logger.info("Definition analysis base initialized")


    @abstractmethod
    def analysis(self, tree: Tree, country_tag: str) -> CountryDefinition:
        """!
        @brief 分析国家定义树，提取国家定义数据
        @details 子类必须实现此方法，解析pyradox树结构并返回国家定义对象
        @param tree pyradox解析的树结构
        @param country_tag 国家标签
        @return 国家定义对象
        """
        pass

    def main(self, manager: FileManager, group: str):
        """!
        @brief 主分析流程，读取文件组并进行分析
        @details 遍历文件组中的所有文件，解析内容并调用analysis方法提取国家定义数据，
                 将结果存储到definition容器中
        @param manager 文件管理器实例
        @param group 文件组名称
        """
        logger.info(f"Starting definition analysis for group '{group}'")

        for file_path, content in manager.read_files_in_range(group):
            if file_path.name == '99_dynamic.txt':
                continue

            logger.debug(f"Processing file: {file_path}")
            content = content.replace('hsv360', '').replace('hsv', '')
            tree = parse(content)

            logger.debug(f"Analyzing definitions in tree")
            for country_tag, definition in tree.items():
                logger.debug(f"Analyzing definition for country '{country_tag}'")
                country_def = self.analysis(definition, country_tag)

                self.definition[country_tag] = country_def
                logger.debug(f"Definition for country '{country_tag}' added to container")

        logger.info(f"Completed definition analysis for group '{group}'")


if __name__ == '__main__':
    pass