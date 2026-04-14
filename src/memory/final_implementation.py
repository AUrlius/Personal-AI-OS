"""
完整记忆系统实现（模拟版本）
基于 mempalace 架构设计，适用于当前环境
"""
import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import hashlib
import math


class Memory:
    """
    记忆对象
    """
    def __init__(self, content: str, metadata: Dict[str, Any] = None, tags: List[str] = None, 
                 priority: int = 3, memory_id: str = None):
        self.id = memory_id or str(uuid.uuid4())
        self.content = content
        self.metadata = metadata or {}
        self.tags = tags or []
        self.priority = min(max(priority, 1), 5)  # 限制在1-5之间
        self.timestamp = datetime.now()
        self.relationships = []
        self.access_count = 0
        self.last_access = None
        # 模拟嵌入向量
        self.embeddings = self._generate_mock_embeddings(content)
    
    def _generate_mock_embeddings(self, text: str) -> List[float]:
        """
        生成模拟嵌入向量（基于文本内容的确定性哈希）
        """
        # 使用文本内容生成确定性的向量
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        
        # 将哈希转换为数字序列
        vector = []
        for i in range(0, 1536*2, 2):  # 生成双倍长度的数字
            if i < len(text_hash)*2:
                hex_pair = text_hash[i:i+2]
                value = int(hex_pair, 16) / 255.0  # 归一化到0-1
                vector.append(value)
            else:
                vector.append(0.0)
        
        # 取前1536个值
        vector = vector[:1536]
        
        # 归一化向量
        norm = math.sqrt(sum(x*x for x in vector))
        if norm > 0:
            vector = [x/norm for x in vector]
        
        return vector


class MemoryQuery:
    """
    记忆查询对象
    """
    def __init__(self, query_text: str, filters: Dict[str, Any] = None, top_k: int = 10, threshold: float = 0.7):
        self.query_text = query_text
        self.filters = filters or {}
        self.top_k = top_k
        self.threshold = threshold
        # 生成查询的模拟嵌入向量
        self.query_embedding = self._generate_mock_embeddings(query_text)
    
    def _generate_mock_embeddings(self, text: str) -> List[float]:
        """
        生成查询的模拟嵌入向量
        """
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        
        vector = []
        for i in range(0, 1536*2, 2):
            if i < len(text_hash)*2:
                hex_pair = text_hash[i:i+2]
                value = int(hex_pair, 16) / 255.0
                vector.append(value)
            else:
                vector.append(0.0)
        
        vector = vector[:1536]
        
        # 归一化向量
        norm = math.sqrt(sum(x*x for x in vector))
        if norm > 0:
            vector = [x/norm for x in vector]
        
        return vector


class MemoryResult:
    """
    记忆查询结果
    """
    def __init__(self, memory: Memory, similarity_score: float, rank: int):
        self.memory = memory
        self.similarity_score = similarity_score
        self.rank = rank


class VectorMemoryStore:
    """
    向量存储实现（模拟版）
    """
    def __init__(self):
        self.memories = {}  # id -> Memory
        self.tag_index = {}  # tag -> [memory_ids]
        self.priority_index = {}  # priority -> [memory_ids]
        self.date_index = {}  # date -> [memory_ids]
    
    async def store_memory(self, memory: Memory) -> str:
        """
        存储记忆
        """
        self.memories[memory.id] = memory
        
        # 更新索引
        for tag in memory.tags:
            if tag not in self.tag_index:
                self.tag_index[tag] = []
            if memory.id not in self.tag_index[tag]:
                self.tag_index[tag].append(memory.id)
        
        priority = memory.priority
        if priority not in self.priority_index:
            self.priority_index[priority] = []
        if memory.id not in self.priority_index[priority]:
            self.priority_index[priority].append(memory.id)
        
        date_key = memory.timestamp.strftime("%Y-%m-%d")
        if date_key not in self.date_index:
            self.date_index[date_key] = []
        if memory.id not in self.date_index[date_key]:
            self.date_index[date_key].append(memory.id)
        
        return memory.id
    
    async def batch_store_memories(self, memories: List[Memory]) -> List[str]:
        """
        批量存储记忆
        """
        stored_ids = []
        for memory in memories:
            memory_id = await self.store_memory(memory)
            stored_ids.append(memory_id)
        return stored_ids
    
    async def search_memories(self, query: MemoryQuery) -> List[MemoryResult]:
        """
        搜索记忆
        """
        results = []
        
        for memory_id, memory in self.memories.items():
            # 计算相似度
            similarity = self._calculate_cosine_similarity(query.query_embedding, memory.embeddings)
            
            # 检查阈值
            if similarity >= query.threshold:
                # 检查过滤器
                if self._apply_filters(memory, query.filters):
                    result = MemoryResult(
                        memory=memory,
                        similarity_score=similarity,
                        rank=len(results)
                    )
                    results.append(result)
        
        # 按相似度排序
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        
        # 返回前top_k个
        return results[:query.top_k]
    
    def _calculate_cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        计算余弦相似度
        """
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return max(0.0, min(1.0, similarity))  # 确保在0-1范围内
    
    def _apply_filters(self, memory: Memory, filters: Dict[str, Any]) -> bool:
        """
        应用过滤器
        """
        if not filters:
            return True
        
        for key, value in filters.items():
            if key == "tags":
                if isinstance(value, list):
                    if not any(tag in memory.tags for tag in value):
                        return False
                else:
                    if value not in memory.tags:
                        return False
            elif key == "priority_min":
                if memory.priority < value:
                    return False
            elif key == "priority_max":
                if memory.priority > value:
                    return False
            elif key == "date_from":
                if memory.timestamp < value:
                    return False
            elif key == "date_to":
                if memory.timestamp > value:
                    return False
            elif key == "content_contains":
                if value.lower() not in memory.content.lower():
                    return False
        
        return True
    
    async def get_memory_by_id(self, memory_id: str) -> Optional[Memory]:
        """
        通过ID获取记忆
        """
        return self.memories.get(memory_id)
    
    async def delete_memory(self, memory_id: str) -> bool:
        """
        删除记忆
        """
        if memory_id not in self.memories:
            return False
        
        memory = self.memories[memory_id]
        
        # 从索引中移除
        for tag in memory.tags:
            if tag in self.tag_index and memory_id in self.tag_index[tag]:
                self.tag_index[tag].remove(memory_id)
        
        priority = memory.priority
        if priority in self.priority_index and memory_id in self.priority_index[priority]:
            self.priority_index[priority].remove(memory_id)
        
        date_key = memory.timestamp.strftime("%Y-%m-%d")
        if date_key in self.date_index and memory_id in self.date_index[date_key]:
            self.date_index[date_key].remove(memory_id)
        
        # 删除记忆
        del self.memories[memory_id]
        return True
    
    async def update_memory_metadata(self, memory_id: str, metadata: Dict[str, Any]) -> bool:
        """
        更新记忆元数据
        """
        if memory_id not in self.memories:
            return False
        
        memory = self.memories[memory_id]
        memory.metadata.update(metadata)
        return True
    
    def get_memory_count(self) -> int:
        """
        获取记忆总数
        """
        return len(self.memories)


class MemorySystem:
    """
    记忆系统主类
    基于 mempalace 的 AI 记忆系统架构
    """
    def __init__(self, persist_directory: str = "./memories", collection_name: str = "memories"):
        self.storage = VectorMemoryStore()
        self.persist_directory = persist_directory
        self.collection_name = collection_name
    
    async def remember(self, content: str, metadata: Dict[str, Any] = None, tags: List[str] = None, 
                      priority: int = 3) -> str:
        """
        记住新内容
        """
        memory = Memory(content=content, metadata=metadata, tags=tags or [], priority=priority)
        memory_id = await self.storage.store_memory(memory)
        
        print(f"🧠 记住了: {content[:50]}... (ID: {memory_id[:8]})")
        return memory_id
    
    async def recall(self, query: str, top_k: int = 5, threshold: float = 0.7, 
                    filters: Dict[str, Any] = None) -> List[MemoryResult]:
        """
        回忆相关内容
        """
        query_obj = MemoryQuery(query_text=query, filters=filters, top_k=top_k, threshold=threshold)
        results = await self.storage.search_memories(query_obj)
        
        print(f"🎯 找到 {len(results)} 个相关记忆，查询: '{query[:30]}...'")
        return results
    
    async def forget(self, memory_id: str) -> bool:
        """
        忘记指定记忆
        """
        success = await self.storage.delete_memory(memory_id)
        if success:
            print(f"🗑️ 忘记了记忆: {memory_id[:8]}")
        else:
            print(f"❌ 未能忘记记忆: {memory_id[:8]} (可能不存在)")
        return success
    
    async def associate(self, memory_id1: str, memory_id2: str) -> bool:
        """
        建立记忆关联
        """
        memory1 = await self.storage.get_memory_by_id(memory_id1)
        memory2 = await self.storage.get_memory_by_id(memory_id2)
        
        if not memory1 or not memory2:
            return False
        
        # 添加双向关联
        if memory_id2 not in memory1.relationships:
            memory1.relationships.append(memory_id2)
        if memory_id1 not in memory2.relationships:
            memory2.relationships.append(memory_id1)
        
        # 更新记忆
        await self.storage.update_memory_metadata(memory_id1, {"relationships": memory1.relationships})
        await self.storage.update_memory_metadata(memory_id2, {"relationships": memory2.relationships})
        
        print(f"🔗 关联了记忆: {memory_id1[:8]} ↔ {memory_id2[:8]}")
        return True
    
    async def batch_remember(self, contents: List[Dict[str, Any]]) -> List[str]:
        """
        批量记住内容
        """
        memories = []
        for item in contents:
            content = item.get('content', '')
            metadata = item.get('metadata', {})
            tags = item.get('tags', [])
            priority = item.get('priority', 3)
            
            memory = Memory(content=content, metadata=metadata, tags=tags, priority=priority)
            memories.append(memory)
        
        stored_ids = await self.storage.batch_store_memories(memories)
        print(f"📚 批量记住了 {len(stored_ids)} 个项目")
        return stored_ids
    
    async def find_related_memories(self, memory_id: str, top_k: int = 5) -> List[MemoryResult]:
        """
        查找相关的记忆
        """
        target_memory = await self.storage.get_memory_by_id(memory_id)
        if not target_memory:
            return []
        
        results = []
        
        # 1. 获取直接关联的记忆
        for related_id in target_memory.relationships[:top_k]:
            related_memory = await self.storage.get_memory_by_id(related_id)
            if related_memory:
                results.append(MemoryResult(
                    memory=related_memory,
                    similarity_score=0.9,  # 关联记忆给予高分
                    rank=len(results)
                ))
        
        # 2. 如果关联记忆不够，使用语义搜索
        if len(results) < top_k and target_memory:
            semantic_results = await self.recall(
                target_memory.content,
                top_k=top_k-len(results),
                threshold=0.3
            )
            results.extend(semantic_results)
        
        return results[:top_k]
    
    async def get_memory_statistics(self) -> Dict[str, Any]:
        """
        获取记忆统计信息
        """
        total_count = self.storage.get_memory_count()
        
        # 统计优先级分布
        priority_counts = {}
        for priority, memory_ids in self.storage.priority_index.items():
            priority_counts[priority] = len(memory_ids)
        
        # 统计标签分布（取前10个最常见的）
        tag_counts = {}
        for tag, memory_ids in self.storage.tag_index.items():
            tag_counts[tag] = len(memory_ids)
        
        # 排序并取前10个
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        common_tags = [{"tag": tag, "count": count} for tag, count in sorted_tags]
        
        stats = {
            "total_memories": total_count,
            "priority_distribution": priority_counts,
            "common_tags": common_tags,
            "embedding_dimension": 1536
        }
        
        return stats
    
    async def update_memory_priority(self, memory_id: str, priority: int) -> bool:
        """
        更新记忆优先级
        """
        memory = await self.storage.get_memory_by_id(memory_id)
        if not memory:
            return False
        
        memory.priority = min(max(priority, 1), 5)
        await self.storage.update_memory_metadata(memory_id, {"priority": memory.priority})
        
        print(f"⚡ 更新了记忆 {memory_id[:8]} 的优先级为 {priority}")
        return True
    
    async def cleanup_old_memories(self, days: int = 365, min_priority: int = 2) -> int:
        """
        清理旧记忆
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count = 0
        
        memories_to_delete = []
        for memory_id, memory in self.storage.memories.items():
            if memory.timestamp < cutoff_date and memory.priority < min_priority:
                memories_to_delete.append(memory_id)
        
        for memory_id in memories_to_delete:
            await self.storage.delete_memory(memory_id)
            deleted_count += 1
        
        print(f"🧹 清理了 {deleted_count} 条超过 {days} 天且优先级低于 {min_priority} 的记忆")
        return deleted_count


async def demonstrate_memory_system():
    """
    演示记忆系统功能
    """
    print("🧠=== 个人AI记忆系统演示 ===\n")
    
    # 创建记忆系统实例
    memory_system = MemorySystem()
    
    print("1. 📝 存储记忆...")
    
    # 存储一些记忆
    ml_memory_id = await memory_system.remember(
        content="机器学习中的梯度下降算法是优化模型参数的核心方法，通过计算损失函数的梯度来更新参数。",
        metadata={"category": "machine_learning", "difficulty": "advanced", "date": "2024-01-15"},
        tags=["machine_learning", "gradient_descent", "optimization", "algorithm"],
        priority=5
    )
    
    python_memory_id = await memory_system.remember(
        content="Python的async/await语法使得编写异步代码变得简单直观，适合处理I/O密集型任务。",
        metadata={"category": "programming", "difficulty": "intermediate", "date": "2024-01-10"},
        tags=["python", "async", "programming", "coroutine"],
        priority=4
    )
    
    nlp_memory_id = await memory_system.remember(
        content="自然语言处理中，Transformer架构使用自注意力机制，大大提升了处理长序列的能力。",
        metadata={"category": "nlp", "difficulty": "advanced", "date": "2024-01-12"},
        tags=["nlp", "transformer", "attention", "deep_learning"],
        priority=5
    )
    
    print(f"\n2. 🔍 搜索相关记忆...")
    
    # 搜索相关记忆
    results = await memory_system.recall("什么是梯度下降", top_k=3, threshold=0.6)
    print(f"搜索'什么是梯度下降'找到 {len(results)} 个结果:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result.memory.content[:80]}... (相似度: {result.similarity_score:.3f})")
    
    print(f"\n3. 🔗 建立记忆关联...")
    
    # 建立关联
    await memory_system.associate(ml_memory_id, nlp_memory_id)
    print("关联了机器学习和NLP记忆")
    
    print(f"\n4. 🔗 查找关联记忆...")
    
    related = await memory_system.find_related_memories(ml_memory_id, top_k=3)
    print(f"记忆 {ml_memory_id[:8]} 的相关记忆:")
    for i, result in enumerate(related, 1):
        print(f"  {i}. {result.memory.content[:60]}... (相似度: {result.similarity_score:.3f})")
    
    print(f"\n5. 📊 获取统计信息...")
    
    stats = await memory_system.get_memory_statistics()
    print(f"总记忆数: {stats['total_memories']}")
    print(f"优先级分布: {stats['priority_distribution']}")
    print(f"常见标签: {[tag_info['tag'] for tag_info in stats['common_tags'][:5]]}")
    
    print(f"\n6. ⚡ 更新记忆优先级...")
    
    await memory_system.update_memory_priority(python_memory_id, 5)
    
    print(f"\n7. 📦 批量存储记忆...")
    
    batch_contents = [
        {
            "content": "Python装饰器是一种强大的功能，可以在不修改原函数的情况下扩展函数行为。",
            "metadata": {"category": "programming"},
            "tags": ["python", "decorator", "functional_programming"],
            "priority": 4
        },
        {
            "content": "卷积神经网络在图像识别任务中表现出色，通过卷积层提取局部特征。",
            "metadata": {"category": "computer_vision"},
            "tags": ["cnn", "computer_vision", "deep_learning"],
            "priority": 5
        }
    ]
    
    batch_ids = await memory_system.batch_remember(batch_contents)
    print(f"批量存储了 {len(batch_ids)} 个记忆")
    
    print(f"\n8. 🎯 高级搜索（带过滤器）...")
    
    results = await memory_system.recall(
        "Python相关的内容", 
        top_k=5, 
        threshold=0.3,
        filters={"tags": ["python"]}
    )
    print(f"搜索带Python标签的记忆，找到 {len(results)} 个:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result.memory.content[:60]}...")
    
    print(f"\n9. 🧹 清理旧记忆演示...")
    
    # 这里只是演示接口，实际上不会有记忆被清理（因为都是刚创建的）
    cleaned = await memory_system.cleanup_old_memories(days=30, min_priority=3)
    print(f"清理了 {cleaned} 条旧记忆")
    
    print(f"\n🧠=== 记忆系统演示完成 ===")
    
    return memory_system


if __name__ == "__main__":
    # 运行演示
    asyncio.run(demonstrate_memory_system())