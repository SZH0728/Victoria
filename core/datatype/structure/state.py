# -*- coding:utf-8 -*-
# AUTHOR: Sun

from dataclasses import dataclass

from core.datatype.prefix import StateNamePrefix, CountryTagPrefix, CultureNamePrefix


@dataclass(frozen=True)
class StructuredStateItem(object):
    """
    @brief 结构化州项目数据类
    @details 表示游戏中的一个州的结构化信息，包含省份、州类型、家园文化和宣称国家
    """
    owned_provinces: tuple[str, ...]              # 拥有的省份列表
    state_type: str | None                        # 州类型
    homeland_cultures: tuple[CultureNamePrefix, ...]  # 家园文化列表（州级别）
    claimed_by: tuple[CountryTagPrefix, ...]      # 宣称该州的国家列表（州级别）

    def __post_init__(self):
        """
        @brief 后初始化方法，确保列表类型属性转换为元组
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
    """
    owned_states: dict[StateNamePrefix, StructuredStateItem]  # 拥有的州字典
    # 注意：claimed_states 和 homeland_states 可通过遍历所有州的 claimed_by 和 homeland_cultures 推导得出
    # 因此不在此存储，以保持数据结构简洁


if __name__ == '__main__':
    pass
