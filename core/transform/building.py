# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from pyradox import Tree

from core.datatype.source.building import BuildingFile, BuildingState, BuildingCountry, BuildingItem, BuildingNoOwnerItem, BuildingCountryOwnership, BuildingPrivateOwnership, BuildingCompanyOwnership, BuildingOwnership
from core.transform.base import TransformBase

logger = getLogger(__name__)


class TransformBuildingDefault(TransformBase):
    """
    @brief 建筑数据转换类
    @details 将BuildingFile对象转换回pyradox Tree对象，用于写入游戏数据文件
    """
    @staticmethod
    def transform_country_ownership(ownership: BuildingCountryOwnership) -> Tree:
        """
        @brief 转换国家所有权数据
        @details 将BuildingCountryOwnership对象转换为pyradox Tree对象
        @param ownership 国家所有权数据对象
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of country ownership")
        tree = Tree()

        tree['country'] = ownership.country.prefix_string
        logger.debug(f"Set country: {ownership.country.prefix_string}")

        tree['levels'] = ownership.levels
        logger.debug(f"Set levels: {ownership.levels}")

        logger.debug(f"Country ownership transformation completed")
        return tree

    @staticmethod
    def transform_private_ownership(ownership: BuildingPrivateOwnership) -> Tree:
        """
        @brief 转换私人所有权数据
        @details 将BuildingPrivateOwnership对象转换为pyradox Tree对象
        @param ownership 私人所有权数据对象
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of private ownership")
        tree = Tree()

        tree['type'] = ownership.type
        logger.debug(f"Set type: {ownership.type}")

        tree['country'] = ownership.country.prefix_string
        logger.debug(f"Set country: {ownership.country.prefix_string}")

        tree['levels'] = ownership.levels
        logger.debug(f"Set levels: {ownership.levels}")

        tree['region'] = ownership.region.prefix_string
        logger.debug(f"Set region: {ownership.region.prefix_string}")

        logger.debug(f"Private ownership transformation completed")
        return tree

    @staticmethod
    def transform_company_ownership(ownership: BuildingCompanyOwnership) -> Tree:
        """
        @brief 转换公司所有权数据
        @details 将BuildingCompanyOwnership对象转换为pyradox Tree对象
        @param ownership 公司所有权数据对象
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of company ownership")
        tree = Tree()

        tree['type'] = ownership.type
        logger.debug(f"Set type: {ownership.type}")

        tree['country'] = ownership.country.prefix_string
        logger.debug(f"Set country: {ownership.country.prefix_string}")

        tree['levels'] = ownership.levels
        logger.debug(f"Set levels: {ownership.levels}")

        logger.debug(f"Company ownership transformation completed")
        return tree

    def transform_ownership_list(self, ownerships: tuple[BuildingOwnership, ...]) -> Tree:
        """
        @brief 转换所有权列表数据
        @details 将所有权元组转换为pyradox Tree对象，根据所有权类型分配到不同键下
        @param ownerships 所有权元组
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of ownership list")
        tree = Tree()

        for ownership in ownerships:
            if isinstance(ownership, BuildingCountryOwnership):
                logger.debug(f"Processing country ownership")
                tree.append('country', self.transform_country_ownership(ownership))
            elif isinstance(ownership, BuildingPrivateOwnership):
                logger.debug(f"Processing private ownership")
                tree.append('building', self.transform_private_ownership(ownership))
            elif isinstance(ownership, BuildingCompanyOwnership):
                logger.debug(f"Processing company ownership")
                tree.append('company', self.transform_company_ownership(ownership))
            else:
                logger.warning(f"Unknown ownership type: {type(ownership)}")

        logger.debug(f"Ownership dict transformation completed")
        return tree

    def transform_building_item(self, building_item: BuildingItem) -> Tree:
        """
        @brief 转换建筑项数据
        @details 将BuildingItem对象转换为pyradox Tree对象
        @param building_item 建筑项数据对象
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of building item")
        tree = Tree()

        tree['building'] = building_item.building
        logger.debug(f"Set building: {building_item.building}")

        if building_item.add_ownership:
            logger.debug(f"Processing add_ownership")
            tree['add_ownership'] = self.transform_ownership_list(building_item.add_ownership)

        if building_item.subsidized is not None:
            tree['subsidized'] = building_item.subsidized
            logger.debug(f"Set subsidized: {building_item.subsidized}")

        if building_item.reserves is not None:
            tree['reserves'] = building_item.reserves
            logger.debug(f"Set reserves: {building_item.reserves}")

        if building_item.activate_production_methods:
            for method in building_item.activate_production_methods:
                tree.append('activate_production_methods', method, in_group=True)
                logger.debug(f"Added production method: {method}")

        logger.debug(f"Building item transformation completed")
        return tree

    @staticmethod
    def transform_no_owner_building_item(building_item: BuildingNoOwnerItem) -> Tree:
        """
        @brief 转换无所有者建筑项数据
        @details 将BuildingNoOwnerItem对象转换为pyradox Tree对象
        @param building_item 无所有者建筑项数据对象
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of no-owner building item")
        tree = Tree()

        tree['building'] = building_item.building
        logger.debug(f"Set building: {building_item.building}")

        tree['level'] = building_item.level
        logger.debug(f"Set level: {building_item.level}")

        logger.debug(f"No-owner building item transformation completed")
        return tree

    def transform_country_building(self, country_building: BuildingCountry) -> Tree:
        """
        @brief 转换国家建筑数据
        @details 将BuildingCountry对象转换为pyradox Tree对象
        @param country_building 国家建筑数据对象
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of country building")
        tree = Tree()

        for building in country_building.create_building:
            if isinstance(building, BuildingItem):
                logger.debug(f"Processing building item: {building}")
                tree.append('create_building', self.transform_building_item(building))
            elif isinstance(building, BuildingNoOwnerItem):
                logger.debug(f"Processing no-owner building item: {building}")
                tree.append('create_building', self.transform_no_owner_building_item(building))
            else:
                logger.warning(f"Unknown building type: {type(building)}")

        logger.debug(f"Country building transformation completed, total buildings: {len(country_building.create_building)}")
        return tree

    def transform_building_state(self, building_state: BuildingState) -> Tree:
        """
        @brief 转换建筑州数据
        @details 将BuildingState对象转换为pyradox Tree对象
        @param building_state 建筑州数据对象
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of building state")
        tree = Tree()

        for region_state_prefix, country_building in building_state.building_country_dict.items():
            logger.debug(f"Processing country building for region: {region_state_prefix.prefix_string}")
            tree[region_state_prefix.prefix_string] = self.transform_country_building(country_building)

        logger.debug(f"Building state transformation completed, total regions: {len(building_state.building_country_dict)}")
        return tree

    def transform(self, target: BuildingFile) -> Tree:
        """
        @brief 转换建筑数据文件
        @details 将BuildingFile对象转换为完整的pyradox Tree对象，包含根键和所有建筑州数据
        @param target 建筑数据文件对象
        @return 转换后的Tree对象
        @throws TypeError 如果target不是BuildingFile类型
        """
        logger.debug(f"Starting transformation of building file")

        self.raise_for_incorrect_type(target, BuildingFile)
        tree, inner_tree = self.create_tree(target.root_key)

        for state_name_prefix, building_state in target.building_state_dict.items():
            logger.debug(f"Transforming building state for key: {state_name_prefix.prefix_string}")
            inner_tree[state_name_prefix.prefix_string] = self.transform_building_state(building_state)

        logger.info(f"Building file transformation completed, total states: {len(target.building_state_dict)}")
        return tree


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager
    from core.analysis.building import AnalysisBuildingDefault

    manager = FileManager()
    manager.create_group('building', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\buildings'))
    manager.collect_file('building', '.txt')

    manager.create_group('new_building', Path(r'C:\Users\User\Documents\Paradox Interactive\Victoria 3\mod\Alternate World\common\history\buildings'))

    analysis = AnalysisBuildingDefault()
    analysis.main(manager, 'building')

    transform = TransformBuildingDefault()
    transform.main(manager, 'new_building', analysis.result)
