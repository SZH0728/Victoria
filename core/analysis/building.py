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
    def __init__(self):
        super().__init__()

        self.result: dict[str, BuildingFile] = {}

    def analysis_building_country_ownership(self, tree: Tree) -> BuildingCountryOwnership:
        result: dict[str, Any] = {}

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'country':
                result['country'] = CountryTagPrefix(str_with_prefix=value)
            elif key == 'levels':
                result['levels'] = int(value)
            else:
                logger.warning(f"Unknown key '{key}' when analyzing building country ownership")

        return BuildingCountryOwnership(**result)

    def analysis_building_private_ownership(self, tree: Tree) -> BuildingPrivateOwnership:
        result: dict[str, Any] = {}

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'type':
                result['type'] = value
            elif key == 'country':
                result['country'] = CountryTagPrefix(str_with_prefix=value)
            elif key == 'levels':
                result['levels'] = int(value)
            elif key == 'region':
                result['region'] = StateNamePurePrefix(str_with_prefix=value)
            else:
                logger.warning(f"Unknown key '{key}' when analyzing building private ownership")

        return BuildingPrivateOwnership(**result)

    def analysis_building_company_ownership(self, tree: Tree) -> BuildingCompanyOwnership:
        result: dict[str, Any] = {}

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'type':
                result['type'] = value
            elif key == 'country':
                result['country'] = CountryTagPrefix(str_with_prefix=value)
            elif key == 'levels':
                result['levels'] = int(value)
            else:
                logger.warning(f"Unknown key '{key}' when analyzing building company ownership")

        return BuildingCompanyOwnership(**result)

    def analysis_building_ownership(self, tree: Tree) -> list[BuildingCountryOwnership|BuildingPrivateOwnership|BuildingCompanyOwnership]:
        result: list[BuildingCountryOwnership|BuildingPrivateOwnership|BuildingCompanyOwnership] = []

        for key, value in tree.items():
            if key == 'country':
                ownership_item = self.analysis_building_country_ownership(value)
            elif key == 'building':
                ownership_item = self.analysis_building_private_ownership(value)
            elif key == 'company':
                ownership_item = self.analysis_building_company_ownership(value)
            else:
                logger.warning(f"Unknown ownership type '{value}' when analyzing building item")
                continue

            result.append(ownership_item)

        return result

    def analysis_building_item(self, tree: Tree) -> BuildingItem:
        result: dict[str, Any] = {}

        for key, value in tree.items():
            if key == 'add_ownership':
                result['add_ownership'] = self.analysis_building_ownership(value)
                continue

            value = self.get_stringify_value_from_tree(value)

            if key == 'building':
                result['building'] = value
            elif key == 'subsidized':
                if isinstance(value, bool):
                    result['subsidized'] = value
                elif isinstance(value, str):
                    result['subsidized'] = (value == 'yes')
                else:
                    result['subsidized'] = None
            elif key == 'reserves':
                result['reserves'] = int(value)
            elif key == 'activate_production_methods':
                self.add_value_to_list_in_dict(result, 'activate_production_methods', value)
            else:
                logger.warning(f"Unknown key '{key}' when analyzing building item")

        self.verify_key_in_dictionary(result, 'subsidized')
        self.verify_key_in_dictionary(result, 'reserves')
        self.verify_key_in_dictionary(result, 'activate_production_methods', [])

        return BuildingItem(**result)

    def analysis_building_no_owner_item(self, tree: Tree) -> BuildingNoOwnerItem:
        result: dict[str, Any] = {}

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'building':
                result['building'] = value
            elif key == 'level':
                result['level'] = int(value)
            else:
                logger.warning(f"Unknown key '{key}' when analyzing building no owner item")

        return BuildingNoOwnerItem(**result)

    def analysis_building_country(self, tree: Tree) -> BuildingCountry:
        result: dict[str, Any] = {}

        for key, value in tree.items():
            if key == 'if':
                key = 'create_building'
                value = value['create_building']

            if key == 'create_building' and 'level' not in value.keys():
                self.add_value_to_list_in_dict(result, 'create_building', self.analysis_building_item(value))
            elif key == 'create_building' and 'level' in value.keys():
                self.add_value_to_list_in_dict(result, 'create_building', self.analysis_building_no_owner_item(value))
            else:
                logger.warning(f"Unknown key '{key}' when analyzing building country")

        if 'create_building' not in result:
            pass
        self.verify_key_in_dictionary(result, 'create_building', [])

        return BuildingCountry(**result)

    def analysis_building_state(self, tree: Tree) -> BuildingState:
        result: dict[str, Any] = {}

        for key, value in tree.items():
            if key.startswith('region_state:'):
                self.add_value_to_dict_in_dict(result, 'building_country_dict', RegionStatePrefix(str_with_prefix=key), self.analysis_building_country(value))
            else:
                logger.warning(f"Unknown key '{key}' when analyzing building state")

        return BuildingState(**result)

    def analysis(self, filename: str, tree: Tree):
        building_state_dict: dict[StateNamePrefix, BuildingState] = {}

        for state_name, state_context in tree['BUILDINGS'].items():
            if state_name == 'if':
                matching_values = [value for key, value in state_context.items() if key.startswith('s:')]
                if matching_values:
                    state_context = matching_values[0]
                else:
                    logger.warning(f"No 's:' prefix key found in conditional state context, skipping state '{state_name}'")
                    continue

            state_name_prefix = StateNamePrefix(str_with_prefix=state_name)
            building_state = self.analysis_building_state(state_context)
            building_state_dict[state_name_prefix] = building_state

        self.result[filename] = BuildingFile(building_state_dict=building_state_dict)


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('building', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\buildings'))
    manager.collect_file('building', '.txt')

    analysis = AnalysisBuildingDefault()
    analysis.main(manager, 'building')
    print(analysis.result)
