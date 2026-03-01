# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.process.modify.population.merge
@brief 人口合并修改器模块
@details 根据州合并结果更新人口数据的国家标签
"""

from typing import Any

from core.datatype.map import Map
from core.datatype.population import RegionPopulation
from core.process.modify.population.base import PopulationModifyBase


class PopulationModifyMerge(PopulationModifyBase):
    """!
    @brief 人口合并修改器
    @details 根据州合并结果更新人口数据的国家标签，将合并后的人口数据与新的国家标签关联
    """
    population: Map[RegionPopulation] = Map()  #!< 人口数据映射（类属性）

    def modify(self) -> Any:
        """!
        @brief 执行人口合并修改
        @details 根据州合并结果更新人口数据的国家标签：
                 1. 遍历中间数据中的国家-州映射（country_state）
                 2. 对于每个国家标签下的每个州
                 3. 从合并后的人口数据中获取对应州的人口数据
                 4. 更新人口数据的国家标签为新的标签
                 5. 存储到新的人口映射中

        @return 更新后的区域人口映射 Map[RegionPopulation]
        """
        population_map: Map[RegionPopulation] = Map()
        for tag, name_list in self.middle['country_state'].items():
            for name in name_list:
                region_population: RegionPopulation = self.middle['population_merged'][name]
                region_population.population[0].country_tag = tag
                population_map[name] = region_population

        return population_map

if __name__ == '__main__':
    pass
