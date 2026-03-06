# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.process.modify.effect.randomize
@brief 效果随机化修改器模块
@details 为国家效果数据随机生成起始技术和法律
"""

from typing import Any
from random import choices

from core.datatype.map import Map
from core.datatype.effect import CountryEffect
from core.datatype.combination import DataGenerateType
from core.process.modify.effect.base import EffectModifyBase


class EffectModifyRandomize(EffectModifyBase):
    """!
    @brief 效果随机化修改器
    @details 为每个新生成的国家随机分配起始技术和法律效果
    """
    def modify(self) -> Any:
        """!
        @brief 执行效果随机化修改
        @details 为每个新生成的国家随机分配起始技术和法律效果：
                 1. 从中间参数获取配置（是否启用随机技术、技术范围、是否启用随机法律）
                 2. 根据技术范围生成技术列表和权重（高级技术权重更低）
                 3. 预定义法律效果列表
                 4. 根据配置随机选择技术和法律效果
                 5. 遍历标签映射，为每个国家创建效果对象

        @return 国家效果映射 Map[CountryEffect]
        """
        effect: Map[CountryEffect] = Map()

        technology_generate_function = self.middle.get('technology_generate_function', DataGenerateType.default)
        technology_fix: int = self.middle.get('technology_fix', 6)
        technology_random_range: tuple[int, int] = self.middle.get('random_technology_range', (1, 6))
        technology_random_weight: list[int] = self.middle.get('random_technology_weight', None)

        if technology_random_range[0] > technology_random_range[1]:
            technology_random_range = (technology_random_range[1], technology_random_range[0])

        technology_random_list: list[str] = [f'effect_starting_technology_tier_{i}_tech' for i in range(technology_random_range[0], technology_random_range[1] + 1)]
        if technology_random_weight is None:
            technology_random_weight = list(range(technology_random_range[0], technology_random_range[1] + 1))

        if (technology_random_range[1] - technology_random_range[0] + 1) != len(technology_random_weight):
            raise ValueError('technology_random_weight length must be equal to technology_random_range')

        laws_generate_function = self.middle.get('laws_generate_function', DataGenerateType.default)
        laws_fix: str = self.middle.get('laws_fix', 'effect_starting_politics_traditional')

        law: list[str] = [
            'effect_starting_politics_traditional',
            'effect_starting_politics_princely_state',
            'effect_starting_politics_conservative',
            'effect_starting_politics_liberal',
            'effect_starting_politics_reactionary'
        ]

        for key, value in self.middle['tag'].items():
            effect_list: list[str] = []

            if technology_generate_function == DataGenerateType.default:
                effect_list.append('effect_starting_technology_tier_6_tech')
            elif technology_generate_function == DataGenerateType.fix:
                effect_list.append(f'effect_starting_technology_tier_{technology_fix}_tech')
            elif technology_generate_function == DataGenerateType.randomize:
                effect_list.append(choices(technology_random_list, weights=technology_random_weight, k=1)[0])

            if laws_generate_function == DataGenerateType.default:
                effect_list.append('effect_starting_politics_traditional')
            elif laws_generate_function == DataGenerateType.fix:
                effect_list.append(laws_fix)
            elif laws_generate_function == DataGenerateType.randomize:
                effect_list.append(choices(law, k=1)[0])

            effect_item = CountryEffect(
                country_name=value,
                country_tag=key,
                effect=tuple(effect_list),
                special_effect=(),
            )

            effect[key] = effect_item

        return effect

if __name__ == '__main__':
    pass
