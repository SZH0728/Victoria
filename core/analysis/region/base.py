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

logger = getLogger(__name__)


class RegionAnalysisBase(ABC):
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

    @staticmethod
    def get_continent_name_by_file_name(name: str | Path) -> str:
        """!
        @brief 根据文件名提取大洲名称
        @details 去除文件名中的'.txt'后缀和'_strategic_regions'后缀
        @param name 文件名或Path对象
        @return 大洲名称
        """
        if isinstance(name, Path):
            name = name.name

        name = name.replace('.txt', '')

        return name.replace('_strategic_regions', '')

    @staticmethod
    def get_region_name_by_key(name: str) -> str:
        """!
        @brief 根据区域键名提取区域名称
        @details 去除区域键名中的'region_'前缀
        @param name 区域键名
        @return 区域名称
        """
        return name.replace('region_', '')

    @abstractmethod
    def analysis(self, tree: Tree) -> list[RegionItem]:
        """!
        @brief 分析战略区域树，提取区域项
        @details 子类必须实现此方法，解析pyradox树结构并返回区域项列表
        @param tree pyradox解析的树结构
        @return 区域项列表
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
            tree = parse(content)
            region_items = self.analysis(tree)
            if region_items:
                logger.debug(f"Processed file {file_path.name}, extracted {len(region_items)} region items")
                region_name = self.get_continent_name_by_file_name(file_path)
                self.region[region_name].extend(region_items)
            else:
                logger.warning(f"No region items extracted from {file_path.name}")
        logger.info(f"Completed region analysis for group '{group}'")

if __name__ == '__main__':
    pass
