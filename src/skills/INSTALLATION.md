# 技能系统安装与使用指南

## 📋 依赖要求

### 系统要求
- Python 3.8+
- 操作系统: Linux/macOS/Windows
- 内存: ≥ 2GB
- 存储: ≥ 500MB

### Python 依赖
```bash
pip install numpy>=1.21.0
pip install aiofiles>=23.0.0
pip install psutil>=5.8.0  # 系统监控
```

## 🛠️ 安装步骤

### 1. 克接到 Personal-AI-OS 项目
技能系统已作为 Personal-AI-OS 的一部分，位于 `src/skills/` 目录。

### 2. 安装依赖
```bash
# 进入项目目录
cd /path/to/Personal-AI-OS

# 安装 Python 依赖
pip install -r requirements.txt
```

### 3. 验证安装
```python
from src.skills import SkillSystem, SkillBuilder

# 创建技能系统实例
skill_system = SkillSystem()
print("✅ 技能系统安装成功！")
```

## 🚀 快速开始

### 基础使用
```python
import asyncio
from src.skills.core import SkillSystem, SkillBuilder
from src.skills.interfaces import SkillVisibility, SkillStatus

async def main():
    # 创建技能系统
    skill_system = SkillSystem()
    
    # 创建一个简单的技能
    hello_skill = (SkillBuilder()
        .id("hello-world")
        .name("Hello World")
        .description("输出Hello World")
        .version("1.0.0")
        .author("user")
        .category("demo")
        .add_input("name", "string", "用户名", required=False, default="World")
        .add_output("greeting", "string", "问候语")
        .code("""
def execute(name):
    return {"greeting": f"Hello, {name}!"}
""")
        .language("python")
        .execution_type("function")
        .visibility(SkillVisibility.PUBLIC)
        .status(SkillStatus.PUBLISHED)
        .build())
    
    # 注册技能
    success = await skill_system.register(hello_skill)
    print(f"技能注册: {success}")
    
    # 执行技能
    result = await skill_system.execute("hello-world", {"name": "Alice"})
    print(f"执行结果: {result.output}")

# 运行
asyncio.run(main())
```

### 高级功能
```python
from src.skills.core import SkillOrchestrator

# 创建编排器
orchestrator = SkillOrchestrator(skill_system)

# 定义技能序列
sequence = [
    {
        "skill_id": "calculator-add",
        "parameters": {"a": 10, "b": 5},
        "output_mapping": {"result": "sum_result"}
    },
    {
        "skill_id": "calculator-multiply", 
        "parameters": {"a": "{{sum_result}}", "b": 2},  # 使用上一步结果
        "output_mapping": {"result": "final_result"}
    }
]

# 执行序列
result = await orchestrator.execute_sequence(sequence)
print(f"序列结果: {result}")
```

## ⚙️ 配置管理

### 默认配置
系统使用默认配置，可按需修改：

```python
from src.skills.config import update_skill_system_config

# 更新配置
config = update_skill_system_config(
    execution_timeout=60,  # 执行超时时间（秒）
    max_concurrent_executions=20,  # 最大并发执行数
    sandbox_max_memory=256,  # 沙箱最大内存（MB）
    enable_cache=True,  # 启用缓存
    cache_ttl=7200  # 缓存生存时间（秒）
)
```

### 环境变量配置
```bash
# 设置环境变量
export SKILL_EXECUTION_TIMEOUT=60
export SKILL_SANDBOX_MAX_MEMORY=512
export SKILL_ENABLE_CACHE=true
export SKILL_CACHE_TTL=3600
```

## 🛡️ 安全指南

### 代码安全
- 所有技能代码在沙箱中执行
- 禁止危险函数调用
- 资源使用限制

### 权限控制
- 按技能可见性控制访问
- 用户权限验证
- API调用限制

### 最佳实践
1. **代码验证**: 执行前验证代码安全性
2. **资源限制**: 设置合理的内存和时间限制
3. **权限最小化**: 按需分配权限
4. **监控告警**: 启用执行监控

## 📊 监控与日志

### 系统指标
- 执行时间
- 资源使用
- 错误率
- 并发数

### 日志配置
```python
import logging

# 设置日志级别
logging.basicConfig(level=logging.INFO)
```

## 🔧 故障排除

### 常见问题
1. **技能注册失败**
   - 检查技能ID格式
   - 验证必填字段

2. **技能执行失败**
   - 检查输入参数类型
   - 验证代码语法

3. **沙箱执行超时**
   - 调整超时时间
   - 优化代码逻辑

### 调试技巧
```python
# 启用调试日志
import logging
logging.getLogger('skills').setLevel(logging.DEBUG)

# 验证技能定义
from src.skills.utils.validator import SkillValidator
validator = SkillValidator()
is_valid = await validator.validate_skill_definition(skill_def)
```

## 🚀 部署指南

### 开发环境
```bash
# 克接到项目
git clone <repository-url>
cd Personal-AI-OS

# 安装依赖
pip install -r requirements.txt

# 运行测试
python -m pytest tests/skills/
```

### 生产环境
```bash
# 使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装生产依赖
pip install -r requirements-prod.txt

# 配置生产环境变量
export SKILL_REGISTRY_TYPE=persistent
export SKILL_EXECUTION_TIMEOUT=30
export SKILL_SANDBOX_TYPE=docker
```

## 📚 学习资源

### 示例代码
- `src/skills/example_usage.py` - 使用示例
- `src/skills/full_demo.py` - 完整演示
- `tests/skills/` - 测试用例

### API 文档
- 核心类: `SkillSystem`, `SkillBuilder`, `SkillOrchestrator`
- 接口: `SkillDefinition`, `SkillExecutionResult`
- 工具: `SkillValidator`, `ConfigManager`

## 🤝 支持

### 问题反馈
- GitHub Issues: 提交 bug 和功能请求
- 讨论区: 技术交流和问题讨论

### 贡献代码
1. Fork 仓库
2. 创建功能分支
3. 提交代码
4. 发起 Pull Request

---

*祝您使用愉快！如需更多帮助，请查看相关文档或寻求社区支持。*