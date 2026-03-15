# -*- coding:utf-8 -*-
# AUTHOR: Sun

from dataclasses import dataclass

from core.datatype.prefix import StateNamePrefix
from core.datatype.source.population import PopulationItem

StructuredPopulationItem = PopulationItem


@dataclass(frozen=True)
class StructuredRegionPopulation(object):
    """
    @brief 州人口项目数据类
    @details 表示一个州内的人口信息，包含区域到区域人口的映射
    """
    state_population_dict: dict[StateNamePrefix, list[StructuredPopulationItem]]  # 区域人口字典


if __name__ == '__main__':
    pass
