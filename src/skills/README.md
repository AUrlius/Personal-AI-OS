# 技能系统 (Skills System)

基于 khazix-skills 架构设计的可扩展技能框架，为 Personal-AI-OS 提供动态功能扩展能力。

## 🏗️ 系统架构

```
┌─────────────────┐    ┌─────────────────┐
│   技能构建器    │ -> │  技能注册表     │
└─────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌─────────────────┐
│  技能执行器     │ <- │  技能沙箱       │
└─────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌─────────────────┐
│  技能编排器     │ <- │  配置管理       │
└─────────────────┘    └─────────────────┘
```

## ✨ 核心功能

### 1. 动态技能注册
- **技能定义**: 支持代码、输入输出、依赖关系定义
- **类型安全**: 严格的输入输出类型验证
- **版本管理**: 完整的版本控制和管理

### 2. 安全沙箱执行
- **语言支持**: Python, JavaScript, Shell
- **权限控制**: 细粒度权限管理
- **资源限制**: 内存、CPU、时间限制

### 3. 智能技能编排
- **序列执行**: 按顺序执行多个技能
- **并行执行**: 同时执行多个技能
- **依赖管理**: 自动处理技能依赖

### 4. 高级管理功能
- **搜索发现**: 基于标签和分类的搜索
- **统计分析**: 技能使用统计
- **监控告警**: 执行监控和性能分析

## 🚀 快速开始

### 基础使用

```python
from skills.core import SkillSystem, SkillBuilder
from skills.interfaces import SkillInput, SkillOutput

# 创建技能系统
skill_system = SkillSystem()

# 创建技能
calculator_skill = (SkillBuilder()
    .id("calculator-add")
    .name("加法计算器")
    .description("执行两个数字的加法运算")
    .version("1.0.0")
    .add_input("a", "number", "第一个数字", required=True)
    .add_input("b", "number", "第二个数字", required=True)
    .add_output("result", "number", "计算结果")
    .code("""
def execute(a, b):
    return {"result": a + b}
""")
    .language("python")
    .build())

# 注册技能
await skill_system.register(calculator_skill)

# 执行技能
result = await skill_system.execute("calculator-add", {"a": 10, "b": 20})
print(result.output)  # {"result": 30}
```

### 高级功能

```python
from skills.core import SkillOrchestrator

# 技能编排
orchestrator = SkillOrchestrator(skill_system)

# 定义技能序列
skill_sequence = [
    {
        "skill_id": "calculator-add",
        "parameters": {"a": 10, "b": 5},
        "output_mapping": {"result": "sum_result"}
    },
    {
        "skill_id": "calculator-add", 
        "parameters": {"a": "{{sum_result}}", "b": 15},  # 使用上一步结果
        "output_mapping": {"result": "final_result"}
    }
]

# 执行序列
sequence_result = await orchestrator.execute_sequence(skill_sequence)
```

## 🛠️ 核心组件

### SkillBuilder
技能构建器，用于简化技能创建过程：
- 链式调用API
- 自动验证输入
- 代码安全检查

### SkillRegistry
技能注册表，管理所有技能：
- 内存/持久化存储
- 快速检索
- 版本控制

### SkillExecutor
技能执行器，负责技能执行：
- 参数验证
- 权限检查
- 结果返回

### SkillSandbox
技能沙箱，提供安全执行环境：
- 代码安全验证
- 资源限制
- 隔离执行

## 📊 技能定义规范

### 基本属性
- `id`: 技能唯一标识符
- `name`: 技能名称
- `description`: 技能描述
- `version`: 版本号 (semver)
- `author`: 作者信息

### 输入输出定义
```python
inputs = [
    SkillInput(
        name="input_name",
        type="string",  # string, number, boolean, object, array, file
        description="输入参数描述",
        required=True,
        default="default_value"
    )
]

outputs = [
    SkillOutput(
        name="output_name",
        type="string",
        description="输出参数描述"
    )
]
```

### 执行配置
- `language`: 代码语言 (python, javascript, shell)
- `execution_type`: 执行类型 (function, script, api_call)
- `timeout`: 执行超时时间
- `max_memory`: 最大内存使用

## 🔐 安全特性

### 代码安全验证
- AST解析检查
- 危险函数识别
- 权限验证

### 执行时安全
- 资源限制
- 隔离环境
- 监控告警

### 访问控制
- 技能可见性
- 用户权限检查
- 调用次数限制

## 🎯 应用场景

1. **AI助手扩展**: 为AI助手添加新功能
2. **自动化任务**: 实现各种自动化任务
3. **数据处理**: 数据分析和处理技能
4. **系统集成**: 集成外部服务和API
5. **用户自定义**: 用户创建个性化技能

## 📈 扩展性设计

### 插件化架构
- 模块化设计
- 标准化接口
- 易于扩展

### 性能优化
- 执行缓存
- 并行执行
- 资源池管理

## 🤝 贡献

我们欢迎各种形式的贡献：
- 新技能开发
- 功能改进
- 安全漏洞报告
- 文档完善

---
*基于 khazix-skills 架构设计，专为 Personal-AI-OS 定制开发*