# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 人口收集数据类模块
@details 提供人口数据收集结果的数据类定义

此模块定义了 CollectPopulationStateItem 和 CollectPopulationResult 数据类，
用于存储人口数据的收集统计结果，按州和人口特征（文化、宗教、类型）合并统计。
"""

from dataclasses import dataclass, field

from core.datatype.prefix import StateNamePrefix


@dataclass
class CollectPopulationStateItem(object):
    """
    @brief 人口收集州项目数据类
    @details 表示一个州内特定人口特征的统计信息，包含特征和合并后的人口规模

    此数据类用于存储按州和人口特征合并后的人口统计信息，
    相同特征（文化、宗教、类型）的人口规模会被相加。
    """
    culture: str | None      # 文化（None 表示空值）
    religion: str | None     # 宗教（None 表示空值）
    pop_type: str | None     # 人口类型（None 表示空值）
    size: int                # 合并后的人口规模

    def __post_init__(self):
        """
        @brief 后初始化方法，验证人口规模非负
        """
        if self.size < 0:
            raise ValueError(f"{self.__class__.__name__}: Population size must be non-negative integer, got: {self.size}")


@dataclass(frozen=True)
class CollectPopulationResult(object):
    """
    @brief 人口收集结果数据类
    @details 表示人口数据收集的完整结果，包含所有州的人口统计信息和总人口

    此数据类存储整个人口收集模块的输出结果，按州组织人口统计信息。
    每个州对应一个 CollectPopulationStateItem 列表，列表中的每个项目表示
    该州内特定人口特征的合并统计信息。
    """
    state_to_population_dict: dict[StateNamePrefix, list[CollectPopulationStateItem]] = field(default_factory=dict)
    state_total_population: dict[StateNamePrefix, int] = field(default_factory=dict)



if __name__ == '__main__':
    pass