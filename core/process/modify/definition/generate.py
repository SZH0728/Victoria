# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.process.modify.definition.generate
@brief 国家定义生成修改器模块
@details 根据人口数据生成新的国家定义，包括国家类型、颜色、文化、首都等
"""

from typing import Any
from random import randint, choices

from core.datatype.map import Map
from core.datatype.population import PopulationItem
from core.datatype.definition import CountryDefinition
from core.process.modify.definition.base import DefinitionModifyBase


class DefinitionModifyGenerate(DefinitionModifyBase):
    """!
    @brief 国家定义生成修改器
    @details 根据人口数据生成新的国家定义，为每个新国家设置基本属性
    """
    def modify(self) -> Any:
        """!
        @brief 执行国家定义生成修改
        @details 根据人口数据生成新的国家定义：
                 1. 从中间参数获取配置（是否启用随机国家类型、权重、固定国家类型）
                 2. 遍历目标人口数据，按国家标签聚合人口项
                 3. 对每个国家的人口项按数量排序，确定主要文化
                 4. 根据配置确定国家类型（可随机或固定）
                 5. 生成随机颜色（RGB值在50-200之间）
                 6. 设置国家等级为"empire"
                 7. 确定首都（从国家-州映射中获取第一个州）
                 8. 创建国家定义对象

        @return 国家定义映射 Map[CountryDefinition]
        """
        population_item_map: Map[list[PopulationItem]] = Map()
        definition_map: Map[CountryDefinition] = Map()

        enable_random_country_type = self.middle.get('enable_random_country_type', False)
        random_country_weight = self.middle.get('random_country_type_weight', [2, 3, 5])
        set_fix_country_type = self.middle.get('set_fix_country_type', 'unrecognized')

        for region_population in self.target.population.values():
            for country_population in region_population.population:
                for population_item in country_population.population:
                    if country_population.country_tag not in population_item_map:
                        population_item_map[country_population.country_tag] = [population_item]
                    else:
                        population_item_map[country_population.country_tag].append(population_item)

        for tag, population_item_list in population_item_map.items():
            population_item_list.sort(key=lambda x: x.size, reverse=True)

            capital_region = self.middle['country_state'][tag][0]

            country_type: list[str] = ['recognized', 'unrecognized', 'decentralized']

            country_type_target: str = set_fix_country_type
            if enable_random_country_type:
                country_type_target = choices(country_type, weights=random_country_weight, k=1)[0]

            main_culture = population_item_list[0].culture
            country_definition = CountryDefinition(
                country_tag=tag,
                color=(randint(50, 200), randint(50, 200), randint(50, 200)),
                country_type=country_type_target,
                tier='empire',
                culture=(main_culture,),
                capital=f'STATE_{capital_region.upper()}',

                religion=None,
                is_named_from_capital=None,
                valid_as_home_country_for_separatists=None,
                social_hierarchy=None,
                unit_color=None
            )
            definition_map[tag] = country_definition

        return definition_map

if __name__ == '__main__':
    pass
