# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from core.datatype.prefix import CountryTagPrefix
from core.datatype.source.definition import DefinitionFile
from core.datatype.structure.definition import StructuredDefinitionCountry
from core.middleware.base import StructureBase

logger = getLogger(__name__)


class StructureDefinition(StructureBase):
    """
    @brief 国家定义数据结构化转换类
    @details 将DefinitionFile字典转换为结构化数据字典
    转换逻辑: dict[str, DefinitionFile] → dict[CountryTagPrefix, StructuredDefinitionCountry]
    注意: 国家定义数据结构未发生变更，StructuredDefinitionCountry = DefinitionCountry
    """
    def convert(self, source_dict: dict[str, DefinitionFile]) -> dict[CountryTagPrefix, StructuredDefinitionCountry]:
        """
        @brief 转换国家定义源数据为结构化数据
        @param source_dict 源数据字典，键为文件名，值为DefinitionFile对象
        @return 结构化数据字典，键为国家标签，值为DefinitionCountry对象
        """
        result: dict[CountryTagPrefix, StructuredDefinitionCountry] = {}
        for filename, definition_file in source_dict.items():
            logger.debug(f"Processing file: {filename}")

            for country_tag, definition_country in definition_file.definition_country_dict.items():
                if country_tag not in result:
                    result[country_tag] = definition_country
                else:
                    logger.warning(f"Country definition '{country_tag}' already exists in result, skipping duplicate")
        return result


if __name__ == '__main__':
    pass