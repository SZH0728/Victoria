# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from pyradox import Tree

from core.file import FileManager
from core.datatype.prefix import CountryTagPrefix, StateNamePrefix
from core.transform.base import TransformBase

logger = getLogger(__name__)


class TransformTranslationDefault(TransformBase):
    """
    @brief 翻译数据转换类
    @details 将翻译字典转换为游戏本地化文件格式
    """

    def __init__(self, tag: dict[CountryTagPrefix, StateNamePrefix]):
        """
        @brief 初始化翻译转换类
        @details 调用父类初始化方法，设置标签字典
        @param tag 国家标签到州名称前缀的映射字典
        """
        super().__init__()
        self.tag: dict[CountryTagPrefix, StateNamePrefix] = tag
        logger.debug(f"TransformTranslationDefault initialized with tag dictionary")

    def transform(self, target: Any) -> Tree:
        """
        @brief 转换翻译数据
        @details 翻译转换类使用main方法直接处理翻译字典，此方法保留为空
        @param target 目标数据
        @throws NotImplementedError 此方法未实现，使用main方法替代
        """
        raise NotImplementedError("transform method not implemented for TransformTranslationDefault, use main method instead")

    def main(self, manager: FileManager, group: str, translation: dict[str, dict[str, str]]):
        """
        @brief 主执行方法
        @details 将翻译字典转换为游戏本地化文件并写入文件
        @param manager 文件管理器实例
        @param group 文件组名称
        @param translation 翻译字典，键为文件名，值为国家标签到翻译字符串的映射
        """
        logger.info(f"Starting translation transformation for group '{group}' with {len(translation)} files")

        for filename, translate_dict in translation.items():
            logger.debug(f"Processing translation file: {filename}")

            filename_list: list[str] = filename.split('_')

            if 'l' not in filename_list:
                logger.error(f"Invalid filename format for translation file: {filename}")
                continue

            filename_list: list[str] = filename_list[filename_list.index('l'):]
            headline: str = '_'.join(filename_list)
            logger.debug(f"Extracted headline: {headline}")

            context: str = headline + '\n'
            processed_count = 0

            for country_tag, state_name in self.tag.items():
                country_tag_string: str = country_tag.original_string.upper()

                if country_tag_string not in translate_dict:
                    logger.debug(f"Translation not found for country tag: {country_tag_string}")
                    continue

                translate_string: str = translate_dict[country_tag_string]
                logger.debug(f"Found translation for {country_tag_string}: {translate_string}")

                context += f'{country_tag_string}: {translate_string.lower()}\n'
                context += f'{country_tag_string}_ADJ: {translate_string.lower()}\n'
                processed_count += 1

            output_filename = f'alternative_world_{headline}'
            logger.debug(f"Writing translation file: {output_filename}, processed {processed_count} entries")
            manager.write_file(group, output_filename, context)
            logger.info(f"Translation file written: {output_filename}")

        logger.info(f"Translation transformation completed for group '{group}'")


if __name__ == '__main__':
    pass