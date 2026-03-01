# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@file base.py
@brief 国家效果分析基础模块，定义国家效果数据结构和分析基类
@details 提供国家效果数据类、容器类以及国家效果分析的抽象基类
"""

from abc import ABC, abstractmethod
from logging import getLogger

from pyradox import Tree, parse

from core.file import FileManager
from core.datatype import Map, CountryEffect
from core.analysis.extract import KeyExtractionMixin

logger = getLogger(__name__)


class EffectAnalysisBase(KeyExtractionMixin, ABC):
    """!
    @brief 国家效果分析抽象基类
    @details 提供国家效果分析的通用框架，子类需实现具体的分析逻辑
    """

    def __init__(self):
        """!
        @brief 初始化国家效果分析器
        """
        self.effect: Map[CountryEffect] = Map()
        logger.info("Effect analysis base initialized")


    @abstractmethod
    def analysis(self, tree: Tree, country_tag: str, country_name: str) -> CountryEffect:
        """!
        @brief 分析国家效果树，提取国家效果数据
        @details 子类必须实现此方法，解析pyradox树结构并返回国家效果对象
        @param tree pyradox解析的树结构
        @param country_tag 国家标签
        @param country_name 国家名称
        @return 国家效果对象
        """
        pass

    def main(self, manager: FileManager, group: str):
        """!
        @brief 主分析流程，读取文件组并进行分析
        @details 遍历文件组中的所有文件，解析内容并调用analysis方法提取国家效果数据，
                 将结果存储到effect容器中
        @param manager 文件管理器实例
        @param group 文件组名称
        """
        logger.info(f"Starting effect analysis for group '{group}'")

        for file_path, content in manager.read_files_in_range(group):
            logger.debug(f"Processing file: {file_path}")

            country_tag, country_name = file_path.stem.split('-', 1)
            country_tag = country_tag.strip().upper()
            country_name = country_name.strip().lower()

            # 预处理：替换 ?= 为 =，以便解析器正确解析
            content = content.replace('?=', '=')
            tree = parse(content)

            logger.debug(f"Analyzing effects in tree")
            for _, effect_definition in tree['COUNTRIES'].items():
                logger.debug(f"Analyzing effect for country '{country_tag} - {country_name}'")
                country_effect = self.analysis(effect_definition, country_tag, country_name)

                self.effect[country_tag] = country_effect
                logger.debug(f"Effect for country '{country_tag}' added to container")

        logger.info(f"Completed effect analysis for group '{group}'")


if __name__ == '__main__':
    pass