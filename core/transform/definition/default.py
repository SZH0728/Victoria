# -*- coding:utf-8 -*-
# AUTHOR: Sun

from pyradox import Tree

from core.datatype import CountryDefinition
from core.transform.definition.base import DefinitionTransformBase


class DefinitionTransformDefault(DefinitionTransformBase):
    """!
    @brief 默认国家定义转换器
    @details 实现具体的国家定义转换逻辑，将CountryDefinition对象转换为pyradox树
    """

    def transform(self, country_definition: CountryDefinition) -> Tree:
        """!
        @brief 转换国家定义对象为pyradox树
        @details 处理所有国家定义字段，包括颜色、类型、等级、文化、首都等，
                 以及可选字段如宗教、是否以首都命名等
        @param country_definition 国家定义对象
        @return 转换后的树
        """
        tree = Tree()

        # 处理颜色 - 使用append with in_group=True生成花括号格式
        if country_definition.color:
            for color_value in country_definition.color:
                tree.append('color', color_value, in_group=True)

        # 处理国家类型
        if country_definition.country_type:
            tree['country_type'] = country_definition.country_type

        # 处理等级
        if country_definition.tier:
            tree['tier'] = country_definition.tier

        # 处理文化
        if country_definition.culture:
            for culture in country_definition.culture:
                tree.append('cultures', culture, in_group=True)

        # 处理首都
        if country_definition.capital:
            tree['capital'] = country_definition.capital

        # 处理可选字段
        if country_definition.religion is not None:
            tree['religion'] = country_definition.religion

        if country_definition.is_named_from_capital is not None and country_definition.is_named_from_capital:
            tree['is_named_from_capital'] = 'yes'

        if country_definition.valid_as_home_country_for_separatists is not None:
            tree['valid_as_home_country_for_separatists'] = country_definition.valid_as_home_country_for_separatists

        if country_definition.social_hierarchy is not None:
            tree['social_hierarchy'] = country_definition.social_hierarchy

        # 处理单位颜色
        if country_definition.unit_color:
            for key, color_tuple in country_definition.unit_color.items():
                # unit_color可能是多个颜色值，使用append
                if isinstance(color_tuple, (tuple, list)):
                    for color_value in color_tuple:
                        tree.append(key, color_value, in_group=True)
                else:
                    tree[key] = color_tuple

        return tree


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager
    from core.analysis.definition.default import DefinitionAnalysisDefault

    # 示例用法
    manager = FileManager()
    # 假设文件路径，根据用户提供的路径调整
    manager.create_group('definition', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\country_definitions'))
    manager.collect_file('definition', '.txt')

    manager.create_group('new_definition', Path(r'D:\poject\Victoria\common'))

    analysis = DefinitionAnalysisDefault()
    analysis.main(manager, 'definition')

    transform = DefinitionTransformDefault()
    transform.main(manager, 'new_definition', 'default.txt', analysis.definition)