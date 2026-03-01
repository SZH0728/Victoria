# Victoria 3 Data Analysis & Transformation Tool

# 维多利亚3 数据分析与转换工具

[English](#english) | [中文](#中文)

---

<a id="english"></a>
## English Version

### Overview

The **Victoria 3 Data Analysis & Transformation Tool** is a comprehensive Python framework designed for analyzing, processing, and transforming game data from Paradox Interactive's Victoria 3. It provides a structured approach to parse game files, extract meaningful information, apply modifications, and generate mod files compatible with the game.

This tool enables modders and data analysts to:
- Parse Victoria 3 game files (strategic regions, states, buildings, population, country definitions, etc.)
- Extract structured data using a type-safe Python framework
- Apply custom modifications to game data
- Generate mod files with transformed data
- Handle localization and translation files

### Features

- **Complete Data Type System**: Comprehensive Python dataclasses representing all major game entities (Regions, States, Buildings, Population, Country Definitions, Effects)
- **Modular Architecture**: Separated analysis, transformation, and processing modules with clear interfaces
- **Extensible Framework**: Abstract base classes allow easy implementation of custom analysis and transformation logic
- **File Management**: Unified file grouping and encoding management with `FileManager` class
- **Data Container**: Generic `Map[T]` container providing dictionary-like interface with attribute access
- **Dependency Management**: Automatic topological sorting for data collection dependencies
- **Translation Support**: Built-in handling for English and Chinese localization files
- **Mod Generation**: Complete pipeline from original game files to mod output

### Project Structure

```
Victoria/
├── core/                          # Core framework modules
│   ├── datatype/                  # Game data type definitions
│   │   ├── map.py                # Generic Map container class
│   │   ├── region.py             # Region data types
│   │   ├── state.py              # State data types
│   │   ├── building.py           # Building data types
│   │   ├── population.py         # Population data types
│   │   ├── definition.py         # Country definition types
│   │   ├── effect.py             # Country effect types
│   │   └── combination.py        # Data combination container
│   │
│   ├── analysis/                  # Data analysis modules
│   │   ├── extract.py            # Key extraction mixin
│   │   ├── translate.py          # Translation analysis
│   │   ├── region/               # Region analysis
│   │   ├── state/                # State analysis
│   │   ├── building/             # Building analysis
│   │   ├── population/           # Population analysis
│   │   ├── definition/           # Country definition analysis
│   │   └── effect/               # Country effect analysis
│   │
│   ├── transform/                 # Data transformation modules
│   │   ├── combine.py            # Key combination mixin
│   │   ├── translate.py          # Translation transformation
│   │   ├── region/               # Region transformation
│   │   ├── state/                # State transformation
│   │   ├── building/             # Building transformation
│   │   ├── population/           # Population transformation
│   │   ├── definition/           # Country definition transformation
│   │   └── effect/               # Country effect transformation
│   │
│   ├── process/                   # Data processing workflows
│   │   ├── collect/              # Data collectors
│   │   │   ├── base.py           # Collector base class
│   │   │   ├── plot.py           # State plot collection
│   │   │   ├── population.py     # Population merge collection
│   │   │   └── adjacent.py       # State adjacency analysis
│   │   │
│   │   └── modify/               # Data modifiers
│   │       ├── base.py           # Modifier base class
│   │       ├── state/            # State modifiers
│   │       ├── population/       # Population modifiers
│   │       ├── building/         # Building modifiers
│   │       ├── definition/       # Country definition modifiers
│   │       ├── effect/           # Country effect modifiers
│   │       └── tag/              # Tag modifiers
│   │
│   ├── file.py                   # File manager with grouping
│   ├── frame.py                  # Main framework class
│   └── __init__.py               # Core module exports
│
├── .gitignore                    # Git ignore patterns
├── LICENSE                       # MIT License
└── README.md                     # This file
```

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Victoria
   ```

2. **Set up Python environment (Python 3.8+ required):**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install pyradox
   ```

### Usage

#### Basic Example

```python
from pathlib import Path
from core.frame import Frame, Modify

# Initialize the framework with game and mod directories
frame = Frame(
    original_file_root=Path(r'D:\application\Steam\steamapps\common\Victoria 3'),
    target_file_root=Path(r'C:\Users\User\Documents\Paradox Interactive\Victoria 3\mod\My Mod')
)

# Configure modifications
frame.set_modify(Modify.state, 'region_merge_country')
frame.set_args('max_merge_percent', 30)

frame.set_modify(Modify.building, 'empty')
frame.set_modify(Modify.population, 'merge')
frame.set_modify(Modify.effect, 'randomize')

# Set randomizer parameters
frame.set_args('enable_random_technology', True)
frame.set_args('random_technology_range', (6, 6))
frame.set_args('enable_random_law', True)

# Execute the complete pipeline
frame.main()
```

#### Available Modifiers

- **State Modifiers:**
  - `region_merge_country`: Merge countries within regions
  - `state`: Basic state modification
  - `merge`: Merge adjacent states

- **Population Modifiers:**
  - `merge`: Merge populations with same traits
  - `default`: Default population modification

- **Building Modifiers:**
  - `empty`: Remove all buildings
  - `default`: Default building modification

- **Country Definition Modifiers:**
  - `generate`: Generate new country definitions
  - `default`: Default definition modification

- **Country Effect Modifiers:**
  - `randomize`: Randomize country effects
  - `empty`: Clear country effects
  - `default`: Default effect modification

- **Tag Modifiers:**
  - `default`: Default tag modification

#### Custom Analysis Implementation

To implement custom analysis logic:

1. Create a new class inheriting from the appropriate base class:
   ```python
   from core.analysis.state.base import StateAnalysisBase

   class CustomStateAnalysis(StateAnalysisBase):
       def analysis(self, tree, state_name):
           # Implement custom analysis logic
           state_data = self.extract_state_data(tree)
           return self.create_state_object(state_data)
   ```

2. Register it in the corresponding `__init__.py` file.

### Configuration

#### File Group Configuration

The framework automatically organizes files into groups:

| Group Name | Description | Source Path |
|------------|-------------|-------------|
| `region` | Strategic region definitions | `game/common/strategic_regions/` |
| `state` | State history files | `game/common/history/states/` |
| `population` | Population data | `game/common/history/pops/` |
| `building` | Building data | `game/common/history/buildings/` |
| `definition` | Country definitions | `game/common/country_definitions/` |
| `effect` | Country effects | `game/common/history/countries/` |
| `translate` | Localization files | `game/localization/` |

#### Processing Pipeline

The framework executes in the following order:

1. **Analysis Phase**: Parse all game files into structured data
2. **Collection Phase**: Gather and process intermediate data with dependency resolution
3. **Modification Phase**: Apply configured modifications to the data
4. **File Preparation**: Generate empty target files for writing
5. **Data Filling**: Ensure all target data containers are populated
6. **Transformation Phase**: Convert structured data back to game file format

### Development

#### Code Style

- **Encoding**: All files use `# -*- coding:utf-8 -*-` header
- **Documentation**: Doxygen-style comments (`@brief`, `@details`, `@param`, etc.)
- **Naming**:
  - Classes: `PascalCase`
  - Methods/Functions: `snake_case`
  - Data class fields have type hints
- **File Encoding**: UTF-8 with BOM (`utf-8-sig`) for all file operations

#### Extending the Framework

1. **Adding New Analysis Types**:
   - Create base class in `core/analysis/<type>/base.py`
   - Implement default version in `core/analysis/<type>/default.py`
   - Register in `core/analysis/<type>/__init__.py`

2. **Adding New Transform Types**:
   - Create base class in `core/transform/<type>/base.py`
   - Implement default version in `core/transform/<type>/default.py`
   - Register in `core/transform/<type>/__init__.py`

3. **Adding New Collectors**:
   - Inherit from `CollectBase` in `core/process/collect/base.py`
   - Implement `collect()` method
   - Register in `core/process/collect/__init__.py`

4. **Adding New Modifiers**:
   - Inherit from `ModifyBase` in `core/process/modify/base.py`
   - Implement `modify()` method
   - Register in corresponding `__init__.py` file

### Dependencies

- **pyradox**: Paradox game file parser
- **Python 3.8+**: Type hints and dataclasses

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a id="中文"></a>
## 中文版本

### 项目概述

**维多利亚3 数据分析与转换工具** 是一个用于解析、处理和转换Paradox Interactive《维多利亚3》游戏数据的完整Python框架。它提供结构化的方法来解析游戏文件、提取有意义的信息、应用修改并生成与游戏兼容的模组文件。

该工具使模组制作者和数据分析师能够：
- 解析《维多利亚3》游戏文件（战略区域、州、建筑、人口、国家定义等）
- 使用类型安全的Python框架提取结构化数据
- 对游戏数据应用自定义修改
- 生成包含转换数据的模组文件
- 处理本地化和翻译文件

### 功能特性

- **完整的数据类型系统**：代表所有主要游戏实体的全面Python数据类（区域、州、建筑、人口、国家定义、效果）
- **模块化架构**：分离的分析、转换和处理模块，具有清晰的接口
- **可扩展框架**：抽象基类允许轻松实现自定义分析和转换逻辑
- **文件管理**：统一的文件分组和编码管理，使用`FileManager`类
- **数据容器**：泛型`Map[T]`容器，提供类似字典的接口和属性访问
- **依赖管理**：数据收集器依赖关系的自动拓扑排序
- **翻译支持**：内置英文和中文本地化文件处理
- **模组生成**：从原始游戏文件到模组输出的完整流水线

### 项目结构

（与英文版相同）

### 安装步骤

1. **克隆仓库：**
   ```bash
   git clone <仓库地址>
   cd Victoria
   ```

2. **设置Python环境（需要Python 3.8+）：**
   ```bash
   python -m venv .venv
   # Windows：
   .venv\Scripts\activate
   # macOS/Linux：
   source .venv/bin/activate
   ```

3. **安装依赖：**
   ```bash
   pip install pyradox
   ```

### 使用示例

#### 基础示例

```python
from pathlib import Path
from core.frame import Frame, Modify

# 使用游戏和模组目录初始化框架
frame = Frame(
    original_file_root=Path(r'D:\application\Steam\steamapps\common\Victoria 3'),
    target_file_root=Path(r'C:\Users\User\Documents\Paradox Interactive\Victoria 3\mod\我的模组')
)

# 配置修改器
frame.set_modify(Modify.state, 'region_merge_country')
frame.set_args('max_merge_percent', 30)

frame.set_modify(Modify.building, 'empty')
frame.set_modify(Modify.population, 'merge')
frame.set_modify(Modify.effect, 'randomize')

# 设置随机化参数
frame.set_args('enable_random_technology', True)
frame.set_args('random_technology_range', (6, 6))
frame.set_args('enable_random_law', True)

# 执行完整流水线
frame.main()
```

#### 可用修改器

- **州修改器：**
  - `region_merge_country`：在区域内合并国家
  - `state`：基础州修改
  - `merge`：合并相邻州

- **人口修改器：**
  - `merge`：合并具有相同特质的人口
  - `default`：默认人口修改

- **建筑修改器：**
  - `empty`：移除所有建筑
  - `default`：默认建筑修改

- **国家定义修改器：**
  - `generate`：生成新的国家定义
  - `default`：默认定义修改

- **国家效果修改器：**
  - `randomize`：随机化国家效果
  - `empty`：清空国家效果
  - `default`：默认效果修改

- **标签修改器：**
  - `default`：默认标签修改

#### 自定义分析实现

要实现自定义分析逻辑：

1. 创建继承自相应基类的新类：
   ```python
   from core.analysis.state.base import StateAnalysisBase

   class CustomStateAnalysis(StateAnalysisBase):
       def analysis(self, tree, state_name):
           # 实现自定义分析逻辑
           state_data = self.extract_state_data(tree)
           return self.create_state_object(state_data)
   ```

2. 在相应的`__init__.py`文件中注册。

### 配置说明

#### 文件组配置

框架自动将文件组织成组：

| 组名 | 描述 | 源路径 |
|------|------|--------|
| `region` | 战略区域定义 | `game/common/strategic_regions/` |
| `state` | 州历史文件 | `game/common/history/states/` |
| `population` | 人口数据 | `game/common/history/pops/` |
| `building` | 建筑数据 | `game/common/history/buildings/` |
| `definition` | 国家定义 | `game/common/country_definitions/` |
| `effect` | 国家效果 | `game/common/history/countries/` |
| `translate` | 本地化文件 | `game/localization/` |

#### 处理流水线

框架按以下顺序执行：

1. **分析阶段**：将所有游戏文件解析为结构化数据
2. **收集阶段**：收集和处理中间数据，解析依赖关系
3. **修改阶段**：应用配置的修改到数据
4. **文件准备**：生成用于写入的空目标文件
5. **数据填充**：确保所有目标数据容器都已填充
6. **转换阶段**：将结构化数据转换回游戏文件格式

### 开发指南

#### 代码风格

- **编码**：所有文件使用`# -*- coding:utf-8 -*-`头部注释
- **文档**：Doxygen风格注释（`@brief`、`@details`、`@param`等）
- **命名约定**：
  - 类名：`PascalCase`
  - 方法/函数名：`snake_case`
  - 数据类字段有类型提示
- **文件编码**：所有文件操作使用带BOM的UTF-8编码（`utf-8-sig`）

#### 扩展框架

1. **添加新的分析类型**：
   - 在`core/analysis/<类型>/base.py`中创建基类
   - 在`core/analysis/<类型>/default.py`中实现默认版本
   - 在`core/analysis/<类型>/__init__.py`中注册

2. **添加新的转换类型**：
   - 在`core/transform/<类型>/base.py`中创建基类
   - 在`core/transform/<类型>/default.py`中实现默认版本
   - 在`core/transform/<类型>/__init__.py`中注册

3. **添加新的收集器**：
   - 继承`core/process/collect/base.py`中的`CollectBase`
   - 实现`collect()`方法
   - 在`core/process/collect/__init__.py`中注册

4. **添加新的修改器**：
   - 继承`core/process/modify/base.py`中的`ModifyBase`
   - 实现`modify()`方法
   - 在相应的`__init__.py`文件中注册

### 依赖项

- **pyradox**：Paradox游戏文件解析器
- **Python 3.8+**：类型提示和数据类

### 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件。

---

### 贡献指南

欢迎提交Issue和Pull Request来改进此项目。

### 支持

如果您遇到问题或有功能建议，请创建GitHub Issue。

### 致谢

- Paradox Interactive 创造了优秀的《维多利亚3》游戏
- pyradox 项目提供了Paradox游戏文件解析功能