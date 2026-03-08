# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from pyradox import Tree

from core.datatype.prefix import StateNamePrefix, CountryTagPrefix, CultureNamePrefix
from core.datatype.state import StateFile, StateItem, StateCountryItem
from core.analysis.base import AnalysisBase

logger = getLogger(__name__)


class AnalysisStateDefault(AnalysisBase):
    """
    @brief 州数据分析类
    @details 分析维多利亚3游戏中的州数据文件，提取州和国家信息
    """
    def __init__(self):
        """
        @brief 初始化州数据分析类
        @details 调用父类初始化方法，设置结果字典类型
        """
        super().__init__()
        self.result: dict[str, StateFile] = {}
        logger.debug(f"AnalysisStateDefault initialized with empty result dict")

    def analysis_state_country_item(self, tree: Tree) -> StateCountryItem:
        """
        @brief 分析州中的国家项数据
        @details 从Tree对象中提取州中的国家相关信息，如国家标签、拥有的省份和州类型
        @param tree 包含国家项数据的Tree对象
        @return 解析后的StateCountryItem对象
        """
        result: dict[str, Any] = {}
        logger.debug(f"Starting analysis of state country item")

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'country':
                result['country'] = CountryTagPrefix(str_with_prefix=value)
                logger.debug(f"Found country key: {value}")
            elif key == 'owned_provinces':
                self.add_value_to_list_in_dict(result, 'owned_provinces', value)
                logger.debug(f"Added owned_province: {value}")
            elif key == 'state_type':
                result['state_type'] = value
                logger.debug(f"Found state_type: {value}")
            else:
                logger.warning(f"Unknown key '{key}' when analyzing state")

        self.verify_key_in_dictionary(result, 'state_type')
        logger.debug(f"State country item analysis completed")
        return StateCountryItem(**result)

    def analysis_state_item(self, tree: Tree) -> StateItem:
        """
        @brief 分析州项数据
        @details 从Tree对象中提取州相关信息，包括创建州、添加家园和添加声明等
        @param tree 包含州项数据的Tree对象
        @return 解析后的StateItem对象
        """
        result: dict[str, Any] = {}
        logger.debug(f"Starting analysis of state item")

        for key, value in tree.items():
            if key == 'create_state':
                logger.debug(f"Found create_state key, analyzing state country item")
                self.add_value_to_list_in_dict(result, 'create_state', self.analysis_state_country_item(value))
                continue

            value = self.get_stringify_value_from_tree(value)

            if key == 'add_homeland':
                logger.debug(f"Found add_homeland key: {value}")
                self.add_value_to_list_in_dict(result, 'add_homeland', CultureNamePrefix(str_with_prefix=value))
            elif key == 'add_claim':
                logger.debug(f"Found add_claim key: {value}")
                self.add_value_to_list_in_dict(result, 'add_claim', CountryTagPrefix(str_with_prefix=value))
            else:
                logger.warning(f"Unknown key '{key}' when analyzing state")

        self.verify_key_in_dictionary(result, 'add_homeland', [])
        self.verify_key_in_dictionary(result, 'add_claim', [])
        logger.debug(f"State item analysis completed")
        return StateItem(**result)


    def analysis(self, filename: str, tree: Tree):
        """
        @brief 分析州数据文件
        @details 从Tree对象中提取所有州数据，构建StateFile对象
        @param filename 正在分析的文件名
        @param tree 解析后的Tree对象
        """
        logger.debug(f"Starting state analysis for file '{filename}'")

        if 'STATES' not in tree:
            logger.error(f"No 'STATES' key found in tree for file '{filename}'")
            return

        state_item_dict: dict[StateNamePrefix, StateItem] = {}
        for name, context in tree['STATES'].items():
            logger.debug(f"Analyzing state: {name}")
            name = StateNamePrefix(str_with_prefix=name)
            state_item_dict[name] = self.analysis_state_item(context)

        self.result[filename] = StateFile(root_key='STATES', state_item_dict=state_item_dict)
        logger.info(f"State analysis completed for file '{filename}'")


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('state', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\states'))
    manager.collect_file('state', '.txt')

    analysis = AnalysisStateDefault()
    analysis.main(manager, 'state')
    print(analysis.result)
