# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from abc import ABC, abstractmethod
from logging import getLogger

from pyradox import Tree

from core.file import FileManager

logger = getLogger(__name__)


class StaticMethodMixin(object):
    """
    @brief 静态工具方法混入类
    @details 提供静态辅助方法，用于数据处理和验证
    """
    @staticmethod
    def raise_for_incorrect_type(value: Any, expected_type: type):
        """
        @brief 验证值类型是否正确
        @details 检查给定值是否为指定类型，如果不是则抛出异常
        @param value 要验证的值
        @param expected_type 期望的类型
        @throws TypeError 如果值类型不正确
        """
        if not isinstance(value, expected_type):
            raise TypeError(f"Expected type {expected_type.__name__}, got {type(value).__name__}")

    @staticmethod
    def create_tree(inner_key: str | None) -> tuple[Tree, Tree]:
        """
        @brief 创建树对象
        @details 创建一个根树对象和一个内部树对象，并返回它们
        @param inner_key 内部树对象对应的键
        @return 树对象
        """
        root_tree = Tree()

        if inner_key:
            root_tree[inner_key] = Tree()
            return root_tree, root_tree[inner_key]
        else:
            return root_tree, root_tree


class TransformBase(StaticMethodMixin, ABC):
    """
    @brief 转换模块基类
    @details 所有数据转换类的抽象基类，提供文件处理框架和转换流程
    """

    def __init__(self):
        """
        @brief 初始化转换基类
        @details 调用父类初始化方法，初始化结果字典
        """
        self.result: dict[str, Any] = {}

    @abstractmethod
    def transform(self, target: Any) -> Tree:
        """
        @brief 抽象转换方法
        @details 子类必须实现此方法，用于将目标数据转换为pyradox Tree对象
        @param target 目标数据对象
        @return 转换后的Tree对象
        @throws NotImplementedError 如果子类未实现此方法
        """
        pass

    def main(self, manager: FileManager, group: str, target: dict[str, Any]):
        """
        @brief 主执行方法
        @details 遍历目标字典中的所有项，调用transform方法转换并写入文件
        @param manager 文件管理器实例
        @param group 文件组名称
        @param target 目标字典，键为文件名，值为要转换的数据对象
        """
        logger.info(f"Starting transformation main for group '{group}' with {len(target)} files")

        for key, value in target.items():
            logger.debug(f"Transforming file: {key}")
            tree = self.transform(value)
            logger.debug(f"Writing transformed tree to file: {key}")
            manager.write_file(group, key, str(tree))
            logger.debug(f"File written: {key}")

        logger.info(f"Transformation main completed for group '{group}'")


if __name__ == '__main__':
    pass