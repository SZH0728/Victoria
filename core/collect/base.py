# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 收集模块基类
@details 所有数据收集类的抽象基类，提供数据统计框架和收集流程
"""

from typing import Any, Tuple
from abc import ABC, abstractmethod
from logging import getLogger

from core.datatype.summarize import SourceSummary, StructureSummary

logger = getLogger(__name__)


class CollectBase(ABC):
    """
    @brief 收集模块基类
    @details 所有数据收集类的抽象基类，提供数据统计框架和收集流程

    此抽象基类定义了收集模块的统一接口，所有具体收集类必须实现 collect 方法。
    收集模块的主要作用是从 SourceSummary 和 StructureSummary 中提取统计信息，
    """
    def __init__(self):
        """
        @brief 初始化收集基类
        @details 调用父类初始化方法，初始化结果属性
        """
        super().__init__()
        self.result: Tuple[str, Any] | None = None

    @abstractmethod
    def collect(self, source_summary: SourceSummary, structure_summary: StructureSummary) -> Tuple[str, Any]:
        """
        @brief 抽象收集方法
        @details 子类必须实现此方法，用于从数据汇总中提取统计信息

        @param source_summary 原始数据汇总对象，包含所有原始数据文件
        @param structure_summary 结构化数据汇总对象，包含所有结构化数据
        @return 元组 (collect名称, 统计结果数据类)
        @throws NotImplementedError 如果子类未实现此方法
        """
        pass

    def main(self, source_summary: SourceSummary, structure_summary: StructureSummary) -> Tuple[str, Any]:
        """
        @brief 主执行方法
        @details 调用 collect 方法进行数据统计，并返回结果

        @param source_summary 原始数据汇总对象
        @param structure_summary 结构化数据汇总对象
        @return 元组 (collect名称, 统计结果数据类)
        """
        logger.info(f"Starting collection for {self.__class__.__name__}")

        self.result = self.collect(source_summary, structure_summary)
        collect_name, collect_result = self.result

        logger.info(f"Collection completed for {self.__class__.__name__}, result name: {collect_name}")

        return self.result


if __name__ == '__main__':
    pass