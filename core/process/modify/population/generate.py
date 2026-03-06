# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.process.modify.population.generate
@brief 人口数量生成修改器模块
@details 根据配置生成新的人口数量，支持默认、固定和随机模式
"""

from typing import Any
from random import randint

from core.datatype.map import Map
from core.datatype.population import RegionPopulation, CountryPopulation, PopulationItem
from core.datatype.combination import DataGenerateType
from core.process.modify.population.base import PopulationModifyBase


class PopulationModifyGenerate(PopulationModifyBase):
    """!
    @brief 人口数量生成修改器
    @details 根据配置生成新的人口数量，支持三种模式：
             1. default模式：保留原人口数量
             2. fix模式：固定为指定总人口数量
             3. randomize模式：在指定范围内随机生成总人口数量
             生成新总人口后，按原有人口比例分配至每个具体人口项
    """
    def modify(self) -> Any:
        """!
        @brief 执行人口数量生成修改
        @details 根据配置生成新的人口数量：
                 1. 从中间参数获取配置（生成模式、固定值、随机范围等）
                 2. 遍历合并后的人口数据（population_merged）
                 3. 计算每个区域的原总人口
                 4. 根据配置计算新总人口
                 5. 按比例分配新人口到每个具体人口项
                 6. 构建新的区域人口映射

        @return 更新后的区域人口映射 Map[RegionPopulation]
        """
        # 获取配置参数
        generate_function = self.middle.get('population_generate_function', DataGenerateType.default)
        population_fix: int = self.middle.get('population_fix', 1000000)
        population_random_range: tuple[int, int] = self.middle.get('population_random_range', (100000, 10000000))

        # 确保随机范围有效
        if population_random_range[0] > population_random_range[1]:
            population_random_range = (population_random_range[1], population_random_range[0])

        # 处理每个区域的人口数据
        population_map: Map[RegionPopulation] = Map()
        for region_name, region_population in self.middle['population_merged'].items():
            region_population: RegionPopulation

            if generate_function == DataGenerateType.default:
                population_map[region_name] = region_population
                continue

            target_population = population_fix
            if generate_function == DataGenerateType.fix:
                pass
            elif generate_function == DataGenerateType.randomize:
                target_population = randint(population_random_range[0], population_random_range[1])

            total_population: int = 0

            for country_population in region_population.population:
                for population_item in country_population.population:
                    total_population += population_item.size

            for country_population in region_population.population:
                for population_item in country_population.population:
                    population_item.size = int(population_item.size / total_population * target_population)

            population_map[region_name] = region_population

        for tag, name_list in self.middle['country_state'].items():
            for name in name_list:
                region_population: RegionPopulation = population_map[name]
                region_population.population[0].country_tag = tag

        return population_map


if __name__ == '__main__':
    pass