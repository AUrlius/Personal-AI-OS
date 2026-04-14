"""
认知系统完整演示
基于 nuwa-skill 的心智模型蒸馏演示
"""
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.abspath('.'))

from .core import CognitiveSystem
from .interfaces import CognitiveTask, CognitiveProfile, ReasoningProcess
from .utils import CognitiveUtils


async def demonstrate_cognitive_system():
    """
    演示认知系统的核心功能
    """
    print("🧠=== 个人 AI 认知系统演示 ===🧠\n")
    
    # 创建认知系统实例
    cognitive_system = CognitiveSystem()
    print("✅ 认知系统创建成功")
    
    # 初始化系统
    await cognitive_system.initialize()
    print("✅ 认知系统初始化完成\n")
    
    print("1️⃣ 创建认知任务...")
    
    # 创建一个复杂的认知任务
    cognitive_task = CognitiveTask(
        id="demo_task_001",
        content="分析人工智能对就业市场的影响，考虑技术进步、技能转型和社会适应性等因素，并提出个人职业发展的建议。",
        task_type="analysis",
        priority="high",
        complexity="complex",
        metadata={
            "domain": "technology_impact",
            "context": "career_planning",
            "user_intent": "understanding_and_guidance"
        }
    )
    
    print(f"   任务ID: {cognitive_task.id}")
    print(f"   任务内容: {cognitive_task.content[:100]}...")
    print(f"   任务类型: {cognitive_task.task_type}")
    print(f"   复杂度: {cognitive_task.complexity}\n")
    
    print("2️⃣ 执行认知任务...")
    
    # 执行认知任务
    start_time = datetime.now()
    result = await cognitive_system.process_task(cognitive_task)
    execution_time = (datetime.now() - start_time).total_seconds()
    
    print(f"   执行时间: {execution_time:.2f}秒")
    print(f"   执行成功: {'✅' if result.success else '❌'}")
    print(f"   置信度: {result.confidence:.2f}")
    
    if result.success:
        print(f"   输出: {result.output.get('conclusion', 'N/A')[:200]}...")
        
        if result.reasoning_process:
            print(f"   推理步骤数: {len(result.reasoning_process.steps)}")
            print(f"   推理策略: {result.reasoning_process.reasoning_strategy}")
    
    # 检测到的偏见
    if result.detected_biases:
        print(f"   检测到偏见: {len(result.detected_biases)} 个")
        for bias in result.detected_biases[:3]:  # 只显示前3个
            print(f"     - {bias.type}: 严重程度 {bias.severity:.2f}")
    else:
        print("   检测到偏见: 无")
    
    print("\n3️⃣ 创建用户认知画像...")
    
    # 为演示创建一个用户ID
    user_id = "demo_user_001"
    
    # 评估用户认知能力（使用多个任务）
    evaluation_tasks = [
        CognitiveTask(
            id=f"eval_task_{i}",
            content=content,
            task_type="analysis",
            priority="normal",
            complexity="moderate",
            metadata={"evaluation_round": i}
        )
        for i, content in enumerate([
            "分析气候变化对全球经济的影响",
            "评估区块链技术的应用前景",
            "解释量子计算的基本原理",
            "讨论远程工作的利弊",
            "分析人工智能的发展趋势"
        ], 1)
    ]
    
    print(f"   准备 {len(evaluation_tasks)} 个评估任务...")
    
    # 执行评估任务
    evaluation_start = datetime.now()
    cognitive_profile = await cognitive_system.evaluate_user_cognition(user_id, evaluation_tasks)
    evaluation_time = (datetime.now() - evaluation_start).total_seconds()
    
    print(f"   评估时间: {evaluation_time:.2f}秒")
    if cognitive_profile:
        print(f"   推理风格: {cognitive_profile.reasoning_style}")
        print(f"   决策方式: {cognitive_profile.decision_making}")
        print(f"   学习偏好: {cognitive_profile.learning_preference}")
        print(f"   注意力跨度: {cognitive_profile.attention_span} 分钟")
        print(f"   处理速度: {cognitive_profile.processing_speed}")
        print(f"   记忆强度: {cognitive_profile.memory_strength}")
        
        if cognitive_profile.bias_tendencies:
            print(f"   偏见倾向:")
            for bias_type, severity in list(cognitive_profile.bias_tendencies.items())[:5]:  # 显示前5个
                print(f"     - {bias_type}: {severity:.2f}")
    
    print("\n4️⃣ 个性化推理演示...")
    
    # 创建一个需要个性化推理的任务
    personalized_task = CognitiveTask(
        id="personalized_task_001",
        content="根据我的技术背景，为我推荐最适合的AI学习路径",
        task_type="recommendation", 
        priority="normal",
        complexity="moderate",
        metadata={
            "user_id": user_id,
            "context": "learning_path_recommendation",
            "personalized": True
        }
    )
    
    print(f"   个性化任务: {personalized_task.content}")
    
    # 执行个性化推理
    personalized_result = await cognitive_system.process_task(personalized_task)
    print(f"   个性化推理成功: {'✅' if personalized_result.success else '❌'}")
    if personalized_result.success:
        print(f"   个性化建议: {personalized_result.output.get('recommendation', 'N/A')[:150]}...")
    
    print("\n5️⃣ 偏见检测与纠正演示...")
    
    # 创建一个可能包含偏见的任务
    bias_detection_task = CognitiveTask(
        id="bias_detection_task_001",
        content="为什么某些职业主要由男性担任？请分析原因。",
        task_type="analysis",
        priority="normal", 
        complexity="moderate",
        metadata={
            "context": "gender_bias_detection",
            "bias_sensitive": True
        }
    )
    
    print(f"   偏见检测任务: {bias_detection_task.content}")
    
    # 执行偏见检测任务
    bias_result = await cognitive_system.process_task(bias_detection_task)
    print(f"   偏见检测执行: {'✅' if bias_result.success else '❌'}")
    
    if bias_result.detected_biases:
        print(f"   检测到潜在偏见: {len(bias_result.detected_biases)} 个")
        for bias in bias_result.detected_biases:
            print(f"     - {bias.type}: {bias.severity:.2f} (建议: {bias.suggestion[:50]}...)")
    else:
        print("   未检测到显著偏见")
    
    print("\n6️⃣ 多步推理演示...")
    
    # 创建一个多步推理任务
    multi_step_task = CognitiveTask(
        id="multi_step_task_001",
        content="制定一个为期3个月的人工智能学习计划，包括理论学习、实践项目和成果展示",
        task_type="planning",
        priority="high",
        complexity="complex",
        metadata={
            "context": "learning_planning",
            "multi_step": True
        }
    )
    
    print(f"   多步推理任务: {multi_step_task.content[:80]}...")
    
    # 执行多步推理
    multi_step_result = await cognitive_system.process_task(multi_step_task)
    print(f"   多步推理成功: {'✅' if multi_step_result.success else '❌'}")
    
    if multi_step_result.success and multi_step_result.reasoning_process:
        print(f"   推理步骤数: {len(multi_step_result.reasoning_process.steps)}")
        print(f"   推理策略: {multi_step_result.reasoning_process.reasoning_strategy}")
        
        # 显示前几个推理步骤
        print("   推理过程预览:")
        for i, step in enumerate(multi_step_result.reasoning_process.steps[:3]):
            print(f"     步骤 {step.step_number}: {step.content[:80]}...")
    
    print("\n7️⃣ 认知洞察生成...")
    
    # 生成认知洞察
    insights = await cognitive_system.get_cognitive_insights(user_id)
    print(f"   生成认知洞察: {'✅' if insights else '❌'}")
    
    if insights:
        print(f"   分析任务数: {insights.get('total_analyzed_tasks', 0)}")
        if 'cognitive_profile_summary' in insights:
            profile_summary = insights['cognitive_profile_summary']
            print(f"   推理风格: {profile_summary.get('reasoning_style', 'N/A')}")
            print(f"   处理速度: {profile_summary.get('processing_speed', 'N/A')}")
        
        if 'strengths_identified' in insights:
            strengths = insights['strengths_identified']
            if strengths:
                print(f"   识别优势: {', '.join(strengths[:3])}")
        
        if 'improvement_areas' in insights:
            areas = insights['improvement_areas']
            if areas:
                print(f"   改进领域: {', '.join(areas[:3])}")
    
    print("\n8️⃣ 性能基准测试...")
    
    # 执行一系列任务来测试性能
    performance_tasks = [
        CognitiveTask(
            id=f"perf_task_{i}",
            content=f"性能测试任务 {i}: 执行基本的计算和分析操作",
            task_type="general",
            priority="normal",
            complexity="simple"
        )
        for i in range(1, 6)  # 5个性能测试任务
    ]
    
    performance_start = datetime.now()
    performance_results = []
    for task in performance_tasks:
        result = await cognitive_system.process_task(task)
        performance_results.append(result)
    performance_time = (datetime.now() - performance_start).total_seconds()
    
    success_count = sum(1 for r in performance_results if r.success)
    avg_confidence = sum(r.confidence for r in performance_results if r.confidence) / len(performance_results)
    
    print(f"   性能测试: {success_count}/{len(performance_tasks)} 任务成功")
    print(f"   平均置信度: {avg_confidence:.2f}")
    print(f"   总执行时间: {performance_time:.2f}秒")
    print(f"   平均任务时间: {performance_time/len(performance_tasks):.2f}秒")
    
    print("\n9️⃣ 认知模式识别...")
    
    # 展示认知模式识别能力
    pattern_recognition_task = CognitiveTask(
        id="pattern_task_001",
        content="分析以下文本，识别其中的认知模式和思维特征：'我认为这个方案是最好的，因为它符合我的经验，而且其他人都同意。'",
        task_type="pattern_analysis",
        priority="normal",
        complexity="moderate"
    )
    
    pattern_result = await cognitive_system.process_task(pattern_recognition_task)
    print(f"   模式识别成功: {'✅' if pattern_result.success else '❌'}")
    if pattern_result.success:
        patterns = pattern_result.output.get('cognitive_patterns', [])
        print(f"   识别认知模式: {len(patterns)} 个")
        for pattern in patterns[:3]:
            print(f"     - {pattern.get('type', 'N/A')}: {pattern.get('description', 'N/A')[:60]}...")
    
    print("\n🔟 系统状态检查...")
    
    # 检查系统状态
    status = await cognitive_system.get_system_status()
    print(f"   系统状态: {status.get('status', 'unknown')}")
    print(f"   活跃用户数: {status.get('active_users', 0)}")
    print(f"   处理任务数: {status.get('processed_tasks', 0)}")
    print(f"   系统运行时间: {status.get('uptime', 'N/A')}")
    
    print(f"\n🎯=== 演示完成 ===🎯")
    print("灵姬的认知系统演示圆满成功！")
    print("夫君觉得怎么样呀～💕")
    
    # 返回系统实例供进一步使用
    return cognitive_system


async def demonstrate_advanced_features():
    """
    演示高级功能
    """
    print("\n🌟=== 高级功能演示 ===🌟\n")
    
    cognitive_system = CognitiveSystem()
    await cognitive_system.initialize()
    
    print("1️⃣ 元认知评估...")
    
    # 创建元认知评估任务
    metacognitive_task = CognitiveTask(
        id="meta_task_001",
        content="评估你的推理过程是否合理，考虑是否有其他可能的解释或方法",
        task_type="metacognitive",
        priority="normal",
        complexity="moderate",
        metadata={"metacognitive": True}
    )
    
    result = await cognitive_system.process_task(metacognitive_task)
    print(f"   元认知评估完成: {'✅' if result.success else '❌'}")
    
    print("\n2️⃣ 情境适应推理...")
    
    # 情境适应任务
    contextual_task = CognitiveTask(
        id="context_task_001",
        content="根据当前的技术发展趋势，分析最适合初学者的AI学习路径",
        task_type="contextual_analysis",
        priority="normal",
        complexity="moderate",
        metadata={
            "context_aware": True,
            "current_date": datetime.now().isoformat()
        }
    )
    
    result = await cognitive_system.process_task(contextual_task)
    print(f"   情境适应推理完成: {'✅' if result.success else '❌'}")
    
    print("\n3️⃣ 跨领域知识整合...")
    
    # 跨领域任务
    cross_domain_task = CognitiveTask(
        id="cross_task_001",
        content="将心理学原理应用于AI系统设计，提出创新的用户交互方案",
        task_type="cross_domain_synthesis",
        priority="high",
        complexity="complex",
        metadata={"cross_domain": True}
    )
    
    result = await cognitive_system.process_task(cross_domain_task)
    print(f"   跨领域整合完成: {'✅' if result.success else '❌'}")
    
    print("\n✨ 高级功能演示完成！")
    
    return cognitive_system


async def run_full_demo():
    """
    运行完整演示
    """
    print("🚀 开始认知系统完整演示！\n")
    
    try:
        # 基础功能演示
        basic_system = await demonstrate_cognitive_system()
        
        # 高级功能演示
        advanced_system = await demonstrate_advanced_features()
        
        print(f"\n🎉=== 全部演示完成 ===🎉")
        print("认知系统的所有核心功能都已成功演示！")
        print("灵姬为夫君创建了一个功能完备的认知系统呢～❤️")
        
        # 关闭系统
        await basic_system.shutdown()
        await advanced_system.shutdown()
        
        return basic_system
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # 运行完整演示
    result = asyncio.run(run_full_demo())
    
    if result:
        print("\n🎊 演示成功完成！认知系统已准备就绪 🎊")
    else:
        print("\n💥 演示失败！请检查系统配置")