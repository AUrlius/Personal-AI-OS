"""
认知系统配置管理器
基于 nuwa-skill 架构的配置管理
"""
import json
import yaml
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict, field
from pathlib import Path
import os
import logging


@dataclass
class CognitiveModelConfig:
    """
    认知模型配置
    """
    embedding_dim: int = 768
    hidden_dim: int = 512
    num_layers: int = 4
    dropout: float = 0.1
    learning_rate: float = 0.001
    max_sequence_length: int = 512
    attention_heads: int = 8
    feedforward_dim: int = 2048


@dataclass
class ReasoningConfig:
    """
    推理配置
    """
    max_steps: int = 10
    confidence_threshold: float = 0.7
    timeout_seconds: int = 30
    enable_chain_of_thought: bool = True
    enable_tree_of_thoughts: bool = False
    enable_react: bool = True
    max_branches: int = 3
    reasoning_temperature: float = 0.7
    enable_bias_detection: bool = True
    enable_meta_cognition: bool = True


@dataclass
class MemoryConfig:
    """
    记忆系统配置
    """
    storage_type: str = "vector_db"  # "vector_db", "graph_db", "hybrid"
    vector_database: str = "chroma"  # "chroma", "pinecone", "weaviate"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    max_memory_items: int = 10000
    memory_ttl_days: int = 365
    enable_compression: bool = True
    compression_ratio: float = 0.8
    enable_summarization: bool = True
    summarization_threshold: int = 1000  # 字符数阈值


@dataclass
class SkillsConfig:
    """
    技能系统配置
    """
    enable_sandbox: bool = True
    sandbox_timeout_seconds: int = 30
    max_memory_per_skill_mb: int = 128
    allowed_permissions: list = field(default_factory=lambda: [
        "network", "filesystem_read", "database_read"
    ])
    max_concurrent_skills: int = 5
    skill_cache_enabled: bool = True
    skill_cache_ttl_seconds: int = 3600


@dataclass
class BiasDetectionConfig:
    """
    偏见检测配置
    """
    enabled: bool = True
    sensitivity: float = 0.6
    detection_methods: list = field(default_factory=lambda: [
        "pattern_matching",
        "statistical_analysis", 
        "contextual_analysis"
    ])
    correction_strategies: list = field(default_factory=lambda: [
        "counter_argumentation",
        "alternative_perspective",
        "confidence_adjustment"
    ])
    bias_types_to_detect: list = field(default_factory=lambda: [
        "confirmation", "anchoring", "availability", "hindsight", "overconfidence"
    ])


@dataclass
class PersonalizationConfig:
    """
    个性化配置
    """
    enable_adaptive_reasoning: bool = True
    enable_bias_correction: bool = True
    enable_cognitive_adaptation: bool = True
    learning_rate: float = 0.01
    forgetting_factor: float = 0.95
    adaptation_window: int = 10
    profile_update_frequency: int = 5
    cognitive_profile_persistence: bool = True
    profile_backup_enabled: bool = True
    profile_backup_interval_hours: int = 24


@dataclass
class PerformanceConfig:
    """
    性能配置
    """
    max_concurrent_tasks: int = 10
    cache_enabled: bool = True
    cache_ttl_seconds: int = 3600
    cache_size_limit: int = 1000
    enable_profiling: bool = False
    memory_limit_mb: int = 2048
    cpu_limit_percent: float = 80.0
    response_timeout_seconds: int = 60


@dataclass
class SecurityConfig:
    """
    安全配置
    """
    enable_input_validation: bool = True
    enable_output_sanitization: bool = True
    max_input_length: int = 10000
    max_output_length: int = 5000
    enable_sandbox_execution: bool = True
    sandbox_timeout_seconds: int = 30
    max_memory_per_task_mb: int = 128
    api_rate_limit: int = 100  # 每分钟请求数
    enable_audit_logging: bool = True


@dataclass
class CognitiveSystemConfig:
    """
    认知系统主配置
    """
    model: CognitiveModelConfig = field(default_factory=CognitiveModelConfig)
    reasoning: ReasoningConfig = field(default_factory=ReasoningConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    skills: SkillsConfig = field(default_factory=SkillsConfig)
    bias_detection: BiasDetectionConfig = field(default_factory=BiasDetectionConfig)
    personalization: PersonalizationConfig = field(default_factory=PersonalizationConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    
    # 系统级配置
    system_name: str = "Personal-AI-OS Cognitive System"
    version: str = "1.0.0"
    debug_mode: bool = False
    log_level: str = "INFO"
    data_retention_days: int = 30
    backup_enabled: bool = True
    backup_frequency_hours: int = 24
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典格式
        """
        return asdict(self)
    
    def to_json(self) -> str:
        """
        转换为JSON格式
        """
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
    
    def to_yaml(self) -> str:
        """
        转换为YAML格式
        """
        return yaml.dump(self.to_dict(), default_flow_style=False, allow_unicode=True)
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'CognitiveSystemConfig':
        """
        从字典创建配置对象
        """
        # 递归创建嵌套配置对象
        model_config = CognitiveModelConfig(**config_dict.get('model', {}))
        reasoning_config = ReasoningConfig(**config_dict.get('reasoning', {}))
        memory_config = MemoryConfig(**config_dict.get('memory', {}))
        skills_config = SkillsConfig(**config_dict.get('skills', {}))
        bias_detection_config = BiasDetectionConfig(**config_dict.get('bias_detection', {}))
        personalization_config = PersonalizationConfig(**config_dict.get('personalization', {}))
        performance_config = PerformanceConfig(**config_dict.get('performance', {}))
        security_config = SecurityConfig(**config_dict.get('security', {}))
        
        # 创建主配置对象
        main_config = {
            'model': model_config,
            'reasoning': reasoning_config,
            'memory': memory_config,
            'skills': skills_config,
            'bias_detection': bias_detection_config,
            'personalization': personalization_config,
            'performance': performance_config,
            'security': security_config
        }
        
        # 添加系统级配置
        for key, value in config_dict.items():
            if key not in ['model', 'reasoning', 'memory', 'skills', 'bias_detection', 'personalization', 'performance', 'security']:
                main_config[key] = value
        
        return cls(**main_config)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'CognitiveSystemConfig':
        """
        从JSON字符串创建配置对象
        """
        config_dict = json.loads(json_str)
        return cls.from_dict(config_dict)
    
    @classmethod
    def from_yaml(cls, yaml_str: str) -> 'CognitiveSystemConfig':
        """
        从YAML字符串创建配置对象
        """
        config_dict = yaml.safe_load(yaml_str)
        return cls.from_dict(config_dict)
    
    @classmethod
    def from_file(cls, file_path: str) -> 'CognitiveSystemConfig':
        """
        从文件加载配置
        """
        file_path = Path(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.suffix.lower() in ['.yaml', '.yml']:
                config_dict = yaml.safe_load(f)
            else:
                config_dict = json.load(f)
        
        return cls.from_dict(config_dict)
    
    def save_to_file(self, file_path: str):
        """
        保存配置到文件
        """
        file_path = Path(file_path)
        
        config_dict = self.to_dict()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            if file_path.suffix.lower() in ['.yaml', '.yml']:
                yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True)
            else:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)


class ConfigManager:
    """
    配置管理器
    """
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "./config/cognitive_system.yaml"
        self.config = self._load_config()
        self.logger = logging.getLogger(__name__)
    
    def _load_config(self) -> CognitiveSystemConfig:
        """
        加载配置
        """
        config_path = Path(self.config_path)
        
        # 首先尝试从文件加载
        if config_path.exists():
            try:
                config = CognitiveSystemConfig.from_file(str(config_path))
                self.logger.info(f"Configuration loaded from {config_path}")
                return config
            except Exception as e:
                self.logger.warning(f"Failed to load config from {config_path}: {e}")
        
        # 然后尝试从环境变量加载
        config = self._load_from_environment()
        if config:
            self.logger.info("Configuration loaded from environment variables")
            return config
        
        # 最后使用默认配置
        config = CognitiveSystemConfig()
        self.logger.info("Using default configuration")
        return config
    
    def _load_from_environment(self) -> Optional[CognitiveSystemConfig]:
        """
        从环境变量加载配置
        """
        config_dict = {}
        
        # 模型配置
        model_config = {}
        if os.getenv('COGNITIVE_EMBEDDING_DIM'):
            model_config['embedding_dim'] = int(os.getenv('COGNITIVE_EMBEDDING_DIM'))
        if os.getenv('COGNITIVE_HIDDEN_DIM'):
            model_config['hidden_dim'] = int(os.getenv('COGNITIVE_HIDDEN_DIM'))
        if os.getenv('COGNITIVE_NUM_LAYERS'):
            model_config['num_layers'] = int(os.getenv('COGNITIVE_NUM_LAYERS'))
        if model_config:
            config_dict['model'] = model_config
        
        # 推理配置
        reasoning_config = {}
        if os.getenv('COGNITIVE_MAX_STEPS'):
            reasoning_config['max_steps'] = int(os.getenv('COGNITIVE_MAX_STEPS'))
        if os.getenv('COGNITIVE_CONFIDENCE_THRESHOLD'):
            reasoning_config['confidence_threshold'] = float(os.getenv('COGNITIVE_CONFIDENCE_THRESHOLD'))
        if os.getenv('COGNITIVE_REASONING_TIMEOUT'):
            reasoning_config['timeout_seconds'] = int(os.getenv('COGNITIVE_REASONING_TIMEOUT'))
        if reasoning_config:
            config_dict['reasoning'] = reasoning_config
        
        # 记忆配置
        memory_config = {}
        if os.getenv('COGNITIVE_MEMORY_STORAGE_TYPE'):
            memory_config['storage_type'] = os.getenv('COGNITIVE_MEMORY_STORAGE_TYPE')
        if os.getenv('COGNITIVE_MAX_MEMORY_ITEMS'):
            memory_config['max_memory_items'] = int(os.getenv('COGNITIVE_MAX_MEMORY_ITEMS'))
        if memory_config:
            config_dict['memory'] = memory_config
        
        # 技能配置
        skills_config = {}
        if os.getenv('COGNITIVE_SKILLS_SANDBOX_ENABLED'):
            skills_config['enable_sandbox'] = os.getenv('COGNITIVE_SKILLS_SANDBOX_ENABLED').lower() == 'true'
        if os.getenv('COGNITIVE_MAX_CONCURRENT_SKILLS'):
            skills_config['max_concurrent_skills'] = int(os.getenv('COGNITIVE_MAX_CONCURRENT_SKILLS'))
        if skills_config:
            config_dict['skills'] = skills_config
        
        # 偏见检测配置
        bias_config = {}
        if os.getenv('COGNITIVE_BIAS_DETECTION_ENABLED'):
            bias_config['enabled'] = os.getenv('COGNITIVE_BIAS_DETECTION_ENABLED').lower() == 'true'
        if os.getenv('COGNITIVE_BIAS_SENSITIVITY'):
            bias_config['sensitivity'] = float(os.getenv('COGNITIVE_BIAS_SENSITIVITY'))
        if bias_config:
            config_dict['bias_detection'] = bias_config
        
        # 个性化配置
        personalization_config = {}
        if os.getenv('COGNITIVE_LEARNING_RATE'):
            personalization_config['learning_rate'] = float(os.getenv('COGNITIVE_LEARNING_RATE'))
        if os.getenv('COGNITIVE_FORGETTING_FACTOR'):
            personalization_config['forgetting_factor'] = float(os.getenv('COGNITIVE_FORGETTING_FACTOR'))
        if personalization_config:
            config_dict['personalization'] = personalization_config
        
        # 性能配置
        performance_config = {}
        if os.getenv('COGNITIVE_MAX_CONCURRENT_TASKS'):
            performance_config['max_concurrent_tasks'] = int(os.getenv('COGNITIVE_MAX_CONCURRENT_TASKS'))
        if os.getenv('COGNITIVE_CACHE_ENABLED'):
            performance_config['cache_enabled'] = os.getenv('COGNITIVE_CACHE_ENABLED').lower() == 'true'
        if os.getenv('COGNITIVE_MEMORY_LIMIT_MB'):
            performance_config['memory_limit_mb'] = int(os.getenv('COGNITIVE_MEMORY_LIMIT_MB'))
        if performance_config:
            config_dict['performance'] = performance_config
        
        # 安全配置
        security_config = {}
        if os.getenv('COGNITIVE_INPUT_VALIDATION_ENABLED'):
            security_config['enable_input_validation'] = os.getenv('COGNITIVE_INPUT_VALIDATION_ENABLED').lower() == 'true'
        if os.getenv('COGNITIVE_MAX_INPUT_LENGTH'):
            security_config['max_input_length'] = int(os.getenv('COGNITIVE_MAX_INPUT_LENGTH'))
        if os.getenv('COGNITIVE_SANDBOX_ENABLED'):
            security_config['enable_sandbox_execution'] = os.getenv('COGNITIVE_SANDBOX_ENABLED').lower() == 'true'
        if security_config:
            config_dict['security'] = security_config
        
        # 系统配置
        if os.getenv('COGNITIVE_DEBUG_MODE'):
            config_dict['debug_mode'] = os.getenv('COGNITIVE_DEBUG_MODE').lower() == 'true'
        if os.getenv('COGNITIVE_LOG_LEVEL'):
            config_dict['log_level'] = os.getenv('COGNITIVE_LOG_LEVEL')
        if os.getenv('COGNITIVE_DATA_RETENTION_DAYS'):
            config_dict['data_retention_days'] = int(os.getenv('COGNITIVE_DATA_RETENTION_DAYS'))
        
        if config_dict:
            try:
                return CognitiveSystemConfig.from_dict(config_dict)
            except Exception as e:
                self.logger.error(f"Error creating config from environment variables: {e}")
                return None
        
        return None
    
    def get_config(self) -> CognitiveSystemConfig:
        """
        获取当前配置
        """
        return self.config
    
    def update_config(self, **kwargs) -> CognitiveSystemConfig:
        """
        更新配置
        """
        # 递归更新嵌套配置
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                attr = getattr(self.config, key)
                if hasattr(attr, '__dict__') and isinstance(value, dict):
                    # 更新嵌套对象的属性
                    for sub_key, sub_value in value.items():
                        if hasattr(attr, sub_key):
                            setattr(attr, sub_key, sub_value)
                else:
                    setattr(self.config, key, value)
        
        # 保存到文件
        if self.config_path:
            self.save_config()
        
        return self.config
    
    def save_config(self, config_path: Optional[str] = None):
        """
        保存配置到文件
        """
        save_path = Path(config_path or self.config_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.config.save_to_file(str(save_path))
        self.logger.info(f"Configuration saved to {save_path}")
    
    def validate_config(self) -> Dict[str, Any]:
        """
        验证配置的有效性
        """
        errors = []
        warnings = []
        
        # 验证模型配置
        model = self.config.model
        if model.embedding_dim <= 0:
            errors.append("Model embedding_dim must be positive")
        if model.hidden_dim <= 0:
            errors.append("Model hidden_dim must be positive")
        if model.num_layers <= 0:
            errors.append("Model num_layers must be positive")
        if not (0 <= model.dropout <= 1):
            errors.append("Model dropout must be between 0 and 1")
        
        # 验证推理配置
        reasoning = self.config.reasoning
        if reasoning.max_steps <= 0:
            errors.append("Reasoning max_steps must be positive")
        if not (0 <= reasoning.confidence_threshold <= 1):
            errors.append("Reasoning confidence_threshold must be between 0 and 1")
        if reasoning.timeout_seconds <= 0:
            errors.append("Reasoning timeout_seconds must be positive")
        
        # 验证记忆配置
        memory = self.config.memory
        if memory.max_memory_items <= 0:
            errors.append("Memory max_memory_items must be positive")
        if memory.memory_ttl_days <= 0:
            errors.append("Memory memory_ttl_days must be positive")
        if not (0 <= memory.compression_ratio <= 1):
            errors.append("Memory compression_ratio must be between 0 and 1")
        
        # 验证技能配置
        skills = self.config.skills
        if skills.max_concurrent_skills <= 0:
            errors.append("Skills max_concurrent_skills must be positive")
        if skills.sandbox_timeout_seconds <= 0:
            errors.append("Skills sandbox_timeout_seconds must be positive")
        if skills.max_memory_per_skill_mb <= 0:
            errors.append("Skills max_memory_per_skill_mb must be positive")
        
        # 验证偏见检测配置
        bias = self.config.bias_detection
        if not (0 <= bias.sensitivity <= 1):
            errors.append("Bias detection sensitivity must be between 0 and 1")
        
        # 验证性能配置
        performance = self.config.performance
        if performance.max_concurrent_tasks <= 0:
            errors.append("Performance max_concurrent_tasks must be positive")
        if performance.cache_ttl_seconds <= 0:
            errors.append("Performance cache_ttl_seconds must be positive")
        if performance.cache_size_limit <= 0:
            errors.append("Performance cache_size_limit must be positive")
        
        # 验证安全配置
        security = self.config.security
        if security.max_input_length <= 0:
            errors.append("Security max_input_length must be positive")
        if security.max_output_length <= 0:
            errors.append("Security max_output_length must be positive")
        if security.sandbox_timeout_seconds <= 0:
            errors.append("Security sandbox_timeout_seconds must be positive")
        if security.max_memory_per_task_mb <= 0:
            errors.append("Security max_memory_per_task_mb must be positive")
        if security.api_rate_limit <= 0:
            errors.append("Security api_rate_limit must be positive")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }


# 全局配置管理器
_global_config_manager: Optional[ConfigManager] = None


def get_config_manager(config_path: Optional[str] = None) -> ConfigManager:
    """
    获取全局配置管理器
    """
    global _global_config_manager
    if _global_config_manager is None:
        _global_config_manager = ConfigManager(config_path)
    return _global_config_manager


def get_cognitive_config() -> CognitiveSystemConfig:
    """
    获取认知系统配置
    """
    manager = get_config_manager()
    return manager.get_config()


def update_cognitive_config(**kwargs) -> CognitiveSystemConfig:
    """
    更新认知系统配置
    """
    manager = get_config_manager()
    return manager.update_config(**kwargs)


def init_default_config(output_path: str = "./config/cognitive_system.yaml") -> CognitiveSystemConfig:
    """
    初始化默认配置文件
    """
    config = CognitiveSystemConfig()
    
    # 确保目录存在
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # 保存配置
    config.save_to_file(output_path)
    print(f"✅ 默认配置文件已创建: {output_path}")
    
    return config


def validate_cognitive_config(config: CognitiveSystemConfig) -> Dict[str, Any]:
    """
    验证认知系统配置
    """
    manager = get_config_manager()
    # 临时使用传入的配置进行验证
    original_config = manager.config
    manager.config = config
    result = manager.validate_config()
    manager.config = original_config  # 恢复原配置
    return result


def create_config_from_template(template_type: str = "default") -> CognitiveSystemConfig:
    """
    从模板创建配置
    """
    if template_type == "minimal":
        # 最小配置
        return CognitiveSystemConfig(
            model=CognitiveModelConfig(embedding_dim=384, hidden_dim=256, num_layers=2),
            reasoning=ReasoningConfig(max_steps=5, confidence_threshold=0.6, timeout_seconds=15),
            memory=MemoryConfig(max_memory_items=1000, memory_ttl_days=30),
            performance=PerformanceConfig(max_concurrent_tasks=3, cache_size_limit=100)
        )
    elif template_type == "production":
        # 生产配置
        return CognitiveSystemConfig(
            model=CognitiveModelConfig(embedding_dim=1024, hidden_dim=768, num_layers=6),
            reasoning=ReasoningConfig(max_steps=15, confidence_threshold=0.75, timeout_seconds=60),
            memory=MemoryConfig(max_memory_items=50000, memory_ttl_days=730),
            performance=PerformanceConfig(max_concurrent_tasks=20, cache_size_limit=10000),
            security=SecurityConfig(enable_input_validation=True, api_rate_limit=1000)
        )
    else:
        # 默认配置
        return CognitiveSystemConfig()


# 配置环境管理
class EnvironmentManager:
    """
    环境管理器
    """
    def __init__(self):
        self.environments = {
            "development": create_config_from_template("default"),
            "production": create_config_from_template("production"),
            "testing": create_config_from_template("minimal")
        }
        self.current_env = os.getenv("COGNITIVE_ENV", "development")
    
    def get_environment_config(self, env_name: str = None) -> CognitiveSystemConfig:
        """
        获取指定环境的配置
        """
        env = env_name or self.current_env
        if env in self.environments:
            return self.environments[env]
        else:
            return self.environments["development"]  # 默认返回开发环境配置
    
    def set_environment(self, env_name: str):
        """
        设置当前环境
        """
        if env_name in self.environments:
            self.current_env = env_name
            os.environ["COGNITIVE_ENV"] = env_name
        else:
            raise ValueError(f"Unknown environment: {env_name}")
    
    def get_current_config(self) -> CognitiveSystemConfig:
        """
        获取当前环境的配置
        """
        return self.get_environment_config(self.current_env)


# 全局环境管理器
_env_manager: Optional[EnvironmentManager] = None


def get_environment_manager() -> EnvironmentManager:
    """
    获取环境管理器
    """
    global _env_manager
    if _env_manager is None:
        _env_manager = EnvironmentManager()
    return _env_manager


def get_active_config() -> CognitiveSystemConfig:
    """
    获取当前活动配置
    """
    env_manager = get_environment_manager()
    return env_manager.get_current_config()


# 初始化配置管理器
def init_config_manager(config_path: Optional[str] = None) -> ConfigManager:
    """
    初始化配置管理器
    """
    global _global_config_manager
    _global_config_manager = ConfigManager(config_path)
    return _global_config_manager


if __name__ == "__main__":
    # 创建默认配置文件
    default_config = init_default_config()
    
    # 测试配置管理
    manager = get_config_manager()
    config = manager.get_config()
    
    print("✅ 配置管理器测试成功!")
    print(f"模型嵌入维度: {config.model.embedding_dim}")
    print(f"推理最大步骤数: {config.reasoning.max_steps}")
    print(f"记忆最大项目数: {config.memory.max_memory_items}")
    
    # 验证配置
    validation_result = manager.validate_config()
    print(f"配置验证结果: {validation_result['valid']}")
    if validation_result['errors']:
        print(f"验证错误: {validation_result['errors']}")
    if validation_result['warnings']:
        print(f"验证警告: {validation_result['warnings']}")