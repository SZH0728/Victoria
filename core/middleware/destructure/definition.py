# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from core.datatype.prefix import CountryTagPrefix
from core.datatype.source.definition import DefinitionFile
from core.datatype.structure.definition import StructuredDefinitionCountry
from core.middleware.base import DestructureBase

logger = getLogger(__name__)


class DestructureDefinition(DestructureBase):
    """
    @brief 国家定义数据解构转换类
    @details 将结构化国家定义数据字典转换回DefinitionFile字典
    转换逻辑: dict[CountryTagPrefix, StructuredDefinitionCountry] → dict[str, DefinitionFile]
    """
    def convert(self, structure_dict: dict[CountryTagPrefix, StructuredDefinitionCountry]) -> dict[str, DefinitionFile]:
        """
        @brief 转换结构化数据回源数据
        @param structure_dict 结构化数据字典，键为国家标签，值为DefinitionCountry对象
        @return 源数据字典，键为文件名，值为DefinitionFile对象
        """
        result: dict[str, DefinitionFile] = {}
        filename = "80_country_definitions.txt"
        result[filename] = DefinitionFile(root_key=None,definition_country_dict=structure_dict)
        return result


if __name__ == '__main__':
    pass