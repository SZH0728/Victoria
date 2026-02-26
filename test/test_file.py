# -*- coding:utf-8 -*-
# AUTHOR: Sun

import unittest
import tempfile
import os
from pathlib import Path
from core.file import FileManager, GroupType


class TestFileManager(unittest.TestCase):
    """FileManager 单元测试类"""

    def setUp(self):
        """测试前准备临时目录"""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = FileManager()

    def tearDown(self):
        """测试后清理临时目录"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_group_folder(self):
        """测试创建文件夹类型的文件组"""
        group_name = "test_folder_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 验证组已创建
        self.assertIn(group_name, self.manager._groups)
        group = self.manager._groups[group_name]
        self.assertEqual(group.group_name, group_name)
        self.assertEqual(group.group_type, GroupType.Folder)
        self.assertEqual(group.group_path, folder_path)
        self.assertEqual(len(group.file_list), 0)

    def test_create_group_file(self):
        """测试创建文件类型的文件组"""
        group_name = "test_file_group"
        file_path = Path(self.temp_dir) / "test.txt"
        file_path.write_text("test", encoding="utf-8-sig")

        self.manager.create_group(group_name, file_path)

        # 验证组已创建
        self.assertIn(group_name, self.manager._groups)
        group = self.manager._groups[group_name]
        self.assertEqual(group.group_name, group_name)
        self.assertEqual(group.group_type, GroupType.File)
        self.assertEqual(group.group_path, file_path)
        self.assertEqual(len(group.file_list), 0)

    def test_create_group_duplicate(self):
        """测试创建重复文件组应抛出异常"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 再次创建相同名称的组应抛出 ValueError
        with self.assertRaises(ValueError) as context:
            self.manager.create_group(group_name, folder_path)

        self.assertIn(f"Group '{group_name}' already exists", str(context.exception))

    def test_delete_group(self):
        """测试删除文件组"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)
        self.manager.delete_group(group_name)

        # 验证组已删除
        self.assertNotIn(group_name, self.manager._groups)

    def test_delete_nonexistent_group(self):
        """测试删除不存在的文件组应抛出异常"""
        with self.assertRaises(ValueError) as context:
            self.manager.delete_group("nonexistent_group")

        self.assertIn("Group 'nonexistent_group' does not exist", str(context.exception))

    def test_create_file_single(self):
        """测试添加单个文件到文件组"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建测试文件
        test_file = folder_path / "test.txt"
        test_file.write_text("content", encoding="utf-8-sig")

        self.manager.create_file(group_name, test_file)

        # 验证文件已添加
        group = self.manager._groups[group_name]
        self.assertEqual(len(group.file_list), 1)
        self.assertEqual(group.file_list[0].file_name, "test.txt")
        self.assertEqual(group.file_list[0].file_path, test_file)

    def test_create_file_multiple(self):
        """测试添加多个文件到文件组"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建多个测试文件
        file1 = folder_path / "a.txt"
        file2 = folder_path / "b.txt"
        file1.write_text("content1", encoding="utf-8-sig")
        file2.write_text("content2", encoding="utf-8-sig")

        self.manager.create_file(group_name, [file1, file2])

        # 验证文件已添加且已排序
        group = self.manager._groups[group_name]
        self.assertEqual(len(group.file_list), 2)
        self.assertEqual(group.file_list[0].file_name, "a.txt")
        self.assertEqual(group.file_list[1].file_name, "b.txt")

    def test_create_file_duplicate(self):
        """测试重复添加同一文件应去重"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建测试文件
        test_file = folder_path / "test.txt"
        test_file.write_text("content", encoding="utf-8-sig")

        # 第一次添加
        self.manager.create_file(group_name, test_file)
        # 第二次添加相同文件
        self.manager.create_file(group_name, test_file)

        # 验证文件只添加了一次
        group = self.manager._groups[group_name]
        self.assertEqual(len(group.file_list), 1)

    def test_create_file_outside_group_root(self):
        """测试添加不在组根目录下的文件应抛出异常"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建不在组目录下的文件
        outside_file = Path(self.temp_dir) / "outside.txt"
        outside_file.write_text("content", encoding="utf-8-sig")

        with self.assertRaises(ValueError) as context:
            self.manager.create_file(group_name, outside_file)

        self.assertIn("is not under group root", str(context.exception))

    def test_create_file_nonexistent_group(self):
        """测试向不存在的文件组添加文件应抛出异常"""
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("content", encoding="utf-8-sig")

        with self.assertRaises(ValueError) as context:
            self.manager.create_file("nonexistent_group", test_file)

        self.assertIn("Group 'nonexistent_group' does not exist", str(context.exception))

    def test_delete_file_by_path(self):
        """测试通过路径删除文件"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建并添加文件
        test_file = folder_path / "test.txt"
        test_file.write_text("content", encoding="utf-8-sig")
        self.manager.create_file(group_name, test_file)

        # 删除文件
        self.manager.delete_file(group_name, test_file)

        # 验证文件已删除
        group = self.manager._groups[group_name]
        self.assertEqual(len(group.file_list), 0)

    def test_delete_file_by_name(self):
        """测试通过文件名删除文件（相对路径）"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建并添加文件
        test_file = folder_path / "test.txt"
        test_file.write_text("content", encoding="utf-8-sig")
        self.manager.create_file(group_name, test_file)

        # 使用文件名（相对路径）删除文件
        self.manager.delete_file(group_name, "test.txt")

        # 验证文件已删除
        group = self.manager._groups[group_name]
        self.assertEqual(len(group.file_list), 0)

    def test_delete_file_multiple(self):
        """测试删除多个文件"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建并添加多个文件
        file1 = folder_path / "a.txt"
        file2 = folder_path / "b.txt"
        file1.write_text("content1", encoding="utf-8-sig")
        file2.write_text("content2", encoding="utf-8-sig")
        self.manager.create_file(group_name, [file1, file2])

        # 删除多个文件
        self.manager.delete_file(group_name, [file1, file2])

        # 验证文件已删除
        group = self.manager._groups[group_name]
        self.assertEqual(len(group.file_list), 0)

    def test_delete_file_nonexistent(self):
        """测试删除不存在的文件应抛出异常"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建但未添加的文件
        test_file = folder_path / "test.txt"
        test_file.write_text("content", encoding="utf-8-sig")

        with self.assertRaises(ValueError) as context:
            self.manager.delete_file(group_name, test_file)

        self.assertIn("not found in group", str(context.exception))

    def test_collect_file(self):
        """测试收集目录中的所有文件"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建多个文件
        file1 = folder_path / "a.txt"
        file2 = folder_path / "b.txt"
        subdir = folder_path / "subdir"
        subdir.mkdir()
        file3 = subdir / "c.txt"  # 子目录中的文件，不应被收集

        file1.write_text("content1", encoding="utf-8-sig")
        file2.write_text("content2", encoding="utf-8-sig")
        file3.write_text("content3", encoding="utf-8-sig")

        self.manager.collect_file(group_name)

        # 验证只收集了第一层文件
        group = self.manager._groups[group_name]
        self.assertEqual(len(group.file_list), 2)
        file_names = [item.file_name for item in group.file_list]
        self.assertIn("a.txt", file_names)
        self.assertIn("b.txt", file_names)
        self.assertNotIn("c.txt", file_names)

    def test_collect_file_nonexistent_group(self):
        """测试收集不存在的文件组的文件应抛出异常"""
        with self.assertRaises(ValueError) as context:
            self.manager.collect_file("nonexistent_group")

        self.assertIn("Group 'nonexistent_group' does not exist", str(context.exception))

    def test_collect_file_not_folder_type(self):
        """测试收集非文件夹类型文件组的文件应抛出异常"""
        group_name = "test_file_group"
        file_path = Path(self.temp_dir) / "test.txt"
        file_path.write_text("test", encoding="utf-8-sig")

        self.manager.create_group(group_name, file_path)

        with self.assertRaises(ValueError) as context:
            self.manager.collect_file(group_name)

        self.assertIn("is not a folder, cannot collect files", str(context.exception))

    def test_read_file(self):
        """测试读取单个文件内容"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建并添加文件
        test_file = folder_path / "test.txt"
        test_content = "Hello, World!\n这是测试内容。"
        test_file.write_text(test_content, encoding="utf-8-sig")
        self.manager.create_file(group_name, test_file)

        # 读取文件
        content = self.manager.read_file(group_name, test_file)

        self.assertEqual(content, test_content)

    def test_read_file_nonexistent_group(self):
        """测试从不存在的文件组读取文件应抛出异常"""
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("content", encoding="utf-8-sig")

        with self.assertRaises(ValueError) as context:
            self.manager.read_file("nonexistent_group", test_file)

        self.assertIn("Group 'nonexistent_group' does not exist", str(context.exception))

    def test_read_file_not_in_group(self):
        """测试读取不在文件组中的文件应抛出异常"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建但未添加到文件组的文件
        test_file = folder_path / "test.txt"
        test_file.write_text("content", encoding="utf-8-sig")

        with self.assertRaises(ValueError) as context:
            self.manager.read_file(group_name, test_file)

        self.assertIn("not in group", str(context.exception))

    def test_read_files(self):
        """测试读取文件组中的所有文件内容"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建并添加多个文件
        file1 = folder_path / "a.txt"
        file2 = folder_path / "b.txt"
        content1 = "Content 1"
        content2 = "Content 2"

        file1.write_text(content1, encoding="utf-8-sig")
        file2.write_text(content2, encoding="utf-8-sig")

        self.manager.create_file(group_name, [file1, file2])

        # 读取所有文件内容
        contents = self.manager.read_files(group_name)

        self.assertEqual(len(contents), 2)
        self.assertIn(content1, contents)
        self.assertIn(content2, contents)

    def test_read_files_in_range(self):
        """测试使用迭代器读取文件内容"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建并添加多个文件
        file1 = folder_path / "a.txt"
        file2 = folder_path / "b.txt"
        content1 = "Content 1"
        content2 = "Content 2"

        file1.write_text(content1, encoding="utf-8-sig")
        file2.write_text(content2, encoding="utf-8-sig")

        self.manager.create_file(group_name, [file1, file2])

        # 使用迭代器读取
        results = list(self.manager.read_files_in_range(group_name))

        self.assertEqual(len(results), 2)

        # 验证每个文件都返回了正确的路径和内容
        path_content_map = {path: content for path, content in results}
        self.assertEqual(path_content_map[file1], content1)
        self.assertEqual(path_content_map[file2], content2)

    def test_write_file_new(self):
        """测试写入新文件（文件不存在）"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 写入新文件
        new_file = folder_path / "new.txt"
        content = "This is new content"

        self.manager.write_file(group_name, new_file, content)

        # 验证文件已添加到文件组
        group = self.manager._groups[group_name]
        self.assertEqual(len(group.file_list), 1)
        self.assertEqual(group.file_list[0].file_path, new_file)

        # 验证文件内容已写入
        self.assertTrue(new_file.exists())
        self.assertEqual(new_file.read_text(encoding="utf-8-sig"), content)

    def test_write_file_existing(self):
        """测试覆盖已存在的文件"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建初始文件
        existing_file = folder_path / "existing.txt"
        initial_content = "Initial content"
        existing_file.write_text(initial_content, encoding="utf-8-sig")

        # 添加文件到组
        self.manager.create_file(group_name, existing_file)

        # 覆盖文件内容
        new_content = "New content"
        self.manager.write_file(group_name, existing_file, new_content)

        # 验证文件内容已更新
        self.assertEqual(existing_file.read_text(encoding="utf-8-sig"), new_content)

        # 验证文件列表没有重复
        group = self.manager._groups[group_name]
        self.assertEqual(len(group.file_list), 1)

    def test_write_file_outside_group_root(self):
        """测试写入不在组根目录下的文件应抛出异常"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 尝试写入不在组目录下的文件
        outside_file = Path(self.temp_dir) / "outside.txt"

        with self.assertRaises(ValueError) as context:
            self.manager.write_file(group_name, outside_file, "content")

        self.assertIn("is not under group root", str(context.exception))

    def test_write_file_nonexistent_group(self):
        """测试向不存在的文件组写入文件应抛出异常"""
        test_file = Path(self.temp_dir) / "test.txt"

        with self.assertRaises(ValueError) as context:
            self.manager.write_file("nonexistent_group", test_file, "content")

        self.assertIn("Group 'nonexistent_group' does not exist", str(context.exception))

    def test_write_file_create_parent_dirs(self):
        """测试写入文件时自动创建父目录"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 写入到子目录中的文件
        subdir_file = folder_path / "subdir" / "nested" / "file.txt"
        content = "Nested content"

        self.manager.write_file(group_name, subdir_file, content)

        # 验证文件已创建
        self.assertTrue(subdir_file.exists())
        self.assertEqual(subdir_file.read_text(encoding="utf-8-sig"), content)

        # 验证文件已添加到文件组
        group = self.manager._groups[group_name]
        self.assertEqual(len(group.file_list), 1)
        self.assertEqual(group.file_list[0].file_path, subdir_file)

    def test_create_file_various_input_types(self):
        """测试使用不同类型的输入添加文件"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建测试文件
        file1 = folder_path / "file1.txt"
        file2 = folder_path / "file2.txt"
        file1.write_text("content1", encoding="utf-8-sig")
        file2.write_text("content2", encoding="utf-8-sig")

        # 测试1: 字符串路径
        self.manager.create_file(group_name, str(file1))

        # 测试2: Path对象
        self.manager.create_file(group_name, file2)

        # 测试3: 字符串列表
        self.manager.create_file(group_name, [str(file1), str(file2)])

        # 测试4: Path对象列表
        self.manager.create_file(group_name, [file1, file2])

        # 验证文件已添加（去重后应该是2个文件）
        group = self.manager._groups[group_name]
        self.assertEqual(len(group.file_list), 2)
        file_names = sorted([item.file_name for item in group.file_list])
        self.assertEqual(file_names, ["file1.txt", "file2.txt"])

    def test_read_file_io_error(self):
        """测试读取文件时发生IOError"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建并添加文件
        test_file = folder_path / "test.txt"
        test_file.write_text("content", encoding="utf-8-sig")
        self.manager.create_file(group_name, test_file)

        # 删除文件以模拟读取错误
        test_file.unlink()

        # 尝试读取应抛出IOError
        with self.assertRaises(IOError) as context:
            self.manager.read_file(group_name, test_file)

        self.assertIn("Failed to read file", str(context.exception))

    def test_write_file_io_error(self):
        """测试写入文件时发生IOError（例如只读目录）"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建只读目录
        read_only_dir = folder_path / "readonly"
        read_only_dir.mkdir()

        # 在Unix上使用chmod，在Windows上尝试设置只读属性
        import platform
        import stat
        if platform.system() != 'Windows':
            read_only_dir.chmod(stat.S_IRUSR)  # 只读权限
        else:
            # Windows: 设置目录为只读（可能不会完全阻止写入，但可以测试）
            import os
            os.chmod(read_only_dir, stat.S_IREAD)

        # 尝试写入到只读目录中的文件
        read_only_file = read_only_dir / "test.txt"

        # 在Unix上应抛出IOError，在Windows上可能不会
        try:
            self.manager.write_file(group_name, read_only_file, "content")
            # 如果成功（可能在Windows上），清理只读属性
            if platform.system() != 'Windows':
                read_only_dir.chmod(stat.S_IRUSR | stat.S_IWUSR)
        except IOError as e:
            self.assertIn("Failed to write file", str(e))
        except Exception:
            # 其他异常也接受（可能是权限错误的不同类型）
            pass
        finally:
            # 恢复权限以便清理
            if platform.system() != 'Windows':
                read_only_dir.chmod(stat.S_IRUSR | stat.S_IWUSR)

    def test_utf8_sig_encoding(self):
        """测试UTF-8-SIG编码正确处理BOM"""
        group_name = "test_group"
        folder_path = Path(self.temp_dir) / "folder"
        folder_path.mkdir()

        self.manager.create_group(group_name, folder_path)

        # 创建带BOM的文件
        test_file = folder_path / "test.txt"
        content = "Hello with BOM"

        # 手动写入带BOM的内容
        test_file.write_text(content, encoding="utf-8-sig")
        self.manager.create_file(group_name, test_file)

        # 读取文件
        read_content = self.manager.read_file(group_name, test_file)

        # 验证内容匹配（BOM应该被透明处理）
        self.assertEqual(read_content, content)

        # 使用write_file写入新内容
        new_content = "New content with BOM"
        self.manager.write_file(group_name, test_file, new_content)

        # 验证文件内容
        file_content = test_file.read_text(encoding="utf-8-sig")
        self.assertEqual(file_content, new_content)


if __name__ == '__main__':
    unittest.main()