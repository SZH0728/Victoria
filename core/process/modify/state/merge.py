# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.process.modify.state.merge
@brief 州合并修改器模块
@details 实现区域内的州合并功能，将多个州分配给新的国家标签
"""

from typing import Any
from random import shuffle

from core.datatype.map import Map
from core.datatype.state import State, CountryState, StatePlot
from core.process.modify.state.base import StateModifyBase


class StateModifyRegionMerge(StateModifyBase):
    """!
    @brief 区域州合并修改器
    @details 将同一区域内的一个或多个州分配到一个国家名下，支持自定义最大合并数量
             处理步骤：
             1. 根据区域划分州列表
             2. 按最大合并百分比计算每组州数量
             3. 随机分组州
             4. 为每组生成唯一的国家标签
             5. 创建新的州和国家关系
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

    @staticmethod
    def random_group_states(state_list: tuple[str, ...], max_merge: int) -> list[list[str]]:
        """!
        @brief 随机分组州列表
        @details 将州列表随机打乱后按最大合并数量分组。如果max_merge <= 0，则所有州分为一组。

        @param state_list 州名称元组
        @param max_merge 每组最大州数量，0表示无限制

        @return 分组后的州列表，每个元素是一个州名称列表
        """
        if not state_list:
            return []

        # 转换为列表并随机打乱
        shuffled_states = list(state_list)
        shuffle(shuffled_states)

        groups = []

        if max_merge <= 0:
            # 无限制，所有州分为一组
            groups.append(shuffled_states)
        else:
            # 按最大合并数分组
            current_group = []
            for state in shuffled_states:
                current_group.append(state)
                # 当前组达到最大数量时，创建新组
                if len(current_group) >= max_merge:
                    groups.append(current_group)
                    current_group = []

            # 处理剩余的州
            if current_group:
                groups.append(current_group)

        return groups
    
    def modify(self) -> Any:
        """!
        @brief 执行州合并修改
        @details 遍历所有区域，将每个区域内的州按最大合并数分组，每组分配一个新的国家标签
                 具体步骤：
                 1. 从中间参数获取最大合并百分比
                 2. 遍历所有区域（排除水域）
                 3. 计算每个区域的最大合并数量
                 4. 随机分组州
                 5. 为每组生成唯一国家标签
                 6. 创建新的州和国家关系
                 7. 存储中间数据（国家-州映射、标签映射等）

        @return 修改后的州映射 Map[State]
        """
        # 获取最大合并数配置，默认为0（无限制）
        max_merge_percent = self.middle.get('max_merge_percent', 0)

        exist_tag: set[str] = set()

        state_map: Map[State] = Map()
        country_state_map: Map[list[str]] = Map()
        country_name_map: Map[str] = Map()
        tag_map: Map[str] = Map()

        group_states: list[list[str]] = []

        for continent_name, continent_item in self.origin.region.items():
            if continent_name == 'water':
                continue

            for region_item in continent_item:
                state_list: tuple[str, ...] = region_item.states

                max_merge: int = len(state_list) * max_merge_percent // 100

                group_state = self.random_group_states(state_list, max_merge)
                group_states.extend(group_state)

        for group in group_states:
            state_list: list[StatePlot] = []
            for state_name in group:
                state: StatePlot = self.middle['state_plot'][state_name]
                state_list.append(state)

            tag = self.generate_country_tag(state_list[0].state_name)
            while tag in exist_tag:
                tag = self.generate_alternative_tag(tag)
            exist_tag.add(tag)

            for state in state_list:
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

            country_state_map[tag] = group
            tag_map[tag] = state_list[0].state_name
            country_name_map[state_list[0].state_name] = tag

        self.middle['country_state'] = country_state_map
        self.middle['country_name'] = country_name_map
        self.middle['tag'] = tag_map

        return state_map


if __name__ == '__main__':
    pass