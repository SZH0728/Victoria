# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@brief 前缀转换基类模块
@details 提供不同类型游戏数据键的前缀转换功能，支持从原始字符串到游戏数据键格式以及反向转换
"""

from abc import ABC, abstractmethod


class BasePrefix(ABC):
    """
    @brief 前缀转换基类
    @details 抽象基类，定义了前缀转换的基本接口
    """

    def __init__(self, str_with_prefix: str = None, str_without_prefix: str = None):
        """
        @brief 初始化前缀转换器
        @param str_with_prefix 带前缀的字符串（可选）
        @param str_without_prefix 不带前缀的原始字符串（可选）
        @throws ValueError 当同时提供两个参数或都不提供时抛出异常
        """
        if str_with_prefix and str_without_prefix:
            raise ValueError("Cannot provide both str_with_prefix and str_without_prefix")

        if not str_with_prefix and not str_without_prefix:
            raise ValueError("Must provide either str_with_prefix or str_without_prefix")

        self.original_string = str_without_prefix

        if str_with_prefix:
            self.original_string = self.prefix_to_origin(str_with_prefix)

    def __hash__(self):
        """@brief 计算哈希值"""
        return hash(self.original_string)

    def __eq__(self, other):
        """
        @brief 比较相等性
        @param other 要比较的对象
        @return 如果相等返回True，否则返回False
        """
        if isinstance(other, self.__class__):
            return self.original_string == other.original_string

        if isinstance(other, str):
            return self.original_string == other

        return False

    def __repr__(self):
        """@brief 返回对象的字符串表示"""
        return f'{self.__class__.__name__}({self.prefix_string}/{self.original_string})'

    @abstractmethod
    def origin_to_prefix(self, string: str) -> str:
        """
        @brief 从原始字符串转换为带前缀的格式
        @param string 原始字符串
        @return 带前缀的字符串
        """
        pass

    @abstractmethod
    def prefix_to_origin(self, string: str) -> str:
        """
        @brief 从带前缀的字符串转换为原始格式
        @param string 带前缀的字符串
        @return 原始字符串
        """
        pass

    @property
    def prefix_string(self) -> str:
        """@brief 获取带前缀的字符串"""
        return self.origin_to_prefix(self.original_string)


class StateNamePrefix(BasePrefix):
    """
    @brief 州名前缀转换器
    @details 处理州名相关的前缀转换，格式为 s:STATE_<NAME>
    """

    def origin_to_prefix(self, string: str) -> str:
        """
        @brief 从原始州名转换为带前缀格式
        @param string 原始州名
        @return 格式为 s:STATE_<NAME> 的字符串
        """
        return f's:STATE_{self.original_string.upper()}'

    def prefix_to_origin(self, string: str) -> str:
        """
        @brief 从带前缀的州名转换为原始格式
        @param string 带前缀的州名字符串
        @return 原始州名（小写）
        """
        return string.replace('s:STATE_', '').lower()


class StateNamePurePrefix(BasePrefix):
    """
    @brief 纯州名前缀转换器
    @details 处理纯州名前缀转换，格式为 STATE_<NAME>
    """

    def origin_to_prefix(self, string: str) -> str:
        """
        @brief 从原始州名转换为带前缀格式
        @param string 原始州名
        @return 格式为 STATE_<NAME> 的字符串
        """
        return f'STATE_{self.original_string.upper()}'

    def prefix_to_origin(self, string: str) -> str:
        """
        @brief 从带前缀的州名转换为原始格式
        @param string 带前缀的州名字符串
        @return 原始州名（小写）
        """
        return string.replace('STATE_', '').lower()


class CountryTagPrefix(BasePrefix):
    """
    @brief 国家标签前缀转换器
    @details 处理国家标签相关的前缀转换，格式为 c:<TAG>
    """

    def origin_to_prefix(self, string: str) -> str:
        """
        @brief 从原始国家标签转换为带前缀格式
        @param string 原始国家标签
        @return 格式为 c:<TAG> 的字符串
        """
        return f'c:{self.original_string.upper()}'

    def prefix_to_origin(self, string: str) -> str:
        """
        @brief 从带前缀的国家标签转换为原始格式
        @param string 带前缀的国家标签字符串
        @return 原始国家标签（小写）
        """
        return string.replace('c:', '').lower()


class CultureNamePrefix(BasePrefix):
    """
    @brief 文化名前缀转换器
    @details 处理文化名相关的前缀转换，格式为 cu:<NAME>
    """

    def origin_to_prefix(self, string: str) -> str:
        """
        @brief 从原始文化名转换为带前缀格式
        @param string 原始文化名
        @return 格式为 cu:<NAME> 的字符串
        """
        return f'cu:{self.original_string.upper()}'

    def prefix_to_origin(self, string: str) -> str:
        """
        @brief 从带前缀的文化名转换为原始格式
        @param string 带前缀的文化名字符串
        @return 原始文化名（小写）
        """
        return string.replace('cu:', '').lower()


class RegionNamePrefix(BasePrefix):
    """
    @brief 区域名前缀转换器
    @details 处理区域名相关的前缀转换，格式为 region:<NAME>
    """

    def origin_to_prefix(self, string: str) -> str:
        """
        @brief 从原始区域名转换为带前缀格式
        @param string 原始区域名
        @return 格式为 region:<NAME> 的字符串
        """
        return f'region_{self.original_string.lower()}'

    def prefix_to_origin(self, string: str) -> str:
        """
        @brief 从带前缀的区域名转换为原始格式
        @param string 带前缀的区域名字符串
        @return 原始区域名（小写）
        """
        return string.replace('region_', '').lower()


class RegionStatePrefix(BasePrefix):
    """
    @brief 区域-州前缀转换器
    @details 处理区域-州相关的前缀转换，格式为 region_state:<NAME>
    """

    def origin_to_prefix(self, string: str) -> str:
        """
        @brief 从原始区域-州名转换为带前缀格式
        @param string 原始区域-州名
        @return 格式为 region_state:<NAME> 的字符串
        """
        return f'region_state:{self.original_string.upper()}'

    def prefix_to_origin(self, string: str) -> str:
        """
        @brief 从带前缀的区域-州名转换为原始格式
        @param string 带前缀的区域-州名字符串
        @return 原始区域-州名（小写）
        """
        return string.replace('region_state:', '').lower()


if __name__ == '__main__':
    pass
