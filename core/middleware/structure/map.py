# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from core.datatype.prefix import StateNamePurePrefix
from core.datatype.source.map import MapFile, MapRegion, MapResource
from core.datatype.structure.map import StructuredMapRegion, StructuredMapResource
from core.middleware.base import StructureBase

logger = getLogger(__name__)


class StructureMap(StructureBase):
    """
    @brief 地图数据结构化转换类
    @details 将MapFile字典转换为结构化数据字典
    转换逻辑: dict[str, MapFile] → dict[StateNamePurePrefix, StructuredMapRegion]
    注意: 地图数据结构未发生变更，StructuredMapRegion = MapRegion, StructuredMapResource = MapResource
    """
    def convert(self, source_dict: dict[str, MapFile]) -> dict[StateNamePurePrefix, StructuredMapRegion]:
        """
        @brief 转换地图源数据为结构化数据
        @param source_dict 源数据字典，键为文件名，值为MapFile对象
        @return 结构化数据字典，键为州名称（纯前缀），值为MapRegion对象
        """
        result: dict[StateNamePurePrefix, StructuredMapRegion] = {}
        for filename, map_file in source_dict.items():
            logger.debug(f"Processing file: {filename}")

            for state_name, map_region in map_file.map_region_dict.items():
                if state_name not in result:
                    result[state_name] = map_region
                else:
                    logger.warning(f"Map region '{state_name}' already exists in result, skipping duplicate")
        return result


if __name__ == '__main__':
    pass