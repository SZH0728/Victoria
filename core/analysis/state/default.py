# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from pyradox import Tree

from core.datatype import CountryState, State
from core.analysis.state.base import StateAnalysisBase

logger = getLogger(__name__)


class StateAnalysisDefault(StateAnalysisBase):
    def analysis_country(self, tree: Tree, state_name: str) -> CountryState:
        country_tag: str = ''
        provinces: list[str] = []
        state_type: str | None = None

        for key, value in tree.items():
            if key == 'country':
                country_tag = self.get_country_tag_by_key(value)
            elif key == 'owned_provinces':
                provinces.append(value)
            elif key == 'state_type':
                state_type = value
            else:
                logger.warning(f"Unknown key '{key}' in state '{state_name}/{country_tag}'")

        country = CountryState(
            state_name=state_name,
            country_tag=country_tag,
            provinces=tuple(provinces),
            state_type=state_type
        )

        return country


    def analysis(self, tree: Tree, state_name: str) -> State:
        country: list[CountryState] = []
        homeland: list[str] = []
        claim: list[str] = []

        for key, value in tree.items():
            if key == 'create_state':
                country.append(self.analysis_country(value, state_name))
            elif key == 'add_homeland':
                homeland.append(value)
            elif key == 'add_claim':
                claim.append(value)
            else:
                logger.warning(f"Unknown key '{key}' in state '{state_name}'")

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
