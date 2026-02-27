# -*- coding:utf-8 -*-
# AUTHOR: Sun

from logging import getLogger

from pyradox import Tree

from core.datatype import BuildingCountryOwnership, BuildingPrivateOwnership, BuildingCompanyOwnership, BuildingItem, BuildingNoOwnerItem, CountryBuilding, StateBuilding
from core.analysis.building.base import BuildingAnalysisBase

logger = getLogger(__name__)


class BuildingAnalysisDefault(BuildingAnalysisBase):
    """!
    @brief 默认建筑分析器
    @details 实现具体的建筑分析逻辑，解析建筑树结构
    """
    def analysis_country_ownership(self, tree: Tree) -> BuildingCountryOwnership:
        """!
        @brief 分析国家所有权树，提取国家所有权数据
        @details 遍历树中的每个节点，提取国家标签和等级信息
        @param tree pyradox解析的树结构
        @return 国家所有权对象
        """
        logger.debug("Analyzing country ownership")
        country: str = ''
        level: int = 0

        for key, value in tree.items():
            if key == 'country':
                country = self.get_country_tag_by_value(value)
            elif key == 'levels':
                level = value
            else:
                logger.warning(f"Unknown key '{key}' in building ownership {country}")

        logger.debug(f"Created country ownership for '{country}' with level {level}")
        ownership = BuildingCountryOwnership(
            country=country,
            level=level
        )
        return ownership

    def analysis_private_ownership(self, tree: Tree) -> BuildingPrivateOwnership:
        """!
        @brief 分析私有所有权树，提取私有所有权数据
        @details 遍历树中的每个节点，提取建筑类型、国家标签、等级和区域信息
        @param tree pyradox解析的树结构
        @return 私有所有权对象
        """
        logger.debug("Analyzing private ownership")
        building: str = ''
        country: str = ''
        level: int = 0
        region: str = ''

        for key, value in tree.items():
            if key == 'type':
                building = value
            elif key == 'country':
                country = self.get_country_tag_by_value(value)
            elif key == 'levels':
                level = value
            elif key == 'region':
                region = value
            else:
                logger.warning(f"Unknown key '{key}' in building ownership {building}")

        logger.debug(f"Created private ownership for building '{building}', country '{country}', level {level}, region '{region}'")
        ownership = BuildingPrivateOwnership(
            building=building,
            country=country,
            level=level,
            region=region
        )
        return ownership

    def analysis_company_ownership(self, tree: Tree) -> BuildingCompanyOwnership:
        """!
        @brief 分析公司所有权树，提取公司所有权数据
        @details 遍历树中的每个节点，提取公司类型、国家标签和等级信息
        @param tree pyradox解析的树结构
        @return 公司所有权对象
        """
        logger.debug("Analyzing company ownership")
        company: str = ''
        country: str = ''
        level: int = 0

        for key, value in tree.items():
            if key == 'type':
                company = value
            elif key == 'country':
                country = self.get_country_tag_by_value(value)
            elif key == 'levels':
                level = value
            else:
                logger.warning(f"Unknown key '{key}' in building ownership {company}")

        logger.debug(f"Created company ownership for company '{company}', country '{country}', level {level}")
        ownership = BuildingCompanyOwnership(
            company=company,
            country=country,
            level=level
        )

        return ownership

    def analysis_ownership(self, tree: Tree) -> list[BuildingCountryOwnership|BuildingPrivateOwnership|BuildingCompanyOwnership]:
        """!
        @brief 分析所有权树，提取所有权列表
        @details 遍历树中的每个节点，根据键类型调用相应的所有权分析方法
        @param tree pyradox解析的树结构
        @return 所有权对象列表
        """
        logger.debug("Analyzing ownership tree")
        ownership: list[BuildingCountryOwnership|BuildingPrivateOwnership|BuildingCompanyOwnership] = []

        for key, value in tree.items():
            if key == 'building':
                ownership.append(self.analysis_private_ownership(value))
            elif key == 'country':
                ownership.append(self.analysis_country_ownership(value))
            elif key == 'company':
                ownership.append(self.analysis_company_ownership(value))
            else:
                logger.warning(f"Unknown key '{key}' in building ownership")

        return ownership

    def analysis_building(self, tree: Tree) -> BuildingItem:
        """!
        @brief 分析建筑树，提取建筑项数据
        @details 遍历树中的每个节点，提取建筑类型、所有权列表、补贴、储备和生产方法信息
        @param tree pyradox解析的树结构
        @return 建筑项对象
        """
        logger.debug("Analyzing building tree")
        building: str = ''
        ownership: list[BuildingCountryOwnership|BuildingPrivateOwnership|BuildingCompanyOwnership] = []
        subsidized: str | None = None
        reserve: int | None = None
        methods: list[str] = []

        for key, value in tree.items():
            if key == 'building':
                building = value
            elif key == 'add_ownership':
                ownership.extend(self.analysis_ownership(value))
            elif key == 'subsidized':
                subsidized = value
            elif key == 'reserves':
                reserve = value
            elif key == 'activate_production_methods':
                methods.append(value)
            else:
                logger.warning(f"Unknown key '{key}' in building {building}")

        logger.debug(f"Created building item for '{building}' with {len(ownership)} ownerships")
        building_item = BuildingItem(
            building=building,
            ownership=tuple(ownership),
            subsidized=subsidized,
            reserve=reserve,
            methods=tuple(methods)
        )
        return building_item

    def analysis_no_owner_building(self, tree: Tree) -> BuildingNoOwnerItem:
        """!
        @brief 分析无所有者建筑树，提取无所有者建筑项数据
        @details 遍历树中的每个节点，提取建筑类型和等级信息
        @param tree pyradox解析的树结构
        @return 无所有者建筑项对象
        """
        logger.debug("Analyzing no-owner building tree")
        building: str = ''
        level: int = 0

        for key, value in tree.items():
            if key == 'building':
                building = value
            elif key == 'level':
                level = value
            else:
                logger.warning(f"Unknown key '{key}' in building {building}")

        logger.debug(f"Created no-owner building item for '{building}' with level {level}")
        building_item = BuildingNoOwnerItem(
            building=building,
            level=level
        )
        return building_item

    def analysis_country(self, tree: Tree, tag: str) -> CountryBuilding:
        """!
        @brief 分析国家建筑树，提取国家建筑数据
        @details 遍历树中的每个节点，根据节点类型调用相应的建筑分析方法
        @param tree pyradox解析的树结构
        @param tag 国家标签
        @return 国家建筑对象
        """
        logger.debug(f"Analyzing country building tree for tag '{tag}'")
        buildings: list[BuildingItem|BuildingNoOwnerItem] = []

        for key, value in tree.items():
            if key == 'create_building' or key == 'if':
                if key == 'if':
                    value = value['create_building']

                if 'level' in value.keys():
                    buildings.append(self.analysis_no_owner_building(value))
                else:
                    buildings.append(self.analysis_building(value))
            else:
                logger.warning(f"Unknown key '{key}' in country {tag}")

        logger.debug(f"Created country building for tag '{tag}' with {len(buildings)} buildings")
        country_building = CountryBuilding(
            country_tag=tag,
            buildings=tuple(buildings)
        )
        return country_building

    def analysis(self, tree: Tree, state_name: str) -> StateBuilding:
        """!
        @brief 分析建筑树，提取州建筑数据
        @details 遍历树中的每个节点，根据键前缀调用相应的国家建筑分析方法
        @param tree pyradox解析的树结构
        @param state_name 州名称
        @return 州建筑对象
        """
        logger.debug(f"Analyzing building tree for state '{state_name}'")
        country_building: list[CountryBuilding] = []

        if state_name == 'if':
            for key, value in tree.items():
                if key.startswith('s:'):
                    tree = value
                    break

        for key, value in tree.items():
            if key.startswith('region_state:'):
                country_tag = self.get_country_tag_by_key(key)
                country_building.append(self.analysis_country(value, country_tag))
            else:
                logger.warning(f"Unknown key '{key}' in state {state_name}")

        logger.debug(f"Created state building for state '{state_name}' with {len(country_building)} countries")
        state_building = StateBuilding(
            state=state_name,
            country=tuple(country_building)
        )
        return state_building

if __name__ == '__main__':
    from pathlib import Path

    from core.file import FileManager

    manager = FileManager()
    manager.create_group('building', Path(r'D:\application\Steam\steamapps\common\Victoria 3\game\common\history\buildings'))
    manager.collect_file('building', '.txt')

    analysis = BuildingAnalysisDefault()
    analysis.main(manager, 'building')
    print(analysis.building)
