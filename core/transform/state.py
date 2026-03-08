# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any

from pyradox import Tree

from core.datatype.state import StateFile, StateItem, StateCountryItem
from core.transform.base import TransformBase


class TransformStateDefault(TransformBase):
    def transform_state_country_item(self, item: StateCountryItem) -> Tree:
        tree = Tree()

        tree['country'] = item.country.prefix_string
        for i in item.owned_provinces:
            tree.append('owned_provinces', i, in_group=True)

        if item.state_type is not None:
            tree['state_type'] = item.state_type

        return tree

    def transform_state_item(self, item: StateItem):
        tree = Tree()

        for i in item.create_state:
            tree.append('create_state', self.transform_state_country_item(i))

        for i in item.add_homeland:
            tree.append('add_homeland', i.prefix_string)

        for i in item.add_claim:
            tree.append('add_claim', i.prefix_string)

        return tree

    def transform(self, target: StateFile) -> Tree:
        tree = Tree()
        tree[target.root_key] = {}

        for key, value in target.state_item_dict.items():
            tree[target.root_key][key.prefix_string] = self.transform_state_item(value)

        return tree


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager
    from core.analysis.state import AnalysisStateDefault

    manager = FileManager()
    manager.create_group('state', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\states'))
    manager.collect_file('state', '.txt')

    manager.create_group('new_state', Path(r'C:\Users\User\Documents\Paradox Interactive\Victoria 3\mod\Alternate World\common\history\states'))

    analysis = AnalysisStateDefault()
    analysis.main(manager, 'state')

    transform = TransformStateDefault()
    transform.main(manager, 'new_state', analysis.result)
