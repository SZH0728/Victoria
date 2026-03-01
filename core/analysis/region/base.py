# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@file base.py
@brief 区域分析基础模块，定义区域数据结构和分析基类
@details 提供区域数据类、区域容器类以及区域分析的抽象基类
"""

from abc import ABC, abstractmethod
from logging import getLogger
from pathlib import Path

from pyradox import Tree, parse

from core.file import FileManager
from core.datatype import Region, RegionItem
from core.analysis.extract import KeyExtractionMixin

logger = getLogger(__name__)


class RegionAnalysisBase(KeyExtractionMixin, ABC):
    """!
    @brief 区域分析抽象基类
    @details 提供区域分析的通用框架，子类需实现具体的分析逻辑
    """

    def __init__(self):
        """!
        @brief 初始化区域分析器
        """
        self.region = Region()  #!< 区域数据容器
        logger.info("Region analysis base initialized")


    @abstractmethod
    def analysis(self, tree: Tree, region_name: str) -> RegionItem:
        """!
        @brief 分析战略区域树，提取区域项
        @details 子类必须实现此方法，解析pyradox树结构并返回区域项
        @param tree pyradox解析的树结构
        @param region_name 区域名称
        @return 区域项
        """
        pass

    def main(self, manager: FileManager, group: str):
        """!
        @brief 主分析流程，读取文件组并进行分析
        @details 遍历文件组中的所有文件，解析内容并调用analysis方法提取区域项，
                 将结果按大洲分类存储到region容器中
        @param manager 文件管理器实例
        @param group 文件组名称
        """
        logger.info(f"Starting region analysis for group '{group}'")

        for file_path, content in manager.read_files_in_range(group):
            logger.debug(f"Processing file: {file_path}")
            continent_name = self.extract_continent_name_from_filename(file_path)

            logger.debug(f"Parsing content for continent '{continent_name}'")
            tree = parse(content)

            logger.debug(f"Analyzing regions in continent '{continent_name}'")
            for region_name, region_definition in tree.items():
                region_name = self.extract_region_name_from_key(region_name)
                logger.debug(f"Analyzing region '{region_name}'")
                region_item = self.analysis(region_definition, region_name)
                self.region[continent_name].append(region_item)
                logger.debug(f"Region '{region_name}' added to continent '{continent_name}'")

        logger.info(f"Completed region analysis for group '{group}'")

if __name__ == '__main__':
    pass
