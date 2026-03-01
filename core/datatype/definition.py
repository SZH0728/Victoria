# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.datatype.definition
@brief 国家定义数据类模块
@details 定义游戏中国家定义的基本信息数据结构
"""

from dataclasses import dataclass


@dataclass
class CountryDefinition(object):
    """!
    @brief 国家定义数据类
    @details 存储游戏中国家定义的基本信息，包括标签、颜色、类型、文化、首都等
    """
    country_tag: str                     #!< 国家标签（3字母代码，如"USA"）
    color: tuple[int, ...]              #!< 国家颜色RGB值
    country_type: str                   #!< 国家类型（"recognized"、"unrecognized"等）
    tier: str                           #!< 国家等级
    culture: tuple[str, ...]            #!< 主要文化列表
    capital: str                        #!< 首都省份编号

    religion: str | None                #!< 主要宗教（可选）
    is_named_from_capital: bool | None  #!< 是否以首都命名（可选）
    valid_as_home_country_for_separatists: str | None  #!< 是否可作为分离主义者的祖国（可选）
    social_hierarchy: str | None        #!< 社会阶层结构（可选）
    unit_color: dict[str, tuple[int, ...]] | None  #!< 单位颜色映射（可选）


if __name__ == '__main__':
    pass