# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from core.datatype.prefix import StateNamePrefix, CountryTagPrefix
from core.datatype.source.state import StateFile, StateItem, StateCountryItem
from core.datatype.structure.state import StateCountryItem as StructuredStateCountryItem
from core.middleware.base import DestructureBase

logger = getLogger(__name__)


class DestructureState(DestructureBase):
    """
    @brief 州数据解构转换类
    @details 将以国家为键的结构化数据字典转换回StateFile字典
    转换逻辑: dict[CountryTagPrefix, StateCountryItem] → dict[str, StateFile]
    输出直接兼容: transform.state.TransformStateDefault().main()的输入
    """
    def convert(self, structure_dict: dict[CountryTagPrefix, StructuredStateCountryItem]) -> dict[str, StateFile]:
        """
        @brief 转换结构化数据回源数据
        @param structure_dict 结构化数据字典，键为国家标签，值为StateCountryItem对象
        @return 源数据字典，键为文件名，值为StateFile对象
                 (可直接传递给transform.state.TransformStateDefault().main())
        """
        state_to_countries: dict[StateNamePrefix, dict[CountryTagPrefix, Any]] = {}

        for country, country_item in structure_dict.items():
            for state_name, structured_state in country_item.owned_states.items():
                if state_name not in state_to_countries:
                    state_to_countries[state_name] = {}

                state_to_countries[state_name][country] = {
                    'owned_provinces': structured_state.owned_provinces,
                    'state_type': structured_state.state_type,
                    'homeland_cultures': structured_state.homeland_cultures,
                    'claimed_by': structured_state.claimed_by
                }

        filename: str = '80_state.txt'
        result: dict[str, StateFile] = {}
        state_item_dict: dict[StateNamePrefix, StateItem] = {}

        for state_name, country_dict in state_to_countries.items():
            create_state_items = []
            all_homeland_cultures = set()
            all_claimed_by = set()

            for country, value in country_dict.items():
                state_country_item = StateCountryItem(
                    country=country,
                    owned_provinces=value['owned_provinces'],
                    state_type=value['state_type']
                )
                create_state_items.append(state_country_item)

                all_homeland_cultures.update(value['homeland_cultures'])
                all_claimed_by.update(value['claimed_by'])

            state_item = StateItem(
                create_state=tuple(create_state_items),
                add_homeland=tuple(all_homeland_cultures),
                add_claim=tuple(all_claimed_by)
            )

            state_item_dict[state_name] = state_item

        result[filename] = StateFile(root_key='state', state_item_dict=state_item_dict)

        return result


if __name__ == '__main__':
    pass