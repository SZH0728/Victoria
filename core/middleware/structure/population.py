# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from core.datatype.prefix import CountryTagPrefix, StateNamePrefix, RegionStatePrefix
from core.datatype.source.population import PopulationFile, PopulationRegion, PopulationCountry, PopulationItem
from core.datatype.structure.population import StructuredRegionPopulation, StructuredPopulationItem
from core.middleware.base import StructureBase

logger = getLogger(__name__)


class StructurePopulationDefault(StructureBase):
    """
    @brief 人口数据结构化转换类
    @details 将PopulationFile字典转换为以国家为键的结构化数据字典
    转换逻辑: dict[str, PopulationFile] → dict[RegionStatePrefix, StructuredRegionPopulation]
    输入直接兼容: analysis.population.AnalysisPopulationDefault().result
    """
    def convert(self, source_dict: dict[str, PopulationFile]) -> dict[RegionStatePrefix, StructuredRegionPopulation]:
        """
        @brief 转换人口源数据为结构化数据
        @param source_dict 源数据字典，键为文件名，值为PopulationFile对象
        @return 结构化数据字典，键为区域状态前缀，值为StructuredRegionPopulation对象
        """
        result: dict[RegionStatePrefix, StructuredRegionPopulation] = {}

        for filename, population_file in source_dict.items():
            logger.debug(f"Processing file: {filename}")

            for state_name_prefix, population_state in population_file.population_region_dict.items():
                for region_state_prefix, population_country in population_state.population_country_dict.items():
                    if region_state_prefix not in result:
                        result[region_state_prefix] = StructuredRegionPopulation(state_population_dict={})

                    if state_name_prefix not in result[region_state_prefix].state_population_dict:
                        result[region_state_prefix].state_population_dict[state_name_prefix] = list(population_country.create_pop)
                    else:
                        result[region_state_prefix].state_population_dict[state_name_prefix].extend(population_country.create_pop)

        return result


if __name__ == '__main__':
    pass