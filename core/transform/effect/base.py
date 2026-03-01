# -*- coding:utf-8 -*-
# AUTHOR: Sun

from abc import ABC, abstractmethod
from logging import getLogger

from pyradox import Tree

from core.file import FileManager
from core.datatype import Map, CountryEffect
from core.transform.combine import KeyCombinationMixin

logger = getLogger(__name__)


class EffectTransformBase(KeyCombinationMixin, ABC):
    """!
    @brief 效果转换抽象基类
    @details 提供效果数据转换的通用框架，子类需实现具体的转换逻辑
    """


    @abstractmethod
    def transform(self, country_effect: CountryEffect) -> Tree:
        """!
        @brief 转换国家效果对象为pyradox树
        @param country_effect 国家效果对象
        @return 转换后的树
        """
        pass

    def main(self, manager: FileManager, group: str, effect_map: Map[CountryEffect]):
        """!
        @brief 主转换流程，将国家效果映射写入文件
        @details 构建COUNTRIES顶层结构，转换每个国家效果并写入文件。
                 文件名根据国家标签和国家名称自动生成
        @param manager 文件管理器实例
        @param group 文件组名称
        @param effect_map 国家效果映射
        """
        for country_effect in effect_map.values():
            tree = Tree()
            tree['COUNTRIES'] = Tree()

            country_key = self.combine_country_key_for_c(country_effect.country_tag)
            tree['COUNTRIES'][country_key] = self.transform(country_effect)

            content = str(tree)
            lines = content.splitlines(keepends=True)
            for i, line in enumerate(lines):
                if line.lstrip().startswith('c:') and '=' in line and '{' in line:
                    # 替换第一个 = 为 ?=
                    lines[i] = line.replace('=', '?=', 1)
            content = ''.join(lines)

            content = content.replace('"{', '{').replace('}"', '}')

            filename = f'{country_effect.country_tag.lower()} - {country_effect.country_name.lower()}.txt'
            manager.write_file(group, filename, content)


if __name__ == '__main__':
    pass