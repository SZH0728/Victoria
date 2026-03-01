# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@file combine.py
@brief 键组合混入类，用于转换模块
@details 提供可重用的方法，通过添加前缀/后缀将名称转换为键。
         每个子类可直接使用这些方法，无需重复实现。
"""

from typing import ClassVar
from pathlib import Path


class KeyCombinationMixin:
    """!
    @brief 键组合混入类
    @details 提供类方法，通过添加硬编码的前缀/后缀将名称转换为键。
             支持多种游戏数据格式（州、国家、文化、区域等）。
    """

    @classmethod
    def combine_state_key(cls, name: str) -> str:
        """!
        @brief 将州名称转换为游戏数据键
        @details 格式为 s:STATE_STATENAME
        @param name 州名称（任意大小写）
        @return 转换后的键（大写州名）
        """
        return f's:STATE_{name.upper()}'

    @classmethod
    def combine_country_key_for_region_state(cls, tag: str) -> str:
        """!
        @brief 将国家标签转换为region_state格式的键
        @details 格式为 region_state:TAG（用于建筑和人口数据）
        @param tag 国家标签（任意大小写）
        @return 转换后的键（大写标签）
        """
        return f'region_state:{tag.upper()}'

    @classmethod
    def combine_country_key_for_c(cls, tag: str) -> str:
        """!
        @brief 将国家标签转换为c格式的键
        @details 格式为 c:TAG（用于州数据）
        @param tag 国家标签（任意大小写）
        @return 转换后的键（大写标签）
        """
        return f'c:{tag.upper()}'

    @classmethod
    def combine_country_value(cls, tag: str) -> str:
        """!
        @brief 将国家标签转换为c格式的值
        @details 格式为 c:TAG（用于建筑数据中的值）
        @param tag 国家标签（任意大小写）
        @return 转换后的值（大写标签）
        """
        return f'c:{tag.upper()}'

    @classmethod
    def combine_culture_key(cls, name: str) -> str:
        """!
        @brief 将文化名称转换为游戏数据键
        @details 格式为 cu:CULTURENAME
        @param name 文化名称（任意大小写）
        @return 转换后的键（小写文化名）
        """
        return f'cu:{name.lower()}'

    @classmethod
    def combine_region_key(cls, name: str) -> str:
        """!
        @brief 将区域名称转换为游戏数据键
        @details 格式为 region_REGIONNAME
        @param name 区域名称（任意大小写）
        @return 转换后的键（小写区域名）
        """
        return f'region_{name.lower()}'

    @classmethod
    def combine_continent_filename(cls, name: str | Path) -> str:
        """!
        @brief 将大洲名称转换为战略区域文件名
        @details 添加后缀 _strategic_regions.txt
        @param name 大洲名称或路径对象
        @return 完整的文件名（小写）
        """
        result = name.name if isinstance(name, Path) else name
        return f"{result.lower()}_strategic_regions.txt"


if __name__ == '__main__':
    pass