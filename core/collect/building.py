# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 建筑收集模块
@details 提供建筑数据的收集功能，统计每个州的建筑类型和等级

此模块实现了 CollectBuildingDefault 类，用于从 StructureSummary 中
提取建筑数据，按州和建筑类型进行合并统计，相同建筑类型的等级相加。
"""

from collections import defaultdict
from logging import getLogger
from typing import Any

from core.collect.base import CollectBase
from core.datatype.summarize import SourceSummary, StructureSummary
from core.datatype.prefix import StateNamePrefix
from core.datatype.collect.building import CollectBuildingStateItem, CollectBuildingStateResult
from core.datatype.structure.building import StructuredBuildingState, StructuredBuildingItem, StructuredBuildingNoOwnerItem

logger = getLogger(__name__)


class CollectBuildingDefault(CollectBase):
    """
    @brief 建筑收集默认实现类
    @details 从 StructureSummary 中提取建筑数据，按州和建筑类型进行合并统计
    """
    def collect(self, source_summary: SourceSummary, structure_summary: StructureSummary) -> tuple[str, Any]:
        """
        @brief 收集建筑数据
        @details 从 StructureSummary 中提取建筑数据，按州和建筑类型进行合并统计

        @param source_summary 原始数据汇总对象（此实现中未使用）
        @param structure_summary 结构化数据汇总对象，包含建筑数据
        @return 元组 ("building", CollectBuildingResult)
        """
        logger.info("Starting building data collection")

        # 初始化数据结构
        state_building_level_dict = self.collect_building_levels(structure_summary)

        # 转换为最终结果
        state_building_dict = self.collect_build_state_building_dict(state_building_level_dict)

        result = CollectBuildingStateResult(state_building_dict=state_building_dict)

        logger.info(f"Building data collection completed, collected {len(state_building_dict)} states")
        return 'building', result

    def collect_building_levels(self, structure_summary: StructureSummary) -> dict[StateNamePrefix, dict[str, int]]:
        """
        @brief 收集建筑等级数据
        @details 遍历结构化建筑数据，按州和建筑类型汇总等级

        @param structure_summary 结构化数据汇总对象
        @return 字典：州前缀 -> {建筑类型: 总等级}
        """
        # 使用 defaultdict 简化字典初始化
        state_building_level_dict: dict[StateNamePrefix, dict[str, int]] = defaultdict(lambda: defaultdict(int))

        # 遍历所有结构化建筑数据
        for structured_building_state in structure_summary.building_data.values():
            if not isinstance(structured_building_state, StructuredBuildingState):
                logger.warning(f"Expected StructuredBuildingState, got {type(structured_building_state)}")
                continue

            # 处理每个结构化州建筑数据
            self.collect_process_structured_building_state(structured_building_state, state_building_level_dict)

        # 将 defaultdict 转换回普通 dict
        return {
            state_prefix: dict(building_dict)
            for state_prefix, building_dict in state_building_level_dict.items()
        }

    def collect_process_structured_building_state(self, structured_building_state: StructuredBuildingState,
                                                  state_building_level_dict: dict[StateNamePrefix, dict[str, int]]) -> None:
        """
        @brief 处理结构化州建筑数据
        @details 遍历州建筑字典，处理每个州的建筑列表

        @param structured_building_state 结构化州建筑数据对象
        @param state_building_level_dict 建筑等级字典（会被修改）
        """
        for state_prefix, building_list in structured_building_state.state_building_dict.items():
            self.collect_process_state_building_list(state_prefix, building_list, state_building_level_dict)

    def collect_process_state_building_list(self, state_prefix: StateNamePrefix,
                                            building_list: list[StructuredBuildingItem | StructuredBuildingNoOwnerItem],
                                            state_building_level_dict: dict[StateNamePrefix, dict[str, int]]) -> None:
        """
        @brief 处理州的建筑列表
        @details 遍历州下的所有建筑项目

        @param state_prefix 州前缀
        @param building_list 建筑项目列表
        @param state_building_level_dict 建筑等级字典（会被修改）
        """
        for building_item in building_list:
            self.collect_process_building_item(state_prefix, building_item, state_building_level_dict)

    def collect_process_building_item(self, state_prefix: StateNamePrefix,
                                      building_item: StructuredBuildingItem | StructuredBuildingNoOwnerItem,
                                      state_building_level_dict: dict[StateNamePrefix, dict[str, int]]) -> None:
        """
        @brief 处理单个建筑项目
        @details 根据建筑项目类型累加等级

        @param state_prefix 州前缀
        @param building_item 建筑项目对象
        @param state_building_level_dict 建筑等级字典（会被修改）
        """
        if isinstance(building_item, StructuredBuildingNoOwnerItem):
            self.collect_process_no_owner_building(state_prefix, building_item, state_building_level_dict)
        elif isinstance(building_item, StructuredBuildingItem):
            self.collect_process_owned_building(state_prefix, building_item, state_building_level_dict)
        else:
            logger.warning(f"Unknown building item type: {type(building_item)}")

    def collect_process_no_owner_building(self, state_prefix: StateNamePrefix, building_item: StructuredBuildingNoOwnerItem,
                                          state_building_level_dict: dict[StateNamePrefix, dict[str, int]]) -> None:
        """
        @brief 处理无所有者的建筑项目
        @details 累加无所有者建筑等级

        @param state_prefix 州前缀
        @param building_item 无所有者建筑项目
        @param state_building_level_dict 建筑等级字典（会被修改）
        """
        building_type = building_item.building
        level = building_item.level

        # 检查建筑类型是否有效
        if not building_type or not building_type.strip():
            logger.warning(f"Empty building type for state {state_prefix}")
            return

        # 检查等级是否有效
        if level <= 0:
            logger.warning(f"Invalid building level ({level}) for type '{building_type}' in state {state_prefix}")
            # 仍可累加，因为可能是游戏数据问题

        # 使用 defaultdict 时不需要检查键是否存在
        state_building_level_dict[state_prefix][building_type] += level

    def collect_process_owned_building(self, state_prefix: StateNamePrefix, building_item: StructuredBuildingItem,
                                       state_building_level_dict: dict[StateNamePrefix, dict[str, int]]) -> None:
        """
        @brief 处理有所有者的建筑项目
        @details 累加有所有者建筑等级（可能有多个所有权）

        @param state_prefix 州前缀
        @param building_item 有所有者建筑项目
        @param state_building_level_dict 建筑等级字典（会被修改）
        """
        building_type = building_item.building

        # 检查建筑类型是否有效
        if not building_type or not building_type.strip():
            logger.warning(f"Empty building type for state {state_prefix}")
            return

        # 检查是否有所有权信息
        if not building_item.add_ownership:
            logger.warning(f"No ownership information for building '{building_type}' in state {state_prefix}")
            return

        # 累加所有所有权等级
        total_level = 0
        for building_ownership in building_item.add_ownership:
            if building_ownership.level <= 0:
                logger.warning(f"Invalid ownership level ({building_ownership.level}) for building '{building_type}' in state {state_prefix}")
            total_level += building_ownership.level

        # 使用 defaultdict 时不需要检查键是否存在
        if total_level > 0:
            state_building_level_dict[state_prefix][building_type] += total_level
        else:
            logger.warning(f"Zero or negative total level for building '{building_type}' in state {state_prefix}")

    def collect_build_state_building_dict(self, state_building_level_dict: dict[StateNamePrefix, dict[str, int]]) -> dict[StateNamePrefix, list[CollectBuildingStateItem]]:
        """
        @brief 构建最终的建筑字典
        @details 将等级字典转换为 CollectBuildingStateItem 列表

        @param state_building_level_dict 建筑等级字典
        @return 字典：州前缀 -> CollectBuildingStateItem 列表
        """
        state_building_dict: dict[StateNamePrefix, list[CollectBuildingStateItem]] = {}

        for state_prefix, building_level_dict in state_building_level_dict.items():
            building_items = [
                CollectBuildingStateItem(building=building, level=level)
                for building, level in building_level_dict.items()
            ]
            state_building_dict[state_prefix] = building_items

        return state_building_dict


if __name__ == '__main__':
    pass
