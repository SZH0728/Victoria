# -*- coding:utf-8 -*-
# AUTHOR: Sun

from dataclasses import dataclass

from core.datatype.prefix import RegionStatePrefix, StateNamePrefix


@dataclass(frozen=True)
class PopulationItem(object):
    """
    @brief 人口项目数据类
    @details 表示游戏中的一个人口群体，包含规模、文化、宗教和人口类型
    """
    size: int              # 人口规模
    culture: str | None    # 文化
    religion: str | None   # 宗教
    pop_type: str | None   # 人口类型

    def __post_init__(self):
        """
        @brief 后初始化方法，验证人口规模非负
        """
        if self.size < 0:
            raise ValueError(f"{self.__class__.__name__}: Population size must be non-negative integer, got: {self.size}")


@dataclass(frozen=True)
class PopulationCountry(object):
    """
    @brief 人口国家数据类
    @details 表示一个国家在特定区域内的人口信息
    """
    create_pop: tuple[PopulationItem, ...]  # 人口创建列表

    def __post_init__(self):
        """
        @brief 后初始化方法，确保列表类型属性转换为元组
        """
        if isinstance(self.create_pop, list):
            object.__setattr__(self, 'create_pop', tuple(self.create_pop))


@dataclass(frozen=True)
class PopulationRegion(object):
    """
    @brief 人口区域数据类
    @details 表示一个区域的人口信息，包含区域到国家人口的映射
    """
    population_country_dict: dict[RegionStatePrefix, PopulationCountry]  # 区域国家人口字典


@dataclass(frozen=True)
class PopulationFile(object):
    """
    @brief 人口文件数据类
    @details 表示整个人口文件的数据结构，包含根键和州到区域人口的映射
    """
    root_key: str | None                                             # 根键
    population_region_dict: dict[StateNamePrefix, PopulationRegion]  # 州区域人口字典


if __name__ == '__main__':
    pass