# -*- coding:utf-8 -*-
# AUTHOR: Sun
from pyradox import Tree

from core.datatype.prefix import StateNamePurePrefix
from core.analysis.base import AnalysisBase
from core.file import FileManager


class AnalysisTranslationDefault(AnalysisBase):
    def __init__(self):
        super().__init__()

        self.result: dict[str, dict[str, str]] = {}

    def analysis(self, filename: str, context: str):
        """
        @brief 分析翻译文件内容，将键值对存储到结果字典中。
        @details 此方法重写基类的analysis方法，但使用context: str参数而非tree: Tree。
                 这是因为翻译文件是原始文本格式，不需要解析为Tree结构。
                 注意：此方法仅由main方法内部调用，不应通过基类AnalysisBase接口直接调用。
        @param filename 文件名
        @param context 文件内容字符串
        """
        self.result[filename] = {}
        for index, line in enumerate(context.split('\n')):
            if index == 0 or not line:
                continue

            state, state_name = line.strip().split(':')
            state_tag: str = StateNamePurePrefix(str_with_prefix=state).original_string
            state_name: str = state_name.replace('0', '').replace('1', '').strip()

            self.result[filename][state_tag] = state_name

    def main(self, manager: FileManager, group: str):
        for file, context in manager.read_files_in_range(group):
            self.analysis(file.name, context)


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('translate', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\localization'))
    manager.create_file('translate', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\localization\simp_chinese\map\states_l_simp_chinese.yml'))
    manager.create_file('translate', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\localization\english\map\states_l_english.yml'))

    analysis = AnalysisTranslationDefault()
    analysis.main(manager, 'translate')
    print(analysis.result)
