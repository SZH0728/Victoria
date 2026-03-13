# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from pyradox import Tree

from core.datatype.prefix import CountryTagPrefix
from core.datatype.source.definition import DefinitionCountry, DefinitionFile
from core.analysis.base import AnalysisBase

logger = getLogger(__name__)


class AnalysisDefinitionDefault(AnalysisBase):
    """
    @brief 国家定义数据分析类
    @details 分析维多利亚3游戏中的国家定义数据文件，提取国家属性和设置信息
    """
    def __init__(self):
        """
        @brief 初始化国家定义数据分析类
        @details 调用父类初始化方法，添加默认忽略文件，设置结果字典类型
        """
        super().__init__()
        self.add_ignore_file('99_dynamic.txt')
        self.result: dict[str, DefinitionFile] = {}
        logger.debug(f"AnalysisDefinitionDefault initialized with empty result dict")

    def analysis_country_definition(self, tree: Tree) -> DefinitionCountry:
        """
        @brief 分析国家定义数据
        @details 从Tree对象中提取国家定义信息，包括颜色、类型、等级、文化、首都等属性
        @param tree 包含国家定义数据的Tree对象
        @return 解析后的CountryDefinition对象
        """
        result: dict[str, Any] = {}
        logger.debug(f"Starting analysis of country definition")

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'color':
                self.add_value_to_list_in_dict(result, 'color', value)
                logger.debug(f"Added color value: {value}")
            elif key == 'country_type':
                result['country_type'] = value
                logger.debug(f"Found country_type: {value}")
            elif key == 'tier':
                result['tier'] = value
                logger.debug(f"Found tier: {value}")
            elif key == 'cultures':
                self.add_value_to_list_in_dict(result, 'cultures', value)
                logger.debug(f"Added culture: {value}")
            elif key == 'capital':
                result['capital'] = CountryTagPrefix(str_with_prefix=value)
                logger.debug(f"Found capital: {value}")
            elif key == 'religion':
                result['religion'] = value
                logger.debug(f"Found religion: {value}")
            elif key == 'is_named_from_capital':
                result['is_named_from_capital'] = value
                logger.debug(f"Found is_named_from_capital: {value}")
            elif key == 'valid_as_home_country_for_separatists':
                result['valid_as_home_country_for_separatists'] = value
                logger.debug(f"Found valid_as_home_country_for_separatists: {value}")
            elif key == 'social_hierarchy':
                result['social_hierarchy'] = value
                logger.debug(f"Found social_hierarchy: {value}")
            elif key.endswith('unit_color'):
                logger.debug(f"Found unit_color key: {key} with value: {value}")
                if 'unit_color' not in result:
                    result['unit_color'] = {}
                    logger.debug(f"Created unit_color dictionary")

                self.add_value_to_list_in_dict(result['unit_color'], key, value)
                logger.debug(f"Added value to unit_color[{key}] list")
            else:
                logger.warning(f"Unknown key '{key}' when analyzing country definition")

        self.verify_key_in_dictionary(result, 'capital')
        self.verify_key_in_dictionary(result, 'religion')
        self.verify_key_in_dictionary(result, 'is_named_from_capital')
        self.verify_key_in_dictionary(result, 'valid_as_home_country_for_separatists')
        self.verify_key_in_dictionary(result, 'social_hierarchy')
        self.verify_key_in_dictionary(result, 'unit_color', {})
        logger.debug(f"Country definition analysis completed")
        return DefinitionCountry(**result)

    def analysis(self, filename: str, tree: Tree):
        """
        @brief 分析国家定义数据文件
        @details 从Tree对象中提取所有国家定义数据，构建国家定义字典
        @param filename 正在分析的文件名
        @param tree 解析后的Tree对象
        """
        logger.debug(f"Starting country definition analysis for file '{filename}'")

        country_definition_dict: dict[CountryTagPrefix, DefinitionCountry] = {}
        for name, context in tree.items():
            logger.debug(f"Analyzing country definition: {name}")
            name = CountryTagPrefix(str_without_prefix=name.lower())
            country_definition_dict[name] = self.analysis_country_definition(context)

        self.result[filename] = DefinitionFile(root_key=None, definition_country_dict=country_definition_dict)
        logger.info(f"Country definition analysis completed for file '{filename}'")

    @staticmethod
    def modify_context(context: str) -> str:
        """
        @brief 修改文件内容上下文
        @details 移除HSV颜色格式前缀，以便正确解析国家定义文件
        @param context 原始文件内容字符串
        @return 处理后的文件内容字符串
        """
        modified_context = context.replace('hsv360', '').replace('hsv', '')
        logger.debug(f"modify_context called, removed HSV prefixes.")
        return modified_context


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('definition', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\country_definitions'))
    manager.collect_file('definition', '.txt')

    analysis = AnalysisDefinitionDefault()
    analysis.main(manager, 'definition')
    print(analysis.result)
