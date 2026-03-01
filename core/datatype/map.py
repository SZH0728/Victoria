# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Iterator, Generator, Any, TypeVar, Generic
from dataclasses import dataclass, field

T = TypeVar('T')

@dataclass
class Map(Generic[T]):
    """!
    @brief 通用映射容器类，存储键到值的映射
    @details 提供类似字典的接口访问值对象，支持通过.和[]操作符读写，
             同时提供keys()、values()、items()、get()等字典常用方法
    """
    _data: dict[str, T] = field(default_factory=dict, init=False, repr=False)

    def __getitem__(self, key: str) -> T:
        """!
        @brief 通过字典键访问值对象
        @param key 键
        @return 对应的值对象
        @throws KeyError 当键名不存在时抛出异常
        """
        return self._data[key]

    def __setitem__(self, key: str, value: T):
        """!
        @brief 通过字典键设置值对象
        @param key 键
        @param value 值对象
        """
        self._data[key] = value

    def __contains__(self, key: str) -> bool:
        """!
        @brief 检查键是否存在
        @param key 键
        @return 键是否存在
        """
        return key in self._data

    def __getattr__(self, name: str) -> Any:
        """!
        @brief 通过属性名访问值对象
        @details 当属性不存在于实例或类中时，尝试从_data字典中获取
        @param name 属性名
        @return 对应的值对象
        @throws AttributeError 当属性名不存在时抛出异常
        """
        # 避免递归调用，检查是否在__dict__中
        if name in self.__dict__ or hasattr(type(self), name):
            # 这应该不会发生，因为__getattr__只在属性未找到时调用
            # 但为了安全起见，调用super().__getattribute__
            return super().__getattribute__(name)
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(f"'Map' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any):
        """!
        @brief 通过属性名设置值对象
        @details 如果属性名不是_data且不是类属性，则存储到_data字典中
        @param name 属性名
        @param value 属性值
        """
        # 如果name是_data，或者name是类属性（方法等），或者是以双下划线开头的特殊属性，则使用默认的__setattr__
        if name == '_data' or hasattr(type(self), name) or name.startswith('__'):
            super().__setattr__(name, value)
        else:
            # 否则存储到_data字典中
            self._data[name] = value

    def __delattr__(self, name: str):
        """!
        @brief 删除属性
        @details 如果属性名在_data中，则从_data中删除；否则如果是类属性则禁止删除，否则调用父类方法
        @param name 属性名
        """
        if name == '_data':
            super().__delattr__(name)
        elif name.startswith('__'):
            # 双下划线特殊属性，调用父类方法
            super().__delattr__(name)
        elif name in self._data:
            del self._data[name]
        elif hasattr(type(self), name):
            raise AttributeError(f"Cannot delete class attribute '{name}'")
        else:
            super().__delattr__(name)

    def __delitem__(self, key: str):
        """!
        @brief 删除键值对
        @param key 键
        """
        del self._data[key]

    def __iter__(self) -> Iterator[str]:
        """!
        @brief 迭代键
        @return 键迭代器
        """
        return iter(self._data)

    def __repr__(self) -> str:
        """!
        @brief 返回对象的可读字符串表示
        @return 映射的字符串表示
        """
        items = []
        for key, value in self._data.items():
            items.append(f"{key}: {repr(value)}")
        return f"Map({{{', '.join(items)}}})"

    def __len__(self) -> int:
        """!
        @brief 获取映射的长度
        @return 映射的长度
        """
        return len(self._data)

    def keys(self) -> tuple[str, ...]:
        """!
        @brief 返回所有键
        @return 键元组
        """
        return tuple(self._data.keys())

    def values(self) -> Generator[T, None, None]:
        """!
        @brief 返回所有值对象
        @return 值对象生成器
        """
        return (value for value in self._data.values())

    def items(self) -> Generator[tuple[str, T], None, None]:
        """!
        @brief 返回所有键值对
        @return 键值对生成器，每个元素为(键, 值对象)
        """
        return ((key, value) for key, value in self._data.items())

    def get(self, key: str, default: Any = None) -> Any:
        """!
        @brief 获取值对象，如果键不存在则返回默认值
        @param key 键
        @param default 默认值
        @return 值对象或默认值
        """
        return self._data.get(key, default)

    def clear(self):
        """!
        @brief 清空映射
        """
        self._data.clear()


if __name__ == '__main__':
    pass