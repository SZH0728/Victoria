# -*- coding:utf-8 -*-
# AUTHOR: Sun

from dataclasses import dataclass

from core.datatype.prefix import RegionNamePrefix, StateNamePurePrefix


@dataclass(frozen=True)
class RegionItem(object):
    """
    @brief 区域项目数据类
    @details 表示游戏中的一个区域，包含图形文化、首府省份、地图颜色和包含的州
    """
    graphical_culture: str | None            # 图形文化
    capital_province: str | None             # 首府省份
    map_color: tuple[int | float, ...]       # 地图颜色
    states: tuple[StateNamePurePrefix, ...]  # 包含的州列表

    def __post_init__(self):
        """
        @brief 后初始化方法，确保列表类型属性转换为元组
        """
        if isinstance(self.map_color, list):
            object.__setattr__(self, 'map_color', tuple(self.map_color))
        if isinstance(self.states, list):
            object.__setattr__(self, 'states', tuple(self.states))


@dataclass(frozen=True)
class RegionFile(object):
    """
    @brief 区域文件数据类
    @details 表示整个区域文件的数据结构，包含根键和区域项目字典
    """
    root_key: str | None                                   # 根键
    region_item_dict: dict[RegionNamePrefix, RegionItem]   # 区域项目字典


if __name__ == '__main__':
    pass