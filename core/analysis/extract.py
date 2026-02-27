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
    @details 提供类方法，通过替换可配置的前缀/后缀从键中提取名称。
             子类应设置类属性以匹配其特定的提取模式。
    """

    # Class attributes to be overridden by subclasses
    STATE_KEY_PREFIX: ClassVar[str] = ''
    COUNTRY_TAG_KEY_PREFIX: ClassVar[str] = ''
    COUNTRY_TAG_VALUE_PREFIX: ClassVar[str] = ''
    CULTURE_KEY_PREFIX: ClassVar[str] = ''
    REGION_KEY_PREFIX: ClassVar[str] = ''
    CONTINENT_FILE_SUFFIXES: ClassVar[tuple[str, ...]] = ('.txt', '_strategic_regions')

    @classmethod
    def get_state_name_by_key(cls, name: str) -> str:
        """!
        @brief 从键中提取州名称，通过移除前缀
        @param name 原始键（例如 's:STATE_CALIFORNIA'）
        @return 小写的州名称
        """
        result = name.replace(cls.STATE_KEY_PREFIX, '')
        return result.lower()

    @classmethod
    def get_country_tag_by_key(cls, tag: str) -> str:
        """!
        @brief 从键中提取国家标签，通过移除前缀
        @param tag 原始键（例如 'region_state:USA'）
        @return 大写的国家标签
        """
        result = tag.replace(cls.COUNTRY_TAG_KEY_PREFIX, '')
        return result.upper()

    @classmethod
    def get_country_tag_by_value(cls, tag: str) -> str:
        """!
        @brief 从值中提取国家标签，通过移除前缀
        @param tag 原始值（例如 'c:USA'）
        @return 大写的国家标签
        """
        result = tag.replace(cls.COUNTRY_TAG_VALUE_PREFIX, '')
        return result.upper()

    @classmethod
    def get_culture_name_by_key(cls, name: str) -> str:
        """!
        @brief 从键中提取文化名称，通过移除前缀
        @param name 原始键（例如 'cu:english'）
        @return 小写的文化名称
        """
        result = name.replace(cls.CULTURE_KEY_PREFIX, '')
        return result.lower()

    @classmethod
    def get_region_name_by_key(cls, name: str) -> str:
        """!
        @brief 从键中提取区域名称，通过移除前缀
        @param name 原始键（例如 'region_europe'）
        @return 小写的区域名称
        """
        result = name.replace(cls.REGION_KEY_PREFIX, '')
        return result.lower()

    @classmethod
    def get_continent_name_by_file_name(cls, name: str | Path) -> str:
        """!
        @brief 从文件名中提取大洲名称，通过移除后缀
        @param name 文件名或路径对象
        @return 小写的大洲名称
        """
        if isinstance(name, Path):
            name = name.name

        result = name
        for suffix in cls.CONTINENT_FILE_SUFFIXES:
            result = result.replace(suffix, '')

        return result.lower()


if __name__ == '__main__':
    pass