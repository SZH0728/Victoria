# -*- coding:utf-8 -*-
# AUTHOR: Sun

from abc import ABC, abstractmethod
from logging import getLogger

from pyradox import Tree

from core.file import FileManager
from core.datatype import Map, CountryDefinition

logger = getLogger(__name__)


class DefinitionTransformBase(ABC):
    """!
    @brief 国家定义转换抽象基类
    @details 提供国家定义转换的通用框架，子类需实现具体的转换逻辑
    """

    @abstractmethod
    def transform(self, country_definition: CountryDefinition) -> Tree:
        """!
        @brief 转换国家定义对象为pyradox树
        @param country_definition 国家定义对象
        @return 转换后的树
        """
        pass

    def main(self, manager: FileManager, group: str, filename: str, definition_map: Map[CountryDefinition]):
        """!
        @brief 主转换流程，将国家定义映射写入文件
        @details 遍历国家定义映射，转换每个国家定义并写入文件
        @param manager 文件管理器实例
        @param group 文件组名称
        @param filename 输出文件名
        @param definition_map 国家定义映射
        """
        logger.info(f"Starting definition transformation for group '{group}'")

        tree = Tree()

        for country_definition in definition_map.values():
            country_tag = country_definition.country_tag
            logger.debug(f"Transforming definition for country '{country_tag}'")
            tree[country_tag] = self.transform(country_definition)

        # 获取树的字符串表示
        content = str(tree)

        # 可选：如果需要，可以在这里进行格式调整
        # 例如，确保颜色格式正确

        manager.write_file(group, filename, content)
        logger.info(f"Completed definition transformation for group '{group}'")


if __name__ == '__main__':
    pass