# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@file default.py
@brief 默认国家效果分析器
@details 实现具体的国家效果分析逻辑，解析国家效果树结构
"""

from logging import getLogger

from pyradox import Tree

from core.datatype import CountryEffect
from core.analysis.effect.base import EffectAnalysisBase

logger = getLogger(__name__)


class EffectAnalysisDefault(EffectAnalysisBase):
    """!
    @brief 默认国家效果分析器
    @details 实现具体的国家效果分析逻辑，解析国家效果树结构
    """

    def analysis(self, tree: Tree, country_tag: str, country_name: str) -> CountryEffect:
        """!
        @brief 分析国家效果树，提取国家效果数据
        @details 遍历树中的每个节点，提取国家名称、效果和特殊效果信息
                 - effect字段存储值为yes的情况
                 - special_effect字段存储值为其他的情况（键值对）
        @param tree pyradox解析的树结构
        @param country_tag 国家标签
        @param country_name 国家名称
        @return 国家效果对象
        """
        logger.debug(f"Analyzing effect for country '{country_tag}'")
        effect: list[str] = []
        special_effect: list[tuple[str, str]] = []

        for key, value in tree.items():
            # 处理效果字段
            if value is True or (isinstance(value, str) and value.lower() == 'yes'):
                effect.append(key)
            else:
                if isinstance(value, Tree):
                    special_effect.append((key, f'{{\n{value}}}'))
                else:
                    special_effect.append((key, str(value)))

        logger.debug(f"Created effect for '{country_tag}' with {len(effect)} effects and {len(special_effect)} special effects")
        country_effect = CountryEffect(
            country_tag=country_tag,
            country_name=country_name,
            effect=tuple(effect),
            special_effect=tuple(special_effect)
        )

        return country_effect


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('effect', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\countries'))
    manager.collect_file('effect', '.txt')

    analysis = EffectAnalysisDefault()
    analysis.main(manager, 'effect')

    print(analysis.effect)