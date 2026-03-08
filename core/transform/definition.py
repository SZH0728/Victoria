# -*- coding:utf-8 -*-
# AUTHOR: Sun

from pyradox import Tree

from core.datatype.definition import DefinitionFile
from core.transform.base import TransformBase


class TransformDefinitionDefault(TransformBase):

    def transform(self, target: DefinitionFile) -> Tree:
        tree = Tree()

        for country_tag, country_definition in target.definition_country_dict.items():
            country_tree = Tree()

            # 处理颜色 - 使用append with in_group=True生成花括号格式
            if country_definition.color:
                for color_value in country_definition.color:
                    country_tree.append('color', color_value, in_group=True)

            # 处理国家类型
            if country_definition.country_type:
                country_tree['country_type'] = country_definition.country_type

            # 处理等级
            if country_definition.tier:
                country_tree['tier'] = country_definition.tier

            # 处理文化
            if country_definition.cultures:
                for culture in country_definition.cultures:
                    country_tree.append('cultures', culture, in_group=True)

            # 处理首都
            if country_definition.capital:
                country_tree['capital'] = country_definition.capital.prefix_string

            # 处理可选字段
            if country_definition.religion is not None:
                country_tree['religion'] = country_definition.religion

            if country_definition.is_named_from_capital is not None and country_definition.is_named_from_capital:
                country_tree['is_named_from_capital'] = 'yes'

            if country_definition.valid_as_home_country_for_separatists is not None:
                country_tree['valid_as_home_country_for_separatists'] = country_definition.valid_as_home_country_for_separatists

            if country_definition.social_hierarchy is not None:
                country_tree['social_hierarchy'] = country_definition.social_hierarchy

            # 处理单位颜色
            if country_definition.unit_color:
                for key, color_tuple in country_definition.unit_color.items():
                    for item in color_tuple:
                        country_tree.append(key, item, in_group=True)

            tree[country_tag.original_string.upper()] = country_tree

        return tree


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager
    from core.analysis.definition import AnalysisDefinitionDefault

    manager = FileManager()
    manager.create_group('definition', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\country_definitions'))
    manager.collect_file('definition', '.txt')

    manager.create_group('new_definition', Path(r'C:\Users\User\Documents\Paradox Interactive\Victoria 3\mod\Alternate World\common\country_definitions'))

    analysis = AnalysisDefinitionDefault()
    analysis.main(manager, 'definition')

    transform = TransformDefinitionDefault()
    transform.main(manager, 'new_definition', analysis.result)