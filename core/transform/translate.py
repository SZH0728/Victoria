# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger
from pathlib import Path

from core.file import FileManager
from core.datatype import Map

logger = getLogger(__name__)


class TranslateTransform(object):
    """!
    @brief 翻译转换器
    @details 将翻译映射转换为游戏可读的本地化文件格式
    """

    @staticmethod
    def main(manager: FileManager, group: str, filename: str | Path, headline: str, translation: Map[str], tag: Map[str]):
        """!
        @brief 主转换流程，生成翻译文件
        @details 根据标签映射和翻译映射生成本地化条目，每个标签生成KEY和KEY_ADJ两行
                格式示例：对于标签"USA"映射到值"United States"，生成：
                USA: 美利坚合众国
                USA_ADJ: 美利坚合众国

        @param manager 文件管理器实例，用于写入文件
        @param group 文件组名称，指定输出到哪个文件组
        @param filename 输出文件名（可以是字符串或Path对象）
        @param headline 文件头部内容，如语言标识符"l_english:"或"l_simp_chinese:"
        @param translation 翻译映射，键为原始值（如"United States"），值为翻译文本（如"美利坚合众国"）
        @param tag 标签映射，键为国家标签（如"USA"），值为对应的原始值（如"United States"）

        @note 只有tag中的值存在于translation中时才会生成对应的翻译条目
        """
        content: str = headline + '\n'
        for key, value in tag.items():
            if value not in translation:
                continue

            translate: str = translation[value]

            content += f' {key.upper()}: {translate}\n'
            content += f' {key.upper()}_ADJ: {translate}\n'

        manager.write_file(group, filename, content)

if __name__ == '__main__':
    pass
