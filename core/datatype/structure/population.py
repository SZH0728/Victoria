# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 结构化人口数据模块
@details 提供人口数据类的结构化版本别名和州人口数据结构
"""

from dataclasses import dataclass

from core.datatype.prefix import StateNamePrefix
from core.datatype.source.population import PopulationItem


StructuredPopulationItem = PopulationItem
"""
@brief 结构化人口项目数据类
@details 人口数据的结构化版本别名，与原始 PopulationItem 相同
"""


@dataclass(frozen=True)
class StructuredRegionPopulation(object):
    """
    @brief 结构化州人口数据类
    @details 表示一个州内的人口信息，以州为键映射到人口列表的字典结构

    @note 此数据结构用于按州组织人口数据，便于按州进行人口信息查询和分析
    """
    state_population_dict: dict[StateNamePrefix, list[StructuredPopulationItem]]  # 区域人口字典


if __name__ == '__main__':
    pass
