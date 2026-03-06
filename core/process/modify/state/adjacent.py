# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.process.modify.state.adjacent
@brief 州相邻合并修改器模块
@details 实现区域内相邻州的合并功能，将多个相邻州分配给新的国家标签
"""

from typing import Any
from random import choice

from core.datatype.map import Map
from core.datatype.state import State, CountryState, StateInRegion
from core.process.modify.state.base import StateModifyBase


class StateModifyRegionAdjacent(StateModifyBase):
    """!
    @brief 区域州相邻合并修改器
    @details 将同一区域内相邻的一个或多个州分配到一个国家名下，支持自定义最大合并数量
             处理步骤：
             1. 根据区域划分州列表
             2. 按最大合并百分比计算每组州数量
             3. 基于相邻关系分组州
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
    def are_states_adjacent(state1: StateInRegion, state2: StateInRegion) -> bool:
        """!
        @brief 判断两个州是否相邻
        @details 两个州相邻的条件：存在至少一对相邻的省份（一个来自state1，一个来自state2）。

        @param state1 第一个州数据
        @param state2 第二个州数据
        @return 如果相邻返回True，否则返回False
        """
        return abs(state1.state_id - state2.state_id) <= 1

    def build_adjacency_graph(self, states: list[StateInRegion]) -> dict[str, list[str]]:
        """!
        @brief 构建州相邻关系图
        @details 返回邻接表，键为州名称，值为相邻州名称列表。

        @param states 州数据列表
        @return 邻接表字典
        """
        graph = {state.state_name: list() for state in states}
        n = len(states)
        for i in range(n):
            for j in range(i + 1, n):
                if self.are_states_adjacent(states[i], states[j]):
                    graph[states[i].state_name].append(states[j].state_name)
                    graph[states[j].state_name].append(states[i].state_name)
        return graph

    def group_adjacent_states(self, states: list[StateInRegion], max_merge: int) -> list[list[str]]:
        """!
        @brief 将相邻州分组
        @details 基于相邻关系将州分组，每组最多包含max_merge个州，且组内州相互连通。
                 使用BFS遍历连通分量，每个连通分量按最大合并数分割。

        @param states 州数据列表
        @param max_merge 每组最大州数量，0表示无限制
        @return 分组后的州列表，每个元素是一个州名称列表
        """
        if not states:
            return []

        # 构建邻接图
        graph = self.build_adjacency_graph(states)
        state_names = [state.state_name for state in states]
        visited = set()
        groups = []

        for state_name in state_names:
            if state_name in visited:
                continue

            # BFS收集连通分量
            component = []
            queue = [state_name]
            visited.add(state_name)

            while queue:
                node = queue.pop(0)
                component.append(node)
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            # 如果连通分量为空（孤立节点），单独成组
            if not component:
                continue

            # 如果max_merge <= 0，整个连通分量作为一组
            if max_merge <= 0:
                groups.append(component)
                continue

            # 将连通分量按max_merge分割
            # 为了保持连通性，我们使用简单方法：从分量中随机选择起始点，进行BFS直到达到max_merge
            # 然后从剩余节点中继续，直到分量被分割完
            remaining = component[:]
            while remaining:
                # 随机选择一个起始节点
                start = choice(remaining)
                # BFS收集最多max_merge个节点
                subgroup = []
                sub_visited = set()
                sub_queue = [start]
                sub_visited.add(start)

                while sub_queue and len(subgroup) < max_merge:
                    node = sub_queue.pop(0)
                    subgroup.append(node)
                    # 添加未访问的相邻节点
                    for neighbor in graph[node]:
                        if neighbor in remaining and neighbor not in sub_visited and len(subgroup) < max_merge:
                            sub_visited.add(neighbor)
                            sub_queue.append(neighbor)

                # 移除已分配的节点
                for node in subgroup:
                    if node in remaining:
                        remaining.remove(node)

                groups.append(subgroup)

        return groups

    def modify(self) -> Any:
        """!
        @brief 执行州相邻合并修改
        @details 遍历所有区域，将每个区域内的相邻州按最大合并数分组，每组分配一个新的国家标签
                 具体步骤：
                 1. 从中间参数获取最大合并百分比
                 2. 获取state_in_region数据（由StateInRegionOrder收集器生成）
                 3. 遍历所有区域（排除水域）
                 4. 计算每个区域的最大合并数量
                 5. 相邻分组州
                 6. 为每组生成唯一国家标签
                 7. 创建新的州和国家关系
                 8. 存储中间数据（国家-州映射、标签映射等）

        @return 修改后的州映射 Map[State]
        """
        # 获取最大合并数配置，默认为0（无限制）
        max_merge_percent = self.middle.get('max_merge_percent', 0)

        # 获取state_in_region数据
        state_in_region_map: Map[Map[StateInRegion]] = self.middle['state_in_region']

        exist_tag: set[str] = set()

        state_map: Map[State] = Map()
        country_state_map: Map[list[str]] = Map()
        country_name_map: Map[str] = Map()
        tag_map: Map[str] = Map()

        group_states: list[list[str]] = []
        # 构建州名到StateInRegion的映射，便于后续查找
        state_name_to_obj: dict[str, StateInRegion] = {}

        # 遍历所有区域
        for region_name, region_states_map in state_in_region_map.items():
            # region_states_map 是 Map[StateInRegion]
            # 转换为列表
            states_in_region = list(region_states_map.values())
            if not states_in_region:
                continue

            # 构建映射
            for state in states_in_region:
                state_name_to_obj[state.state_name] = state

            state_list: tuple[str, ...] = tuple(state.state_name for state in states_in_region)
            max_merge: int = len(state_list) * max_merge_percent // 100

            if max_merge == 0 and max_merge_percent > 0:
                max_merge = 1

            # 相邻分组
            group_state = self.group_adjacent_states(states_in_region, max_merge)
            group_states.extend(group_state)

        # 为每个分组创建新的国家标签和州数据
        for group in group_states:
            state_objs: list[StateInRegion] = []
            for state_name in group:
                state_objs.append(state_name_to_obj[state_name])

            # 生成国家标签
            tag = self.generate_country_tag(state_objs[0].state_name)
            while tag in exist_tag:
                tag = self.generate_alternative_tag(tag)
            exist_tag.add(tag)

            # 创建新的州和国家关系
            for state in state_objs:
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
                    claim=tuple(state.claim),
                )

                state_map[state.state_name] = state_item

            country_state_map[tag] = group
            tag_map[tag] = state_objs[0].state_name
            country_name_map[state_objs[0].state_name] = tag

        # 存储中间数据
        self.middle['country_state'] = country_state_map
        self.middle['country_name'] = country_name_map
        self.middle['tag'] = tag_map

        return state_map


if __name__ == '__main__':
    pass
