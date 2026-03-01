# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.process.modify.effect.empty
@brief 效果清空修改器模块
@details 创建空的国家效果数据，移除所有原始效果
"""

from typing import Any

from core.datatype.map import Map
from core.datatype.effect import CountryEffect
from core.process.modify.effect.base import EffectModifyBase


class EffectModifyEmpty(EffectModifyBase):
    """!
    @brief 效果清空修改器
    @details 创建空的国家效果数据结构，用于移除所有原始效果信息
    """
    def modify(self) -> Any:
        """!
        @brief 执行效果清空修改
        @details 创建空的效果数据结构：
                 1. 遍历中间数据中的标签映射
                 2. 为每个国家标签创建空的CountryEffect对象（效果和特殊效果字段为空元组）
                 3. 存储到效果映射中

        @return 空的效果映射 Map[CountryEffect]
        """
        effect: Map[CountryEffect] = Map()

        for key, value in self.middle['tag'].items():
            effect_item = CountryEffect(
                country_name=value,
                country_tag=key,
                effect=(),
                special_effect=(),
            )

            effect[key] = effect_item

        return effect

if __name__ == '__main__':
    pass
