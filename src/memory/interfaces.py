"""
记忆系统模块接口定义
基于 mempalace 的 AI 记忆系统架构
"""
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, Optional, List, Dict, Any, Union
from dataclasses import dataclass
from datetime import datetime
import numpy as np


@dataclass
class Memory:
    """
    记忆对象数据结构
    """
    id: str
    content: str
    embeddings: List[float]
    metadata: Dict[str, Any]
    timestamp: datetime
    tags: List[str]
    priority: int  # 1-5
    relationships: List[str]  # 关联记忆ID列表
    access_count: int = 0
    last_access: Optional[datetime] = None


@dataclass
class MemoryQuery:
    """
    记忆查询对象
    """
    query_text: str
    query_embedding: Optional[List[float]] = None
    filters: Optional[Dict[str, Any]] = None
    top_k: int = 10
    threshold: float = 0.7


@dataclass
class MemoryResult:
    """
    记忆查询结果
    """
    memory: Memory
    similarity_score: float
    rank: int


@runtime_checkable
class MemoryStorage(Protocol):
    """
    记忆存储接口
    """
    async def store(self, memory: Memory) -> str:
        """存储记忆"""
        ...
    
    async def batch_store(self, memories: List[Memory]) -> List[str]:
        """批量存储记忆"""
        ...
    
    async def retrieve(self, memory_id: str) -> Optional[Memory]:
        """检索单个记忆"""
        ...
    
    async def delete(self, memory_id: str) -> bool:
        """删除记忆"""
        ...
    
    async def update(self, memory: Memory) -> bool:
        """更新记忆"""
        ...


@runtime_checkable
class MemoryRetrieval(Protocol):
    """
    记忆检索接口
    """
    async def semantic_search(self, query: MemoryQuery) -> List[MemoryResult]:
        """语义搜索"""
        ...
    
    async def find_similar(self, memory_id: str, top_k: int = 5) -> List[MemoryResult]:
        """查找相似记忆"""
        ...
    
    async def search_by_tags(self, tags: List[str], top_k: int = 10) -> List[MemoryResult]:
        """按标签搜索"""
        ...
    
    async def temporal_search(self, start_date: datetime, end_date: datetime) -> List[MemoryResult]:
        """时间范围搜索"""
        ...


@runtime_checkable
class MemoryManagement(Protocol):
    """
    记忆管理接口
    """
    async def get_statistics(self) -> Dict[str, Any]:
        """获取记忆统计"""
        ...
    
    async def get_memory_timeline(self, days: int = 30) -> List[Memory]:
        """获取记忆时间线"""
        ...
    
    async def cleanup_old_memories(self, days: int = 365) -> int:
        """清理旧记忆"""
        ...
    
    async def update_memory_priority(self, memory_id: str, priority: int) -> bool:
        """更新记忆优先级"""
        ...


class MemorySystemABC(ABC):
    """
    记忆系统抽象基类
    """
    @abstractmethod
    async def remember(self, content: str, metadata: Dict[str, Any] = None, tags: List[str] = None) -> str:
        """记住新内容"""
        pass
    
    @abstractmethod
    async def recall(self, query: str, top_k: int = 5, threshold: float = 0.7) -> List[MemoryResult]:
        """回忆相关内容"""
        pass
    
    @abstractmethod
    async def forget(self, memory_id: str) -> bool:
        """忘记指定记忆"""
        pass
    
    @abstractmethod
    async def associate(self, memory_id1: str, memory_id2: str) -> bool:
        """建立记忆关联"""
        pass