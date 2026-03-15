# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 结构化地图数据模块
@details 提供地图数据类的结构化版本别名
"""

from core.datatype.source.map import MapResource, MapRegion


StructuredMapRegion = MapRegion
"""
@brief 结构化地图区域数据类
@details 地图区域数据的结构化版本别名，与原始 MapRegion 相同
"""

StructuredMapResource = MapResource
"""
@brief 结构化地图资源数据类
@details 地图资源数据的结构化版本别名，与原始 MapResource 相同
"""


if __name__ == '__main__':
    pass
