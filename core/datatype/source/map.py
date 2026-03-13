# -*- coding:utf-8 -*-
# AUTHOR: Sun

from dataclasses import dataclass

from core.datatype.prefix import StateNamePurePrefix


@dataclass(frozen=True)
class MapResource(object):
    """
    @brief 地图资源数据类
    @details 表示游戏地图中的资源信息，包括资源类型、枯竭类型、未发现数量和已发现数量
    """
    type: str                         # 资源类型
    depleted_type: str | None         # 资源枯竭后的类型
    undiscovered_amount: int | None   # 未发现的资源数量
    discovered_amount: int | None     # 已发现的资源数量


@dataclass(frozen=True)
class MapRegion(object):
    """
    @brief 地图区域数据类
    @details 表示游戏地图中的区域信息，包含省份、特性、建筑、资源和海军出口等
    """
    id: int                            # 区域ID
    subsistence_building: str          # 生存建筑类型
    provinces: tuple[str, ...]         # 包含的省份列表
    traits: tuple[str, ...]            # 区域特性列表

    city: str                          # 城市建筑
    port: str | None                   # 港口建筑
    farm: str                          # 农场建筑
    mine: str                          # 矿山建筑
    wood: str                          # 伐木场建筑

    arable_land: int                   # 可耕地数量
    arable_resources: tuple[str, ...]  # 可耕地资源列表
    capped_resources: dict[str, int]   # 限制资源字典
    resource: tuple[MapResource, ...]  # 资源列表
    naval_exit_id: int | None          # 海军出口ID

    def __post_init__(self):
        """
        @brief 后初始化方法，确保列表类型属性转换为元组，并验证数据有效性
        """
        if isinstance(self.provinces, list):
            object.__setattr__(self, 'provinces', tuple(self.provinces))
        if isinstance(self.traits, list):
            object.__setattr__(self, 'traits', tuple(self.traits))
        if isinstance(self.arable_resources, list):
            object.__setattr__(self, 'arable_resources', tuple(self.arable_resources))
        if isinstance(self.resource, list):
            object.__setattr__(self, 'resource', tuple(self.resource))

        # 验证可耕地数量非负
        if self.arable_land < 0:
            raise ValueError(f"{self.__class__.__name__}: Arable land amount must be non-negative integer, got: {self.arable_land}")


@dataclass(frozen=True)
class MapFile(object):
    """
    @brief 地图文件数据类
    @details 表示整个地图文件的数据结构，包含根键和区域字典
    """
    root_key: str | None                                   # 根键
    map_region_dict: dict[StateNamePurePrefix, MapRegion]  # 区域字典


if __name__ == '__main__':
    pass