"""
技能系统配置管理
"""
import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class SkillSystemConfig:
    """
    技能系统配置
    """
    # 注册表配置
    registry_type: str = "in_memory"  # "in_memory", "persistent", "redis"
    registry_storage_path: str = "./skills_data"
    
    # 执行器配置
    executor_type: str = "advanced"  # "basic", "advanced"
    execution_timeout: int = 30  # 秒
    max_concurrent_executions: int = 10
    
    # 沙箱配置
    sandbox_type: str = "default"  # "default", "docker", "python", "javascript"
    sandbox_timeout: int = 30
    sandbox_max_memory: int = 128  # MB
    sandbox_allowed_languages: list = None
    
    # 安全配置
    enable_code_validation: bool = True
    enable_permission_check: bool = True
    max_code_size: int = 1024 * 100  # 100KB
    allowed_permissions: list = None
    
    # 缓存配置
    enable_cache: bool = True
    cache_ttl: int = 3600  # 秒
    cache_size_limit: int = 1000
    
    # 监控配置
    enable_monitoring: bool = True
    log_level: str = "INFO"
    metrics_collection_interval: int = 60  # 秒
    
    # 初始化默认值
    def __post_init__(self):
        if self.sandbox_allowed_languages is None:
            self.sandbox_allowed_languages = ["python", "javascript", "shell"]
        if self.allowed_permissions is None:
            self.allowed_permissions = [
                "network", "filesystem", "database", "camera", 
                "microphone", "location", "clipboard", "notifications"
            ]


class ConfigManager:
    """
    配置管理器
    """
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "./skill_system_config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> SkillSystemConfig:
        """
        加载配置，优先级：文件 > 环境变量 > 默认值
        """
        # 首先尝试从文件加载
        if Path(self.config_path).exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config_dict = json.load(f)
                
                # 将字典转换为配置对象
                config = SkillSystemConfig(**config_dict)
                print(f"Configuration loaded from {self.config_path}")
                return config
            except Exception as e:
                print(f"Warning: Could not load config from {self.config_path}: {e}")
        
        # 然后尝试从环境变量加载
        try:
            config = self._load_from_env()
            if config:
                self.save_config(config)
                return config
        except Exception as e:
            print(f"Warning: Could not load config from environment: {e}")
        
        # 使用默认配置
        config = SkillSystemConfig()
        self.save_config(config)
        print("Using default configuration")
        return config
    
    def _load_from_env(self) -> Optional[SkillSystemConfig]:
        """
        从环境变量加载配置
        """
        config_dict = {}
        
        # 注册表配置
        if os.getenv('SKILL_REGISTRY_TYPE'):
            config_dict['registry_type'] = os.getenv('SKILL_REGISTRY_TYPE')
        if os.getenv('SKILL_REGISTRY_STORAGE_PATH'):
            config_dict['registry_storage_path'] = os.getenv('SKILL_REGISTRY_STORAGE_PATH')
        
        # 执行器配置
        if os.getenv('SKILL_EXECUTOR_TYPE'):
            config_dict['executor_type'] = os.getenv('SKILL_EXECUTOR_TYPE')
        if os.getenv('SKILL_EXECUTION_TIMEOUT'):
            config_dict['execution_timeout'] = int(os.getenv('SKILL_EXECUTION_TIMEOUT'))
        if os.getenv('SKILL_MAX_CONCURRENT_EXECUTIONS'):
            config_dict['max_concurrent_executions'] = int(os.getenv('SKILL_MAX_CONCURRENT_EXECUTIONS'))
        
        # 沙箱配置
        if os.getenv('SKILL_SANDBOX_TYPE'):
            config_dict['sandbox_type'] = os.getenv('SKILL_SANDBOX_TYPE')
        if os.getenv('SKILL_SANDBOX_TIMEOUT'):
            config_dict['sandbox_timeout'] = int(os.getenv('SKILL_SANDBOX_TIMEOUT'))
        if os.getenv('SKILL_SANDBOX_MAX_MEMORY'):
            config_dict['sandbox_max_memory'] = int(os.getenv('SKILL_SANDBOX_MAX_MEMORY'))
        
        # 安全配置
        if os.getenv('SKILL_ENABLE_CODE_VALIDATION'):
            config_dict['enable_code_validation'] = os.getenv('SKILL_ENABLE_CODE_VALIDATION').lower() == 'true'
        if os.getenv('SKILL_MAX_CODE_SIZE'):
            config_dict['max_code_size'] = int(os.getenv('SKILL_MAX_CODE_SIZE'))
        
        # 缓存配置
        if os.getenv('SKILL_ENABLE_CACHE'):
            config_dict['enable_cache'] = os.getenv('SKILL_ENABLE_CACHE').lower() == 'true'
        if os.getenv('SKILL_CACHE_TTL'):
            config_dict['cache_ttl'] = int(os.getenv('SKILL_CACHE_TTL'))
        if os.getenv('SKILL_CACHE_SIZE_LIMIT'):
            config_dict['cache_size_limit'] = int(os.getenv('SKILL_CACHE_SIZE_LIMIT'))
        
        # 监控配置
        if os.getenv('SKILL_ENABLE_MONITORING'):
            config_dict['enable_monitoring'] = os.getenv('SKILL_ENABLE_MONITORING').lower() == 'true'
        if os.getenv('SKILL_LOG_LEVEL'):
            config_dict['log_level'] = os.getenv('SKILL_LOG_LEVEL')
        
        if config_dict:
            return SkillSystemConfig(**config_dict)
        return None
    
    def get_config(self) -> SkillSystemConfig:
        """
        获取当前配置
        """
        return self.config
    
    def update_config(self, **kwargs) -> SkillSystemConfig:
        """
        更新配置
        """
        # 更新配置对象
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        
        # 保存到文件
        self.save_config(self.config)
        return self.config
    
    def save_config(self, config: Optional[SkillSystemConfig] = None):
        """
        保存配置到文件
        """
        config = config or self.config
        config_dict = asdict(config)
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)
        
        print(f"Configuration saved to {self.config_path}")
    
    def reset_to_defaults(self) -> SkillSystemConfig:
        """
        重置为默认配置
        """
        self.config = SkillSystemConfig()
        self.save_config()
        return self.config


# 全局配置管理器
_config_manager: Optional[ConfigManager] = None


def get_config_manager(config_path: Optional[str] = None) -> ConfigManager:
    """
    获取全局配置管理器
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_path)
    return _config_manager


def get_skill_system_config() -> SkillSystemConfig:
    """
    获取技能系统配置
    """
    manager = get_config_manager()
    return manager.get_config()


def update_skill_system_config(**kwargs) -> SkillSystemConfig:
    """
    更新技能系统配置
    """
    manager = get_config_manager()
    return manager.update_config(**kwargs)


# 验证配置
def validate_config(config: SkillSystemConfig) -> Dict[str, Any]:
    """
    验证配置的有效性
    """
    errors = []
    
    # 验证注册表类型
    valid_registry_types = ["in_memory", "persistent", "redis"]
    if config.registry_type not in valid_registry_types:
        errors.append(f"Invalid registry type: {config.registry_type}, must be one of {valid_registry_types}")
    
    # 验证执行器类型
    valid_executor_types = ["basic", "advanced"]
    if config.executor_type not in valid_executor_types:
        errors.append(f"Invalid executor type: {config.executor_type}, must be one of {valid_executor_types}")
    
    # 验证沙箱类型
    valid_sandbox_types = ["default", "docker", "python", "javascript"]
    if config.sandbox_type not in valid_sandbox_types:
        errors.append(f"Invalid sandbox type: {config.sandbox_type}, must be one of {valid_sandbox_types}")
    
    # 验证超时时间
    if config.execution_timeout <= 0 or config.execution_timeout > 3600:
        errors.append(f"Invalid execution timeout: {config.execution_timeout}, must be between 1 and 3600 seconds")
    
    if config.sandbox_timeout <= 0 or config.sandbox_timeout > 3600:
        errors.append(f"Invalid sandbox timeout: {config.sandbox_timeout}, must be between 1 and 3600 seconds")
    
    # 验证内存限制
    if config.sandbox_max_memory <= 0 or config.sandbox_max_memory > 4096:
        errors.append(f"Invalid sandbox memory limit: {config.sandbox_max_memory}, must be between 1 and 4096 MB")
    
    # 验证并发执行数
    if config.max_concurrent_executions <= 0 or config.max_concurrent_executions > 100:
        errors.append(f"Invalid max concurrent executions: {config.max_concurrent_executions}, must be between 1 and 100")
    
    # 验证缓存配置
    if config.cache_ttl <= 0:
        errors.append(f"Invalid cache TTL: {config.cache_ttl}, must be positive")
    
    if config.cache_size_limit <= 0:
        errors.append(f"Invalid cache size limit: {config.cache_size_limit}, must be positive")
    
    # 验证日志级别
    valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if config.log_level not in valid_log_levels:
        errors.append(f"Invalid log level: {config.log_level}, must be one of {valid_log_levels}")
    
    # 验证监控间隔
    if config.metrics_collection_interval <= 0:
        errors.append(f"Invalid metrics collection interval: {config.metrics_collection_interval}, must be positive")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": []
    }


def init_config(config_path: Optional[str] = None) -> SkillSystemConfig:
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