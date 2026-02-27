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


@dataclass
class CountryState(object):
    state_name: str
    country_tag: str
    provinces: tuple[str, ...]
    state_type: str | None


@dataclass
class State(object):
    state_name: str
    country: list[CountryState]
    homeland: tuple[str, ...]
    claim: tuple[str, ...]


@dataclass
class StateMap(object):
    """!
    @brief 状态映射容器类，存储状态名称到状态对象的映射
    @details 提供类似字典的接口访问状态对象，支持通过.和[]操作符读写，
             同时提供keys()、values()、items()、get()等字典常用方法
    """
    _data: dict[str, State] = field(default_factory=dict, init=False, repr=False)

    def __getitem__(self, key: str) -> State:
        """!
        @brief 通过字典键访问状态对象
        @param key 状态名称
        @return 对应的状态对象
        @throws KeyError 当键名不存在时抛出异常
        """
        return self._data[key]

    def __setitem__(self, key: str, value: State):
        """!
        @brief 通过字典键设置状态对象
        @param key 状态名称
        @param value 状态对象
        """
        self._data[key] = value

    def __contains__(self, key: str) -> bool:
        """!
        @brief 检查键是否存在
        @param key 状态名称
        @return 键是否存在
        """
        return key in self._data

    def __getattr__(self, name: str) -> Any:
        """!
        @brief 通过属性名访问状态对象
        @details 当属性不存在于实例或类中时，尝试从_data字典中获取
        @param name 属性名
        @return 对应的状态对象
        @throws AttributeError 当属性名不存在时抛出异常
        """
        # 避免递归调用，检查是否在__dict__中
        if name in self.__dict__ or hasattr(type(self), name):
            # 这应该不会发生，因为__getattr__只在属性未找到时调用
            # 但为了安全起见，调用super().__getattribute__
            return super().__getattribute__(name)
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(f"'StateMap' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any):
        """!
        @brief 通过属性名设置状态对象
        @details 如果属性名不是_data且不是类属性，则存储到_data字典中
        @param name 属性名
        @param value 属性值
        """
        # 如果name是_data，或者name是类属性（方法等），则使用默认的__setattr__
        if name == '_data' or hasattr(type(self), name):
            super().__setattr__(name, value)
        else:
            # 否则存储到_data字典中
            self._data[name] = value

    def __delattr__(self, name: str):
        """!
        @brief 删除属性
        @details 如果属性名在_data中，则从_data中删除；否则如果是类属性则禁止删除，否则调用父类方法
        @param name 属性名
        """
        if name == '_data':
            super().__delattr__(name)
        elif name in self._data:
            del self._data[name]
        elif hasattr(type(self), name):
            raise AttributeError(f"Cannot delete class attribute '{name}'")
        else:
            super().__delattr__(name)

    def __delitem__(self, key: str):
        """!
        @brief 删除键值对
        @param key 状态名称
        """
        del self._data[key]

    def __iter__(self) -> Iterator[str]:
        """!
        @brief 迭代状态名称键
        @return 状态名称键迭代器
        """
        return iter(self._data)

    def __repr__(self) -> str:
        """!
        @brief 返回对象的可读字符串表示
        @return 状态映射的字符串表示
        """
        items = []
        for key, value in self._data.items():
            items.append(f"{key}: {value.state_name}")
        return f"StateMap({{{', '.join(items)}}})"

    def keys(self) -> tuple[str, ...]:
        """!
        @brief 返回所有状态名称键
        @return 状态名称键元组
        """
        return tuple(self._data.keys())

    def values(self) -> Generator[State, None, None]:
        """!
        @brief 返回所有状态对象
        @return 状态对象生成器
        """
        return (value for value in self._data.values())

    def items(self) -> Generator[tuple[str, State], None, None]:
        """!
        @brief 返回所有键值对
        @return 键值对生成器，每个元素为(状态名称, 状态对象)
        """
        return ((key, value) for key, value in self._data.items())

    def get(self, key: str, default: Any = None) -> Any:
        """!
        @brief 获取状态对象，如果键不存在则返回默认值
        @param key 状态名称
        @param default 默认值
        @return 状态对象或默认值
        """
        return self._data.get(key, default)


if __name__ == '__main__':
    pass
