# -*- coding:utf-8 -*-
# AUTHOR: Sun

from abc import ABC, abstractmethod
from logging import getLogger

from pyradox import Tree

from core.file import FileManager
from core.datatype import Map, State
from core.transform.combine import KeyCombinationMixin

logger = getLogger(__name__)


class StateTransformBase(KeyCombinationMixin, ABC):
    """!
    @brief 州转换抽象基类
    @details 提供州数据转换的通用框架，子类需实现具体的转换逻辑
    """


    @abstractmethod
    def transform(self, state: State) -> Tree:
        """!
        @brief 转换州对象为pyradox树
        @param state 州对象
        @return 转换后的树
        """
        pass

    def main(self, manager: FileManager, group: str, filename: str, state_map: Map[State]):
        """!
        @brief 主转换流程，将州映射写入文件
        @details 构建STATES顶层结构，转换每个州并写入文件
        @param manager 文件管理器实例
        @param group 文件组名称
        @param filename 输出文件名
        @param state_map 州映射
        """
        tree = Tree()

        tree['STATES'] = Tree()

        for i in state_map.values():
            state_name = self.combine_state_key(i.state_name)
            tree['STATES'][state_name] = self.transform(i)

        manager.write_file(group, filename, str(tree))


if __name__ == '__main__':
    pass
