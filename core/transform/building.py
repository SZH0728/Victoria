# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any

from pyradox import Tree

from core.datatype.building import (
    BuildingFile, BuildingState, BuildingCountry, BuildingItem, BuildingNoOwnerItem,
    BuildingCountryOwnership, BuildingPrivateOwnership, BuildingCompanyOwnership
)
from core.transform.base import TransformBase


class TransformBuildingDefault(TransformBase):

    def transform_country_ownership(self, ownership: BuildingCountryOwnership) -> Tree:
        tree = Tree()

        tree['country'] = ownership.country.prefix_string
        tree['levels'] = ownership.levels

        return tree

    def transform_private_ownership(self, ownership: BuildingPrivateOwnership) -> Tree:
        tree = Tree()

        tree['type'] = ownership.type
        tree['country'] = ownership.country.prefix_string
        tree['levels'] = ownership.levels
        tree['region'] = ownership.region.prefix_string

        return tree

    def transform_company_ownership(self, ownership: BuildingCompanyOwnership) -> Tree:
        tree = Tree()

        tree['type'] = ownership.type
        tree['country'] = ownership.country.prefix_string
        tree['levels'] = ownership.levels

        return tree

    def transform_ownership_dict(self, ownerships: tuple[BuildingCountryOwnership | BuildingPrivateOwnership | BuildingCompanyOwnership, ...]) -> Tree:
        tree = Tree()

        for ownership in ownerships:
            if isinstance(ownership, BuildingCountryOwnership):
                tree.append('country', self.transform_country_ownership(ownership))
            elif isinstance(ownership, BuildingPrivateOwnership):
                tree.append('building', self.transform_private_ownership(ownership))
            elif isinstance(ownership, BuildingCompanyOwnership):
                tree.append('company', self.transform_company_ownership(ownership))

        return tree

    def transform_building_item(self, building_item: BuildingItem) -> Tree:
        tree = Tree()

        tree['building'] = building_item.building

        if building_item.add_ownership:
            tree['add_ownership'] = self.transform_ownership_dict(building_item.add_ownership)

        if building_item.subsidized is not None:
            tree['subsidized'] = building_item.subsidized

        if building_item.reserves is not None:
            tree['reserves'] = building_item.reserves

        if building_item.activate_production_methods:
            for method in building_item.activate_production_methods:
                tree.append('activate_production_methods', method, in_group=True)

        return tree

    def transform_no_owner_building_item(self, building_item: BuildingNoOwnerItem) -> Tree:
        tree = Tree()

        tree['building'] = building_item.building
        tree['level'] = building_item.level

        return tree

    def transform_country_building(self, country_building: BuildingCountry) -> Tree:
        tree = Tree()

        for building in country_building.create_building:
            if isinstance(building, BuildingItem):
                tree.append('create_building', self.transform_building_item(building))
            elif isinstance(building, BuildingNoOwnerItem):
                tree.append('create_building', self.transform_no_owner_building_item(building))

        return tree

    def transform_building_state(self, building_state: BuildingState) -> Tree:
        tree = Tree()

        for region_state_prefix, country_building in building_state.building_country_dict.items():
            tree[region_state_prefix.prefix_string] = self.transform_country_building(country_building)

        return tree

    def transform(self, target: BuildingFile) -> Tree:
        tree = Tree()

        tree['BUILDINGS'] = Tree()

        for state_name_prefix, building_state in target.building_state_dict.items():
            tree['BUILDINGS'][state_name_prefix.prefix_string] = self.transform_building_state(building_state)

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