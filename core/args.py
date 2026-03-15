# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.args
@brief 参数管理器模块
@details 提供分组参数管理、权限控制、键冲突处理和只读访问功能
"""

from typing import Any, Iterator
from logging import getLogger

logger = getLogger(__name__)

KEYS_KEY = '__keys__'  # 保留键名，用于存储参数键值对的字典
MAX_GROUP_DEPTH = 100   # 最大组深度限制，防止无限嵌套


class PathMixin(object):
    """!
    @brief 路径处理工具类
    @details 提供组路径的规范化、验证和解析功能。供ArgsManager和GroupReader使用。
    """
    @staticmethod
    def normalize_group_path(group: str) -> list[str]:
        """!
        @brief 规范化组路径为令牌列表
        @details 将组路径字符串转换为令牌列表，跳过空段，处理根组表示。
                 禁止父组引用语法（如".."）和连续点号（如"..."）。
        @param group 组路径字符串
        @return 规范化后的令牌列表
        @raises ValueError 如果路径包含父组引用或连续点号
        """
        # 空字符串和单个点都视为根组
        if group == '' or group == '.':
            return []

        # 禁止父组引用语法 ".." 和连续点号
        if group == '..' or '..' in group:
            raise ValueError(f"Group path contains parent reference '..' or consecutive dots: '{group}'")

        tokens: list[str] = []
        for token in group.split('.'):
            if not token:
                continue
            tokens.append(token)

        return tokens

    @staticmethod
    def validate_group_token(token: str) -> None:
        """!
        @brief 验证组令牌有效性
        @details 组令牌必须仅包含字母数字字符（a-z, A-Z, 0-9）。
                 这是当前设计限制，如需支持其他字符（如下划线、连字符），需修改此方法。
        @param token 待验证的令牌
        @raises ValueError 如果令牌无效
        """
        if not token:
            return  # 空令牌已在normalize_group_path中跳过

        if not token.isalnum():
            raise ValueError(
                f"Group token must contain only alphanumeric characters: '{token}'"
            )

    @staticmethod
    def validate_group_depth(tokens: list[str]) -> None:
        """!
        @brief 验证组路径深度
        @details 组路径不能超过最大深度限制（硬编码为 MAX_GROUP_DEPTH = 100）。
                 此限制为防止无限递归和过深嵌套。
        @param tokens 组路径令牌列表
        @raises ValueError 如果路径深度超过限制
        """
        if len(tokens) > MAX_GROUP_DEPTH:
            raise ValueError(
                f"Group path too deep: {len(tokens)} > {MAX_GROUP_DEPTH}"
            )


    def validate_group_path(self, group: str) -> list[str]:
        """!
        @brief 验证并规范化组路径
        @details 完整验证组路径，包括令牌格式和深度限制。
                 验证步骤：1) 规范化路径；2) 验证令牌格式；3) 验证深度限制。
        @param group 组路径字符串
        @return 规范化后的令牌列表
        @raises ValueError 如果路径无效（包含非法字符、父组引用或深度超限）
        """
        tokens = self.normalize_group_path(group)

        for token in tokens:
            self.validate_group_token(token)

        self.validate_group_depth(tokens)
        return tokens


class GroupReader(PathMixin):
    """!
    @brief 组阅读器类
    @details 提供只读访问权限范围内的参数。
    """
    def __init__(self, data: dict[str, Any], group: str) -> None:
        """!
        @brief 初始化组阅读器
        @param data 参数数据字典
        @param group 当前组路径（规范化）
        """
        self._data = data
        self._group = group

    @property
    def group(self) -> str:
        """!
        @brief 获取当前组路径
        @return 当前组路径字符串
        """
        return self._group

    def resolve_group_dict(self, group_path: str) -> dict[str, Any]:
        """!
        @brief 解析组路径到对应的字典
        @param group_path 组路径字符串
        @return 组对应的字典
        @raises KeyError 如果组路径不存在
        """
        if group_path == '':
            return self._data

        tokens = self.normalize_group_path(group_path)

        group_dict: dict[str, Any] = self._data
        for index, token in enumerate(tokens):
            if token not in group_dict:
                current_path = '.'.join(tokens[:index])
                current_path = current_path if current_path else 'root'
                raise KeyError(f"Group path segment '{token}' not found. Full path: '{group_path}', current: '{current_path}'")

            group_dict = group_dict[token]

        return group_dict

    def get(self, key: str, child: str | None = None, default: Any = None) -> Any:
        """!
        @brief 获取参数值
        @details 如果键不存在，返回默认值而不抛出异常。
                 注意：child参数使用lstrip('.')移除前导点号，这意味着".sub"和"sub"被视为相同。
                     父组引用语法（如"..sub"）已被normalize_group_path禁止。
        @param key 参数键名
        @param child 子组路径，None表示在当前组查找
        @param default 默认值，当键或组不存在时返回
        @return 参数值或默认值
        @raises ValueError 如果路径无效（包含非法字符、父组引用或深度超限）
        """
        group_path = self._group
        if child is not None:
            child_stripped = child.lstrip('.')
            group_path = '.'.join((group_path, child_stripped))

        try:
            group_dict = self.resolve_group_dict(group_path)
        except KeyError:
            return default

        if KEYS_KEY not in group_dict or not group_dict[KEYS_KEY]:
            return default

        if key not in group_dict[KEYS_KEY]:
            return default

        return group_dict[KEYS_KEY][key]

    def __getitem__(self, path: str) -> Any:
        """!
        @brief 通过[]操作符访问参数值
        @details 与get()不同，此方法在键不存在时抛出KeyError。
                 路径分割时过滤空令牌，因此".key"和"key."都被视为"key"。
                 父组引用语法已被normalize_group_path禁止。
        @param path 键路径，支持点号分隔的子组路径（如'subgroup.key'）
        @return 参数值
        @raises KeyError 如果路径不存在
        @raises ValueError 如果路径无效（包含非法字符、父组引用或深度超限）
        """
        # 分割路径为令牌，处理空令牌和尾随点号
        parts = [p for p in path.split('.') if p]  # 过滤空字符串
        if not parts:
            raise KeyError(f"Empty path: '{path}'")

        if len(parts) == 1:
            # 没有点号，直接在当前组查找
            key = parts[0]
            child = None
        else:
            # 有点号，最后一部分是键，前面是子组路径
            key = parts[-1]
            child = '.'.join(parts[:-1])

        group_path = self._group
        if child is not None:
            child_stripped = child.lstrip('.')
            group_path = '.'.join((group_path, child_stripped))

        group_dict = self.resolve_group_dict(group_path)

        if KEYS_KEY not in group_dict or not group_dict[KEYS_KEY]:
            raise KeyError(f"Group '{group_path}' has no parameters")

        if key not in group_dict[KEYS_KEY]:
            raise KeyError(f"Key '{key}' not found in group '{group_path}'")

        return group_dict[KEYS_KEY][key]

    def reader(self, sub_group: str = '') -> GroupReader:
        """!
        @brief 获取子组的阅读器
        @details 返回一个新的GroupReader实例，其组路径为当前组路径加上sub_group。
                 使用lstrip('.')移除前导点号，".sub"和"sub"被视为相同。
        @param sub_group 子组路径，相对当前组，默认空字符串表示当前组
        @return 新GroupReader实例
        @raises TypeError 如果sub_group不是字符串
        @raises ValueError 如果路径无效（包含非法字符、父组引用或深度超限）
        """
        if not isinstance(sub_group, str):
            raise TypeError(f"sub_group must be str, got {type(sub_group).__name__}")

        group = self._group
        if sub_group:
            sub_group_stripped = sub_group.lstrip('.')
            group = '.'.join((group, sub_group_stripped))

        return GroupReader(self._data, group)

    def keys(self) -> Iterator[str]:
        """!
        @brief 返回当前组所有键的迭代器
        @details 如果当前组不存在或没有参数，返回空迭代器。
        @return 键的迭代器
        @raises ValueError 如果当前组路径无效（包含非法字符、父组引用或深度超限）
        """
        try:
            group_dict = self.resolve_group_dict(self._group)
        except KeyError:
            return iter(())

        if KEYS_KEY not in group_dict or not group_dict[KEYS_KEY]:
            return iter(())

        return iter(group_dict[KEYS_KEY].keys())

    def values(self) -> Iterator[Any]:
        """!
        @brief 返回当前组所有值的迭代器
        @details 如果当前组不存在或没有参数，返回空迭代器。
        @return 值的迭代器
        @raises ValueError 如果当前组路径无效（包含非法字符、父组引用或深度超限）
        """
        try:
            group_dict = self.resolve_group_dict(self._group)
        except KeyError:
            return iter(())

        if KEYS_KEY not in group_dict or not group_dict[KEYS_KEY]:
            return iter(())

        return iter(group_dict[KEYS_KEY].values())

    def items(self) -> Iterator[tuple[str, Any]]:
        """!
        @brief 返回当前组所有键值对的迭代器
        @details 如果当前组不存在或没有参数，返回空迭代器。
        @return 键值对的迭代器
        @raises ValueError 如果当前组路径无效（包含非法字符、父组引用或深度超限）
        """
        try:
            group_dict = self.resolve_group_dict(self._group)
        except KeyError:
            return iter(())

        if KEYS_KEY not in group_dict or not group_dict[KEYS_KEY]:
            return iter(())

        return iter(group_dict[KEYS_KEY].items())


class ArgsManager(PathMixin):
    """!
    @brief 参数管理器类
    @details 管理分组参数，支持权限控制、键冲突检测和只读访问。
    """

    def __init__(self, data: dict[str, Any] | None = None):
        """!
        @brief 初始化参数管理器
        """
        self._data: dict[str, Any] = data if data else {}

    def get_or_create_group_dict(self, group: str, create: bool = True) -> dict[str, Any]:
        """!
        @brief 获取或创建组字典
        @details 空字符串""和单个点"."都视为根组。
                 如果create=True且组不存在，会自动创建中间组。
                 路径会经过完整验证（令牌格式、父组引用、深度限制）。
        @param group 组路径
        @param create 如果组不存在是否创建
        @return 组对应的字典
        @raises KeyError 如果组不存在且create=False
        @raises ValueError 如果路径无效（包含非法字符、父组引用或深度超限）
        """
        if group == '' or group == '.':
            return self._data

        tokens = self.validate_group_path(group)  # 验证路径并规范化

        group_dict = self._data
        for token in tokens:
            if token not in group_dict and not create:
                raise KeyError(f"Group '{group}' does not exist")

            if token not in group_dict:
                group_dict[token] = {}

            group_dict = group_dict[token]

        return group_dict

    def add(self, group: str, key: str, value: Any) -> None:
        """!
        @brief 添加参数到指定组
        @details 如果组不存在会自动创建，如果键已存在则会覆盖。
                 KEYS_KEY是保留键名，不能用作参数键。
        @param group 组路径
        @param key 参数键名
        @param value 参数值，任意类型
        @raises ValueError 如果key为保留键KEYS_KEY
        @raises ValueError 如果路径无效（包含非法字符、父组引用或深度超限）
        """
        if key == KEYS_KEY:
            raise ValueError(f"'{KEYS_KEY}' is a reserved key name")

        group_dict = self.get_or_create_group_dict(group, create=True)

        if KEYS_KEY not in group_dict:
            group_dict[KEYS_KEY] = {}

        logger.info(f"Adding parameter: group='{group}', key='{key}'")

        group_dict[KEYS_KEY][key] = value

    def reader(self, group: str = '.') -> GroupReader:
        """!
        @brief 获取指定组的只读视图
        @details 空字符串""和单个点"."都视为根组，内部统一使用""表示。
        @param group 组路径，'.'表示根组，空字符串''也表示根组
        @return GroupReader实例
        @raises ValueError 如果路径无效（包含非法字符、父组引用或深度超限）
        """
        if group == '.':
            group = ''

        logger.info(f"Creating reader for group: '{group if group else 'root'}'")
        return GroupReader(self._data, group)

    def remove(self, group: str, key: str) -> None:
        """!
        @brief 删除指定组的参数
        @details 如果删除后组的KEYS_KEY字典为空，会删除KEYS_KEY本身。
        @param group 组路径
        @param key 参数键名
        @raises KeyError 如果组或键不存在
        @raises ValueError 如果路径无效（包含非法字符、父组引用或深度超限）
        """
        try:
            group_dict = self.get_or_create_group_dict(group, create=False)
        except KeyError:
            raise KeyError(f"Group '{group}' does not exist")

        if KEYS_KEY not in group_dict or key not in group_dict[KEYS_KEY]:
            raise KeyError(f"Key '{key}' not found in group '{group}'")

        del group_dict[KEYS_KEY][key]
        logger.info(f"Removed parameter: group='{group}', key='{key}'")

        if not group_dict[KEYS_KEY]:
            del group_dict[KEYS_KEY]

    def has_key(self, group: str, key: str) -> bool:
        """!
        @brief 检查键是否存在
        @details 如果组不存在或组没有KEYS_KEY字典，返回False。
                 不抛出异常，静默返回False。
        @param group 组路径
        @param key 参数键名
        @return 如果键存在返回True，否则返回False
        @raises ValueError 如果路径无效（包含非法字符、父组引用或深度超限）
        """
        try:
            group_dict = self.get_or_create_group_dict(group, create=False)
        except KeyError:
            return False

        return KEYS_KEY in group_dict and key in group_dict[KEYS_KEY]

    def has_group(self, group: str) -> bool:
        """!
        @brief 检查组是否存在
        @details 调用get_or_create_group_dict(group, create=False)检查组是否存在。
                 不抛出异常，静默返回False。
        @param group 组路径
        @return 如果组存在返回True，否则返回False
        @raises ValueError 如果路径无效（包含非法字符、父组引用或深度超限）
        """
        try:
            self.get_or_create_group_dict(group, create=False)
            return True
        except KeyError:
            return False


if __name__ == "__main__":
    pass
