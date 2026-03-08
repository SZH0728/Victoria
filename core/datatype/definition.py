# -*- coding:utf-8 -*-
# AUTHOR: Sun

from dataclasses import dataclass

from core.datatype.prefix import StateNamePurePrefix


@dataclass(frozen=True)
class CountryDefinition(object):
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


if __name__ == '__main__':
    pass