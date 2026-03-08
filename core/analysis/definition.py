# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from pyradox import Tree

from core.datatype.prefix import CountryTagPrefix
from core.datatype.definition import CountryDefinition
from core.analysis.base import AnalysisBase

logger = getLogger(__name__)


class AnalysisDefinitionDefault(AnalysisBase):
    def __init__(self):
        super().__init__()
        self.add_ignore_file('99_dynamic.txt')

        self.result: dict[str, dict[CountryTagPrefix, CountryDefinition]] = {}

    def analysis_country_definition(self, tree: Tree) -> CountryDefinition:
        result: dict[str, Any] = {}

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'color':
                self.add_value_to_list_in_dict(result, 'color', value)
            elif key == 'country_type':
                result['country_type'] = value
            elif key == 'tier':
                result['tier'] = value
            elif key == 'cultures':
                self.add_value_to_list_in_dict(result, 'cultures', value)
            elif key == 'capital':
                result['capital'] = CountryTagPrefix(str_with_prefix=value)

            elif key == 'religion':
                result['religion'] = value
            elif key == 'is_named_from_capital':
                result['is_named_from_capital'] = value
            elif key == 'valid_as_home_country_for_separatists':
                result['valid_as_home_country_for_separatists'] = value
            elif key == 'social_hierarchy':
                result['social_hierarchy'] = value
            elif key.endswith('unit_color'):
                if 'unit_color' not in result:
                    result['unit_color'] = {}

                if key not in result['unit_color']:
                    result['unit_color'][key] = []

                result['unit_color'][key].append(value)
            else:
                logger.warning(f"Unknown key '{key}' when analyzing country definition")

        self.verify_key_in_dictionary(result, 'capital')
        self.verify_key_in_dictionary(result, 'religion')
        self.verify_key_in_dictionary(result, 'is_named_from_capital')
        self.verify_key_in_dictionary(result, 'valid_as_home_country_for_separatists')
        self.verify_key_in_dictionary(result, 'social_hierarchy')
        self.verify_key_in_dictionary(result, 'unit_color', {})

        return CountryDefinition(**result)

    def analysis(self, filename: str, tree: Tree):
        country_definition_dict: dict[CountryTagPrefix, CountryDefinition] = {}

        for name, context in tree.items():
            name = CountryTagPrefix(str_without_prefix=name.lower())
            country_definition_dict[name] = self.analysis_country_definition(context)

        self.result[filename] = country_definition_dict

    @staticmethod
    def modify_context(context: str) -> str:
        return context.replace('hsv360', '').replace('hsv', '')


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('definition', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\country_definitions'))
    manager.collect_file('definition', '.txt')

    analysis = AnalysisDefinitionDefault()
    analysis.main(manager, 'definition')
    print(analysis.result)
