"""
记忆系统模块初始化
"""
from .core import MemorySystem, AsyncMemorySystem
from .interfaces import Memory, MemoryQuery, MemoryResult
from .config import (
    MemoryConfig, 
    ConfigManager, 
    get_config_manager, 
    get_memory_config, 
    update_memory_config,
    init_config
)
from .utils.embedding_service import (
    EmbeddingService,
    MockEmbeddingService,
    CachedEmbeddingService,
    create_embedding_service
)
from .storage.vector_store import VectorMemoryStore

__version__ = "1.0.0"
__all__ = [
    # 核心类
    "MemorySystem",
    "AsyncMemorySystem",
    
    # 数据模型
    "Memory",
    "MemoryQuery", 
    "MemoryResult",
    
    # 配置相关
    "MemoryConfig",
    "ConfigManager",
    "get_config_manager",
    "get_memory_config", 
    "update_memory_config",
    "init_config",
    
    # 嵌入服务
    "EmbeddingService",
    "MockEmbeddingService", 
    "CachedEmbeddingService",
    "create_embedding_service",
    
    # 存储
    "VectorMemoryStore"
]

# 初始化日志配置
import logging

def setup_logging(level=logging.INFO):
    """
    设置日志配置
    """
    logger = logging.getLogger(__name__.split('.')[0])  # 获取根logger
    logger.setLevel(level)
    
    # 避免重复添加handler
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


# 默认初始化
logger = setup_logging()