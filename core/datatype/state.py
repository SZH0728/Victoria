# -*- coding:utf-8 -*-
# AUTHOR: Sun

from dataclasses import dataclass

from core.datatype.prefix import StateNamePrefix, CountryTagPrefix, CultureNamePrefix


@dataclass(frozen=True)
class StateCountryItem(object):
    """
    @brief 州国家项目数据类
    @details 表示一个国家在州中的所有权信息，包含国家、拥有的省份和州类型
    """
    country: CountryTagPrefix             # 国家标签
    owned_provinces: tuple[str, ...]      # 拥有的省份列表
    state_type: str | None                # 州类型

    def __post_init__(self):
        """
        @brief 后初始化方法，确保列表类型属性转换为元组
        """
        if isinstance(self.owned_provinces, list):
            object.__setattr__(self, 'owned_provinces', tuple(self.owned_provinces))


@dataclass(frozen=True)
class StateItem(object):
    """
    @brief 州项目数据类
    @details 表示游戏中的一个州，包含创建州信息、家园文化和宣称国家
    """
    create_state: tuple[StateCountryItem, ...]   # 创建州信息列表
    add_homeland: tuple[CultureNamePrefix, ...]  # 家园文化列表
    add_claim: tuple[CountryTagPrefix, ...]      # 宣称国家列表

    def __post_init__(self):
        """
        @brief 后初始化方法，确保列表类型属性转换为元组
        """
        if isinstance(self.create_state, list):
            object.__setattr__(self, 'create_state', tuple(self.create_state))
        if isinstance(self.add_homeland, list):
            object.__setattr__(self, 'add_homeland', tuple(self.add_homeland))
        if isinstance(self.add_claim, list):
            object.__setattr__(self, 'add_claim', tuple(self.add_claim))


@dataclass(frozen=True)
class StateFile(object):
    """
    @brief 州文件数据类
    @details 表示整个州文件的数据结构，包含根键和州项目字典
    """
    root_key: str | None                               # 根键
    state_item_dict: dict[StateNamePrefix, StateItem]   # 州项目字典


if __name__ == '__main__':
    pass