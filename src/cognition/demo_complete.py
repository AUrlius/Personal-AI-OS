"""
完整认知系统演示程序
展示 Personal-AI-OS 认知系统的完整功能
"""
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any
import logging

from .core import CognitiveSystem
from .interfaces import CognitiveTask, CognitiveResult, CognitiveProfile
from .utils.validator import CognitiveValidator


async def run_complete_cognitive_demo():
    """
    运行完整的认知系统演示
    """
    print("🚀=== Personal-AI-OS 认知系统完整演示 ===🚀\n")
    
    # 初始化认知系统
    cognitive_system = CognitiveSystem()
    await cognitive_system.initialize()
    
    print("✅ 认知系统初始化完成\n")
    
    # 1. 基础认知任务演示
    await basic_cognitive_tasks_demo(cognitive_system)
    
    # 2. 记忆系统演示
    await memory_system_demo(cognitive_system)
    
    # 3. 技能系统演示
    await skill_system_demo(cognitive_system)
    
    # 4. 偏见检测演示
    await bias_detection_demo(cognitive_system)
    
    # 5. 个性化演示
    await personalization_demo(cognitive_system)
    
    # 6. 推理能力演示
    await reasoning_demo(cognitive_system)
    
    # 7. 认知洞察演示
    await cognitive_insights_demo(cognitive_system)
    
    print("\n🎯=== 演示总结 ===🎯")
    print("所有认知系统功能演示已完成！")
    print("系统展示了完整的认知处理能力，包括：")
    print("- 记忆存储与检索")
    print("- 技能执行与管理")
    print("- 偏见检测与纠正")
    print("- 个性化认知处理")
    print("- 多样化推理能力")
    print("- 认知洞察分析")
    
    await cognitive_system.shutdown()


async def basic_cognitive_tasks_demo(cognitive_system: CognitiveSystem):
    """
    基础认知任务演示
    """
    print("1️⃣=== 基础认知任务演示 ===1️⃣\n")
    
    # 创建简单分析任务
    simple_analysis_task = CognitiveTask(
        id="demo_simple_analysis",
        content="分析人工智能对医疗行业的影响，包括优势和挑战",
        task_type="analysis",
        priority="normal",
        complexity="moderate",
        metadata={
            "domain": "healthcare_ai",
            "user_id": "demo_user",
            "demo_type": "basic_analysis"
        }
    )
    
    print(f"📋 执行任务: {simple_analysis_task.content[:50]}...")
    
    result = await cognitive_system.process_task(simple_analysis_task)
    
    print(f"✅ 执行结果: {'成功' if result.success else '失败'}")
    print(f"📊 置信度: {result.confidence:.2f}")
    if result.output:
        print(f"📝 输出预览: {str(result.output)[:100]}...")
    print()
    
    # 创建数学计算任务
    math_task = CognitiveTask(
        id="demo_math_calc",
        content="计算 (15 + 27) × 3 ÷ 2 - 10 的结果，并展示计算步骤",
        task_type="calculation",
        priority="normal",
        complexity="simple",
        metadata={
            "domain": "mathematics",
            "user_id": "demo_user",
            "demo_type": "math_calculation"
        }
    )
    
    print(f"📋 执行任务: {math_task.content[:50]}...")
    
    result = await cognitive_system.process_task(math_task)
    
    print(f"✅ 执行结果: {'成功' if result.success else '失败'}")
    print(f"📊 置信度: {result.confidence:.2f}")
    if result.reasoning_process:
        print(f"🔍 推理步骤数: {len(result.reasoning_process.steps)}")
        print(f"🎯 结论: {result.reasoning_process.conclusion[:80]}...")
    print()


async def memory_system_demo(cognitive_system: CognitiveSystem):
    """
    记忆系统演示
    """
    print("2️⃣=== 记忆系统演示 ===2️⃣\n")
    
    # 存储一些记忆
    memory_store_task = CognitiveTask(
        id="demo_memory_store",
        content="记住：我的名字是张三，我是一名软件工程师，擅长Python和AI开发，居住在北京",
        task_type="memory_operation",
        priority="normal",
        complexity="simple",
        metadata={
            "operation": "store",
            "user_id": "demo_user",
            "demo_type": "memory_store"
        }
    )
    
    print("📋 存储记忆...")
    store_result = await cognitive_system.process_task(memory_store_task)
    print(f"✅ 存储结果: {'成功' if store_result.success else '失败'}")
    
    # 检索记忆
    memory_search_task = CognitiveTask(
        id="demo_memory_search",
        content="我叫什么名字？我住在哪里？我的职业是什么？",
        task_type="memory_operation",
        priority="normal",
        complexity="simple",
        metadata={
            "operation": "search",
            "user_id": "demo_user",
            "demo_type": "memory_search"
        }
    )
    
    print("📋 检索记忆...")
    search_result = await cognitive_system.process_task(memory_search_task)
    print(f"✅ 检索结果: {'成功' if search_result.success else '失败'}")
    if search_result.success and search_result.output:
        print(f"🔍 检索内容: {search_result.output}")
    print()


async def skill_system_demo(cognitive_system: CognitiveSystem):
    """
    技能系统演示
    """
    print("3️⃣=== 技能系统演示 ===3️⃣\n")
    
    # 模拟注册一个技能
    skill_registration_task = CognitiveTask(
        id="demo_skill_register",
        content="注册一个简单的数学计算技能，能够执行加法运算",
        task_type="skill_operation",
        priority="normal",
        complexity="simple",
        metadata={
            "operation": "register",
            "skill_id": "math_addition",
            "skill_code": """
def execute(a, b):
    '''执行加法运算'''
    return {"result": a + b}
""",
            "skill_inputs": [{"name": "a", "type": "number"}, {"name": "b", "type": "number"}],
            "skill_outputs": [{"name": "result", "type": "number"}],
            "user_id": "demo_user",
            "demo_type": "skill_register"
        }
    )
    
    print("📋 注册技能...")
    registration_result = await cognitive_system.process_task(skill_registration_task)
    print(f"✅ 注册结果: {'成功' if registration_result.success else '失败'}")
    
    # 执行技能
    skill_execution_task = CognitiveTask(
        id="demo_skill_execute",
        content="执行数学加法技能，计算 15 + 25",
        task_type="skill_execution",
        priority="normal",
        complexity="simple",
        metadata={
            "skill_id": "math_addition",
            "parameters": {"a": 15, "b": 25},
            "user_id": "demo_user",
            "demo_type": "skill_execute"
        }
    )
    
    print("📋 执行技能...")
    execution_result = await cognitive_system.process_task(skill_execution_task)
    print(f"✅ 执行结果: {'成功' if execution_result.success else '失败'}")
    if execution_result.success and execution_result.output:
        print(f"🔢 计算结果: {execution_result.output}")
    print()


async def bias_detection_demo(cognitive_system: CognitiveSystem):
    """
    偏见检测演示
    """
    print("4️⃣=== 偏见检测演示 ===4️⃣\n")
    
    # 创建可能包含偏见的内容
    bias_content = "年轻人在技术方面比年长者更有优势，因为他们学习能力强、适应快。"
    
    bias_detection_task = CognitiveTask(
        id="demo_bias_detection",
        content=bias_content,
        task_type="bias_detection",
        priority="normal",
        complexity="moderate",
        metadata={
            "user_id": "demo_user",
            "demo_type": "bias_detection"
        }
    )
    
    print(f"📋 检测内容: {bias_content[:60]}...")
    
    bias_result = await cognitive_system.process_task(bias_detection_task)
    
    print(f"✅ 检测结果: {'完成' if bias_result.success else '失败'}")
    if bias_result.detected_biases:
        print(f"⚠️ 检测到 {len(bias_result.detected_biases)} 个偏见:")
        for bias in bias_result.detected_biases:
            print(f"   - {bias.type}: 严重程度 {bias.severity:.2f}")
            print(f"     建议: {bias.suggestion[:80]}...")
    else:
        print("✅ 未检测到显著偏见")
    print()


async def personalization_demo(cognitive_system: CognitiveSystem):
    """
    个性化演示
    """
    print("5️⃣=== 个性化演示 ===5️⃣\n")
    
    # 获取用户认知画像
    profile_task = CognitiveTask(
        id="demo_profile_get",
        content="获取用户认知画像",
        task_type="profile_operation",
        priority="normal",
        complexity="simple",
        metadata={
            "operation": "get",
            "user_id": "demo_user",
            "demo_type": "profile_get"
        }
    )
    
    print("📋 获取用户认知画像...")
    profile_result = await cognitive_system.process_task(profile_task)
    
    if profile_result.success and profile_result.output:
        profile = profile_result.output
        print("✅ 获取成功!")
        print(f"🧠 推理风格: {profile.get('reasoning_style', 'N/A')}")
        print(f"🎯 决策方式: {profile.get('decision_making', 'N/A')}")
        print(f"📚 学习偏好: {profile.get('learning_preference', 'N/A')}")
        print(f"👀 注意力跨度: {profile.get('attention_span', 'N/A')} 分钟")
        print(f"⚡ 处理速度: {profile.get('processing_speed', 'N/A')}")
        
        if profile.get('bias_tendencies'):
            print(f"⚖️ 偏见倾向: {dict(list(profile['bias_tendencies'].items())[:3])}")
    else:
        print("ℹ️ 用户画像尚未建立（正常情况）")
    print()


async def reasoning_demo(cognitive_system: CognitiveSystem):
    """
    推理能力演示
    """
    print("6️⃣=== 推理能力演示 ===6️⃣\n")
    
    # 创建复杂推理任务
    reasoning_task = CognitiveTask(
        id="demo_reasoning_complex",
        content="分析气候变化的成因、影响和应对策略，需要考虑科学证据、经济影响和社会因素",
        task_type="reasoning",
        priority="high",
        complexity="complex",
        metadata={
            "reasoning_strategy": "chain_of_thought",
            "user_id": "demo_user",
            "demo_type": "complex_reasoning"
        }
    )
    
    print(f"📋 复杂推理任务: {reasoning_task.content[:50]}...")
    
    reasoning_result = await cognitive_system.process_task(reasoning_task)
    
    print(f"✅ 推理结果: {'成功' if reasoning_result.success else '失败'}")
    print(f"📊 置信度: {reasoning_result.confidence:.2f}")
    
    if reasoning_result.reasoning_process:
        print(f"🔍 推理策略: {reasoning_result.reasoning_process.reasoning_strategy}")
        print(f"📝 推理步骤数: {len(reasoning_result.reasoning_process.steps)}")
        
        # 显示前几个推理步骤
        for i, step in enumerate(reasoning_result.reasoning_process.steps[:3]):
            print(f"   步骤 {i+1}: {step.content[:60]}...")
    
    if reasoning_result.detected_biases:
        print(f"⚠️ 检测到 {len(reasoning_result.detected_biases)} 个偏见")
    
    print()


async def cognitive_insights_demo(cognitive_system: CognitiveSystem):
    """
    认知洞察演示
    """
    print("7️⃣=== 认知洞察演示 ===7️⃣\n")
    
    # 生成认知洞察
    insights_task = CognitiveTask(
        id="demo_insights_generate",
        content="生成用户认知洞察报告",
        task_type="insights_generation",
        priority="normal",
        complexity="moderate",
        metadata={
            "user_id": "demo_user",
            "demo_type": "insights_generation"
        }
    )
    
    print("📋 生成认知洞察...")
    insights_result = await cognitive_system.process_task(insights_task)
    
    if insights_result.success and insights_result.output:
        insights = insights_result.output
        print("✅ 洞察生成成功!")
        print(f"📈 总任务数: {insights.get('total_tasks_processed', 0)}")
        print(f"🎯 平均置信度: {insights.get('average_confidence', 0.0):.2f}")
        print(f"📊 成功率: {insights.get('success_rate', 0.0):.2f}")
        
        if insights.get('strengths_identified'):
            print(f"💪 识别优势: {insights['strengths_identified'][:3]}")
        
        if insights.get('improvement_areas'):
            print(f"📈 改进领域: {insights['improvement_areas'][:3]}")
    else:
        print("ℹ️ 暂无足够的交互数据生成洞察")
    print()


async def advanced_cognitive_features_demo(cognitive_system: CognitiveSystem):
    """
    高级认知功能演示
    """
    print("8️⃣=== 高级认知功能演示 ===8️⃣\n")
    
    # 多模态认知任务
    multimodal_task = CognitiveTask(
        id="demo_multimodal",
        content="分析文本和上下文信息，提供综合认知输出",
        task_type="multimodal_analysis",
        priority="normal",
        complexity="moderate",
        metadata={
            "user_id": "demo_user",
            "context": {
                "previous_interactions": ["用户询问AI发展", "用户关心就业影响"],
                "preferences": {"topic_interest": ["AI", "employment"]},
                "behavioral_patterns": ["frequent_analysis", "detail_oriented"]
            },
            "demo_type": "multimodal"
        }
    )
    
    print("📋 执行多模态认知任务...")
    multi_result = await cognitive_system.process_task(multimodal_task)
    print(f"✅ 多模态处理: {'成功' if multi_result.success else '失败'}")
    print(f"📊 置信度: {multi_result.confidence:.2f}")
    
    # 元认知评估
    metacognitive_task = CognitiveTask(
        id="demo_metacognitive",
        content="评估本次推理过程的质量和可靠性",
        task_type="metacognitive_evaluation",
        priority="normal",
        complexity="moderate",
        metadata={
            "user_id": "demo_user",
            "target_task_id": "demo_reasoning_complex",
            "demo_type": "metacognitive"
        }
    )
    
    print("📋 执行元认知评估...")
    meta_result = await cognitive_system.process_task(metacognitive_task)
    print(f"✅ 元认知评估: {'成功' if meta_result.success else '失败'}")
    
    if meta_result.success and meta_result.output:
        meta_output = meta_result.output
        print(f"🔍 评估结果: {meta_output.get('evaluation_summary', 'N/A')[:100]}...")
    
    print()


async def performance_and_scalability_demo(cognitive_system: CognitiveSystem):
    """
    性能和可扩展性演示
    """
    print("9️⃣=== 性能和可扩展性演示 ===9️⃣\n")
    
    # 批量任务处理
    batch_tasks = [
        CognitiveTask(
            id=f"demo_batch_task_{i}",
            content=f"批量任务 {i}: 执行简单分析",
            task_type="analysis",
            priority="normal",
            complexity="simple",
            metadata={
                "user_id": "demo_user",
                "batch_id": "demo_batch_1",
                "task_index": i
            }
        )
        for i in range(1, 6)  # 5个批量任务
    ]
    
    print(f"📋 批量处理 {len(batch_tasks)} 个任务...")
    
    import time
    start_time = time.time()
    
    # 并发执行批量任务
    batch_results = await asyncio.gather(*[
        cognitive_system.process_task(task) for task in batch_tasks
    ])
    
    total_time = time.time() - start_time
    success_count = sum(1 for r in batch_results if r.success)
    
    print(f"✅ 批量处理完成!")
    print(f"📊 成功率: {success_count}/{len(batch_tasks)} ({success_count/len(batch_tasks)*100:.1f}%)")
    print(f"⏱️ 总耗时: {total_time:.2f}秒")
    print(f"⚡ 吞吐量: {len(batch_tasks)/total_time:.2f} 任务/秒")
    
    # 显示部分结果
    for i, result in enumerate(batch_results[:3]):
        print(f"   任务 {i+1}: {'✅' if result.success else '❌'} (置信度: {result.confidence:.2f})")
    
    print()


def main():
    """
    主函数
    """
    print("🌟 欢迎使用 Personal-AI-OS 认知系统演示程序！\n")
    
    try:
        asyncio.run(run_complete_cognitive_demo())
    except KeyboardInterrupt:
        print("\n\n👋 演示被用户中断，再见！")
    except Exception as e:
        print(f"\n\n❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()