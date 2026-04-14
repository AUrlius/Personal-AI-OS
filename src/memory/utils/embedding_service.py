"""
嵌入服务实现
提供文本到向量的转换功能
"""
import numpy as np
from typing import List, Union
import logging
from abc import ABC, abstractmethod
import asyncio
import hashlib


class EmbeddingService(ABC):
    """
    嵌入服务抽象接口
    """
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """
        将文本转换为嵌入向量
        """
        pass
    
    @abstractmethod
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        将多个文本转换为嵌入向量
        """
        pass
    
    @abstractmethod
    def get_embedding_dimension(self) -> int:
        """
        获取嵌入向量的维度
        """
        pass


class MockEmbeddingService(EmbeddingService):
    """
    模拟嵌入服务 - 用于测试和开发初期
    实际部署时应替换为真实的嵌入模型
    """
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.logger = logging.getLogger(__name__)
    
    def embed_text(self, text: str) -> List[float]:
        """
        使用哈希函数生成伪嵌入向量
        在实际应用中，这里应该调用真实的嵌入模型
        """
        # 使用文本内容作为种子生成确定性随机向量
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        
        # 将哈希转换为随机数种子
        seed = int(text_hash[:8], 16)  # 使用前8位十六进制字符
        np.random.seed(seed % (2**32))  # 确保种子在合适范围内
        
        # 生成指定维度的随机向量
        vector = np.random.random(self.dimension).tolist()
        
        # 归一化向量（单位向量）
        norm = np.linalg.norm(vector)
        if norm != 0:
            vector = (np.array(vector) / norm).tolist()
        
        self.logger.debug(f"Generated embedding for text: '{text[:50]}...' with shape ({self.dimension},)")
        return vector
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        批量嵌入文本
        """
        embeddings = []
        for text in texts:
            embeddings.append(self.embed_text(text))
        return embeddings
    
    def get_embedding_dimension(self) -> int:
        """
        获取嵌入维度
        """
        return self.dimension


class CachedEmbeddingService(EmbeddingService):
    """
    带缓存的嵌入服务包装器
    """
    def __init__(self, embedding_service: EmbeddingService, cache_size: int = 1000):
        self.service = embedding_service
        self.cache = {}
        self.cache_order = []  # 用于LRU淘汰
        self.cache_size = cache_size
        self.logger = logging.getLogger(__name__)
    
    def embed_text(self, text: str) -> List[float]:
        """
        带缓存的文本嵌入
        """
        # 检查缓存
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        if text_hash in self.cache:
            self.logger.debug(f"Cache hit for text: '{text[:50]}...'")
            # 更新使用顺序
            if text_hash in self.cache_order:
                self.cache_order.remove(text_hash)
            self.cache_order.append(text_hash)
            return self.cache[text_hash]
        
        # 生成嵌入
        embedding = self.service.embed_text(text)
        
        # 添加到缓存
        self._add_to_cache(text_hash, embedding, text)
        
        return embedding
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        批量嵌入，带缓存
        """
        embeddings = []
        for text in texts:
            embeddings.append(self.embed_text(text))
        return embeddings
    
    def get_embedding_dimension(self) -> int:
        """
        获取嵌入维度
        """
        return self.service.get_embedding_dimension()
    
    def _add_to_cache(self, text_hash: str, embedding: List[float], text: str):
        """
        添加到缓存，必要时进行LRU淘汰
        """
        if len(self.cache) >= self.cache_size:
            # LRU淘汰
            oldest_hash = self.cache_order.pop(0)
            del self.cache[oldest_hash]
            self.logger.debug(f"Cache eviction: removed oldest entry")
        
        self.cache[text_hash] = embedding
        self.cache_order.append(text_hash)
        self.logger.debug(f"Added to cache: '{text[:50]}...'")
    
    def clear_cache(self):
        """
        清空缓存
        """
        self.cache.clear()
        self.cache_order.clear()
        self.logger.info("Embedding cache cleared")


class OpenAIEmbeddingService(EmbeddingService):
    """
    OpenAI 嵌入服务实现
    注意：需要设置 OPENAI_API_KEY 环境变量
    """
    def __init__(self, model: str = "text-embedding-ada-002", dimension: int = 1536):
        self.model = model
        self.dimension = dimension
        self.logger = logging.getLogger(__name__)
        self._client = None
    
    def _get_client(self):
        """
        延迟加载OpenAI客户端
        """
        if self._client is None:
            try:
                import openai
                self._client = openai.AsyncOpenAI()  # 使用异步客户端
            except ImportError:
                raise ImportError("Please install openai package: pip install openai")
        return self._client
    
    async def embed_text(self, text: str) -> List[float]:
        """
        异步嵌入单个文本
        """
        client = self._get_client()
        
        try:
            response = await client.embeddings.create(
                input=text,
                model=self.model
            )
            embedding = response.data[0].embedding
            self.logger.debug(f"OpenAI embedding generated for text: '{text[:50]}...' with shape ({len(embedding)},)")
            return embedding
        except Exception as e:
            self.logger.error(f"Error calling OpenAI embedding API: {e}")
            raise
    
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        异步批量嵌入文本
        """
        client = self._get_client()
        
        try:
            response = await client.embeddings.create(
                input=texts,
                model=self.model
            )
            embeddings = [data.embedding for data in response.data]
            self.logger.debug(f"OpenAI batch embedding generated for {len(texts)} texts")
            return embeddings
        except Exception as e:
            self.logger.error(f"Error calling OpenAI batch embedding API: {e}")
            raise
    
    def get_embedding_dimension(self) -> int:
        """
        获取嵌入维度
        """
        return self.dimension


class SentenceTransformerEmbeddingService(EmbeddingService):
    """
    Sentence Transformer 嵌入服务实现
    本地运行，无需API密钥
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", dimension: int = 384):
        self.model_name = model_name
        self.dimension = dimension
        self.logger = logging.getLogger(__name__)
        self._model = None
    
    def _get_model(self):
        """
        延迟加载模型
        """
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self.logger.info(f"Loading sentence transformer model: {self.model_name}")
                self._model = SentenceTransformer(self.model_name)
            except ImportError:
                raise ImportError("Please install sentence-transformers: pip install sentence-transformers")
        return self._model
    
    def embed_text(self, text: str) -> List[float]:
        """
        嵌入单个文本
        """
        model = self._get_model()
        embedding = model.encode([text])[0].tolist()
        self.logger.debug(f"SentenceTransformer embedding generated for text: '{text[:50]}...' with shape ({len(embedding)},)")
        return embedding
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        批量嵌入文本
        """
        model = self._get_model()
        embeddings = model.encode(texts).tolist()
        self.logger.debug(f"SentenceTransformer batch embedding generated for {len(texts)} texts")
        return embeddings
    
    def get_embedding_dimension(self) -> int:
        """
        获取嵌入维度
        """
        return self.dimension


# 工厂模式创建嵌入服务
def create_embedding_service(service_type: str = "mock", **kwargs) -> EmbeddingService:
    """
    创建嵌入服务的工厂函数
    """
    if service_type == "mock":
        return MockEmbeddingService(kwargs.get("dimension", 1536))
    elif service_type == "openai":
        return CachedEmbeddingService(
            OpenAIEmbeddingService(
                kwargs.get("model", "text-embedding-ada-002"),
                kwargs.get("dimension", 1536)
            )
        )
    elif service_type == "sentence_transformer":
        return CachedEmbeddingService(
            SentenceTransformerEmbeddingService(
                kwargs.get("model_name", "all-MiniLM-L6-v2"),
                kwargs.get("dimension", 384)
            )
        )
    else:
        raise ValueError(f"Unknown embedding service type: {service_type}")