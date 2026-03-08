# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from abc import ABC, abstractmethod
from logging import getLogger

from pyradox import Tree, parse

from core.file import FileManager

logger = getLogger(__name__)


class IgnoreFileMixin(object):
    """
    @brief 文件忽略功能混入类
    @details 提供文件忽略列表管理功能，允许在分析过程中跳过特定文件
    """
    def __init__(self, *args, **kwargs):
        """
        @brief 初始化忽略文件混入类
        @details 初始化内部忽略文件集合
        """
        super().__init__(*args, **kwargs)
        self.ignore: set[str] = set()
        logger.debug(f"IgnoreFileMixin initialized with empty ignore set")

    def should_skip_file(self, filename: str) -> bool:
        """
        @brief 检查文件是否应该被跳过
        @details 根据忽略列表检查给定文件名是否应该被跳过
        @param filename 要检查的文件名
        @return 如果文件在忽略列表中则返回True，否则返回False
        """
        should_skip: bool = filename in self.ignore
        if should_skip:
            logger.debug(f"File '{filename}' is in ignore list, will be skipped")
        return should_skip

    def add_ignore_file(self, filename: str):
        """
        @brief 添加文件到忽略列表
        @details 将指定文件名添加到忽略列表中
        @param filename 要添加到忽略列表的文件名
        """
        self.ignore.add(filename)
        logger.debug(f"Added file '{filename}' to ignore list. Current ignore set: {self.ignore}")

    def remove_ignore_file(self, filename: str):
        """
        @brief 从忽略列表中移除文件
        @details 将指定文件名从忽略列表中移除，如果文件不在列表中则静默处理
        @param filename 要从忽略列表中移除的文件名
        """
        self.ignore.discard(filename)
        logger.debug(f"Removed file '{filename}' from ignore list. Current ignore set: {self.ignore}")


class AnalysisStaticMethodMixin(object):
    """
    @brief 静态工具方法混入类
    @details 提供静态辅助方法，用于数据处理和验证
    """
    @staticmethod
    def get_stringify_value_from_tree(value: Any) -> Any:
        """
        @brief 从Tree对象中提取字符串值
        @details 如果值是Tree对象，则转换为字符串；否则返回原值
        @param value 要处理的值，可以是任意类型
        @return 处理后的值，如果是Tree则返回字符串表示
        """
        if isinstance(value, Tree):
            logger.debug(f"Converting Tree object to string: {value}")
            return str(value)

        logger.debug(f"Returning value unchanged: {value}")
        return value

    @staticmethod
    def add_value_to_list_in_dict(dictionary: dict[str, Any], key: str, value: Any):
        """
        @brief 向字典中的列表添加值
        @details 如果键不存在，则创建空列表，然后将值添加到列表中
        @param dictionary 目标字典
        @param key 字典键
        @param value 要添加到列表的值
        """
        if key not in dictionary:
            dictionary[key] = []
            logger.debug(f"Created new list for key '{key}' in dictionary")

        dictionary[key].append(value)
        logger.debug(f"Added value '{value}' to list for key '{key}'")

    @staticmethod
    def add_value_to_dict_in_dict(dictionary: dict[str, Any], key: str, sub_key: Any, value: Any):
        """
        @brief 向字典中的字典添加值
        @details 如果外层键不存在，则创建空字典，然后将值设置到内层字典
        @param dictionary 目标字典
        @param key 外层字典键
        @param sub_key 内层字典键
        @param value 要设置的值
        """
        if key not in dictionary:
            dictionary[key] = {}
            logger.debug(f"Created new dict for key '{key}' in dictionary")

        dictionary[key][sub_key] = value
        logger.debug(f"Set value '{value}' for sub_key '{sub_key}' in dict for key '{key}'")

    @staticmethod
    def verify_key_in_dictionary(dictionary: dict[str, Any], key: str, value: Any = None):
        """
        @brief 验证字典中是否存在指定键，不存在则设置默认值
        @details 检查字典是否包含指定键，如果不包含则设置默认值
        @param dictionary 目标字典
        @param key 要验证的键
        @param value 默认值，默认为None
        """
        if key not in dictionary:
            dictionary[key] = value
            logger.debug(f"Key '{key}' not found in dictionary, set to default value: {value}")


class AnalysisBase(IgnoreFileMixin, AnalysisStaticMethodMixin, ABC):
    """
    @brief 分析模块基类
    @details 所有数据分析类的抽象基类，提供文件处理框架和分析流程
    """
    def __init__(self):
        """
        @brief 初始化分析基类
        @details 调用父类初始化方法，初始化结果字典
        """
        super().__init__()
        self.result: dict[str, Any] = {}

    @abstractmethod
    def analysis(self, filename: str, tree: Tree):
        """
        @brief 抽象分析方法
        @details 子类必须实现此方法，用于分析具体的游戏数据文件
        @param filename 正在分析的文件名
        @param tree 解析后的Tree对象
        @throws NotImplementedError 如果子类未实现此方法
        """
        pass

    @staticmethod
    def modify_context(context: str) -> str:
        """
        @brief 修改文件内容上下文
        @details 在解析前对文件内容进行预处理，子类可重写此方法
        @param context 原始文件内容字符串
        @return 处理后的文件内容字符串
        """
        logger.debug(f"modify_context called, returning original context (length: {len(context)})")
        return context

    def main(self, manager: FileManager, group: str):
        """
        @brief 主执行方法
        @details 遍历文件组中的所有文件，进行解析和分析
        @param manager 文件管理器实例
        @param group 文件组名称
        """
        logger.info(f"Starting analysis for group '{group}'")

        for file, context in manager.read_files_in_range(group):
            logger.debug(f"Processing file: '{file.name}'")

            if self.should_skip_file(file.name):
                logger.info(f"Skipping ignored file: {file.name}")
                continue

            logger.debug(f"Modifying context for file '{file.name}'")
            context: str = self.modify_context(context)
            logger.debug(f"Parsing modified context for file '{file.name}'")
            tree: Tree = parse(context)

            logger.debug(f"Calling analysis method for file '{file.name}'")
            self.analysis(file.name, tree)

        logger.info(f"Analysis completed for group '{group}'")


if __name__ == '__main__':
    pass
