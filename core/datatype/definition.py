# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 国家定义数据模块
@details 定义了维多利亚3游戏中国家定义相关的数据结构，包括颜色、类型、文化、首都等
"""

from dataclasses import dataclass

from core.datatype.prefix import StateNamePurePrefix


@dataclass(frozen=True)
class CountryDefinition(object):
    """
    @brief 国家定义数据类
    @details 表示一个国家的基本定义信息，包括颜色、类型、文化、首都等属性
    """

    color: tuple[int, ...]              #!< 国家颜色RGB值
    """@brief 国家颜色RGB值"""

    country_type: str                   #!< 国家类型
    """@brief 国家类型"""

    tier: str                           #!< 国家等级
    """@brief 国家等级"""

    cultures: tuple[str, ...]           #!< 主要文化列表
    """@brief 主要文化列表"""

    capital: StateNamePurePrefix | None        #!< 首都省份编号
    """@brief 首都省份编号（可选）"""

    religion: str | None                #!< 主要宗教
    """@brief 主要宗教（可选）"""

    is_named_from_capital: bool | None  #!< 是否以首都命名
    """@brief 是否以首都命名（可选）"""

    valid_as_home_country_for_separatists: str | None  #!< 是否可作为分离主义者的祖国
    """@brief 是否可作为分离主义者的祖国（可选）"""

    social_hierarchy: str | None        #!< 社会阶层结构
    """@brief 社会阶层结构（可选）"""

    unit_color: dict[str, list[int]]    #!< 单位颜色映射
    """@brief 单位颜色映射"""

    def __post_init__(self):
        """@brief 初始化后处理，确保color和cultures为元组类型"""
        if isinstance(self.color, list):
            object.__setattr__(self, 'color', tuple(self.color))
        if isinstance(self.cultures, list):
            object.__setattr__(self, 'cultures', tuple(self.cultures))


if __name__ == '__main__':
    pass