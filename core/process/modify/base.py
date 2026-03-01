# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.process.modify.base
@brief 修改器抽象基类模块
@details 定义数据修改器的抽象接口和基础实现
"""

from typing import Any
from abc import ABC, abstractmethod
from enum import Enum

from core.datatype import DataCombination


class DataType(Enum):
    """!
    @brief 数据类型枚举
    @details 定义修改器可以处理的数据类型
    """
    building = 0    #!< 建筑数据
    definition = 1  #!< 国家定义数据
    effect = 2      #!< 国家效果数据
    population = 3  #!< 人口数据
    state = 4       #!< 州数据
    tag = 5         #!< 标签数据


class ModifyBase(ABC):
    """!
    @brief 修改器抽象基类
    @details 所有数据修改器的基类，提供原始数据、中间数据和目标数据访问
    """
    def __init__(self, origin: DataCombination, middle: dict[str, Any], target: DataCombination):
        """!
        @brief 初始化修改器
        @param origin 原始数据容器，包含分析阶段解析的游戏数据
        @param middle 中间数据字典，包含收集器生成的数据
        @param target 目标数据容器，用于存储修改后的数据
        """
        self.origin = origin      #!< 原始数据容器
        self.middle = middle      #!< 中间数据字典
        self.target = target      #!< 目标数据容器

    @abstractmethod
    def modify(self) -> Any:
        """!
        @brief 执行数据修改
        @details 抽象方法，子类必须实现具体的修改逻辑
        @return 修改后的数据（类型由具体实现决定）
        """
        pass

    @abstractmethod
    def abstract_modify(self) -> tuple[DataType, Any]:
        """!
        @brief 抽象修改方法
        @details 抽象方法，子类必须实现具体的修改逻辑并返回数据类型和修改后的数据
        @return 元组（数据类型枚举值, 修改后的数据）
        """
        pass

    def main(self):
        """!
        @brief 主执行方法
        @details 调用abstract_modify()方法获取数据类型和修改后的数据，然后将数据存储到target容器的对应字段中
        """
        data_type, data = self.abstract_modify()

        if data_type == DataType.building:
            self.target.building = data
        elif data_type == DataType.definition:
            self.target.definition = data
        elif data_type == DataType.effect:
            self.target.effect = data
        elif data_type == DataType.population:
            self.target.population = data
        elif data_type == DataType.state:
            self.target.state = data
        elif data_type == DataType.tag:
            self.target.tag = data


if __name__ == '__main__':
    pass
