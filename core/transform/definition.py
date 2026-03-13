# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from pyradox import Tree

from core.datatype.source.definition import DefinitionFile, DefinitionCountry
from core.transform.base import TransformBase

logger = getLogger(__name__)


class TransformDefinitionDefault(TransformBase):
    """
    @brief 国家定义数据转换类
    @details 将DefinitionFile对象转换回pyradox Tree对象，用于写入游戏数据文件
    """
    @staticmethod
    def transform_definition_country(definition_country: DefinitionCountry) -> Tree:
        """
        @brief 转换单个国家定义数据
        @details 将DefinitionCountry对象转换为pyradox Tree对象，包含颜色、类型、文化等字段
        @param definition_country 国家定义数据对象
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of definition country")
        country_tree = Tree()


        for color_value in definition_country.color:
            country_tree.append('color', color_value, in_group=True)
            logger.debug(f"Added color value: {color_value}")


        country_tree['country_type'] = definition_country.country_type
        logger.debug(f"Set country_type: {definition_country.country_type}")

        country_tree['tier'] = definition_country.tier
        logger.debug(f"Set tier: {definition_country.tier}")

        for culture in definition_country.cultures:
            country_tree.append('cultures', culture, in_group=True)
            logger.debug(f"Added culture: {culture}")

        if definition_country.capital is not None:
            country_tree['capital'] = definition_country.capital.prefix_string
            logger.debug(f"Set capital: {definition_country.capital.prefix_string}")

        if definition_country.religion is not None:
            country_tree['religion'] = definition_country.religion
            logger.debug(f"Set religion: {definition_country.religion}")

        if definition_country.is_named_from_capital is not None and definition_country.is_named_from_capital:
            country_tree['is_named_from_capital'] = 'yes'
            logger.debug(f"Set is_named_from_capital: yes")

        if definition_country.valid_as_home_country_for_separatists is not None and definition_country.valid_as_home_country_for_separatists:
            country_tree['valid_as_home_country_for_separatists'] = 'yes'
            logger.debug(f"Set valid_as_home_country_for_separatists: yes")

        if definition_country.social_hierarchy is not None:
            country_tree['social_hierarchy'] = definition_country.social_hierarchy
            logger.debug(f"Set social_hierarchy: {definition_country.social_hierarchy}")

        # 处理单位颜色
        if definition_country.unit_color:
            for key, color_tuple in definition_country.unit_color.items():
                for item in color_tuple:
                    country_tree.append(key, item, in_group=True)
                    logger.debug(f"Added unit color {key}: {item}")

        logger.debug(f"Definition country transformation completed")
        return country_tree

    def transform(self, target: DefinitionFile) -> Tree:
        """
        @brief 转换国家定义数据文件
        @details 将DefinitionFile对象转换为完整的pyradox Tree对象，包含所有国家定义
        @param target 国家定义数据文件对象
        @return 转换后的Tree对象
        @throws TypeError 如果target不是DefinitionFile类型
        """
        logger.debug(f"Starting transformation of definition file: {target}")

        self.raise_for_incorrect_type(target, DefinitionFile)
        tree, inner_tree = self.create_tree(target.root_key)

        for country_tag, definition_country in target.definition_country_dict.items():
            logger.debug(f"Processing country definition for tag: {country_tag.original_string.upper()}")
            country_tree = self.transform_definition_country(definition_country)
            inner_tree[country_tag.original_string.upper()] = country_tree
            logger.debug(f"Added country tree for tag: {country_tag.original_string.upper()}")

        logger.info(f"Definition file transformation completed, total countries: {len(target.definition_country_dict)}")
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
