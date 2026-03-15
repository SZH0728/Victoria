# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 结构化州数据模块
@details 提供州数据的结构化版本，包括州项目数据类和国家州项目数据类

此模块定义了以国家为顶层键的州数据结构，用于按国家组织州信息。
"""

from dataclasses import dataclass

from core.datatype.prefix import StateNamePrefix, CountryTagPrefix, CultureNamePrefix


@dataclass(frozen=True)
class StructuredStateItem(object):
    """
    @brief 结构化州项目数据类
    @details 表示游戏中的一个州的结构化信息，包含省份、州类型、家园文化和宣称国家

    此数据类用于存储州级别的核心信息，所有列表属性在初始化后会转换为不可变的元组。
    """
    owned_provinces: tuple[str, ...]                  # 拥有的省份列表
    state_type: str | None                            # 州类型
    homeland_cultures: tuple[CultureNamePrefix, ...]  # 家园文化列表（州级别）
    claimed_by: tuple[CountryTagPrefix, ...]          # 宣称该州的国家列表（州级别）

    def __post_init__(self):
        """
        @brief 后初始化方法，确保列表类型属性转换为元组
        @details 此方法在对象初始化后自动调用，将可能传入的列表转换为不可变元组，
                 以保持数据类的不可变性和哈希性
        """
        if isinstance(self.owned_provinces, list):
            object.__setattr__(self, 'owned_provinces', tuple(self.owned_provinces))
        if isinstance(self.homeland_cultures, list):
            object.__setattr__(self, 'homeland_cultures', tuple(self.homeland_cultures))
        if isinstance(self.claimed_by, list):
            object.__setattr__(self, 'claimed_by', tuple(self.claimed_by))


@dataclass(frozen=True)
class StateCountryItem(object):
    """
    @brief 国家州项目数据类
    @details 表示一个国家拥有的州信息，以国家为顶层键的结构化数据

    此数据类用于按国家组织州信息，每个国家包含其拥有的州字典。
    注意：claimed_states（宣称的州）和 homeland_states（家园州）可以通过遍历
    所有州的 claimed_by 和 homeland_cultures 推导得出，因此不在此存储，
    以保持数据结构简洁。
    """
    owned_states: dict[StateNamePrefix, StructuredStateItem]  # 拥有的州字典


if __name__ == '__main__':
    pass
