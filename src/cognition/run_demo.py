#!/usr/bin/env python3
"""
认知系统完整演示脚本
展示 Personal-AI-OS 认知系统的全部功能
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 导入认知系统组件
from .core import CognitiveSystem
from .interfaces import CognitiveTask, CognitiveResult
from .utils import CognitiveUtils
from .config_manager import get_config_manager


async def demonstrate_memory_system():
    """
    演示记忆系统功能
    """
    print("🧠=== 记忆系统演示 ===🧠\n")
    
    cognitive_system = await initialize_cognitive_system()
    
    # 演示记忆存储
    print("1️⃣ 存储记忆...")
    memory_store_task = CognitiveTask(
        id="demo_memory_store_001",
        content="记住：我叫张三，是一名软件工程师，住在北京市朝阳区，喜欢编程和阅读",
        task_type="memory_operation",
        priority="normal",
        complexity="simple",
        metadata={"operation": "store", "memory_type": "personal_info"}
    )
    
    store_result = await cognitive_system.process_task(memory_store_task)
    print(f"   存储结果: {'✅ 成功' if store_result.success else '❌ 失败'}")
    
    # 演示记忆检索
    print("\n2️⃣ 检索记忆...")
    memory_search_task = CognitiveTask(
        id="demo_memory_search_001",
        content="我的名字是什么？我住在哪里？我的职业是什么？",
        task_type="memory_operation",
        priority="normal",
        complexity="simple",
        metadata={"operation": "search", "query_type": "personal_info"}
    )
    
    search_result = await cognitive_system.process_task(memory_search_task)
    print(f"   检索结果: {'✅ 成功' if search_result.success else '❌ 失败'}")
    if search_result.success and search_result.output:
        print(f"   检索内容: {search_result.output}")
    
    print("\n--- 记忆系统演示完成 ---\n")


async def demonstrate_reasoning_system():
    """
    演示推理系统功能
    """
    print("🧮=== 推理系统演示 ===🧮\n")
    
    cognitive_system = await initialize_cognitive_system()
    
    # 演示链式思维推理
    print("1️⃣ 链式思维推理...")
    chain_task = CognitiveTask(
        id="demo_chain_of_thought_001",
        content="如果一个矩形的长是宽的2倍，周长是30厘米，求它的面积是多少？",
        task_type="reasoning",
        priority="normal",
        complexity="moderate",
        metadata={"reasoning_strategy": "chain_of_thought"}
    )
    
    chain_result = await cognitive_system.process_task(chain_task)
    print(f"   链式推理结果: {'✅ 成功' if chain_result.success else '❌ 失败'}")
    if chain_result.success:
        print(f"   推理步骤数: {len(chain_result.reasoning_process.steps) if chain_result.reasoning_process else 0}")
        print(f"   置信度: {chain_result.confidence:.2f}")
    
    # 演示树状思维推理
    print("\n2️⃣ 树状思维推理...")
    tree_task = CognitiveTask(
        id="demo_tree_of_thoughts_001",
        content="分析在家办公的优缺点，并给出是否适合长期实施的建议",
        task_type="reasoning",
        priority="normal",
        complexity="complex",
        metadata={"reasoning_strategy": "tree_of_thoughts"}
    )
    
    tree_result = await cognitive_system.process_task(tree_task)
    print(f"   树状推理结果: {'✅ 成功' if tree_result.success else '❌ 失败'}")
    if tree_result.success:
        print(f"   推理策略: {tree_result.reasoning_process.reasoning_strategy if tree_result.reasoning_process else 'N/A'}")
        print(f"   推理步骤数: {len(tree_result.reasoning_process.steps) if tree_result.reasoning_process else 0}")
    
    print("\n--- 推理系统演示完成 ---\n")


async def demonstrate_skills_system():
    """
    演示技能系统功能
    """
    print("🛠️=== 技能系统演示 ===🛠️\n")
    
    cognitive_system = await initialize_cognitive_system()
    
    # 演示技能注册
    print("1️⃣ 技能注册演示...")
    
    # 创建一个简单的技能定义
    skill_registration_task = CognitiveTask(
        id="demo_skill_register_001",
        content="注册一个简单的数学计算技能，用于执行加法运算",
        task_type="skill_operation",
        priority="normal",
        complexity="simple",
        metadata={
            "operation": "register",
            "skill_id": "math_addition_demo",
            "skill_name": "数学加法技能",
            "skill_description": "执行两个数字的加法运算",
            "skill_code": """
def execute(a: float, b: float) -> dict:
    '''执行加法运算'''
    result = a + b
    return {
        "result": result,
        "expression": f"{a} + {b} = {result}",
        "operation": "addition"
    }
""",
            "skill_inputs": [
                {"name": "a", "type": "number", "description": "第一个数字"},
                {"name": "b", "type": "number", "description": "第二个数字"}
            ],
            "skill_outputs": [
                {"name": "result", "type": "number", "description": "计算结果"},
                {"name": "expression", "type": "string", "description": "运算表达式"}
            ]
        }
    )
    
    skill_register_result = await cognitive_system.process_task(skill_registration_task)
    print(f"   技能注册: {'✅ 成功' if skill_register_result.success else '❌ 失败'}")
    
    # 演示技能执行
    print("\n2️⃣ 技能执行演示...")
    skill_execution_task = CognitiveTask(
        id="demo_skill_execute_001",
        content="执行数学加法技能，计算 15.5 + 24.3",
        task_type="skill_execution",
        priority="normal",
        complexity="simple",
        metadata={
            "skill_id": "math_addition_demo",
            "parameters": {"a": 15.5, "b": 24.3}
        }
    )
    
    skill_execute_result = await cognitive_system.process_task(skill_execution_task)
    print(f"   技能执行: {'✅ 成功' if skill_execute_result.success else '❌ 失败'}")
    if skill_execute_result.success and skill_execute_result.output:
        print(f"   计算结果: {skill_execute_result.output}")
    
    print("\n--- 技能系统演示完成 ---\n")


async def demonstrate_bias_detection():
    """
    演示偏见检测功能
    """
    print("⚖️=== 偏见检测演示 ===⚖️\n")
    
    cognitive_system = await initialize_cognitive_system()
    
    # 创建可能包含偏见的内容
    bias_content = "年轻程序员在技术能力上通常比年长程序员更强，因为年轻人学习能力更强，接受新技术更快。"
    
    print(f"📋 检测内容: {bias_content[:80]}...")
    
    bias_detection_task = CognitiveTask(
        id="demo_bias_detection_001",
        content=bias_content,
        task_type="bias_detection",
        priority="normal",
        complexity="moderate",
        metadata={"analysis_type": "cognitive_bias"}
    )
    
    bias_result = await cognitive_system.process_task(bias_detection_task)
    print(f"   偏见检测: {'✅ 完成' if bias_result.success else '❌ 失败'}")
    
    if bias_result.detected_biases:
        print(f"   检测到 {len(bias_result.detected_biases)} 个偏见:")
        for bias in bias_result.detected_biases:
            print(f"     - {bias.type}: 严重程度 {bias.severity:.2f}")
            print(f"       建议: {bias.suggestion[:60]}...")
    else:
        print("   未检测到显著偏见")
    
    print("\n--- 偏见检测演示完成 ---\n")


async def demonstrate_personalization():
    """
    演示个性化功能
    """
    print("👤=== 个性化功能演示 ===👤\n")
    
    cognitive_system = await initialize_cognitive_system()
    
    # 获取用户认知画像
    print("1️⃣ 获取用户认知画像...")
    profile_task = CognitiveTask(
        id="demo_profile_get_001",
        content="获取用户认知画像",
        task_type="profile_operation",
        priority="normal",
        complexity="simple",
        metadata={"operation": "get", "user_id": "demo_user_001"}
    )
    
    profile_result = await cognitive_system.process_task(profile_task)
    print(f"   画像获取: {'✅ 成功' if profile_result.success else '❌ 失败'}")
    
    if profile_result.success and profile_result.output:
        profile = profile_result.output
        print(f"   推理风格: {profile.get('reasoning_style', 'N/A')}")
        print(f"   决策方式: {profile.get('decision_making', 'N/A')}")
        print(f"   学习偏好: {profile.get('learning_preference', 'N/A')}")
        print(f"   注意力跨度: {profile.get('attention_span', 'N/A')} 分钟")
        
        if profile.get('bias_tendencies'):
            print(f"   偏见倾向: {dict(list(profile['bias_tendencies'].items())[:3])}")
    else:
        print("   用户画像尚未建立（这很正常）")
    
    print("\n2️⃣ 个性化推理演示...")
    
    # 创建一个可以个性化处理的任务
    personal_task = CognitiveTask(
        id="demo_personal_task_001",
        content="分析人工智能对就业市场的影响，考虑技术进步、技能转型和社会适应性等因素",
        task_type="analysis",
        priority="normal",
        complexity="complex",
        metadata={"user_id": "demo_user_001", "personalized": True}
    )
    
    personal_result = await cognitive_system.process_task(personal_task)
    print(f"   个性化分析: {'✅ 成功' if personal_result.success else '❌ 失败'}")
    if personal_result.success:
        print(f"   置信度: {personal_result.confidence:.2f}")
        if personal_result.reasoning_process:
            print(f"   推理策略: {personal_result.reasoning_process.reasoning_strategy}")
    
    print("\n--- 个性化功能演示完成 ---\n")


async def demonstrate_career_assistance():
    """
    演示职业助手功能
    """
    print("💼=== 职业助手演示 ===💼\n")
    
    cognitive_system = await initialize_cognitive_system()
    
    # 演示职位匹配
    print("1️⃣ 职位匹配分析...")
    career_task = CognitiveTask(
        id="demo_career_analysis_001",
        content="分析我的技能和经验，推荐适合的AI相关职位",
        task_type="career_analysis",
        priority="high",
        complexity="moderate",
        metadata={
            "user_profile": {
                "skills": ["Python", "Machine Learning", "NLP", "Data Analysis"],
                "experience_years": 3,
                "education": "Bachelor in Computer Science",
                "location": "Beijing"
            },
            "target_domain": "AI/ML"
        }
    )
    
    career_result = await cognitive_system.process_task(career_task)
    print(f"   职业分析: {'✅ 成功' if career_result.success else '❌ 失败'}")
    if career_result.success and career_result.output:
        print(f"   分析结果: {career_result.output.get('recommendations', 'N/A')[:100]}...")
    
    # 演示简历优化
    print("\n2️⃣ 简历优化建议...")
    resume_task = CognitiveTask(
        id="demo_resume_optimize_001",
        content="基于AI工程师职位要求，优化以下简历内容：负责数据处理和分析工作",
        task_type="resume_optimization",
        priority="normal",
        complexity="moderate",
        metadata={"target_position": "AI Engineer"}
    )
    
    resume_result = await cognitive_system.process_task(resume_task)
    print(f"   简历优化: {'✅ 成功' if resume_result.success else '❌ 失败'}")
    if resume_result.success and resume_result.output:
        print(f"   优化建议: {resume_result.output.get('suggestions', 'N/A')[:100]}...")
    
    print("\n--- 职业助手演示完成 ---\n")


async def demonstrate_advanced_features():
    """
    演示高级功能
    """
    print("🔮=== 高级功能演示 ===🔮\n")
    
    cognitive_system = await initialize_cognitive_system()
    
    # 演示元认知能力
    print("1️⃣ 元认知评估...")
    metacognitive_task = CognitiveTask(
        id="demo_metacognitive_001",
        content="评估以下推理过程的质量和可靠性：AI技术发展迅速，因此所有程序员都应该立即学习AI编程",
        task_type="metacognitive_evaluation",
        priority="normal",
        complexity="moderate",
        metadata={"evaluation_target": "reasoning_process_quality"}
    )
    
    meta_result = await cognitive_system.process_task(metacognitive_task)
    print(f"   元认知评估: {'✅ 完成' if meta_result.success else '❌ 失败'}")
    if meta_result.success:
        print(f"   评估置信度: {meta_result.confidence:.2f}")
        if meta_result.output:
            print(f"   评估结果: {meta_result.output.get('evaluation_summary', 'N/A')[:80]}...")
    
    # 演示多模态推理
    print("\n2️⃣ 多模态推理...")
    multimodal_task = CognitiveTask(
        id="demo_multimodal_001",
        content="结合文本分析和上下文信息，评估当前AI技术趋势并预测未来发展方向",
        task_type="multimodal_analysis",
        priority="high",
        complexity="complex",
        metadata={"analysis_modes": ["text", "context", "prediction"]}
    )
    
    multi_result = await cognitive_system.process_task(multimodal_task)
    print(f"   多模态分析: {'✅ 完成' if multi_result.success else '❌ 失败'}")
    if multi_result.success:
        print(f"   分析置信度: {multi_result.confidence:.2f}")
        if multi_result.reasoning_process:
            print(f"   推理步骤数: {len(multi_result.reasoning_process.steps)}")
    
    print("\n--- 高级功能演示完成 ---\n")


async def demonstrate_system_integration():
    """
    演示系统集成能力
    """
    print("🔗=== 系统集成演示 ===🔗\n")
    
    cognitive_system = await initialize_cognitive_system()
    
    # 演示技能编排
    print("1️⃣ 技能编排演示...")
    
    # 创建一个复杂的任务序列
    orchestration_task = CognitiveTask(
        id="demo_orchestration_001",
        content="执行一个复杂的任务序列：1)分析用户技能 2)匹配职位 3)生成求职建议",
        task_type="orchestration",
        priority="high",
        complexity="complex",
        metadata={
            "sub_tasks": [
                {
                    "task_id": "skill_analysis",
                    "content": "分析用户技能：Python, Machine Learning, NLP",
                    "task_type": "analysis"
                },
                {
                    "task_id": "job_matching", 
                    "content": "匹配AI相关职位",
                    "task_type": "matching",
                    "depends_on": ["skill_analysis"]
                },
                {
                    "task_id": "recommendation",
                    "content": "生成求职建议",
                    "task_type": "generation",
                    "depends_on": ["job_matching"]
                }
            ]
        }
    )
    
    orchestration_result = await cognitive_system.process_task(orchestration_task)
    print(f"   任务编排: {'✅ 成功' if orchestration_result.success else '❌ 失败'}")
    if orchestration_result.success:
        print(f"   执行步骤数: {len(orchestration_result.output.get('execution_steps', [])) if orchestration_result.output else 0}")
        print(f"   整体置信度: {orchestration_result.confidence:.2f}")
    
    print("\n2️⃣ 系统状态监控...")
    
    # 获取系统状态
    status = await cognitive_system.get_system_status()
    print(f"   系统状态: {status.get('status', 'unknown')}")
    print(f"   活跃任务数: {status.get('active_tasks', 0)}")
    print(f"   内存使用: {status.get('memory_usage', 'N/A')}")
    print(f"   处理器负载: {status.get('cpu_usage', 'N/A')}")
    
    print("\n--- 系统集成演示完成 ---\n")


async def run_complete_demo():
    """
    运行完整演示
    """
    print("🚀=== Personal-AI-OS 认知系统完整演示 ===🚀\n")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        # 1. 记忆系统演示
        await demonstrate_memory_system()
        
        # 2. 推理系统演示
        await demonstrate_reasoning_system()
        
        # 3. 技能系统演示
        await demonstrate_skills_system()
        
        # 4. 偏见检测演示
        await demonstrate_bias_detection()
        
        # 5. 个性化功能演示
        await demonstrate_personalization()
        
        # 6. 职业助手演示
        await demonstrate_career_assistance()
        
        # 7. 高级功能演示
        await demonstrate_advanced_features()
        
        # 8. 系统集成演示
        await demonstrate_system_integration()
        
        print("🎉=== 演示完成 ===🎉")
        print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n✨ Personal-AI-OS 认知系统所有功能演示成功！")
        print("系统已准备好为用户提供全方位的认知增强服务～💕")
        
    except Exception as e:
        logger.error(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


async def initialize_cognitive_system():
    """
    初始化认知系统
    """
    from .core import CognitiveSystem
    from .config_manager import get_config_manager
    
    # 获取配置
    config_manager = get_config_manager()
    config = config_manager.get_config()
    
    # 创建认知系统实例
    cognitive_system = CognitiveSystem(config=config)
    
    # 初始化系统
    await cognitive_system.initialize()
    
    return cognitive_system


def run_demo():
    """
    运行演示的便捷函数
    """
    asyncio.run(run_complete_demo())


if __name__ == "__main__":
    run_demo()