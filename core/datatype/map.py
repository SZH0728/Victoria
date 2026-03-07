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
    """@brief 区域唯一标识符"""

    subsistence_building: str
    """@brief 生存建筑类型"""

    provinces: tuple[str, ...]
    """@brief 所属省份ID列表"""

    traits: tuple[str, ...]
    """@brief 区域特性列表"""

    city: str
    """@brief 城市建筑"""

    port: str | None
    """@brief 港口建筑（可选）"""

    farm: str
    """@brief 农场建筑"""

    mine: str
    """@brief 矿山建筑"""

    wood: str
    """@brief 木材建筑"""

    arable_land: int
    """@brief 可耕种土地数量"""

    arable_resources: tuple[str, ...]
    """@brief 可耕种资源类型列表"""

    capped_resources: dict[str, int]
    """@brief 资源上限字典"""

    naval_exit_id: int | None
    """@brief 海军出口ID（可选）"""


@dataclass(frozen=True)
class MapFile(object):
    """
    @brief 地图文件数据容器
    @details 包含地图数据的根键和区域字典
    """

    root_key: str | None
    """@brief 文件根键（可选）"""

    map_region_dict: dict[StateNamePurePrefix, MapRegion]
    """@brief 区域名称到区域数据的映射字典"""


if __name__ == '__main__':
    pass
