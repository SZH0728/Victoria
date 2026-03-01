# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from pyradox import Tree

from core.datatype import CountryState, State
from core.analysis.state.base import StateAnalysisBase

logger = getLogger(__name__)


class StateAnalysisDefault(StateAnalysisBase):
    """!
    @brief 默认州分析器
    @details 实现具体的州分析逻辑，解析州树结构
    """
    def analysis_country(self, tree: Tree, state_name: str) -> CountryState:
        """!
        @brief 分析国家州树，提取国家州数据
        @details 遍历树中的每个节点，提取国家标签、省份列表和州类型信息
        @param tree pyradox解析的树结构
        @param state_name 州名称
        @return 国家州对象
        """
        logger.debug(f"Analyzing country state for state '{state_name}'")
        country_tag: str = ''
        provinces: list[str] = []
        state_type: str | None = None

        for key, value in tree.items():
            if isinstance(value, Tree):
                value = str(value)

            if key == 'country':
                country_tag = self.extract_country_tag_from_key(value)
            elif key == 'owned_provinces':
                provinces.append(value)
            elif key == 'state_type':
                state_type = value
            else:
                logger.warning(f"Unknown key '{key}' in state '{state_name}/{country_tag}'")

        logger.debug(f"Created country state for '{state_name}' with tag '{country_tag}'")
        country = CountryState(
            state_name=state_name,
            country_tag=country_tag,
            provinces=tuple(provinces),
            state_type=state_type
        )

        return country


    def analysis(self, tree: Tree, state_name: str) -> State:
        """!
        @brief 分析州树，提取州数据
        @details 遍历树中的每个节点，提取国家州列表、家园文化和宣称信息
        @param tree pyradox解析的树结构
        @param state_name 州名称
        @return 州对象
        """
        logger.debug(f"Analyzing state '{state_name}'")
        country: list[CountryState] = []
        homeland: list[str] = []
        claim: list[str] = []

        for key, value in tree.items():
            if key == 'create_state':
                country.append(self.analysis_country(value, state_name))
            elif key == 'add_homeland':
                homeland.append(self.extract_culture_name_from_key(str(value) if isinstance(value, Tree) else value))
            elif key == 'add_claim':
                claim.append(self.extract_country_tag_from_key(str(value) if isinstance(value, Tree) else value))
            else:
                if isinstance(value, Tree):
                    logger.warning(f"Unknown key '{key}' in state '{state_name}', value converted from Tree to string")
                else:
                    logger.warning(f"Unknown key '{key}' in state '{state_name}'")

        logger.debug(f"Created state '{state_name}' with {len(country)} countries")
        state = State(
            state_name=state_name,
            country=country,
            homeland=tuple(homeland),
            claim=tuple(claim)
        )

        return state

if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('state', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\states'))
    manager.collect_file('state', '.txt')

    analysis = StateAnalysisDefault()
    analysis.main(manager, 'state')
    print(analysis.state)
