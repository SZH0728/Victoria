# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 建筑收集数据类模块
@details 提供建筑数据收集结果的数据类定义

此模块定义了 CollectBuildingStateItem 和 CollectBuildingResult 数据类，
用于存储建筑数据的收集统计结果，以州为单位统计建筑类型和等级。
"""

from dataclasses import dataclass, field

from core.datatype.prefix import StateNamePrefix


@dataclass
class CollectBuildingStateItem(object):
    """
    @brief 建筑收集州项目数据类
    @details 表示一个州内特定建筑类型的统计信息，包含建筑类型和总等级

    此数据类用于存储按州和建筑类型合并后的建筑统计信息，
    相同建筑类型的等级会被相加。
    """
    building: str  # 建筑类型
    level: int     # 建筑总等级

    def __post_init__(self):
        """
        @brief 后初始化方法，验证建筑等级为正整数
        """
        if self.level <= 0:
            raise ValueError(f"{self.__class__.__name__}: Building level must be a positive integer, got: {self.level}")


@dataclass
class CollectBuildingStateResult(object):
    """
    @brief 建筑收集结果数据类
    @details 表示建筑数据收集的完整结果，包含所有州的建筑统计信息

    此数据类存储整个建筑收集模块的输出结果，按州组织建筑统计信息。
    每个州对应一个 CollectBuildingStateItem 列表，列表中的每个项目表示
    该州内特定建筑类型的合并统计信息。
    """
    state_building_dict: dict[StateNamePrefix, list[CollectBuildingStateItem]] = field(default_factory=dict)


if __name__ == '__main__':
    pass
