# -*- coding:utf-8 -*-
# AUTHOR: Sun

from dataclasses import dataclass

from core.datatype.prefix import StateNamePurePrefix, CountryTagPrefix


@dataclass(frozen=True)
class DefinitionCountry(object):
    """
    @brief 国家定义数据类
    @details 表示游戏中的国家定义，包含颜色、类型、等级、文化、首都等信息
    """
    color: tuple[int, ...]                              # 国家颜色
    country_type: str                                   # 国家类型
    tier: str                                           # 国家等级
    cultures: tuple[str, ...]                           # 文化列表
    capital: StateNamePurePrefix | None                 # 首都

    religion: str | None                                # 宗教
    is_named_from_capital: bool | None                  # 是否以首都命名
    valid_as_home_country_for_separatists: str | None   # 可作为分离主义者母国
    social_hierarchy: str | None                        # 社会等级制度
    unit_color: dict[str, list[int]]                    # 单位颜色字典

    def __post_init__(self):
        """
        @brief 后初始化方法，确保列表类型属性转换为元组
        """
        if isinstance(self.color, list):
            object.__setattr__(self, 'color', tuple(self.color))
        if isinstance(self.cultures, list):
            object.__setattr__(self, 'cultures', tuple(self.cultures))


@dataclass(frozen=True)
class DefinitionFile(object):
    """
    @brief 国家定义文件数据类
    @details 包含国家定义文件的根键和以国家标签为键的国家定义字典
    """
    root_key: str | None                                                # 根键
    definition_country_dict: dict[CountryTagPrefix, DefinitionCountry]  # 国家定义字典，键为国家标签前缀


if __name__ == '__main__':
    pass