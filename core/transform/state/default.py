# -*- coding:utf-8 -*-
# AUTHOR: Sun

from pyradox import Tree

from core.datatype import State, CountryState, Map
from core.transform.state.base import StateTransformBase


class StateTransformDefault(StateTransformBase):
    """!
    @brief 默认州转换器
    @details 实现具体的州转换逻辑，将州数据对象转换为pyradox树
    """

    def transform_country_state(self, country_state: CountryState) -> Tree:
        """!
        @brief 转换国家州对象为pyradox树
        @param country_state 国家州对象
        @return 转换后的树
        """
        tree = Tree()

        tree['country'] = self.combine_country_key_for_c(country_state.country_tag)
        for i in country_state.provinces:
            tree.append('owned_provinces', i, in_group=True)

        return tree

    def transform(self, state: State) -> Tree:
        """!
        @brief 转换州对象为pyradox树
        @details 实现抽象方法，处理州的所有字段，包括国家关系、家园文化和宣称
        @param state 州对象
        @return 转换后的树
        """
        tree = Tree()

        for i in state.country:
            tree.append('create_state', self.transform_country_state(i))

        for i in state.homeland:
            tree.append('add_homeland', self.combine_culture_key(i))

        for i in state.claim:
            tree.append('add_claim', self.combine_country_key_for_c(i))

        return tree

if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager
    from core.analysis.state.default import StateAnalysisDefault

    manager = FileManager()
    manager.create_group('state', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\states'))
    manager.collect_file('state', '.txt')

    manager.create_group('new_state', Path(r'D:\poject\Victoria\common'))

    analysis = StateAnalysisDefault()
    analysis.main(manager, 'state')

    transform = StateTransformDefault()
    transform.main(manager, 'new_state', 'default.txt', analysis.state)
