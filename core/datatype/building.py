# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 建筑数据定义模块
@details 定义了维多利亚3游戏中建筑相关的数据结构，包括国家、私有、公司所有权等
"""

from dataclasses import dataclass

from core.datatype.prefix import CountryTagPrefix, StateNamePurePrefix, RegionStatePrefix, StateNamePrefix


@dataclass(frozen=True)
class BuildingCountryOwnership(object):
    """
    @brief 国家建筑所有权数据类
    @details 表示国家拥有的建筑物，包含国家标签和建筑等级
    """

    country: CountryTagPrefix         #!< 国家标签
    levels: int                       #!< 建筑等级


@dataclass(frozen=True)
class BuildingPrivateOwnership(object):
    """
    @brief 私有建筑所有权数据类
    @details 表示私有拥有的建筑物，包含建筑类型、国家标签、等级和所属区域
    """

    type: str                         #!< 建筑类型
    country: CountryTagPrefix         #!< 国家标签
    levels: int                       #!< 建筑等级
    region: StateNamePurePrefix       #!< 所属区域


@dataclass(frozen=True)
class BuildingCompanyOwnership(object):
    """
    @brief 公司建筑所有权数据类
    @details 表示公司拥有的建筑物，包含公司名称、国家标签和建筑等级
    """

    type: str                         #!< 公司名称
    country: CountryTagPrefix         #!< 国家标签
    levels: int                       #!< 建筑等级


@dataclass(frozen=True)
class BuildingItem(object):
    """
    @brief 建筑项数据类
    @details 表示一个建筑物的详细信息，包括所有权、补贴状态、储备和生产方法
    """

    building: str                                 #!< 建筑类型
    add_ownership: dict[str, BuildingCountryOwnership|BuildingPrivateOwnership|BuildingCompanyOwnership]  #!< 所有权列表
    subsidized: bool | None                       #!< 补贴状态（如"yes"，可选）
    reserves: int | None                          #!< 建筑储备（可选）
    activate_production_methods: tuple[str, ...]  #!< 生产方法列表

    def __post_init__(self):
        """@brief 初始化后处理，确保activate_production_methods为元组类型"""
        if isinstance(self.activate_production_methods, list):
            object.__setattr__(self, 'activate_production_methods', tuple(self.activate_production_methods))


@dataclass(frozen=True)
class BuildingNoOwnerItem(object):
    """
    @brief 无所有者建筑项数据类
    @details 表示没有所有者的建筑物，包含建筑类型和等级
    """

    building: str                    #!< 建筑类型
    level: int                       #!< 建筑等级


@dataclass(frozen=True)
class BuildingCountry(object):
    """
    @brief 国家建筑数据类
    @details 表示一个国家拥有的建筑物列表
    """

    create_building: tuple[BuildingItem|BuildingNoOwnerItem, ...]  #!< 建筑项列表

    def __post_init__(self):
        """@brief 初始化后处理，确保create_building为元组类型"""
        if isinstance(self.create_building, list):
            object.__setattr__(self, 'create_building', tuple(self.create_building))


@dataclass(frozen=True)
class BuildingState(object):
    """
    @brief 州建筑数据类
    @details 表示一个州的建筑数据，包含区域到国家建筑的映射
    """

    building_country_dict: dict[RegionStatePrefix, BuildingCountry]  #!< 区域状态到国家建筑的映射字典


@dataclass(frozen=True)
class BuildingFile(object):
    """
    @brief 建筑文件数据容器
    @details 包含建筑数据的州到州建筑映射
    """

    building_state_dict: dict[StateNamePrefix, BuildingState]  #!< 州名称到州建筑数据的映射字典


if __name__ == '__main__':
    pass