"""
简化版记忆系统测试
不依赖外部库，验证核心逻辑
"""
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional


class SimpleMemory:
    """
    简化版记忆类
    """
    def __init__(self, content: str, metadata: Dict = None, tags: List[str] = None, priority: int = 3):
        self.id = str(uuid.uuid4())
        self.content = content
        self.metadata = metadata or {}
        self.tags = tags or []
        self.priority = min(max(priority, 1), 5)  # 限制在1-5之间
        self.timestamp = datetime.now().isoformat()
        self.relationships = []
        self.access_count = 0
        self.embeddings = [0.0] * 1536  # 模拟嵌入向量


class SimpleMemorySystem:
    """
    简化版记忆系统，用于测试核心逻辑
    """
    def __init__(self):
        self.memories = {}  # id -> SimpleMemory
        self.tag_index = {}  # tag -> [memory_ids]
        self.content_to_id = {}  # content -> id (用于模拟相似度搜索)
    
    async def remember(self, content: str, metadata: Dict = None, tags: List[str] = None, priority: int = 3) -> str:
        """
        记住新内容
        """
        memory = SimpleMemory(content, metadata, tags, priority)
        self.memories[memory.id] = memory
        
        # 构建标签索引
        for tag in memory.tags:
            if tag not in self.tag_index:
                self.tag_index[tag] = []
            self.tag_index[tag].append(memory.id)
        
        # 构建内容索引（用于模拟相似度搜索）
        self.content_to_id[content.lower()] = memory.id
        
        print(f"记住: {content[:50]}... (ID: {memory.id[:8]})")
        return memory.id
    
    async def recall(self, query: str, top_k: int = 5, threshold: float = 0.7) -> List[Dict]:
        """
        回忆相关内容 - 简化版相似度搜索
        """
        results = []
        query_lower = query.lower()
        
        for memory_id, memory in self.memories.items():
            # 简单的文本匹配模拟
            similarity = self._calculate_similarity(query_lower, memory.content.lower())
            
            if similarity >= threshold:
                results.append({
                    'memory': memory,
                    'similarity_score': similarity,
                    'rank': len(results)
                })
        
        # 按相似度排序
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return results[:top_k]
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        简单的相似度计算（基于公共词汇比例）
        """
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        # Jaccard相似度
        return len(intersection) / len(union)
    
    async def forget(self, memory_id: str) -> bool:
        """
        忘记指定记忆
        """
        if memory_id in self.memories:
            memory = self.memories[memory_id]
            
            # 从标签索引中移除
            for tag in memory.tags:
                if tag in self.tag_index and memory_id in self.tag_index[tag]:
                    self.tag_index[tag].remove(memory_id)
            
            # 从内容索引中移除
            if memory.content.lower() in self.content_to_id:
                del self.content_to_id[memory.content.lower()]
            
            # 删除记忆
            del self.memories[memory_id]
            print(f"忘记: {memory_id[:8]}")
            return True
        return False
    
    async def associate(self, memory_id1: str, memory_id2: str) -> bool:
        """
        建立记忆关联
        """
        if memory_id1 in self.memories and memory_id2 in self.memories:
            if memory_id2 not in self.memories[memory_id1].relationships:
                self.memories[memory_id1].relationships.append(memory_id2)
            if memory_id1 not in self.memories[memory_id2].relationships:
                self.memories[memory_id2].relationships.append(memory_id1)
            print(f"关联: {memory_id1[:8]} <-> {memory_id2[:8]}")
            return True
        return False
    
    def get_memory_count(self) -> int:
        """
        获取记忆总数
        """
        return len(self.memories)
    
    async def find_related_memories(self, memory_id: str, top_k: int = 5) -> List[Dict]:
        """
        查找相关记忆
        """
        if memory_id not in self.memories:
            return []
        
        results = []
        memory = self.memories[memory_id]
        
        # 返回直接关联的记忆
        for related_id in memory.relationships[:top_k]:
            if related_id in self.memories:
                results.append({
                    'memory': self.memories[related_id],
                    'similarity_score': 0.9,  # 关联记忆给予高分
                    'rank': len(results)
                })
        
        return results


async def test_simple_memory_system():
    """
    测试简化版记忆系统
    """
    print("🧪 开始测试简化版记忆系统...\n")
    
    # 创建记忆系统
    memory_system = SimpleMemorySystem()
    
    print("1. 存储记忆...")
    
    # 存储一些记忆
    id1 = await memory_system.remember(
        "今天学习了Python的async/await特性，非常有用",
        metadata={"subject": "programming"},
        tags=["python", "async", "learning"],
        priority=4
    )
    
    id2 = await memory_system.remember(
        "Python的装饰器是一种强大的功能，可以修改函数行为",
        metadata={"subject": "programming"},
        tags=["python", "decorator", "advanced"],
        priority=3
    )
    
    id3 = await memory_system.remember(
        "机器学习中的梯度下降是优化模型的核心算法",
        metadata={"subject": "ML"},
        tags=["machine_learning", "gradient_descent", "optimization"],
        priority=5
    )
    
    print(f"\n2. 当前记忆总数: {memory_system.get_memory_count()}")
    
    print("\n3. 搜索相关记忆...")
    
    # 搜索相关记忆
    results = await memory_system.recall("Python编程", top_k=5, threshold=0.1)
    print(f"搜索 'Python编程' 找到 {len(results)} 个结果:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result['memory'].content[:50]}... (相似度: {result['similarity_score']:.3f})")
    
    print("\n4. 建立记忆关联...")
    
    # 建立关联
    await memory_system.associate(id1, id2)
    
    print("\n5. 查找关联记忆...")
    
    # 查找关联记忆
    related = await memory_system.find_related_memories(id1, top_k=3)
    print(f"记忆 {id1[:8]} 的关联记忆:")
    for i, result in enumerate(related, 1):
        print(f"  {i}. {result['memory'].content[:50]}...")
    
    print("\n6. 删除记忆测试...")
    
    # 删除记忆
    success = await memory_system.forget(id3)
    print(f"删除记忆 {id3[:8]}: {'成功' if success else '失败'}")
    print(f"删除后的记忆总数: {memory_system.get_memory_count()}")
    
    print("\n✅ 简化版记忆系统测试完成！")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_simple_memory_system())