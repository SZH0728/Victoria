# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@file base.py
@brief 区域分析基础模块，定义区域数据结构和分析基类
@details 提供区域数据类、区域容器类以及区域分析的抽象基类
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Generator, Tuple, Optional, Any

from pyradox import Tree, parse

from core.file import FileManager


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

    def items(self) -> Generator[Tuple[str, list[RegionItem]], None, None]:
        """!
        @brief 返回所有键值对
        @return 键值对生成器，每个元素为(地区键, 区域项列表)
        """
        return ((key, getattr(self, key)) for key in self._region_keys)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """!
        @brief 获取地区列表，如果键不存在则返回默认值
        @param key 地区键名
        @param default 默认值
        @return 区域项列表或默认值
        """
        if key in self._region_keys:
            return getattr(self, key)
        return default


class RegionAnalysisBase(ABC):
    """!
    @brief 区域分析抽象基类
    @details 提供区域分析的通用框架，子类需实现具体的分析逻辑
    """
    def __init__(self):
        """!
        @brief 初始化区域分析器
        """
        self.region = Region()  #!< 区域数据容器

    @staticmethod
    def get_continent_name_by_file_name(name: str | Path) -> str:
        """!
        @brief 根据文件名提取大洲名称
        @details 去除文件名中的'.txt'后缀和'_strategic_regions'后缀
        @param name 文件名或Path对象
        @return 大洲名称
        """
        if isinstance(name, Path):
            name = name.name

        name = name.replace('.txt', '')

        return name.replace('_strategic_regions', '')

    @staticmethod
    def get_region_name_by_key(name: str) -> str:
        """!
        @brief 根据区域键名提取区域名称
        @details 去除区域键名中的'region_'前缀
        @param name 区域键名
        @return 区域名称
        """
        return name.replace('region_', '')

    @abstractmethod
    def analysis(self, tree: Tree) -> list[RegionItem]:
        """!
        @brief 分析战略区域树，提取区域项
        @details 子类必须实现此方法，解析pyradox树结构并返回区域项列表
        @param tree pyradox解析的树结构
        @return 区域项列表
        """
        pass

    def main(self, manager: FileManager, group: str):
        """!
        @brief 主分析流程，读取文件组并进行分析
        @details 遍历文件组中的所有文件，解析内容并调用analysis方法提取区域项，
                 将结果按大洲分类存储到region容器中
        @param manager 文件管理器实例
        @param group 文件组名称
        """
        for file_path, content in manager.read_files_in_range(group):
            tree = parse(content)
            region_items = self.analysis(tree)

            if region_items:
                region_name = self.get_continent_name_by_file_name(file_path)
                self.region[region_name].extend(region_items)


if __name__ == '__main__':
    pass
