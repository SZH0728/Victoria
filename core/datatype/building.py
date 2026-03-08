# -*- coding:utf-8 -*-
# AUTHOR: Sun

from dataclasses import dataclass

from core.datatype.prefix import CountryTagPrefix, StateNamePurePrefix, RegionStatePrefix, StateNamePrefix


@dataclass(frozen=True)
class BuildingCountryOwnership(object):
    """
    @brief 建筑国家所有权数据类
    @details 表示建筑的国家所有权信息，包含国家和等级
    """
    country: CountryTagPrefix   # 国家标签
    levels: int                 # 建筑等级

    def __post_init__(self):
        """
        @brief 后初始化方法，验证建筑等级为正整数
        """
        if self.levels <= 0:
            raise ValueError(f"{self.__class__.__name__}: Building level must be a positive integer, got: {self.levels}")


@dataclass(frozen=True)
class BuildingPrivateOwnership(object):
    """
    @brief 建筑私人所有权数据类
    @details 表示建筑的私人所有权信息，包含类型、国家、等级和区域
    """
    type: str                   # 所有权类型
    country: CountryTagPrefix   # 国家标签
    levels: int                 # 建筑等级
    region: StateNamePurePrefix # 区域

    def __post_init__(self):
        """
        @brief 后初始化方法，验证建筑等级为正整数
        """
        if self.levels <= 0:
            raise ValueError(f"{self.__class__.__name__}: Building level must be a positive integer, got: {self.levels}")


@dataclass(frozen=True)
class BuildingCompanyOwnership(object):
    """
    @brief 建筑公司所有权数据类
    @details 表示建筑的公司所有权信息，包含类型、国家和等级
    """
    type: str                   # 所有权类型
    country: CountryTagPrefix   # 国家标签
    levels: int                 # 建筑等级

    def __post_init__(self):
        """
        @brief 后初始化方法，验证建筑等级为正整数
        """
        if self.levels <= 0:
            raise ValueError(f"{self.__class__.__name__}: Building level must be a positive integer, got: {self.levels}")


# 建筑所有权类型别名
BuildingOwnership = BuildingCountryOwnership | BuildingPrivateOwnership | BuildingCompanyOwnership

@dataclass(frozen=True)
class BuildingItem(object):
    """
    @brief 建筑项目数据类
    @details 表示游戏中的一个建筑，包含建筑类型、所有权、补贴、储备和生产方法
    """
    building: str  # 建筑类型
    add_ownership: tuple[BuildingOwnership, ...]  # 所有权列表
    subsidized: bool | None                       # 是否补贴
    reserves: int | None                          # 储备数量
    activate_production_methods: tuple[str, ...]  # 激活的生产方法列表

    def __post_init__(self):
        """
        @brief 后初始化方法，确保列表类型属性转换为元组
        """
        if isinstance(self.add_ownership, list):
            object.__setattr__(self, 'add_ownership', tuple(self.add_ownership))
        if isinstance(self.activate_production_methods, list):
            object.__setattr__(self, 'activate_production_methods', tuple(self.activate_production_methods))


@dataclass(frozen=True)
class BuildingNoOwnerItem(object):
    """
    @brief 无所有者建筑项目数据类
    @details 表示没有所有者的建筑信息，包含建筑类型和等级
    """
    building: str  # 建筑类型
    level: int     # 建筑等级


@dataclass(frozen=True)
class BuildingCountry(object):
    """
    @brief 建筑国家数据类
    @details 表示一个国家在特定区域内的建筑信息
    """
    create_building: tuple[BuildingItem|BuildingNoOwnerItem, ...]  # 建筑创建列表

    def __post_init__(self):
        """
        @brief 后初始化方法，确保列表类型属性转换为元组
        """
        if isinstance(self.create_building, list):
            object.__setattr__(self, 'create_building', tuple(self.create_building))


@dataclass(frozen=True)
class BuildingState(object):
    """
    @brief 建筑州数据类
    @details 表示一个州内的建筑信息，包含区域到国家建筑的映射
    """
    building_country_dict: dict[RegionStatePrefix, BuildingCountry]  # 区域国家建筑字典


@dataclass(frozen=True)
class BuildingFile(object):
    """
    @brief 建筑文件数据类
    @details 表示整个建筑文件的数据结构，包含州到州建筑信息的映射
    """
    building_state_dict: dict[StateNamePrefix, BuildingState]  # 州建筑字典


if __name__ == '__main__':
    pass