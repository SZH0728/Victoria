# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@file extract.py
@brief 键提取混入类，用于分析模块
@details 提供可重用的方法，通过替换前缀/后缀从键中提取名称。
         每个子类应设置适当的类属性以自定义提取模式。
"""

from typing import ClassVar
from pathlib import Path


class KeyExtractionMixin:
    """!
    @brief 键提取混入类
    @details 提供类方法，通过硬编码的前缀/后缀从键中提取名称。
             每种类型支持一组已知的前缀，自动匹配并移除。
    """


    @classmethod
    def extract_state_name_from_key(cls, name: str) -> str:
        """!
        @brief 从键中提取州名称，通过移除前缀
        @param name 原始键（例如 's:STATE_CALIFORNIA'）
        @return 小写的州名称
        """
        prefixes = ['s:STATE_', 'STATE_']
        result = name

        for prefix in prefixes:
            if result.startswith(prefix):
                result = result.replace(prefix, '', 1)
                break

        return result.lower()

    @classmethod
    def extract_country_tag_from_key(cls, tag: str) -> str:
        """!
        @brief 从键中提取国家标签，通过移除前缀
        @param tag 原始键（例如 'region_state:USA'）
        @return 大写的国家标签
        """
        prefixes = ['c:', 'region_state:']
        result = tag

        for prefix in prefixes:
            if result.startswith(prefix):
                result = result.replace(prefix, '', 1)
                break

        return result.upper()

    @classmethod
    def extract_country_tag_from_value(cls, tag: str) -> str:
        """!
        @brief 从值中提取国家标签，通过移除前缀
        @param tag 原始值（例如 'c:USA'）
        @return 大写的国家标签
        """
        prefix = 'c:'
        result = tag

        if result.startswith(prefix):
            result = result.replace(prefix, '', 1)

        return result.upper()

    @classmethod
    def extract_culture_name_from_key(cls, name: str) -> str:
        """!
        @brief 从键中提取文化名称，通过移除前缀
        @param name 原始键（例如 'cu:english'）
        @return 小写的文化名称
        """
        prefix = 'cu:'
        result = name

        if result.startswith(prefix):
            result = result.replace(prefix, '', 1)

        return result.lower()

    @classmethod
    def extract_region_name_from_key(cls, name: str) -> str:
        """!
        @brief 从键中提取区域名称，通过移除前缀
        @param name 原始键（例如 'region_europe'）
        @return 小写的区域名称
        """
        prefix = 'region_'
        result = name

        if result.startswith(prefix):
            result = result.replace(prefix, '', 1)

        return result.lower()

    @classmethod
    def extract_continent_name_from_filename(cls, name: str | Path) -> str:
        """!
        @brief 从文件名中提取大洲名称，通过移除后缀
        @param name 文件名或路径对象
        @return 小写的大洲名称
        """
        result = name.name if isinstance(name, Path) else name
        suffixes = ('.txt', '_strategic_regions')

        for suffix in suffixes:
            result = result.replace(suffix, '')

        return result.lower()


if __name__ == '__main__':
    pass