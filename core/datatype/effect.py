# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.datatype.effect
@brief 国家效果数据类模块
@details 定义游戏中国家效果的数据结构
"""

from dataclasses import dataclass


@dataclass
class CountryEffect(object):
    """!
    @brief 国家效果数据类
    @details 存储游戏中国家效果信息，包括国家标签、名称、效果列表等
    """
    country_tag: str                     #!< 国家标签（3字母代码）
    country_name: str                    #!< 国家名称
    effect: tuple[str, ...]              #!< 效果列表（游戏指令字符串）
    special_effect: tuple[tuple[str, str], ...]  #!< 特殊效果列表（(键, 值)元组）


if __name__ == '__main__':
    pass