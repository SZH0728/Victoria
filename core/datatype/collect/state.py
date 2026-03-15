# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 州收集数据类模块
@details 提供州数据收集结果的数据类定义
"""

from dataclasses import dataclass, field

from core.datatype.prefix import StateNamePrefix, RegionNamePrefix


@dataclass(frozen=True)
class CollectStateResult(object):
    """
    @brief 州收集结果数据类
    @details 表示州数据收集的完整结果，包含所有州的统计信息
    """
    state_province_dict: dict[StateNamePrefix, list[str]] = field(default_factory=dict)
    region_states_dict: dict[RegionNamePrefix, list[StateNamePrefix]] = field(default_factory=dict)


if __name__ == '__main__':
    pass