# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.process.modify.state.state
@brief 单州国家修改器模块
@details 将每个州分配为独立的国家，创建一对一的国家-州关系
"""

from typing import Any

from core.datatype.state import StatePlot, State, CountryState
from core.datatype.map import Map
from core.process.modify.state.base import StateModifyBase

class StateModifySingleStateCountry(StateModifyBase):
    """!
    @brief 单州国家修改器
    @details 将每个州分配为独立的国家，每个国家只拥有一个州
    """
    @staticmethod
    def generate_country_tag(name: str) -> str:
        """!
        @brief 根据州名生成国家标签
        @details 从州名称生成3位国家标签，规则：
                 1. 使用"AW"作为前缀（Alternate World）
                 2. 如果州名是一个单词：取前3个字母
                 3. 如果州名是两个单词：各取前2个和1个字母
                 4. 如果州名是三个及以上单词：各取首字母
                 示例："new_york" -> "AWNY"

        @param name 州名称（可能包含下划线分隔的单词）
        @return 生成的国家标签（如"AWNY"）
        """
        tokens = name.split('_')

        if len(tokens) == 1:
            # 单词：取前3个字母
            tag = tokens[0][:3].upper()
        elif len(tokens) == 2:
            # 两个单词：各取前2个和1个字母
            tag = tokens[0][:2].upper() + tokens[1][:1].upper()
        else:
            # 三个及以上单词：各取首字母
            tag = ''.join(token[:1].upper() for token in tokens[:3])

        return f'AW{tag}'

    @staticmethod
    def generate_alternative_tag(existing_tag: str) -> str:
        """!
        @brief 生成替代标签以避免重复
        @details 当生成的标签已存在时，通过递增最后一个字母来生成新标签
                 示例："AWNY" -> "AWNZ"，如果到"Z"则回绕到"A"

        @param existing_tag 已存在的标签
        @return 新的替代标签
        """
        letter = existing_tag[-1]
        next_letter = chr((ord(letter) - ord('A') + 1) % 26 + ord('A'))
        return f'{existing_tag[:-1]}{next_letter}'

    def modify(self) -> Any:
        """!
        @brief 执行单州国家修改
        @details 将每个州分配为独立的国家：
                 1. 遍历所有州的绘图数据
                 2. 为每个州生成唯一的国家标签
                 3. 创建国家-州关系（每个国家只拥有一个州）
                 4. 创建新的州数据和国家关系
                 5. 存储中间数据（国家-州映射、标签映射等）

        @return 修改后的州映射 Map[State]
        """
        exist_tag: set[str] = set()

        state_map: Map[State] = Map()
        country_state_map: Map[list[str]] = Map()
        country_name_map: Map[str] = Map()
        tag_map: Map[str] = Map()

        for state in self.middle['state_plot'].values():
            state: StatePlot

            tag = self.generate_country_tag(state.state_name)
            while tag in exist_tag:
                tag = self.generate_alternative_tag(tag)
            exist_tag.add(tag)

            country = CountryState(
                state_name=state.state_name,
                state_type=None,
                country_tag=tag,
                provinces=tuple(state.provinces),
            )

            state_item = State(
                state_name=state.state_name,
                country=[country],
                homeland=tuple(state.homeland),
                claim=(),
            )

            state_map[state.state_name] = state_item
            country_state_map[tag] = [state.state_name]
            country_name_map[state.state_name] = tag
            tag_map[tag] = state.state_name

        self.middle['country_state'] = country_state_map
        self.middle['country_name'] = country_name_map
        self.middle['tag'] = tag_map

        return state_map

if __name__ == '__main__':
    pass
