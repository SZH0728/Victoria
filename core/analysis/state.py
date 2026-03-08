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
    def __init__(self):
        super().__init__()

        self.result: dict[str, StateFile] = {}

    def analysis_state_country_item(self, tree: Tree) -> StateCountryItem:
        result: dict[str, Any] = {}

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'country':
                result['country'] = CountryTagPrefix(str_with_prefix=value)
            elif key == 'owned_provinces':
                self.add_value_to_list_in_dict(result, 'owned_provinces', value)
            elif key == 'state_type':
                result['state_type'] = value
            else:
                logger.warning(f"Unknown key '{key}' when analyzing state")

        self.verify_key_in_dictionary(result, 'state_type')
        return StateCountryItem(**result)

    def analysis_state_item(self, tree: Tree) -> StateItem:
        result: dict[str, Any] = {}

        for key, value in tree.items():
            if key == 'create_state':
                self.add_value_to_list_in_dict(result, 'create_state', self.analysis_state_country_item(value))
                continue

            value = self.get_stringify_value_from_tree(value)

            if key == 'add_homeland':
                self.add_value_to_list_in_dict(result, 'add_homeland', CultureNamePrefix(str_with_prefix=value))
            elif key == 'add_claim':
                self.add_value_to_list_in_dict(result, 'add_claim', CountryTagPrefix(str_with_prefix=value))
            else:
                logger.warning(f"Unknown key '{key}' when analyzing state")

        self.verify_key_in_dictionary(result, 'add_homeland', [])
        self.verify_key_in_dictionary(result, 'add_claim', [])

        return StateItem(**result)


    def analysis(self, filename: str, tree: Tree):
        state_item_dict: dict[StateNamePrefix, StateItem] = {}

        for name, context in tree['STATES'].items():
            name = StateNamePrefix(str_with_prefix=name)
            state_item_dict[name] = self.analysis_state_item(context)

        self.result[filename] = StateFile(root_key='STATES', state_item_dict=state_item_dict)


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('state', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\states'))
    manager.collect_file('state', '.txt')

    analysis = AnalysisStateDefault()
    analysis.main(manager, 'state')
    print(analysis.result)
