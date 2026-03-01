# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any

from core.datatype import PopulationItem, CountryPopulation, RegionPopulation
from core.datatype.map import Map
from core.process.collect.base import CollectBase


class PopulationMergeCollect(CollectBase):
    """!
    @brief 人口合并收集器
    @details 合并具有相同特质（文化、宗教、人口类型）的人口，将size相加
             在同一地块（州）内进行合并，忽略国家标签
    """
    def collect(self) -> list[tuple[str, Any]]:
        """!
        @brief 收集并合并人口数据
        @details 遍历origin.population中的每个RegionPopulation，
                 合并相同特质的人口项，生成新的RegionPopulation
        @return 包含合并后人口数据的列表，格式[('population_merged', Map[RegionPopulation])]
        """
        if self.origin.population is None:
            # 如果没有人口数据，返回空映射
            return [('population_merged', Map())]

        merged_population: Map[RegionPopulation] = Map()

        for region_name, region_pop in self.origin.population.items():
            # region_name 实际上是州名称
            # 收集该州内的所有人口项
            all_items: list[PopulationItem] = []
            for country_pop in region_pop.population:
                all_items.extend(country_pop.population)

            # 按特质分组
            groups: dict[tuple[str | None, str | None, str | None], int] = {}
            for item in all_items:
                key = (item.culture, item.religion, item.population_type)
                groups[key] = groups.get(key, 0) + item.size

            # 创建合并后的人口项
            merged_items: list[PopulationItem] = []
            for (culture, religion, pop_type), total_size in groups.items():
                merged_items.append(PopulationItem(
                    size=total_size,
                    culture=culture,
                    religion=religion,
                    population_type=pop_type
                ))

            # 创建一个CountryPopulation来容纳合并后的人口项
            # 国家标签设为"merged"，因为人口可能来自多个国家
            merged_country_pop = CountryPopulation(
                country_tag="merged",
                population=tuple(merged_items)
            )

            # 创建新的RegionPopulation
            merged_region_pop = RegionPopulation(
                region=region_name,
                population=(merged_country_pop,)
            )

            merged_population[region_name] = merged_region_pop

        return [('population_merged', merged_population)]


if __name__ == '__main__':
    pass