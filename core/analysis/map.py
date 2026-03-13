# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from pyradox import Tree

from core.datatype.prefix import StateNamePurePrefix
from core.datatype.source.map import MapFile, MapRegion, MapResource
from core.analysis.base import AnalysisBase

logger = getLogger(__name__)


class AnalysisMapDefault(AnalysisBase):
    """
    @brief 地图数据分析类
    @details 分析维多利亚3游戏中的地图数据文件，提取州区域、资源和地理特征信息
    """
    def __init__(self):
        """
        @brief 初始化地图数据分析类
        @details 调用父类初始化方法，添加默认忽略文件，设置结果字典类型
        """
        super().__init__()
        self.add_ignore_file('99_seas.txt')
        self.result: dict[str, MapFile] = {}
        logger.debug(f"AnalysisMapDefault initialized with empty result dict")

    def analysis_map_undiscovered_resource(self, tree: Tree) -> MapResource:
        """
        @brief 分析未发现资源数据
        @details 从Tree对象中提取未发现资源信息，包括资源类型、枯竭类型和数量
        @param tree 包含资源数据的Tree对象
        @return 解析后的MapResource对象
        """
        result: dict[str, Any] = {}
        logger.debug(f"Starting analysis of map undiscovered resource")

        for key, value in tree.items():
            value = self.get_stringify_value_from_tree(value)

            if key == 'type':
                result['type'] = value
                logger.debug(f"Found resource type: {value}")
            elif key == 'depleted_type':
                result['depleted_type'] = value
                logger.debug(f"Found depleted type: {value}")
            elif key == 'undiscovered_amount':
                result['undiscovered_amount'] = value
                logger.debug(f"Found undiscovered amount: {value}")
            elif key == 'discovered_amount':
                result['discovered_amount'] = value
                logger.debug(f"Found discovered amount: {value}")
            else:
                logger.warning(f"Unknown key '{key}' when analyzing map resource")

        self.verify_key_in_dictionary(result, 'depleted_type')
        self.verify_key_in_dictionary(result, 'undiscovered_amount')
        self.verify_key_in_dictionary(result, 'discovered_amount')
        logger.debug(f"Map resource analysis completed")
        return MapResource(**result)

    @staticmethod
    def analysis_map_resources(tree: Tree) -> dict[str, int]:
        """
        @brief 分析地图资源数据
        @details 从Tree对象中提取资源名称和数量的映射关系，转换为整数类型
        @param tree 包含资源数据的Tree对象
        @return 资源名称到整数值的字典
        """
        result: dict[str, int] = {}
        logger.debug(f"Starting analysis of map resources")

        for key, value in tree.items():
            result[key] = int(value)
            logger.debug(f"Added resource: {key} = {value}")

        logger.debug(f"Map resources analysis completed, found {len(result)} resources")
        return result

    def analysis_map_region(self, tree: Tree) -> MapRegion:
        """
        @brief 分析地图区域数据
        @details 从Tree对象中提取州区域详细信息，包括资源、省份、特征和地理属性
        @param tree 包含区域数据的Tree对象
        @return 解析后的MapRegion对象
        """
        result: dict[str, Any] = {}
        logger.debug(f"Starting analysis of map region")

        for key, value in tree.items():
            if key == 'capped_resources':
                logger.debug(f"Found capped_resources key, analyzing resources")
                result['capped_resources'] = self.analysis_map_resources(value)
                continue

            if key == 'resource':
                logger.debug(f"Found resource key, analyzing undiscovered resource")
                self.add_value_to_list_in_dict(result, 'resource', self.analysis_map_undiscovered_resource(value))
                continue

            value = self.get_stringify_value_from_tree(value)

            if key == 'id':
                result['id'] = value
                logger.debug(f"Found region id: {value}")

            elif key == 'subsistence_building':
                result['subsistence_building'] = value
                logger.debug(f"Found subsistence_building: {value}")
            elif key == 'provinces':
                self.add_value_to_list_in_dict(result, 'provinces', value)
                logger.debug(f"Added province: {value}")
            elif key == 'traits':
                self.add_value_to_list_in_dict(result, 'traits', value)
                logger.debug(f"Added trait: {value}")

            elif key == 'city':
                result['city'] = value
                logger.debug(f"Found city: {value}")
            elif key == 'port':
                result['port'] = value
                logger.debug(f"Found port: {value}")
            elif key == 'farm':
                result['farm'] = value
                logger.debug(f"Found farm: {value}")
            elif key == 'mine':
                result['mine'] = value
                logger.debug(f"Found mine: {value}")
            elif key == 'wood':
                result['wood'] = value
                logger.debug(f"Found wood: {value}")

            elif key == 'arable_land':
                result['arable_land'] = value
                logger.debug(f"Found arable_land: {value}")
            elif key == 'arable_resources':
                self.add_value_to_list_in_dict(result, 'arable_resources', value)
                logger.debug(f"Added arable_resource: {value}")

            elif key == 'naval_exit_id':
                result['naval_exit_id'] = value
                logger.debug(f"Found naval_exit_id: {value}")

        self.verify_key_in_dictionary(result, 'traits', [])
        self.verify_key_in_dictionary(result, 'port')
        self.verify_key_in_dictionary(result, 'capped_resources', {})
        self.verify_key_in_dictionary(result, 'resource', [])
        self.verify_key_in_dictionary(result, 'naval_exit_id')
        logger.debug(f"Map region analysis completed")
        return MapRegion(**result)

    def analysis(self, filename: str, tree: Tree):
        """
        @brief 分析地图数据文件
        @details 从Tree对象中提取所有州区域数据，构建MapFile对象
        @param filename 正在分析的文件名
        @param tree 解析后的Tree对象
        """
        logger.debug(f"Starting map analysis for file '{filename}'")

        map_region_dict: dict[StateNamePurePrefix, MapRegion] = {}
        for state_name, state_context in tree.items():
            logger.debug(f"Analyzing map region: {state_name}")
            state_name = StateNamePurePrefix(str_with_prefix=state_name)
            map_region_dict[state_name] = self.analysis_map_region(state_context)

        self.result[filename] = MapFile(root_key=None, map_region_dict=map_region_dict)
        logger.info(f"Map analysis completed for file '{filename}'")

if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('map', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\map_data\state_regions'))
    manager.collect_file('map', '.txt')

    analysis = AnalysisMapDefault()
    analysis.main(manager, 'map')
    print(analysis.result)
