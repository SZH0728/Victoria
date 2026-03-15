# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from abc import ABC, abstractmethod
from logging import getLogger

logger = getLogger(__name__)


class StructureBase(ABC):
    """
    @brief 结构化转换基类
    @details 所有源数据到结构化数据转换类的抽象基类
    @note 输入类型: dict[str, SourceFile] (analysis.result)
          输出类型: dict[KeyPrefix, StructuredData] (按国家/标识符组织的结构化数据)
    """
    def __init__(self):
        """
        @brief 初始化转换基类
        """
        self.result: dict[str, Any] = {}
        logger.debug(f"{self.__class__.__name__} initialized with empty result dict")

    @abstractmethod
    def convert(self, source_dict: dict[str, Any]) -> dict[Any, Any]:
        """
        @brief 抽象转换方法
        @details 子类必须实现此方法，将源数据字典转换为结构化数据字典
        @param source_dict 源数据字典，键为文件名，值为源数据类实例
                           (直接来自analysis.result)
        @return 结构化数据字典，键通常为国家标签等标识符，值为结构化数据类实例
        @throws NotImplementedError 如果子类未实现此方法
        """
        pass

    def main(self, source_dict: dict[str, Any]):
        """
        @brief 主执行方法
        @details 执行转换并返回结果，设计为直接接收analysis模块的输出
        @param source_dict 源数据字典 (analysis.result)
        @return 转换后的结构化数据字典
        """
        logger.info(f"Starting {self.__class__.__name__} conversion with {len(source_dict)} source files")
        self.result = self.convert(source_dict)
        logger.info(f"Conversion completed, result contains {len(self.result)} items")


class DestructureBase(ABC):
    """
    @brief 解构转换基类
    @details 所有结构化数据到源数据转换类的抽象基类
    @note 输入类型: dict[KeyPrefix, StructuredData] (structure模块的输出)
          输出类型: dict[str, SourceFile] (可直接传递给transform模块)
    """
    def __init__(self):
        """
        @brief 初始化转换基类
        """
        self.result: dict[str, Any] = {}
        logger.debug(f"{self.__class__.__name__} initialized with empty result dict")

    @abstractmethod
    def convert(self, structure_dict: dict[Any, Any]) -> dict[str, Any]:
        """
        @brief 抽象转换方法
        @details 子类必须实现此方法，将结构化数据字典转换回源数据字典
        @param structure_dict 结构化数据字典，键通常为国家标签等标识符，值为结构化数据类实例
        @return 源数据字典，键为文件名，值为源数据类实例
        @throws NotImplementedError 如果子类未实现此方法
        """
        pass

    def main(self, structure_dict: dict[Any, Any]):
        """
        @brief 主执行方法
        @details 执行转换并返回结果，设计为输出可直接传递给transform模块
        @param structure_dict 结构化数据字典 (structure模块的输出)
        @return 源数据字典 (transform模块的输入)
        """
        logger.info(f"Starting {self.__class__.__name__} conversion with {len(structure_dict)} structure items")
        self.result = self.convert(structure_dict)
        logger.info(f"Conversion completed, result contains {len(self.result)} files")


if __name__ == '__main__':
    pass