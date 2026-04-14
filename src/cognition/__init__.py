"""
认知系统模块初始化
基于 nuwa-skill 的心智模型蒸馏架构
"""
import logging
from typing import Dict, Any, Optional

# 从核心模块导入主要类和函数
from .core import (
    CognitiveSystem, 
    AdvancedCognitiveSystem,
    CognitiveSystemManager
)
from .interfaces import (
    CognitiveTask,
    CognitiveResult, 
    ReasoningProcess,
    ReasoningStep,
    CognitiveProfile,
    BiasDetectionResult,
    CognitivePattern,
    CognitiveSystemABC
)
from .models import (
    NeuralCognitiveModel,
    CognitiveModel
)
from .reasoning import (
    ChainOfThoughtReasoning,
    TreeOfThoughtsReasoning,
    ReActReasoning,
    ReasoningEngine
)
from .personalization import (
    CognitivePersonalizationEngine,
    PersonalizationEngine
)
from .evaluation import (
    CognitiveEvaluator,
    AdvancedCognitiveEvaluator
)
from .config import (
    CognitiveSystemConfig,
    ConfigManager,
    get_config_manager,
    get_cognitive_config,
    update_cognitive_config
)
from .utils import (
    sanitize_input,
    sanitize_output,
    calculate_similarity,
    extract_keywords,
    normalize_vector,
    cosine_similarity,
    CognitiveUtils,
    get_cognitive_utils
)


# 版本信息
__version__ = "1.0.0"
__author__ = "nuwa-skill inspired"
__description__ = "Personal AI Operating System - Cognitive System Module"


# 模块级日志配置
def setup_logging(level: int = logging.INFO):
    """
    设置模块日志
    """
    logger = logging.getLogger(__name__.split('.')[0])
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


# 全局日志实例
logger = setup_logging()


def create_cognitive_system(config_path: Optional[str] = None, system_type: str = "standard") -> CognitiveSystem:
    """
    创建认知系统实例的工厂函数
    """
    if system_type == "standard":
        return CognitiveSystem()
    elif system_type == "advanced":
        return AdvancedCognitiveSystem()
    else:
        raise ValueError(f"Unknown cognitive system type: {system_type}")


def init_cognitive_framework(config: Optional[Dict[str, Any]] = None) -> CognitiveSystem:
    """
    初始化认知框架
    """
    try:
        # 创建配置管理器
        config_manager = get_config_manager()
        
        # 如果提供了自定义配置，更新系统配置
        if config:
            for key, value in config.items():
                config_manager.update_config(**{key: value})
        
        # 创建认知系统
        cognitive_system = create_cognitive_system()
        
        logger.info("Cognitive framework initialized successfully")
        return cognitive_system
        
    except Exception as e:
        logger.error(f"Error initializing cognitive framework: {e}")
        raise


# 系统状态跟踪
_system_initialized = False
_cognitive_system_instance: Optional[CognitiveSystem] = None


def get_global_cognitive_system() -> Optional[CognitiveSystem]:
    """
    获取全局认知系统实例
    """
    global _cognitive_system_instance
    return _cognitive_system_instance


def is_system_initialized() -> bool:
    """
    检查系统是否已初始化
    """
    global _system_initialized
    return _system_initialized


async def initialize_global_system(config_path: Optional[str] = None) -> CognitiveSystem:
    """
    初始化全局认知系统
    """
    global _system_initialized, _cognitive_system_instance
    
    if _system_initialized:
        return _cognitive_system_instance
    
    try:
        # 创建配置管理器
        config_manager = get_config_manager(config_path)
        
        # 创建认知系统实例
        _cognitive_system_instance = CognitiveSystem(
            config=config_manager.get_config()
        )
        
        # 初始化系统
        await _cognitive_system_instance.initialize()
        
        _system_initialized = True
        logger.info("Global cognitive system initialized successfully")
        
        return _cognitive_system_instance
        
    except Exception as e:
        logger.error(f"Error initializing global cognitive system: {e}")
        raise


async def shutdown_global_system():
    """
    关闭全局认知系统
    """
    global _system_initialized, _cognitive_system_instance
    
    if _cognitive_system_instance:
        await _cognitive_system_instance.shutdown()
        _cognitive_system_instance = None
        _system_initialized = False
        logger.info("Global cognitive system shut down successfully")


# 便捷函数
async def process_cognitive_task(task: CognitiveTask) -> CognitiveResult:
    """
    处理认知任务的便捷函数
    """
    system = get_global_cognitive_system()
    if not system:
        system = await initialize_global_system()
    
    return await system.process_task(task)


async def evaluate_user_cognition(user_id: str, tasks: List[CognitiveTask]) -> CognitiveProfile:
    """
    评估用户认知能力的便捷函数
    """
    system = get_global_cognitive_system()
    if not system:
        system = await initialize_global_system()
    
    return await system.evaluate_user_cognition(user_id, tasks)


def get_cognitive_insights(user_id: str) -> Dict[str, Any]:
    """
    获取认知洞察的便捷函数
    """
    system = get_global_cognitive_system()
    if not system:
        raise RuntimeError("Cognitive system not initialized")
    
    return system.get_cognitive_insights(user_id)


# 模块导出
__all__ = [
    # 核心类
    'CognitiveSystem',
    'AdvancedCognitiveSystem', 
    'CognitiveSystemManager',
    
    # 接口和数据类
    'CognitiveTask',
    'CognitiveResult',
    'ReasoningProcess', 
    'ReasoningStep',
    'CognitiveProfile',
    'BiasDetectionResult',
    'CognitivePattern',
    'CognitiveSystemABC',
    
    # 模型
    'NeuralCognitiveModel',
    'CognitiveModel',
    
    # 推理引擎
    'ChainOfThoughtReasoning',
    'TreeOfThoughtsReasoning', 
    'ReActReasoning',
    'ReasoningEngine',
    
    # 个性化
    'CognitivePersonalizationEngine',
    'PersonalizationEngine',
    
    # 评估
    'CognitiveEvaluator',
    'AdvancedCognitiveEvaluator',
    
    # 配置
    'CognitiveSystemConfig',
    'ConfigManager',
    'get_config_manager',
    'get_cognitive_config', 
    'update_cognitive_config',
    
    # 工具
    'sanitize_input',
    'sanitize_output',
    'calculate_similarity',
    'extract_keywords',
    'normalize_vector',
    'cosine_similarity',
    'CognitiveUtils',
    'get_cognitive_utils',
    
    # 工厂函数
    'create_cognitive_system',
    'init_cognitive_framework',
    
    # 全局管理
    'get_global_cognitive_system',
    'is_system_initialized',
    'initialize_global_system',
    'shutdown_global_system',
    
    # 便捷函数
    'process_cognitive_task',
    'evaluate_user_cognition',
    'get_cognitive_insights'
]


# 初始化全局系统（可选）
async def auto_initialize():
    """
    自动初始化（在导入时可选调用）
    """
    try:
        await initialize_global_system()
    except Exception as e:
        logger.warning(f"Could not auto-initialize cognitive system: {e}")


# 如果需要自动初始化，取消下面的注释
# asyncio.create_task(auto_initialize())