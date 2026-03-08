# -*- coding:utf-8 -*-
# AUTHOR: Sun

from pyradox import Tree

from core.datatype.effect import EffectFile, EffectCountry
from core.transform.base import TransformBase


class TransformEffectDefault(TransformBase):

    def transform(self, target: EffectFile) -> Tree:
        tree = Tree()

        root_key = target.root_key if target.root_key is not None else 'COUNTRIES'
        tree[root_key] = Tree()

        for country_tag, country_effect in target.effect_country_dict.items():
            country_tree = Tree()

            # 处理effect列表中的效果，值为yes
            for effect_key in country_effect.boolean_effect:
                country_tree[effect_key] = True  # pyradox会将True输出为yes

            # 处理special_effect列表中的键值对
            for key, value in country_effect.special_effect:
                country_tree[key] = value

            tree[root_key][country_tag.prefix_string] = country_tree

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