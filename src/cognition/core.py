"""
认知模型系统核心实现
基于 nuwa-skill 的心智模型蒸馏架构
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import uuid
import numpy as np
from .interfaces import (
    CognitiveTask, CognitiveResult, ReasoningProcess, ReasoningStep,
    CognitiveProfile, BiasDetectionResult, CognitivePattern,
    CognitiveSystemABC, CognitiveModel, ReasoningEngine, PersonalizationEngine
)
from .models import NeuralCognitiveModel
from .reasoning import ChainOfThoughtReasoning, TreeOfThoughtsReasoning
from .personalization import CognitivePersonalizationEngine
from .utils.bias_detector import BiasDetector


class CognitiveSystem(CognitiveSystemABC):
    """
    认知系统主类
    基于 nuwa-skill 的心智模型蒸馏架构
    """
    def __init__(self):
        self.model: CognitiveModel = NeuralCognitiveModel()
        self.reasoning_engine: ReasoningEngine = ChainOfThoughtReasoning()
        self.personalization_engine: PersonalizationEngine = CognitivePersonalizationEngine()
        self.bias_detector: BiasDetector = BiasDetector()
        self.user_profiles: Dict[str, CognitiveProfile] = {}
        self.logger = logging.getLogger(__name__)
        
    async def process_task(self, task: CognitiveTask) -> CognitiveResult:
        """
        处理认知任务
        """
        start_time = datetime.now()
        
        try:
            # 获取用户认知画像（如果提供）
            user_profile = None
            if task.user_profile:
                user_profile = task.user_profile
            elif task.metadata and "user_id" in task.metadata:
                user_id = task.metadata["user_id"]
                user_profile = await self.get_user_profile(user_id)
            
            # 个性化推理策略
            if user_profile:
                adapted_task = await self.personalize_for_user(user_profile.user_id, task)
                reasoning_strategy = await self.personalization_engine.adapt_reasoning_strategy(adapted_task, user_profile)
            else:
                adapted_task = task
                reasoning_strategy = "chain_of_thought"
            
            # 执行推理
            reasoning_process = await self.reasoning_engine.reason(
                adapted_task.content, 
                adapted_task.context
            )
            
            # 检测认知偏见
            detected_biases = await self.reasoning_engine.detect_biases(reasoning_process)
            
            # 纠正认知偏见（如果检测到）
            if detected_biases:
                reasoning_process = await self.reasoning_engine.correct_biases(reasoning_process, detected_biases)
            
            # 计算执行时间
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # 构建结果
            result = CognitiveResult(
                success=True,
                output={
                    "conclusion": reasoning_process.conclusion,
                    "steps": [step.content for step in reasoning_process.steps],
                    "confidence": reasoning_process.confidence
                },
                reasoning_process=reasoning_process,
                detected_biases=detected_biases,
                confidence=reasoning_process.confidence,
                execution_time=execution_time,
                resources_used={
                    "processing_time_seconds": execution_time,
                    "memory_mb": 0  # 简化处理
                }
            )
            
            self.logger.info(f"Cognitive task processed successfully: {task.id}")
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Error processing cognitive task {task.id}: {e}")
            
            return CognitiveResult(
                success=False,
                output=None,
                reasoning_process=None,
                detected_biases=[],
                confidence=0.0,
                execution_time=execution_time,
                resources_used={"processing_time_seconds": execution_time}
            )
    
    async def analyze_reasoning(self, input_problem: str, context: Dict[str, Any] = None) -> ReasoningProcess:
        """
        分析推理过程
        """
        return await self.reasoning_engine.reason(input_problem, context)
    
    async def personalize_for_user(self, user_id: str, task: CognitiveTask) -> CognitiveTask:
        """
        为用户个性化任务
        """
        user_profile = await self.get_user_profile(user_id)
        if user_profile:
            # 根据用户画像调整任务
            return await self.personalization_engine.personalize_task(task, user_profile)
        return task
    
    async def get_user_profile(self, user_id: str) -> Optional[CognitiveProfile]:
        """
        获取用户认知画像
        """
        if user_id in self.user_profiles:
            return self.user_profiles[user_id]
        
        # 从存储中加载（简化实现，实际应该从数据库加载）
        profile = await self._load_user_profile(user_id)
        if profile:
            self.user_profiles[user_id] = profile
        return profile
    
    async def _load_user_profile(self, user_id: str) -> Optional[CognitiveProfile]:
        """
        从存储加载用户画像（简化实现）
        """
        # 这里应该是从数据库或存储加载
        # 为了演示，创建一个默认画像
        return CognitiveProfile(
            user_id=user_id,
            reasoning_style="analytical",
            decision_making="risk_neutral",
            learning_preference="visual",
            attention_span=25,
            processing_speed="normal",
            memory_strength="working",
            bias_tendencies={"confirmation": 0.3, "anchoring": 0.2},
            performance_history=[],
            last_updated=datetime.now()
        )
    
    async def update_user_profile(self, user_id: str, interaction_data: Dict[str, Any]) -> bool:
        """
        更新用户认知画像
        """
        try:
            updated_profile = await self.personalization_engine.update_cognitive_profile(
                user_id, 
                interaction_data
            )
            self.user_profiles[user_id] = updated_profile
            self.logger.info(f"User profile updated: {user_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating user profile {user_id}: {e}")
            return False
    
    async def train_model(self, training_data: List[Dict[str, Any]]) -> bool:
        """
        训练认知模型
        """
        try:
            success = await self.model.train(training_data)
            self.logger.info(f"Cognitive model training completed, success: {success}")
            return success
        except Exception as e:
            self.logger.error(f"Error training cognitive model: {e}")
            return False


class CognitiveModelImpl(CognitiveModel):
    """
    认知模型实现
    """
    def __init__(self):
        self.neural_model = NeuralCognitiveModel()
        self.patterns: Dict[str, CognitivePattern] = {}
        self.logger = logging.getLogger(__name__)
    
    async def process(self, task: CognitiveTask) -> CognitiveResult:
        """
        处理认知任务
        """
        # 使用神经认知模型处理任务
        return await self.neural_model.process(task)
    
    async def update_model(self, user_id: str, feedback: Dict[str, Any]) -> bool:
        """
        更新模型
        """
        return await self.neural_model.update(user_id, feedback)
    
    async def get_cognitive_profile(self, user_id: str) -> Optional[CognitiveProfile]:
        """
        获取认知画像
        """
        return await self.neural_model.get_cognitive_profile(user_id)
    
    async def store_cognitive_pattern(self, pattern: CognitivePattern) -> bool:
        """
        存储认知模式
        """
        try:
            self.patterns[pattern.id] = pattern
            self.logger.info(f"Cognitive pattern stored: {pattern.id}")
            return True
        except Exception as e:
            self.logger.error(f"Error storing cognitive pattern: {e}")
            return False
    
    async def get_cognitive_pattern(self, pattern_id: str) -> Optional[CognitivePattern]:
        """
        获取认知模式
        """
        return self.patterns.get(pattern_id)


class AdvancedCognitiveSystem(CognitiveSystem):
    """
    高级认知系统，支持更复杂的认知功能
    """
    def __init__(self):
        super().__init__()
        self.tree_of_thoughts_reasoning = TreeOfThoughtsReasoning()
        self.pattern_memory = {}  # 认知模式记忆
        self.meta_cognition_enabled = True  # 元认知能力开关
    
    async def process_complex_task(self, task: CognitiveTask) -> CognitiveResult:
        """
        处理复杂认知任务
        """
        start_time = datetime.now()
        
        try:
            # 根据任务复杂度选择推理策略
            if self._is_complex_task(task):
                reasoning_process = await self.tree_of_thoughts_reasoning.reason(
                    task.content, 
                    task.context
                )
            else:
                reasoning_process = await self.reasoning_engine.reason(
                    task.content, 
                    task.context
                )
            
            # 元认知评估
            if self.meta_cognition_enabled:
                reasoning_process = await self._meta_cognitive_evaluation(reasoning_process)
            
            # 检测和纠正偏见
            detected_biases = await self.reasoning_engine.detect_biases(reasoning_process)
            if detected_biases:
                reasoning_process = await self.reasoning_engine.correct_biases(reasoning_process, detected_biases)
            
            # 计算执行时间
            execution_time = (datetime.now() - start_time).total_seconds()
            
            result = CognitiveResult(
                success=True,
                output={
                    "conclusion": reasoning_process.conclusion,
                    "steps": [step.content for step in reasoning_process.steps],
                    "confidence": reasoning_process.confidence,
                    "reasoning_path": [step.reasoning_type for step in reasoning_process.steps]
                },
                reasoning_process=reasoning_process,
                detected_biases=detected_biases,
                confidence=reasoning_process.confidence,
                execution_time=execution_time,
                resources_used={
                    "processing_time_seconds": execution_time,
                    "reasoning_complexity": len(reasoning_process.steps)
                }
            )
            
            self.logger.info(f"Complex cognitive task processed: {task.id}")
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Error processing complex cognitive task {task.id}: {e}")
            
            return CognitiveResult(
                success=False,
                output=None,
                reasoning_process=None,
                detected_biases=[],
                confidence=0.0,
                execution_time=execution_time,
                resources_used={"processing_time_seconds": execution_time}
            )
    
    def _is_complex_task(self, task: CognitiveTask) -> bool:
        """
        判断是否为复杂任务
        """
        # 简化的复杂度判断逻辑
        content_length = len(task.content)
        complexity_indicators = ["analyze", "compare", "evaluate", "synthesize", "critique"]
        
        is_long = content_length > 200
        has_complex_indicators = any(indicator in task.content.lower() for indicator in complexity_indicators)
        
        return is_long or has_complex_indicators
    
    async def _meta_cognitive_evaluation(self, reasoning_process: ReasoningProcess) -> ReasoningProcess:
        """
        元认知评估 - 评估推理过程的质量
        """
        # 评估推理步骤的合理性
        total_steps = len(reasoning_process.steps)
        if total_steps == 0:
            return reasoning_process
        
        # 计算推理质量指标
        avg_confidence = sum(step.confidence for step in reasoning_process.steps) / total_steps
        reasoning_types = [step.reasoning_type for step in reasoning_process.steps]
        
        # 添加元认知信息到推理过程
        reasoning_process.metadata["meta_cognition"] = {
            "average_step_confidence": avg_confidence,
            "reasoning_diversity": len(set(reasoning_types)),
            "total_steps": total_steps,
            "quality_assessment": self._assess_reasoning_quality(reasoning_process)
        }
        
        return reasoning_process
    
    def _assess_reasoning_quality(self, reasoning_process: ReasoningProcess) -> str:
        """
        评估推理质量
        """
        steps = reasoning_process.steps
        if not steps:
            return "low"
        
        # 基于置信度和步骤多样性评估质量
        avg_confidence = sum(step.confidence for step in steps) / len(steps)
        diversity = len(set(step.reasoning_type for step in steps))
        
        if avg_confidence >= 0.8 and diversity >= 2:
            return "high"
        elif avg_confidence >= 0.6 and diversity >= 1:
            return "medium"
        else:
            return "low"


class CognitivePatternMatcher:
    """
    认知模式匹配器
    """
    def __init__(self):
        self.patterns: List[CognitivePattern] = []
        self.logger = logging.getLogger(__name__)
    
    def add_pattern(self, pattern: CognitivePattern):
        """
        添加认知模式
        """
        self.patterns.append(pattern)
        self.logger.info(f"Added cognitive pattern: {pattern.id}")
    
    def find_matching_patterns(self, input_text: str, threshold: float = 0.7) -> List[Tuple[CognitivePattern, float]]:
        """
        查找匹配的认知模式
        """
        matches = []
        
        for pattern in self.patterns:
            similarity = self._calculate_pattern_similarity(input_text, pattern)
            if similarity >= threshold:
                matches.append((pattern, similarity))
        
        # 按相似度排序
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
    
    def _calculate_pattern_similarity(self, text: str, pattern: CognitivePattern) -> float:
        """
        计算文本与模式的相似度
        """
        text_lower = text.lower()
        
        # 计算触发词匹配度
        trigger_matches = sum(1 for trigger in pattern.triggers if trigger.lower() in text_lower)
        trigger_score = trigger_matches / len(pattern.triggers) if pattern.triggers else 0
        
        # 计算类型匹配度
        type_score = 0.5  # 简化处理
        
        # 综合评分
        similarity = (trigger_score * 0.7) + (type_score * 0.3)
        return min(similarity, 1.0)  # 确保不超过1.0


# 工厂函数
def create_cognitive_system(system_type: str = "standard", **kwargs) -> CognitiveSystem:
    """
    创建认知系统实例
    """
    if system_type == "standard":
        return CognitiveSystem()
    elif system_type == "advanced":
        return AdvancedCognitiveSystem()
    else:
        raise ValueError(f"Unknown cognitive system type: {system_type}")