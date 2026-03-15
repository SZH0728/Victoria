# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 人口收集模块
@details 提供人口数据的收集功能，按州和人口特征合并统计人口规模

此模块实现了 CollectPopulationDefault 类，用于从 StructureSummary 中
提取人口数据，按州和人口特征（文化、宗教、类型）进行合并统计，
相同特征的人口规模相加，并计算州级和全局总人口。
"""

from typing import Dict, List, Tuple, Any, Optional
from logging import getLogger

from core.collect.base import CollectBase
from core.datatype.summarize import SourceSummary, StructureSummary
from core.datatype.prefix import StateNamePrefix, RegionStatePrefix
from core.datatype.collect.population import CollectPopulationStateItem, CollectPopulationResult
from core.datatype.structure.population import StructuredRegionPopulation
from core.datatype.source.population import PopulationItem

logger = getLogger(__name__)


class CollectPopulationDefault(CollectBase):
    """
    @brief 人口收集默认实现类
    @details 从 StructureSummary 中提取人口数据，按州和人口特征进行合并统计
    """

    def collect(self, source_summary: SourceSummary, structure_summary: StructureSummary) -> Tuple[str, Any]:
        """
        @brief 收集人口数据
        @details 从 StructureSummary 中提取人口数据，按州和人口特征进行合并统计

        @param source_summary 原始数据汇总对象（此实现中未使用）
        @param structure_summary 结构化数据汇总对象，包含人口数据
        @return 元组 ("population", CollectPopulationResult)
        """
        logger.info("Starting population data collection")

        # 初始化数据结构
        population_stats_dict: dict[StateNamePrefix, dict[Tuple[str, str, str], int]] = {}
        state_population_dict: dict[StateNamePrefix, list[CollectPopulationStateItem]] = {}
        state_total: dict[StateNamePrefix, int] = {}

        for population_file in source_summary.population_files.values():
            for state_name_prefix, population_region in population_file.population_region_dict.items():
                if state_name_prefix not in population_stats_dict:
                    population_stats_dict[state_name_prefix] = {}

                if state_name_prefix not in state_total:
                    state_total[state_name_prefix] = 0

                for _, population_country in population_region.population_country_dict.items():
                    for population_item in population_country.create_pop:
                        feature = (population_item.culture or '', population_item.religion or '', population_item.pop_type or '')
                        if feature not in population_stats_dict[state_name_prefix]:
                            population_stats_dict[state_name_prefix][feature] = 0

                        population_stats_dict[state_name_prefix][feature] += population_item.size
                        state_total[state_name_prefix] += population_item.size

        for state_name_prefix, population_dict in population_stats_dict.items():
            if state_name_prefix not in state_population_dict:
                state_population_dict[state_name_prefix] = []

            for feature, size in population_dict.items():
                collect_population_state_item = CollectPopulationStateItem(*(feature + (size,)))
                state_population_dict[state_name_prefix].append(collect_population_state_item)

        result = CollectPopulationResult(state_population_dict, state_total)

        return 'population', result


if __name__ == '__main__':
    pass