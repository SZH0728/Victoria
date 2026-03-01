# -*- coding:utf-8 -*-
# AUTHOR: Sun

from pyradox import Tree

from core.datatype import RegionPopulation, CountryPopulation, PopulationItem
from core.transform.population.base import PopulationTransformBase


class PopulationTransformDefault(PopulationTransformBase):
    """!
    @brief 默认人口转换器
    @details 实现具体的人口转换逻辑，将人口数据对象转换为pyradox树
    """

    @staticmethod
    def transform_population_item(population_item: PopulationItem) -> Tree:
        """!
        @brief 转换人口条目对象为pyradox树
        @details 处理人口条目的所有字段，包括规模、文化、宗教、人口类型等
        @param population_item 人口条目对象
        @return 转换后的树
        """
        tree = Tree()

        # size should always be present
        tree['size'] = population_item.size
        if population_item.culture is not None:
            tree['culture'] = population_item.culture
        if population_item.religion is not None:
            tree['religion'] = population_item.religion
        if population_item.population_type is not None:
            tree['pop_type'] = population_item.population_type

        return tree

    def transform_country_population(self, country_population: CountryPopulation) -> Tree:
        """!
        @brief 转换国家人口对象为pyradox树
        @details 遍历国家人口中的所有人口条目，转换为create_pop结构
        @param country_population 国家人口对象
        @return 转换后的树
        """
        tree = Tree()

        for population_item in country_population.population:
            tree.append('create_pop', self.transform_population_item(population_item))

        return tree

    def transform(self, region_population: RegionPopulation) -> Tree:
        """!
        @brief 转换区域人口对象为pyradox树
        @details 实现抽象方法，遍历区域人口中的每个国家人口，使用国家标签作为键
        @param region_population 区域人口对象
        @return 转换后的树
        """
        tree = Tree()

        for country_population in region_population.population:
            country_key = self.combine_country_key_for_region_state(country_population.country_tag)
            tree[country_key] = self.transform_country_population(country_population)

        return tree


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager
    from core.analysis.population.default import PopulationAnalysisDefault

    manager = FileManager()
    manager.create_group('population', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\pops'))
    manager.collect_file('population', '.txt')

    manager.create_group('new_population', Path(r'D:\poject\Victoria\common'))

    analysis = PopulationAnalysisDefault()
    analysis.main(manager, 'population')

    transform = PopulationTransformDefault()
    transform.main(manager, 'new_population', 'default.txt', analysis.population)
