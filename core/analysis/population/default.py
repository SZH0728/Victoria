# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from pyradox import Tree

from core.datatype import PopulationItem, CountryPopulation, RegionPopulation
from core.analysis.population.base import PopulationAnalysisBase

logger = getLogger(__name__)


class PopulationAnalysisDefault(PopulationAnalysisBase):
    """!
    @brief 默认人口分析器
    @details 实现具体的人口分析逻辑，解析人口树结构
    """
    @staticmethod
    def analysis_population(tree: Tree) -> PopulationItem:
        """!
        @brief 分析人口树，提取人口项数据
        @details 遍历树中的每个节点，提取人口规模、文化、宗教和人口类型信息
        @param tree pyradox解析的树结构
        @return 人口项对象
        """
        logger.debug("Analyzing population tree")
        size: int = 0
        culture: str | None = None
        religion: str | None = None
        population_type: str | None = None

        for key, value in tree.items():
            if isinstance(value, Tree):
                value = str(value)

            if key == 'size':
                size = value
            elif key == 'culture':
                culture = value
            elif key == 'religion':
                religion = value
            elif key == 'pop_type':
                population_type = value
            else:
                logger.warning(f"Unknown key '{key}' in population")

        logger.debug(f"Created population item with size {size}, culture {culture}, religion {religion}, type {population_type}")
        population_item = PopulationItem(
            size=size,
            culture=culture,
            religion=religion,
            population_type=population_type
        )
        return population_item

    def analysis_country(self, tree: Tree, country_tag: str) -> CountryPopulation:
        """!
        @brief 分析国家人口树，提取国家人口数据
        @details 遍历树中的每个节点，提取人口项列表
        @param tree pyradox解析的树结构
        @param country_tag 国家标签
        @return 国家人口对象
        """
        logger.debug(f"Analyzing country population for tag '{country_tag}'")
        population: list[PopulationItem] = []

        for key, value in tree.items():
            if key == 'create_pop':
                population.append(self.analysis_population(value))
            else:
                # 如果值是Tree节点，转换为字符串
                if isinstance(value, Tree):
                    logger.warning(f"Unknown key '{key}' in country {country_tag}, value converted from Tree to string")
                else:
                    logger.warning(f"Unknown key '{key}' in country {country_tag}")

        logger.debug(f"Created country population for tag '{country_tag}' with {len(population)} population items")
        country_population = CountryPopulation(
            country_tag=country_tag,
            population=tuple(population)
        )

        return country_population

    def analysis(self, tree: Tree, state_name: str) -> RegionPopulation:
        """!
        @brief 分析人口树，提取区域人口数据
        @details 遍历树中的每个节点，根据键前缀调用相应的国家人口分析方法
        @param tree pyradox解析的树结构
        @param state_name 州名称
        @return 区域人口对象
        """
        logger.debug(f"Analyzing population tree for state '{state_name}'")
        population: list[CountryPopulation] = []

        for key, value in tree.items():
            if key.startswith('region_state:'):
                country_tag = self.extract_country_tag_from_key(key)
                population.append(self.analysis_country(value, country_tag))
            else:
                # 如果值是Tree节点，转换为字符串
                if isinstance(value, Tree):
                    logger.warning(f"Unknown key '{key}' in state {state_name}, value converted from Tree to string")
                else:
                    logger.warning(f"Unknown key '{key}' in state {state_name}")

        logger.debug(f"Created region population for state '{state_name}' with {len(population)} countries")
        region_population = RegionPopulation(
            region=state_name,
            population=tuple(population)
        )
        return region_population


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('population', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\pops'))
    manager.collect_file('population', '.txt')

    analysis = PopulationAnalysisDefault()
    analysis.main(manager, 'population')
    print(analysis.population)

