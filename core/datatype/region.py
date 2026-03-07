# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 区域数据定义模块
@details 定义了维多利亚3游戏中战略区域相关的数据结构，包括区域信息、首府、颜色等
"""

from dataclasses import dataclass

from core.datatype.prefix import RegionNamePrefix, StateNamePurePrefix


@dataclass(frozen=True)
class RegionItem(object):
    """
    @brief 区域项数据类
    @details 表示一个战略区域的所有相关信息，包括图形文化、首府、颜色和所属州
    """
    graphical_culture: str | None                #!< 图形文化标识
    capital_province: str | None                 #!< 首府省份ID
    map_color: tuple[int | float, ...]           #!< 地图颜色RGB元组
    states: tuple[StateNamePurePrefix, ...]      #!< 所属州ID列表

    def __post_init__(self):
        """@brief 初始化后处理，确保所有字段都是元组类型"""
        if isinstance(self.map_color, list):
            object.__setattr__(self, 'map_color', tuple(self.map_color))
        if isinstance(self.states, list):
            object.__setattr__(self, 'states', tuple(self.states))


@dataclass(frozen=True)
class RegionFile(object):
    """
    @brief 区域文件数据容器
    @details 包含区域数据的根键和区域项字典
    """
    root_key: str | None
    region_item_dict: dict[RegionNamePrefix, RegionItem]


if __name__ == '__main__':
    pass