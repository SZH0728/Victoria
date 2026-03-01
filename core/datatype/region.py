# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Iterator, Generator, Any
from dataclasses import dataclass, field


@dataclass
class RegionItem(object):
    """!
    @brief 区域项数据类，表示单个战略区域的信息
    @details 包含区域的名称、图形文化、首府省份、地图颜色和所属州列表
    """
    region_name: str                    #!< 区域名称
    graphical_culture: str              #!< 图形文化标识
    capital_province: str               #!< 首府省份ID
    map_color: tuple[int, ...]          #!< 地图颜色RGB元组
    states: tuple[str, ...]             #!< 所属州ID列表


@dataclass
class Region(object):
    """!
    @brief 区域容器类，按大洲分类存储区域项
    @details 提供类似字典的接口访问各洲区域列表，支持迭代、键值对访问等操作
    """
    europe: list[RegionItem] = field(default_factory=list)           #!< 欧洲区域列表
    east_asia: list[RegionItem] = field(default_factory=list)        #!< 东亚区域列表
    west_south_asia: list[RegionItem] = field(default_factory=list)  #!< 西亚南亚区域列表
    north_america: list[RegionItem] = field(default_factory=list)    #!< 北美洲区域列表
    south_america: list[RegionItem] = field(default_factory=list)    #!< 南美洲区域列表
    african: list[RegionItem] = field(default_factory=list)          #!< 非洲区域列表
    water: list[RegionItem] = field(default_factory=list)            #!< 水域区域列表

    #! 地区键列表，定义所有有效的大洲分类键
    _region_keys = ('europe', 'east_asia', 'west_south_asia', 'north_america',
                    'south_america', 'african', 'water')

    def __iter__(self) -> Iterator[str]:
        """!
        @brief 迭代地区键
        @return 地区键迭代器
        """
        return iter(self._region_keys)

    def __getitem__(self, key: str) -> list[RegionItem]:
        """!
        @brief 通过字典键访问地区列表
        @param key 地区键名
        @return 对应的区域项列表
        @throws KeyError 当键名不存在时抛出异常
        """
        if key not in self._region_keys:
            raise KeyError(f"Region key '{key}' not found")
        return getattr(self, key)

    def __setitem__(self, key: str, value: list[RegionItem]):
        """!
        @brief 通过字典键设置地区列表
        @param key 地区键名
        @param value 区域项列表
        @throws KeyError 当键名不存在时抛出异常
        """
        if key not in self._region_keys:
            raise KeyError(f"Region key '{key}' not found")
        setattr(self, key, value)

    def __contains__(self, key: str) -> bool:
        """!
        @brief 检查键是否存在
        @param key 地区键名
        @return 键是否存在
        """
        return key in self._region_keys

    def keys(self) -> tuple[str, ...]:
        """!
        @brief 返回所有地区键
        @return 地区键元组
        """
        return self._region_keys

    def values(self) -> Generator[list[RegionItem], None, None]:
        """!
        @brief 返回所有地区列表
        @return 地区列表生成器
        """
        return (getattr(self, key) for key in self._region_keys)

    def items(self) -> Generator[tuple[str, list[RegionItem]], None, None]:
        """!
        @brief 返回所有键值对
        @return 键值对生成器，每个元素为(地区键, 区域项列表)
        """
        return ((key, getattr(self, key)) for key in self._region_keys)

    def get(self, key: str, default: Any = None) -> Any:
        """!
        @brief 获取地区列表，如果键不存在则返回默认值
        @param key 地区键名
        @param default 默认值
        @return 区域项列表或默认值
        """
        if key in self._region_keys:
            return getattr(self, key)
        return default


if __name__ == '__main__':
    pass