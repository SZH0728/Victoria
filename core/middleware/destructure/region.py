# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from core.datatype.prefix import RegionNamePrefix
from core.datatype.source.region import RegionFile
from core.datatype.structure.region import StructuredRegionItem
from core.middleware.base import DestructureBase

logger = getLogger(__name__)


class DestructureRegion(DestructureBase):
    """
    @brief 区域数据解构转换类
    @details 将结构化区域数据字典转换回RegionFile字典
    转换逻辑: dict[RegionNamePrefix, StructuredRegionItem] → dict[str, RegionFile]
    注意: 区域数据结构未发生变更，StructuredRegionItem = RegionItem
    """
    def convert(self, structure_dict: dict[RegionNamePrefix, StructuredRegionItem]) -> dict[str, RegionFile]:
        """
        @brief 转换结构化数据回源数据
        @param structure_dict 结构化数据字典，键为区域名称，值为RegionItem对象
        @return 源数据字典，键为文件名，值为RegionFile对象
        """
        result: dict[str, RegionFile] = {}
        filename = "strategic_regions.txt"
        result[filename] = RegionFile(root_key=None, region_item_dict=structure_dict)
        return result


if __name__ == '__main__':
    pass