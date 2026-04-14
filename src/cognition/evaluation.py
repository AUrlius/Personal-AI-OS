"""
认知评估模块
基于 nuwa-skill 的认知能力评估架构
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from .interfaces import (
    CognitiveAssessment, AssessmentResult, CognitiveProfile, 
    ReasoningProcess, ReasoningStep, CognitiveTask
)
from .utils.bias_detector import BiasDetector


class CognitiveEvaluator:
    """
    认知评估器
    评估用户的认知能力、推理质量和偏见倾向
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.bias_detector = BiasDetector()
        self.assessment_history: Dict[str, List[CognitiveAssessment]] = {}
        self.performance_metrics: Dict[str, Dict[str, float]] = {}
    
    async def evaluate_cognitive_profile(self, user_id: str, tasks: List[CognitiveTask]) -> CognitiveProfile:
        """
        评估用户认知画像
        """
        start_time = datetime.now()
        
        try:
            assessment_results = []
            
            # 对每个任务进行评估
            for task in tasks:
                result = await self._assess_task_performance(task)
                assessment_results.append(result)
            
            # 综合分析
            profile = await self._synthesize_cognitive_profile(user_id, assessment_results)
            
            # 计算执行时间
            execution_time = (datetime.now() - start_time).total_seconds()
            
            self.logger.info(f"Cognitive profile evaluated for user {user_id}, execution time: {execution_time}s")
            return profile
            
        except Exception as e:
            self.logger.error(f"Error evaluating cognitive profile for user {user_id}: {e}")
            raise
    
    async def _assess_task_performance(self, task: CognitiveTask) -> AssessmentResult:
        """
        评估任务表现
        """
        try:
            # 执行任务（这里使用模拟，实际应该连接到推理引擎）
            reasoning_process = await self._simulate_reasoning_process(task)
            
            # 分析推理过程
            analysis = await self._analyze_reasoning_quality(reasoning_process)
            
            # 检测认知偏见
            biases = await self.bias_detector.detect_biases(reasoning_process)
            
            # 计算各项指标
            metrics = await self._calculate_cognitive_metrics(reasoning_process, analysis, biases)
            
            result = AssessmentResult(
                task_id=task.id,
                reasoning_process=reasoning_process,
                detected_biases=biases,
                cognitive_metrics=metrics,
                confidence=analysis.get('overall_confidence', 0.7),
                execution_time=analysis.get('execution_time', 0),
                resources_used=analysis.get('resources_used', {}),
                timestamp=datetime.now()
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error assessing task performance: {e}")
            return AssessmentResult(
                task_id=task.id,
                reasoning_process=None,
                detected_biases=[],
                cognitive_metrics={},
                confidence=0.0,
                execution_time=0,
                resources_used={},
                timestamp=datetime.now()
            )
    
    async def _simulate_reasoning_process(self, task: CognitiveTask) -> ReasoningProcess:
        """
        模拟推理过程（实际应用中应连接到推理引擎）
        """
        # 这里应该是真实的推理过程，为演示目的创建模拟过程
        steps = [
            ReasoningStep(
                step_number=1,
                content=f"理解任务: {task.content[:50]}...",
                reasoning_type="comprehension",
                confidence=0.9,
                supporting_evidence=[task.content],
                alternatives_considered=[],
                timestamp=datetime.now()
            ),
            ReasoningStep(
                step_number=2,
                content="分析任务要求和约束条件",
                reasoning_type="analytical",
                confidence=0.85,
                supporting_evidence=["task_requirements", "constraints"],
                alternatives_considered=[],
                timestamp=datetime.now()
            ),
            ReasoningStep(
                step_number=3,
                content="生成解决方案思路",
                reasoning_type="generative",
                confidence=0.8,
                supporting_evidence=["analysis_results"],
                alternatives_considered=["approach_a", "approach_b"],
                timestamp=datetime.now()
            ),
            ReasoningStep(
                step_number=4,
                content="验证方案可行性和有效性",
                reasoning_type="verificational",
                confidence=0.75,
                supporting_evidence=["solution_approaches"],
                alternatives_considered=["validated_approach"],
                timestamp=datetime.now()
            ),
            ReasoningStep(
                step_number=5,
                content="形成最终结论和建议",
                reasoning_type="synthetic",
                confidence=0.85,
                supporting_evidence=["validated_solution"],
                alternatives_considered=[],
                timestamp=datetime.now()
            )
        ]
        
        return ReasoningProcess(
            id=f"reasoning_{hash(task.id) % 10000}",
            input_problem=task.content,
            steps=steps,
            conclusion="基于分析得出的结论",
            confidence=0.82,
            reasoning_strategy="analytical",
            bias_indicators=[],
            timestamp=datetime.now(),
            metadata={"task_type": task.task_type, "complexity": task.complexity}
        )
    
    async def _analyze_reasoning_quality(self, process: ReasoningProcess) -> Dict[str, Any]:
        """
        分析推理质量
        """
        if not process.steps:
            return {
                "overall_confidence": 0.0,
                "execution_time": 0,
                "resources_used": {},
                "quality_indicators": {
                    "coherence": 0.0,
                    "completeness": 0.0,
                    "logical_flow": 0.0,
                    "evidence_support": 0.0
                }
            }
        
        # 分析推理步骤质量
        total_confidence = sum(step.confidence for step in process.steps)
        avg_confidence = total_confidence / len(process.steps)
        
        # 分析逻辑连贯性
        coherence_score = self._assess_logical_coherence(process.steps)
        
        # 分析完整性
        completeness_score = self._assess_completeness(process.steps)
        
        # 分析证据支持度
        evidence_support_score = self._assess_evidence_support(process.steps)
        
        # 分析推理流畅性
        logical_flow_score = self._assess_logical_flow(process.steps)
        
        analysis = {
            "overall_confidence": avg_confidence,
            "execution_time": 0,  # 实际应用中应记录执行时间
            "resources_used": {"memory_usage_mb": 0, "cpu_cycles": 0},  # 实际应用中应记录资源使用
            "quality_indicators": {
                "coherence": coherence_score,
                "completeness": completeness_score,
                "logical_flow": logical_flow_score,
                "evidence_support": evidence_support_score
            }
        }
        
        return analysis
    
    def _assess_logical_coherence(self, steps: List[ReasoningStep]) -> float:
        """
        评估逻辑连贯性
        """
        if len(steps) < 2:
            return 0.8  # 单一步骤假设为连贯
        
        coherent_transitions = 0
        total_transitions = len(steps) - 1
        
        for i in range(total_transitions):
            # 简化的连贯性评估：检查步骤内容的相关性
            current_content = steps[i].content.lower()
            next_content = steps[i + 1].content.lower()
            
            # 检查是否有连接词或逻辑关系
            transition_indicators = ["因此", "所以", "然而", "但是", "另外", "接着", "然后", "此外", "另一方面"]
            has_transition = any(indicator in next_content for indicator in transition_indicators)
            
            # 检查内容相关性（简化版本）
            content_overlap = len(set(current_content.split()) & set(next_content.split()))
            has_content_connection = content_overlap > 0
            
            if has_transition or has_content_connection:
                coherent_transitions += 1
        
        return coherent_transitions / total_transitions if total_transitions > 0 else 0.8
    
    def _assess_completeness(self, steps: List[ReasoningStep]) -> float:
        """
        评估完整性
        """
        # 基于步骤数量和推理覆盖范围评估完整性
        if len(steps) == 0:
            return 0.0
        
        # 基础分数基于步骤数量
        step_based_score = min(len(steps) * 0.2, 0.6)  # 最多60%基于步骤数量
        
        # 基于推理类型多样性
        reasoning_types = set(step.reasoning_type for step in steps)
        diversity_bonus = min(len(reasoning_types) * 0.1, 0.4)  # 最多40%基于多样性
        
        return step_based_score + diversity_bonus
    
    def _assess_evidence_support(self, steps: List[ReasoningStep]) -> float:
        """
        评估证据支持度
        """
        if not steps:
            return 0.0
        
        total_evidence = sum(len(step.supporting_evidence) for step in steps)
        total_steps = len(steps)
        
        if total_steps == 0:
            return 0.0
        
        # 平均每个步骤的证据数量
        avg_evidence_per_step = total_evidence / total_steps
        
        # 将证据数量转换为支持度分数
        evidence_score = min(avg_evidence_per_step * 0.3, 1.0)
        
        return evidence_score
    
    def _assess_logical_flow(self, steps: List[ReasoningStep]) -> float:
        """
        评估逻辑流程
        """
        if len(steps) < 2:
            return 0.8
        
        flow_score = 0.0
        transitions_analyzed = 0
        
        for i in range(len(steps) - 1):
            current_step = steps[i]
            next_step = steps[i + 1]
            
            # 评估步骤间的逻辑关系
            # 简化的评估：基于推理类型的逻辑性
            if current_step.reasoning_type == "comprehension" and next_step.reasoning_type in ["analytical", "generative"]:
                flow_score += 0.9  # 好的逻辑流程
            elif current_step.reasoning_type == "analytical" and next_step.reasoning_type in ["generative", "verificational"]:
                flow_score += 0.85  # 良好的逻辑流程
            elif current_step.reasoning_type == "generative" and next_step.reasoning_type == "verificational":
                flow_score += 0.8  # 合理的逻辑流程
            elif current_step.reasoning_type == "verificational" and next_step.reasoning_type == "synthetic":
                flow_score += 0.95  # 很好的逻辑流程
            else:
                flow_score += 0.6  # 一般逻辑流程
            
            transitions_analyzed += 1
        
        return flow_score / transitions_analyzed if transitions_analyzed > 0 else 0.8
    
    async def _calculate_cognitive_metrics(self, process: ReasoningProcess, analysis: Dict[str, Any], biases: List[BiasDetectionResult]) -> Dict[str, float]:
        """
        计算认知指标
        """
        metrics = {}
        
        # 基础指标
        metrics["reasoning_quality"] = analysis["quality_indicators"]["coherence"] * 0.3 + \
                                      analysis["quality_indicators"]["completeness"] * 0.2 + \
                                      analysis["quality_indicators"]["logical_flow"] * 0.3 + \
                                      analysis["quality_indicators"]["evidence_support"] * 0.2
        
        # 置信度指标
        metrics["confidence_calibration"] = self._calculate_confidence_calibration(process)
        
        # 偏见倾向指标
        metrics["bias_tendency"] = self._calculate_bias_tendency(biases)
        
        # 推理效率指标
        metrics["reasoning_efficiency"] = self._calculate_reasoning_efficiency(process)
        
        # 适应性指标
        metrics["adaptive_reasoning"] = self._calculate_adaptive_reasoning(process)
        
        # 元认知指标
        metrics["metacognitive_awareness"] = self._calculate_metacognitive_awareness(process)
        
        # 学习能力指标
        metrics["learning_capacity"] = self._calculate_learning_capacity(process)
        
        return metrics
    
    def _calculate_confidence_calibration(self, process: ReasoningProcess) -> float:
        """
        计算置信度校准
        """
        if not process.steps:
            return 0.5  # 默认中等校准
        
        # 检查置信度与推理质量的一致性
        avg_step_confidence = sum(step.confidence for step in process.steps) / len(process.steps)
        
        # 这里可以加入与实际结果的对比（如果有基准真值的话）
        # 简化实现：基于步骤置信度的一致性
        confidence_variance = np.var([step.confidence for step in process.steps])
        
        # 置信度校准：一致性越高越好
        calibration_score = 1.0 - min(confidence_variance * 2, 0.5)
        
        return calibration_score
    
    def _calculate_bias_tendency(self, biases: List[BiasDetectionResult]) -> float:
        """
        计算偏见倾向
        """
        if not biases:
            return 0.1  # 没有检测到偏见，倾向很低
        
        # 计算平均偏见严重程度
        avg_severity = sum(bias.severity for bias in biases) / len(biases)
        
        # 反转分数：偏见越少，倾向越低
        bias_tendency = min(avg_severity, 1.0)
        
        return bias_tendency
    
    def _calculate_reasoning_efficiency(self, process: ReasoningProcess) -> float:
        """
        计算推理效率
        """
        if not process.steps:
            return 0.5
        
        # 基于步骤数量和推理质量计算效率
        # 质量高、步骤少 = 高效率
        quality_score = sum(step.confidence for step in process.steps) / len(process.steps)
        efficiency_factor = 1.0 / max(len(process.steps), 1)  # 步骤越少效率越高
        
        # 综合效率分数
        efficiency_score = (quality_score * 0.7) + (efficiency_factor * 0.3)
        
        return min(efficiency_score, 1.0)
    
    def _calculate_adaptive_reasoning(self, process: ReasoningProcess) -> float:
        """
        计算适应性推理能力
        """
        if not process.steps:
            return 0.5
        
        # 检查推理过程中是否展示了适应性
        adaptive_indicators = 0
        total_indicators = len(process.steps)
        
        for step in process.steps:
            content_lower = step.content.lower()
            
            # 检查适应性指示词
            adaptive_terms = [
                "however", "but", "on the other hand", "alternatively", 
                "considering", "reconsidering", "adjusting", "modifying",
                "changing approach", "new perspective", "different angle"
            ]
            
            if any(term in content_lower for term in adaptive_terms):
                adaptive_indicators += 1
        
        return min(adaptive_indicators / max(total_indicators, 1) * 2, 1.0)  # 最多2倍，但不超过1.0
    
    def _calculate_metacognitive_awareness(self, process: ReasoningProcess) -> float:
        """
        计算元认知意识
        """
        if not process.steps:
            return 0.3  # 默认较低的元认知意识
        
        meta_cognitive_indicators = 0
        total_indicators = len(process.steps)
        
        for step in process.steps:
            content_lower = step.content.lower()
            
            # 检查元认知指示词
            meta_terms = [
                "I think", "I believe", "I consider", "it seems", "appears to be",
                "this suggests", "indicates that", "implies", "could mean",
                "potential error", "possible mistake", "need to verify",
                "checking my reasoning", "reflecting on", "considering alternatives"
            ]
            
            if any(term in content_lower for term in meta_terms):
                meta_cognitive_indicators += 1
        
        return min(meta_cognitive_indicators / max(total_indicators, 1) * 2, 1.0)
    
    def _calculate_learning_capacity(self, process: ReasoningProcess) -> float:
        """
        计算学习能力
        """
        if not process.steps:
            return 0.4  # 默认中等学习能力
        
        learning_indicators = 0
        total_indicators = len(process.steps)
        
        for step in process.steps:
            content_lower = step.content.lower()
            
            # 检查学习指示词
            learning_terms = [
                "learned", "realized", "discovered", "understood", "gained insight",
                "new information", "changed my view", "updated my belief",
                "incorporating new data", "building on previous knowledge",
                "connecting concepts", "making connections", "drawing parallels"
            ]
            
            if any(term in content_lower for term in learning_terms):
                learning_indicators += 1
        
        return min(learning_indicators / max(total_indicators, 1) * 2, 1.0)
    
    async def _synthesize_cognitive_profile(self, user_id: str, assessment_results: List[AssessmentResult]) -> CognitiveProfile:
        """
        综合分析认知画像
        """
        if not assessment_results:
            # 返回默认画像
            return CognitiveProfile(
                user_id=user_id,
                reasoning_style="balanced",
                decision_making="rational",
                learning_preference="mixed",
                attention_span=25,
                processing_speed="normal",
                memory_strength="working",
                bias_tendencies={},
                performance_history=[],
                last_updated=datetime.now()
            )
        
        # 计算各项能力的平均值
        reasoning_styles = []
        decision_making_styles = []
        learning_preferences = []
        
        total_metrics = {}
        for result in assessment_results:
            for metric, value in result.cognitive_metrics.items():
                if metric not in total_metrics:
                    total_metrics[metric] = []
                total_metrics[metric].append(value)
        
        # 计算平均指标
        averaged_metrics = {}
        for metric, values in total_metrics.items():
            averaged_metrics[metric] = sum(values) / len(values)
        
        # 确定推理风格
        reasoning_quality = averaged_metrics.get("reasoning_quality", 0.5)
        adaptive_score = averaged_metrics.get("adaptive_reasoning", 0.5)
        metacognitive_score = averaged_metrics.get("metacognitive_awareness", 0.5)
        
        if adaptive_score > 0.7 and metacognitive_score > 0.6:
            reasoning_style = "adaptive_reflective"
        elif reasoning_quality > 0.7:
            reasoning_style = "analytical"
        elif adaptive_score > 0.6:
            reasoning_style = "flexible"
        else:
            reasoning_style = "balanced"
        
        # 确定决策风格
        bias_tendency = averaged_metrics.get("bias_tendency", 0.3)
        confidence_calibration = averaged_metrics.get("confidence_calibration", 0.5)
        
        if bias_tendency < 0.3 and confidence_calibration > 0.6:
            decision_making_style = "rational"
        elif bias_tendency > 0.6:
            decision_making_style = "intuitive"
        else:
            decision_making_style = "balanced"
        
        # 确定学习偏好
        learning_capacity = averaged_metrics.get("learning_capacity", 0.5)
        if learning_capacity > 0.7:
            learning_preference = "active"
        elif learning_capacity > 0.5:
            learning_preference = "mixed"
        else:
            learning_preference = "passive"
        
        # 计算注意力跨度（基于任务完成情况）
        attention_span = self._calculate_attention_span(assessment_results)
        
        # 计算处理速度（基于执行时间）
        processing_speed = self._calculate_processing_speed(assessment_results)
        
        # 计算记忆强度（基于推理一致性）
        memory_strength = self._calculate_memory_strength(assessment_results)
        
        # 汇总偏见倾向
        bias_tendencies = self._aggregate_bias_tendencies(assessment_results)
        
        # 创建认知画像
        profile = CognitiveProfile(
            user_id=user_id,
            reasoning_style=reasoning_style,
            decision_making=decision_making_style,
            learning_preference=learning_preference,
            attention_span=attention_span,
            processing_speed=processing_speed,
            memory_strength=memory_strength,
            bias_tendencies=bias_tendencies,
            performance_history=[
                {
                    "task_type": result.task_id,
                    "metrics": result.cognitive_metrics,
                    "timestamp": result.timestamp
                }
                for result in assessment_results
            ],
            last_updated=datetime.now()
        )
        
        # 存储评估历史
        if user_id not in self.assessment_history:
            self.assessment_history[user_id] = []
        self.assessment_history[user_id].extend(assessment_results)
        
        # 限制历史长度
        if len(self.assessment_history[user_id]) > 100:
            self.assessment_history[user_id] = self.assessment_history[user_id][-50:]
        
        return profile
    
    def _calculate_attention_span(self, results: List[AssessmentResult]) -> int:
        """
        计算注意力跨度
        """
        # 基于任务复杂度和完成质量计算
        if not results:
            return 25  # 默认25分钟
        
        # 简化的计算：基于任务复杂度和推理质量
        total_complexity = sum(
            len(result.reasoning_process.steps) if result.reasoning_process else 0 
            for result in results
        )
        
        avg_quality = sum(
            result.cognitive_metrics.get("reasoning_quality", 0.5) 
            for result in results
        ) / len(results)
        
        # 基于复杂度和质量估算注意力跨度
        attention_span = 15 + (total_complexity / len(results)) * 0.5 + (avg_quality * 10)
        
        return min(int(attention_span), 60)  # 最多60分钟
    
    def _calculate_processing_speed(self, results: List[AssessmentResult]) -> str:
        """
        计算处理速度
        """
        if not results:
            return "normal"
        
        # 基于执行时间计算
        avg_execution_time = sum(result.execution_time for result in results) / len(results)
        
        if avg_execution_time < 2.0:  # 少于2秒
            return "fast"
        elif avg_execution_time < 5.0:  # 2-5秒
            return "normal"
        else:  # 超过5秒
            return "slow"
    
    def _calculate_memory_strength(self, results: List[AssessmentResult]) -> str:
        """
        计算记忆强度
        """
        if not results:
            return "working"
        
        # 基于推理一致性计算
        consistency_scores = []
        for result in results:
            if result.reasoning_process and result.reasoning_process.steps:
                # 简化的记忆强度评估
                consistency = sum(step.confidence for step in result.reasoning_process.steps) / len(result.reasoning_process.steps)
                consistency_scores.append(consistency)
        
        if not consistency_scores:
            return "working"
        
        avg_consistency = sum(consistency_scores) / len(consistency_scores)
        
        if avg_consistency > 0.8:
            return "strong"
        elif avg_consistency > 0.6:
            return "working"
        else:
            return "weak"
    
    def _aggregate_bias_tendencies(self, results: List[AssessmentResult]) -> Dict[str, float]:
        """
        汇总偏见倾向
        """
        bias_aggregates = {}
        
        for result in results:
            for bias in result.detected_biases:
                bias_type = bias.type
                if bias_type not in bias_aggregates:
                    bias_aggregates[bias_type] = []
                bias_aggregates[bias_type].append(bias.severity)
        
        # 计算每种偏见的平均严重程度
        averaged_biases = {}
        for bias_type, severities in bias_aggregates.items():
            averaged_biases[bias_type] = sum(severities) / len(severities)
        
        return averaged_biases
    
    async def evaluate_reasoning_quality(self, reasoning_process: ReasoningProcess) -> Dict[str, float]:
        """
        评估推理质量
        """
        if not reasoning_process.steps:
            return {
                "coherence": 0.0,
                "completeness": 0.0,
                "logical_consistency": 0.0,
                "evidence_support": 0.0,
                "creativity": 0.0,
                "critical_thinking": 0.0,
                "overall_quality": 0.0
            }
        
        # 评估各项质量指标
        coherence = self._assess_logical_coherence(reasoning_process.steps)
        completeness = self._assess_completeness(reasoning_process.steps)
        evidence_support = self._assess_evidence_support(reasoning_process.steps)
        logical_flow = self._assess_logical_flow(reasoning_process.steps)
        
        # 创造性评估
        creativity = self._assess_creativity(reasoning_process.steps)
        
        # 批判性思维评估
        critical_thinking = self._assess_critical_thinking(reasoning_process.steps)
        
        # 综合质量分数
        overall_quality = (
            coherence * 0.2 +
            completeness * 0.2 +
            evidence_support * 0.2 +
            logical_flow * 0.15 +
            creativity * 0.15 +
            critical_thinking * 0.1
        )
        
        return {
            "coherence": coherence,
            "completeness": completeness,
            "logical_consistency": logical_flow,
            "evidence_support": evidence_support,
            "creativity": creativity,
            "critical_thinking": critical_thinking,
            "overall_quality": overall_quality
        }
    
    def _assess_creativity(self, steps: List[ReasoningStep]) -> float:
        """
        评估创造性
        """
        if not steps:
            return 0.3
        
        creative_indicators = 0
        total_indicators = len(steps)
        
        for step in steps:
            content_lower = step.content.lower()
            
            # 检查创造性指示词
            creative_terms = [
                "novel", "innovative", "unique", "original", "unusual",
                "different approach", "new perspective", "creative solution",
                "think outside", "breakthrough", "revolutionary", "groundbreaking",
                "unconventional", "non-obvious", "unexpected"
            ]
            
            if any(term in content_lower for term in creative_terms):
                creative_indicators += 1
        
        return min(creative_indicators / max(total_indicators, 1) * 3, 1.0)  # 给创造性更多权重
    
    def _assess_critical_thinking(self, steps: List[ReasoningStep]) -> float:
        """
        评估批判性思维
        """
        if not steps:
            return 0.4
        
        critical_indicators = 0
        total_indicators = len(steps)
        
        for step in steps:
            content_lower = step.content.lower()
            
            # 检查批判性思维指示词
            critical_terms = [
                "question", "challenge", "examine", "analyze", "evaluate",
                "assumption", "evidence", "proof", "verify", "validate",
                "counterargument", "opposing view", "alternative explanation",
                "critical analysis", "skeptical", "doubt", "questioning"
            ]
            
            if any(term in content_lower for term in critical_terms):
                critical_indicators += 1
        
        return min(critical_indicators / max(total_indicators, 1) * 2, 1.0)
    
    async def generate_cognitive_insights(self, user_id: str) -> Dict[str, Any]:
        """
        生成认知洞察
        """
        try:
            if user_id not in self.assessment_history:
                return {"message": "No assessment history found for user", "user_id": user_id}
            
            assessments = self.assessment_history[user_id]
            
            insights = {
                "user_id": user_id,
                "total_assessments": len(assessments),
                "last_assessment": assessments[-1].timestamp if assessments else None,
                "cognitive_profile_summary": await self._get_profile_summary(user_id),
                "trend_analysis": await self._analyze_trends(user_id),
                "strengths_identified": await self._identify_strengths(user_id),
                "improvement_areas": await self._identify_improvement_areas(user_id),
                "bias_patterns": await self._analyze_bias_patterns(user_id),
                "generated_at": datetime.now().isoformat()
            }
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Error generating cognitive insights for user {user_id}: {e}")
            return {"error": str(e), "user_id": user_id}
    
    async def _get_profile_summary(self, user_id: str) -> Dict[str, Any]:
        """
        获取画像摘要
        """
        profile = await self.get_current_cognitive_profile(user_id)
        if not profile:
            return {"message": "No cognitive profile found"}
        
        return {
            "reasoning_style": profile.reasoning_style,
            "decision_making": profile.decision_making,
            "learning_preference": profile.learning_preference,
            "attention_span_minutes": profile.attention_span,
            "processing_speed": profile.processing_speed,
            "memory_strength": profile.memory_strength,
            "top_biases": sorted(profile.bias_tendencies.items(), key=lambda x: x[1], reverse=True)[:3],
            "last_updated": profile.last_updated.isoformat() if profile.last_updated else None
        }
    
    async def _analyze_trends(self, user_id: str) -> Dict[str, Any]:
        """
        分析趋势
        """
        if user_id not in self.assessment_history:
            return {"message": "No history available for trend analysis"}
        
        assessments = self.assessment_history[user_id]
        
        if len(assessments) < 2:
            return {"message": "Insufficient data for trend analysis"}
        
        # 分析各项指标的趋势
        metrics_over_time = {
            "reasoning_quality": [],
            "confidence_calibration": [],
            "bias_tendency": [],
            "reasoning_efficiency": []
        }
        
        for assessment in assessments[-10:]:  # 分析最近10次评估
            for metric in metrics_over_time.keys():
                if metric in assessment.cognitive_metrics:
                    metrics_over_time[metric].append(assessment.cognitive_metrics[metric])
        
        trends = {}
        for metric, values in metrics_over_time.items():
            if len(values) >= 2:
                # 计算趋势（简单线性趋势）
                if len(values) == 1:
                    trends[metric] = "stable"
                else:
                    # 计算斜率
                    time_points = list(range(len(values)))
                    slope = np.polyfit(time_points, values, 1)[0] if len(values) > 1 else 0
                    
                    if slope > 0.05:
                        trends[metric] = "improving"
                    elif slope < -0.05:
                        trends[metric] = "declining"
                    else:
                        trends[metric] = "stable"
            else:
                trends[metric] = "insufficient_data"
        
        return {
            "metric_trends": trends,
            "improvement_rate": self._calculate_improvement_rate(metrics_over_time),
            "consistency_score": self._calculate_consistency(metrics_over_time)
        }
    
    def _calculate_improvement_rate(self, metrics_over_time: Dict[str, List[float]]) -> float:
        """
        计算改善率
        """
        improvement_count = 0
        total_metrics = 0
        
        for metric, values in metrics_over_time.items():
            if len(values) >= 2:
                total_metrics += 1
                # 比较最后两个值
                if values[-1] > values[-2]:
                    improvement_count += 1
        
        return improvement_count / total_metrics if total_metrics > 0 else 0.0
    
    def _calculate_consistency(self, metrics_over_time: Dict[str, List[float]]) -> float:
        """
        计算一致性
        """
        consistencies = []
        
        for metric, values in metrics_over_time.items():
            if len(values) >= 2:
                # 计算标准差的倒数作为一致性指标
                std = np.std(values)
                mean = np.mean(values)
                if mean != 0:
                    coefficient_of_variation = std / abs(mean) if abs(mean) > 0.01 else 1.0
                    consistency = max(0, 1 - coefficient_of_variation)  # 一致性 = 1 - 变异系数
                    consistencies.append(consistency)
        
        return sum(consistencies) / len(consistencies) if consistencies else 0.5
    
    async def _identify_strengths(self, user_id: str) -> List[Dict[str, Any]]:
        """
        识别优势
        """
        profile = await self.get_current_cognitive_profile(user_id)
        if not profile:
            return []
        
        strengths = []
        
        # 根据画像识别优势
        if profile.reasoning_style in ["analytical", "adaptive_reflective"]:
            strengths.append({
                "area": "reasoning",
                "description": f"Strong analytical and systematic reasoning abilities ({profile.reasoning_style})"
            })
        
        if profile.decision_making == "rational":
            strengths.append({
                "area": "decision_making", 
                "description": "Rational and well-calibrated decision making abilities"
            })
        
        if profile.learning_preference == "active":
            strengths.append({
                "area": "learning",
                "description": "Active learning approach with strong capacity for incorporating new information"
            })
        
        if profile.attention_span > 30:
            strengths.append({
                "area": "attention",
                "description": f"Strong attention span ({profile.attention_span} minutes) allowing for deep focus"
            })
        
        if profile.processing_speed == "fast":
            strengths.append({
                "area": "processing",
                "description": "Quick processing speed enabling rapid analysis"
            })
        
        if profile.memory_strength == "strong":
            strengths.append({
                "area": "memory",
                "description": "Strong memory capabilities supporting consistent reasoning"
            })
        
        return strengths
    
    async def _identify_improvement_areas(self, user_id: str) -> List[Dict[str, Any]]:
        """
        识别改进领域
        """
        profile = await self.get_current_cognitive_profile(user_id)
        if not profile:
            return []
        
        improvement_areas = []
        
        # 根据画像识别改进领域
        if profile.reasoning_style == "balanced":
            improvement_areas.append({
                "area": "reasoning",
                "description": "Could develop more specialized reasoning approaches for complex problems",
                "suggestion": "Practice analytical and creative reasoning exercises"
            })
        
        if profile.bias_tendencies:
            # 找出最严重的偏见
            worst_bias = max(profile.bias_tendencies.items(), key=lambda x: x[1])
            improvement_areas.append({
                "area": "bias_awareness",
                "description": f"High tendency toward {worst_bias[0]} bias (severity: {worst_bias[1]:.2f})",
                "suggestion": f"Practice awareness and mitigation techniques for {worst_bias[0]} bias"
            })
        
        if profile.attention_span < 20:
            improvement_areas.append({
                "area": "attention",
                "description": f"Attention span ({profile.attention_span} minutes) could be improved for complex tasks",
                "suggestion": "Practice mindfulness and focused attention exercises"
            })
        
        if profile.processing_speed == "slow":
            improvement_areas.append({
                "area": "processing",
                "description": "Processing speed could be enhanced for time-sensitive tasks",
                "suggestion": "Practice rapid decision-making exercises"
            })
        
        if profile.memory_strength == "weak":
            improvement_areas.append({
                "area": "memory",
                "description": "Memory strength could be enhanced to support complex reasoning",
                "suggestion": "Use memory aids and practice chunking techniques"
            })
        
        return improvement_areas
    
    async def _analyze_bias_patterns(self, user_id: str) -> Dict[str, Any]:
        """
        分析偏见模式
        """
        profile = await self.get_current_cognitive_profile(user_id)
        if not profile or not profile.bias_tendencies:
            return {"message": "No bias tendencies recorded"}
        
        # 分析偏见模式
        severe_biases = {k: v for k, v in profile.bias_tendencies.items() if v > 0.6}
        moderate_biases = {k: v for k, v in profile.bias_tendencies.items() if 0.3 <= v <= 0.6}
        mild_biases = {k: v for k, v in profile.bias_tendencies.items() if v < 0.3}
        
        return {
            "severe_biases": severe_biases,
            "moderate_biases": moderate_biases,
            "mild_biases": mild_biases,
            "bias_diversity": len(profile.bias_tendencies),
            "overall_bias_level": sum(profile.bias_tendencies.values()) / len(profile.bias_tendencies) if profile.bias_tendencies else 0
        }


class AdvancedCognitiveEvaluator(CognitiveEvaluator):
    """
    高级认知评估器
    包含更复杂的评估算法和长期跟踪
    """
    def __init__(self):
        super().__init__()
        self.longitudinal_tracking = True
        self.cross_domain_analysis = True
        self.meta_cognitive_evaluation = True
    
    async def evaluate_longitudinal_cognitive_changes(self, user_id: str, time_period: str = "30d") -> Dict[str, Any]:
        """
        评估长期认知变化
        """
        try:
            if user_id not in self.assessment_history:
                return {"message": "No assessment history for user", "user_id": user_id}
            
            # 根据时间周期过滤历史记录
            cutoff_date = datetime.now() - timedelta(days=30 if time_period.endswith('30d') else 7)
            recent_assessments = [
                a for a in self.assessment_history[user_id] 
                if a.timestamp >= cutoff_date
            ]
            
            if len(recent_assessments) < 2:
                return {"message": "Insufficient data for longitudinal analysis", "required_minimum": 2, "actual": len(recent_assessments)}
            
            # 分析变化趋势
            changes = await self._analyze_cognitive_changes(recent_assessments)
            
            return {
                "user_id": user_id,
                "time_period": time_period,
                "assessments_analyzed": len(recent_assessments),
                "start_date": min(a.timestamp for a in recent_assessments).isoformat(),
                "end_date": max(a.timestamp for a in recent_assessments).isoformat(),
                "changes_identified": changes,
                "improvement_areas": await self._identify_improvement_trends(changes),
                "concerning_patterns": await self._identify_concerning_patterns(changes),
                "recommendations": await self._generate_longitudinal_recommendations(changes),
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in longitudinal cognitive evaluation: {e}")
            return {"error": str(e), "user_id": user_id}
    
    async def _analyze_cognitive_changes(self, assessments: List[AssessmentResult]) -> Dict[str, Any]:
        """
        分析认知变化
        """
        if len(assessments) < 2:
            return {"message": "Need at least 2 assessments for change analysis"}
        
        # 按时间排序
        sorted_assessments = sorted(assessments, key=lambda x: x.timestamp)
        
        # 计算各项指标的变化
        changes = {}
        
        # 计算首末评估的差异
        first_assessment = sorted_assessments[0]
        last_assessment = sorted_assessments[-1]
        
        for metric in first_assessment.cognitive_metrics:
            if metric in last_assessment.cognitive_metrics:
                first_value = first_assessment.cognitive_metrics[metric]
                last_value = last_assessment.cognitive_metrics[metric]
                change = last_value - first_value
                percent_change = (change / first_value * 100) if first_value != 0 else 0
                
                changes[metric] = {
                    "initial_value": first_value,
                    "final_value": last_value,
                    "absolute_change": change,
                    "percent_change": percent_change,
                    "trend": "improving" if change > 0.05 else "declining" if change < -0.05 else "stable"
                }
        
        # 分析偏见模式变化
        first_biases = {b.type: b.severity for b in first_assessment.detected_biases}
        last_biases = {b.type: b.severity for b in last_assessment.detected_biases}
        
        bias_changes = {}
        all_bias_types = set(first_biases.keys()) | set(last_biases.keys())
        
        for bias_type in all_bias_types:
            first_severity = first_biases.get(bias_type, 0)
            last_severity = last_biases.get(bias_type, 0)
            change = last_severity - first_severity
            
            bias_changes[bias_type] = {
                "initial_severity": first_severity,
                "final_severity": last_severity,
                "change": change,
                "trend": "increasing" if change > 0.1 else "decreasing" if change < -0.1 else "stable"
            }
        
        return {
            "metric_changes": changes,
            "bias_changes": bias_changes,
            "overall_trajectory": self._determine_overall_trajectory(changes)
        }
    
    def _determine_overall_trajectory(self, changes: Dict[str, Any]) -> str:
        """
        确定总体轨迹
        """
        improving_metrics = sum(1 for v in changes.values() if v.get("trend") == "improving")
        declining_metrics = sum(1 for v in changes.values() if v.get("trend") == "declining")
        
        if improving_metrics > declining_metrics * 1.5:
            return "improving"
        elif declining_metrics > improving_metrics * 1.5:
            return "declining"
        else:
            return "stable"
    
    async def _identify_improvement_trends(self, changes: Dict[str, Any]) -> List[str]:
        """
        识别改进趋势
        """
        improvements = []
        
        for metric, data in changes.get("metric_changes", {}).items():
            if data.get("trend") == "improving" and abs(data.get("percent_change", 0)) > 5:
                improvements.append(f"{metric} improved by {data['percent_change']:.1f}%")
        
        for bias_type, data in changes.get("bias_changes", {}).items():
            if data.get("trend") == "decreasing" and data.get("change", 0) < -0.1:
                improvements.append(f"{bias_type} bias reduced by {abs(data['change']):.2f}")
        
        return improvements
    
    async def _identify_concerning_patterns(self, changes: Dict[str, Any]) -> List[str]:
        """
        识别令人担忧的模式
        """
        concerns = []
        
        for metric, data in changes.get("metric_changes", {}).items():
            if data.get("trend") == "declining" and abs(data.get("percent_change", 0)) > 10:
                concerns.append(f"{metric} declined by {abs(data['percent_change']):.1f}%")
        
        for bias_type, data in changes.get("bias_changes", {}).items():
            if data.get("trend") == "increasing" and data.get("change", 0) > 0.15:
                concerns.append(f"{bias_type} bias increased by {data['change']:.2f}")
        
        return concerns
    
    async def _generate_longitudinal_recommendations(self, changes: Dict[str, Any]) -> List[str]:
        """
        生成纵向建议
        """
        recommendations = []
        
        if changes.get("overall_trajectory") == "declining":
            recommendations.append("Overall cognitive performance appears to be declining. Consider taking a break and focusing on cognitive rest.")
        
        # 基于具体变化提供建议
        metric_changes = changes.get("metric_changes", {})
        if "reasoning_quality" in metric_changes:
            rq_change = metric_changes["reasoning_quality"]
            if rq_change["trend"] == "declining":
                recommendations.append("Reasoning quality is declining. Practice structured reasoning exercises.")
            elif rq_change["trend"] == "improving":
                recommendations.append("Continue current approach - reasoning quality is improving.")
        
        bias_changes = changes.get("bias_changes", {})
        if "confirmation" in bias_changes:
            conf_bias_change = bias_changes["confirmation"]
            if conf_bias_change["trend"] == "increasing":
                recommendations.append("Confirmation bias is increasing. Actively seek out opposing viewpoints.")
        
        if not recommendations:
            recommendations.append("Cognitive performance remains stable. Continue current practices.")
        
        return recommendations
    
    async def cross_domain_cognitive_analysis(self, user_id: str) -> Dict[str, Any]:
        """
        跨领域认知分析
        """
        try:
            if user_id not in self.assessment_history:
                return {"message": "No assessment history for user", "user_id": user_id}
            
            assessments = self.assessment_history[user_id]
            
            # 按领域分组
            domain_assessments = {}
            for assessment in assessments:
                domain = assessment.metadata.get("domain", "general") if hasattr(assessment, 'metadata') and assessment.metadata else "general"
                if domain not in domain_assessments:
                    domain_assessments[domain] = []
                domain_assessments[domain].append(assessment)
            
            domain_analysis = {}
            for domain, domain_assessments_list in domain_assessments.items():
                if len(domain_assessments_list) >= 1:
                    # 计算该领域的平均表现
                    avg_metrics = {}
                    for metric in ["reasoning_quality", "confidence_calibration", "reasoning_efficiency"]:
                        values = [a.cognitive_metrics.get(metric, 0) for a in domain_assessments_list]
                        if values:
                            avg_metrics[metric] = sum(values) / len(values)
                    
                    # 识别该领域的偏见模式
                    all_biases = []
                    for assessment in domain_assessments_list:
                        all_biases.extend(assessment.detected_biases)
                    
                    bias_pattern = {}
                    for bias in all_biases:
                        if bias.type not in bias_pattern:
                            bias_pattern[bias.type] = []
                        bias_pattern[bias.type].append(bias.severity)
                    
                    avg_bias_severity = {k: sum(v)/len(v) for k, v in bias_pattern.items()}
                    
                    domain_analysis[domain] = {
                        "average_performance": avg_metrics,
                        "bias_patterns": avg_bias_severity,
                        "sample_size": len(domain_assessments_list),
                        "strengths": self._identify_domain_strengths(avg_metrics),
                        "weaknesses": self._identify_domain_weaknesses(avg_metrics)
                    }
            
            # 识别跨领域模式
            cross_domain_patterns = await self._identify_cross_domain_patterns(domain_analysis)
            
            return {
                "user_id": user_id,
                "domains_analyzed": list(domain_analysis.keys()),
                "domain_performance": domain_analysis,
                "cross_domain_patterns": cross_domain_patterns,
                "transfer_opportunities": await self._identify_transfer_opportunities(domain_analysis),
                "domain_specific_recommendations": await self._generate_domain_specific_recommendations(domain_analysis),
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in cross-domain cognitive analysis: {e}")
            return {"error": str(e), "user_id": user_id}
    
    def _identify_domain_strengths(self, metrics: Dict[str, float]) -> List[str]:
        """
        识别领域优势
        """
        strengths = []
        if metrics.get("reasoning_quality", 0) > 0.7:
            strengths.append("high reasoning quality")
        if metrics.get("confidence_calibration", 0) > 0.7:
            strengths.append("well-calibrated confidence")
        if metrics.get("reasoning_efficiency", 0) > 0.7:
            strengths.append("efficient reasoning")
        return strengths
    
    def _identify_domain_weaknesses(self, metrics: Dict[str, float]) -> List[str]:
        """
        识别领域弱点
        """
        weaknesses = []
        if metrics.get("reasoning_quality", 1.0) < 0.5:
            weaknesses.append("low reasoning quality")
        if metrics.get("confidence_calibration", 1.0) < 0.5:
            weaknesses.append("poor confidence calibration")
        if metrics.get("reasoning_efficiency", 1.0) < 0.5:
            weaknesses.append("inefficient reasoning")
        return weaknesses
    
    async def _identify_cross_domain_patterns(self, domain_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        识别跨领域模式
        """
        # 检查是否存在跨领域的共同模式
        all_domains = list(domain_analysis.keys())
        
        if len(all_domains) < 2:
            return {"message": "Need at least 2 domains for cross-domain analysis"}
        
        # 检查偏见的一致性
        bias_consistency = {}
        for bias_type in set().union(*(domain_analysis[domain]["bias_patterns"].keys() for domain in all_domains)):
            severities = []
            for domain in all_domains:
                if bias_type in domain_analysis[domain]["bias_patterns"]:
                    severities.append(domain_analysis[domain]["bias_patterns"][bias_type])
            
            if len(severities) > 1:
                # 计算偏见在不同领域的一致性
                std_dev = np.std(severities)
                consistency = 1 - min(std_dev, 0.5)  # 一致性 = 1 - 标准差
                bias_consistency[bias_type] = {
                    "consistency_score": consistency,
                    "average_severity": np.mean(severities),
                    "domains_affected": len(severities)
                }
        
        # 检查能力的一致性
        capability_consistency = {}
        for metric in ["reasoning_quality", "confidence_calibration", "reasoning_efficiency"]:
            values = []
            for domain in all_domains:
                if metric in domain_analysis[domain]["average_performance"]:
                    values.append(domain_analysis[domain]["average_performance"][metric])
            
            if len(values) > 1:
                std_dev = np.std(values)
                consistency = 1 - min(std_dev, 0.5)
                capability_consistency[metric] = {
                    "consistency_score": consistency,
                    "average_performance": np.mean(values)
                }
        
        return {
            "bias_consistency": bias_consistency,
            "capability_consistency": capability_consistency,
            "universal_strengths": self._identify_universal_strengths(bias_consistency, capability_consistency),
            "universal_challenges": self._identify_universal_challenges(bias_consistency, capability_consistency)
        }
    
    def _identify_universal_strengths(self, bias_consistency: Dict[str, Any], capability_consistency: Dict[str, Any]) -> List[str]:
        """
        识别普遍优势
        """
        strengths = []
        
        # 低偏见一致性（偏见在各领域都较轻）
        for bias_type, data in bias_consistency.items():
            if data["average_severity"] < 0.3 and data["consistency_score"] > 0.7:
                strengths.append(f"Consistent low {bias_type} bias across domains")
        
        # 高能力一致性（能力在各领域都较强）
        for capability, data in capability_consistency.items():
            if data["average_performance"] > 0.7 and data["consistency_score"] > 0.7:
                strengths.append(f"Consistent high {capability} across domains")
        
        return strengths
    
    def _identify_universal_challenges(self, bias_consistency: Dict[str, Any], capability_consistency: Dict[str, Any]) -> List[str]:
        """
        识别普遍挑战
        """
        challenges = []
        
        # 高偏见一致性（偏见在各领域都较重）
        for bias_type, data in bias_consistency.items():
            if data["average_severity"] > 0.6 and data["consistency_score"] > 0.7:
                challenges.append(f"Consistent high {bias_type} bias across domains")
        
        # 低能力一致性（能力在各领域都较弱）
        for capability, data in capability_consistency.items():
            if data["average_performance"] < 0.5 and data["consistency_score"] > 0.7:
                challenges.append(f"Consistent low {capability} across domains")
        
        return challenges


# 工厂函数
def create_evaluator(evaluator_type: str = "standard", **kwargs) -> object:
    """
    创建评估器实例
    """
    if evaluator_type == "standard":
        return CognitiveEvaluator()
    elif evaluator_type == "advanced":
        return AdvancedCognitiveEvaluator()
    else:
        raise ValueError(f"Unknown evaluator type: {evaluator_type}")