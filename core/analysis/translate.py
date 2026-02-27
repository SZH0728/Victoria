# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from core.file import FileManager
from core.datatype import Map
from core.analysis.extract import KeyExtractionMixin

logger = getLogger(__name__)


class TranslateAnalysis(KeyExtractionMixin):
    """!
    @brief 翻译分析类
    @details 提供本地化文件翻译分析功能
    """
    STATE_KEY_PREFIX = 'STATE_'

    def __init__(self):
        """!
        @brief 初始化翻译分析器
        """
        self.translation = Map[str]()
        logger.info("Translation analysis initialized")


    def main(self, manager: FileManager, group: str, filename: str):
        """!
        @brief 主分析流程，读取翻译文件并进行分析
        @details 解析本地化文件，提取州标志和州名称的映射
        @param manager 文件管理器实例
        @param group 文件组名称
        @param filename 文件名
        """
        logger.info(f"Starting translation analysis for file '{filename}' in group '{group}'")
        content = manager.read_file(group, filename).split('\n')
        logger.debug(f"Read {len(content)} lines from file")

        for index, i in enumerate(content):
            if index == 0 or not i:
                continue

            state_flag, state_name = i.strip().split(':')
            state_flag = self.get_state_name_by_key(state_flag).strip()
            state_name = state_name.replace('0', '').replace('1', '').strip()
            logger.debug(f"Extracted translation: {state_flag} -> {state_name}")

            self.translation[state_flag] = state_name

        logger.info(f"Completed translation analysis for file '{filename}'")


if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('translate', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\localization'))
    manager.create_file('translate', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\localization\simp_chinese\map\states_l_simp_chinese.yml'))
    manager.create_file('translate', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\localization\english\map\states_l_english.yml'))

    chinese = TranslateAnalysis()
    chinese.main(manager, 'translate', 'states_l_simp_chinese.yml')

    english = TranslateAnalysis()
    english.main(manager, 'translate', 'states_l_english.yml')

    print(chinese.translation)
    print(english.translation)
