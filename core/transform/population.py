# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from pyradox import Tree

from core.datatype.population import PopulationFile, PopulationRegion, PopulationCountry, PopulationItem
from core.transform.base import TransformBase

logger = getLogger(__name__)


class TransformPopulationDefault(TransformBase):
    """
    @brief 人口数据转换类
    @details 将PopulationFile对象转换回pyradox Tree对象，用于写入游戏数据文件
    """

    @staticmethod
    def transform_population_item(population_item: PopulationItem) -> Tree:
        """
        @brief 转换人口项数据
        @details 将PopulationItem对象转换为pyradox Tree对象
        @param population_item 人口项数据对象
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of population item")
        tree = Tree()

        # size should always be present
        tree['size'] = population_item.size
        logger.debug(f"Set size: {population_item.size}")

        if population_item.culture is not None:
            tree['culture'] = population_item.culture
            logger.debug(f"Set culture: {population_item.culture}")

        if population_item.religion is not None:
            tree['religion'] = population_item.religion
            logger.debug(f"Set religion: {population_item.religion}")

        if population_item.pop_type is not None:
            tree['pop_type'] = population_item.pop_type
            logger.debug(f"Set pop_type: {population_item.pop_type}")

        logger.debug(f"Population item transformation completed")
        return tree

    def transform_country_population(self, population_country: PopulationCountry) -> Tree:
        """
        @brief 转换国家人口数据
        @details 将PopulationCountry对象转换为pyradox Tree对象
        @param population_country 国家人口数据对象
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of country population")
        tree = Tree()

        for population_item in population_country.create_pop:
            logger.debug(f"Processing population item: {population_item}")
            tree.append('create_pop', self.transform_population_item(population_item))

        logger.debug(f"Country population transformation completed, total pops: {len(population_country.create_pop)}")
        return tree

    @staticmethod
    def transform_population_region(population_region: PopulationRegion) -> Tree:
        """
        @brief 转换人口区域数据
        @details 将PopulationRegion对象转换为pyradox Tree对象
        @param population_region 人口区域数据对象
        @return 转换后的Tree对象
        """
        logger.debug(f"Starting transformation of population region")
        tree = Tree()

        for region_state_prefix, country_population in population_region.population_country_dict.items():
            logger.debug(f"Processing country population for region: {region_state_prefix.prefix_string}")
            tree[region_state_prefix.prefix_string] = TransformPopulationDefault.transform_country_population(country_population)

        logger.debug(f"Population region transformation completed, total regions: {len(population_region.population_country_dict)}")
        return tree

    def transform(self, target: PopulationFile) -> Tree:
        """
        @brief 转换人口数据文件
        @details 将PopulationFile对象转换为完整的pyradox Tree对象，包含根键和所有人口区域数据
        @param target 人口数据文件对象
        @return 转换后的Tree对象
        @throws TypeError 如果target不是PopulationFile类型
        """
        logger.debug(f"Starting transformation of population file: {target}")

        self.raise_for_incorrect_type(target, PopulationFile)
        tree, inner_tree = self.create_tree(target.root_key)

        for state_name_prefix, population_region in target.population_region_dict.items():
            logger.debug(f"Transforming population region for key: {state_name_prefix.prefix_string}")
            inner_tree[state_name_prefix.prefix_string] = self.transform_population_region(population_region)

        logger.info(f"Population file transformation completed, total states: {len(target.population_region_dict)}")
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
