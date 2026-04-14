"""
技能系统模块初始化
"""
from .core import SkillSystem, SkillBuilder, SkillOrchestrator
from .interfaces import (
    SkillDefinition,
    SkillInput,
    SkillOutput,
    SkillExecutionRequest,
    SkillExecutionResult,
    SkillStatus,
    SkillVisibility
)
from .registry import InMemorySkillRegistry, PersistentSkillRegistry, create_registry
from .executor import SkillExecutorImpl, AdvancedSkillExecutor
from .sandbox import (
    SkillSandboxImpl,
    PythonSandbox,
    JavaScriptSandbox,
    DockerSandbox,
    create_sandbox
)
from .config import (
    SkillSystemConfig,
    ConfigManager,
    get_config_manager,
    get_skill_system_config,
    update_skill_system_config,
    init_config
)
from .utils.validator import SkillValidator

__version__ = "1.0.0"
__author__ = "khazix-skills inspired"

__all__ = [
    # 核心类
    "SkillSystem",
    "SkillBuilder",
    "SkillOrchestrator",
    
    # 接口和数据类
    "SkillDefinition",
    "SkillInput", 
    "SkillOutput",
    "SkillExecutionRequest",
    "SkillExecutionResult",
    "SkillStatus",
    "SkillVisibility",
    
    # 注册表
    "InMemorySkillRegistry",
    "PersistentSkillRegistry",
    "create_registry",
    
    # 执行器
    "SkillExecutorImpl",
    "AdvancedSkillExecutor",
    
    # 沙箱
    "SkillSandboxImpl",
    "PythonSandbox",
    "JavaScriptSandbox", 
    "DockerSandbox",
    "create_sandbox",
    
    # 配置
    "SkillSystemConfig",
    "ConfigManager",
    "get_config_manager",
    "get_skill_system_config",
    "update_skill_system_config",
    "init_config",
    
    # 验证器
    "SkillValidator"
]


def create_default_skill_system() -> SkillSystem:
    """
    创建默认的技能系统实例
    """
    from .config import init_config
    from .registry import InMemorySkillRegistry
    from .executor import AdvancedSkillExecutor
    from .sandbox import create_sandbox
    
    # 初始化配置
    config = init_config()
    
    # 创建组件
    registry = InMemorySkillRegistry()
    executor = AdvancedSkillExecutor(create_sandbox(config.sandbox_type))
    
    # 创建技能系统
    skill_system = SkillSystem(
        registry=registry,
        executor=executor,
        sandbox=create_sandbox(config.sandbox_type)
    )
    
    return skill_system


# 设置日志
import logging

def setup_logging(level=logging.INFO):
    """
    设置日志配置
    """
    logger = logging.getLogger(__name__.split('.')[0])
    logger.setLevel(level)
    
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