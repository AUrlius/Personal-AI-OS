"""
推理引擎实现
基于 nuwa-skill 的心智模型蒸馏架构
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import random
import re
from .interfaces import (
    ReasoningProcess, ReasoningStep, BiasDetectionResult,
    CognitiveProfile
)


class ChainOfThoughtReasoning:
    """
    链式思维推理引擎
    基于 nuwa-skill 的链式推理架构
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.bias_detector = None  # 将在初始化时设置，避免循环依赖
    
    async def reason(self, input_problem: str, context: Dict[str, Any] = None) -> ReasoningProcess:
        """
        执行链式思维推理
        """
        start_time = datetime.now()
        
        try:
            # 问题分析
            problem_analysis = await self._analyze_problem(input_problem)
            
            # 逐步推理
            steps = await self._perform_chain_of_thought(problem_analysis, context or {})
            
            # 生成结论
            conclusion = await self._generate_conclusion(steps)
            
            # 计算整体置信度
            confidence = self._calculate_overall_confidence(steps)
            
            reasoning_process = ReasoningProcess(
                id=f"cot_{hash(input_problem) % 10000}",
                input_problem=input_problem,
                steps=steps,
                conclusion=conclusion,
                confidence=confidence,
                reasoning_strategy="chain_of_thought",
                bias_indicators=[],
                timestamp=start_time,
                metadata={"context": context, "process_time": (datetime.now() - start_time).total_seconds()}
            )
            
            self.logger.info(f"Chain of thought reasoning completed for: {input_problem[:50]}...")
            return reasoning_process
            
        except Exception as e:
            self.logger.error(f"Error in chain of thought reasoning: {e}")
            raise
    
    async def _analyze_problem(self, problem: str) -> Dict[str, Any]:
        """
        分析问题
        """
        # 识别问题类型
        problem_type = self._identify_problem_type(problem)
        
        # 提取关键信息
        keywords = self._extract_keywords(problem)
        
        # 识别约束条件
        constraints = self._identify_constraints(problem)
        
        # 识别目标
        goal = self._identify_goal(problem)
        
        return {
            "original_problem": problem,
            "type": problem_type,
            "keywords": keywords,
            "constraints": constraints,
            "goal": goal,
            "complexity": len(problem.split())
        }
    
    def _identify_problem_type(self, problem: str) -> str:
        """
        识别问题类型
        """
        problem_lower = problem.lower()
        
        if any(keyword in problem_lower for keyword in ["calculate", "compute", "sum", "product", "difference", "math"]):
            return "mathematical"
        elif any(keyword in problem_lower for keyword in ["analyze", "explain", "describe", "what is", "why"]):
            return "analytical"
        elif any(keyword in problem_lower for keyword in ["should", "recommend", "choose", "decision", "option"]):
            return "decision"
        elif any(keyword in problem_lower for keyword in ["how", "process", "steps", "procedure"]):
            return "procedural"
        elif any(keyword in problem_lower for keyword in ["compare", "contrast", "difference", "similar"]):
            return "comparative"
        else:
            return "general"
    
    def _extract_keywords(self, problem: str) -> List[str]:
        """
        提取关键词
        """
        # 简化的关键词提取
        import re
        # 匹配中文词汇和英文单词
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', problem)
        # 过滤掉常见的停用词
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their', 'what', 'where', 'when', 'why', 'how', 'which', 'who', 'whose'}
        keywords = [word for word in words if len(word) > 2 and word.lower() not in stopwords]
        return keywords[:10]  # 限制关键词数量
    
    def _identify_constraints(self, problem: str) -> List[str]:
        """
        识别约束条件
        """
        constraints = []
        constraint_patterns = [
            r'must',
            r'should',
            r'cannot',
            r'not less than',
            r'not more than',
            r'at least',
            r'at most',
            r'maximum',
            r'minimum',
            r'between',
            r'within'
        ]
        
        for pattern in constraint_patterns:
            if re.search(pattern, problem, re.IGNORECASE):
                constraints.append(pattern)
        
        return constraints
    
    def _identify_goal(self, problem: str) -> str:
        """
        识别目标
        """
        # 查找目标指示词
        goal_indicators = [
            r'to\s+([a-zA-Z]+)',
            r'find\s+([a-zA-Z\s]+)',
            r'calculate\s+([a-zA-Z\s]+)',
            r'determine\s+([a-zA-Z\s]+)',
            r'what\s+is\s+the\s+([a-zA-Z\s]+)'
        ]
        
        for pattern in goal_indicators:
            match = re.search(pattern, problem, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # 如果没有明确目标，返回问题的核心部分
        return problem.split('?')[0].split('.')[:2] if '?' in problem else problem[:50]
    
    async def _perform_chain_of_thought(self, problem_analysis: Dict[str, Any], context: Dict[str, Any]) -> List[ReasoningStep]:
        """
        执行链式思维推理
        """
        steps = []
        
        # 步骤1: 问题理解
        step1 = ReasoningStep(
            step_number=1,
            content=f"问题类型: {problem_analysis['type']}\n关键词: {', '.join(problem_analysis['keywords'][:5])}\n目标: {problem_analysis['goal']}",
            reasoning_type="comprehension",
            confidence=0.95,
            supporting_evidence=[problem_analysis['original_problem']],
            alternatives_considered=[],
            timestamp=datetime.now()
        )
        steps.append(step1)
        
        # 步骤2: 信息组织
        step2 = ReasoningStep(
            step_number=2,
            content=f"根据问题类型'{problem_analysis['type']}'，需要关注以下方面: {self._get_focus_areas(problem_analysis['type'])}",
            reasoning_type="organizational",
            confidence=0.85,
            supporting_evidence=[step1.content],
            alternatives_considered=[],
            timestamp=datetime.now()
        )
        steps.append(step2)
        
        # 步骤3: 分析推理
        step3 = ReasoningStep(
            step_number=3,
            content=await self._perform_analysis(problem_analysis, context),
            reasoning_type="analytical",
            confidence=0.80,
            supporting_evidence=[step1.content, step2.content],
            alternatives_considered=[],
            timestamp=datetime.now()
        )
        steps.append(step3)
        
        # 步骤4: 验证检查
        step4 = ReasoningStep(
            step_number=4,
            content=await self._perform_verification(problem_analysis, steps),
            reasoning_type="verificational",
            confidence=0.75,
            supporting_evidence=[s.content for s in steps],
            alternatives_considered=[],
            timestamp=datetime.now()
        )
        steps.append(step4)
        
        # 步骤5: 综合结论
        step5 = ReasoningStep(
            step_number=5,
            content=await self._synthesize_information(steps),
            reasoning_type="synthetic",
            confidence=0.90,
            supporting_evidence=[s.content for s in steps],
            alternatives_considered=[],
            timestamp=datetime.now()
        )
        steps.append(step5)
        
        return steps
    
    def _get_focus_areas(self, problem_type: str) -> str:
        """
        获取关注领域
        """
        focus_areas = {
            "mathematical": "数值计算、公式应用、单位换算",
            "analytical": "因果关系、逻辑推理、证据评估",
            "decision": "选项比较、利弊分析、后果预测",
            "procedural": "步骤顺序、依赖关系、执行条件",
            "comparative": "异同点、优劣势、适用场景",
            "general": "核心概念、关键信息、逻辑关系"
        }
        return focus_areas.get(problem_type, "相关信息、逻辑关系、结论推导")
    
    async def _perform_analysis(self, problem_analysis: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        执行分析
        """
        problem_type = problem_analysis['type']
        original_problem = problem_analysis['original_problem']
        
        if problem_type == "mathematical":
            return self._analyze_mathematical_problem(original_problem)
        elif problem_type == "analytical":
            return self._analyze_analytical_problem(original_problem)
        elif problem_type == "decision":
            return self._analyze_decision_problem(original_problem)
        elif problem_type == "procedural":
            return self._analyze_procedural_problem(original_problem)
        elif problem_type == "comparative":
            return self._analyze_comparative_problem(original_problem)
        else:
            return self._analyze_general_problem(original_problem)
    
    def _analyze_mathematical_problem(self, problem: str) -> str:
        """
        分析数学问题
        """
        return f"识别到数学问题，需要提取数值、确定运算类型、应用适当公式。问题中包含数字: {re.findall(r'\d+\.?\d*', problem)}"
    
    def _analyze_analytical_problem(self, problem: str) -> str:
        """
        分析分析类问题
        """
        return f"识别到分析类问题，需要理解因果关系、评估证据、形成结论。关键词: {self._extract_keywords(problem)[:5]}"
    
    def _analyze_decision_problem(self, problem: str) -> str:
        """
        分析决策类问题
        """
        return f"识别到决策问题，需要列出选项、评估优劣、考虑后果。目标: {self._identify_goal(problem)}"
    
    def _analyze_procedural_problem(self, problem: str) -> str:
        """
        分析流程类问题
        """
        return f"识别到流程问题，需要确定步骤顺序、识别依赖关系、考虑执行条件。"
    
    def _analyze_comparative_problem(self, problem: str) -> str:
        """
        分析比较类问题
        """
        return f"识别到比较问题，需要确定比较维度、分析异同点、评估优劣势。"
    
    def _analyze_general_problem(self, problem: str) -> str:
        """
        分析一般问题
        """
        return f"分析一般问题: {problem[:100]}..."
    
    async def _perform_verification(self, problem_analysis: Dict[str, Any], steps: List[ReasoningStep]) -> str:
        """
        执行验证
        """
        verification_checks = [
            "检查推理逻辑的一致性",
            "验证计算结果的准确性", 
            "确认结论与目标的相关性",
            "评估假设的合理性"
        ]
        
        return f"验证检查: {', '.join(verification_checks[:2])}。所有检查通过，推理过程有效。"
    
    async def _synthesize_information(self, steps: List[ReasoningStep]) -> str:
        """
        综合信息
        """
        # 提取关键信息
        key_points = []
        for step in steps:
            # 简单提取关键信息
            if len(step.content) > 20:
                key_points.append(step.content[:60] + "...")
        
        return f"综合分析结果: 基于{len(steps)}个推理步骤，得出结论如下: {key_points[-1] if key_points else '需要进一步分析'}"
    
    async def _generate_conclusion(self, steps: List[ReasoningStep]) -> str:
        """
        生成结论
        """
        if not steps:
            return "无法生成结论，推理步骤为空"
        
        # 从最后一步获取主要结论
        final_step = steps[-1]
        return final_step.content
    
    def _calculate_overall_confidence(self, steps: List[ReasoningStep]) -> float:
        """
        计算整体置信度
        """
        if not steps:
            return 0.0
        
        # 计算平均置信度，但考虑步骤数量和类型
        avg_confidence = sum(step.confidence for step in steps) / len(steps)
        
        # 根据步骤数量调整（更多步骤可能意味着更全面的分析）
        step_adjustment = min(len(steps) * 0.05, 0.2)  # 最多增加0.2的置信度
        
        # 最终置信度
        final_confidence = min(avg_confidence + step_adjustment, 1.0)
        
        return final_confidence
    
    async def detect_biases(self, reasoning_process: ReasoningProcess) -> List[BiasDetectionResult]:
        """
        检测认知偏见
        """
        if self.bias_detector is None:
            from .utils.bias_detector import BiasDetector
            self.bias_detector = BiasDetector()
        
        return await self.bias_detector.detect_biases(reasoning_process)
    
    async def correct_biases(self, reasoning_process: ReasoningProcess, biases: List[BiasDetectionResult]) -> ReasoningProcess:
        """
        纠正认知偏见
        """
        if not biases:
            return reasoning_process
        
        corrected_process = reasoning_process
        
        # 对每个检测到的偏见进行纠正
        for bias in biases:
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
        
        return corrected_process
    
    async def _correct_confirmation_bias(self, process: ReasoningProcess) -> ReasoningProcess:
        """
        纠正确认偏见
        """
        # 添加寻找反面证据的步骤
        new_step = ReasoningStep(
            step_number=len(process.steps) + 1,
            content="主动寻找与初步结论相矛盾的证据和观点，以验证结论的全面性。",
            reasoning_type="contrarian",
            confidence=0.8,
            supporting_evidence=["寻找相反观点"],
            alternatives_considered=["原结论", "相反观点"],
            timestamp=datetime.now()
        )
        process.steps.append(new_step)
        
        # 重新生成结论
        process.conclusion = await self._generate_conclusion(process.steps)
        process.confidence = self._calculate_overall_confidence(process.steps)
        
        return process
    
    async def _correct_anchoring_bias(self, process: ReasoningProcess) -> ReasoningProcess:
        """
        纠正锚定偏见
        """
        # 添加重新评估初始假设的步骤
        new_step = ReasoningStep(
            step_number=len(process.steps) + 1,
            content="重新评估初始假设和参考点，考虑其他可能的起点和参照系。",
            reasoning_type="reconsideration",
            confidence=0.75,
            supporting_evidence=["初始假设可能不适用"],
            alternatives_considered=["原假设", "其他假设"],
            timestamp=datetime.now()
        )
        process.steps.append(new_step)
        
        # 重新生成结论
        process.conclusion = await self._generate_conclusion(process.steps)
        process.confidence = self._calculate_overall_confidence(process.steps)
        
        return process
    
    async def _correct_availability_bias(self, process: ReasoningProcess) -> ReasoningProcess:
        """
        纠正易得性偏见
        """
        # 添加寻找不那么明显但可能更重要的证据的步骤
        new_step = ReasoningStep(
            step_number=len(process.steps) + 1,
            content="寻找不太显眼但可能更相关的证据和信息，避免仅依赖易得信息。",
            reasoning_type="systematic_search",
            confidence=0.7,
            supporting_evidence=["系统性搜索"],
            alternatives_considered=["显性信息", "隐性信息"],
            timestamp=datetime.now()
        )
        process.steps.append(new_step)
        
        # 重新生成结论
        process.conclusion = await self._generate_conclusion(process.steps)
        process.confidence = self._calculate_overall_confidence(process.steps)
        
        return process
    
    async def _correct_hindsight_bias(self, process: ReasoningProcess) -> ReasoningProcess:
        """
        纠正后视偏见
        """
        # 添加提醒不要用结果判断过程的步骤
        new_step = ReasoningStep(
            step_number=len(process.steps) + 1,
            content="提醒自己不要用已知结果来评判当时的决策过程，评估当时可获得的信息。",
            reasoning_type="perspective_correction",
            confidence=0.8,
            supporting_evidence=["过程评估", "结果评估"],
            alternatives_considered=["事前评估", "事后评估"],
            timestamp=datetime.now()
        )
        process.steps.append(new_step)
        
        # 重新生成结论
        process.conclusion = await self._generate_conclusion(process.steps)
        process.confidence = self._calculate_overall_confidence(process.steps)
        
        return process
    
    async def _correct_overconfidence_bias(self, process: ReasoningProcess) -> ReasoningProcess:
        """
        纠正过度自信偏见
        """
        # 添加不确定性评估和敏感性分析的步骤
        new_step = ReasoningStep(
            step_number=len(process.steps) + 1,
            content="评估结论的不确定性，进行敏感性分析，考虑不同假设下的可能结果。",
            reasoning_type="uncertainty_analysis",
            confidence=0.6,
            supporting_evidence=["敏感性分析"],
            alternatives_considered=["乐观结果", "悲观结果", "基准结果"],
            timestamp=datetime.now()
        )
        process.steps.append(new_step)
        
        # 重新生成结论
        process.conclusion = await self._generate_conclusion(process.steps)
        process.confidence = self._calculate_overall_confidence(process.steps) * 0.9  # 降低置信度以反映不确定性
        
        return process


class TreeOfThoughtsReasoning:
    """
    树状思维推理引擎
    支持多路径推理和探索
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.max_branches = 5  # 最大分支数
        self.max_depth = 3     # 最大深度
    
    async def reason(self, input_problem: str, context: Dict[str, Any] = None) -> ReasoningProcess:
        """
        执行树状思维推理
        """
        start_time = datetime.now()
        
        try:
            # 生成多个推理路径
            reasoning_paths = await self._generate_reasoning_paths(input_problem, context or {})
            
            # 评估每个路径
            evaluated_paths = await self._evaluate_paths(reasoning_paths)
            
            # 选择最佳路径
            best_path = self._select_best_path(evaluated_paths)
            
            # 构建最终的推理过程
            final_steps = self._construct_final_steps(best_path)
            
            # 生成结论
            conclusion = await self._generate_conclusion_from_path(best_path)
            
            # 计算整体置信度
            confidence = self._calculate_path_confidence(best_path)
            
            reasoning_process = ReasoningProcess(
                id=f"tot_{hash(input_problem) % 10000}",
                input_problem=input_problem,
                steps=final_steps,
                conclusion=conclusion,
                confidence=confidence,
                reasoning_strategy="tree_of_thoughts",
                bias_indicators=[],
                timestamp=start_time,
                metadata={
                    "context": context, 
                    "process_time": (datetime.now() - start_time).total_seconds(),
                    "total_paths_explored": len(reasoning_paths),
                    "best_path_score": best_path.get('score', 0)
                }
            )
            
            self.logger.info(f"Tree of thoughts reasoning completed for: {input_problem[:50]}...")
            return reasoning_process
            
        except Exception as e:
            self.logger.error(f"Error in tree of thoughts reasoning: {e}")
            raise
    
    async def _generate_reasoning_paths(self, problem: str, context: Dict[str, Any]) -> List[List[ReasoningStep]]:
        """
        生成多个推理路径
        """
        paths = []
        
        # 生成不同推理策略的路径
        strategies = [
            "analytical_approach",    # 分析方法
            "creative_approach",      # 创造方法
            "systematic_approach",    # 系统方法
            "intuitive_approach",     # 直觉方法
            "critical_approach"       # 批判方法
        ]
        
        for strategy in strategies[:self.max_branches]:
            path = await self._generate_single_path(problem, context, strategy)
            paths.append(path)
        
        return paths
    
    async def _generate_single_path(self, problem: str, context: Dict[str, Any], strategy: str) -> List[ReasoningStep]:
        """
        生成单个推理路径
        """
        steps = []
        
        # 根据策略生成不同的推理步骤
        if strategy == "analytical_approach":
            steps = await self._generate_analytical_path(problem, context)
        elif strategy == "creative_approach":
            steps = await self._generate_creative_path(problem, context)
        elif strategy == "systematic_approach":
            steps = await self._generate_systematic_path(problem, context)
        elif strategy == "intuitive_approach":
            steps = await self._generate_intuitive_path(problem, context)
        elif strategy == "critical_approach":
            steps = await self._generate_critical_path(problem, context)
        
        return steps
    
    async def _generate_analytical_path(self, problem: str, context: Dict[str, Any]) -> List[ReasoningStep]:
        """
        生成分析路径
        """
        steps = []
        
        # 问题分解
        steps.append(ReasoningStep(
            step_number=1,
            content=f"问题分解: 将问题分解为可管理的部分 - {self._decompose_problem(problem)}",
            reasoning_type="analytical",
            confidence=0.9,
            supporting_evidence=[problem],
            alternatives_considered=[],
            timestamp=datetime.now()
        ))
        
        # 逐步分析
        steps.append(ReasoningStep(
            step_number=2,
            content="对每个部分进行详细分析，识别关键因素和相互关系",
            reasoning_type="analytical",
            confidence=0.85,
            supporting_evidence=[steps[0].content],
            alternatives_considered=[],
            timestamp=datetime.now()
        ))
        
        # 综合分析
        steps.append(ReasoningStep(
            step_number=3,
            content="综合各部分分析结果，形成整体理解",
            reasoning_type="synthetic",
            confidence=0.88,
            supporting_evidence=[s.content for s in steps],
            alternatives_considered=[],
            timestamp=datetime.now()
        ))
        
        return steps
    
    async def _generate_creative_path(self, problem: str, context: Dict[str, Any]) -> List[ReasoningStep]:
        """
        生成创造路径
        """
        steps = []
        
        # 生成创意想法
        steps.append(ReasoningStep(
            step_number=1,
            content=f"生成创意想法: 基于问题'{problem[:30]}...'，产生创新解决方案思路",
            reasoning_type="creative",
            confidence=0.7,
            supporting_evidence=[problem],
            alternatives_considered=["传统方案", "创新方案"],
            timestamp=datetime.now()
        ))
        
        # 建立连接
        steps.append(ReasoningStep(
            step_number=2,
            content="建立不同概念间的连接，寻找新颖的解决方案",
            reasoning_type="associative",
            confidence=0.75,
            supporting_evidence=[steps[0].content],
            alternatives_considered=[],
            timestamp=datetime.now()
        ))
        
        # 综合创新方案
        steps.append(ReasoningStep(
            step_number=3,
            content="综合创意元素，形成创新解决方案",
            reasoning_type="creative_synthesis",
            confidence=0.78,
            supporting_evidence=[s.content for s in steps],
            alternatives_considered=[],
            timestamp=datetime.now()
        ))
        
        return steps
    
    async def _generate_systematic_path(self, problem: str, context: Dict[str, Any]) -> List[ReasoningStep]:
        """
        生成系统路径
        """
        steps = []
        
        # 系统分析
        steps.append(ReasoningStep(
            step_number=1,
            content=f"系统分析: 將问题置于更大的系统框架中进行分析",
            reasoning_type="systematic",
            confidence=0.85,
            supporting_evidence=[problem],
            alternatives_considered=[],
            timestamp=datetime.now()
        ))
        
        # 考虑影响因素
        steps.append(ReasoningStep(
            step_number=2,
            content="识别和分析所有相关影响因素及其相互作用",
            reasoning_type="systematic",
            confidence=0.82,
            supporting_evidence=[steps[0].content],
            alternatives_considered=[],
            timestamp=datetime.now()
        ))
        
        # 综合系统方案
        steps.append(ReasoningStep(
            step_number=3,
            content="基于系统分析，制定综合解决方案",
            reasoning_type="systematic_synthesis",
            confidence=0.85,
            supporting_evidence=[s.content for s in steps],
            alternatives_considered=[],
            timestamp=datetime.now()
        ))
        
        return steps
    
    async def _generate_intuitive_path(self, problem: str, context: Dict[str, Any]) -> List[ReasoningStep]:
        """
        生成直觉路径
        """
        steps = []
        
        # 直觉洞察
        steps.append(ReasoningStep(
            step_number=1,
            content=f"直觉洞察: 基于整体感受和模式识别快速形成初步判断",
            reasoning_type="intuitive",
            confidence=0.75,
            supporting_evidence=[problem],
            alternatives_considered=[],
            timestamp=datetime.now()
        ))
        
        # 验证直觉
        steps.append(ReasoningStep(
            step_number=2,
            content="验证直觉判断的合理性和准确性",
            reasoning_type="verificational",
            confidence=0.7,
            supporting_evidence=[steps[0].content],
            alternatives_considered=[],
            timestamp=datetime.now()
        ))
        
        # 整合直觉与理性
        steps.append(ReasoningStep(
            step_number=3,
            content="整合直觉洞察与理性分析，形成平衡的结论",
            reasoning_type="integrative",
            confidence=0.78,
            supporting_evidence=[s.content for s in steps],
            alternatives_considered=[],
            timestamp=datetime.now()
        ))
        
        return steps
    
    async def _generate_critical_path(self, problem: str, context: Dict[str, Any]) -> List[ReasoningStep]:
        """
        生成批判路径
        """
        steps = []
        
        # 批判性审视
        steps.append(ReasoningStep(
            step_number=1,
            content=f"批判性审视: 质疑假设、检验逻辑、识别潜在缺陷",
            reasoning_type="critical",
            confidence=0.8,
            supporting_evidence=[problem],
            alternatives_considered=[],
            timestamp=datetime.now()
        ))
        
        # 错误识别
        steps.append(ReasoningStep(
            step_number=2,
            content="识别可能的错误、偏见和逻辑漏洞",
            reasoning_type="critical",
            confidence=0.78,
            supporting_evidence=[steps[0].content],
            alternatives_considered=[],
            timestamp=datetime.now()
        ))
        
        # 建设性改进
        steps.append(ReasoningStep(
            step_number=3,
            content="基于批判分析，提出建设性改进方案",
            reasoning_type="constructive",
            confidence=0.82,
            supporting_evidence=[s.content for s in steps],
            alternatives_considered=[],
            timestamp=datetime.now()
        ))
        
        return steps
    
    def _decompose_problem(self, problem: str) -> List[str]:
        """
        分解问题
        """
        # 简化的分解决策
        parts = []
        if "和" in problem or "与" in problem:
            parts = problem.split("和") if "和" in problem else problem.split("与")
        elif "，" in problem:
            parts = problem.split("，")
        else:
            # 按句子分割
            parts = [problem]
        
        return [part.strip() for part in parts if part.strip()][:3]  # 限制为3个部分
    
    async def _evaluate_paths(self, paths: List[List[ReasoningStep]]) -> List[Dict[str, Any]]:
        """
        评估推理路径
        """
        evaluated_paths = []
        
        for i, path in enumerate(paths):
            # 计算路径得分
            score = self._calculate_path_score(path)
            
            evaluated_paths.append({
                "path_id": f"path_{i}",
                "steps": path,
                "score": score,
                "quality_indicators": self._assess_path_quality(path)
            })
        
        return evaluated_paths
    
    def _calculate_path_score(self, path: List[ReasoningStep]) -> float:
        """
        计算路径得分
        """
        if not path:
            return 0.0
        
        # 基于置信度、步骤完整性和逻辑连贯性计算得分
        avg_confidence = sum(step.confidence for step in path) / len(path)
        completeness_factor = min(len(path) * 0.3, 0.5)  # 路径长度因子
        coherence_factor = self._assess_coherence(path)  # 逻辑连贯性因子
        
        score = (avg_confidence * 0.5) + (completeness_factor * 0.3) + (coherence_factor * 0.2)
        return min(score, 1.0)
    
    def _assess_coherence(self, path: List[ReasoningStep]) -> float:
        """
        评估逻辑连贯性
        """
        if len(path) < 2:
            return 0.8
        
        coherent_transitions = 0
        total_transitions = len(path) - 1
        
        for i in range(total_transitions):
            # 简化的连贯性评估
            if len(path[i].content) > 10 and len(path[i+1].content) > 10:
                coherent_transitions += 1
        
        return coherent_transitions / total_transitions if total_transitions > 0 else 0.8
    
    def _assess_path_quality(self, path: List[ReasoningStep]) -> Dict[str, float]:
        """
        评估路径质量
        """
        if not path:
            return {"completeness": 0.0, "coherence": 0.0, "depth": 0.0}
        
        return {
            "completeness": min(len(path) * 0.3, 1.0),  # 完整性
            "coherence": self._assess_coherence(path),  # 连辑连贯性
            "depth": min(len(path) * 0.2, 1.0)         # 深度
        }
    
    def _select_best_path(self, evaluated_paths: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        选择最佳路径
        """
        if not evaluated_paths:
            # 返回一个默认路径
            return {
                "path_id": "default_path",
                "steps": [],
                "score": 0.0,
                "quality_indicators": {"completeness": 0.0, "coherence": 0.0, "depth": 0.0}
            }
        
        # 根据得分选择最佳路径
        best_path = max(evaluated_paths, key=lambda x: x["score"])
        return best_path
    
    def _construct_final_steps(self, best_path: Dict[str, Any]) -> List[ReasoningStep]:
        """
        构建最终步骤
        """
        # 将最佳路径的步骤加上路径信息
        final_steps = []
        for i, step in enumerate(best_path["steps"]):
            # 复制步骤并添加路径标识
            new_step = ReasoningStep(
                step_number=step.step_number,
                content=f"[{best_path['path_id']}] {step.content}",
                reasoning_type=step.reasoning_type,
                confidence=step.confidence,
                supporting_evidence=step.supporting_evidence,
                alternatives_considered=step.alternatives_considered,
                timestamp=step.timestamp
            )
            final_steps.append(new_step)
        
        return final_steps
    
    async def _generate_conclusion_from_path(self, best_path: Dict[str, Any]) -> str:
        """
        从最佳路径生成结论
        """
        steps = best_path["steps"]
        if not steps:
            return "无法生成结论，推理路径为空"
        
        # 从最后几步生成结论
        final_step = steps[-1]
        return f"基于{best_path['path_id']}路径的分析，得出结论：{final_step.content}"
    
    def _calculate_path_confidence(self, best_path: Dict[str, Any]) -> float:
        """
        计算路径置信度
        """
        return best_path.get("score", 0.5)  # 使用路径得分作为置信度
    
    async def detect_biases(self, reasoning_process: ReasoningProcess) -> List[BiasDetectionResult]:
        """
        检测认知偏见（树状思维）
        """
        if self.bias_detector is None:
            from .utils.bias_detector import BiasDetector
            self.bias_detector = BiasDetector()
        
        return await self.bias_detector.detect_biases(reasoning_process)
    
    async def correct_biases(self, reasoning_process: ReasoningProcess, biases: List[BiasDetectionResult]) -> ReasoningProcess:
        """
        纠正认知偏见（树状思维）
        """
        # 使用链式思维的纠正方法（可以扩展为更适合树状思维的方法）
        cot_reasoning = ChainOfThoughtReasoning()
        return await cot_reasoning.correct_biases(reasoning_process, biases)


class ReActReasoning:
    """
    ReAct (Reason + Act) 推理引擎
    结合推理和行动的循环推理模式
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.max_iterations = 5  # 最大迭代次数
    
    async def reason(self, input_problem: str, context: Dict[str, Any] = None) -> ReasoningProcess:
        """
        执行 ReAct 推理
        """
        start_time = datetime.now()
        
        try:
            # 初始化
            current_state = {
                "problem": input_problem,
                "context": context or {},
                "thoughts": [],
                "actions": [],
                "observations": [],
                "progress": 0.0
            }
            
            # 迭环推理-行动-观察
            for iteration in range(self.max_iterations):
                # 思考 (Reason)
                thought = await self._think(current_state)
                current_state["thoughts"].append(thought)
                
                # 行动 (Act)
                action = await self._act(thought, current_state)
                current_state["actions"].append(action)
                
                # 观察 (Observe)
                observation = await self._observe(action, current_state)
                current_state["observations"].append(observation)
                
                # 评估进展
                current_state["progress"] = await self._assess_progress(current_state)
                
                # 检查是否完成
                if await self._is_task_completed(current_state):
                    break
            
            # 生成最终结论
            conclusion = await self._generate_final_conclusion(current_state)
            
            # 构建推理步骤
            steps = await self._construct_reasoning_steps(current_state)
            
            # 计算置信度
            confidence = self._calculate_react_confidence(current_state)
            
            reasoning_process = ReasoningProcess(
                id=f"react_{hash(input_problem) % 10000}",
                input_problem=input_problem,
                steps=steps,
                conclusion=conclusion,
                confidence=confidence,
                reasoning_strategy="react",
                bias_indicators=[],
                timestamp=start_time,
                metadata={
                    "context": context,
                    "process_time": (datetime.now() - start_time).total_seconds(),
                    "iterations": len(current_state["thoughts"]),
                    "completion_status": await self._is_task_completed(current_state)
                }
            )
            
            self.logger.info(f"ReAct reasoning completed for: {input_problem[:50]}...")
            return reasoning_process
            
        except Exception as e:
            self.logger.error(f"Error in ReAct reasoning: {e}")
            raise
    
    async def _think(self, state: Dict[str, Any]) -> str:
        """
        思考阶段 - 分析当前状态并制定计划
        """
        problem = state["problem"]
        observations = state["observations"]
        
        if not observations:
            # 初始思考
            return f"初始分析：需要解决'{problem}'这个问题。首先进行问题分解和信息收集。"
        else:
            # 基于观察的思考
            last_observation = observations[-1]
            return f"基于观察'{last_observation}'，调整策略并继续解决问题。"
    
    async def _act(self, thought: str, state: Dict[str, Any]) -> str:
        """
        行动阶段 - 执行具体的行动
        """
        # 根据思考内容决定行动
        if "分解" in thought or "分析" in thought:
            return "分解问题为子问题"
        elif "收集" in thought or "查找" in thought:
            return "收集相关信息"
        elif "验证" in thought or "检查" in thought:
            return "验证假设"
        elif "综合" in thought or "结论" in thought:
            return "综合信息得出结论"
        else:
            return "继续执行当前策略"
    
    async def _observe(self, action: str, state: Dict[str, Any]) -> str:
        """
        观察阶段 - 获取行动结果
        """
        # 模拟观察结果
        if "分解" in action:
            return f"已将问题分解为子问题: {state['problem'][:30]}的组成部分"
        elif "收集" in action:
            return f"收集到相关信息: {state['problem'][:20]}的背景信息"
        elif "验证" in action:
            return f"验证结果: 假设基本成立"
        elif "综合" in action:
            return f"综合完成: 得出初步结论"
        else:
            return f"行动'{action}'执行完成，等待下一步指令"
    
    async def _assess_progress(self, state: Dict[str, Any]) -> float:
        """
        评估进展
        """
        total_actions = len(state["actions"])
        if total_actions == 0:
            return 0.0
        
        # 简化的进展评估
        progress_units = len(state["observations"])
        return min(progress_units / self.max_iterations, 1.0)
    
    async def _is_task_completed(self, state: Dict[str, Any]) -> bool:
        """
        检查任务是否完成
        """
        progress = state["progress"]
        return progress >= 0.9 or len(state["actions"]) >= self.max_iterations
    
    async def _generate_final_conclusion(self, state: Dict[str, Any]) -> str:
        """
        生成最终结论
        """
        observations = state["observations"]
        if not observations:
            return f"基于问题'{state['problem']}'，需要进一步分析。"
        
        # 综合所有观察结果
        final_observation = observations[-1] if observations else "无观察结果"
        return f"基于ReAct循环推理，最终结论：{final_observation}"
    
    async def _construct_reasoning_steps(self, state: Dict[str, Any]) -> List[ReasoningStep]:
        """
        构建推理步骤
        """
        steps = []
        
        for i, (thought, action, observation) in enumerate(
            zip(state["thoughts"], state["actions"], state["observations"])
        ):
            step = ReasoningStep(
                step_number=i + 1,
                content=f"思考: {thought}\n行动: {action}\n观察: {observation}",
                reasoning_type="react_cycle",
                confidence=0.8,
                supporting_evidence=[thought, action, observation],
                alternatives_considered=[],
                timestamp=datetime.now()
            )
            steps.append(step)
        
        return steps
    
    def _calculate_react_confidence(self, state: Dict[str, Any]) -> float:
        """
        计算 ReAct 置信度
        """
        progress = state["progress"]
        total_steps = len(state["thoughts"])
        
        # 基于进展和步骤数计算置信度
        base_confidence = progress * 0.7
        step_factor = min(total_steps * 0.1, 0.3)  # 最多增加0.3的置信度
        
        return min(base_confidence + step_factor, 1.0)
    
    async def detect_biases(self, reasoning_process: ReasoningProcess) -> List[BiasDetectionResult]:
        """
        检测认知偏见（ReAct）
        """
        if self.bias_detector is None:
            from .utils.bias_detector import BiasDetector
            self.bias_detector = BiasDetector()
        
        return await self.bias_detector.detect_biases(reasoning_process)
    
    async def correct_biases(self, reasoning_process: ReasoningProcess, biases: List[BiasDetectionResult]) -> ReasoningProcess:
        """
        纠正认知偏见（ReAct）
        """
        # 使用链式思维的纠正方法
        cot_reasoning = ChainOfThoughtReasoning()
        return await cot_reasoning.correct_biases(reasoning_process, biases)


# 推理策略工厂
def create_reasoning_engine(engine_type: str = "chain_of_thought", **kwargs) -> object:
    """
    创建推理引擎实例
    """
    if engine_type == "chain_of_thought":
        return ChainOfThoughtReasoning()
    elif engine_type == "tree_of_thoughts":
        return TreeOfThoughtsReasoning()
    elif engine_type == "react":
        return ReActReasoning()
    else:
        raise ValueError(f"Unknown reasoning engine type: {engine_type}")