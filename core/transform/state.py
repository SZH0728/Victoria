# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from pyradox import Tree

from core.datatype.source.state import StateFile, StateItem, StateCountryItem
from core.transform.base import TransformBase

logger = getLogger(__name__)


class TransformStateDefault(TransformBase):
    """
    @brief 州数据转换类
    @details 将StateFile对象转换回pyradox Tree对象，用于写入游戏数据文件
    """
    @staticmethod
    def transform_state_country_item(item: StateCountryItem) -> Tree:
        """
        @brief 转换州中国家项数据
        @details 将StateCountryItem对象转换为pyradox Tree对象
        @param item 州中国家项数据对象
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of state country item")
        tree = Tree()

        tree['country'] = item.country.prefix_string
        logger.debug(f"Set country: {item.country.prefix_string}")

        for i in item.owned_provinces:
            tree.append('owned_provinces', i, in_group=True)
            logger.debug(f"Added owned_province: {i}")

        if item.state_type is not None:
            tree['state_type'] = item.state_type
            logger.debug(f"Set state_type: {item.state_type}")

        logger.debug(f"State country item transformation completed")
        return tree

    def transform_state_item(self, item: StateItem) -> Tree:
        """
        @brief 转换州项数据
        @details 将StateItem对象转换为pyradox Tree对象
        @param item 州项数据对象
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of state item")
        tree = Tree()

        for i in item.create_state:
            logger.debug(f"Processing create_state item: {i}")
            tree.append('create_state', self.transform_state_country_item(i))

        for i in item.add_homeland:
            logger.debug(f"Adding homeland: {i.prefix_string}")
            tree.append('add_homeland', i.prefix_string)

        for i in item.add_claim:
            logger.debug(f"Adding claim: {i.prefix_string}")
            tree.append('add_claim', i.prefix_string)

        logger.debug(f"State item transformation completed")
        return tree

    def transform(self, target: StateFile) -> Tree:
        """
        @brief 转换州数据文件
        @details 将StateFile对象转换为完整的pyradox Tree对象，包含根键和所有州项
        @param target 州数据文件对象
        @return 转换后的Tree对象
        @throws TypeError 如果target不是StateFile类型
        """
        logger.debug(f"Starting transformation of state file: {target}")

        self.raise_for_incorrect_type(target, StateFile)
        tree, inner_tree = self.create_tree(target.root_key)

        for key, value in target.state_item_dict.items():
            logger.debug(f"Transforming state item for key: {key.prefix_string}")
            inner_tree[key.prefix_string] = self.transform_state_item(value)

        logger.info(f"State file transformation completed, total states: {len(target.state_item_dict)}")
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
