# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from pyradox import Tree, parse

from core.datatype.prefix import CountryTagPrefix
from core.datatype.effect import EffectFile, EffectCountry
from core.analysis.base import AnalysisBase

logger = getLogger(__name__)


class AnalysisEffectDefault(AnalysisBase):
    """
    @brief 国家效果数据分析类
    @details 分析维多利亚3游戏中的国家效果数据文件，提取布尔效果和特殊效果信息
    """
    def __init__(self):
        """
        @brief 初始化国家效果数据分析类
        @details 调用父类初始化方法，设置结果字典类型
        """
        super().__init__()
        self.result: dict[str, EffectFile] = {}
        logger.debug(f"AnalysisEffectDefault initialized with empty result dict")

    def analysis_effect_country(self, tree: Tree) -> EffectCountry:
        """
        @brief 分析国家效果数据
        @details 从Tree对象中提取国家效果信息，将效果分为布尔效果和特殊效果两类
        @param tree 包含国家效果数据的Tree对象
        @return 解析后的EffectCountry对象
        """
        result: dict[str, Any] = {}
        logger.debug(f"Starting analysis of effect country")

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if value is True or (isinstance(value, str) and value.lower() == 'yes'):
                self.add_value_to_list_in_dict(result, 'boolean_effect', key)
                logger.debug(f"Added boolean effect: {key}")
            else:
                self.add_value_to_list_in_dict(result, 'special_effect', (key, value))
                logger.debug(f"Added special effect: {key} = {value}")

        self.verify_key_in_dictionary(result, 'boolean_effect', [])
        self.verify_key_in_dictionary(result, 'special_effect', [])
        logger.debug(f"Effect country analysis completed. Boolean effects: {len(result.get('boolean_effect', []))}, Special effects: {len(result.get('special_effect', []))}")
        return EffectCountry(**result)

    def analysis(self, filename: str, tree: Tree):
        """
        @brief 分析国家效果数据文件
        @details 从Tree对象中提取所有国家效果数据，构建EffectFile对象
        @param filename 正在分析的文件名
        @param tree 解析后的Tree对象
        """
        logger.debug(f"Starting effect analysis for file '{filename}'")

        if 'COUNTRIES' not in tree:
            logger.error(f"No 'COUNTRIES' key found in tree for file '{filename}'")
            return

        effect_country_dict: dict[CountryTagPrefix, EffectCountry] = {}

        for name, context in tree['COUNTRIES'].items():
            logger.debug(f"Analyzing effect for country: {name}")
            name = CountryTagPrefix(str_with_prefix=name)
            effect_country_dict[name] = self.analysis_effect_country(context)

        self.result[filename] = EffectFile(root_key='COUNTRIES', effect_country_dict=effect_country_dict)
        logger.info(f"Effect analysis completed for file '{filename}'")

    @staticmethod
    def modify_context(context: str) -> str:
        """
        @brief 修改文件内容上下文
        @details 将条件赋值运算符'?='替换为普通赋值运算符'='，以便正确解析效果文件
        @param context 原始文件内容字符串
        @return 处理后的文件内容字符串
        """
        modified_context = context.replace('?=', '=')
        logger.debug(f"modify_context called, replaced '?=' with '='. Original length: {len(context)}, modified length: {len(modified_context)}")
        return modified_context


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('effect', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\countries'))
    manager.collect_file('effect', '.txt')

    analysis = AnalysisEffectDefault()
    analysis.main(manager, 'effect')
    print(analysis.result)
