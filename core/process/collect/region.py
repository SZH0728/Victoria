# -*- coding:utf-8 -*-
# AUTHOR: Sun

from typing import Any

from core.datatype.map import Map
from core.datatype.state import StateInRegion
from core.process.collect.base import CollectBase

class StateInRegionOrder(CollectBase):
    def collect(self) -> list[tuple[str, Any]]:
        water: set[str] = set()
        state_to_region: dict[str, str] = {}

        for region in self.origin.region.water:
            for name in region.states:
                water.add(name)

        for continent in self.origin.region.values():
            for region in continent:
                for name in region.states:
                    if name in water:
                        continue

                    state_to_region[name] = region.region_name

        state_map: Map[Map[StateInRegion]] = Map()
        for state in self.origin.state.values():
            if state.state_name in water:
                continue

            provinces: list[str] = []

            for country in state.country:
                provinces.extend(country.provinces)

            state_id = self.origin.map[state.state_name]

            region = state_to_region[state.state_name]
            if region not in state_map:
                state_map[region] = Map()

            state_item = StateInRegion(
                state_id=state_id,
                state_name=state.state_name,
                region_name=region,
                provinces=provinces,
                homeland=list(state.homeland),
                claim=list(state.claim),
            )
            state_map[region][state.state_name] = state_item

        return [('state_in_region', state_map)]


if __name__ == '__main__':
    pass
