# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 人口数据定义模块
@details 定义了维多利亚3游戏中人口相关的数据结构，包括人口项、国家人口、区域人口等
"""

from dataclasses import dataclass

from core.datatype.prefix import RegionStatePrefix, StateNamePrefix


@dataclass(frozen=True)
class PopulationItem(object):
    """
    @brief 人口项数据类
    @details 表示一个人口群体的基本信息，包括数量、文化、宗教和人口类型
    """
    size: int                       #!< 人口数量
    culture: str | None             #!< 文化
    religion: str | None            #!< 宗教
    pop_type: str | None            #!< 人口类型


@dataclass(frozen=True)
class PopulationCountry(object):
    """
    @brief 国家人口数据类
    @details 表示一个国家的人口列表
    """
    create_pop: tuple[PopulationItem, ...]  #!< 人口项列表

    def __post_init__(self):
        """@brief 初始化后处理，确保create_pop为元组类型"""
        if isinstance(self.create_pop, list):
            object.__setattr__(self, 'create_pop', tuple(self.create_pop))


@dataclass(frozen=True)
class PopulationRegion(object):
    """
    @brief 区域人口数据类
    @details 表示一个区域的人口数据，包含区域状态到国家人口的映射
    """
    population_country_dict: dict[RegionStatePrefix, PopulationCountry]  #!< 国家人口字典


@dataclass(frozen=True)
class PopulationFile(object):
    """
    @brief 人口文件数据容器
    @details 包含人口数据的根键和区域人口字典
    """
    root_key: str | None
    population_region_dict: dict[StateNamePrefix, PopulationRegion]


if __name__ == '__main__':
    pass