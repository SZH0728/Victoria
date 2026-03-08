# -*- coding:utf-8 -*-
# AUTHOR: Sun
from logging import getLogger

from core.datatype.prefix import StateNamePurePrefix
from core.analysis.base import AnalysisBase
from core.file import FileManager

logger = getLogger(__name__)


class AnalysisTranslationDefault(AnalysisBase):
    """
    @brief 翻译数据分析类
    @details 分析维多利亚3游戏中的翻译文件，提取州名称的本地化映射关系
    """
    def __init__(self):
        """
        @brief 初始化翻译数据分析类
        @details 调用父类初始化方法，设置结果字典类型
        """
        super().__init__()
        self.result: dict[str, dict[str, str]] = {}
        logger.debug(f"AnalysisTranslationDefault initialized with empty result dict")

    def analysis(self, filename: str, context: str):
        """
        @brief 分析翻译文件内容，将键值对存储到结果字典中。
        @details 此方法重写基类的analysis方法，但使用context: str参数而非tree: Tree。
                 这是因为翻译文件是原始文本格式，不需要解析为Tree结构。
                 注意：此方法仅由main方法内部调用，不应通过基类AnalysisBase接口直接调用。
        @param filename 文件名
        @param context 文件内容字符串
        """
        logger.debug(f"Starting translation analysis for file '{filename}'")
        self.result[filename] = {}
        lines: list[str] = context.split('\n')
        logger.debug(f"Processing {len(lines)} lines in translation file")

        for index, line in enumerate(lines):
            if index == 0 or not line:
                continue

            try:
                state, state_name = line.strip().split(':')
                state_tag: str = StateNamePurePrefix(str_with_prefix=state).original_string
                state_name: str = state_name.replace('0', '').replace('1', '').strip()

                self.result[filename][state_tag] = state_name
                logger.debug(f"Added translation: {state_tag} -> {state_name}")
            except ValueError as e:
                logger.warning(f"Failed to parse line {index} in file '{filename}': {line.strip()} - {e}")

        logger.info(f"Translation analysis completed for file '{filename}'")

    def main(self, manager: FileManager, group: str):
        """
        @brief 主执行方法
        @details 遍历文件组中的所有翻译文件，直接处理文件内容而不进行Tree解析
        @param manager 文件管理器实例
        @param group 文件组名称
        """
        logger.info(f"Starting translation analysis for group '{group}'")

        for file, context in manager.read_files_in_range(group):
            logger.debug(f"Processing translation file: '{file.name}'")
            self.analysis(file.name, context)

        logger.info(f"Translation analysis completed for group '{group}'")


if __name__ == '__main__':
    from pathlib import Path

    manager = FileManager()
    manager.create_group('translate', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\localization'))
    manager.create_file('translate', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\localization\simp_chinese\map\states_l_simp_chinese.yml'))
    manager.create_file('translate', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\localization\english\map\states_l_english.yml'))

    analysis = AnalysisTranslationDefault()
    analysis.main(manager, 'translate')
    print(analysis.result)
