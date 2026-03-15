# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 数据汇总模块
@details 提供原始数据和结构化数据的汇总容器类

此模块定义了 SourceSummary 和 StructureSummary 数据类，用于存储
source 和 structure 模块的整体数据，便于在模块间传递和统一管理。
"""

from dataclasses import dataclass, field

from core.datatype.prefix import CountryTagPrefix, RegionStatePrefix, RegionNamePrefix, StateNamePurePrefix

from core.datatype.source.state import StateFile
from core.datatype.source.building import BuildingFile
from core.datatype.source.population import PopulationFile
from core.datatype.source.region import RegionFile
from core.datatype.source.definition import DefinitionFile
from core.datatype.source.effect import EffectFile
from core.datatype.source.map import MapFile

from core.datatype.structure.state import StateCountryItem
from core.datatype.structure.building import StructuredBuildingState
from core.datatype.structure.population import StructuredRegionPopulation
from core.datatype.structure.region import StructuredRegionItem
from core.datatype.structure.definition import StructuredDefinitionCountry
from core.datatype.structure.effect import StructuredEffectCountry
from core.datatype.structure.map import StructuredMapRegion


@dataclass
class SourceSummary:
    """
    @brief 原始数据汇总类
    @details 存储所有原始数据的容器，包含每种数据类型的文件字典

    此数据类用于汇总 source 模块的所有输出，便于在模块间传递和统一管理。
    每个字段对应一种游戏实体的文件数据字典，键为文件名，值为对应的File对象实例。
    数据来源直接兼容 analysis 模块的输出格式。
    """
    # 州数据文件：文件名 -> StateFile对象
    state_files: dict[str, StateFile] = field(default_factory=dict)

    # 建筑数据文件：文件名 -> BuildingFile对象
    building_files: dict[str, BuildingFile] = field(default_factory=dict)

    # 人口数据文件：文件名 -> PopulationFile对象
    population_files: dict[str, PopulationFile] = field(default_factory=dict)

    # 区域数据文件：文件名 -> RegionFile对象
    region_files: dict[str, RegionFile] = field(default_factory=dict)

    # 国家定义数据文件：文件名 -> DefinitionFile对象
    definition_files: dict[str, DefinitionFile] = field(default_factory=dict)

    # 国家效果数据文件：文件名 -> EffectFile对象
    effect_files: dict[str, EffectFile] = field(default_factory=dict)

    # 地图数据文件：文件名 -> MapFile对象
    map_files: dict[str, MapFile] = field(default_factory=dict)


@dataclass
class StructureSummary:
    """
    @brief 结构化数据汇总类
    @details 存储所有结构化数据的容器，包含每种数据类型的结构化字典

    此数据类用于汇总 structure 模块的所有输出，便于在模块间传递和统一管理。
    每个字段对应一种游戏实体的结构化数据字典，键为相应前缀，值为结构化数据类实例。
    """
    # 州数据：国家 -> 州信息
    state_data: dict[CountryTagPrefix, StateCountryItem] = field(default_factory=dict)

    # 建筑数据：区域州 -> 州建筑信息
    building_data: dict[RegionStatePrefix, StructuredBuildingState] = field(default_factory=dict)

    # 人口数据：区域州 -> 州人口信息
    population_data: dict[RegionStatePrefix, StructuredRegionPopulation] = field(default_factory=dict)

    # 区域数据：区域名称 -> 区域信息
    region_data: dict[RegionNamePrefix, StructuredRegionItem] = field(default_factory=dict)

    # 国家定义数据：国家标签 -> 国家定义信息
    definition_data: dict[CountryTagPrefix, StructuredDefinitionCountry] = field(default_factory=dict)

    # 国家效果数据：国家标签 -> 国家效果信息
    effect_data: dict[CountryTagPrefix, StructuredEffectCountry] = field(default_factory=dict)

    # 地图区域数据：州名称（纯前缀） -> 地图区域信息
    map_region_data: dict[StateNamePurePrefix, StructuredMapRegion] = field(default_factory=dict)


if __name__ == '__main__':
    pass