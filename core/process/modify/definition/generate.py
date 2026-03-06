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
from core.datatype.combination import DataGenerateType
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

        country_type_generate_function: DataGenerateType = self.middle.get('country_type_generate_function', DataGenerateType.default)
        country_type_fix: str = self.middle.get('set_fix_country_type', 'recognized')
        country_type_random_weight = self.middle.get('set_random_country_type_weight', [2, 3, 5])

        main_culture_generate_function: DataGenerateType = self.middle.get('main_culture_generate_function', DataGenerateType.default)
        main_culture_max_number: int = self.middle.get('set_main_culture_max_number', 1)
        main_culture_fix: str = self.middle.get('set_fix_main_culture', None)

        if main_culture_fix is None and main_culture_generate_function == DataGenerateType.fix:
            raise ValueError('Invalid main_culture_fix')

        enable_named_from_capital: bool = self.middle.get('enable_named_from_capital', None)

        for region_population in self.target.population.values():
            for country_population in region_population.population:
                for population_item in country_population.population:
                    if country_population.country_tag not in population_item_map:
                        population_item_map[country_population.country_tag] = [population_item]
                    else:
                        population_item_map[country_population.country_tag].append(population_item)

        for tag, population_item_list in population_item_map.items():
            capital_region = self.middle['country_state'][tag][0]

            country_type: str = 'recognized'
            if country_type_generate_function == DataGenerateType.default:
                pass
            elif country_type_generate_function == DataGenerateType.fix:
                country_type = country_type_fix
            elif country_type_generate_function == DataGenerateType.randomize:
                country_type_list: list[str] = ['recognized', 'unrecognized', 'decentralized']
                country_type = choices(country_type_list, weights=country_type_random_weight, k=1)[0]
            else:
                raise ValueError('Invalid country_type_generate_function')

            main_culture: list[str] = []
            population_item_list.sort(key=lambda x: x.size, reverse=True)
            if main_culture_generate_function == DataGenerateType.default:
                for population_item in population_item_list:
                    culture = population_item.culture
                    if culture not in main_culture:
                        main_culture.append(culture)

                    if len(main_culture) >= main_culture_max_number:
                        break
            elif main_culture_generate_function == DataGenerateType.fix:
                main_culture = [main_culture_fix]
            elif main_culture_generate_function == DataGenerateType.randomize:
                all_culture = set([population_item.culture for population_item in population_item_list])
                main_culture = choices(list(all_culture), k=main_culture_max_number)
            else:
                raise ValueError('Invalid main_culture_generate_function')

            country_definition = CountryDefinition(
                country_tag=tag,
                color=(randint(50, 200), randint(50, 200), randint(50, 200)),
                country_type=country_type,
                tier='empire',
                culture=tuple(main_culture),
                capital=f'STATE_{capital_region.upper()}',

                religion=None,
                is_named_from_capital='yes' if enable_named_from_capital else None,
                valid_as_home_country_for_separatists=None,
                social_hierarchy=None,
                unit_color=None
            )
            definition_map[tag] = country_definition

        return definition_map

if __name__ == '__main__':
    pass
