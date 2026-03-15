# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from core.datatype.prefix import StateNamePrefix, RegionStatePrefix
from core.datatype.source.building import BuildingFile, BuildingState, BuildingCountry, BuildingItem, BuildingNoOwnerItem
from core.datatype.structure.building import StructuredBuildingState
from core.middleware.base import DestructureBase

logger = getLogger(__name__)


class DestructureBuildingDefault(DestructureBase):
    """
    @brief 建筑数据解构转换类
    @details 将以区域状态为键的结构化数据字典转换回BuildingFile字典
    转换逻辑: dict[RegionStatePrefix, StructuredBuildingState] → dict[str, BuildingFile]
    输出直接兼容: transform.building.TransformBuildingDefault().main()的输入
    """
    def convert(self, structure_dict: dict[RegionStatePrefix, StructuredBuildingState]) -> dict[str, BuildingFile]:
        """
        @brief 转换结构化数据回源数据
        @param structure_dict 结构化数据字典，键为区域状态前缀，值为StructuredBuildingState对象
        @return 源数据字典，键为文件名，值为BuildingFile对象
        """
        result: dict[str, BuildingFile] = {}

        filename = '80_buildings.txt'
        raw_data_dict: dict[StateNamePrefix, dict[RegionStatePrefix, list[BuildingItem | BuildingNoOwnerItem]]] = {}
        building_state_dict: dict[StateNamePrefix, BuildingState] = {}

        for region_state_prefix, structured_building_state in structure_dict.items():
            for state_name_prefix, structured_building_item_list in structured_building_state.state_building_dict.items():
                if state_name_prefix not in raw_data_dict:
                    raw_data_dict[state_name_prefix] = {}

                if region_state_prefix not in raw_data_dict[state_name_prefix]:
                    raw_data_dict[state_name_prefix][region_state_prefix] = []

                raw_data_dict[state_name_prefix][region_state_prefix].extend(structured_building_item_list)

        for state_name_prefix, state_building_dict in raw_data_dict.items():
            for region_state_prefix, building_item_list in state_building_dict.items():
                if state_name_prefix not in building_state_dict:
                    building_state_dict[state_name_prefix] = BuildingState(building_country_dict={})

                if region_state_prefix not in building_state_dict[state_name_prefix].building_country_dict:
                    building_state_dict[state_name_prefix].building_country_dict[region_state_prefix] = BuildingCountry(create_building=tuple(building_item_list))
                else:
                    building_state_dict[state_name_prefix].building_country_dict[region_state_prefix] = BuildingCountry(
                        create_building=building_state_dict[state_name_prefix].building_country_dict[region_state_prefix].create_building + tuple(building_item_list),
                    )

        result[filename] = BuildingFile(root_key='BUILDINGS', building_state_dict=building_state_dict)

        return result


if __name__ == '__main__':
    pass
