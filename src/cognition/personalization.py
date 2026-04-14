"""
个性化引擎实现
基于 nuwa-skill 的个性化认知架构
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import numpy as np
from .interfaces import (
    CognitiveTask, CognitiveProfile, CognitiveResult,
    ReasoningProcess, ReasoningStep
)


class CognitivePersonalizationEngine:
    """
    认知个性化引擎
    基于 nuwa-skill 的个性化认知架构
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.user_interaction_history: Dict[str, List[Dict[str, Any]]] = {}
        self.personalization_models: Dict[str, Dict[str, Any]] = {}
        self.learning_rate = 0.1
        self.forgetting_factor = 0.95  # 遏忘因子
    
    async def adapt_reasoning_strategy(self, task: CognitiveTask, profile: CognitiveProfile) -> str:
        """
        根据用户画像调整推理策略
        """
        try:
            # 根据用户的推理风格选择策略
            reasoning_style = profile.reasoning_style
            
            if reasoning_style == "analytical":
                # 分析型用户适合链式思维
                return "chain_of_thought"
            elif reasoning_style == "intuitive":
                # 直觉型用户适合树状思维
                return "tree_of_thoughts"
            elif reasoning_style == "balanced":
                # 平衡型用户根据任务类型选择
                return await self._select_strategy_by_task_type(task, profile)
            else:
                # 默认使用链式思维
                return "chain_of_thought"
                
        except Exception as e:
            self.logger.error(f"Error adapting reasoning strategy: {e}")
            return "chain_of_thought"  # 默认策略
    
    async def _select_strategy_by_task_type(self, task: CognitiveTask, profile: CognitiveProfile) -> str:
        """
        根据任务类型选择推理策略
        """
        task_type = task.task_type
        
        if task_type in ["analysis", "evaluation"]:
            # 分析和评估任务适合链式思维
            return "chain_of_thought"
        elif task_type in ["creation", "brainstorming"]:
            # 创造和头脑风暴适合树状思维
            return "tree_of_thoughts"
        elif task_type in ["decision", "problem_solving"]:
            # 决策和问题解决适合 ReAct
            return "react"
        else:
            # 其他任务根据用户偏好
            return self._select_based_on_preferences(profile)
    
    def _select_based_on_preferences(self, profile: CognitiveProfile) -> str:
        """
        根据用户偏好选择策略
        """
        # 根据学习偏好和处理速度选择
        learning_pref = profile.learning_preference
        speed = profile.processing_speed
        
        if learning_pref in ["visual", "reading"] and speed in ["slow", "normal"]:
            # 视觉和阅读型，较慢处理速度适合链式思维
            return "chain_of_thought"
        elif learning_pref == "kinesthetic" or speed == "fast":
            # 动觉型或快速处理适合树状思维
            return "tree_of_thoughts"
        else:
            return "chain_of_thought"
    
    async def personalize_task(self, task: CognitiveTask, profile: CognitiveProfile) -> CognitiveTask:
        """
        个性化任务
        """
        try:
            # 根据用户认知特征调整任务
            personalized_task = task
            
            # 根据注意力跨度调整任务复杂度
            if profile.attention_span < 15:  # 注意力较短
                personalized_task = await self._simplify_task(task)
            elif profile.attention_span > 30:  # 注意力较长
                personalized_task = await self._enrich_task(task)
            
            # 根据处理速度调整任务详细程度
            if profile.processing_speed == "slow":
                personalized_task = await self._simplify_task_details(task)
            elif profile.processing_speed == "fast":
                personalized_task = await self._add_task_details(task)
            
            # 根据记忆强度调整信息呈现方式
            if profile.memory_strength == "working":
                personalized_task = await self._reduce_memory_load(task)
            elif profile.memory_strength == "long_term":
                personalized_task = await self._add_contextual_info(task)
            
            self.logger.info(f"Task personalized for user {profile.user_id}")
            return personalized_task
            
        except Exception as e:
            self.logger.error(f"Error personalizing task: {e}")
            return task  # 返回原任务
    
    async def _simplify_task(self, task: CognitiveTask) -> CognitiveTask:
        """
        简化任务（适合注意力较短的用户）
        """
        # 这里实现任务简化逻辑
        simplified_content = self._break_down_complex_content(task.content)
        task.content = simplified_content
        task.metadata["simplified"] = True
        return task
    
    def _break_down_complex_content(self, content: str) -> str:
        """
        拆分复杂内容
        """
        # 简化的拆分逻辑
        sentences = content.split('。')
        if len(sentences) > 3:
            # 限制句子数量
            return '。'.join(sentences[:3]) + '。'
        return content
    
    async def _enrich_task(self, task: CognitiveTask) -> CognitiveTask:
        """
        丰富任务（适合注意力较长的用户）
        """
        # 增加更多上下文信息
        task.metadata["enriched"] = True
        return task
    
    async def _simplify_task_details(self, task: CognitiveTask) -> CognitiveTask:
        """
        简化任务细节（适合处理速度较慢的用户）
        """
        task.metadata["simplified_details"] = True
        return task
    
    async def _add_task_details(self, task: CognitiveTask) -> CognitiveTask:
        """
        増加任务细节（适合处理速度较快的用户）
        """
        task.metadata["detailed"] = True
        return task
    
    async def _reduce_memory_load(self, task: CognitiveTask) -> CognitiveTask:
        """
        减少记忆负载（适合工作记忆较弱的用户）
        """
        task.metadata["low_memory_load"] = True
        return task
    
    async def _add_contextual_info(self, task: CognitiveTask) -> CognitiveTask:
        """
        増加上下文信息（适合长期记忆强的用户）
        """
        task.metadata["contextual_enriched"] = True
        return task
    
    async def update_cognitive_profile(self, user_id: str, interaction_data: Dict[str, Any]) -> CognitiveProfile:
        """
        更新认知画像
        """
        try:
            # 获取现有画像或创建新的
            current_profile = await self._get_or_create_profile(user_id)
            
            # 更新推理风格
            if "reasoning_style" in interaction_data:
                current_profile.reasoning_style = interaction_data["reasoning_style"]
            
            # 更新决策风格
            if "decision_making" in interaction_data:
                current_profile.decision_making = interaction_data["decision_making"]
            
            # 更新学习偏好
            if "learning_preference" in interaction_data:
                current_profile.learning_preference = interaction_data["learning_preference"]
            
            # 更新注意力跨度
            if "attention_span" in interaction_data:
                current_profile.attention_span = interaction_data["attention_span"]
            
            # 更新处理速度
            if "processing_speed" in interaction_data:
                current_profile.processing_speed = interaction_data["processing_speed"]
            
            # 更新记忆强度
            if "memory_strength" in interaction_data:
                current_profile.memory_strength = interaction_data["memory_strength"]
            
            # 更新偏见倾向
            if "bias_feedback" in interaction_data:
                for bias_type, bias_level in interaction_data["bias_feedback"].items():
                    current_profile.bias_tendencies[bias_type] = bias_level
            
            # 更新性能历史
            if "performance_data" in interaction_data:
                current_profile.performance_history.append(interaction_data["performance_data"])
            
            # 限制性能历史长度
            if len(current_profile.performance_history) > 100:
                current_profile.performance_history = current_profile.performance_history[-50:]
            
            # 更新时间戳
            current_profile.last_updated = datetime.now()
            
            # 存储交互历史
            await self._store_interaction_history(user_id, interaction_data)
            
            # 更新个性化模型
            await self._update_personalization_model(user_id, current_profile, interaction_data)
            
            self.logger.info(f"Cognitive profile updated for user: {user_id}")
            return current_profile
            
        except Exception as e:
            self.logger.error(f"Error updating cognitive profile for user {user_id}: {e}")
            raise
    
    async def _get_or_create_profile(self, user_id: str) -> CognitiveProfile:
        """
        获取或创建用户画像
        """
        # 这里应该是从数据库获取，简化实现
        if not hasattr(self, '_profiles'):
            self._profiles = {}
        
        if user_id in self._profiles:
            return self._profiles[user_id]
        
        # 创建默认画像
        default_profile = CognitiveProfile(
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
        
        self._profiles[user_id] = default_profile
        return default_profile
    
    async def _store_interaction_history(self, user_id: str, interaction_data: Dict[str, Any]):
        """
        存储交互历史
        """
        if user_id not in self.user_interaction_history:
            self.user_interaction_history[user_id] = []
        
        # 添加时间戳
        interaction_data["timestamp"] = datetime.now().isoformat()
        
        # 存储交互数据
        self.user_interaction_history[user_id].append(interaction_data)
        
        # 限制历史长度，应用遗忘因子
        if len(self.user_interaction_history[user_id]) > 100:
            # 保留最近的记录，应用遗忘因子
            recent_history = self.user_interaction_history[user_id][-50:]
            self.user_interaction_history[user_id] = recent_history
    
    async def _update_personalization_model(self, user_id: str, profile: CognitiveProfile, interaction_data: Dict[str, Any]):
        """
        更新个性化模型
        """
        if user_id not in self.personalization_models:
            self.personalization_models[user_id] = {
                "preferences": {},
                "behavioral_patterns": [],
                "adaptation_history": []
            }
        
        model = self.personalization_models[user_id]
        
        # 更新偏好
        if "preferences" in interaction_data:
            for pref_key, pref_value in interaction_data["preferences"].items():
                model["preferences"][pref_key] = pref_value
        
        # 更新行为模式
        if "behavior_pattern" in interaction_data:
            model["behavioral_patterns"].append(interaction_data["behavior_pattern"])
        
        # 限制行为模式数量
        if len(model["behavioral_patterns"]) > 50:
            model["behavioral_patterns"] = model["behavioral_patterns"][-30:]
        
        # 记录适应历史
        adaptation_record = {
            "timestamp": datetime.now().isoformat(),
            "changes": {
                "reasoning_style": profile.reasoning_style,
                "decision_making": profile.decision_making,
                "learning_preference": profile.learning_preference
            },
            "interaction_type": interaction_data.get("type", "general")
        }
        model["adaptation_history"].append(adaptation_record)
        
        # 限制适应历史长度
        if len(model["adaptation_history"]) > 100:
            model["adaptation_history"] = model["adaptation_history"][-50:]
    
    async def get_personalization_insights(self, user_id: str) -> Dict[str, Any]:
        """
        获取个性化洞察
        """
        try:
            insights = {
                "user_id": user_id,
                "profile_summary": await self._get_profile_summary(user_id),
                "behavioral_patterns": await self._get_behavioral_patterns(user_id),
                "adaptation_effectiveness": await self._get_adaptation_effectiveness(user_id),
                "personalization_recommendations": await self._get_recommendations(user_id),
                "generated_at": datetime.now().isoformat()
            }
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Error generating personalization insights for user {user_id}: {e}")
            return {"error": str(e)}
    
    async def _get_profile_summary(self, user_id: str) -> Dict[str, Any]:
        """
        获取画像摘要
        """
        profile = await self._get_or_create_profile(user_id)
        
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
    
    async def _get_behavioral_patterns(self, user_id: str) -> List[Dict[str, Any]]:
        """
        获取行为模式
        """
        if user_id in self.personalization_models:
            return self.personalization_models[user_id]["behavioral_patterns"]
        return []
    
    async def _get_adaptation_effectiveness(self, user_id: str) -> Dict[str, Any]:
        """
        获取适应效果
        """
        if user_id in self.personalization_models:
            model = self.personalization_models[user_id]
            adaptation_history = model["adaptation_history"]
            
            if not adaptation_history:
                return {"effectiveness_score": 0.0, "total_adaptations": 0}
            
            # 计算适应效果（简化计算）
            total_adaptations = len(adaptation_history)
            recent_changes = min(5, total_adaptations)
            
            effectiveness_score = min(0.5 + (recent_changes * 0.1), 1.0)  # 简化计算
            
            return {
                "effectiveness_score": effectiveness_score,
                "total_adaptations": total_adaptations,
                "recent_adaptations": recent_changes,
                "last_adaptation": adaptation_history[-1]["timestamp"] if adaptation_history else None
            }
        
        return {"effectiveness_score": 0.0, "total_adaptations": 0}
    
    async def _get_recommendations(self, user_id: str) -> List[str]:
        """
        获取个性化推荐
        """
        profile = await self._get_or_create_profile(user_id)
        recommendations = []
        
        # 根据推理风格推荐
        if profile.reasoning_style == "analytical":
            recommendations.append("推荐使用结构化分析工具")
        elif profile.reasoning_style == "intuitive":
            recommendations.append("推荐使用创意思维工具")
        else:
            recommendations.append("推荐平衡使用分析和直觉方法")
        
        # 根据注意力跨度推荐
        if profile.attention_span < 15:
            recommendations.append("建议将复杂任务分解为小块")
        elif profile.attention_span > 30:
            recommendations.append("可以处理较长的复杂任务")
        
        # 根据学习偏好推荐
        if profile.learning_preference == "visual":
            recommendations.append("推荐使用图表和视觉化工具")
        elif profile.learning_preference == "auditory":
            recommendations.append("推荐使用语音和听觉辅助")
        elif profile.learning_preference == "kinesthetic":
            recommendations.append("推荐使用互动和实践方式")
        else:
            recommendations.append("推荐多模态学习方式")
        
        return recommendations
    
    async def adapt_task_complexity(self, task: CognitiveTask, profile: CognitiveProfile) -> CognitiveTask:
        """
        根据用户画像调整任务复杂度
        """
        try:
            # 计算基础复杂度
            base_complexity = await self._calculate_task_complexity(task)
            
            # 根据用户能力调整
            user_capability = await self._calculate_user_capability(profile)
            
            # 计算适应系数
            adaptation_factor = user_capability / base_complexity
            
            # 调整任务
            if adaptation_factor < 0.7:
                # 用户能力低于任务要求，简化任务
                task = await self._simplify_task_for_user(task, profile)
            elif adaptation_factor > 1.3:
                # 用户能力高于任务要求，增加挑战
                task = await self._enhance_task_for_user(task, profile)
            
            task.metadata["adaptation_factor"] = adaptation_factor
            task.metadata["user_capability"] = user_capability
            task.metadata["task_complexity"] = base_complexity
            
            return task
            
        except Exception as e:
            self.logger.error(f"Error adapting task complexity: {e}")
            return task
    
    async def _calculate_task_complexity(self, task: CognitiveTask) -> float:
        """
        计算任务复杂度
        """
        # 简化的复杂度计算
        complexity = 0.0
        
        # 内容长度
        content_length = len(task.content)
        complexity += min(content_length / 1000, 0.5)  # 最多0.5的复杂度
        
        # 任务类型
        type_complexity = {
            "analysis": 0.7,
            "synthesis": 0.8,
            "evaluation": 0.6,
            "creation": 0.9,
            "decision": 0.5,
            "general": 0.4
        }
        complexity += type_complexity.get(task.task_type, 0.4)
        
        # 上下文复杂度
        if task.context:
            complexity += min(len(task.context) * 0.1, 0.3)
        
        return min(complexity, 1.0)
    
    async def _calculate_user_capability(self, profile: CognitiveProfile) -> float:
        """
        计算用户能力
        """
        # 基于多个维度计算用户能力
        capability = 0.0
        
        # 推理风格 (分析型=0.8, 直觉型=0.6, 平衡型=0.7)
        reasoning_factors = {
            "analytical": 0.8,
            "intuitive": 0.6,
            "balanced": 0.7
        }
        capability += reasoning_factors.get(profile.reasoning_style, 0.7) * 0.3
        
        # 注意力跨度 (标准化到0-1)
        capability += min(profile.attention_span / 50, 1.0) * 0.2
        
        # 处理速度 (慢=0.6, 正常=0.8, 快=1.0)
        speed_factors = {
            "slow": 0.6,
            "normal": 0.8,
            "fast": 1.0
        }
        capability += speed_factors.get(profile.processing_speed, 0.8) * 0.25
        
        # 记忆强度 (工作记忆=0.7, 长期记忆=0.8, 情节记忆=0.6)
        memory_factors = {
            "working": 0.7,
            "long_term": 0.8,
            "episodic": 0.6
        }
        capability += memory_factors.get(profile.memory_strength, 0.7) * 0.25
        
        return min(capability, 1.0)
    
    async def _simplify_task_for_user(self, task: CognitiveTask, profile: CognitiveProfile) -> CognitiveTask:
        """
        为用户简化任务
        """
        # 根据用户特点简化任务
        task.metadata["simplified_for_user"] = True
        
        # 如果注意力跨度短，分解任务
        if profile.attention_span < 15:
            task.metadata["broken_down"] = True
            # 这里可以实现具体的任务分解逻辑
        
        # 如果处理速度慢，减少信息密度
        if profile.processing_speed == "slow":
            task.metadata["reduced_density"] = True
            # 这里可以实现信息密度降低逻辑
        
        return task
    
    async def _enhance_task_for_user(self, task: CognitiveTask, profile: CognitiveProfile) -> CognitiveTask:
        """
        为用户增强任务
        """
        # 根据用户特点增强任务
        task.metadata["enhanced_for_user"] = True
        
        # 如果注意力跨度长，可以增加更多信息
        if profile.attention_span > 30:
            task.metadata["enriched_content"] = True
            # 这里可以实现内容丰富逻辑
        
        # 如果处理速度快，可以增加复杂度
        if profile.processing_speed == "fast":
            task.metadata["increased_complexity"] = True
            # 这里可以实现复杂度增加逻辑
        
        return task
    
    async def predict_task_performance(self, task: CognitiveTask, profile: CognitiveProfile) -> Dict[str, float]:
        """
        预测任务表现
        """
        try:
            # 计算任务-用户匹配度
            complexity = await self._calculate_task_complexity(task)
            capability = await self._calculate_user_capability(profile)
            
            # 计算匹配度
            match_score = min(capability / complexity, 1.0) if complexity > 0 else 1.0
            
            # 考虑其他因素
            confidence_factors = []
            
            # 推理风格匹配
            if task.task_type in ["analysis", "evaluation"] and profile.reasoning_style == "analytical":
                confidence_factors.append(0.9)
            elif task.task_type in ["creation", "brainstorming"] and profile.reasoning_style == "intuitive":
                confidence_factors.append(0.85)
            else:
                confidence_factors.append(0.7)
            
            # 注意力匹配
            if task.task_type in ["analysis", "detailed_work"] and profile.attention_span >= 25:
                confidence_factors.append(0.85)
            elif profile.attention_span < 15 and "short" in task.metadata.get("duration_hint", ""):
                confidence_factors.append(0.8)
            else:
                confidence_factors.append(0.7)
            
            # 平均置信度
            avg_confidence = sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.7
            
            # 最终预测
            performance_prediction = {
                "success_probability": min(match_score * avg_confidence * 1.2, 1.0),  # 最多1.0
                "completion_time_multiplier": 1.0 / max(capability, 0.1),  # 能力越高，时间越短
                "difficulty_level": complexity,
                "confidence": avg_confidence,
                "recommendations": []
            }
            
            # 生成建议
            if performance_prediction["success_probability"] < 0.6:
                performance_prediction["recommendations"].append("建议分解任务或提供更多指导")
            elif performance_prediction["success_probability"] > 0.85:
                performance_prediction["recommendations"].append("用户有能力处理更具挑战性的任务")
            
            if complexity > capability:
                performance_prediction["recommendations"].append("任务可能过于复杂，建议简化")
            
            return performance_prediction
            
        except Exception as e:
            self.logger.error(f"Error predicting task performance: {e}")
            return {
                "success_probability": 0.5,
                "completion_time_multiplier": 1.0,
                "difficulty_level": 0.5,
                "confidence": 0.5,
                "recommendations": ["无法生成准确预测"]
            }
    
    async def generate_adaptive_feedback(self, result: CognitiveResult, profile: CognitiveProfile) -> str:
        """
        生成自适应反馈
        """
        try:
            feedback_parts = []
            
            # 基于置信度的反馈
            if result.confidence >= 0.8:
                feedback_parts.append("推理过程表现出很高的置信度，结果可信。")
            elif result.confidence >= 0.6:
                feedback_parts.append("推理过程较为可靠，结果基本可信。")
            else:
                feedback_parts.append("推理过程置信度较低，建议进一步验证结果。")
            
            # 基于推理类型的反馈
            if result.reasoning_process:
                reasoning_type = result.reasoning_process.reasoning_strategy
                if reasoning_type == "chain_of_thought":
                    feedback_parts.append("链式思维推理适合逐步分析问题。")
                elif reasoning_type == "tree_of_thoughts":
                    feedback_parts.append("树状思维推理适合探索多种可能性。")
                elif reasoning_type == "react":
                    feedback_parts.append("ReAct推理适合需要行动和观察的场景。")
            
            # 基于用户画像的个性化反馈
            if profile.reasoning_style == "analytical":
                feedback_parts.append("作为分析型思考者，您适合使用结构化方法解决问题。")
            elif profile.reasoning_style == "intuitive":
                feedback_parts.append("作为直觉型思考者，您的快速判断能力值得信赖。")
            else:
                feedback_parts.append("您在分析和直觉之间取得了良好的平衡。")
            
            # 基于检测到的偏见的反馈
            if result.detected_biases:
                bias_types = [bias.type for bias in result.detected_biases]
                feedback_parts.append(f"检测到可能的认知偏见: {', '.join(bias_types)}。建议在决策时考虑这些因素。")
            
            # 基于性能历史的反馈
            if profile.performance_history:
                recent_performance = profile.performance_history[-1] if profile.performance_history else {}
                if recent_performance.get("improvement_suggested"):
                    feedback_parts.append(f"系统建议: {recent_performance['improvement_suggested']}")
            
            return " ".join(feedback_parts)
            
        except Exception as e:
            self.logger.error(f"Error generating adaptive feedback: {e}")
            return "系统反馈：任务已处理，结果可供参考。"


class AdvancedCognitivePersonalizationEngine(CognitivePersonalizationEngine):
    """
    高级认知个性化引擎
    支持更复杂的个性化算法
    """
    def __init__(self):
        super().__init__()
        self.ml_models = {}  # 机器学习模型
        self.context_awareness = True  # 上下文感知
        self.transfer_learning_enabled = True  # 迁移学习启用
    
    async def adapt_to_context(self, task: CognitiveTask, profile: CognitiveProfile, context: Dict[str, Any]) -> CognitiveTask:
        """
        根据上下文进行适应
        """
        try:
            # 分析上下文
            context_analysis = await self._analyze_context(context)
            
            # 根据上下文调整任务
            if context_analysis.get("urgency") == "high":
                # 紧急情况下简化任务
                task = await self._optimize_for_speed(task)
            elif context_analysis.get("distraction_level", 0) > 0.6:
                # 分心环境下增强注意力引导
                task = await self._enhance_attention_guidance(task)
            elif context_analysis.get("stress_level", 0) > 0.7:
                # 高压力下简化决策
                task = await self._simplify_under_stress(task)
            
            # 记录上下文适应
            task.metadata["context_adapted"] = True
            task.metadata["context_analysis"] = context_analysis
            
            return task
            
        except Exception as e:
            self.logger.error(f"Error adapting to context: {e}")
            return task
    
    async def _analyze_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析上下文
        """
        analysis = {
            "urgency": "normal",
            "distraction_level": 0.0,
            "stress_level": 0.0,
            "environment": "neutral",
            "time_pressure": False,
            "cognitive_load": "moderate"
        }
        
        # 分析上下文特征
        if "time_constraint" in context:
            if context["time_constraint"] < 5:  # 5分钟以内
                analysis["urgency"] = "high"
                analysis["time_pressure"] = True
        
        if "distractions" in context:
            analysis["distraction_level"] = min(len(context["distractions"]) * 0.2, 1.0)
        
        if "stress_indicators" in context:
            analysis["stress_level"] = min(len(context["stress_indicators"]) * 0.3, 1.0)
        
        if "environment" in context:
            analysis["environment"] = context["environment"]
        
        return analysis
    
    async def _optimize_for_speed(self, task: CognitiveTask) -> CognitiveTask:
        """
        为速度优化任务
        """
        task.metadata["optimized_for_speed"] = True
        task.metadata["speed_optimization_applied"] = datetime.now().isoformat()
        return task
    
    async def _enhance_attention_guidance(self, task: CognitiveTask) -> CognitiveTask:
        """
        増强注意力引导
        """
        task.metadata["attention_guidance_enhanced"] = True
        task.metadata["focus_support_added"] = True
        return task
    
    async def _simplify_under_stress(self, task: CognitiveTask) -> CognitiveTask:
        """
        在压力下简化任务
        """
        task.metadata["stress_adapted"] = True
        task.metadata["simplified_under_stress"] = True
        return task
    
    async def enable_transfer_learning(self, source_user_id: str, target_user_id: str) -> bool:
        """
        启用用户间的知识迁徙
        """
        try:
            # 获取源用户的画像
            source_profile = await self._get_or_create_profile(source_user_id)
            
            # 获取目标用户的画像
            target_profile = await self._get_or_create_profile(target_user_id)
            
            # 迁移相似特征
            transferable_attributes = [
                "reasoning_style", 
                "learning_preference", 
                "memory_strength"
            ]
            
            for attr in transferable_attributes:
                source_attr = getattr(source_profile, attr)
                target_attr = getattr(target_profile, attr)
                
                # 如果目标用户没有明确设置该属性，使用源用户的值
                if source_attr != target_attr and target_attr in ["analytical", "visual", "working"]:  # 默认值
                    setattr(target_profile, attr, source_attr)
            
            # 更新目标用户画像
            self._profiles[target_user_id] = target_profile
            
            self.logger.info(f"Transfer learning applied from {source_user_id} to {target_user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error enabling transfer learning: {e}")
            return False
    
    async def get_cognitive_insights(self, user_id: str, time_window: int = 30) -> Dict[str, Any]:
        """
        获取认知洞察（包含时间维度）
        """
        try:
            insights = await self.get_personalization_insights(user_id)
            
            # 添加时间维度分析
            time_insights = await self._analyze_time_based_patterns(user_id, time_window)
            insights["time_based_patterns"] = time_insights
            
            # 添加性能趋势
            performance_trends = await self._analyze_performance_trends(user_id)
            insights["performance_trends"] = performance_trends
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Error getting cognitive insights: {e}")
            return {"error": str(e)}
    
    async def _analyze_time_based_patterns(self, user_id: str, days: int) -> Dict[str, Any]:
        """
        分析时间模式
        """
        # 这里实现时间模式分析
        return {
            "peak_performance_times": ["morning", "evening"],  # 示例
            "attention_span_variations": "decreases in evening",
            "learning_efficiency_by_time": "highest in morning"
        }
    
    async def _analyze_performance_trends(self, user_id: str) -> Dict[str, Any]:
        """
        分析性能趋势
        """
        # 这里实现性能趋势分析
        return {
            "improvement_trend": "positive",
            "skill_acquisition_rate": 0.15,  # 每天15%的提升
            "adaptation_speed": "fast"
        }


# 个性化引擎工厂
def create_personalization_engine(engine_type: str = "standard", **kwargs) -> object:
    """
    创建个性化引擎实例
    """
    if engine_type == "standard":
        return CognitivePersonalizationEngine()
    elif engine_type == "advanced":
        return AdvancedCognitivePersonalizationEngine()
    else:
        raise ValueError(f"Unknown personalization engine type: {engine_type}")