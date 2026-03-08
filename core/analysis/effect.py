# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from pyradox import Tree, parse

from core.datatype.prefix import CountryTagPrefix
from core.datatype.effect import EffectFile, EffectCountry
from core.analysis.base import AnalysisBase

logger = getLogger(__name__)


class AnalysisEffectDefault(AnalysisBase):
    def __init__(self):
        super().__init__()

        self.result: dict[str, EffectFile] = {}

    def analysis_effect_country(self, tree: Tree) -> EffectCountry:
        result: dict[str, Any] = {}

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if value is True or (isinstance(value, str) and value.lower() == 'yes'):
                self.add_value_to_list_in_dict(result, 'boolean_effect', key)
            else:
                self.add_value_to_list_in_dict(result, 'special_effect', (key, value))

        self.verify_key_in_dictionary(result, 'boolean_effect', ())
        self.verify_key_in_dictionary(result, 'special_effect', ())

        return EffectCountry(**result)

    def analysis(self, filename: str, tree: Tree):
        effect_country_dict: dict[CountryTagPrefix, EffectCountry] = {}

        for name, context in tree['COUNTRIES'].items():
            name = CountryTagPrefix(str_with_prefix=name)
            effect_country_dict[name] = self.analysis_effect_country(context)

        self.result[filename] = EffectFile(root_key=None, effect_country_dict=effect_country_dict)

    @staticmethod
    def modify_context(context: str) -> str:
        return context.replace('?=', '=')


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('effect', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\countries'))
    manager.collect_file('effect', '.txt')

    analysis = AnalysisEffectDefault()
    analysis.main(manager, 'effect')
    print(analysis.result)
