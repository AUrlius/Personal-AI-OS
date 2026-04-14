"""
认知系统工具函数库
提供认知系统开发所需的各种工具函数
"""
import asyncio
import logging
import json
import re
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from .interfaces import (
    CognitiveTask, CognitiveResult, ReasoningProcess, ReasoningStep,
    CognitiveProfile, BiasDetectionResult, CognitivePattern
)


def sanitize_input(text: str, max_length: int = 10000) -> str:
    """
    清理输入文本，防止注入攻击
    """
    if not isinstance(text, str):
        return ""
    
    # 限制长度
    if len(text) > max_length:
        text = text[:max_length]
    
    # 移除潜在的恶意内容
    # 移除潜在的代码注入
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    
    # 移除潜在的系统命令
    dangerous_patterns = [
        r'exec\(',
        r'eval\(',
        r'__import__\(',
        r'compile\(',
        r'open\([^)]*\)',
        r'os\.', 
        r'subprocess\.',
        r'sys\.',
        r'import\s+os',
        r'import\s+sys',
        r'import\s+subprocess'
    ]
    
    for pattern in dangerous_patterns:
        text = re.sub(pattern, '[REDACTED]', text, flags=re.IGNORECASE)
    
    return text.strip()


def sanitize_output(output: Any, max_length: int = 5000) -> Any:
    """
    清理输出内容
    """
    if isinstance(output, str):
        if len(output) > max_length:
            output = output[:max_length]
        return output
    elif isinstance(output, dict):
        sanitized = {}
        for key, value in output.items():
            sanitized[key] = sanitize_output(value, max_length)
        return sanitized
    elif isinstance(output, list):
        return [sanitize_output(item, max_length) for item in output]
    else:
        return output


def calculate_similarity(text1: str, text2: str) -> float:
    """
    计算两个文本的相似度
    使用简单的Jaccard相似度
    """
    if not text1 or not text2:
        return 0.0
    
    # 转换为小写并分词
    words1 = set(re.findall(r'[\u4e00-\u9fff\w]+', text1.lower()))
    words2 = set(re.findall(r'[\u4e00-\u9fff\w]+', text2.lower()))
    
    if not words1 and not words2:
        return 1.0
    if not words1 or not words2:
        return 0.0
    
    # 计算Jaccard相似度
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union)


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    从文本中提取关键词
    """
    # 简化的关键词提取
    # 在实际应用中，可以使用TF-IDF或更复杂的NLP技术
    
    # 移除标点符号，保留中英文字符
    words = re.findall(r'[\u4e00-\u9fff\w]+', text.lower())
    
    # 过滤停用词（简化版）
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall', 'this', 'that', 'these', 
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 
        'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their',
        'what', 'where', 'when', 'why', 'how', 'which', 'who', 'whose',
        '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', 
        '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', 
        '看', '好', '自己', '这'
    }
    
    # 过滤停用词和短词
    keywords = [word for word in words if word not in stopwords and len(word) > 1]
    
    # 按频率排序并返回前max_keywords个
    word_freq = {}
    for word in keywords:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_keywords[:max_keywords]]


def normalize_vector(vector: List[float]) -> List[float]:
    """
    向量归一化
    """
    if not vector:
        return []
    
    # 计算向量的模长
    magnitude = sum(x * x for x in vector) ** 0.5
    
    # 避免除零错误
    if magnitude == 0:
        return [0.0] * len(vector)
    
    # 归一化
    return [x / magnitude for x in vector]


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    计算余弦相似度
    """
    if len(vec1) != len(vec2):
        return 0.0
    
    if not vec1 or not vec2:
        return 0.0
    
    # 计算点积
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    
    # 计算向量模长
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5
    
    # 避免除零错误
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    # 计算余弦相似度
    similarity = dot_product / (magnitude1 * magnitude2)
    
    # 确保结果在[-1, 1]范围内
    return max(-1.0, min(1.0, similarity))


def semantic_search(query_vector: List[float], 
                   document_vectors: List[List[float]], 
                   top_k: int = 5) -> List[Tuple[int, float]]:
    """
    语义搜索
    """
    similarities = []
    
    for i, doc_vector in enumerate(document_vectors):
        sim = cosine_similarity(query_vector, doc_vector)
        similarities.append((i, sim))
    
    # 按相似度排序
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # 返回前top_k个结果
    return similarities[:top_k]


def calculate_entropy(probabilities: List[float]) -> float:
    """
    计算熵值
    """
    entropy = 0.0
    for p in probabilities:
        if p > 0:  # 避免log(0)
            entropy -= p * np.log2(p)
    return entropy


def calculate_confidence_interval(success_count: int, total_count: int, confidence_level: float = 0.95) -> Tuple[float, float]:
    """
    计算置信区间 (Wilson Score Interval)
    """
    if total_count == 0:
        return (0.0, 0.0)
    
    z = {
        0.90: 1.645,
        0.95: 1.96,
        0.99: 2.576
    }.get(confidence_level, 1.96)
    
    p = success_count / total_count
    n = total_count
    
    # Wilson Score Interval
    denominator = 1 + z * z / n
    centre_adjusted_probability = (p + z * z / (2 * n)) / denominator
    adjusted_standard_deviation = np.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / denominator
    
    lower_bound = centre_adjusted_probability - z * adjusted_standard_deviation
    upper_bound = centre_adjusted_probability + z * adjusted_standard_deviation
    
    return (lower_bound, upper_bound)


def detect_potential_bias(text: str, bias_keywords: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    """
    检测文本中的潜在偏见
    """
    detected_biases = []
    
    text_lower = text.lower()
    
    for bias_type, keywords in bias_keywords.items():
        found_keywords = []
        for keyword in keywords:
            if keyword.lower() in text_lower:
                found_keywords.append(keyword)
        
        if found_keywords:
            detected_biases.append({
                "type": bias_type,
                "severity": len(found_keywords) / len(keywords),  # 基于匹配关键词比例
                "evidence": found_keywords,
                "confidence": min(len(found_keywords) * 0.3, 1.0)  # 简化的置信度计算
            })
    
    return detected_biases


def extract_structured_data(text: str) -> Dict[str, Any]:
    """
    从文本中提取结构化数据
    """
    structured_data = {
        "numbers": re.findall(r'\d+\.?\d*', text),
        "dates": re.findall(r'\d{4}-\d{2}-\d{2}|\d{4}/\d{2}/\d{2}|\d{2}/\d{2}/\d{4}', text),
        "emails": re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text),
        "urls": re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text),
        "phones": re.findall(r'\b\d{3}-?\d{3}-?\d{4}\b', text),
        "organizations": [],  # 需要NLP模型才能准确识别
        "people": [],  # 需要NLP模型才能准确识别
        "locations": []  # 需要NLP模型才能准确识别
    }
    
    return structured_data


def validate_cognitive_task(task: CognitiveTask) -> Tuple[bool, List[str]]:
    """
    验证认知任务的有效性
    """
    errors = []
    
    if not task.id:
        errors.append("Task ID is required")
    
    if not task.content:
        errors.append("Task content is required")
    
    if len(task.content) > 10000:  # 限制内容长度
        errors.append("Task content exceeds maximum length (10000 characters)")
    
    if task.priority not in ["low", "normal", "high", "critical"]:
        errors.append("Invalid priority level")
    
    if task.task_type not in ["analysis", "synthesis", "evaluation", "creation", "decision", "general"]:
        errors.append("Invalid task type")
    
    if task.complexity not in ["simple", "moderate", "complex", "very_complex"]:
        errors.append("Invalid complexity level")
    
    return len(errors) == 0, errors


def format_reasoning_process(process: ReasoningProcess, format_type: str = "detailed") -> str:
    """
    格式化推理过程
    """
    if format_type == "brief":
        return f"Conclusion: {process.conclusion} (Confidence: {process.confidence:.2f})"
    elif format_type == "steps_only":
        return "\n".join([f"Step {step.step_number}: {step.content}" for step in process.steps])
    else:  # detailed
        formatted = f"Input Problem: {process.input_problem}\n"
        formatted += f"Conclusion: {process.conclusion}\n"
        formatted += f"Confidence: {process.confidence:.2f}\n"
        formatted += f"Reasoning Strategy: {process.reasoning_strategy}\n"
        formatted += "Steps:\n"
        for step in process.steps:
            formatted += f"  {step.step_number}. {step.content}\n"
            formatted += f"     Type: {step.reasoning_type}, Confidence: {step.confidence:.2f}\n"
        
        if process.bias_indicators:
            formatted += f"Bias Indicators: {len(process.bias_indicators)} detected\n"
        
        return formatted


def analyze_reasoning_quality(process: ReasoningProcess) -> Dict[str, float]:
    """
    分析推理质量
    """
    if not process.steps:
        return {
            "coherence": 0.0,
            "completeness": 0.0,
            "logical_flow": 0.0,
            "evidence_support": 0.0,
            "overall_quality": 0.0
        }
    
    # 计算连贯性（基于步骤间的逻辑关系）
    coherence = calculate_reasoning_coherence(process.steps)
    
    # 计算完整性（基于是否覆盖了问题的关键方面）
    completeness = calculate_reasoning_completeness(process.input_problem, process.steps)
    
    # 计算逻辑流（基于推理类型的多样性）
    logical_flow = calculate_logical_flow(process.steps)
    
    # 计算证据支持度（基于步骤中的证据引用）
    evidence_support = calculate_evidence_support(process.steps)
    
    # 综合质量评分
    overall_quality = (
        coherence * 0.3 +
        completeness * 0.25 +
        logical_flow * 0.25 +
        evidence_support * 0.2
    )
    
    return {
        "coherence": coherence,
        "completeness": completeness,
        "logical_flow": logical_flow,
        "evidence_support": evidence_support,
        "overall_quality": overall_quality
    }


def calculate_reasoning_coherence(steps: List[ReasoningStep]) -> float:
    """
    计算推理连贯性
    """
    if len(steps) < 2:
        return 0.8  # 单一步骤假设有一定连贯性
    
    coherent_transitions = 0
    total_transitions = len(steps) - 1
    
    for i in range(total_transitions):
        current_step = steps[i]
        next_step = steps[i + 1]
        
        # 检查步骤间是否有逻辑连接
        # 这里使用简化的连接词检测
        next_content_lower = next_step.content.lower()
        has_connectors = any(conn in next_content_lower for conn in 
                           ["因此", "所以", "然而", "但是", "此外", "接着", "然后", "综上"])
        
        # 检查内容相关性（基于关键词重叠）
        current_keywords = set(extract_keywords(current_step.content, max_keywords=5))
        next_keywords = set(extract_keywords(next_step.content, max_keywords=5))
        content_overlap = len(current_keywords.intersection(next_keywords))
        
        # 如果有连接词或内容重叠，则认为是连贯的
        if has_connectors or content_overlap > 0:
            coherent_transitions += 1
    
    return coherent_transitions / total_transitions if total_transitions > 0 else 0.8


def calculate_reasoning_completeness(problem: str, steps: List[ReasoningStep]) -> float:
    """
    计算推理完整性
    """
    if not steps:
        return 0.0
    
    # 提取问题的关键要素
    problem_keywords = set(extract_keywords(problem, max_keywords=10))
    
    # 提取推理步骤中涉及的要素
    covered_keywords = set()
    for step in steps:
        step_keywords = set(extract_keywords(step.content, max_keywords=10))
        covered_keywords.update(step_keywords)
    
    # 计算覆盖比例
    if not problem_keywords:
        return 0.7  # 如果问题中没有可提取的关键词，假设中等完整性
    
    covered_count = len(problem_keywords.intersection(covered_keywords))
    total_count = len(problem_keywords)
    
    return min(covered_count / total_count, 1.0)


def calculate_logical_flow(steps: List[ReasoningStep]) -> float:
    """
    计算逻辑流
    """
    if not steps:
        return 0.5
    
    # 计算推理类型的多样性
    reasoning_types = [step.reasoning_type for step in steps]
    unique_types = len(set(reasoning_types))
    total_steps = len(steps)
    
    # 多样性评分（鼓励使用不同类型的推理）
    diversity_score = unique_types / min(total_steps, 5)  # 限制最大多样性为1.0
    
    # 流畅性评分（基于推理类型的合理组合）
    flow_score = calculate_reasoning_flow_score(reasoning_types)
    
    # 综合评分
    return (diversity_score * 0.4) + (flow_score * 0.6)


def calculate_reasoning_flow_score(reasoning_types: List[str]) -> float:
    """
    计算推理流评分
    """
    if len(reasoning_types) < 2:
        return 0.7
    
    # 定义合理的推理类型转换
    reasonable_transitions = {
        ("comprehension", "analytical"),
        ("analytical", "generative"), 
        ("analytical", "verificational"),
        ("generative", "verificational"),
        ("verificational", "synthetic"),
        ("synthetic", "conclusive")
    }
    
    valid_transitions = 0
    total_transitions = len(reasoning_types) - 1
    
    for i in range(total_transitions):
        transition = (reasoning_types[i], reasoning_types[i+1])
        if transition in reasonable_transitions or transition[0] == transition[1]:  # 相同类型也算合理
            valid_transitions += 1
    
    return valid_transitions / total_transitions if total_transitions > 0 else 0.7


def calculate_evidence_support(steps: List[ReasoningStep]) -> float:
    """
    计算证据支持度
    """
    if not steps:
        return 0.3
    
    total_steps = len(steps)
    steps_with_evidence = 0
    
    for step in steps:
        # 检查步骤是否有支持证据
        if step.supporting_evidence and len(step.supporting_evidence) > 0:
            steps_with_evidence += 1
        # 或者检查内容中是否包含证据相关的词汇
        elif any(word in step.content.lower() for word in ["因为", "由于", "基于", "根据", "证据", "证明", "显示", "表明"]):
            steps_with_evidence += 1
    
    return steps_with_evidence / total_steps


def detect_reasoning_biases(process: ReasoningProcess) -> List[BiasDetectionResult]:
    """
    检测推理过程中的偏见
    """
    detected_biases = []
    
    # 检查确认偏见：只考虑支持初始观点的证据
    confirmation_indicators = []
    for step in process.steps:
        content_lower = step.content.lower()
        if any(indicator in content_lower for indicator in ["显然", "明显", "当然", "毫无疑问", "肯定"]):
            confirmation_indicators.append(step.content[:50] + "...")
    
    if len(confirmation_indicators) > len(process.steps) * 0.5:  # 超过一半的步骤有确认迹象
        detected_biases.append(BiasDetectionResult(
            type="confirmation",
            severity=min(len(confirmation_indicators) / len(process.steps), 1.0),
            evidence=confirmation_indicators,
            suggestion="Consider actively seeking contradictory evidence and alternative viewpoints.",
            confidence=0.8
        ))
    
    # 检查锚定偏见：过度依赖初始信息
    if process.steps and len(process.steps) > 2:
        initial_content = process.steps[0].content.lower()
        if any(anchor_word in initial_content for anchor_word in ["首先", "一开始", "最初的", "初始", "起始"]):
            # 检查后续步骤是否过度引用初始信息
            anchor_refs = 0
            for step in process.steps[1:]:
                if any(anchor_word in step.content.lower() for anchor_word in ["上述", "前面", "初始", "首先"]):
                    anchor_refs += 1
            
            if anchor_refs > len(process.steps) * 0.6:  # 超过60%的步骤引用初始信息
                detected_biases.append(BiasDetectionResult(
                    type="anchoring",
                    severity=0.7,
                    evidence=[f"Found {anchor_refs} references to initial information out of {len(process.steps)-1} subsequent steps"],
                    suggestion="Consider whether initial information unduly influenced your judgment. Adjust estimates based on additional information.",
                    confidence=0.75
                ))
    
    # 检查可得性偏见：依赖容易回忆的信息
    availability_indicators = []
    for step in process.steps:
        content_lower = step.content.lower()
        if any(indicator in content_lower for indicator in ["我记得", "最近", "刚刚", "上次", "以前"]):
            availability_indicators.append(step.content[:50] + "...")
    
    if len(availability_indicators) > len(process.steps) * 0.3:  # 超过30%的步骤提及过去事件
        detected_biases.append(BiasDetectionResult(
            type="availability",
            severity=min(len(availability_indicators) / len(process.steps) * 1.5, 1.0),  # 提高权重
            evidence=availability_indicators,
            suggestion="Seek out less memorable but potentially more relevant information to balance your judgment.",
            confidence=0.65
        ))
    
    return detected_biases


def generate_cognitive_insights(profile: CognitiveProfile, recent_tasks: List[CognitiveResult]) -> Dict[str, Any]:
    """
    生成认知洞察
    """
    insights = {
        "reasoning_patterns": analyze_reasoning_patterns(recent_tasks),
        "bias_tendencies": analyze_bias_tendencies(profile, recent_tasks),
        "performance_trends": analyze_performance_trends(recent_tasks),
        "strengths": identify_strengths(profile, recent_tasks),
        "improvement_areas": identify_improvement_areas(profile, recent_tasks),
        "recommendations": generate_recommendations(profile, recent_tasks)
    }
    
    return insights


def analyze_reasoning_patterns(tasks: List[CognitiveResult]) -> Dict[str, Any]:
    """
    分析推理模式
    """
    if not tasks:
        return {"message": "No tasks to analyze"}
    
    # 统计推理策略使用情况
    strategy_counts = {}
    confidence_scores = []
    
    for task in tasks:
        if task.reasoning_process:
            strategy = task.reasoning_process.reasoning_strategy
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
            confidence_scores.append(task.reasoning_process.confidence)
    
    avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
    
    return {
        "most_used_strategies": sorted(strategy_counts.items(), key=lambda x: x[1], reverse=True),
        "average_confidence": avg_confidence,
        "strategy_effectiveness": calculate_strategy_effectiveness(tasks)
    }


def calculate_strategy_effectiveness(tasks: List[CognitiveResult]) -> Dict[str, float]:
    """
    计算策略有效性
    """
    strategy_performance = {}
    
    for task in tasks:
        if task.reasoning_process:
            strategy = task.reasoning_process.reasoning_strategy
            if strategy not in strategy_performance:
                strategy_performance[strategy] = {"total": 0, "success": 0}
            
            strategy_performance[strategy]["total"] += 1
            if task.success:
                strategy_performance[strategy]["success"] += 1
    
    effectiveness = {}
    for strategy, data in strategy_performance.items():
        effectiveness[strategy] = data["success"] / data["total"] if data["total"] > 0 else 0.0
    
    return effectiveness


def analyze_bias_tendencies(profile: CognitiveProfile, tasks: List[CognitiveResult]) -> Dict[str, float]:
    """
    分析偏见倾向
    """
    # 合并画像中的偏见倾向和任务中检测到的偏见
    bias_tendencies = dict(profile.bias_tendencies) if profile.bias_tendencies else {}
    
    # 从任务中提取偏见信息
    for task in tasks:
        for bias in task.detected_biases:
            bias_type = bias.type
            severity = bias.severity
            if bias_type in bias_tendencies:
                # 更新偏见倾向（考虑新旧信息的权重）
                bias_tendencies[bias_type] = (bias_tendencies[bias_type] * 0.7 + severity * 0.3)
            else:
                bias_tendencies[bias_type] = severity
    
    return bias_tendencies


def analyze_performance_trends(tasks: List[CognitiveResult]) -> Dict[str, Any]:
    """
    分析性能趋势
    """
    if not tasks:
        return {"message": "No tasks to analyze"}
    
    # 按时间排序任务
    sorted_tasks = sorted(tasks, key=lambda x: x.timestamp if hasattr(x, 'timestamp') else datetime.now())
    
    # 计算性能指标随时间的变化
    confidences = [task.confidence for task in sorted_tasks if task.confidence is not None]
    success_rates = [1.0 if task.success else 0.0 for task in sorted_tasks]
    
    # 计算趋势
    if len(confidences) >= 2:
        # 简单的趋势分析
        early_confidence = np.mean(confidences[:max(1, len(confidences)//2)])
        late_confidence = np.mean(confidences[max(0, len(confidences)//2):])
        confidence_trend = "improving" if late_confidence > early_confidence + 0.05 else \
                          "declining" if late_confidence < early_confidence - 0.05 else "stable"
    else:
        confidence_trend = "insufficient_data"
    
    if len(success_rates) >= 2:
        early_success = np.mean(success_rates[:max(1, len(success_rates)//2)])
        late_success = np.mean(success_rates[max(0, len(success_rates)//2):])
        success_trend = "improving" if late_success > early_success + 0.05 else \
                       "declining" if late_success < early_success - 0.05 else "stable"
    else:
        success_trend = "insufficient_data"
    
    return {
        "confidence_trend": confidence_trend,
        "success_trend": success_trend,
        "recent_average_confidence": np.mean(confidences[-5:]) if confidences else 0.0,
        "recent_success_rate": np.mean(success_rates[-5:]) if success_rates else 0.0
    }


def identify_strengths(profile: CognitiveProfile, tasks: List[CognitiveResult]) -> List[str]:
    """
    识别优势
    """
    strengths = []
    
    # 基于画像的推理风格
    if profile.reasoning_style == "analytical":
        strengths.append("Strong analytical reasoning skills")
    elif profile.reasoning_style == "creative":
        strengths.append("Creative and innovative thinking")
    elif profile.reasoning_style == "balanced":
        strengths.append("Balanced analytical and intuitive thinking")
    
    # 基于任务表现
    if tasks:
        avg_confidence = np.mean([t.confidence for t in tasks if t.confidence is not None])
        if avg_confidence > 0.8:
            strengths.append("High confidence in reasoning processes")
        
        success_rate = len([t for t in tasks if t.success]) / len(tasks)
        if success_rate > 0.8:
            strengths.append("High task completion success rate")
    
    return strengths


def identify_improvement_areas(profile: CognitiveProfile, tasks: List[CognitiveResult]) -> List[str]:
    """
    识别改进领域
    """
    improvement_areas = []
    
    # 基于偏见倾向
    if profile.bias_tendencies:
        highest_bias = max(profile.bias_tendencies.items(), key=lambda x: x[1])
        if highest_bias[1] > 0.6:
            improvement_areas.append(f"Address {highest_bias[0]} bias (severity: {highest_bias[1]:.2f})")
    
    # 基于任务表现
    if tasks:
        avg_confidence = np.mean([t.confidence for t in tasks if t.confidence is not None])
        if avg_confidence < 0.6:
            improvement_areas.append("Work on building confidence in reasoning processes")
        
        success_rate = len([t for t in tasks if t.success]) / len(tasks)
        if success_rate < 0.7:
            improvement_areas.append("Focus on improving task completion success rate")
    
    return improvement_areas


def generate_recommendations(profile: CognitiveProfile, tasks: List[CognitiveResult]) -> List[str]:
    """
    生成建议
    """
    recommendations = []
    
    # 基于推理风格的建议
    if profile.reasoning_style == "intuitive":
        recommendations.append("Consider using more analytical approaches for complex problems")
    elif profile.reasoning_style == "analytical":
        recommendations.append("Try incorporating more intuitive insights for creative solutions")
    
    # 基于偏见倾向的建议
    if profile.bias_tendencies:
        for bias_type, severity in profile.bias_tendencies.items():
            if severity > 0.5:
                if bias_type == "confirmation":
                    recommendations.append("Actively seek out contradictory evidence and alternative viewpoints")
                elif bias_type == "anchoring":
                    recommendations.append("Be cautious of initial impressions and consider multiple reference points")
                elif bias_type == "availability":
                    recommendations.append("Look for less memorable but potentially more relevant information")
    
    # 基于任务表现的建议
    if tasks:
        recent_tasks = tasks[-5:]  # 最近5个任务
        low_confidence_tasks = [t for t in recent_tasks if t.confidence and t.confidence < 0.6]
        if len(low_confidence_tasks) > len(recent_tasks) * 0.5:  # 超过一半的任务置信度低
            recommendations.append("Practice building stronger justification for conclusions")
    
    if not recommendations:
        recommendations.append("Continue current approach - performance is generally strong")
    
    return recommendations


def create_cognitive_pattern_matcher():
    """
    创建认知模式匹配器
    """
    class CognitivePatternMatcher:
        def __init__(self):
            self.patterns = []
        
        def add_pattern(self, pattern: CognitivePattern):
            """添加认知模式"""
            self.patterns.append(pattern)
        
        def match_patterns(self, input_text: str, threshold: float = 0.7) -> List[Tuple[CognitivePattern, float]]:
            """匹配认知模式"""
            matches = []
            
            for pattern in self.patterns:
                similarity = self._calculate_pattern_similarity(input_text, pattern)
                if similarity >= threshold:
                    matches.append((pattern, similarity))
            
            # 按相似度排序
            matches.sort(key=lambda x: x[1], reverse=True)
            return matches
        
        def _calculate_pattern_similarity(self, text: str, pattern: CognitivePattern) -> float:
            """计算文本与模式的相似度"""
            # 基于关键词匹配的简化相似度计算
            text_keywords = set(extract_keywords(text, max_keywords=20))
            pattern_keywords = set(pattern.triggers) if hasattr(pattern, 'triggers') else set()
            
            if not text_keywords and not pattern_keywords:
                return 1.0
            if not text_keywords or not pattern_keywords:
                return 0.0
            
            intersection = text_keywords.intersection(pattern_keywords)
            union = text_keywords.union(pattern_keywords)
            
            return len(intersection) / len(union)  # Jaccard相似度
    
    return CognitivePatternMatcher()


def calculate_cognitive_load(text: str) -> float:
    """
    计算认知负荷
    基于文本复杂度的简化计算
    """
    # 计算句子长度（平均）
    sentences = re.split(r'[.!?。！？]', text)
    avg_sentence_length = np.mean([len(s.split()) for s in sentences if s.strip()])
    
    # 计算词汇复杂度（长词比例）
    words = re.findall(r'\w+', text)
    long_words = [w for w in words if len(w) > 8]  # 中文词可能较短，这里主要针对英文
    complexity_ratio = len(long_words) / len(words) if words else 0
    
    # 计算句法复杂度（从句数量）
    subordinate_clauses = len(re.findall(r'如果|当|虽然|因为|所以|但是', text))
    clause_density = subordinate_clauses / len(sentences) if sentences else 0
    
    # 综合认知负荷
    cognitive_load = (
        min(avg_sentence_length / 30, 1.0) * 0.4 +  # 句子长度影响
        complexity_ratio * 0.3 +  # 词汇复杂度影响
        min(clause_density * 5, 1.0) * 0.3  # 句法复杂度影响
    )
    
    return min(cognitive_load, 1.0)


def detect_emotional_tone(text: str) -> Dict[str, float]:
    """
    检测情感语调
    """
    # 简化的积极/消极词典
    positive_words = {
        'good', 'great', 'excellent', 'wonderful', 'fantastic', 'amazing', 'perfect', 
        'love', 'like', 'enjoy', 'happy', 'positive', 'beneficial', 'advantage',
        '好', '棒', '优秀', '完美', '喜欢', '开心', '积极', '有益'
    }
    
    negative_words = {
        'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'sad', 
        'negative', 'problem', 'issue', 'difficult', 'hard', 'challenging',
        '不好', '糟糕', '讨厌', '难过', '消极', '问题', '困难'
    }
    
    words = [w.lower() for w in re.findall(r'[\u4e00-\u9fff\w]+', text)]
    
    positive_count = sum(1 for w in words if w in positive_words)
    negative_count = sum(1 for w in words if w in negative_words)
    total_meaningful_words = len([w for w in words if w in positive_words or w in negative_words])
    
    return {
        "positive": positive_count / total_meaningful_words if total_meaningful_words > 0 else 0.0,
        "negative": negative_count / total_meaningful_words if total_meaningful_words > 0 else 0.0,
        "neutral": 1.0 - (positive_count + negative_count) / total_meaningful_words if total_meaningful_words > 0 else 1.0
    }


def extract_thinking_trace(process: ReasoningProcess) -> List[Dict[str, Any]]:
    """
    提取思维轨迹
    """
    trace = []
    
    for step in process.steps:
        trace.append({
            "step_number": step.step_number,
            "content": step.content,
            "reasoning_type": step.reasoning_type,
            "confidence": step.confidence,
            "timestamp": step.timestamp.isoformat() if hasattr(step, 'timestamp') and step.timestamp else None,
            "supporting_evidence": step.supporting_evidence if hasattr(step, 'supporting_evidence') else [],
            "alternatives_considered": step.alternatives_considered if hasattr(step, 'alternatives_considered') else []
        })
    
    return trace


def calculate_metacognitive_awareness(process: ReasoningProcess) -> float:
    """
    计算元认知意识
    检测推理过程中对自身认知过程的反思
    """
    if not process.steps:
        return 0.2  # 默认较低的元认知意识
    
    metacognitive_indicators = 0
    total_indicators = len(process.steps)
    
    for step in process.steps:
        content_lower = step.content.lower()
        
        # 检查元认知指示词
        metacognitive_terms = [
            "我认为", "我觉得", "我意识到", "我注意到", "我思考", "我反思",
            "我质疑", "我怀疑", "我确认", "我验证", "我检查", "我评估",
            "我分析我的", "我考虑我的", "我重新评估", "我调整我的",
            "可能不对", "也许我错了", "让我重新考虑", "需要验证"
        ]
        
        if any(term in content_lower for term in metacognitive_terms):
            metacognitive_indicators += 1
    
    return min(metacognitive_indicators / max(total_indicators, 1) * 2, 1.0)  # 最多2倍权重，但不超过1.0


def generate_learning_insights(tasks: List[CognitiveResult]) -> Dict[str, Any]:
    """
    生成学习洞察
    """
    if not tasks:
        return {"message": "No tasks to analyze for learning insights"}
    
    # 分析学习模式
    learning_insights = {
        "learning_speed": calculate_learning_speed(tasks),
        "improvement_areas": identify_improvement_areas_from_tasks(tasks),
        "successful_strategies": identify_successful_strategies(tasks),
        "growth_trajectory": calculate_growth_trajectory(tasks)
    }
    
    return learning_insights


def calculate_learning_speed(tasks: List[CognitiveResult]) -> str:
    """
    计算学习速度
    """
    if len(tasks) < 3:
        return "insufficient_data"
    
    # 按时间排序
    sorted_tasks = sorted(tasks, key=lambda x: x.timestamp if hasattr(x, 'timestamp') else datetime.now())
    
    # 计算最近和最早任务的表现差异
    early_tasks = sorted_tasks[:len(sorted_tasks)//3]
    recent_tasks = sorted_tasks[-len(sorted_tasks)//3:]
    
    early_performance = np.mean([t.confidence for t in early_tasks if t.confidence is not None])
    recent_performance = np.mean([t.confidence for t in recent_tasks if t.confidence is not None])
    
    if recent_performance > early_performance + 0.1:
        return "fast_learner"
    elif recent_performance > early_performance + 0.05:
        return "moderate_learner"
    else:
        return "needs_support"


def identify_improvement_areas_from_tasks(tasks: List[CognitiveResult]) -> List[str]:
    """
    从任务中识别改进领域
    """
    if not tasks:
        return []
    
    # 分析失败任务的原因
    failed_tasks = [t for t in tasks if not t.success]
    low_confidence_tasks = [t for t in tasks if t.confidence and t.confidence < 0.6]
    
    improvement_areas = []
    
    if len(failed_tasks) / len(tasks) > 0.3:
        improvement_areas.append("Focus on improving task completion success rate")
    
    if len(low_confidence_tasks) / len(tasks) > 0.4:
        improvement_areas.append("Work on building confidence in reasoning processes")
    
    # 分析推理质量问题
    quality_issues = []
    for task in tasks:
        if task.reasoning_process:
            quality_analysis = analyze_reasoning_quality(task.reasoning_process)
            if quality_analysis["overall_quality"] < 0.6:
                quality_issues.append(quality_analysis)
    
    if quality_issues:
        avg_quality = {k: np.mean([q[k] for q in quality_issues]) for k in quality_issues[0].keys()}
        lowest_aspect = min(avg_quality.items(), key=lambda x: x[1])
        improvement_areas.append(f"Improve {lowest_aspect[0]} (currently {lowest_aspect[1]:.2f})")
    
    return improvement_areas


def identify_successful_strategies(tasks: List[CognitiveResult]) -> List[str]:
    """
    识别成功的策略
    """
    successful_strategies = []
    
    # 分析成功任务的策略
    successful_tasks = [t for t in tasks if t.success and t.reasoning_process]
    
    if successful_tasks:
        strategy_success_rates = {}
        
        for task in successful_tasks:
            if task.reasoning_process:
                strategy = task.reasoning_process.reasoning_strategy
                if strategy not in strategy_success_rates:
                    strategy_success_rates[strategy] = {"total": 0, "success": 0}
                strategy_success_rates[strategy]["total"] += 1
                if task.success:
                    strategy_success_rates[strategy]["success"] += 1
        
        for strategy, data in strategy_success_rates.items():
            success_rate = data["success"] / data["total"] if data["total"] > 0 else 0
            if success_rate > 0.8:  # 高成功率策略
                successful_strategies.append(f"{strategy} (success rate: {success_rate:.2f})")
    
    return successful_strategies


def calculate_growth_trajectory(tasks: List[CognitiveResult]) -> Dict[str, float]:
    """
    计算成长轨迹
    """
    if not tasks:
        return {"slope": 0.0, "significance": 0.0, "trend": "neutral"}
    
    # 按时间排序
    sorted_tasks = sorted(tasks, key=lambda x: x.timestamp if hasattr(x, 'timestamp') else datetime.now())
    
    # 提取时间和表现分数
    times = []
    performances = []
    
    for i, task in enumerate(sorted_tasks):
        if task.confidence is not None:
            times.append(i)  # 使用索引作为时间点
            performances.append(task.confidence)
    
    if len(performances) < 2:
        return {"slope": 0.0, "significance": 0.0, "trend": "insufficient_data"}
    
    # 计算趋势线
    slope = np.polyfit(times, performances, 1)[0] if len(times) > 1 else 0.0
    
    # 计算显著性（简化版）
    from scipy import stats
    if len(times) >= 3:
        _, _, r_value, p_value, _ = stats.linregress(times, performances)
        significance = 1 - p_value  # 简化的显著性计算
    else:
        significance = 0.0
    
    # 确定趋势
    if slope > 0.05:
        trend = "improving"
    elif slope < -0.05:
        trend = "declining"
    else:
        trend = "stable"
    
    return {
        "slope": float(slope),
        "significance": float(significance),
        "trend": trend
    }


# 实用工具类
class CognitiveUtils:
    """
    认知工具类
    """
    @staticmethod
    def batch_process_tasks(tasks: List[CognitiveTask], processor_func) -> List[CognitiveResult]:
        """
        批量处理任务
        """
        results = []
        for task in tasks:
            try:
                result = processor_func(task)
                results.append(result)
            except Exception as e:
                results.append(CognitiveResult(
                    success=False,
                    output=None,
                    reasoning_process=None,
                    detected_biases=[],
                    confidence=0.0,
                    execution_time=0,
                    resources_used={}
                ))
        return results
    
    @staticmethod
    def cache_result(key: str, result: Any, ttl: int = 3600):
        """
        缓存结果
        """
        # 这里应该连接到实际的缓存系统（如Redis）
        # 为简化，使用内存缓存
        if not hasattr(CognitiveUtils, '_cache'):
            CognitiveUtils._cache = {}
            CognitiveUtils._cache_timestamps = {}
        
        import time
        CognitiveUtils._cache[key] = result
        CognitiveUtils._cache_timestamps[key] = time.time() + ttl
    
    @staticmethod
    def get_cached_result(key: str) -> Optional[Any]:
        """
        获取缓存结果
        """
        if not hasattr(CognitiveUtils, '_cache'):
            return None
        
        import time
        if key in CognitiveUtils._cache:
            if time.time() < CognitiveUtils._cache_timestamps.get(key, 0):
                return CognitiveUtils._cache[key]
            else:
                # 清除过期缓存
                del CognitiveUtils._cache[key]
                if key in CognitiveUtils._cache_timestamps:
                    del CognitiveUtils._cache_timestamps[key]
        
        return None
    
    @staticmethod
    def measure_performance(func):
        """
        性能测量装饰器
        """
        def wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            execution_time = end_time - start_time
            
            # 添加性能指标到结果中（如果结果是字典或对象）
            if hasattr(result, 'execution_time'):
                result.execution_time = execution_time
            elif isinstance(result, dict):
                result['execution_time'] = execution_time
            
            return result
        return wrapper


# 工厂函数
def create_cognitive_utils() -> CognitiveUtils:
    """
    创建认知工具实例
    """
    return CognitiveUtils()


def get_cognitive_insights(profile: CognitiveProfile, recent_tasks: List[CognitiveResult]) -> Dict[str, Any]:
    """
    获取认知洞察（便捷函数）
    """
    return generate_cognitive_insights(profile, recent_tasks)


def analyze_task_performance(tasks: List[CognitiveResult]) -> Dict[str, Any]:
    """
    分析任务性能（便捷函数）
    """
    return analyze_performance_trends(tasks)


def detect_cognitive_biases_in_process(process: ReasoningProcess) -> List[BiasDetectionResult]:
    """
    检测推理过程中的偏见（便捷函数）
    """
    return detect_reasoning_biases(process)


def calculate_reasoning_quality(process: ReasoningProcess) -> Dict[str, float]:
    """
    计算推理质量（便捷函数）
    """
    return analyze_reasoning_quality(process)


# 异步工具函数
async def async_batch_process(tasks: List[CognitiveTask], processor_func, max_concurrent: int = 5) -> List[CognitiveResult]:
    """
    异步批量处理任务
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_with_semaphore(task):
        async with semaphore:
            return await processor_func(task)
    
    tasks = [process_with_semaphore(task) for task in tasks]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 处理可能的异常
    processed_results = []
    for result in results:
        if isinstance(result, Exception):
            processed_results.append(CognitiveResult(
                success=False,
                output=None,
                reasoning_process=None,
                detected_biases=[],
                confidence=0.0,
                execution_time=0,
                resources_used={}
            ))
        else:
            processed_results.append(result)
    
    return processed_results


async def async_retry_with_backoff(func, max_retries: int = 3, base_delay: float = 1.0):
    """
    带退避的异步重试
    """
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            delay = base_delay * (2 ** attempt)  # 指数退避
            await asyncio.sleep(delay)
    
    raise Exception("Max retries exceeded")


# 数据验证工具
def validate_cognitive_profile(profile: CognitiveProfile) -> Tuple[bool, List[str]]:
    """
    验证认知画像
    """
    errors = []
    
    if not profile.user_id:
        errors.append("User ID is required")
    
    if profile.reasoning_style not in ["analytical", "intuitive", "balanced", "creative"]:
        errors.append("Invalid reasoning style")
    
    if profile.decision_making not in ["rational", "intuitive", "balanced", "cautious", "risky"]:
        errors.append("Invalid decision making style")
    
    if profile.learning_preference not in ["visual", "auditory", "kinesthetic", "reading", "balanced"]:
        errors.append("Invalid learning preference")
    
    if not (5 <= profile.attention_span <= 60):
        errors.append("Attention span must be between 5 and 60 minutes")
    
    if profile.processing_speed not in ["slow", "normal", "fast"]:
        errors.append("Invalid processing speed")
    
    if profile.memory_strength not in ["weak", "working", "long_term", "strong"]:
        errors.append("Invalid memory strength")
    
    return len(errors) == 0, errors


def validate_reasoning_process(process: ReasoningProcess) -> Tuple[bool, List[str]]:
    """
    验证推理过程
    """
    errors = []
    
    if not process.input_problem:
        errors.append("Input problem is required")
    
    if not process.steps:
        errors.append("Reasoning steps are required")
    
    if not process.conclusion:
        errors.append("Conclusion is required")
    
    if not (0 <= process.confidence <= 1):
        errors.append("Confidence must be between 0 and 1")
    
    if process.reasoning_strategy not in ["chain_of_thought", "tree_of_thoughts", "react", "plan_and_execute"]:
        errors.append("Invalid reasoning strategy")
    
    # 验证步骤
    step_numbers = []
    for i, step in enumerate(process.steps):
        if step.step_number != i + 1:
            errors.append(f"Step {i+1} has incorrect step number: {step.step_number}")
        if not step.content:
            errors.append(f"Step {i+1} content is required")
        if not (0 <= step.confidence <= 1):
            errors.append(f"Step {i+1} confidence must be between 0 and 1")
    
    return len(errors) == 0, errors


def create_sample_cognitive_task(content: str, task_type: str = "general") -> CognitiveTask:
    """
    创建示例认知任务
    """
    return CognitiveTask(
        id=f"sample_task_{int(datetime.now().timestamp())}",
        content=content,
        task_type=task_type,
        priority="normal",
        complexity="moderate",
        metadata={
            "created_at": datetime.now().isoformat(),
            "source": "sample_generator"
        }
    )


def create_sample_reasoning_process(input_problem: str, conclusion: str) -> ReasoningProcess:
    """
    创建示例推理过程
    """
    return ReasoningProcess(
        id=f"sample_process_{int(datetime.now().timestamp())}",
        input_problem=input_problem,
        steps=[
            ReasoningStep(
                step_number=1,
                content="Analyze the problem and identify key elements",
                reasoning_type="analytical",
                confidence=0.9,
                supporting_evidence=[input_problem],
                alternatives_considered=[],
                timestamp=datetime.now()
            ),
            ReasoningStep(
                step_number=2,
                content="Apply relevant knowledge and principles",
                reasoning_type="logical",
                confidence=0.85,
                supporting_evidence=["relevant knowledge", "principles"],
                alternatives_considered=[],
                timestamp=datetime.now()
            ),
            ReasoningStep(
                step_number=3,
                content=f"Draw conclusion: {conclusion}",
                reasoning_type="synthetic",
                confidence=0.9,
                supporting_evidence=["reasoning process"],
                alternatives_considered=[],
                timestamp=datetime.now()
            )
        ],
        conclusion=conclusion,
        confidence=0.88,
        reasoning_strategy="chain_of_thought",
        bias_indicators=[],
        timestamp=datetime.now(),
        metadata={"sample": True}
    )


# 初始化工具
def init_cognitive_tools():
    """
    初始化认知工具
    """
    # 设置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Cognitive tools initialized successfully")
    
    return logger


# 初始化
logger = init_cognitive_tools()