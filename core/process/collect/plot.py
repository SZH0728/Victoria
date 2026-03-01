# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.process.collect.plot
@brief 州绘图数据收集器模块
@details 收集州绘图所需的数据，包括省份、文化等信息
"""

from typing import Any

from core.datatype.map import Map
from core.datatype.state import StatePlot
from core.process.collect.base import CollectBase

class StatePlotCollect(CollectBase):
    """!
    @brief 州绘图数据收集器
    @details 从原始州数据中提取绘图所需信息，包括省份列表、本土文化和宣称文化
    """
    def collect(self) -> list[tuple[str, Any]]:
        """!
        @brief 收集州绘图数据
        @details 处理步骤：
                 1. 从水域区域中提取水域州列表
                 2. 遍历所有州，排除水域州
                 3. 提取每个州的省份列表（合并所有国家的省份）
                 4. 创建StatePlot对象并存储到映射中

        @return 包含('state_plot', StatePlot映射)的列表
        """
        water: set[str] = set()

        for state in self.origin.region.water:
            for name in state.states:
                water.add(name)

        state_map: Map[StatePlot] = Map()
        for state in self.origin.state.values():
            if state.state_name in water:
                continue

            provinces: list[str] = []

            for country in state.country:
                provinces.extend(country.provinces)

            state_map[state.state_name] = StatePlot(
                state_name=state.state_name,
                provinces=provinces,
                homeland=list(state.homeland),
                claim=list(state.claim),
            )

        return [('state_plot', state_map)]

if __name__ == '__main__':
    pass
