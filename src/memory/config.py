"""
记忆系统配置管理
"""
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import json


@dataclass
class MemoryConfig:
    """
    记忆系统配置
    """
    # 存储配置
    persist_directory: str = "./chroma_data"
    collection_name: str = "memories"
    
    # 嵌入服务配置
    embedding_service_type: str = "mock"  # "mock", "openai", "sentence_transformer"
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_dimension: int = 384
    
    # 记忆管理配置
    max_memory_count: int = 10000
    default_priority: int = 3
    retention_days: int = 365
    
    # 检索配置
    default_top_k: int = 10
    default_threshold: float = 0.7
    
    # 性能配置
    cache_size: int = 1000
    batch_size: int = 10
    
    def save_to_file(self, config_path: str):
        """
        保存配置到文件
        """
        config_dict = asdict(self)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, config_path: str) -> 'MemoryConfig':
        """
        从文件加载配置
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)
        return cls(**config_dict)
    
    @classmethod
    def from_env(cls) -> 'MemoryConfig':
        """
        从环境变量创建配置
        """
        config_dict = {}
        
        # 存储配置
        if os.getenv('MEMORY_PERSIST_DIR'):
            config_dict['persist_directory'] = os.getenv('MEMORY_PERSIST_DIR')
        if os.getenv('MEMORY_COLLECTION_NAME'):
            config_dict['collection_name'] = os.getenv('MEMORY_COLLECTION_NAME')
        
        # 嵌入服务配置
        if os.getenv('EMBEDDING_SERVICE_TYPE'):
            config_dict['embedding_service_type'] = os.getenv('EMBEDDING_SERVICE_TYPE')
        if os.getenv('EMBEDDING_MODEL'):
            config_dict['embedding_model'] = os.getenv('EMBEDDING_MODEL')
        if os.getenv('EMBEDDING_DIMENSION'):
            config_dict['embedding_dimension'] = int(os.getenv('EMBEDDING_DIMENSION'))
        
        # 记忆管理配置
        if os.getenv('MAX_MEMORY_COUNT'):
            config_dict['max_memory_count'] = int(os.getenv('MAX_MEMORY_COUNT'))
        if os.getenv('DEFAULT_PRIORITY'):
            config_dict['default_priority'] = int(os.getenv('DEFAULT_PRIORITY'))
        if os.getenv('RETENTION_DAYS'):
            config_dict['retention_days'] = int(os.getenv('RETENTION_DAYS'))
        
        # 检索配置
        if os.getenv('DEFAULT_TOP_K'):
            config_dict['default_top_k'] = int(os.getenv('DEFAULT_TOP_K'))
        if os.getenv('DEFAULT_THRESHOLD'):
            config_dict['default_threshold'] = float(os.getenv('DEFAULT_THRESHOLD'))
        
        # 性能配置
        if os.getenv('CACHE_SIZE'):
            config_dict['cache_size'] = int(os.getenv('CACHE_SIZE'))
        if os.getenv('BATCH_SIZE'):
            config_dict['batch_size'] = int(os.getenv('BATCH_SIZE'))
        
        return cls(**config_dict)


class ConfigManager:
    """
    配置管理器
    """
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "./memory_config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> MemoryConfig:
        """
        加载配置，优先级：文件 > 环境变量 > 默认值
        """
        # 首先尝试从文件加载
        if Path(self.config_path).exists():
            try:
                return MemoryConfig.load_from_file(self.config_path)
            except Exception as e:
                print(f"Warning: Could not load config from {self.config_path}: {e}")
        
        # 然后尝试从环境变量加载
        try:
            env_config = MemoryConfig.from_env()
            # 如果环境变量中有配置，则保存到文件
            if any(value != getattr(MemoryConfig(), key) for key, value in asdict(env_config).items()):
                self.save_config(env_config)
            return env_config
        except Exception:
            pass
        
        # 使用默认配置
        default_config = MemoryConfig()
        self.save_config(default_config)
        return default_config
    
    def get_config(self) -> MemoryConfig:
        """
        获取当前配置
        """
        return self.config
    
    def update_config(self, **kwargs) -> MemoryConfig:
        """
        更新配置
        """
        # 更新当前配置
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        
        # 保存到文件
        self.save_config(self.config)
        return self.config
    
    def save_config(self, config: MemoryConfig = None):
        """
        保存配置到文件
        """
        config = config or self.config
        config.save_to_file(self.config_path)
        print(f"Configuration saved to {self.config_path}")
    
    def reset_to_defaults(self) -> MemoryConfig:
        """
        重置为默认配置
        """
        self.config = MemoryConfig()
        self.save_config()
        return self.config


# 全局配置实例
_config_manager: Optional[ConfigManager] = None


def get_config_manager(config_path: Optional[str] = None) -> ConfigManager:
    """
    获取全局配置管理器实例
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_path)
    return _config_manager


def get_memory_config() -> MemoryConfig:
    """
    获取记忆系统配置
    """
    manager = get_config_manager()
    return manager.get_config()


def update_memory_config(**kwargs) -> MemoryConfig:
    """
    更新记忆系统配置
    """
    manager = get_config_manager()
    return manager.update_config(**kwargs)


# 配置验证
def validate_config(config: MemoryConfig) -> Dict[str, Any]:
    """
    验证配置的有效性
    """
    errors = []
    
    # 验证优先级范围
    if not 1 <= config.default_priority <= 5:
        errors.append("default_priority must be between 1 and 5")
    
    if not 1 <= config.max_memory_count:
        errors.append("max_memory_count must be positive")
    
    if not 1 <= config.retention_days:
        errors.append("retention_days must be positive")
    
    if not 0 < config.default_threshold <= 1:
        errors.append("default_threshold must be between 0 and 1")
    
    if not 1 <= config.default_top_k <= 100:
        errors.append("default_top_k must be between 1 and 100")
    
    if not 1 <= config.cache_size:
        errors.append("cache_size must be positive")
    
    if not 1 <= config.batch_size <= 100:
        errors.append("batch_size must be between 1 and 100")
    
    # 验证嵌入服务类型
    valid_services = ["mock", "openai", "sentence_transformer"]
    if config.embedding_service_type not in valid_services:
        errors.append(f"embedding_service_type must be one of {valid_services}")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": []
    }


# 初始化配置
def init_config(config_path: Optional[str] = None):
    """
    初始化配置
    """
    manager = get_config_manager(config_path)
    config = manager.get_config()
    
    # 验证配置
    validation_result = validate_config(config)
    if not validation_result["valid"]:
        raise ValueError(f"Invalid configuration: {validation_result['errors']}")
    
    return config