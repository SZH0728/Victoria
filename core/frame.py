# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""!
@package core.frame
@brief 维多利亚3数据分析框架模块
@details 提供游戏数据分析、处理、转换的完整流程框架
"""

from typing import Any
from logging import getLogger
from enum import Enum
from pathlib import Path

from core.analysis import RegionAnalysisBase, StateAnalysisBase, PopulationAnalysisBase, BuildingAnalysisBase, DefinitionAnalysisBase, EffectAnalysisBase
from core.datatype.combination import DataCombination, DataGenerateType
from core.file import FileManager

from core.analysis.building import BUILDING_ANALYSIS_LIST
from core.analysis.definition import DEFINITION_ANALYSIS_LIST
from core.analysis.effect import EFFECT_ANALYSIS_LIST
from core.analysis.population import POPULATION_ANALYSIS_LIST
from core.analysis.region import REGION_ANALYSIS_LIST
from core.analysis.state import STATE_ANALYSIS_LIST
from core.analysis.map import MapAnalysis
from core.analysis.translate import TranslateAnalysis

from core.process.collect import COLLECT_LIST, COLLECT_DEPENDENCY
from core.process.collect.base import CollectBase

from core.process.modify.base import ModifyBase
from core.process.modify.building import BUILDING_MODIFY_LIST, BUILDING_MODIFY_DEPENDENCY
from core.process.modify.definition import DEFINITION_MODIFY_LIST, DEFINITION_MODIFY_DEPENDENCY
from core.process.modify.effect import EFFECT_MODIFY_LIST, EFFECT_MODIFY_DEPENDENCY
from core.process.modify.population import POPULATION_MODIFY_LIST, POPULATION_MODIFY_DEPENDENCY
from core.process.modify.state import STATE_MODIFY_LIST, STATE_MODIFY_DEPENDENCY
from core.process.modify.tag import TAG_MODIFY_LIST, TAG_MODIFY_DEPENDENCY

from core.transform.building import  BUILDING_TRANSFORM_LIST, BuildingTransformBase
from core.transform.definition import DefinitionTransformBase, DEFINITION_TRANSFORM_LIST
from core.transform.effect import EffectTransformBase, EFFECT_TRANSFORM_LIST
from core.transform.population import POPULATION_TRANSFORM_LIST, PopulationTransformBase
from core.transform.state import STATE_TRANSFORM_LIST, StateTransformBase
from core.transform.translate import TranslateTransform

logger = getLogger(__name__)


class Analysis(Enum):
    """!
    @brief 分析类型枚举
    @details 定义可用的数据分析类型及其执行顺序
    """
    region = 0      #!< 区域分析
    state = 1       #!< 州分析
    population = 2  #!< 人口分析
    building = 3    #!< 建筑分析
    definition = 4  #!< 国家定义分析
    effect = 5      #!< 国家效果分析


class Modify(Enum):
    """!
    @brief 修改器类型枚举
    @details 定义可用的数据修改类型及其执行顺序
    """
    state = 0       #!< 州修改器
    population = 1  #!< 人口修改器
    building = 2    #!< 建筑修改器
    definition = 3  #!< 国家定义修改器
    effect = 4      #!< 国家效果修改器
    tag = 5         #!< 标签修改器


class Transform(Enum):
    """!
    @brief 转换器类型枚举
    @details 定义可用的数据转换类型及其执行顺序
    """
    state = 1       #!< 州转换器
    population = 2  #!< 人口转换器
    building = 3    #!< 建筑转换器
    definition = 4  #!< 国家定义转换器
    effect = 5      #!< 国家效果转换器


class Frame(object):
    """!
    @brief 维多利亚3数据分析框架主类
    @details 负责协调数据分析、收集、修改和转换的完整流程，提供配置接口和执行引擎
    """
    def __init__(self, original_file_root: Path, target_file_root: Path):
        """!
        @brief 初始化框架
        @details 设置原始文件路径和目标文件路径，初始化所有数据容器和默认处理流程

        @param original_file_root 原始游戏文件根目录（Steam安装目录下的Victoria 3目录）
        @param target_file_root 目标文件根目录（Mod输出目录）
        """
        self.original_file_root = original_file_root
        self.target_file_root = target_file_root

        self._origin: DataCombination = DataCombination()
        self._target: DataCombination = DataCombination()

        self._middle: dict[str, Any] = {}

        self._cover_file_group: dict[str, str] = {}
        self._manager: FileManager | None = None
        self.reset_file_manager()

        self._analysis_order: list[Any] = [None for _ in range(6)]

        self._collect_order: list[Any] = []
        self._exist_collect_name: set[str] = set()

        self._modify_order: list[Any] = [None for _ in range(6)]

        self._transform_order: list[Any] = [None for _ in range(5)]

    def reset_file_manager(self):
        """!
        @brief 重置文件管理器
        @details 创建并配置FileManager实例，设置所有必要的文件组，包括：
                 - 原始数据文件组（region, state, population, building, definition, effect）
                 - 目标数据文件组（new_state, new_population等）
                 - 翻译文件组
                 - 文件覆盖映射关系
        """
        self._manager = FileManager()

        self._manager.create_group('region', self.original_file_root / r'game\common\strategic_regions')
        self._manager.create_group('state', self.original_file_root / r'game\common\history\states')
        self._manager.create_group('population', self.original_file_root / r'game\common\history\pops')
        self._manager.create_group('building', self.original_file_root / r'game\common\history\buildings')
        self._manager.create_group('definition', self.original_file_root / r'game\common\country_definitions')
        self._manager.create_group('effect', self.original_file_root / r'game\common\history\countries')
        self._manager.create_group('map', self.original_file_root / r'game\map_data\state_regions')

        self._manager.collect_file('region', '.txt')
        self._manager.collect_file('state', '.txt')
        self._manager.collect_file('population', '.txt')
        self._manager.collect_file('building', '.txt')
        self._manager.collect_file('definition', '.txt')
        self._manager.collect_file('effect', '.txt')
        self._manager.collect_file('map', '.txt')

        self._manager.create_group('new_state', self.target_file_root / r'common\history\states')
        self._manager.create_group('new_population', self.target_file_root / r'common\history\pops')
        self._manager.create_group('new_building', self.target_file_root / r'common\history\buildings')
        self._manager.create_group('new_definition', self.target_file_root / r'common\country_definitions')
        self._manager.create_group('new_effect', self.target_file_root / r'common\history\countries')

        self._cover_file_group['state'] = 'new_state'
        self._cover_file_group['population'] = 'new_population'
        self._cover_file_group['building'] = 'new_building'

        self._manager.create_group('translate', self.original_file_root / r'game\localization')
        self._manager.create_group('new_translate', self.target_file_root / r'localization')
        self._manager.create_file('translate', self.original_file_root / r'game\localization\simp_chinese\map\states_l_simp_chinese.yml')
        self._manager.create_file('translate', self.original_file_root / r'game\localization\english\map\states_l_english.yml')

    def cover_file_generator(self):
        """!
        @brief 生成覆盖文件
        @details 为需要覆盖的文件组创建空的覆盖文件
        @details 处理以下文件组：state → new_state, population → new_population, building → new_building
        """
        for old_group, new_group in self._cover_file_group.items():
            file_list: list[Path] = self._manager.list_file(old_group)

            for file in file_list:
                self._manager.write_file(new_group, file.name, '')

    def set_analysis(self, analysis: Analysis, name: str):
        """!
        @brief 设置分析器配置
        @details 根据分析器类型和名称配置对应的分析器，替换默认分析器

        @param analysis 分析器类型枚举值
            - Analysis.region: 区域分析器
            - Analysis.state: 州分析器
            - Analysis.population: 人口分析器
            - Analysis.building: 建筑分析器
            - Analysis.definition: 国家定义分析器
            - Analysis.effect: 国家效果分析器

        @param name 分析器名称，必须是对应类型中存在的分析器

        @throws ValueError 当分析器名称不存在于对应类型中时抛出
        """
        analysis_list = []

        if analysis == Analysis.region:
            analysis_list = REGION_ANALYSIS_LIST
        elif analysis == Analysis.state:
            analysis_list = STATE_ANALYSIS_LIST
        elif analysis == Analysis.population:
            analysis_list = POPULATION_ANALYSIS_LIST
        elif analysis == Analysis.building:
            analysis_list = BUILDING_ANALYSIS_LIST
        elif analysis == Analysis.definition:
            analysis_list = DEFINITION_ANALYSIS_LIST
        elif analysis == Analysis.effect:
            analysis_list = EFFECT_ANALYSIS_LIST

        if not name in analysis_list:
            raise ValueError(f'{name} is not in {analysis}')

        analysis_object = analysis_list[name]

        if analysis == Analysis.region:
            self._analysis_order[0] = analysis_object
        elif analysis == Analysis.state:
            self._analysis_order[1] = analysis_object
        elif analysis == Analysis.population:
            self._analysis_order[2] = analysis_object
        elif analysis == Analysis.building:
            self._analysis_order[3] = analysis_object
        elif analysis == Analysis.definition:
            self._analysis_order[4] = analysis_object
        elif analysis == Analysis.effect:
            self._analysis_order[5] = analysis_object

    def set_modify(self, modify: Modify, name: str):
        """!
        @brief 设置修改器配置
        @details 根据修改器类型和名称配置对应的修改器，并自动处理依赖关系

        @param modify 修改器类型枚举值
            - Modify.state: 州修改器
            - Modify.population: 人口修改器
            - Modify.building: 建筑修改器
            - Modify.definition: 国家定义修改器
            - Modify.effect: 国家效果修改器
            - Modify.tag: 标签修改器

        @param name 修改器名称，必须是对应类型中存在的修改器

        @throws ValueError 当修改器名称不存在于对应类型中时抛出
        @throws RuntimeError 当依赖关系解析失败时抛出

        @note 此方法会自动添加修改器依赖的收集器
        """
        modify_list = []
        modify_dependency = []

        if modify == Modify.state:
            modify_list = STATE_MODIFY_LIST
            modify_dependency = STATE_MODIFY_DEPENDENCY
        elif modify == Modify.population:
            modify_list = POPULATION_MODIFY_LIST
            modify_dependency = POPULATION_MODIFY_DEPENDENCY
        elif modify == Modify.building:
            modify_list = BUILDING_MODIFY_LIST
            modify_dependency = BUILDING_MODIFY_DEPENDENCY
        elif modify == Modify.definition:
            modify_list = DEFINITION_MODIFY_LIST
            modify_dependency = DEFINITION_MODIFY_DEPENDENCY
        elif modify == Modify.effect:
            modify_list = EFFECT_MODIFY_LIST
            modify_dependency = EFFECT_MODIFY_DEPENDENCY
        elif modify == Modify.tag:
            modify_list = TAG_MODIFY_LIST
            modify_dependency = TAG_MODIFY_DEPENDENCY

        if not name in modify_list or not name in modify_dependency:
            raise ValueError(f'{name} is not in {modify}')

        modify_object = modify_list[name]
        modify_dependency = modify_dependency[name]

        for i in modify_dependency:
            self.add_collect(i)

        if modify == Modify.state:
            self._modify_order[0] = modify_object
        elif modify == Modify.population:
            self._modify_order[1] = modify_object
        elif modify == Modify.building:
            self._modify_order[2] = modify_object
        elif modify == Modify.definition:
            self._modify_order[3] = modify_object
        elif modify == Modify.effect:
            self._modify_order[4] = modify_object
        elif modify == Modify.tag:
            self._modify_order[5] = modify_object

    def set_transform(self, transform: Transform, name: str):
        """!
        @brief 设置转换器配置
        @details 根据转换器类型和名称配置对应的转换器，替换默认转换器

        @param transform 转换器类型枚举值
            - Transform.state: 州转换器
            - Transform.population: 人口转换器
            - Transform.building: 建筑转换器
            - Transform.definition: 国家定义转换器
            - Transform.effect: 国家效果转换器

        @param name 转换器名称，必须是对应类型中存在的转换器

        @throws ValueError 当转换器名称不存在于对应类型中时抛出
        """
        transform_list = []

        if transform == Transform.state:
            transform_list = STATE_TRANSFORM_LIST
        elif transform == Transform.population:
            transform_list = POPULATION_TRANSFORM_LIST
        elif transform == Transform.building:
            transform_list = BUILDING_TRANSFORM_LIST
        elif transform == Transform.definition:
            transform_list = DEFINITION_TRANSFORM_LIST
        elif transform == Transform.effect:
            transform_list = EFFECT_TRANSFORM_LIST

        if not name in transform_list:
            raise ValueError(f'{name} is not in {transform}')

        transform_object = transform_list[name]

        if transform == Transform.state:
            self._transform_order[0] = transform_object
        elif transform == Transform.population:
            self._transform_order[1] = transform_object
        elif transform == Transform.building:
            self._transform_order[2] = transform_object
        elif transform == Transform.definition:
            self._transform_order[3] = transform_object
        elif transform == Transform.effect:
            self._transform_order[4] = transform_object

    def set_args(self, key: str, value: Any):
        """!
        @brief 设置中间参数
        @details 存储用户自定义参数，供收集器、修改器和转换器使用

        @param key 参数键名
        @param value 参数值，可以是任意类型
        """
        self._middle[key] = value

    def add_collect(self, name: str):
        """!
        @brief 添加收集器
        @details 将指定名称的收集器添加到执行流程中，避免重复添加

        @param name 收集器名称，必须存在于COLLECT_LIST中

        @throws ValueError 当收集器名称不存在于COLLECT_LIST中时抛出
        """
        if name in self._exist_collect_name:
            return

        if name not in COLLECT_LIST:
            raise ValueError(f'{name} is not in collect list: {COLLECT_LIST}')

        self._collect_order.append(COLLECT_LIST[name])
        self._exist_collect_name.add(name)

    def preprocess(self):
        if None in self._analysis_order:
            raise ValueError(f'Analysis class cannot be None: {self._analysis_order}')

        if None in self._modify_order:
            raise ValueError(f'Modify class cannot be None: {self._modify_order}')

        if None in self._transform_order:
            raise ValueError(f'Transform class cannot be None: {self._transform_order}')

    def sort_collects_by_dependency(self):
        """对_collect_order中的collect进行拓扑排序，确保依赖项先执行"""

        # 构建类对象到名称的映射
        class_to_name = {cls: name for name, cls in COLLECT_LIST.items()}

        # 获取当前collect列表对应的名称
        collect_names = []
        for cls in self._collect_order:
            if cls not in class_to_name:
                # 理论上不会发生，但以防万一
                raise ValueError(f'Collect class {cls} not found in COLLECT_LIST')
            collect_names.append(class_to_name[cls])

        # 构建依赖图
        graph = {name: [] for name in collect_names}
        in_degree = {name: 0 for name in collect_names}

        for name in collect_names:
            for dep in COLLECT_DEPENDENCY.get(name, ()):
                if dep in collect_names:  # 只考虑在当前列表中的依赖
                    graph[dep].append(name)
                    in_degree[name] = in_degree.get(name, 0) + 1

        # 拓扑排序
        sorted_names = []
        queue = [name for name in collect_names if in_degree[name] == 0]

        while queue:
            node = queue.pop(0)
            sorted_names.append(node)
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # 检查是否有循环依赖
        if len(sorted_names) != len(collect_names):
            # 找出未排序的节点（有循环依赖）
            remaining = set(collect_names) - set(sorted_names)
            raise ValueError(f'Circular dependency detected among collects: {remaining}')

        # 根据排序后的名称重新排列_collect_order
        name_to_class = COLLECT_LIST
        self._collect_order = [name_to_class[name] for name in sorted_names]

    def analysis(self):
        """!
        @brief 执行数据分析阶段
        @details 按顺序执行所有分析器，解析原始游戏数据并存储到_origin中：
                 1. 区域分析
                 2. 州分析
                 3. 人口分析
                 4. 建筑分析
                 5. 国家定义分析
                 6. 国家效果分析
                 7. 英文翻译分析
                 8. 中文翻译分析
        """

        map_analysis: MapAnalysis = MapAnalysis()
        map_analysis.main(self._manager, 'map')
        self._origin.map = map_analysis.map

        # 区域分析
        region_analysis: RegionAnalysisBase = self._analysis_order[0]()
        region_analysis.main(self._manager, 'region')
        self._origin.region = region_analysis.region

        # 州分析
        state_analysis: StateAnalysisBase = self._analysis_order[1]()
        state_analysis.main(self._manager, 'state')
        self._origin.state = state_analysis.state

        # 人口分析
        population_analysis: PopulationAnalysisBase = self._analysis_order[2]()
        population_analysis.main(self._manager, 'population')
        self._origin.population = population_analysis.population

        # 建筑分析
        building_analysis: BuildingAnalysisBase = self._analysis_order[3]()
        building_analysis.main(self._manager, 'building')
        self._origin.building = building_analysis.building

        # 定义分析
        definition_analysis: DefinitionAnalysisBase = self._analysis_order[4]()
        definition_analysis.main(self._manager, 'definition')
        self._origin.definition = definition_analysis.definition

        # 效果分析
        effect_analysis: EffectAnalysisBase = self._analysis_order[5]()
        effect_analysis.main(self._manager, 'effect')
        self._origin.effect = effect_analysis.effect

        # 翻译分析
        english_translate_analysis: TranslateAnalysis = TranslateAnalysis()
        english_translate_analysis.main(self._manager, 'translate', 'states_l_english.yml')
        self._origin.english_translation = english_translate_analysis.translation

        chinese_translate_analysis: TranslateAnalysis = TranslateAnalysis()
        chinese_translate_analysis.main(self._manager, 'translate', 'states_l_simp_chinese.yml')
        self._origin.chinese_translation = chinese_translate_analysis.translation

    def collect(self):
        """!
        @brief 执行数据收集阶段
        @details 按依赖排序后的顺序执行所有收集器，处理原始数据并生成中间数据
        @details 收集器使用_origin数据和_middle参数进行计算
        """
        for i in self._collect_order:
            collect_object: CollectBase = i(self._origin, self._middle)
            collect_object.main()

    def modify(self):
        """!
        @brief 执行数据修改阶段
        @details 按顺序执行所有修改器，将原始数据转换为目标数据
        @details 修改器使用_origin数据、_middle参数和_target容器
        """
        for i in self._modify_order:
            modify_object: ModifyBase = i(self._origin, self._middle, self._target)
            modify_object.main()

    def fill(self):
        """!
        @brief 填充缺失的目标数据
        @details 检查_target中的各个数据容器，如果为空则使用_origin中的对应数据填充
        @details 确保转换阶段有完整的数据可用
        """
        if self._target.state is None or len(self._target.state) == 0:
            self._target.state = self._origin.state

        if self._target.population is None or len(self._target.population) == 0:
            self._target.population = self._origin.population

        if self._target.building is None or len(self._target.building) == 0:
            self._target.building = self._origin.building

        if self._target.definition is None or len(self._target.definition) == 0:
            self._target.definition = self._origin.definition

        if self._target.effect is None or len(self._target.effect) == 0:
            self._target.effect = self._origin.effect

        if self._target.english_translation is None or len(self._target.english_translation) == 0:
            self._target.english_translation = self._origin.english_translation

        if self._target.chinese_translation is None or len(self._target.chinese_translation) == 0:
            self._target.chinese_translation = self._origin.chinese_translation

    def transform(self):
        """!
        @brief 执行数据转换阶段
        @details 按顺序执行所有转换器，将目标数据写入游戏文件格式：
                 1. 州数据转换
                 2. 人口数据转换
                 3. 建筑数据转换
                 4. 国家定义转换
                 5. 国家效果转换
                 6. 翻译文件转换（如有标签修改）
        """
        # 州转换
        state_transform: StateTransformBase = self._transform_order[0]()
        state_transform.main(self._manager, 'new_state', '80_states.txt', self._target.state)

        # 人口转换
        population_transform: PopulationTransformBase = self._transform_order[1]()
        population_transform.main(self._manager, 'new_population', '80_pops.txt', self._target.population)

        # 建筑转换
        building_transform: BuildingTransformBase = self._transform_order[2]()
        building_transform.main(self._manager, 'new_building', '80_buildings.txt', self._target.building)

        # 定义转换
        definition_transform: DefinitionTransformBase = self._transform_order[3]()
        definition_transform.main(self._manager, 'new_definition', '80_countries.txt', self._target.definition)

        # 效果转换
        effect_transform: EffectTransformBase = self._transform_order[4]()
        effect_transform.main(self._manager, 'new_effect', self._target.effect)

        if self._target.tag:
            english_translate_transform = TranslateTransform()
            english_translate_transform.main(
                self._manager,
                'new_translate',
                self.target_file_root / r'localization\english\alternate_world_l_english.yml',
                'l_english:',
                self._target.english_translation,
                self._target.tag
            )

            chinese_translate_transform = TranslateTransform()
            chinese_translate_transform.main(
                self._manager,
                'new_translate',
                self.target_file_root / r'localization\simplified_chinese\alternate_world_l_simp_chinese.yml',
                'l_simp_chinese:',
                self._target.chinese_translation,
                self._target.tag
            )

    def main(self):
        """!
        @brief 主执行流程
        @details 按顺序执行完整的处理流程：
                 1. 数据分析：解析原始游戏数据
                 2. 收集器依赖排序：确保依赖关系正确
                 3. 数据收集：处理中间数据
                 4. 数据修改：应用修改规则
                 5. 覆盖文件生成：创建目标文件占位符
                 6. 数据填充：确保目标数据完整
                 7. 数据转换：生成最终游戏文件
        """
        self.preprocess()

        self.analysis()

        self.sort_collects_by_dependency()

        self.collect()

        self.modify()

        self.cover_file_generator()

        self.fill()

        self.transform()


if __name__ == '__main__':
    frame: Frame = Frame(Path(r'D:\application\Steam\steamapps\common\Victoria 3'), Path(r'C:\Users\User\Documents\Paradox Interactive\Victoria 3\mod\Alternate World'))

    frame.set_analysis(Analysis.region, 'default')
    frame.set_analysis(Analysis.state, 'default')
    frame.set_analysis(Analysis.population, 'default')
    frame.set_analysis(Analysis.building, 'default')
    frame.set_analysis(Analysis.definition, 'default')
    frame.set_analysis(Analysis.effect, 'default')

    frame.set_modify(Modify.state, 'region_adjacent_country')
    frame.set_args('max_merge_percent', 35)

    frame.set_modify(Modify.building, 'empty')

    frame.set_modify(Modify.population, 'generate')
    frame.set_args('population_generate_function', DataGenerateType.randomize)
    frame.set_args('population_random_range', (1000000, 10000000))

    frame.set_modify(Modify.effect, 'generate')
    frame.set_args('technology_generate_function', DataGenerateType.randomize)
    frame.set_args('random_technology_range', (5, 6))
    frame.set_args('laws_generate_function', DataGenerateType.randomize)

    frame.set_modify(Modify.definition, 'generate')
    frame.set_args('country_type_generate_function', DataGenerateType.randomize)
    frame.set_args('set_random_country_type_weight', [2, 6, 2])
    frame.set_args('main_culture_generate_function', DataGenerateType.default)
    frame.set_args('set_main_culture_max_number', 2)
    frame.set_args('enable_named_from_capital', True)

    frame.set_modify(Modify.tag, 'default')

    frame.set_transform(Transform.state, 'default')
    frame.set_transform(Transform.population, 'default')
    frame.set_transform(Transform.building, 'default')
    frame.set_transform(Transform.definition, 'default')
    frame.set_transform(Transform.effect, 'default')

    frame.main()
