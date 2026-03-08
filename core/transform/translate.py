# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any
from logging import getLogger

from pyradox import Tree

from core.file import FileManager
from core.datatype.prefix import CountryTagPrefix, StateNamePrefix
from core.transform.base import TransformBase

logger = getLogger(__name__)


class TranslateTransform(TransformBase):
    def __init__(self):
        super().__init__()

        self.tag: dict[CountryTagPrefix, StateNamePrefix] | None = None
    def transform(self, target: Any) -> Tree:
        pass

    def main(self, manager: FileManager, group: str, translation: dict[str, dict[str, str]]):
        for filename, context in translation.items():
            headline: list[str] = filename.split('_')
            headline: list[str] = headline[headline.index('l'):]
            headline: str = '_'.join(headline)

            context: str = headline + '\n'

            for country_tag, state_name in self.tag.items():
                context += f'{country_tag.original_string.upper()}: {state_name.prefix_string.lower()}\n'
                context += f'{country_tag.original_string.upper()}_ADJ: {state_name.prefix_string.lower()}\n'

            manager.write_file(group, f'alternative_world_{headline}', context)


if __name__ == '__main__':
    pass