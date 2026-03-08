# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from pyradox import Tree

from core.datatype.prefix import CountryTagPrefix, StateNamePrefix, RegionStatePrefix, StateNamePurePrefix
from core.datatype.building import BuildingFile, BuildingState, BuildingCountry, BuildingItem, BuildingCountryOwnership, BuildingPrivateOwnership, BuildingCompanyOwnership, BuildingNoOwnerItem
from core.analysis.base import AnalysisBase

logger = getLogger(__name__)


class AnalysisBuildingDefault(AnalysisBase):
    """
    @brief 建筑数据分析类
    @details 分析维多利亚3游戏中的建筑数据文件，提取建筑所有权和属性信息
    """
    def __init__(self):
        """
        @brief 初始化建筑数据分析类
        @details 调用父类初始化方法，设置结果字典类型
        """
        super().__init__()
        self.result: dict[str, BuildingFile] = {}
        logger.debug(f"AnalysisBuildingDefault initialized with empty result dict")

    def analysis_building_country_ownership(self, tree: Tree) -> BuildingCountryOwnership:
        """
        @brief 分析国家建筑所有权数据
        @details 从Tree对象中提取国家建筑所有权信息，包括国家标签和建筑等级
        @param tree 包含国家建筑所有权数据的Tree对象
        @return 解析后的BuildingCountryOwnership对象
        """
        result: dict[str, Any] = {}
        logger.debug(f"Starting analysis of building country ownership")

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'country':
                result['country'] = CountryTagPrefix(str_with_prefix=value)
                logger.debug(f"Found country key: {value}")
            elif key == 'levels':
                result['levels'] = int(value)
                logger.debug(f"Found levels key: {value}")
            else:
                logger.warning(f"Unknown key '{key}' when analyzing building country ownership")

        logger.debug(f"Building country ownership analysis completed")
        return BuildingCountryOwnership(**result)

    def analysis_building_private_ownership(self, tree: Tree) -> BuildingPrivateOwnership:
        """
        @brief 分析私人建筑所有权数据
        @details 从Tree对象中提取私人建筑所有权信息，包括建筑类型、国家、等级和区域
        @param tree 包含私人建筑所有权数据的Tree对象
        @return 解析后的BuildingPrivateOwnership对象
        """
        result: dict[str, Any] = {}
        logger.debug(f"Starting analysis of building private ownership")

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'type':
                result['type'] = value
                logger.debug(f"Found type key: {value}")
            elif key == 'country':
                result['country'] = CountryTagPrefix(str_with_prefix=value)
                logger.debug(f"Found country key: {value}")
            elif key == 'levels':
                result['levels'] = int(value)
                logger.debug(f"Found levels key: {value}")
            elif key == 'region':
                result['region'] = StateNamePurePrefix(str_with_prefix=value)
                logger.debug(f"Found region key: {value}")
            else:
                logger.warning(f"Unknown key '{key}' when analyzing building private ownership")

        logger.debug(f"Building private ownership analysis completed")
        return BuildingPrivateOwnership(**result)

    def analysis_building_company_ownership(self, tree: Tree) -> BuildingCompanyOwnership:
        """
        @brief 分析公司建筑所有权数据
        @details 从Tree对象中提取公司建筑所有权信息，包括建筑类型、国家和等级
        @param tree 包含公司建筑所有权数据的Tree对象
        @return 解析后的BuildingCompanyOwnership对象
        """
        result: dict[str, Any] = {}
        logger.debug(f"Starting analysis of building company ownership")

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'type':
                result['type'] = value
                logger.debug(f"Found type key: {value}")
            elif key == 'country':
                result['country'] = CountryTagPrefix(str_with_prefix=value)
                logger.debug(f"Found country key: {value}")
            elif key == 'levels':
                result['levels'] = int(value)
                logger.debug(f"Found levels key: {value}")
            else:
                logger.warning(f"Unknown key '{key}' when analyzing building company ownership")

        logger.debug(f"Building company ownership analysis completed")
        return BuildingCompanyOwnership(**result)

    def analysis_building_ownership(self, tree: Tree) -> list[BuildingCountryOwnership|BuildingPrivateOwnership|BuildingCompanyOwnership]:
        """
        @brief 分析建筑所有权数据
        @details 从Tree对象中提取所有类型的建筑所有权信息，包括国家、私人和公司所有权
        @param tree 包含建筑所有权数据的Tree对象
        @return 解析后的所有权对象列表
        """
        result: list[BuildingCountryOwnership|BuildingPrivateOwnership|BuildingCompanyOwnership] = []
        logger.debug(f"Starting analysis of building ownership")

        for key, value in tree.items():
            if key == 'country':
                logger.debug(f"Found country ownership type")
                ownership_item = self.analysis_building_country_ownership(value)
            elif key == 'building':
                logger.debug(f"Found private building ownership type")
                ownership_item = self.analysis_building_private_ownership(value)
            elif key == 'company':
                logger.debug(f"Found company ownership type")
                ownership_item = self.analysis_building_company_ownership(value)
            else:
                logger.warning(f"Unknown ownership type '{value}' when analyzing building item")
                continue

            result.append(ownership_item)

        logger.debug(f"Building ownership analysis completed, found {len(result)} ownership items")
        return result

    def analysis_building_item(self, tree: Tree) -> BuildingItem:
        """
        @brief 分析建筑项数据
        @details 从Tree对象中提取建筑详细信息，包括所有权、补贴、储备和生产方法
        @param tree 包含建筑项数据的Tree对象
        @return 解析后的BuildingItem对象
        """
        result: dict[str, Any] = {}
        logger.debug(f"Starting analysis of building item")

        for key, value in tree.items():
            if key == 'add_ownership':
                logger.debug(f"Found add_ownership key, analyzing building ownership")
                result['add_ownership'] = self.analysis_building_ownership(value)
                continue

            value = self.get_stringify_value_from_tree(value)

            if key == 'building':
                result['building'] = value
                logger.debug(f"Found building type: {value}")
            elif key == 'subsidized':
                if isinstance(value, bool):
                    result['subsidized'] = value
                elif isinstance(value, str):
                    result['subsidized'] = (value == 'yes')
                else:
                    result['subsidized'] = None
                logger.debug(f"Found subsidized key: {value} -> {result['subsidized']}")
            elif key == 'reserves':
                result['reserves'] = int(value)
                logger.debug(f"Found reserves key: {value}")
            elif key == 'activate_production_methods':
                self.add_value_to_list_in_dict(result, 'activate_production_methods', value)
                logger.debug(f"Added production method: {value}")
            else:
                logger.warning(f"Unknown key '{key}' when analyzing building item")

        self.verify_key_in_dictionary(result, 'subsidized')
        self.verify_key_in_dictionary(result, 'reserves')
        self.verify_key_in_dictionary(result, 'activate_production_methods', [])
        logger.debug(f"Building item analysis completed")
        return BuildingItem(**result)

    def analysis_building_no_owner_item(self, tree: Tree) -> BuildingNoOwnerItem:
        """
        @brief 分析无所有者建筑项数据
        @details 从Tree对象中提取无所有者建筑信息，包括建筑类型和等级
        @param tree 包含无所有者建筑数据的Tree对象
        @return 解析后的BuildingNoOwnerItem对象
        """
        result: dict[str, Any] = {}
        logger.debug(f"Starting analysis of building no owner item")

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'building':
                result['building'] = value
                logger.debug(f"Found building type: {value}")
            elif key == 'level':
                result['level'] = int(value)
                logger.debug(f"Found level key: {value}")
            else:
                logger.warning(f"Unknown key '{key}' when analyzing building no owner item")

        logger.debug(f"Building no owner item analysis completed")
        return BuildingNoOwnerItem(**result)

    def analysis_building_country(self, tree: Tree) -> BuildingCountry:
        """
        @brief 分析国家建筑数据
        @details 从Tree对象中提取国家级别的建筑创建信息，处理条件语句和不同建筑类型
        @param tree 包含国家建筑数据的Tree对象
        @return 解析后的BuildingCountry对象
        """
        result: dict[str, Any] = {}
        logger.debug(f"Starting analysis of building country with {len(tree)} keys")

        for key, value in tree.items():
            if key == 'if':
                logger.debug(f"Found 'if' condition, extracting create_building from condition")
                key = 'create_building'
                value = value['create_building']

            if key == 'create_building' and 'level' not in value.keys():
                logger.debug(f"Found create_building without level key, analyzing as building item")
                self.add_value_to_list_in_dict(result, 'create_building', self.analysis_building_item(value))
            elif key == 'create_building' and 'level' in value.keys():
                logger.debug(f"Found create_building with level key, analyzing as no owner building item")
                self.add_value_to_list_in_dict(result, 'create_building', self.analysis_building_no_owner_item(value))
            else:
                logger.warning(f"Unknown key '{key}' when analyzing building country")

        if 'create_building' not in result:
            logger.debug(f"No create_building key found in building country data")
        else:
            logger.debug(f"Building country analysis completed, create_building items: {len(result.get('create_building', []))}")

        self.verify_key_in_dictionary(result, 'create_building', [])

        return BuildingCountry(**result)

    def analysis_building_state(self, tree: Tree) -> BuildingState:
        """
        @brief 分析州建筑数据
        @details 从Tree对象中提取州级别的建筑数据，处理region_state前缀的键
        @param tree 包含州建筑数据的Tree对象
        @return 解析后的BuildingState对象
        """
        result: dict[str, Any] = {}
        logger.debug(f"Starting analysis of building state")

        for key, value in tree.items():
            if key.startswith('region_state:'):
                logger.debug(f"Found region_state key: {key}")
                self.add_value_to_dict_in_dict(result, 'building_country_dict', RegionStatePrefix(str_with_prefix=key), self.analysis_building_country(value))
            else:
                logger.warning(f"Unknown key '{key}' when analyzing building state")

        logger.debug(f"Building state analysis completed, building_country_dict entries: {len(result.get('building_country_dict', {}))}")
        return BuildingState(**result)

    def analysis(self, filename: str, tree: Tree):
        """
        @brief 分析建筑数据文件
        @details 从Tree对象中提取所有州建筑数据，处理条件语句和状态转换，构建BuildingFile对象
        @param filename 正在分析的文件名
        @param tree 解析后的Tree对象
        """
        logger.debug(f"Starting building analysis for file '{filename}'")

        if 'BUILDINGS' not in tree:
            logger.error(f"No 'BUILDINGS' key found in tree for file '{filename}'")
            return

        building_state_dict: dict[StateNamePrefix, BuildingState] = {}
        for state_name, state_context in tree['BUILDINGS'].items():
            logger.debug(f"Analyzing building state: {state_name}")

            if state_name == 'if':
                logger.debug(f"Processing conditional state '{state_name}'")
                matching_values = [value for key, value in state_context.items() if key.startswith('s:')]
                if matching_values:
                    state_context = matching_values[0]
                    logger.debug(f"Found matching 's:' prefix key for conditional state")
                else:
                    logger.warning(f"No 's:' prefix key found in conditional state context, skipping state '{state_name}'")
                    continue

            state_name_prefix = StateNamePrefix(str_with_prefix=state_name)
            building_state = self.analysis_building_state(state_context)
            building_state_dict[state_name_prefix] = building_state
            logger.debug(f"Completed analysis for building state: {state_name}")

        self.result[filename] = BuildingFile(root_key='BUILDINGS' ,building_state_dict=building_state_dict)
        logger.info(f"Building analysis completed for file '{filename}'")


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('building', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\buildings'))
    manager.collect_file('building', '.txt')

    analysis = AnalysisBuildingDefault()
    analysis.main(manager, 'building')
    print(analysis.result)
