# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 州数据定义模块
@details 定义了维多利亚3游戏中州相关的数据结构，包括州与国家的关系、文化信息等
"""

from dataclasses import dataclass

from core.datatype.prefix import StateNamePrefix, CountryTagPrefix, CultureNamePrefix


@dataclass(frozen=True)
class StateCountryItem(object):
    """
    @brief 州-国家项数据类
    @details 表示一个州与国家之间的关系，包含国家标签、所属省份和州类型信息
    """

    country: CountryTagPrefix           #!< 国家标签
    owned_provinces: tuple[str, ...]    #!< 所属省份ID列表
    state_type: str | None              #!< 州类型

    def __post_init__(self):
        """@brief 初始化后处理，确保owned_provinces为元组类型"""
        if isinstance(self.owned_provinces, list):
            object.__setattr__(self, 'owned_provinces', tuple(self.owned_provinces))


@dataclass(frozen=True)
class StateItem(object):
    """
    @brief 州数据项
    @details 表示一个州的所有相关信息，包括国家所有权、本土文化和宣称文化
    """

    create_state: tuple[StateCountryItem, ...]    #!< 国家所有权列表（一个州可能有多个国家拥有）
    add_homeland: tuple[CultureNamePrefix, ...]   #!< 本土文化列表
    add_claim: tuple[CountryTagPrefix, ...]       #!< 宣称文化列表

    def __post_init__(self):
        """@brief 初始化后处理，确保所有字段都是元组类型"""
        if isinstance(self.create_state, list):
            object.__setattr__(self, 'create_state', tuple(self.create_state))
        if isinstance(self.add_homeland, list):
            object.__setattr__(self, 'add_homeland', tuple(self.add_homeland))
        if isinstance(self.add_claim, list):
            object.__setattr__(self, 'add_claim', tuple(self.add_claim))


@dataclass(frozen=True)
class StateFile(object):
    """
    @brief 州文件数据容器
    @details 包含州数据的根键和州项字典
    """

    root_key: str | None
    """@brief 文件根键（可选）"""

    stat_item_dict: dict[StateNamePrefix, StateItem]
    """@brief 州名称到州项的映射字典"""


if __name__ == '__main__':
    pass