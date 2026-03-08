# -*- coding:utf-8 -*-
# AUTHOR: Sun

from pyradox import Tree

from core.datatype.population import PopulationFile, PopulationRegion, PopulationCountry, PopulationItem
from core.transform.base import TransformBase


class TransformPopulationDefault(TransformBase):

    @staticmethod
    def transform_population_item(population_item: PopulationItem) -> Tree:
        tree = Tree()

        # size should always be present
        tree['size'] = population_item.size
        if population_item.culture is not None:
            tree['culture'] = population_item.culture
        if population_item.religion is not None:
            tree['religion'] = population_item.religion
        if population_item.pop_type is not None:
            tree['pop_type'] = population_item.pop_type

        return tree

    def transform_country_population(self, country_population: PopulationCountry) -> Tree:
        tree = Tree()

        for population_item in country_population.create_pop:
            tree.append('create_pop', self.transform_population_item(population_item))

        return tree

    def transform_population_region(self, population_region: PopulationRegion) -> Tree:
        tree = Tree()

        for region_state_prefix, country_population in population_region.population_country_dict.items():
            tree[region_state_prefix.prefix_string] = self.transform_country_population(country_population)

        return tree

    def transform(self, target: PopulationFile) -> Tree:
        tree = Tree()

        root_key = target.root_key if target.root_key is not None else 'POPS'
        tree[root_key] = Tree()

        for state_name_prefix, population_region in target.population_region_dict.items():
            tree[root_key][state_name_prefix.prefix_string] = self.transform_population_region(population_region)

        return tree


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager
    from core.analysis.population import AnalysisPopulationDefault

    manager = FileManager()
    manager.create_group('population', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\pops'))
    manager.collect_file('population', '.txt')

    manager.create_group('new_population', Path(r'C:\Users\User\Documents\Paradox Interactive\Victoria 3\mod\Alternate World\common\history\pops'))

    analysis = AnalysisPopulationDefault()
    analysis.main(manager, 'population')

    transform = TransformPopulationDefault()
    transform.main(manager, 'new_population', analysis.result)