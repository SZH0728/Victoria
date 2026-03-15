# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from core.datatype.prefix import RegionNamePrefix
from core.datatype.source.region import RegionFile, RegionItem
from core.datatype.structure.region import StructuredRegionItem
from core.middleware.base import StructureBase

logger = getLogger(__name__)


class StructureRegion(StructureBase):
    """
    @brief 区域数据结构化转换类
    @details 将RegionFile字典转换为结构化数据字典
    转换逻辑: dict[str, RegionFile] → dict[RegionNamePrefix, StructuredRegionItem]
    注意: 区域数据结构未发生变更，StructuredRegionItem = RegionItem
          转换主要是为了接口一致性
    """
    def convert(self, source_dict: dict[str, RegionFile]) -> dict[RegionNamePrefix, StructuredRegionItem]:
        """
        @brief 转换区域源数据为结构化数据
        @param source_dict 源数据字典，键为文件名，值为RegionFile对象
        @return 结构化数据字典，键为区域名称，值为RegionItem对象
        """
        result: dict[RegionNamePrefix, StructuredRegionItem] = {}

        for filename, region_file in source_dict.items():
            logger.debug(f"Processing file: {filename}")

            for region_name, region_item in region_file.region_item_dict.items():
                if region_name not in result:
                    result[region_name] = region_item
                else:
                    logger.warning(f"Region '{region_name}' already exists in result, skipping duplicate")

        return result


if __name__ == '__main__':
    pass