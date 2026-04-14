"""
认知偏见检测器
基于 nuwa-skill 的偏见检测架构
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import re
from ..interfaces import ReasoningProcess, BiasDetectionResult


class BiasDetector:
    """
    认知偏见检测器
    检测和分析推理过程中的各种认知偏见
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 各种偏见的检测模式
        self.confirmation_bias_patterns = [
            r'only.*supporting',
            r'ignore.*contradict',
            r'biased.*toward',
            r'favor.*hypothesis',
            r'seek.*agreeable',
            r'interpret.*desired'
        ]
        
        self.anchoring_bias_patterns = [
            r'first.*impression',
            r'initial.*value',
            r'anchor.*point',
            r'fixate.*number',
            r'adjust.*insufficiently',
            r'insufficient.*adjustment'
        ]
        
        self.availability_bias_patterns = [
            r'recent.*event',
            r'easily.*recall',
            r'vivid.*memory',
            r'dramatic.*example',
            r'memorable.*case',
            r'available.*information'
        ]
        
        self.hindsight_bias_patterns = [
            r'knew.*all along',
            r'obvious.*outcome',
            r'predictable.*result',
            r'inevitable.*conclusion',
            r'foreseeable.*consequence',
            r'should.*have known'
        ]
        
        self.overconfidence_bias_patterns = [
            r'certain.*about',
            r'confident.*level',
            r'probability.*overestimated',
            r'accuracy.*overrated',
            r'overestimate.*precision',
            r'underestimate.*uncertainty'
        ]
        
        self.ambiguity_bias_patterns = [
            r'avoid.*uncertain',
            r'prefer.*known',
            r'risk.*averse.*uncertainty',
            r'unknown.*scary',
            r'ambiguous.*negative',
            r'uncertainty.*avoid'
        ]
        
        self.contrast_bias_patterns = [
            r'compared.*other',
            r'relative.*absolute',
            r'influence.*adjacent',
            r'judgment.*context',
            r'perception.*framed',
            r'comparison.*affect'
        ]
        
        self.framing_bias_patterns = [
            r'positively.*phrased',
            r'negatively.*framed',
            r'loss.*averse',
            r'gain.*seeking',
            r'presentation.*affects',
            r'wording.*influence'
        ]
        
        self.self_serving_bias_patterns = [
            r'attributed.*success',
            r'blame.*external',
            r'credit.*internal',
            r'failure.*circumstances',
            r'achievement.*ability',
            r'my.*success'
        ]
        
        self.illusory_correlation_patterns = [
            r'believe.*connected',
            r'perceive.*relationship',
            r'illusory.*correlation',
            r'false.*association',
            r'spurious.*connection',
            r'coincidence.*causation'
        ]
    
    async def detect_biases(self, reasoning_process: ReasoningProcess) -> List[BiasDetectionResult]:
        """
        检测推理过程中的认知偏见
        """
        try:
            detected_biases = []
            
            # 检测确认偏见
            confirmation_results = await self._detect_confirmation_bias(reasoning_process)
            detected_biases.extend(confirmation_results)
            
            # 检测锚定偏见
            anchoring_results = await self._detect_anchoring_bias(reasoning_process)
            detected_biases.extend(anchoring_results)
            
            # 检测易得性偏见
            availability_results = await self._detect_availability_bias(reasoning_process)
            detected_biases.extend(availability_results)
            
            # 检测后视偏见
            hindsight_results = await self._detect_hindsight_bias(reasoning_process)
            detected_biases.extend(hindsight_results)
            
            # 检测过度自信偏见
            overconfidence_results = await self._detect_overconfidence_bias(reasoning_process)
            detected_biases.extend(overconfidence_results)
            
            # 检测模糊性偏见
            ambiguity_results = await self._detect_ambiguity_bias(reasoning_process)
            detected_biases.extend(ambiguity_results)
            
            # 检测对比偏见
            contrast_results = await self._detect_contrast_bias(reasoning_process)
            detected_biases.extend(contrast_results)
            
            # 检测框架偏见
            framing_results = await self._detect_framing_bias(reasoning_process)
            detected_biases.extend(framing_results)
            
            # 检测自我服务偏见
            self_serving_results = await self._detect_self_serving_bias(reasoning_process)
            detected_biases.extend(self_serving_results)
            
            # 检测虚假相关偏见
            illusory_correlation_results = await self._detect_illusory_correlation(reasoning_process)
            detected_biases.extend(illusory_correlation_results)
            
            # 按严重程度排序
            detected_biases.sort(key=lambda x: x.severity, reverse=True)
            
            self.logger.info(f"Detected {len(detected_biases)} cognitive biases in reasoning process")
            return detected_biases
            
        except Exception as e:
            self.logger.error(f"Error detecting biases: {e}")
            return []
    
    async def _detect_confirmation_bias(self, process: ReasoningProcess) -> List[BiasDetectionResult]:
        """
        检测确认偏见
        """
        results = []
        
        # 检查推理步骤中的内容
        for step in process.steps:
            content_lower = step.content.lower()
            
            # 检查确认偏见模式
            for pattern in self.confirmation_bias_patterns:
                if re.search(pattern, content_lower):
                    evidence = re.findall(pattern, content_lower)
                    severity = min(len(evidence) * 0.2, 1.0)  # 基于匹配数量计算严重程度
                    
                    results.append(BiasDetectionResult(
                        type="confirmation",
                        severity=severity,
                        evidence=evidence,
                        suggestion="Consider actively seeking contradictory evidence and alternative viewpoints.",
                        confidence=0.8
                    ))
                    break  # 找到一个模式就足够
        
        # 检查结论
        conclusion_lower = process.conclusion.lower()
        for pattern in self.confirmation_bias_patterns:
            if re.search(pattern, conclusion_lower):
                evidence = re.findall(pattern, conclusion_lower)
                severity = min(len(evidence) * 0.25, 1.0)
                
                results.append(BiasDetectionResult(
                    type="confirmation",
                    severity=severity,
                    evidence=evidence,
                    suggestion="Reconsider the conclusion by examining opposing viewpoints.",
                    confidence=0.75
                ))
                break
        
        return results
    
    async def _detect_anchoring_bias(self, process: ReasoningProcess) -> List[BiasDetectionResult]:
        """
        检测锚定偏见
        """
        results = []
        
        # 检查是否过度依赖初始信息
        if process.steps:
            first_step_content = process.steps[0].content.lower()
            
            for pattern in self.anchoring_bias_patterns:
                if re.search(pattern, first_step_content):
                    evidence = re.findall(pattern, first_step_content)
                    severity = min(len(evidence) * 0.3, 1.0)
                    
                    results.append(BiasDetectionResult(
                        type="anchoring",
                        severity=severity,
                        evidence=evidence,
                        suggestion="Consider whether initial information unduly influenced your judgment. Adjust estimates based on additional information.",
                        confidence=0.7
                    ))
                    break
        
        # 检查数值相关的锚定
        if re.search(r'\b\d+\.?\d*\b', process.input_problem):
            # 检查推理过程中是否围绕初始数值进行调整
            numbers_in_problem = re.findall(r'\b\d+\.?\d*\b', process.input_problem)
            numbers_in_reasoning = []
            for step in process.steps:
                numbers_in_reasoning.extend(re.findall(r'\b\d+\.?\d*\b', step.content))
            
            # 如果推理过程中的数字与问题中的数字过于接近，可能表示锚定
            if numbers_in_problem and numbers_in_reasoning:
                close_numbers = 0
                for prob_num in numbers_in_problem:
                    for reason_num in numbers_in_reasoning:
                        if abs(float(prob_num) - float(reason_num)) < float(prob_num) * 0.1:  # 10% 内差内
                            close_numbers += 1
                
                if close_numbers > len(numbers_in_problem) * 0.5:  # 超过一半
                    results.append(BiasDetectionResult(
                        type="anchoring",
                        severity=0.6,
                        evidence=[f"Numbers in reasoning closely match problem numbers: {numbers_in_problem}"],
                        suggestion="Ensure adjustments from initial values are sufficient and well-justified.",
                        confidence=0.65
                    ))
        
        return results
    
    async def _detect_availability_bias(self, process: ReasoningProcess) -> List[BiasDetectionResult]:
        """
        检测易得性偏见
        """
        results = []
        
        # 检查是否过度依赖容易回忆的信息
        content = " ".join([step.content for step in process.steps]).lower()
        
        for pattern in self.availability_bias_patterns:
            if re.search(pattern, content):
                evidence = re.findall(pattern, content)
                severity = min(len(evidence) * 0.25, 1.0)
                
                results.append(BiasDetectionResult(
                    type="availability",
                    severity=severity,
                    evidence=evidence,
                    suggestion="Seek out less memorable but potentially more relevant information to balance your judgment.",
                    confidence=0.7
                ))
                break
        
        # 检查是否使用了戏剧性或显著的例子
        dramatic_words = ['disaster', 'tragedy', 'accident', 'crisis', 'emergency', 'catastrophe', 'incident']
        for word in dramatic_words:
            if word in content:
                # 检查这个词是否被过度强调
                occurrences = len(re.findall(r'\b' + word + r'\b', content))
                if occurrences > 1:  # 多次提及
                    results.append(BiasDetectionResult(
                        type="availability",
                        severity=0.5,
                        evidence=[f"Dramatic term '{word}' mentioned {occurrences} times"],
                        suggestion="Ensure your judgment isn't overly influenced by vivid but potentially unrepresentative examples.",
                        confidence=0.6
                    ))
                    break
        
        return results
    
    async def _detect_hindsight_bias(self, process: ReasoningProcess) -> List[BiasDetectionResult]:
        """
        检测后视偏见
        """
        results = []
        
        content = " ".join([step.content for step in process.steps]).lower() + " " + process.conclusion.lower()
        
        for pattern in self.hindsight_bias_patterns:
            if re.search(pattern, content):
                evidence = re.findall(pattern, content)
                severity = min(len(evidence) * 0.3, 1.0)
                
                results.append(BiasDetectionResult(
                    type="hindsight",
                    severity=severity,
                    evidence=evidence,
                    suggestion="Remember that outcomes weren't predictable beforehand. Evaluate decisions based on information available at the time.",
                    confidence=0.75
                ))
                break
        
        # 检查是否使用了表示预测的词汇来描述已知结果
        hindsight_words = ['inevitable', 'predictable', 'foreseeable', 'obvious', 'should_have_known']
        for word in hindsight_words:
            if word.replace('_', ' ') in content:
                results.append(BiasDetectionResult(
                    type="hindsight",
                    severity=0.6,
                    evidence=[f"Hindsight term '{word}' detected"],
                    suggestion="Consider whether this outcome was truly predictable beforehand.",
                    confidence=0.6
                ))
                break
        
        return results
    
    async def _detect_overconfidence_bias(self, process: ReasoningProcess) -> List[BiasDetectionResult]:
        """
        检测过度自信偏见
        """
        results = []
        
        # 检查推理步骤中的高置信度声明
        for step in process.steps:
            content_lower = step.content.lower()
            
            # 检查过度自信的表述
            overconfident_expressions = [
                'definitely', 'certainly', 'absolutely', 'without doubt', 'clearly', 
                'obviously', 'surely', 'undoubtedly', 'certain', '100%', 'always', 'never'
            ]
            
            found_expressions = []
            for expr in overconfident_expressions:
                if expr in content_lower:
                    found_expressions.append(expr)
            
            if found_expressions:
                # 根据步骤的置信度和使用的绝对性词汇来判断
                if step.confidence > 0.9 and len(found_expressions) > 2:  # 高置信度+多绝对性词汇
                    results.append(BiasDetectionResult(
                        type="overconfidence",
                        severity=min(len(found_expressions) * 0.15, 1.0),
                        evidence=found_expressions,
                        suggestion="Consider the uncertainty in your analysis. Express conclusions with appropriate confidence intervals.",
                        confidence=0.8
                    ))
                    break
        
        # 检查结论中的过度自信
        conclusion_lower = process.conclusion.lower()
        for expr in ['definitely', 'certainly', 'absolutely', 'without a doubt']:
            if expr in conclusion_lower:
                results.append(BiasDetectionResult(
                    type="overconfidence",
                    severity=0.7,
                    evidence=[f"Overconfident expression '{expr}' in conclusion"],
                    suggestion="Qualify your conclusion with appropriate uncertainty language.",
                    confidence=0.7
                ))
                break
        
        return results
    
    async def _detect_ambiguity_bias(self, process: ReasoningProcess) -> List[BiasDetectionResult]:
        """
        检测模糊性偏见
        """
        results = []
        
        content = " ".join([step.content for step in process.steps]).lower()
        
        for pattern in self.ambiguity_bias_patterns:
            if re.search(pattern, content):
                evidence = re.findall(pattern, content)
                severity = min(len(evidence) * 0.2, 1.0)
                
                results.append(BiasDetectionResult(
                    type="ambiguity",
                    severity=severity,
                    evidence=evidence,
                    suggestion="Embrace uncertainty and consider ambiguous options as potentially valuable.",
                    confidence=0.65
                ))
                break
        
        return results
    
    async def _detect_contrast_bias(self, process: ReasoningProcess) -> List[BiasDetectionResult]:
        """
        检测对比偏见
        """
        results = []
        
        content = " ".join([step.content for step in process.steps]).lower()
        
        for pattern in self.contrast_bias_patterns:
            if re.search(pattern, content):
                evidence = re.findall(pattern, content)
                severity = min(len(evidence) * 0.25, 1.0)
                
                results.append(BiasDetectionResult(
                    type="contrast",
                    severity=severity,
                    evidence=evidence,
                    suggestion="Evaluate options based on absolute merits rather than relative comparisons.",
                    confidence=0.6
                ))
                break
        
        return results
    
    async def _detect_framing_bias(self, process: ReasoningProcess) -> List[BiasDetectionResult]:
        """
        检测框架偏见
        """
        results = []
        
        content = " ".join([step.content for step in process.steps]).lower()
        
        for pattern in self.framing_bias_patterns:
            if re.search(pattern, content):
                evidence = re.findall(pattern, content)
                severity = min(len(evidence) * 0.3, 1.0)
                
                results.append(BiasDetectionResult(
                    type="framing",
                    severity=severity,
                    evidence=evidence,
                    suggestion="Reframe the problem in neutral terms to avoid biased presentation influencing your judgment.",
                    confidence=0.7
                ))
                break
        
        return results
    
    async def _detect_self_serving_bias(self, process: ReasoningProcess) -> List[BiasDetectionResult]:
        """
        检测自我服务偏见
        """
        results = []
        
        content = " ".join([step.content for step in process.steps]).lower()
        
        for pattern in self.self_serving_bias_patterns:
            if re.search(pattern, content):
                evidence = re.findall(pattern, content)
                severity = min(len(evidence) * 0.25, 1.0)
                
                results.append(BiasDetectionResult(
                    type="self-serving",
                    severity=severity,
                    evidence=evidence,
                    suggestion="Consider external factors that contributed to success and internal factors in failures.",
                    confidence=0.65
                ))
                break
        
        return results
    
    async def _detect_illusory_correlation(self, process: ReasoningProcess) -> List[BiasDetectionResult]:
        """
        检测虚假相关偏见
        """
        results = []
        
        content = " ".join([step.content for step in process.steps]).lower()
        
        for pattern in self.illusory_correlation_patterns:
            if re.search(pattern, content):
                evidence = re.findall(pattern, content)
                severity = min(len(evidence) * 0.2, 1.0)
                
                results.append(BiasDetectionResult(
                    type="illusory_correlation",
                    severity=severity,
                    evidence=evidence,
                    suggestion="Look for statistical evidence of correlation rather than relying on perceived connections.",
                    confidence=0.6
                ))
                break
        
        return results
    
    async def analyze_bias_severity(self, bias_results: List[BiasDetectionResult]) -> Dict[str, float]:
        """
        分析偏见严重程度
        """
        severity_analysis = {}
        
        for bias in bias_results:
            if bias.type not in severity_analysis:
                severity_analysis[bias.type] = []
            severity_analysis[bias.type].append(bias.severity)
        
        # 计算每种偏见的平均严重程度
        avg_severity = {}
        for bias_type, severities in severity_analysis.items():
            avg_severity[bias_type] = sum(severities) / len(severities)
        
        return avg_severity
    
    async def generate_bias_report(self, reasoning_process: ReasoningProcess) -> Dict[str, Any]:
        """
        生成偏见报告
        """
        detected_biases = await self.detect_biases(reasoning_process)
        
        report = {
            "process_id": reasoning_process.id,
            "total_biases_detected": len(detected_biases),
            "bias_types_found": list(set(bias.type for bias in detected_biases)),
            "severity_analysis": await self.analyze_bias_severity(detected_biases),
            "detailed_findings": [
                {
                    "type": bias.type,
                    "severity": bias.severity,
                    "evidence": bias.evidence,
                    "suggestion": bias.suggestion,
                    "confidence": bias.confidence
                } for bias in detected_biases
            ],
            "overall_bias_level": self._calculate_overall_bias_level(detected_biases),
            "recommendations": self._generate_recommendations(detected_biases),
            "generated_at": datetime.now().isoformat()
        }
        
        return report
    
    def _calculate_overall_bias_level(self, biases: List[BiasDetectionResult]) -> str:
        """
        计算整体偏见水平
        """
        if not biases:
            return "low"
        
        avg_severity = sum(bias.severity for bias in biases) / len(biases)
        
        if avg_severity >= 0.7:
            return "high"
        elif avg_severity >= 0.4:
            return "medium"
        else:
            return "low"
    
    def _generate_recommendations(self, biases: List[BiasDetectionResult]) -> List[str]:
        """
        生成建议
        """
        recommendations = []
        
        bias_types = [bias.type for bias in biases]
        
        if "confirmation" in bias_types:
            recommendations.append("Actively seek out contradictory evidence and alternative viewpoints.")
        
        if "anchoring" in bias_types:
            recommendations.append("Adjust your estimates sufficiently from initial values and consider multiple reference points.")
        
        if "availability" in bias_types:
            recommendations.append("Look for less memorable but potentially more relevant information.")
        
        if "overconfidence" in bias_types:
            recommendations.append("Express conclusions with appropriate confidence intervals and acknowledge uncertainty.")
        
        if not recommendations:
            recommendations.append("No significant cognitive biases were detected in the reasoning process.")
        
        return recommendations
    
    async def correct_biases(self, reasoning_process: ReasoningProcess, detected_biases: List[BiasDetectionResult]) -> ReasoningProcess:
        """
        纠正检测到的认知偏见
        """
        corrected_process = reasoning_process
        
        for bias in detected_biases:
            if bias.type == "confirmation":
                corrected_process = await self._correct_confirmation_bias(corrected_process)
            elif bias.type == "anchoring":
                corrected_process = await self._correct_anchoring_bias(corrected_process)
            elif bias.type == "availability":
                corrected_process = await self._correct_availability_bias(corrected_process)
            elif bias.type == "hindsight":
                corrected_process = await self._correct_hindsight_bias(corrected_process)
            elif bias.type == "overconfidence":
                corrected_process = await self._correct_overconfidence_bias(corrected_process)
            elif bias.type == "ambiguity":
                corrected_process = await self._correct_ambiguity_bias(corrected_process)
            elif bias.type == "contrast":
                corrected_process = await self._correct_contrast_bias(corrected_process)
            elif bias.type == "framing":
                corrected_process = await self._correct_framing_bias(corrected_process)
            elif bias.type == "self-serving":
                corrected_process = await self._correct_self_serving_bias(corrected_process)
            elif bias.type == "illusory_correlation":
                corrected_process = await self._correct_illusory_correlation_bias(corrected_process)
        
        return corrected_process
    
    async def _correct_confirmation_bias(self, process: ReasoningProcess) -> ReasoningProcess:
        """
        纠正确认偏见
        """
        # 添加寻找反面证据的步骤
        new_step = process.steps[-1] if process.steps else None
        if new_step:
            # 在最后一步添加反面证据寻找
            contradiction_step = f"{new_step.content} Additionally, I should consider evidence that contradicts this conclusion and alternative explanations."
            process.steps[-1] = new_step.__class__(
                step_number=new_step.step_number,
                content=contradiction_step,
                reasoning_type=new_step.reasoning_type,
                confidence=new_step.confidence * 0.9,  # 降低置信度
                supporting_evidence=new_step.supporting_evidence,
                alternatives_considered=new_step.alternatives_considered + ["opposing viewpoints"],
                timestamp=new_step.timestamp
            )
        
        return process
    
    async def _correct_anchoring_bias(self, process: ReasoningProcess) -> ReasoningProcess:
        """
        纠正锚定偏见
        """
        # 添加重新评估参考点的步骤
        if process.steps:
            reevaluation_step = f"Reevaluating initial assumptions and considering alternative reference points beyond the first impression."
            new_step = process.steps[-1].__class__(
                step_number=len(process.steps) + 1,
                content=reevaluation_step,
                reasoning_type="reevaluation",
                confidence=0.7,
                supporting_evidence=["alternative_reference_points"],
                alternatives_considered=["initial_anchor", "alternative_values"],
                timestamp=datetime.now()
            )
            process.steps.append(new_step)
        
        return process
    
    async def _correct_availability_bias(self, process: ReasoningProcess) -> ReasoningProcess:
        """
        纠正易得性偏见
        """
        # 添加系统性搜索的步骤
        if process.steps:
            search_step = f"Conducting systematic search for less memorable but potentially more representative information."
            new_step = process.steps[-1].__class__(
                step_number=len(process.steps) + 1,
                content=search_step,
                reasoning_type="systematic_search",
                confidence=0.75,
                supporting_evidence=["systematic_search"],
                alternatives_considered=["vivid_examples", "statistical_data"],
                timestamp=datetime.now()
            )
            process.steps.append(new_step)
        
        return process
    
    async def _correct_hindsight_bias(self, process: ReasoningProcess) -> ReasoningProcess:
        """
        纠正后视偏见
        """
        # 添加历史情境回顾的步骤
        if process.steps:
            context_step = f"Considering what information was available at the time of the decision, rather than with outcome knowledge."
            new_step = process.steps[-1].__class__(
                step_number=len(process.steps) + 1,
                content=context_step,
                reasoning_type="historical_context",
                confidence=0.8,
                supporting_evidence=["contemporary_information"],
                alternatives_considered=["with_hindsight", "at_the_time"],
                timestamp=datetime.now()
            )
            process.steps.append(new_step)
        
        return process
    
    async def _correct_overconfidence_bias(self, process: ReasoningProcess) -> ReasoningProcess:
        """
        纠正过度自信偏见
        """
        # 降低整体置信度
        process.confidence = process.confidence * 0.85
        
        # 添加不确定性分析
        if process.steps:
            uncertainty_step = f"Analyzing the uncertainty and potential errors in this analysis. Confidence should be appropriately qualified."
            new_step = process.steps[-1].__class__(
                step_number=len(process.steps) + 1,
                content=uncertainty_step,
                reasoning_type="uncertainty_analysis",
                confidence=0.6,
                supporting_evidence=["uncertainty_consideration"],
                alternatives_considered=["confident_assessment", "qualified_assessment"],
                timestamp=datetime.now()
            )
            process.steps.append(new_step)
        
        return process
    
    async def _correct_ambiguity_bias(self, process: ReasoningProcess) -> ReasoningProcess:
        """
        纠正模糊性偏见
        """
        # 添加处理不确定性的步骤
        if process.steps:
            ambiguity_step = f"Embracing the ambiguity and considering uncertain options as potentially valuable rather than avoiding them."
            new_step = process.steps[-1].__class__(
                step_number=len(process.steps) + 1,
                content=ambiguity_step,
                reasoning_type="ambiguity_acceptance",
                confidence=0.7,
                supporting_evidence=["uncertainty_value"],
                alternatives_considered=["avoid_ambiguous", "consider_ambiguous"],
                timestamp=datetime.now()
            )
            process.steps.append(new_step)
        
        return process
    
    async def _correct_contrast_bias(self, process: ReasoningProcess) -> ReasoningProcess:
        """
        纠正对比偏见
        """
        # 添加绝对评估的步骤
        if process.steps:
            absolute_step = f"Evaluating options based on absolute merits rather than relative comparisons to adjacent items."
            new_step = process.steps[-1].__class__(
                step_number=len(process.steps) + 1,
                content=absolute_step,
                reasoning_type="absolute_evaluation",
                confidence=0.75,
                supporting_evidence=["absolute_criteria"],
                alternatives_considered=["relative_comparison", "absolute_evaluation"],
                timestamp=datetime.now()
            )
            process.steps.append(new_step)
        
        return process
    
    async def _correct_framing_bias(self, process: ReasoningProcess) -> ReasoningProcess:
        """
        纠正框架偏见
        """
        # 添加重新框架的步骤
        if process.steps:
            reframing_step = f"Reframing the problem in neutral terms to avoid biased presentation influencing the judgment."
            new_step = process.steps[-1].__class__(
                step_number=len(process.steps) + 1,
                content=reframing_step,
                reasoning_type="reframing",
                confidence=0.7,
                supporting_evidence=["neutral_presentation"],
                alternatives_considered=["framed_presentation", "neutral_framing"],
                timestamp=datetime.now()
            )
            process.steps.append(new_step)
        
        return process
    
    async def _correct_self_serving_bias(self, process: ReasoningProcess) -> ReasoningProcess:
        """
        纠正自我服务偏见
        """
        # 添加客观归因的步骤
        if process.steps:
            attribution_step = f"Considering both internal and external factors that contributed to outcomes, rather than attributing successes to ability and failures to circumstances."
            new_step = process.steps[-1].__class__(
                step_number=len(process.steps) + 1,
                content=attribution_step,
                reasoning_type="attribution_analysis",
                confidence=0.75,
                supporting_evidence=["balanced_attribution"],
                alternatives_considered=["self_serving_attribution", "balanced_attribution"],
                timestamp=datetime.now()
            )
            process.steps.append(new_step)
        
        return process
    
    async def _correct_illusory_correlation_bias(self, process: ReasoningProcess) -> ReasoningProcess:
        """
        纠正虚假相关偏见
        """
        # 添加统计验证的步骤
        if process.steps:
            correlation_step = f"Looking for statistical evidence of correlation rather than relying on perceived connections. Examining base rates and sample sizes."
            new_step = process.steps[-1].__class__(
                step_number=len(process.steps) + 1,
                content=correlation_step,
                reasoning_type="statistical_analysis",
                confidence=0.65,
                supporting_evidence=["statistical_evidence"],
                alternatives_considered=["perceived_connection", "statistical_correlation"],
                timestamp=datetime.now()
            )
            process.steps.append(new_step)
        
        return process


class AdvancedBiasDetector(BiasDetector):
    """
    高级偏见检测器
    包含更复杂的检测算法
    """
    def __init__(self):
        super().__init__()
        self.contextual_bias_detection = True
        self.temporal_bias_patterns = True
        self.cross_domain_patterns = True
    
    async def detect_contextual_biases(self, reasoning_process: ReasoningProcess, context: Dict[str, Any]) -> List[BiasDetectionResult]:
        """
        检测上下文相关的偏见
        """
        results = []
        
        # 分析上下文是否影响推理
        if "emotional_state" in context:
            emotional_state = context["emotional_state"]
            if emotional_state in ["stressed", "anxious", "excited"]:
                results.append(BiasDetectionResult(
                    type="emotional_influence",
                    severity=0.5,
                    evidence=[f"Emotional state: {emotional_state} may influence judgment"],
                    suggestion="Be aware that your emotional state may be affecting your reasoning.",
                    confidence=0.6
                ))
        
        if "time_pressure" in context and context["time_pressure"]:
            results.append(BiasDetectionResult(
                type="time_pressure",
                severity=0.4,
                evidence=["Decision made under time pressure"],
                suggestion="Consider whether time pressure led to rushed judgments.",
                confidence=0.5
            ))
        
        return results


# 工厂函数
def create_bias_detector(detector_type: str = "standard", **kwargs) -> object:
    """
    创建偏见检测器实例
    """
    if detector_type == "standard":
        return BiasDetector()
    elif detector_type == "advanced":
        return AdvancedBiasDetector()
    else:
        raise ValueError(f"Unknown bias detector type: {detector_type}")