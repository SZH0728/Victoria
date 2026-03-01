# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.process.collect.base
@brief 收集器抽象基类模块
@details 定义数据收集器的抽象接口和基础实现
"""

from typing import Any
from abc import ABC, abstractmethod

from core.datatype import DataCombination


class CollectBase(ABC):
    """!
    @brief 收集器抽象基类
    @details 所有数据收集器的基类，提供原始数据访问和中间数据存储功能
    """
    def __init__(self, origin: DataCombination, middle: dict[str, Any]):
        """!
        @brief 初始化收集器
        @param origin 原始数据容器，包含分析阶段解析的游戏数据
        @param middle 中间数据字典，用于存储收集器生成的数据
        """
        self.origin = origin      #!< 原始数据容器
        self.middle = middle      #!< 中间数据字典

    @abstractmethod
    def collect(self) -> list[tuple[str, Any]]:
        """!
        @brief 执行数据收集
        @details 抽象方法，子类必须实现具体的收集逻辑

        @return 收集结果列表，每个元素为(键名, 值)的元组
        @note 收集的结果将被存储到middle字典中
        """
        pass

    def main(self):
        """!
        @brief 主执行方法
        @details 调用collect()方法获取结果，并将结果存储到middle字典中
        """
        result: list[tuple[str, Any]] = self.collect()

        for key, value in result:
            self.middle[key] = value


if __name__ == '__main__':
    pass
