"""
记忆系统核心实现
整合存储、检索和管理功能
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import uuid
import hashlib
from .interfaces import Memory, MemoryQuery, MemoryResult, MemorySystemABC
from .storage.vector_store import VectorMemoryStore
from .utils.embedding_service import create_embedding_service, EmbeddingService


class MemorySystem(MemorySystemABC):
    """
    记忆系统核心实现
    基于 mempalace 的 AI 记忆系统架构
    """
    def __init__(
        self, 
        persist_directory: str = "./chroma_data", 
        collection_name: str = "memories",
        embedding_service_type: str = "mock",
        **embedding_kwargs
    ):
        self.storage = VectorMemoryStore(persist_directory, collection_name)
        self.embedding_service = create_embedding_service(embedding_service_type, **embedding_kwargs)
        self.logger = logging.getLogger(__name__)
        
        # 设置日志格式
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    async def remember(self, content: str, metadata: Dict[str, Any] = None, tags: List[str] = None, priority: int = 3) -> str:
        """
        记住新内容
        """
        try:
            # 生成嵌入向量
            embedding = self.embedding_service.embed_text(content)
            
            # 创建记忆对象
            memory_id = str(uuid.uuid4())
            memory = Memory(
                id=memory_id,
                content=content,
                embeddings=embedding,
                metadata=metadata or {},
                timestamp=datetime.now(),
                tags=tags or [],
                priority=min(max(priority, 1), 5),  # 限制在1-5之间
                relationships=[]
            )
            
            # 存储记忆
            stored_id = await self.storage.store_memory(memory)
            
            self.logger.info(f"New memory stored with ID: {stored_id}")
            return stored_id
            
        except Exception as e:
            self.logger.error(f"Error storing memory: {e}")
            raise
    
    async def recall(self, query: str, top_k: int = 5, threshold: float = 0.7) -> List[MemoryResult]:
        """
        回忆相关内容
        """
        try:
            # 生成查询嵌入
            query_embedding = self.embedding_service.embed_text(query)
            
            # 创建查询对象
            memory_query = MemoryQuery(
                query_text=query,
                query_embedding=query_embedding,
                top_k=top_k,
                threshold=threshold
            )
            
            # 执行搜索
            results = await self.storage.search_memories(memory_query)
            
            self.logger.info(f"Found {len(results)} relevant memories for query: '{query[:50]}...'")
            return results
            
        except Exception as e:
            self.logger.error(f"Error recalling memories: {e}")
            raise
    
    async def forget(self, memory_id: str) -> bool:
        """
        忘记指定记忆
        """
        try:
            success = await self.storage.delete_memory(memory_id)
            
            if success:
                self.logger.info(f"Memory forgotten: {memory_id}")
            else:
                self.logger.warning(f"Failed to forget memory: {memory_id} (not found)")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error forgetting memory: {e}")
            return False
    
    async def associate(self, memory_id1: str, memory_id2: str) -> bool:
        """
        建立记忆关联
        """
        try:
            # 获取两个记忆
            memory1 = await self.storage.get_memory_by_id(memory_id1)
            memory2 = await self.storage.get_memory_by_id(memory_id2)
            
            if not memory1 or not memory2:
                self.logger.warning(f"One or both memories not found: {memory_id1}, {memory_id2}")
                return False
            
            # 添加关联关系
            if memory_id2 not in memory1.relationships:
                memory1.relationships.append(memory_id2)
            
            if memory_id1 not in memory2.relationships:
                memory2.relationships.append(memory_id1)
            
            # 更新记忆
            await self.storage.update_memory_metadata(memory_id1, {"relationships": memory1.relationships})
            await self.storage.update_memory_metadata(memory_id2, {"relationships": memory2.relationships})
            
            self.logger.info(f"Association created between memories: {memory_id1} <-> {memory_id2}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error associating memories: {e}")
            return False
    
    async def batch_remember(self, contents: List[Dict[str, Any]]) -> List[str]:
        """
        批量记住内容
        contents: [{'content': '...', 'metadata': {...}, 'tags': [...], 'priority': 3}, ...]
        """
        try:
            memories = []
            
            for item in contents:
                content = item.get('content', '')
                metadata = item.get('metadata', {})
                tags = item.get('tags', [])
                priority = item.get('priority', 3)
                
                # 生成嵌入向量
                embedding = self.embedding_service.embed_text(content)
                
                # 创建记忆对象
                memory_id = str(uuid.uuid4())
                memory = Memory(
                    id=memory_id,
                    content=content,
                    embeddings=embedding,
                    metadata=metadata,
                    timestamp=datetime.now(),
                    tags=tags,
                    priority=min(max(priority, 1), 5),
                    relationships=[]
                )
                
                memories.append(memory)
            
            # 批量存储
            stored_ids = await self.storage.batch_store_memories(memories)
            
            self.logger.info(f"Batch stored {len(stored_ids)} memories")
            return stored_ids
            
        except Exception as e:
            self.logger.error(f"Error batch storing memories: {e}")
            raise
    
    async def search_by_tags(self, tags: List[str], top_k: int = 10) -> List[MemoryResult]:
        """
        按标签搜索记忆
        """
        try:
            # 这里需要从向量数据库中获取所有记忆并按标签过滤
            # 由于ChromaDB本身不直接支持复杂的元数据过滤，我们需要获取所有记忆
            # 实际应用中，可能需要额外的索引来优化此操作
            
            all_memories = []
            # 注意：这里是一个简化实现，实际可能需要更复杂的查询逻辑
            # 在真实应用中，可能需要结合SQL数据库或其他索引方案
            
            # 模拟按标签搜索
            results = []
            for memory in all_memories:
                if any(tag in memory.tags for tag in tags):
                    results.append(MemoryResult(
                        memory=memory,
                        similarity_score=1.0,  # 标签匹配视为完全相关
                        rank=len(results)
                    ))
            
            return results[:top_k]
            
        except Exception as e:
            self.logger.error(f"Error searching by tags: {e}")
            raise
    
    async def get_memory_statistics(self) -> Dict[str, Any]:
        """
        获取记忆统计信息
        """
        try:
            total_count = self.storage.get_memory_count()
            
            # 这里可以添加更详细的统计，如按标签、时间等分组
            stats = {
                "total_memories": total_count,
                "embedding_dimension": self.embedding_service.get_embedding_dimension(),
                "average_memory_age": "N/A",  # 需要计算
                "most_common_tags": [],  # 需要统计
                "memory_growth_rate": "N/A"  # 需要计算
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting memory statistics: {e}")
            raise
    
    async def find_related_memories(self, memory_id: str, top_k: int = 5) -> List[MemoryResult]:
        """
        查找相关的记忆（基于关联关系和语义相似性）
        """
        try:
            # 获取目标记忆
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
            
            # 2. 基于语义相似性查找
            if len(results) < top_k:
                semantic_results = await self.recall(
                    target_memory.content, 
                    top_k=top_k-len(results), 
                    threshold=0.5
                )
                results.extend(semantic_results)
            
            # 3. 确保结果数量不超过top_k
            return results[:top_k]
            
        except Exception as e:
            self.logger.error(f"Error finding related memories: {e}")
            raise
    
    async def update_memory_priority(self, memory_id: str, priority: int) -> bool:
        """
        更新记忆优先级
        """
        try:
            # 获取记忆
            memory = await self.storage.get_memory_by_id(memory_id)
            if not memory:
                return False
            
            # 更新优先级
            memory.priority = min(max(priority, 1), 5)
            
            # 更新元数据
            success = await self.storage.update_memory_metadata(
                memory_id, 
                {"priority": memory.priority}
            )
            
            if success:
                self.logger.info(f"Updated priority for memory {memory_id} to {priority}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error updating memory priority: {e}")
            return False
    
    async def cleanup_old_memories(self, days: int = 365, min_priority: int = 2) -> int:
        """
        清理旧记忆（保留高优先级记忆）
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # 获取所有记忆（这是一个简化实现）
            # 在实际应用中，可能需要更高效的查询方式
            # 这里只是占位符，实际实现需要考虑性能
            deleted_count = 0
            
            # 模拟清理过程
            self.logger.info(f"Cleanup initiated: removing memories older than {days} days with priority < {min_priority}")
            
            return deleted_count
            
        except Exception as e:
            self.logger.error(f"Error cleaning up old memories: {e}")
            raise


class AsyncMemorySystem(MemorySystem):
    """
    异步记忆系统实现
    为所有方法提供异步支持
    """
    pass


# 使用示例和测试
async def example_usage():
    """
    使用示例
    """
    # 创建记忆系统实例
    memory_system = MemorySystem(
        persist_directory="./test_memories",
        collection_name="test_collection",
        embedding_service_type="mock",  # 在生产环境中使用 "openai" 或 "sentence_transformer"
        dimension=1536
    )
    
    # 记住一些内容
    memory_id1 = await memory_system.remember(
        content="今天学习了Python的异步编程，async/await关键字非常有用。",
        metadata={"subject": "programming", "difficulty": "beginner"},
        tags=["python", "async", "programming"],
        priority=4
    )
    
    memory_id2 = await memory_system.remember(
        content="Python的装饰器是一种很强大的功能，可以修改函数的行为。",
        metadata={"subject": "programming", "difficulty": "intermediate"},
        tags=["python", "decorator", "programming"],
        priority=3
    )
    
    print(f"Stored memories with IDs: {memory_id1}, {memory_id2}")
    
    # 建立关联
    await memory_system.associate(memory_id1, memory_id2)
    print(f"Associated memories: {memory_id1} <-> {memory_id2}")
    
    # 回忆相关内容
    results = await memory_system.recall("Python异步编程", top_k=3, threshold=0.5)
    print(f"Recall results: {len(results)} memories found")
    
    for result in results:
        print(f"  - {result.memory.content[:50]}... (similarity: {result.similarity_score:.3f})")
    
    # 查找相关记忆
    related = await memory_system.find_related_memories(memory_id1, top_k=3)
    print(f"Related memories: {len(related)} found")
    
    # 获取统计信息
    stats = await memory_system.get_memory_statistics()
    print(f"Memory statistics: {stats}")


# 如果直接运行此文件，执行示例
if __name__ == "__main__":
    # 注意：这只是一个示例，实际运行需要适当的环境设置
    pass