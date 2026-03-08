# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from pyradox import Tree

from core.datatype.prefix import StateNamePrefix, RegionStatePrefix
from core.datatype.population import PopulationFile, PopulationRegion, PopulationCountry, PopulationItem
from core.analysis.base import AnalysisBase

logger = getLogger(__name__)


class AnalysisPopulationDefault(AnalysisBase):
    def __init__(self):
        super().__init__()

        self.result: dict[str, PopulationFile] = {}

    def analysis_population_item(self, tree: Tree) -> PopulationItem:
        result: dict[str, Any] = {}

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'size':
                result['size'] = int(value)
            elif key == 'culture':
                result['culture'] = value
            elif key == 'religion':
                result['religion'] = value
            elif key == 'pop_type':
                result['pop_type'] = value
            else:
                logger.warning(f"Unknown key '{key}' when analyzing population item")

        self.verify_key_in_dictionary(result, 'culture')
        self.verify_key_in_dictionary(result, 'religion')
        self.verify_key_in_dictionary(result, 'pop_type')

        return PopulationItem(**result)

    def analysis_population_country(self, tree: Tree) -> PopulationCountry:
        result: dict[str, Any] = {}

        for key, value in tree.items():
            if key == 'create_pop':
                self.add_value_to_list_in_dict(result, 'create_pop', self.analysis_population_item(value))
            else:
                logger.warning(f"Unknown key '{key}' when analyzing population country")

        return PopulationCountry(**result)

    def analysis_population_region(self, tree: Tree) -> PopulationRegion:
        result: dict[str, Any] = {}

        for key, value in tree.items():
            if key.startswith('region_state:'):
                key = RegionStatePrefix(str_with_prefix=key)
                self.add_value_to_dict_in_dict(result, 'population_country_dict', key, self.analysis_population_country(value))
            else:
                logger.warning(f"Unknown key '{key}' when analyzing population region")

        return PopulationRegion(**result)

    def analysis(self, filename: str, tree: Tree):
        region_population_dict: dict[StateNamePrefix, PopulationRegion] = {}

        for state_name, state_context in tree['POPS'].items():
            state_name = StateNamePrefix(str_with_prefix=state_name)
            region_population_dict[state_name] = self.analysis_population_region(state_context)

        self.result[filename] = PopulationFile(root_key='POPS', population_region_dict=region_population_dict)


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('population', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\pops'))
    manager.collect_file('population', '.txt')

    analysis = AnalysisPopulationDefault()
    analysis.main(manager, 'population')
    print(analysis.result)
