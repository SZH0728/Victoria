# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 地图区域数据定义模块
@details 定义了维多利亚3游戏中地图区域相关的数据结构，包括区域基本信息、资源、建筑等
"""

from dataclasses import dataclass

from core.datatype.prefix import StateNamePurePrefix


@dataclass(frozen=True)
class MapRegion(object):
    """
    @brief 地图区域数据类
    @details 表示游戏地图上的一个区域，包含区域ID、建筑、资源、人口等相关信息
    """
    id: int
    subsistence_building: str
    provinces: tuple[str, ...]
    traits: tuple[str, ...]

    city: str
    port: str | None
    farm: str
    mine: str
    wood: str

    arable_land: int
    arable_resources: tuple[str, ...]
    capped_resources: dict[str, int]

    naval_exit_id: int | None


@dataclass(frozen=True)
class MapFile(object):
    """
    @brief 地图文件数据容器
    @details 包含地图数据的根键和区域字典
    """
    root_key: str | None
    map_region_dict: dict[StateNamePurePrefix, MapRegion]


if __name__ == '__main__':
    pass
