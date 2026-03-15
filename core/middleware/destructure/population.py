# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from core.datatype.prefix import CountryTagPrefix, StateNamePrefix, RegionStatePrefix
from core.datatype.source.population import PopulationFile, PopulationRegion, PopulationCountry, PopulationItem
from core.datatype.structure.population import StructuredRegionPopulation, StructuredPopulationItem
from core.middleware.base import DestructureBase

logger = getLogger(__name__)


class DestructurePopulationDefault(DestructureBase):
    """
    @brief 人口数据解构转换类
    @details 将以区域状态为键的结构化数据字典转换回PopulationFile字典
    转换逻辑: dict[RegionStatePrefix, StructuredRegionPopulation] → dict[str, PopulationFile]
    输出直接兼容: transform.population.TransformPopulationDefault().main()的输入
    """
    def convert(self, structure_dict: dict[RegionStatePrefix, StructuredRegionPopulation]) -> dict[str, PopulationFile]:
        """
        @brief 转换结构化数据回源数据
        @param structure_dict 结构化数据字典，键为区域状态前缀，值为StructuredRegionPopulation对象
        @return 源数据字典，键为文件名，值为PopulationFile对象
        """
        result: dict[str, PopulationFile] = {}

        filename: str = '80_population.txt'
        raw_data_dict: dict[StateNamePrefix, dict[RegionStatePrefix, list[PopulationItem]]] = {}
        population_state_dict: dict[StateNamePrefix, PopulationRegion] = {}

        for region_state_prefix, structured_region_population in structure_dict.items():
            for state_name_prefix, structured_region_population_list in structured_region_population.state_population_dict.items():
                if state_name_prefix not in raw_data_dict:
                    raw_data_dict[state_name_prefix] = {}

                if region_state_prefix not in raw_data_dict[state_name_prefix]:
                    raw_data_dict[state_name_prefix][region_state_prefix] = []

                raw_data_dict[state_name_prefix][region_state_prefix].extend(structured_region_population_list)

        for state_name_prefix, state_population_dict in raw_data_dict.items():
            for region_state_prefix, population_item_list in state_population_dict.items():
                if state_name_prefix not in population_state_dict:
                    population_state_dict[state_name_prefix] = PopulationRegion(population_country_dict={})

                if region_state_prefix not in population_state_dict[state_name_prefix].population_country_dict:
                    population_state_dict[state_name_prefix].population_country_dict[region_state_prefix] = PopulationCountry(create_pop=tuple(population_item_list))
                else:
                    population_state_dict[state_name_prefix].population_country_dict[region_state_prefix] = PopulationCountry(
                        create_pop=population_state_dict[state_name_prefix].population_country_dict[region_state_prefix].create_pop + tuple(population_item_list),
                    )

        result[filename] = PopulationFile(root_key='POPS', population_region_dict=population_state_dict)

        return result


if __name__ == '__main__':
    pass