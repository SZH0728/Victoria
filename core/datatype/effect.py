# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 效果数据定义模块
@details 定义了维多利亚3游戏中效果相关的数据结构，包括布尔效果、特殊效果等
"""

from dataclasses import dataclass

from core.datatype.prefix import CountryTagPrefix


@dataclass(frozen=True)
class EffectCountry(object):
    """
    @brief 国家效果数据类
    @details 表示一个国家的游戏效果，包括布尔效果指令和特殊效果
    """
    boolean_effect: tuple[str, ...]              #!< 效果列表（游戏指令字符串）
    special_effect: tuple[tuple[str, str], ...]  #!< 特殊效果列表（(键, 值)元组）

    def __post_init__(self):
        """@brief 初始化后处理，确保所有字段都是元组类型"""
        if isinstance(self.boolean_effect, list):
            object.__setattr__(self, 'boolean_effect', tuple(self.boolean_effect))
        if isinstance(self.special_effect, list):
            object.__setattr__(self, 'special_effect', tuple(self.special_effect))


@dataclass(frozen=True)
class EffectFile(object):
    """
    @brief 效果文件数据容器
    @details 包含效果数据的根键和国家效果字典
    """
    root_key: str | None
    effect_country_dict: dict[CountryTagPrefix, EffectCountry]


if __name__ == '__main__':
    pass