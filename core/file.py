# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Iterable, Iterator
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path
from logging import getLogger

logger = getLogger(__name__)


class GroupType(Enum):
    """文件组类型枚举"""
    File = 0
    Folder = 1


@dataclass
class GroupItem(object):
    """文件组项数据类"""
    group_name: str
    group_type: GroupType

    file_name: str
    file_path: Path


@dataclass
class Group(object):
    """文件组数据类"""
    group_name: str
    group_type: GroupType
    group_path: Path

    file_list: list[GroupItem] = field(default_factory=list)


class FileManager(object):
    """文件管理类，统一配置文件的读取与写入，均使用 utf-8-sig 编码"""
    def __init__(self):
        """初始化文件管理器"""
        self._groups: dict[str, Group] = {}

    def create_group(self, name: str, path: Path):
        """!
        创建新文件组，并根据路径自动推断组类型
        @param name 文件组名称
        @param path 文件组路径
        @throws ValueError 当文件组已存在时抛出异常
        """
        logger.debug(f"Creating group '{name}' at path {path}")
        if name in self._groups:
            logger.error(f"Group '{name}' already exists")
            raise ValueError(f"Group '{name}' already exists")

        path = Path(path)
        if path.exists() and path.is_file():
            group_type = GroupType.File
        else:
            group_type = GroupType.Folder

        self._groups[name] = Group(
            group_name=name,
            group_type=group_type,
            group_path=path
        )
        logger.info(f"Group '{name}' created successfully (type: {group_type})")

    def delete_group(self, name: str):
        """!
        删除文件组
        @param name 文件组名称
        @throws ValueError 当文件组不存在时抛出异常
        """
        logger.debug(f"Deleting group '{name}'")
        if name not in self._groups:
            logger.error(f"Group '{name}' does not exist")
            raise ValueError(f"Group '{name}' does not exist")
        del self._groups[name]
        logger.info(f"Group '{name}' deleted successfully")
    
    @staticmethod
    def _normalize_paths(path: str | Path | Iterable[str] | Iterable[Path]) -> list[Path]:
        """!
        将输入规范化为 Path 对象列表
        @param path 输入路径，可以是字符串、Path对象或可迭代对象
        @return 规范化后的Path对象列表
        """
        if isinstance(path, (str, Path)):
            paths = [Path(path)]
        else:
            # 假设是可迭代对象
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
            logger.error(f"Group '{group}' does not exist")
            raise ValueError(f"Group '{group}' does not exist")

        target_group = self._groups[group]

        # 规范化路径为 Path 列表
        paths = self._normalize_paths(path)

        for p in paths:
            # 检查路径是否在组路径下
            if not p.is_relative_to(target_group.group_path):
                logger.error(f"Path '{p}' is not under group root '{target_group.group_path}'")
                raise ValueError(f"Path '{p}' is not under group root '{target_group.group_path}'")

            # 创建 GroupItem
            item = GroupItem(
                group_name=group,
                group_type=target_group.group_type,
                file_name=p.name,
                file_path=p
            )

            # 避免重复添加
            if not any(i.file_path == p for i in target_group.file_list):
                target_group.file_list.append(item)
                logger.debug(f"File '{p}' added to group '{group}'")
            else:
                logger.debug(f"File '{p}' already exists in group '{group}', skipped")

        # 按文件名排序
        target_group.file_list.sort(key=lambda x: x.file_name)
        logger.info(f"File addition to group '{group}' completed. Total files in group: {len(target_group.file_list)}")

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
            logger.error(f"Group '{group}' does not exist")
            raise ValueError(f"Group '{group}' does not exist")

        target_group = self._groups[group]
        paths = self._normalize_paths(path)

        for p in paths:
            # 查找匹配的文件
            found = False
            for item in target_group.file_list:
                if item.file_path == p:
                    target_group.file_list.remove(item)
                    logger.debug(f"File '{p}' removed from group '{group}' (by path)")
                    found = True
                    break
            # 如果未找到且 p 是纯文件名（无目录部分），尝试匹配 file_name
            if not found and not p.is_absolute() and p.parent == Path('.'):
                for item in target_group.file_list:
                    if item.file_name == p.name:
                        target_group.file_list.remove(item)
                        logger.debug(f"File '{p.name}' removed from group '{group}' (by name)")
                        found = True
                        break
            if not found:
                logger.error(f"File '{p}' not found in group '{group}'")
                raise ValueError(f"File '{p}' not found in group '{group}'")
        logger.info(f"File deletion from group '{group}' completed. Remaining files in group: {len(target_group.file_list)}")

    def collect_file(self, group: str, suffix: str = None):
        """!
        根据组的根目录，添加目录中所有文件。仅包括第一层文件
        @param group 文件组名称
        @param suffix 文件后缀，可选
        @throws ValueError 当文件组不存在或不是文件夹类型时抛出异常
        """
        logger.debug(f"Collecting files in group '{group}' with suffix '{suffix}'")
        if group not in self._groups:
            logger.error(f"Group '{group}' does not exist")
            raise ValueError(f"Group '{group}' does not exist")

        target_group = self._groups[group]
        if target_group.group_type != GroupType.Folder:
            logger.error(f"Group '{group}' is not a folder, cannot collect files")
            raise ValueError(f"Group '{group}' is not a folder, cannot collect files")

        # 收集第一层文件
        file_paths = [
            item for item in target_group.group_path.iterdir()
            if item.is_file() and (not suffix or item.suffix.lower() == suffix)
        ]

        # 使用 create_file 添加文件（会处理去重和排序）
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

        target_group = self._groups[group]
        p = Path(path)

        # 验证文件属于组
        if not any(item.file_path == p for item in target_group.file_list):
            raise ValueError(f"File '{p}' not in group '{group}'")

        # 读取文件内容
        try:
            return p.read_text(encoding='utf-8-sig')
        except OSError as e:
            raise IOError(f"Failed to read file '{p}': {e}")

    def read_files(self, group: str) -> list[str]:
        """!
        读取组中所有文件内容
        @param group 文件组名称
        @return 文件内容列表
        @throws ValueError 当文件组不存在时抛出异常
        @throws IOError 当文件读取失败时抛出异常
        """
        if group not in self._groups:
            raise ValueError(f"Group '{group}' does not exist")

        target_group = self._groups[group]
        contents = []
        for item in target_group.file_list:
            try:
                content = item.file_path.read_text(encoding='utf-8-sig')
                contents.append(content)
            except OSError as e:
                raise IOError(f"Failed to read file '{item.file_path}': {e}")
        return contents

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
        for item in target_group.file_list:
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
        p = Path(path)

        # 检查路径是否在组路径下
        if not p.is_relative_to(target_group.group_path):
            raise ValueError(f"Path '{p}' is not under group root '{target_group.group_path}'")

        # 如果文件不在文件列表中，则添加
        if not any(item.file_path == p for item in target_group.file_list):
            self.create_file(group, p)

        # 确保父目录存在
        p.parent.mkdir(parents=True, exist_ok=True)

        # 写入文件
        try:
            p.write_text(content, encoding='utf-8-sig')
        except OSError as e:
            raise IOError(f"Failed to write file '{p}': {e}")

if __name__ == '__main__':
    pass
