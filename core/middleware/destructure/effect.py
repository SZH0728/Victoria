# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from core.datatype.prefix import CountryTagPrefix
from core.datatype.source.effect import EffectFile
from core.datatype.structure.effect import StructuredEffectCountry
from core.middleware.base import DestructureBase

logger = getLogger(__name__)


class DestructureEffectDefault(DestructureBase):
    """
    @brief 效果数据解构转换类
    @details 将结构化效果数据字典转换回EffectFile字典
    转换逻辑: dict[CountryTagPrefix, StructuredEffectCountry] → dict[str, EffectFile]
    """
    def convert(self, structure_dict: dict[CountryTagPrefix, StructuredEffectCountry]) -> dict[str, EffectFile]:
        """
        @brief 转换结构化数据回源数据
        @param structure_dict 结构化数据字典，键为国家标签，值为EffectCountry对象
        @return 源数据字典，键为文件名，值为EffectFile对象
        """
        result: dict[str, EffectFile] = {}
        filename = "country_effects.txt"
        result[filename] = EffectFile(root_key='COUNTRIES',effect_country_dict=structure_dict)
        return result


if __name__ == '__main__':
    pass