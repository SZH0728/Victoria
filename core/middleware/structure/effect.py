# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from core.datatype.prefix import CountryTagPrefix
from core.datatype.source.effect import EffectFile
from core.datatype.structure.effect import StructuredEffectCountry
from core.middleware.base import StructureBase

logger = getLogger(__name__)


class StructureEffectDefault(StructureBase):
    """
    @brief 效果数据结构化转换类
    @details 将EffectFile字典转换为结构化数据字典
    转换逻辑: dict[str, EffectFile] → dict[CountryTagPrefix, StructuredEffectCountry]
    注意: 效果数据结构未发生变更，StructuredEffectCountry = EffectCountry
    """
    def convert(self, source_dict: dict[str, EffectFile]) -> dict[CountryTagPrefix, StructuredEffectCountry]:
        """
        @brief 转换效果源数据为结构化数据
        @param source_dict 源数据字典，键为文件名，值为EffectFile对象
        @return 结构化数据字典，键为国家标签，值为EffectCountry对象
        """
        result: dict[CountryTagPrefix, StructuredEffectCountry] = {}
        for filename, effect_file in source_dict.items():
            logger.debug(f"Processing file: {filename}")

            for country_tag, effect_country in effect_file.effect_country_dict.items():
                if country_tag not in result:
                    result[country_tag] = effect_country
                else:
                    logger.warning(f"Country effect '{country_tag}' already exists in result")
        return result


if __name__ == '__main__':
    pass