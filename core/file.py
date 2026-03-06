# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.file
@brief 文件管理模块
@details 提供游戏文件的分组管理、读写操作，统一使用utf-8-sig编码
"""

from logging import getLogger
from typing import Iterable, Iterator
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path

logger = getLogger(__name__)


class GroupType(Enum):
    """!
    @brief 文件组类型枚举
    """
    File = 0    #!< 文件类型组（单个文件）
    Folder = 1  #!< 文件夹类型组（多个文件）


@dataclass
class GroupItem(object):
    """!
    @brief 文件组项数据类
    @details 存储单个文件在文件组中的信息
    """
    group_name: str                 #!< 所属文件组名称
    group_type: GroupType           #!< 文件组类型

    file_name: str                  #!< 文件名
    file_path: Path                 #!< 文件完整路径


@dataclass
class Group(object):
    """!
    @brief 文件组数据类
    @details 存储文件组的完整信息，包括组内所有文件字典
    """
    group_name: str                 #!< 文件组名称
    group_type: GroupType           #!< 文件组类型
    group_path: Path                #!< 文件组路径

    file_dict: dict[str, GroupItem] = field(default_factory=dict)  #!< 文件字典，键为文件名，值为GroupItem对象


class FileManager(object):
    """!
    @brief 文件管理类
    @details 统一配置文件的读取与写入，均使用utf-8-sig编码，支持文件组管理
    """
    def __init__(self):
        """!
        @brief 初始化文件管理器
        """
        self._groups: dict[str, Group] = {}  #!< 文件组字典，键为组名，值为Group对象

    def create_group(self, name: str, path: Path):
        """!
        创建新文件组，并根据路径自动推断组类型
        @param name 文件组名称
        @param path 文件组路径
        @throws ValueError 当文件组已存在时抛出异常
        """
        logger.debug(f"Creating group '{name}' at path {path}")
        if name in self._groups:
            raise ValueError(f"Group '{name}' already exists")

        path = Path(path)
        if path.exists() and path.is_file():
            group_type = GroupType.File
        else:
            group_type = GroupType.Folder

        self._groups[name] = Group(group_name=name, group_type=group_type, group_path=path)

        logger.info(f"Group '{name}' created successfully (type: {group_type})")

    def delete_group(self, name: str):
        """!
        删除文件组
        @param name 文件组名称
        @throws ValueError 当文件组不存在时抛出异常
        """
        logger.debug(f"Deleting group '{name}'")

        if name not in self._groups:
            raise ValueError(f"Group '{name}' does not exist")

        del self._groups[name]

        logger.info(f"Group '{name}' deleted successfully")
    
    @staticmethod
    def normalize_paths(path: str | Path | Iterable[str] | Iterable[Path]) -> list[Path]:
        """!
        将输入规范化为 Path 对象列表
        @param path 输入路径，可以是字符串、Path对象或可迭代对象
        @return 规范化后的Path对象列表
        """
        if isinstance(path, (str, Path)):
            paths = [Path(path)]
        else:
            paths = [Path(p) if isinstance(p, str) else p for p in path]

        return paths

    def create_file(self, group: str, path: str | Path | Iterable[str] | Iterable[Path]):
        """!
        添加文件到文件组，需判断文件是否为文件组的子目录，文件可以已经存在，也可以不存在。
        完成后，对文件列表按文件名排序
        @param group 文件组名称
        @param path 文件路径，可以是字符串、Path对象或可迭代对象
        @throws ValueError 当文件组不存在或路径不在组根目录下时抛出异常
        """
        logger.debug(f"Adding file(s) to group '{group}': {path}")

        if group not in self._groups:
            raise ValueError(f"Group '{group}' does not exist")

        target_group = self._groups[group]

        # 规范化路径为 Path 列表
        paths = self.normalize_paths(path)

        for p in paths:
            # 检查路径是否在组路径下
            if not p.is_relative_to(target_group.group_path):
                raise ValueError(f"Path '{p}' is not under group root '{target_group.group_path}'")

            # 避免重复添加
            if p.name not in target_group.file_dict:
                item = GroupItem(group_name=group, group_type=target_group.group_type, file_name=p.name, file_path=p)
                target_group.file_dict[p.name] = item

                logger.debug(f"File '{p}' added to group '{group}'")
            else:
                logger.debug(f"File '{p}' already exists in group '{group}', skipped")

        logger.info(f"File addition to group '{group}' completed. Total files in group: {len(target_group.file_dict)}")

    def delete_file(self, group: str, path: str | Path | Iterable[str] | Iterable[Path]):
        """!
        根据组名，文件名或路径删除文件。
        文件可以不存在于文件系统中，但一定存在于此类中，否则抛出异常
        @param group 文件组名称
        @param path 文件路径，可以是字符串、Path对象或可迭代对象
        @throws ValueError 当文件组不存在或文件未找到时抛出异常
        """
        logger.debug(f"Deleting file(s) from group '{group}': {path}")

        if group not in self._groups:
            raise ValueError(f"Group '{group}' does not exist")

        target_group = self._groups[group]
        paths = self.normalize_paths(path)

        for p in paths:
            # 查找匹配的文件
            found = False

            if p in target_group.file_dict:
                del target_group.file_dict[p.name]

                logger.debug(f"File '{p}' removed from group '{group}' (by path)")
                found = True
            # 如果未找到且 p 是纯文件名（无目录部分），尝试匹配 file_name
            elif not p.is_absolute() and p.parent == Path('.') and p.name in target_group.file_dict:
                del target_group.file_dict[p.name]

                logger.debug(f"File '{p.name}' removed from group '{group}' (by name)")
                found = True

            if not found:
                raise ValueError(f"File '{p}' not found in group '{group}'")

        logger.info(f"File deletion from group '{group}' completed. Remaining files in group: {len(target_group.file_dict)}")

    def collect_file(self, group: str, suffix: str = None):
        """!
        根据组的根目录，添加目录中所有文件。仅包括第一层文件
        @param group 文件组名称
        @param suffix 文件后缀，可选
        @throws ValueError 当文件组不存在或不是文件夹类型时抛出异常
        """
        logger.debug(f"Collecting files in group '{group}' with suffix '{suffix}'")

        if group not in self._groups:
            raise ValueError(f"Group '{group}' does not exist")

        target_group = self._groups[group]

        if target_group.group_type != GroupType.Folder:
            raise ValueError(f"Group '{group}' is not a folder, cannot collect files")

        # 收集第一层文件
        file_paths = [
            item for item in target_group.group_path.iterdir()
            if item.is_file() and (not suffix or item.suffix.lower() == suffix)
        ]

        # 使用 create_file 添加文件
        if file_paths:
            self.create_file(group, file_paths)
            logger.info(f"Collected {len(file_paths)} file(s) from directory '{target_group.group_path}'")
        else:
            logger.warning(f"No files found in directory '{target_group.group_path}' with suffix '{suffix}'")

    def read_file(self, group: str, path: str | Path) -> str:
        """!
        读取单个文件内容
        @param group 文件组名称
        @param path 文件路径
        @return 文件内容字符串
        @throws ValueError 当文件组不存在或文件不在组中时抛出异常
        @throws IOError 当文件读取失败时抛出异常
        """
        if group not in self._groups:
            raise ValueError(f"Group '{group}' does not exist")

        target_group: Group = self._groups[group]

        # 验证文件属于组
        if isinstance(path, Path) and not path.is_relative_to(target_group.group_path):
            raise ValueError(f"File '{path}' not in group '{group}'")

        if isinstance(path, str):
            file_item: GroupItem = target_group.file_dict[path]
        else:
            file_item: GroupItem = target_group.file_dict[path.name]

        # 读取文件内容
        try:
            return file_item.file_path.read_text(encoding='utf-8-sig')
        except OSError as e:
            raise IOError(f"Failed to read file '{path}': {e}")

    def read_files(self, group: str) -> list[str]:
        """!
        读取组中所有文件内容
        @param group 文件组名称
        @return 文件内容列表
        @throws ValueError 当文件组不存在时抛出异常
        @throws IOError 当文件读取失败时抛出异常
        """
        return [context for _, context in self.read_files_in_range(group)]

    def read_files_in_range(self, group: str) -> Iterator[tuple[Path, str]]:
        """!
        读取组中所有文件内容，使用迭代器，迭代器返回文件 path 对象与文件内容
        @param group 文件组名称
        @return 迭代器，每次返回(文件路径, 文件内容)元组
        @throws ValueError 当文件组不存在时抛出异常
        @throws IOError 当文件读取失败时抛出异常
        """
        if group not in self._groups:
            raise ValueError(f"Group '{group}' does not exist")

        target_group = self._groups[group]

        for item in target_group.file_dict.values():
            try:
                content = item.file_path.read_text(encoding='utf-8-sig')
                yield item.file_path, content
            except OSError as e:
                raise IOError(f"Failed to read file '{item.file_path}': {e}")

    def write_file(self, group: str, path: str | Path, content: str):
        """!
        写入文件内容，若文件存在，则覆盖，若不存在，则先添加到此类中，再写入文件
        @param group 文件组名称
        @param path 文件路径
        @param content 文件内容
        @throws ValueError 当文件组不存在或路径不在组根目录下时抛出异常
        @throws IOError 当文件写入失败时抛出异常
        """
        if group not in self._groups:
            raise ValueError(f"Group '{group}' does not exist")

        target_group = self._groups[group]

        if isinstance(path, str):
            p = target_group.group_path / path
        elif isinstance(path, Path):
            p = path
        else:
            raise ValueError(f"Invalid path type: {type(path)}")

        # 检查路径是否在组路径下
        if not p.is_relative_to(target_group.group_path):
            raise ValueError(f"Path '{p}' is not under group root '{target_group.group_path}'")

        # 如果文件不在文件字典中，则添加
        if p.name not in target_group.file_dict:
            self.create_file(group, p)

        # 确保父目录存在
        p.parent.mkdir(parents=True, exist_ok=True)

        # 写入文件
        try:
            p.write_text(content, encoding='utf-8-sig')
        except OSError as e:
            raise IOError(f"Failed to write file '{p}': {e}")

    def list_file(self, group: str) -> list[Path]:
        """!
        列出组中的所有文件
        @param group 文件组名称
        @return 文件列表
        @throws ValueError 当文件组不存在时抛出异常
        """
        if group not in self._groups:
            raise ValueError(f"Group '{group}' does not exist")

        return [item.file_path for item in self._groups[group].file_dict.values()]

if __name__ == '__main__':
    pass
