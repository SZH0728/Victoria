# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from pyradox import Tree

from core.datatype.effect import EffectFile, EffectCountry
from core.transform.base import TransformBase

logger = getLogger(__name__)


class TransformEffectDefault(TransformBase):
    """
    @brief 国家效果数据转换类
    @details 将EffectFile对象转换回pyradox Tree对象，用于写入游戏数据文件
    """
    @staticmethod
    def transform_effect_country(effect_country: EffectCountry) -> Tree:
        """
        @brief 转换国家效果数据
        @details 将EffectCountry对象转换为pyradox Tree对象
        @param effect_country 国家效果数据对象
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of effect country: {effect_country}")
        tree = Tree()

        # 处理effect列表中的效果，值为yes
        for effect_key in effect_country.boolean_effect:
            tree[effect_key] = True  # pyradox会将True输出为yes
            logger.debug(f"Set boolean effect: {effect_key} = True")

        # 处理special_effect列表中的键值对
        for key, value in effect_country.special_effect:
            tree[key] = value
            logger.debug(f"Set special effect: {key} = {value}")

        logger.debug(f"Effect country transformation completed")
        return tree

    def transform(self, target: EffectFile) -> Tree:
        """
        @brief 转换国家效果数据文件
        @details 将EffectFile对象转换为完整的pyradox Tree对象，包含根键和所有国家效果
        @param target 国家效果数据文件对象
        @return 转换后的Tree对象
        @throws TypeError 如果target不是EffectFile类型
        """
        logger.debug(f"Starting transformation of effect file: {target}")

        self.raise_for_incorrect_type(target, EffectFile)
        tree, inner_tree = self.create_tree(target.root_key)

        for country_tag, effect_country in target.effect_country_dict.items():
            logger.debug(f"Processing country effect for tag: {country_tag.prefix_string}")
            country_tree = self.transform_effect_country(effect_country)

            inner_tree[country_tag.prefix_string] = country_tree
            logger.debug(f"Added country tree for tag: {country_tag.prefix_string}")

        logger.info(f"Effect file transformation completed, total countries: {len(target.effect_country_dict)}")
        return tree


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager
    from core.analysis.effect import AnalysisEffectDefault

    manager = FileManager()
    manager.create_group('effect', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\countries'))
    manager.collect_file('effect', '.txt')

    manager.create_group('new_effect', Path(r'C:\Users\User\Documents\Paradox Interactive\Victoria 3\mod\Alternate World\common\history\countries'))

    analysis = AnalysisEffectDefault()
    analysis.main(manager, 'effect')

    transform = TransformEffectDefault()
    transform.main(manager, 'new_effect', analysis.result)
