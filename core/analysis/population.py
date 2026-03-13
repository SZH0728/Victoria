# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from pyradox import Tree

from core.datatype.prefix import StateNamePrefix, RegionStatePrefix
from core.datatype.source.population import PopulationFile, PopulationRegion, PopulationCountry, PopulationItem
from core.analysis.base import AnalysisBase

logger = getLogger(__name__)


class AnalysisPopulationDefault(AnalysisBase):
    """
    @brief 人口数据分析类
    @details 分析维多利亚3游戏中的人口数据文件，提取人口统计和分布信息
    """
    def __init__(self):
        """
        @brief 初始化人口数据分析类
        @details 调用父类初始化方法，设置结果字典类型
        """
        super().__init__()
        self.result: dict[str, PopulationFile] = {}
        logger.debug(f"AnalysisPopulationDefault initialized with empty result dict")

    def analysis_population_item(self, tree: Tree) -> PopulationItem:
        """
        @brief 分析人口项数据
        @details 从Tree对象中提取人口详细信息，包括人口规模、文化、宗教和人口类型
        @param tree 包含人口项数据的Tree对象
        @return 解析后的PopulationItem对象
        """
        result: dict[str, Any] = {}
        logger.debug(f"Starting analysis of population item")

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'size':
                result['size'] = int(value)
                logger.debug(f"Found population size: {value}")
            elif key == 'culture':
                result['culture'] = value
                logger.debug(f"Found culture: {value}")
            elif key == 'religion':
                result['religion'] = value
                logger.debug(f"Found religion: {value}")
            elif key == 'pop_type':
                result['pop_type'] = value
                logger.debug(f"Found pop_type: {value}")
            else:
                logger.warning(f"Unknown key '{key}' when analyzing population item")

        self.verify_key_in_dictionary(result, 'culture')
        self.verify_key_in_dictionary(result, 'religion')
        self.verify_key_in_dictionary(result, 'pop_type')
        logger.debug(f"Population item analysis completed")
        return PopulationItem(**result)

    def analysis_population_country(self, tree: Tree) -> PopulationCountry:
        """
        @brief 分析国家人口数据
        @details 从Tree对象中提取国家级别的人口创建信息
        @param tree 包含国家人口数据的Tree对象
        @return 解析后的PopulationCountry对象
        """
        result: dict[str, Any] = {}
        logger.debug(f"Starting analysis of population country")

        for key, value in tree.items():
            if key == 'create_pop':
                logger.debug(f"Found create_pop key, analyzing population item")
                self.add_value_to_list_in_dict(result, 'create_pop', self.analysis_population_item(value))
            else:
                logger.warning(f"Unknown key '{key}' when analyzing population country")

        logger.debug(f"Population country analysis completed, create_pop items: {len(result.get('create_pop', []))}")
        return PopulationCountry(**result)

    def analysis_population_region(self, tree: Tree) -> PopulationRegion:
        """
        @brief 分析区域人口数据
        @details 从Tree对象中提取区域级别的人口数据，处理region_state前缀的键
        @param tree 包含区域人口数据的Tree对象
        @return 解析后的PopulationRegion对象
        """
        result: dict[str, Any] = {}
        logger.debug(f"Starting analysis of population region")

        for key, value in tree.items():
            if key.startswith('region_state:'):
                logger.debug(f"Found region_state key: {key}")
                key = RegionStatePrefix(str_with_prefix=key)
                self.add_value_to_dict_in_dict(result, 'population_country_dict', key, self.analysis_population_country(value))
            else:
                logger.warning(f"Unknown key '{key}' when analyzing population region")

        logger.debug(f"Population region analysis completed, population_country_dict entries: {len(result.get('population_country_dict', {}))}")
        return PopulationRegion(**result)

    def analysis(self, filename: str, tree: Tree):
        """
        @brief 分析人口数据文件
        @details 从Tree对象中提取所有州人口数据，构建PopulationFile对象
        @param filename 正在分析的文件名
        @param tree 解析后的Tree对象
        """
        logger.debug(f"Starting population analysis for file '{filename}'")

        if 'POPS' not in tree:
            logger.error(f"No 'POPS' key found in tree for file '{filename}'")
            return

        region_population_dict: dict[StateNamePrefix, PopulationRegion] = {}
        for state_name, state_context in tree['POPS'].items():
            logger.debug(f"Analyzing population for state: {state_name}")
            state_name = StateNamePrefix(str_with_prefix=state_name)
            region_population_dict[state_name] = self.analysis_population_region(state_context)

        self.result[filename] = PopulationFile(root_key='POPS', population_region_dict=region_population_dict)
        logger.info(f"Population analysis completed for file '{filename}'")


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('population', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\pops'))
    manager.collect_file('population', '.txt')

    analysis = AnalysisPopulationDefault()
    analysis.main(manager, 'population')
    print(analysis.result)
