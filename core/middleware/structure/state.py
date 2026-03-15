# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from core.datatype.prefix import StateNamePrefix, CountryTagPrefix
from core.datatype.source.state import StateFile, StateItem, StateCountryItem
from core.datatype.structure.state import StateCountryItem as StructuredStateCountryItem
from core.datatype.structure.state import StructuredStateItem
from core.middleware.base import StructureBase

logger = getLogger(__name__)


class StructureState(StructureBase):
    """
    @brief 州数据结构化转换类
    @details 将StateFile字典转换为以国家为键的结构化数据字典
    转换逻辑: dict[str, StateFile] → dict[CountryTagPrefix, StateCountryItem]
    输入直接兼容: analysis.state.AnalysisStateDefault().result
    """
    def convert(self, source_dict: dict[str, StateFile]) -> dict[CountryTagPrefix, StructuredStateCountryItem]:
        """
        @brief 转换州源数据为结构化数据
        @param source_dict 源数据字典，键为文件名，值为StateFile对象
                           (来自analysis.state.AnalysisStateDefault().result)
        @return 结构化数据字典，键为国家标签，值为StateCountryItem对象
        """
        result: dict[CountryTagPrefix, StructuredStateCountryItem] = {}

        for filename, state_file in source_dict.items():
            logger.debug(f"Processing file: {filename}")

            for state_name_prefix, state_item in state_file.state_item_dict.items():
                # 遍历每个州中的国家信息
                for state_country_item in state_item.create_state:
                    country = state_country_item.country

                    if country not in result:
                        # 创建新的国家州项目
                        result[country] = StructuredStateCountryItem(owned_states={})

                    # 构建结构化州信息
                    structured_state = StructuredStateItem(
                        owned_provinces=state_country_item.owned_provinces,
                        state_type=state_country_item.state_type,
                        homeland_cultures=state_item.add_homeland,
                        claimed_by=state_item.add_claim
                    )

                    result[country].owned_states[state_name_prefix] = structured_state

        return result


if __name__ == '__main__':
    pass