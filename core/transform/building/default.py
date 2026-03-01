# -*- coding:utf-8 -*-
# AUTHOR: Sun

from pyradox import Tree

from core.datatype import (
    StateBuilding, CountryBuilding, BuildingItem, BuildingNoOwnerItem,
    BuildingCountryOwnership, BuildingPrivateOwnership, BuildingCompanyOwnership
)
from core.transform.building.base import BuildingTransformBase


class BuildingTransformDefault(BuildingTransformBase):
    """!
    @brief 默认建筑转换器
    @details 实现具体的建筑转换逻辑，将建筑数据对象转换为pyradox树
    """

    def transform_country_ownership(self, ownership: BuildingCountryOwnership) -> Tree:
        """!
        @brief 转换国家所有权对象为pyradox树
        @param ownership 国家所有权对象
        @return 转换后的树
        """
        tree = Tree()

        tree['country'] = self.combine_country_value(ownership.country)
        tree['levels'] = ownership.level

        return tree

    def transform_private_ownership(self, ownership: BuildingPrivateOwnership) -> Tree:
        """!
        @brief 转换私人所有权对象为pyradox树
        @param ownership 私人所有权对象
        @return 转换后的树
        """
        tree = Tree()

        tree['type'] = ownership.building
        tree['country'] = self.combine_country_value(ownership.country)
        tree['levels'] = ownership.level
        tree['region'] = ownership.region

        return tree

    def transform_company_ownership(self, ownership: BuildingCompanyOwnership) -> Tree:
        """!
        @brief 转换公司所有权对象为pyradox树
        @param ownership 公司所有权对象
        @return 转换后的树
        """
        tree = Tree()

        tree['type'] = ownership.company
        tree['country'] = self.combine_country_value(ownership.country)
        tree['levels'] = ownership.level

        return tree

    def transform_ownership(self, ownership_list: tuple[BuildingCountryOwnership|BuildingPrivateOwnership|BuildingCompanyOwnership, ...]) -> Tree:
        """!
        @brief 转换所有权列表为pyradox树
        @details 根据所有权类型分发到相应的转换方法
        @param ownership_list 所有权对象元组
        @return 转换后的树
        """
        tree = Tree()

        for ownership in ownership_list:
            if isinstance(ownership, BuildingCountryOwnership):
                tree.append('country', self.transform_country_ownership(ownership))
            elif isinstance(ownership, BuildingPrivateOwnership):
                tree.append('building', self.transform_private_ownership(ownership))
            elif isinstance(ownership, BuildingCompanyOwnership):
                tree.append('company', self.transform_company_ownership(ownership))

        return tree

    def transform_building_item(self, building_item: BuildingItem) -> Tree:
        """!
        @brief 转换建筑条目对象为pyradox树
        @details 处理建筑条目的所有字段，包括建筑类型、所有权、补贴、储备、生产方法等
        @param building_item 建筑条目对象
        @return 转换后的树
        """
        tree = Tree()

        tree['building'] = building_item.building

        if building_item.ownership:
            tree['add_ownership'] = self.transform_ownership(building_item.ownership)

        if building_item.subsidized is not None:
            tree['subsidized'] = building_item.subsidized

        if building_item.reserve is not None:
            tree['reserves'] = building_item.reserve

        if building_item.methods:
            for method in building_item.methods:
                tree.append('activate_production_methods', method, in_group=True)

        return tree

    def transform_no_owner_building_item(self, building_item: BuildingNoOwnerItem) -> Tree:
        """!
        @brief 转换无所有者建筑条目对象为pyradox树
        @details 处理无所有者建筑条目的字段，包括建筑类型和等级
        @param building_item 无所有者建筑条目对象
        @return 转换后的树
        """
        tree = Tree()

        tree['building'] = building_item.building
        tree['level'] = building_item.level

        return tree

    def transform_country_building(self, country_building: CountryBuilding) -> Tree:
        """!
        @brief 转换国家建筑对象为pyradox树
        @details 遍历国家建筑中的所有建筑条目，转换为create_building结构
        @param country_building 国家建筑对象
        @return 转换后的树
        """
        tree = Tree()

        for building in country_building.buildings:
            if isinstance(building, BuildingItem):
                tree.append('create_building', self.transform_building_item(building))
            elif isinstance(building, BuildingNoOwnerItem):
                tree.append('create_building', self.transform_no_owner_building_item(building))

        return tree

    def transform(self, state_building: StateBuilding) -> Tree:
        """!
        @brief 转换州建筑对象为pyradox树
        @details 实现抽象方法，遍历州建筑中的每个国家建筑，使用国家标签作为键
        @param state_building 州建筑对象
        @return 转换后的树
        """
        tree = Tree()

        for country_building in state_building.country:
            country_key = self.combine_country_key_for_region_state(country_building.country_tag)
            tree[country_key] = self.transform_country_building(country_building)

        return tree


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager
    from core.analysis.building.default import BuildingAnalysisDefault

    manager = FileManager()
    manager.create_group('building', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\buildings'))
    manager.collect_file('building', '.txt')

    manager.create_group('new_building', Path(r'D:\poject\Victoria\common'))

    analysis = BuildingAnalysisDefault()
    analysis.main(manager, 'building')

    transform = BuildingTransformDefault()
    transform.main(manager, 'new_building', 'default.txt', analysis.building)