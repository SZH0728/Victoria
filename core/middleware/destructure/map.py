# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from core.datatype.prefix import StateNamePurePrefix
from core.datatype.source.map import MapFile, MapRegion, MapResource
from core.datatype.structure.map import StructuredMapRegion, StructuredMapResource
from core.middleware.base import DestructureBase

logger = getLogger(__name__)


class DestructureMap(DestructureBase):
    """
    @brief 地图数据解构转换类
    @details 将结构化地图数据字典转换回MapFile字典
    转换逻辑: dict[StateNamePurePrefix, StructuredMapRegion] → dict[str, MapFile]
    """
    def convert(self, structure_dict: dict[StateNamePurePrefix, StructuredMapRegion]) -> dict[str, MapFile]:
        """
        @brief 转换结构化数据回源数据
        @param structure_dict 结构化数据字典，键为州名称（纯前缀），值为MapRegion对象
        @return 源数据字典，键为文件名，值为MapFile对象
        """
        result: dict[str, MapFile] = {}
        filename = "80_map.txt"
        result[filename] = MapFile(root_key=None, map_region_dict=structure_dict)
        return result


if __name__ == '__main__':
    pass