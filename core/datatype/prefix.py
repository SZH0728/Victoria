# -*- coding:utf-8 -*-
# AUTHOR: Sun

from abc import ABC, abstractmethod


class BasePrefix(ABC):
    """
    @brief 前缀抽象基类
    @details 提供游戏数据键的前缀转换功能，支持带前缀和不带前缀的字符串互相转换
    """
    def __init__(self, str_with_prefix: str | None = None, str_without_prefix: str | None = None):
        """
        @brief 初始化前缀对象
        @param str_with_prefix 带前缀的字符串
        @param str_without_prefix 不带前缀的字符串
        @note 只能提供其中一个参数，不能同时提供两个
        """
        if str_with_prefix is not None and str_without_prefix is not None:
            raise ValueError("Cannot provide both str_with_prefix and str_without_prefix")

        if str_with_prefix is None and str_without_prefix is None:
            raise ValueError("Must provide either str_with_prefix or str_without_prefix")

        self.original_string = str_without_prefix  # 原始字符串（不带前缀）

        if str_with_prefix:
            self.original_string = self.prefix_to_origin(str_with_prefix)

    def __hash__(self):
        """
        @brief 哈希方法，基于原始字符串生成哈希值
        """
        return hash(self.original_string)

    def __eq__(self, other):
        """
        @brief 相等比较方法，支持与同类对象或字符串比较
        """
        if isinstance(other, self.__class__):
            return self.original_string == other.original_string

        if isinstance(other, str):
            return self.original_string == other

        return False

    def __repr__(self):
        """
        @brief 字符串表示方法，显示类名、前缀字符串和原始字符串
        """
        return f'{self.__class__.__name__}({self.prefix_string}/{self.original_string})'

    def __str__(self):
        """
        @brief 字符串转换方法，返回带前缀的字符串
        """
        return self.prefix_string

    @abstractmethod
    def origin_to_prefix(self, string: str) -> str:
        """
        @brief 将原始字符串转换为带前缀的字符串（抽象方法）
        @param string 原始字符串（不带前缀）
        @return 带前缀的字符串
        """
        pass

    @abstractmethod
    def prefix_to_origin(self, string: str) -> str:
        """
        @brief 将带前缀的字符串转换为原始字符串（抽象方法）
        @param string 带前缀的字符串
        @return 原始字符串（不带前缀）
        """
        pass

    @property
    def prefix_string(self) -> str:
        """
        @brief 前缀字符串属性，获取带前缀的字符串表示
        """
        return self.origin_to_prefix(self.original_string)


class StateNamePrefix(BasePrefix):
    """
    @brief 州名前缀类
    @details 处理带 "s:STATE_" 前缀的州名转换，如 "s:STATE_CALIFORNIA"
    """
    def origin_to_prefix(self, string: str) -> str:
        """
        @brief 将州名转换为带 "s:STATE_" 前缀的字符串
        @param string 原始州名（小写）
        @return 带前缀的州名（大写）
        """
        return f's:STATE_{string.upper()}'

    def prefix_to_origin(self, string: str) -> str:
        """
        @brief 将带前缀的州名转换为原始州名
        @param string 带 "s:STATE_" 前缀的州名
        @return 原始州名（小写）
        """
        return string.replace('s:STATE_', '').lower()


class StateNamePurePrefix(BasePrefix):
    """
    @brief 纯州名前缀类
    @details 处理带 "STATE_" 前缀的州名转换，如 "STATE_CALIFORNIA"
    """
    def origin_to_prefix(self, string: str) -> str:
        """
        @brief 将州名转换为带 "STATE_" 前缀的字符串
        @param string 原始州名（小写）
        @return 带前缀的州名（大写）
        """
        return f'STATE_{string.upper()}'

    def prefix_to_origin(self, string: str) -> str:
        """
        @brief 将带前缀的州名转换为原始州名
        @param string 带 "STATE_" 前缀的州名
        @return 原始州名（小写）
        """
        return string.replace('STATE_', '').lower()


class CountryTagPrefix(BasePrefix):
    """
    @brief 国家标签前缀类
    @details 处理带 "c:" 前缀的国家标签转换，如 "c:USA"
    """
    def origin_to_prefix(self, string: str) -> str:
        """
        @brief 将国家标签转换为带 "c:" 前缀的字符串
        @param string 原始国家标签（小写）
        @return 带前缀的国家标签（大写）
        """
        return f'c:{string.upper()}'

    def prefix_to_origin(self, string: str) -> str:
        """
        @brief 将带前缀的国家标签转换为原始标签
        @param string 带 "c:" 前缀的国家标签
        @return 原始国家标签（小写）
        """
        return string.replace('c:', '').lower()


class CultureNamePrefix(BasePrefix):
    """
    @brief 文化名前缀类
    @details 处理带 "cu:" 前缀的文化名转换，如 "cu:ENGLISH"
    """
    def origin_to_prefix(self, string: str) -> str:
        """
        @brief 将文化名转换为带 "cu:" 前缀的字符串
        @param string 原始文化名（小写）
        @return 带前缀的文化名（大写）
        """
        return f'cu:{string.upper()}'

    def prefix_to_origin(self, string: str) -> str:
        """
        @brief 将带前缀的文化名转换为原始文化名
        @param string 带 "cu:" 前缀的文化名
        @return 原始文化名（小写）
        """
        return string.replace('cu:', '').lower()


class RegionNamePrefix(BasePrefix):
    """
    @brief 区域名前缀类
    @details 处理带 "region_" 前缀的区域名转换，如 "region_europe"
    """
    def origin_to_prefix(self, string: str) -> str:
        """
        @brief 将区域名转换为带 "region_" 前缀的字符串
        @param string 原始区域名
        @return 带前缀的区域名（小写）
        """
        return f'region_{string.lower()}'

    def prefix_to_origin(self, string: str) -> str:
        """
        @brief 将带前缀的区域名转换为原始区域名
        @param string 带 "region_" 前缀的区域名
        @return 原始区域名（小写）
        """
        return string.replace('region_', '').lower()


class RegionStatePrefix(BasePrefix):
    """
    @brief 区域州前缀类
    @details 处理带 "region_state:" 前缀的区域州名转换，如 "region_state:USA"
    """
    def origin_to_prefix(self, string: str) -> str:
        """
        @brief 将区域州名转换为带 "region_state:" 前缀的字符串
        @param string 原始区域州名（小写）
        @return 带前缀的区域州名（大写）
        """
        return f'region_state:{string.upper()}'

    def prefix_to_origin(self, string: str) -> str:
        """
        @brief 将带前缀的区域州名转换为原始区域州名
        @param string 带 "region_state:" 前缀的区域州名
        @return 原始区域州名（小写）
        """
        return string.replace('region_state:', '').lower()


if __name__ == '__main__':
    pass