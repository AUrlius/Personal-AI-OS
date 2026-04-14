# 个人AI记忆系统 (Memory System)

基于 mempalace 架构设计的 AI 记忆系统，实现了智能记忆存储、检索和管理功能。

## 🧠 系统架构

```
┌─────────────────┐    ┌─────────────────┐
│   用户输入      │ -> │  记忆存储       │
└─────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌─────────────────┐
│  语义检索       │ <- │  向量存储       │
└─────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌─────────────────┐
│  记忆管理       │ <- │  关联分析       │
└─────────────────┘    └─────────────────┘
```

## ✨ 核心功能

### 1. 智能记忆存储
- **内容存储**: 支持文本、元数据、标签等多种信息存储
- **优先级管理**: 支持1-5级优先级设置
- **向量化存储**: 内容自动转换为向量表示

### 2. 语义检索
- **相似度搜索**: 基于向量相似度的语义检索
- **多维度过滤**: 支持标签、时间、优先级等多维度过滤
- **相关性排序**: 检索结果按相关性排序

### 3. 记忆关联
- **关系建立**: 支持记忆间的关系建立
- **关联检索**: 支持基于关系的关联记忆检索
- **网络分析**: 记忆关系网络分析

### 4. 记忆管理
- **批量操作**: 支持批量存储和检索
- **统计分析**: 提供记忆使用统计
- **优先级调整**: 支持动态调整记忆优先级

## 🏗️ 核心模块

### Memory 类
```python
class Memory:
    id: str                    # 记忆唯一标识
    content: str               # 记忆内容
    embeddings: List[float]    # 向量表示
    metadata: Dict[str, Any]   # 元数据
    tags: List[str]           # 标签列表
    priority: int             # 优先级 (1-5)
    timestamp: datetime       # 时间戳
    relationships: List[str]  # 关联记忆ID列表
```

### MemorySystem 类
主要接口：
- `remember()` - 存储新记忆
- `recall()` - 检索相关记忆  
- `forget()` - 删除记忆
- `associate()` - 建立记忆关联
- `find_related_memories()` - 查找关联记忆
- `get_memory_statistics()` - 获取统计信息

## 🚀 使用示例

```python
# 创建记忆系统实例
memory_system = MemorySystem()

# 记住新内容
memory_id = await memory_system.remember(
    content="机器学习中的梯度下降算法是优化模型参数的核心方法...",
    metadata={"category": "machine_learning", "difficulty": "advanced"},
    tags=["machine_learning", "gradient_descent", "optimization"],
    priority=5
)

# 检索相关记忆
results = await memory_system.recall("什么是梯度下降", top_k=5, threshold=0.7)
for result in results:
    print(f"内容: {result.memory.content}")
    print(f"相似度: {result.similarity_score}")

# 建立记忆关联
await memory_system.associate(memory_id1, memory_id2)

# 查找关联记忆
related = await memory_system.find_related_memories(memory_id, top_k=3)
```

## 🎯 技术特点

### 向量相似度算法
- **余弦相似度**: 计算向量间的角度相似度
- **归一化处理**: 确保向量长度不影响相似度计算
- **阈值过滤**: 支持相似度阈值过滤

### 存储架构
- **索引优化**: 多重索引提升检索效率
- **批量操作**: 支持批量存储和检索
- **内存管理**: 优化内存使用和垃圾回收

### 扩展性设计
- **模块化架构**: 各组件可独立扩展
- **接口标准化**: 统一接口便于替换实现
- **配置灵活**: 支持多种配置选项

## 📊 应用场景

1. **个人知识管理**: 个人学习笔记、工作经验存储
2. **智能助手**: 为AI助手提供记忆能力
3. **内容推荐**: 基于记忆的个性化推荐
4. **决策支持**: 基于历史记忆的决策辅助

## 🛠️ 依赖

- Python 3.8+
- NumPy (向量计算)
- ChromaDB (向量数据库)
- Transformers (嵌入模型)

## 📈 未来发展方向

1. **多模态支持**: 图像、音频等多媒体记忆
2. **实时学习**: 在线学习和记忆更新
3. **隐私保护**: 端侧加密和隐私保护
4. **协作记忆**: 多用户协作记忆系统

---
*基于 mempalace 架构设计，专为 Personal-AI-OS 定制开发*