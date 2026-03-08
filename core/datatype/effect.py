# -*- coding:utf-8 -*-
# AUTHOR: Sun

from dataclasses import dataclass

from core.datatype.prefix import CountryTagPrefix


@dataclass(frozen=True)
class EffectCountry(object):
    """
    @brief 效果国家数据类
    @details 表示一个国家的效果信息，包含布尔效果和特殊效果
    """
    boolean_effect: tuple[str, ...]                   # 布尔效果列表
    special_effect: tuple[tuple[str, str], ...]       # 特殊效果列表（键值对）

    def __post_init__(self):
        """
        @brief 后初始化方法，确保列表类型属性转换为元组，并验证特殊效果格式
        """
        if isinstance(self.boolean_effect, list):
            object.__setattr__(self, 'boolean_effect', tuple(self.boolean_effect))
        if isinstance(self.special_effect, list):
            object.__setattr__(self, 'special_effect', tuple(self.special_effect))

        # 验证特殊效果元组长度均为2（键值对）
        if self.special_effect and not all(len(pair) == 2 for pair in self.special_effect):
            raise ValueError("特殊效果列表中的每个元素必须为长度为2的元组（键值对）")


@dataclass(frozen=True)
class EffectFile(object):
    """
    @brief 效果文件数据类
    @details 表示整个效果文件的数据结构，包含根键和国家效果字典
    """
    root_key: str | None                                        # 根键
    effect_country_dict: dict[CountryTagPrefix, EffectCountry]  # 国家效果字典


if __name__ == '__main__':
    pass