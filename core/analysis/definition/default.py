# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@file default.py
@brief 默认国家定义分析器
@details 实现具体的国家定义分析逻辑，解析国家定义树结构
"""

from logging import getLogger

from pyradox import Tree

from core.datatype import CountryDefinition
from core.analysis.definition.base import DefinitionAnalysisBase

logger = getLogger(__name__)


class DefinitionAnalysisDefault(DefinitionAnalysisBase):
    """!
    @brief 默认国家定义分析器
    @details 实现具体的国家定义分析逻辑，解析国家定义树结构
    """

    def analysis(self, tree: Tree, country_tag: str) -> CountryDefinition:
        """!
        @brief 分析国家定义树，提取国家定义数据
        @details 遍历树中的每个节点，提取国家标签、颜色、等级、文化、首都等信息
        @param tree pyradox解析的树结构
        @param country_tag 国家标签
        @return 国家定义对象
        """
        logger.debug(f"Analyzing definition for country '{country_tag}'")
        color: list[int] = []
        country_type: str = ''
        tier: str = ''
        capital: str = ''
        culture: list[str] = []

        religion: str | None = None
        is_named_from_capital: bool | None = None
        valid_as_home_country_for_separatists: str | None = None
        social_hierarchy: str | None = None
        unit_color: dict[str, list[int] | tuple[int, ...]] | None = {}

        for key, value in tree.items():
            if isinstance(value, Tree):
                value = str(value)

            if key == 'color':
                color.append(value)
            elif key == 'tier':
                tier = value
            elif key == 'country_type':
                country_type = value
            elif key == 'capital':
                capital = value
            elif key == 'cultures':
                culture.append(value)

            elif key == 'religion':
                religion = value
            elif key == 'is_named_from_capital':
                if isinstance(value, bool):
                    is_named_from_capital = value
                else:
                    is_named_from_capital = (value == 'yes')
            elif key == 'valid_as_home_country_for_separatists':
                valid_as_home_country_for_separatists = str(value)
            elif key == 'social_hierarchy':
                social_hierarchy = str(value)
            elif 'unit_color' in key:
                if key not in unit_color:
                    unit_color[key] = []
                unit_color[key].append(value)
            else:
                logger.warning(f"Unknown key '{key}' in country definition '{country_tag}'")

        unit_color = {key: tuple(value) for key, value in unit_color.items()} if unit_color else None

        logger.debug(f"Created definition for '{country_tag}' with type '{country_type}'")
        country_def = CountryDefinition(
            country_tag=country_tag,
            color=tuple(color),
            country_type=country_type,
            tier=tier,
            culture=tuple(culture),
            capital=capital,
            religion=religion,
            is_named_from_capital=is_named_from_capital,
            valid_as_home_country_for_separatists=valid_as_home_country_for_separatists,
            social_hierarchy=social_hierarchy,
            unit_color=unit_color
        )

        return country_def


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    # 示例用法
    manager = FileManager()
    # 假设文件路径，根据用户提供的路径调整
    manager.create_group('definition', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\country_definitions'))
    manager.collect_file('definition', '.txt')

    analysis = DefinitionAnalysisDefault()
    analysis.main(manager, 'definition')
    print(analysis.definition)