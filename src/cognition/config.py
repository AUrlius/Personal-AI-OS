"""
认知系统配置管理
基于 nuwa-skill 的配置架构设计
"""
import os
import json
import yaml
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime


@dataclass
class ModelConfig:
    """
    模型配置
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
    enable_react: bool = False
    max_branches: int = 3
    reasoning_temperature: float = 0.7


@dataclass
class PersonalizationConfig:
    """
    个性化配置
    """
    learning_rate: float = 0.01
    forgetting_factor: float = 0.95
    adaptation_window: int = 10
    profile_update_frequency: int = 10  # 每10次交互更新一次画像
    enable_adaptive_reasoning: bool = True
    enable_bias_correction: bool = True
    enable_cognitive_adaptation: bool = True


@dataclass
class EvaluationConfig:
    """
    评估配置
    """
    metrics: list = field(default_factory=lambda: [
        "reasoning_quality",
        "confidence_calibration", 
        "reasoning_efficiency",
        "bias_detection",
        "metacognitive_awareness"
    ])
    weight_distribution: dict = field(default_factory=lambda: {
        "reasoning_quality": 0.25,
        "confidence_calibration": 0.2,
        "reasoning_efficiency": 0.2,
        "bias_detection": 0.2,
        "metacognitive_awareness": 0.15
    })
    evaluation_frequency: int = 5  # 每5次任务评估一次
    enable_longitudinal_tracking: bool = True
    enable_cross_domain_analysis: bool = True


@dataclass
class BiasDetectionConfig:
    """
    偏见检测配置
    """
    enabled: bool = True
    sensitivity: float = 0.6
    correction_enabled: bool = True
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
    memory_limit_mb: int = 1024
    cpu_limit_percent: float = 80.0


@dataclass
class LoggingConfig:
    """
    日志配置
    """
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: str = "cognitive_system.log"
    enable_console: bool = True
    enable_file: bool = True
    max_file_size_mb: int = 10
    backup_count: int = 5


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


@dataclass
class CognitiveSystemConfig:
    """
    认知系统主配置
    """
    model: ModelConfig = field(default_factory=ModelConfig)
    reasoning: ReasoningConfig = field(default_factory=ReasoningConfig)
    personalization: PersonalizationConfig = field(default_factory=PersonalizationConfig)
    evaluation: EvaluationConfig = field(default_factory=EvaluationConfig)
    bias_detection: BiasDetectionConfig = field(default_factory=BiasDetectionConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    
    # 系统级配置
    system_name: str = "Personal-AI-OS Cognitive System"
    version: str = "1.0.0"
    debug_mode: bool = False
    data_retention_days: int = 30
    backup_enabled: bool = True
    backup_frequency_hours: int = 24
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典格式
        """
        return asdict(self)
    
    def to_yaml(self) -> str:
        """
        转换为YAML格式
        """
        return yaml.dump(self.to_dict(), default_flow_style=False, allow_unicode=True)
    
    def to_json(self) -> str:
        """
        转换为JSON格式
        """
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'CognitiveSystemConfig':
        """
        从字典创建配置对象
        """
        # 递归创建嵌套的配置对象
        model_config = ModelConfig(**config_dict.get('model', {}))
        reasoning_config = ReasoningConfig(**config_dict.get('reasoning', {}))
        personalization_config = PersonalizationConfig(**config_dict.get('personalization', {}))
        evaluation_config = EvaluationConfig(**config_dict.get('evaluation', {}))
        bias_detection_config = BiasDetectionConfig(**config_dict.get('bias_detection', {}))
        performance_config = PerformanceConfig(**config_dict.get('performance', {}))
        logging_config = LoggingConfig(**config_dict.get('logging', {}))
        security_config = SecurityConfig(**config_dict.get('security', {}))
        
        # 主配置
        main_config = {
            'model': model_config,
            'reasoning': reasoning_config,
            'personalization': personalization_config,
            'evaluation': evaluation_config,
            'bias_detection': bias_detection_config,
            'performance': performance_config,
            'logging': logging_config,
            'security': security_config
        }
        
        # 添加系统级配置
        for key, value in config_dict.items():
            if key not in ['model', 'reasoning', 'personalization', 'evaluation', 'bias_detection', 'performance', 'logging', 'security']:
                main_config[key] = value
        
        return cls(**main_config)
    
    @classmethod
    def from_yaml(cls, yaml_str: str) -> 'CognitiveSystemConfig':
        """
        从YAML字符串创建配置对象
        """
        config_dict = yaml.safe_load(yaml_str)
        return cls.from_dict(config_dict)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'CognitiveSystemConfig':
        """
        从JSON字符串创建配置对象
        """
        config_dict = json.loads(json_str)
        return cls.from_dict(config_dict)
    
    @classmethod
    def from_file(cls, file_path: str) -> 'CognitiveSystemConfig':
        """
        从文件加载配置
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                content = yaml.safe_load(f)
            else:
                content = json.load(f)
        
        return cls.from_dict(content)
    
    def save_to_file(self, file_path: str):
        """
        保存配置到文件
        """
        config_dict = self.to_dict()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True)
            else:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)


class ConfigManager:
    """
    配置管理器
    负责配置的加载、验证和管理
    """
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.config = self._load_config()
        self.logger = logging.getLogger(__name__)
    
    def _load_config(self) -> CognitiveSystemConfig:
        """
        加载配置
        """
        # 首先尝试从文件加载
        if self.config_path and os.path.exists(self.config_path):
            try:
                config = CognitiveSystemConfig.from_file(self.config_path)
                self.logger.info(f"Configuration loaded from {self.config_path}")
                return config
            except Exception as e:
                self.logger.warning(f"Failed to load config from {self.config_path}: {e}")
        
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
        env_config = {}
        
        # 模型配置
        model_config = {}
        if os.getenv('COGNITIVE_EMBEDDING_DIM'):
            model_config['embedding_dim'] = int(os.getenv('COGNITIVE_EMBEDDING_DIM'))
        if os.getenv('COGNITIVE_HIDDEN_DIM'):
            model_config['hidden_dim'] = int(os.getenv('COGNITIVE_HIDDEN_DIM'))
        if model_config:
            env_config['model'] = model_config
        
        # 推理配置
        reasoning_config = {}
        if os.getenv('COGNITIVE_MAX_STEPS'):
            reasoning_config['max_steps'] = int(os.getenv('COGNITIVE_MAX_STEPS'))
        if os.getenv('COGNITIVE_CONFIDENCE_THRESHOLD'):
            reasoning_config['confidence_threshold'] = float(os.getenv('COGNITIVE_CONFIDENCE_THRESHOLD'))
        if os.getenv('COGNITIVE_TIMEOUT_SECONDS'):
            reasoning_config['timeout_seconds'] = int(os.getenv('COGNITIVE_TIMEOUT_SECONDS'))
        if reasoning_config:
            env_config['reasoning'] = reasoning_config
        
        # 个性化配置
        personalization_config = {}
        if os.getenv('COGNITIVE_LEARNING_RATE'):
            personalization_config['learning_rate'] = float(os.getenv('COGNITIVE_LEARNING_RATE'))
        if os.getenv('COGNITIVE_FORGETTING_FACTOR'):
            personalization_config['forgetting_factor'] = float(os.getenv('COGNITIVE_FORGETTING_FACTOR'))
        if os.getenv('COGNITIVE_ADAPTATION_WINDOW'):
            personalization_config['adaptation_window'] = int(os.getenv('COGNITIVE_ADAPTATION_WINDOW'))
        if personalization_config:
            env_config['personalization'] = personalization_config
        
        # 偏见检测配置
        bias_config = {}
        if os.getenv('COGNITIVE_BIAS_DETECTION_ENABLED'):
            bias_config['enabled'] = os.getenv('COGNITIVE_BIAS_DETECTION_ENABLED').lower() == 'true'
        if os.getenv('COGNITIVE_BIAS_SENSITIVITY'):
            bias_config['sensitivity'] = float(os.getenv('COGNITIVE_BIAS_SENSITIVITY'))
        if os.getenv('COGNITIVE_BIAS_CORRECTION_ENABLED'):
            bias_config['correction_enabled'] = os.getenv('COGNITIVE_BIAS_CORRECTION_ENABLED').lower() == 'true'
        if bias_config:
            env_config['bias_detection'] = bias_config
        
        # 性能配置
        perf_config = {}
        if os.getenv('COGNITIVE_MAX_CONCURRENT_TASKS'):
            perf_config['max_concurrent_tasks'] = int(os.getenv('COGNITIVE_MAX_CONCURRENT_TASKS'))
        if os.getenv('COGNITIVE_CACHE_ENABLED'):
            perf_config['cache_enabled'] = os.getenv('COGNITIVE_CACHE_ENABLED').lower() == 'true'
        if os.getenv('COGNITIVE_MEMORY_LIMIT_MB'):
            perf_config['memory_limit_mb'] = int(os.getenv('COGNITIVE_MEMORY_LIMIT_MB'))
        if perf_config:
            env_config['performance'] = perf_config
        
        # 日志配置
        log_config = {}
        if os.getenv('COGNITIVE_LOG_LEVEL'):
            log_config['level'] = os.getenv('COGNITIVE_LOG_LEVEL')
        if os.getenv('COGNITIVE_LOG_FILE'):
            log_config['file'] = os.getenv('COGNITIVE_LOG_FILE')
        if log_config:
            env_config['logging'] = log_config
        
        # 安全配置
        security_config = {}
        if os.getenv('COGNITIVE_INPUT_VALIDATION_ENABLED'):
            security_config['enable_input_validation'] = os.getenv('COGNITIVE_INPUT_VALIDATION_ENABLED').lower() == 'true'
        if os.getenv('COGNITIVE_MAX_INPUT_LENGTH'):
            security_config['max_input_length'] = int(os.getenv('COGNITIVE_MAX_INPUT_LENGTH'))
        if os.getenv('COGNITIVE_SANDBOX_ENABLED'):
            security_config['enable_sandbox_execution'] = os.getenv('COGNITIVE_SANDBOX_ENABLED').lower() == 'true'
        if security_config:
            env_config['security'] = security_config
        
        # 系统配置
        if os.getenv('COGNITIVE_DEBUG_MODE'):
            env_config['debug_mode'] = os.getenv('COGNITIVE_DEBUG_MODE').lower() == 'true'
        if os.getenv('COGNITIVE_DATA_RETENTION_DAYS'):
            env_config['data_retention_days'] = int(os.getenv('COGNITIVE_DATA_RETENTION_DAYS'))
        
        if env_config:
            try:
                return CognitiveSystemConfig.from_dict(env_config)
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
        # 这里需要实现配置更新逻辑
        # 为了简化，我们只更新顶层属性
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        
        # 保存到文件（如果指定了路径）
        if self.config_path:
            self.save_config()
        
        return self.config
    
    def save_config(self, config_path: Optional[str] = None):
        """
        保存配置到文件
        """
        save_path = config_path or self.config_path
        if save_path:
            self.config.save_to_file(save_path)
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
        
        # 验证个性化配置
        personalization = self.config.personalization
        if not (0 < personalization.learning_rate <= 1):
            errors.append("Personalization learning_rate must be between 0 and 1")
        if not (0 <= personalization.forgetting_factor <= 1):
            errors.append("Personalization forgetting_factor must be between 0 and 1")
        if personalization.adaptation_window <= 0:
            errors.append("Personalization adaptation_window must be positive")
        
        # 验证评估配置
        evaluation = self.config.evaluation
        if evaluation.weight_distribution:
            total_weight = sum(evaluation.weight_distribution.values())
            if abs(total_weight - 1.0) > 0.01:
                warnings.append(f"Evaluation weight distribution sums to {total_weight}, not 1.0")
        
        # 验证偏见检测配置
        bias = self.config.bias_detection
        if not (0 <= bias.sensitivity <= 1):
            errors.append("Bias detection sensitivity must be between 0 and 1")
        
        # 验证性能配置
        perf = self.config.performance
        if perf.max_concurrent_tasks <= 0:
            errors.append("Performance max_concurrent_tasks must be positive")
        if perf.cache_ttl_seconds <= 0:
            errors.append("Performance cache_ttl_seconds must be positive")
        if perf.cache_size_limit <= 0:
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
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def get_config_schema(self) -> Dict[str, Any]:
        """
        获取配置架构定义
        """
        return {
            "type": "object",
            "properties": {
                "model": {
                    "type": "object",
                    "properties": {
                        "embedding_dim": {"type": "integer", "minimum": 1},
                        "hidden_dim": {"type": "integer", "minimum": 1},
                        "num_layers": {"type": "integer", "minimum": 1},
                        "dropout": {"type": "number", "minimum": 0, "maximum": 1}
                    },
                    "required": ["embedding_dim", "hidden_dim", "num_layers", "dropout"]
                },
                "reasoning": {
                    "type": "object",
                    "properties": {
                        "max_steps": {"type": "integer", "minimum": 1},
                        "confidence_threshold": {"type": "number", "minimum": 0, "maximum": 1},
                        "timeout_seconds": {"type": "integer", "minimum": 1}
                    },
                    "required": ["max_steps", "confidence_threshold", "timeout_seconds"]
                },
                "personalization": {
                    "type": "object",
                    "properties": {
                        "learning_rate": {"type": "number", "minimum": 0, "maximum": 1},
                        "forgetting_factor": {"type": "number", "minimum": 0, "maximum": 1},
                        "adaptation_window": {"type": "integer", "minimum": 1}
                    },
                    "required": ["learning_rate", "forgetting_factor", "adaptation_window"]
                },
                "bias_detection": {
                    "type": "object",
                    "properties": {
                        "enabled": {"type": "boolean"},
                        "sensitivity": {"type": "number", "minimum": 0, "maximum": 1},
                        "correction_enabled": {"type": "boolean"}
                    },
                    "required": ["enabled", "sensitivity", "correction_enabled"]
                },
                "performance": {
                    "type": "object",
                    "properties": {
                        "max_concurrent_tasks": {"type": "integer", "minimum": 1},
                        "cache_enabled": {"type": "boolean"},
                        "cache_ttl_seconds": {"type": "integer", "minimum": 1},
                        "cache_size_limit": {"type": "integer", "minimum": 1}
                    },
                    "required": ["max_concurrent_tasks", "cache_enabled"]
                },
                "security": {
                    "type": "object",
                    "properties": {
                        "enable_input_validation": {"type": "boolean"},
                        "max_input_length": {"type": "integer", "minimum": 1},
                        "max_output_length": {"type": "integer", "minimum": 1},
                        "enable_sandbox_execution": {"type": "boolean"},
                        "sandbox_timeout_seconds": {"type": "integer", "minimum": 1},
                        "max_memory_per_task_mb": {"type": "integer", "minimum": 1}
                    },
                    "required": ["enable_input_validation", "max_input_length", "max_output_length"]
                }
            },
            "required": ["model", "reasoning", "personalization", "bias_detection", "performance", "security"]
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


def create_default_config(output_path: str = "./cognitive_config.yaml"):
    """
    创建默认配置文件
    """
    default_config = CognitiveSystemConfig()
    
    # 保存到文件
    default_config.save_to_file(output_path)
    print(f"默认配置文件已创建: {output_path}")
    
    return default_config


def validate_config(config: CognitiveSystemConfig) -> Dict[str, Any]:
    """
    验证配置
    """
    manager = get_config_manager()
    # 临时使用传入的配置进行验证
    original_config = manager.config
    manager.config = config
    result = manager.validate_config()
    manager.config = original_config  # 恢复原配置
    return result


# 配置加载工具函数
def load_config_from_path(config_path: str) -> CognitiveSystemConfig:
    """
    从指定路径加载配置
    """
    return CognitiveSystemConfig.from_file(config_path)


def load_config_from_string(config_str: str, format_type: str = "yaml") -> CognitiveSystemConfig:
    """
    从字符串加载配置
    """
    if format_type.lower() == "yaml":
        return CognitiveSystemConfig.from_yaml(config_str)
    elif format_type.lower() == "json":
        return CognitiveSystemConfig.from_json(config_str)
    else:
        raise ValueError(f"Unsupported format: {format_type}")


def merge_configs(base_config: CognitiveSystemConfig, override_config: CognitiveSystemConfig) -> CognitiveSystemConfig:
    """
    合并配置（覆盖配置会覆盖基础配置的值）
    """
    # 将配置转换为字典
    base_dict = base_config.to_dict()
    override_dict = override_config.to_dict()
    
    # 递归合并字典
    def deep_merge(dict1, dict2):
        result = dict1.copy()
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    merged_dict = deep_merge(base_dict, override_dict)
    return CognitiveSystemConfig.from_dict(merged_dict)


def get_config_diff(config1: CognitiveSystemConfig, config2: CognitiveSystemConfig) -> Dict[str, Any]:
    """
    获取两个配置之间的差异
    """
    def dict_diff(d1, d2, path=""):
        diff = {}
        for key in set(d1.keys()) | set(d2.keys()):
            current_path = f"{path}.{key}" if path else key
            
            if key not in d1:
                diff[current_path] = {"added": d2[key]}
            elif key not in d2:
                diff[current_path] = {"removed": d1[key]}
            elif d1[key] != d2[key]:
                if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                    nested_diff = dict_diff(d1[key], d2[key], current_path)
                    diff.update(nested_diff)
                else:
                    diff[current_path] = {"old": d1[key], "new": d2[key]}
        return diff
    
    return dict_diff(config1.to_dict(), config2.to_dict())


# 环境特定配置
def get_production_config() -> CognitiveSystemConfig:
    """
    获取生产环境配置
    """
    config = CognitiveSystemConfig()
    
    # 生产环境特定设置
    config.performance.max_concurrent_tasks = 50
    config.performance.memory_limit_mb = 2048
    config.performance.enable_profiling = True
    config.logging.level = "INFO"
    config.security.enable_input_validation = True
    config.security.enable_output_sanitization = True
    config.security.max_input_length = 5000
    config.security.max_output_length = 2000
    config.data_retention_days = 90
    config.backup_enabled = True
    config.backup_frequency_hours = 12
    
    return config


def get_development_config() -> CognitiveSystemConfig:
    """
    获取开发环境配置
    """
    config = CognitiveSystemConfig()
    
    # 开发环境特定设置
    config.reasoning.max_steps = 5
    config.reasoning.timeout_seconds = 60
    config.performance.max_concurrent_tasks = 5
    config.performance.memory_limit_mb = 512
    config.performance.enable_profiling = True
    config.logging.level = "DEBUG"
    config.debug_mode = True
    config.data_retention_days = 7
    config.backup_enabled = False
    
    return config


def get_testing_config() -> CognitiveSystemConfig:
    """
    获取测试环境配置
    """
    config = CognitiveSystemConfig()
    
    # 测试环境特定设置
    config.reasoning.max_steps = 2
    config.reasoning.timeout_seconds = 10
    config.performance.max_concurrent_tasks = 1
    config.performance.memory_limit_mb = 128
    config.performance.cache_enabled = False
    config.logging.level = "WARNING"
    config.debug_mode = True
    config.data_retention_days = 1
    config.backup_enabled = False
    
    return config


# 配置环境管理
class EnvironmentManager:
    """
    环境管理器
    """
    def __init__(self):
        self.environments = {
            "production": get_production_config(),
            "development": get_development_config(),
            "testing": get_testing_config()
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
            # 如果环境不存在，返回开发环境配置
            return self.environments["development"]
    
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


# 配置验证装饰器
def validate_config_on_set(func):
    """
    配置设置时验证的装饰器
    """
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if hasattr(self, 'config_manager'):
            validation_result = self.config_manager.validate_config()
            if not validation_result['valid']:
                raise ValueError(f"Configuration validation failed: {validation_result['errors']}")
        return result
    return wrapper


if __name__ == "__main__":
    # 创建默认配置文件
    create_default_config()
    
    # 测试配置管理
    manager = ConfigManager("./cognitive_config.yaml")
    config = manager.get_config()
    
    print("配置加载成功!")
    print(f"模型嵌入维度: {config.model.embedding_dim}")
    print(f"推理最大步骤数: {config.reasoning.max_steps}")
    print(f"个性化学习率: {config.personalization.learning_rate}")
    
    # 验证配置
    validation_result = manager.validate_config()
    print(f"配置验证结果: {validation_result['valid']}")
    if validation_result['errors']:
        print(f"验证错误: {validation_result['errors']}")
    if validation_result['warnings']:
        print(f"验证警告: {validation_result['warnings']}")