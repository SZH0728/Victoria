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
    def __init__(self) -> None:
        """!
        @brief 初始化文件管理器
        """
        self._groups: dict[str, Group] = {}  #!< 文件组字典，键为组名，值为Group对象

    @staticmethod
    def normalize_paths(path: str | Path | Iterable[str] | Iterable[Path]) -> list[Path]:
        """!
        将输入规范化为 Path 对象列表
        @param path 输入路径，可以是字符串、Path对象或可迭代对象
        @return 规范化后的Path对象列表
        """
        # 处理字符串输入
        if isinstance(path, str):
            return [Path(path)]

        # 处理Path对象输入
        if isinstance(path, Path):
            return [path]

        # 处理可迭代对象输入（列表、元组等）
        paths: list[Path] = []
        for p in path:
            # 检查元素类型并进行相应转换
            if isinstance(p, str):
                paths.append(Path(p))
            elif isinstance(p, Path):
                paths.append(p)
            else:
                raise ValueError(f"Invalid path type in iterable: {type(p)} - {p}")

        return paths

    def raise_for_group_not_exist(self, group: str):
        """!
        检查文件组是否存在，不存在则抛出异常
        @param group 文件组名称
        @throws ValueError 当文件组不存在时抛出异常
        """
        # 验证文件组是否存在
        if group not in self._groups:
            available_groups = list(self._groups.keys())
            raise ValueError(f"Group '{group}' does not exist. Available groups: {available_groups}")

    def raise_for_group_is_exist(self, group: str):
        """!
        检查文件组是否存在，存在则抛出异常
        @param group 文件组名称
        @throws ValueError 当文件组已存在时抛出异常
        """
        # 验证文件组是否已存在
        if group in self._groups:
            raise ValueError(f"Group '{group}' already exists. Existing groups: {list(self._groups.keys())}")

    @staticmethod
    def raise_for_file_path_not_in_group(group: Group, path: Path):
        """!
        检查文件路径是否在文件组中，不在则抛出异常
        @param group 文件组对象
        @param path 文件路径
        @throws ValueError 当文件路径不在组中时抛出异常
        """
        # 验证文件路径是否在文件组根目录下
        if not path.is_relative_to(group.group_path):
            raise ValueError(f"Path '{path}' is not under group root '{group.group_path}'. "
                           f"Expected path to be relative to group directory.")

    @staticmethod
    def read_file_or_raise(path: Path) -> str:
        """!
        读取文件内容，并返回字符串
        @param path 文件路径
        @return 文件内容字符串
        @throws IOError 如果文件不存在或无法读取时抛出异常
        """
        try:
            # 使用utf-8-sig编码读取文件，支持字节顺序标记(BOM)
            return path.read_text(encoding='utf-8-sig')
        except OSError as e:
            raise IOError(f"Failed to read file '{path}': {e}. Check if file exists and has proper read permissions.")

    @staticmethod
    def write_file_or_raise(path: Path, content: str) -> None:
        """!
        将内容写入文件
        @param path 文件路径
        @param content 文件内容
        @throws IOError 如果文件无法写入时抛出异常
        """
        try:
            # 使用utf-8-sig编码写入文件，保持与读取的一致性
            path.write_text(content, encoding='utf-8-sig')
        except OSError as e:
            raise IOError(f"Failed to write file '{path}': {e}. Check if directory exists and has write permissions.")


    def create_group(self, name: str, path: Path):
        """!
        创建新文件组，并根据路径自动推断组类型
        @param name 文件组名称
        @param path 文件组路径
        @throws ValueError 当文件组已存在时抛出异常
        """
        logger.info(f"Creating new file group '{name}' at path '{path}'")
        self.raise_for_group_is_exist(name)

        path: Path = Path(path)

        # 自动推断组类型：检查路径是否存在且为文件
        if path.exists() and path.is_file():
            group_type: GroupType = GroupType.File
            logger.debug(f"Detected file group type for '{name}': {group_type} (path exists and is file)")
        else:
            group_type: GroupType = GroupType.Folder
            logger.debug(f"Detected folder group type for '{name}': {group_type} (path does not exist or is not file)")

        # 创建新的Group对象并存储到内部字典
        self._groups[name] = Group(group_name=name, group_type=group_type, group_path=path)

        logger.info(f"Group '{name}' created successfully (type: {group_type}, path: '{path}')")

    def delete_group(self, name: str):
        """!
        删除文件组
        @param name 文件组名称
        @throws ValueError 当文件组不存在时抛出异常
        """
        logger.info(f"Deleting file group '{name}'")
        self.raise_for_group_not_exist(name)

        # 从内部字典中删除组
        del self._groups[name]

        logger.info(f"Group '{name}' deleted successfully. Remaining groups: {len(self._groups)}")

    def create_file(self, group: str, path: str | Path | Iterable[str] | Iterable[Path]):
        """!
        添加文件到文件组，需判断文件是否为文件组的子目录，文件可以已经存在，也可以不存在。
        完成后，对文件列表按文件名排序
        @param group 文件组名称
        @param path 文件路径，可以是字符串、Path对象或可迭代对象
        @throws ValueError 当文件组不存在或路径不在组根目录下时抛出异常
        """
        logger.info(f"Adding file(s) to group '{group}': {path}")

        self.raise_for_group_not_exist(group)

        target_group: Group = self._groups[group]

        # 规范化路径为 Path 列表
        paths: list[Path] = self.normalize_paths(path)

        for p in paths:
            # 检查路径是否在组路径下
            self.raise_for_file_path_not_in_group(target_group, p)

            # 避免重复添加已存在的文件
            if p.name not in target_group.file_dict:
                # 创建新的GroupItem对象
                item: GroupItem = GroupItem(group_name=group, group_type=target_group.group_type, file_name=p.name, file_path=p)
                target_group.file_dict[p.name] = item
                logger.debug(f"File '{p}' added to group '{group}'")
            else:
                logger.debug(f"File '{p.name}' already exists in group '{group}', skipped")

        logger.info(f"File addition to group '{group}' completed. Total files in group: {len(target_group.file_dict)}")

    def delete_file(self, group: str, path: str | Path | Iterable[str] | Iterable[Path]):
        """!
        根据组名，文件名或路径删除文件。
        文件可以不存在于文件系统中，但一定存在于此类中，否则抛出异常
        @param group 文件组名称
        @param path 文件路径，可以是字符串、Path对象或可迭代对象
        @throws ValueError 当文件组不存在或文件未找到时抛出异常
        """
        logger.info(f"Deleting file(s) from group '{group}': {path}")

        self.raise_for_group_not_exist(group)

        target_group: Group = self._groups[group]
        paths: list[Path] = self.normalize_paths(path)

        all_available_files = list(target_group.file_dict.keys())

        for p in paths:
            # 查找匹配的文件
            found: bool = False

            # 首先尝试按完整路径查找
            if p in target_group.file_dict:
                del target_group.file_dict[p.name]
                logger.debug(f"File '{p}' removed from group '{group}' (by path)")
                found: bool = True
            # 如果未找到且 p 是纯文件名（无目录部分），尝试匹配 file_name
            elif not p.is_absolute() and p.parent == Path('.') and p.name in target_group.file_dict:
                del target_group.file_dict[p.name]
                logger.debug(f"File '{p.name}' removed from group '{group}' (by name)")
                found: bool = True

            if not found:
                logger.warning(f"File '{p}' not found in group '{group}'. Available files: {all_available_files}")

        logger.info(f"File deletion from group '{group}' completed. Remaining files in group: {len(target_group.file_dict)}")

    def collect_file(self, group: str, suffix: str | None = None):
        """!
        根据组的根目录，添加目录中所有文件。仅包括第一层文件
        @param group 文件组名称
        @param suffix 文件后缀，可选
        @throws ValueError 当文件组不存在或不是文件夹类型时抛出异常
        """
        logger.info(f"Collecting files in group '{group}' with suffix '{suffix}'")

        self.raise_for_group_not_exist(group)

        target_group: Group = self._groups[group]

        # 检查组类型是否为文件夹类型
        if target_group.group_type != GroupType.Folder:
            raise ValueError(f"Group '{group}' is not a folder (type: {target_group.group_type}), cannot collect files")

        # 收集第一层文件，可选后缀过滤
        file_paths = [
            item for item in target_group.group_path.iterdir()
            if item.is_file() and (not suffix or item.suffix.lower() == suffix)
        ]

        # 使用 create_file 添加文件
        if file_paths:
            self.create_file(group, file_paths)
            logger.info(f"Collected {len(file_paths)} file(s) from directory '{target_group.group_path}' with suffix '{suffix}'")
        else:
            logger.warning(f"No files found in directory '{target_group.group_path}' with suffix '{suffix}'. "
                           f"Directory contents: {list(target_group.group_path.iterdir()) if target_group.group_path.exists() else 'Directory does not exist'}")

    def read_file(self, group: str, path: str | Path) -> str:
        """!
        读取单个文件内容
        @param group 文件组名称
        @param path 文件路径
        @return 文件内容字符串
        @throws ValueError 当文件组不存在或文件不在组中时抛出异常
        @throws IOError 当文件读取失败时抛出异常
        """
        logger.info(f"Reading file '{path}' from group '{group}'")

        self.raise_for_group_not_exist(group)

        target_group: Group = self._groups[group]

        # 验证文件路径在组范围内
        self.raise_for_file_path_not_in_group(target_group, path)

        # 根据路径类型查找对应的GroupItem对象
        if isinstance(path, str):
            if path not in target_group.file_dict:
                raise ValueError(f"File '{path}' not found in group '{group}'. Available files: {list(target_group.file_dict.keys())}")
            file_item: GroupItem = target_group.file_dict[path]
        elif isinstance(path, Path):
            if path.name not in target_group.file_dict:
                raise ValueError(f"File '{path.name}' not found in group '{group}'. Available files: {list(target_group.file_dict.keys())}")
            file_item: GroupItem = target_group.file_dict[path.name]
        else:
            raise ValueError(f"Invalid path type: {type(path)}. Expected str or Path.")

        logger.debug(f"Successfully reading file '{file_item.file_path}' from group '{group}'")
        return self.read_file_or_raise(file_item.file_path)

    def read_files(self, group: str) -> list[str]:
        """!
        读取组中所有文件内容
        @param group 文件组名称
        @return 文件内容列表
        @throws ValueError 当文件组不存在时抛出异常
        @throws IOError 当文件读取失败时抛出异常
        """
        self.raise_for_group_not_exist(group)

        file_count = len(self._groups[group].file_dict)
        logger.info(f"Reading all files from group '{group}' (total files: {file_count})")

        contents = [context for _, context in self.read_files_in_range(group)]
        logger.info(f"Successfully read {len(contents)} files from group '{group}'")
        return contents

    def read_files_in_range(self, group: str) -> Iterator[tuple[Path, str]]:
        """!
        读取组中所有文件内容，使用迭代器，迭代器返回文件 path 对象与文件内容
        @param group 文件组名称
        @return 迭代器，每次返回(文件路径, 文件内容)元组
        @throws ValueError 当文件组不存在时抛出异常
        @throws IOError 当文件读取失败时抛出异常
        """
        self.raise_for_group_not_exist(group)

        target_group: Group = self._groups[group]

        for item in target_group.file_dict.values():
            content: str = self.read_file_or_raise(item.file_path)
            yield item.file_path, content

    def write_file(self, group: str, path: str | Path, content: str):
        """!
        写入文件内容，若文件存在，则覆盖，若不存在，则先添加到此类中，再写入文件
        @param group 文件组名称
        @param path 文件路径
        @param content 文件内容
        @throws ValueError 当文件组不存在或路径不在组根目录下时抛出异常
        @throws IOError 当文件写入失败时抛出异常
        """
        logger.info(f"Writing file '{path}' to group '{group}'")

        self.raise_for_group_not_exist(group)

        target_group: Group = self._groups[group]

        # 规范化路径为绝对路径
        if isinstance(path, str):
            path: Path = target_group.group_path / path
        elif isinstance(path, Path):
            path: Path = path
        else:
            raise ValueError(f"Invalid path type: {type(path)}. Expected str or Path.")

        # 检查路径是否在组路径下
        self.raise_for_file_path_not_in_group(target_group, path)

        # 如果文件不在文件字典中，则添加到组中
        if path.name not in target_group.file_dict:
            logger.debug(f"File '{path.name}' not in group, adding to group '{group}'")
            self.create_file(group, path)

        # 确保父目录存在
        path.parent.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured parent directory exists: '{path.parent}'")

        self.write_file_or_raise(path, content)
        logger.info(f"Successfully wrote file '{path}' to group '{group}'")

    def list_file(self, group: str) -> list[Path]:
        """!
        列出组中的所有文件
        @param group 文件组名称
        @return 文件路径列表
        @throws ValueError 当文件组不存在时抛出异常
        """
        self.raise_for_group_not_exist(group)

        files = [item.file_path for item in self._groups[group].file_dict.values()]
        logger.debug(f"Listed {len(files)} files from group '{group}'")
        return files

if __name__ == '__main__':
    pass
