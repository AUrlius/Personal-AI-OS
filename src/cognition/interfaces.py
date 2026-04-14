"""
认知模型模块接口定义
基于 nuwa-skill 的心智模型蒸馏架构
"""
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, Optional, List, Dict, Any, Union, Tuple
from dataclasses import dataclass
from datetime import datetime
import numpy as np


@dataclass
class CognitivePattern:
    """
    认知模式数据结构
    """
    id: str
    pattern_type: str  # "reasoning", "decision", "learning", "memory", "attention"
    weights: List[float]  # 模式权重
    triggers: List[str]  # 触发条件
    responses: List[Dict[str, Any]]  # 认知响应
    effectiveness: float  # 有效性评分 (0-1)
    last_updated: datetime
    metadata: Dict[str, Any]


@dataclass
class ReasoningStep:
    """
    推理步骤
    """
    step_number: int
    content: str
    reasoning_type: str  # "deductive", "inductive", "abductive", "analogical"
    confidence: float
    supporting_evidence: List[str]
    alternatives_considered: List[str]
    timestamp: datetime


@dataclass
class ReasoningProcess:
    """
    推理过程
    """
    id: str
    input_problem: str
    steps: List[ReasoningStep]
    conclusion: str
    confidence: float
    reasoning_strategy: str  # "chain_of_thought", "tree_of_thoughts", "react", "plan_and_execute"
    bias_indicators: List[Dict[str, Any]]  # 检测到的认知偏见
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass
class CognitiveProfile:
    """
    认知特征画像
    """
    user_id: str
    reasoning_style: str  # "analytical", "intuitive", "balanced"
    decision_making: str  # "risk_averse", "risk_neutral", "risk_seeking"
    learning_preference: str  # "visual", "auditory", "kinesthetic", "reading"
    attention_span: int  # 分钟
    processing_speed: str  # "slow", "normal", "fast"
    memory_strength: str  # "working", "long_term", "episodic"
    bias_tendencies: Dict[str, float]  # 偏见倾向 (0-1)
    performance_history: List[Dict[str, Any]]
    last_updated: datetime


@dataclass
class BiasDetectionResult:
    """
    偏见检测结果
    """
    type: str  # "confirmation", "anchoring", "availability", "hindsight", "overconfidence"
    severity: float  # 严重程度 (0-1)
    evidence: List[str]  # 检测到的证据
    suggestion: str  # 纠正建议
    confidence: float  # 检测置信度


@dataclass
class CognitiveTask:
    """
    认知任务
    """
    id: str
    task_type: str  # "analysis", "synthesis", "evaluation", "creation", "decision"
    content: str
    context: Dict[str, Any]
    user_profile: Optional[CognitiveProfile] = None
    metadata: Dict[str, Any] = None


@dataclass
class CognitiveResult:
    """
    认知结果
    """
    success: bool
    output: Optional[Dict[str, Any]]
    reasoning_process: Optional[ReasoningProcess]
    detected_biases: List[BiasDetectionResult]
    confidence: float
    execution_time: float
    resources_used: Dict[str, Any]


@runtime_checkable
class CognitiveModel(Protocol):
    """
    认知模型接口
    """
    async def process(self, task: CognitiveTask) -> CognitiveResult:
        """处理认知任务"""
        ...
    
    async def update_model(self, user_id: str, feedback: Dict[str, Any]) -> bool:
        """更新认知模型"""
        ...
    
    async def get_cognitive_profile(self, user_id: str) -> Optional[CognitiveProfile]:
        """获取认知特征画像"""
        ...


@runtime_checkable
class ReasoningEngine(Protocol):
    """
    推理引擎接口
    """
    async def reason(self, input_problem: str, context: Dict[str, Any] = None) -> ReasoningProcess:
        """执行推理过程"""
        ...
    
    async def detect_biases(self, reasoning_process: ReasoningProcess) -> List[BiasDetectionResult]:
        """检测认知偏见"""
        ...
    
    async def correct_biases(self, reasoning_process: ReasoningProcess, biases: List[BiasDetectionResult]) -> ReasoningProcess:
        """纠正认知偏见"""
        ...


@runtime_checkable
class PersonalizationEngine(Protocol):
    """
    个性化引擎接口
    """
    async def adapt_reasoning_strategy(self, task: CognitiveTask, profile: CognitiveProfile) -> str:
        """根据用户画像调整推理策略"""
        ...
    
    async def update_cognitive_profile(self, user_id: str, interaction_data: Dict[str, Any]) -> CognitiveProfile:
        """更新认知画像"""
        ...


@runtime_checkable
class CognitiveMemory(Protocol):
    """
    认知记忆接口
    """
    async def store_cognitive_pattern(self, pattern: CognitivePattern) -> str:
        """存储认知模式"""
        ...
    
    async def retrieve_cognitive_pattern(self, pattern_id: str) -> Optional[CognitivePattern]:
        """检索认知模式"""
        ...
    
    async def find_related_patterns(self, query: str, top_k: int = 5) -> List[CognitivePattern]:
        """查找相关认知模式"""
        ...


class CognitiveSystemABC(ABC):
    """
    认知系统抽象基类
    """
    @abstractmethod
    async def process_task(self, task: CognitiveTask) -> CognitiveResult:
        """处理认知任务"""
        pass
    
    @abstractmethod
    async def analyze_reasoning(self, input_problem: str, context: Dict[str, Any] = None) -> ReasoningProcess:
        """分析推理过程"""
        pass
    
    @abstractmethod
    async def personalize_for_user(self, user_id: str, task: CognitiveTask) -> CognitiveTask:
        """为用户个性化任务"""
        pass