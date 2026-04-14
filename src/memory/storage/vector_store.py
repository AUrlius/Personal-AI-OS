"""
向量存储实现
基于 ChromaDB 的向量存储系统
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import numpy as np
import logging
from ..interfaces import Memory, MemoryResult, MemoryQuery
import uuid


class VectorMemoryStore:
    """
    基于 ChromaDB 的向量存储实现
    """
    def __init__(self, persist_directory: str = "./chroma_data", collection_name: str = "memories"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection_name = collection_name
        
        # 获取或创建集合
        try:
            self.collection = self.client.get_collection(name=collection_name)
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}  # 使用余弦距离
            )
        
        self.logger = logging.getLogger(__name__)
    
    async def store_memory(self, memory: Memory) -> str:
        """
        存储记忆到向量数据库
        """
        try:
            memory_id = memory.id or str(uuid.uuid4())
            
            # 将记忆数据转换为向量数据库格式
            self.collection.add(
                documents=[memory.content],
                embeddings=[memory.embeddings],
                metadatas=[{
                    "id": memory_id,
                    "timestamp": memory.timestamp.isoformat(),
                    "tags": ",".join(memory.tags),
                    "priority": str(memory.priority),
                    "access_count": str(memory.access_count),
                    "metadata": str(memory.metadata)
                }],
                ids=[memory_id]
            )
            
            self.logger.info(f"Memory stored with ID: {memory_id}")
            return memory_id
            
        except Exception as e:
            self.logger.error(f"Error storing memory: {e}")
            raise
    
    async def batch_store_memories(self, memories: List[Memory]) -> List[str]:
        """
        批量存储记忆
        """
        try:
            ids = []
            documents = []
            embeddings = []
            metadatas = []
            
            for memory in memories:
                memory_id = memory.id or str(uuid.uuid4())
                ids.append(memory_id)
                documents.append(memory.content)
                embeddings.append(memory.embeddings)
                metadatas.append({
                    "id": memory_id,
                    "timestamp": memory.timestamp.isoformat(),
                    "tags": ",".join(memory.tags),
                    "priority": str(memory.priority),
                    "access_count": str(memory.access_count),
                    "metadata": str(memory.metadata)
                })
            
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            self.logger.info(f"Batch stored {len(memories)} memories")
            return ids
            
        except Exception as e:
            self.logger.error(f"Error batch storing memories: {e}")
            raise
    
    async def search_memories(self, query: MemoryQuery) -> List[MemoryResult]:
        """
        搜索记忆
        """
        try:
            if query.query_embedding is None:
                raise ValueError("Query embedding is required for vector search")
            
            # 执行向量搜索
            results = self.collection.query(
                query_embeddings=[query.query_embedding],
                n_results=query.top_k,
                include=["documents", "metadatas", "distances"]
            )
            
            memory_results = []
            for i in range(len(results["ids"][0])):
                distance = results["distances"][0][i]
                # 转换距离为相似度分数 (0-1之间，越接近1越相似)
                similarity_score = 1 - distance if distance <= 1 else 0
                
                if similarity_score >= query.threshold:
                    metadata = results["metadatas"][0][i]
                    memory_result = MemoryResult(
                        memory=Memory(
                            id=metadata["id"],
                            content=results["documents"][0][i],
                            embeddings=[],  # 在实际使用中可能需要重新获取
                            metadata=eval(metadata["metadata"]) if metadata["metadata"] else {},
                            timestamp=datetime.fromisoformat(metadata["timestamp"]),
                            tags=metadata["tags"].split(",") if metadata["tags"] else [],
                            priority=int(metadata["priority"]),
                            relationships=[],
                            access_count=int(metadata["access_count"])
                        ),
                        similarity_score=similarity_score,
                        rank=i
                    )
                    memory_results.append(memory_result)
            
            # 按相似度排序
            memory_results.sort(key=lambda x: x.similarity_score, reverse=True)
            
            return memory_results
            
        except Exception as e:
            self.logger.error(f"Error searching memories: {e}")
            raise
    
    async def get_memory_by_id(self, memory_id: str) -> Optional[Memory]:
        """
        通过ID获取记忆
        """
        try:
            result = self.collection.get(
                ids=[memory_id],
                include=["documents", "metadatas", "embeddings"]
            )
            
            if not result["ids"]:
                return None
            
            metadata = result["metadatas"][0][0]
            return Memory(
                id=metadata["id"],
                content=result["documents"][0][0],
                embeddings=result["embeddings"][0][0] if result["embeddings"] else [],
                metadata=eval(metadata["metadata"]) if metadata["metadata"] else {},
                timestamp=datetime.fromisoformat(metadata["timestamp"]),
                tags=metadata["tags"].split(",") if metadata["tags"] else [],
                priority=int(metadata["priority"]),
                relationships=[],
                access_count=int(metadata["access_count"])
            )
            
        except Exception as e:
            self.logger.error(f"Error getting memory by ID: {e}")
            return None
    
    async def delete_memory(self, memory_id: str) -> bool:
        """
        删除记忆
        """
        try:
            self.collection.delete(ids=[memory_id])
            self.logger.info(f"Memory deleted: {memory_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting memory: {e}")
            return False
    
    async def update_memory_metadata(self, memory_id: str, metadata: Dict[str, Any]) -> bool:
        """
        更新记忆元数据
        """
        # 由于ChromaDB不直接支持更新，我们需要删除并重新添加
        memory = await self.get_memory_by_id(memory_id)
        if memory:
            memory.metadata.update(metadata)
            await self.delete_memory(memory_id)
            await self.store_memory(memory)
            return True
        return False
    
    def get_memory_count(self) -> int:
        """
        获取记忆总数
        """
        return self.collection.count()


# 为了兼容性，添加一个简单的向量相似度计算器
def calculate_cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    计算两个向量的余弦相似度
    """
    # 转换为numpy数组
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    
    # 计算余弦相似度
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    
    return float(dot_product / (norm_v1 * norm_v2))


def find_most_similar_vectors(target_vector: List[float], 
                            candidate_vectors: List[List[float]], 
                            top_k: int = 5) -> List[tuple]:
    """
    找到最相似的向量
    """
    similarities = []
    for i, candidate in enumerate(candidate_vectors):
        sim = calculate_cosine_similarity(target_vector, candidate)
        similarities.append((i, sim))
    
    # 按相似度排序
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]