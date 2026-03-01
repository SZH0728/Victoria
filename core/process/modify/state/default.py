# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any

from core.datatype.map import Map
from core.process.modify.state.base import StateModifyBase


class StateModifyDefault(StateModifyBase):
    def modify(self) -> Any:
        country_state_map: Map[list[str]] = Map()
        country_name_map: Map[str] = Map()
        tag_map: Map[str] = Map()

        for effect in self.origin.effect.values():
            tag_map[effect.country_tag] = effect.country_name
            country_name_map[effect.country_name] = effect.country_tag

        for state in self.origin.state.values():
            for country in state.country:
                country_tag = country.country_tag

                if country_tag in country_state_map:
                    country_state_map[country_tag].append(state.state_name)
                else:
                    country_state_map[country_tag] = [state.state_name]

        self.middle['country_state'] = country_state_map
        self.middle['country_name'] = country_name_map
        self.middle['tag'] = tag_map

        return self.origin.state

if __name__ == '__main__':
    pass
