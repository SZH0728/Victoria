# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from core.datatype.prefix import  RegionStatePrefix
from core.datatype.source.building import BuildingFile
from core.datatype.structure.building import StructuredBuildingState
from core.middleware.base import StructureBase

logger = getLogger(__name__)


class StructureBuildingDefault(StructureBase):
    """
    @brief 建筑数据结构化转换类
    @details 将BuildingFile字典转换为以国家为键的结构化数据字典
             转换逻辑: dict[str, BuildingFile] → dict[RegionStatePrefix, StructuredBuildingState]
             输入直接兼容: analysis.building.AnalysisBuildingDefault().result
    @note 建筑数据结构复杂，需要多层嵌套重组
    """
    def convert(self, source_dict: dict[str, BuildingFile]) -> dict[RegionStatePrefix, StructuredBuildingState]:
        """
        @brief 转换建筑源数据为结构化数据
        @param source_dict 源数据字典，键为文件名，值为BuildingFile对象
        @return 结构化数据字典，键为区域状态前缀，值为StructuredBuildingState对象
        """
        result: dict[RegionStatePrefix, StructuredBuildingState] = {}

        for filename, building_file in source_dict.items():
            logger.debug(f"Processing file: {filename}")

            for state_name_prefix, building_state in building_file.building_state_dict.items():
                for region_state_prefix, building_country in building_state.building_country_dict.items():
                    if region_state_prefix not in result:
                        result[region_state_prefix] = StructuredBuildingState(state_building_dict={})

                    if state_name_prefix not in result[region_state_prefix].state_building_dict:
                        result[region_state_prefix].state_building_dict[state_name_prefix] = list(building_country.create_building)
                    else:
                        result[region_state_prefix].state_building_dict[state_name_prefix].extend(building_country.create_building)

        return result


if __name__ == '__main__':
    pass