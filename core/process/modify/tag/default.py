# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.process.modify.tag.default
@brief 标签默认修改器模块
@details 默认标签修改器，直接返回中间数据中的标签映射
"""

from typing import Any

from core.process.modify.tag.base import TagModifyBase


class TagModifyDefault(TagModifyBase):
    """!
    @brief 标签默认修改器
    @details 默认实现，直接返回中间数据中的标签映射，不做任何修改
    """
    def modify(self) -> Any:
        """!
        @brief 执行标签修改
        @details 直接返回中间数据中的标签映射，不做任何处理

        @return 标签映射 Map[str]
        """
        return self.middle['tag']

if __name__ == '__main__':
    pass
