# -*- coding:utf-8 -*-
# AUTHOR: Sun

from pyradox import Tree

from core.datatype import CountryEffect
from core.transform.effect.base import EffectTransformBase


class EffectTransformDefault(EffectTransformBase):
    """!
    @brief 默认效果转换器
    @details 实现具体的效果转换逻辑，将效果数据对象转换为pyradox树
    """

    def transform(self, country_effect: CountryEffect) -> Tree:
        """!
        @brief 转换国家效果对象为pyradox树
        @details 将effect列表中的每个效果设为yes，将special_effect列表中的每个键值对保留原值
        @param country_effect 国家效果对象
        @return 转换后的树
        """
        tree = Tree()

        # 处理effect列表中的效果，值为yes
        for effect_key in country_effect.effect:
            tree[effect_key] = True  # pyradox会将True输出为yes

        # 处理special_effect列表中的键值对
        for key, value in country_effect.special_effect:
            tree[key] = value

        return tree


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager
    from core.analysis.effect.default import EffectAnalysisDefault

    manager = FileManager()
    manager.create_group('effect', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\countries'))
    manager.collect_file('effect', '.txt')

    manager.create_group('new_effect', Path(r'D:\poject\Victoria\common'))

    analysis = EffectAnalysisDefault()
    analysis.main(manager, 'effect')

    transform = EffectTransformDefault()
    transform.main(manager, 'new_effect', analysis.effect)