"""
认知系统使用示例
展示如何在实际应用中使用认知系统
"""
import asyncio
from datetime import datetime
from typing import Dict, List, Any
import json

from .core import CognitiveSystem
from .interfaces import CognitiveTask, CognitiveProfile, ReasoningProcess
from .utils import CognitiveUtils


async def example_basic_usage():
    """
    基础使用示例
    """
    print("🧠=== 认知系统基础使用示例 ===🧠\n")
    
    # 1. 创建认知系统实例
    cognitive_system = CognitiveSystem()
    await cognitive_system.initialize()
    print("✅ 认知系统初始化完成")
    
    # 2. 创建一个简单的认知任务
    simple_task = CognitiveTask(
        id="simple_task_001",
        content="计算 25 × 17 + 89 的结果",
        task_type="mathematical",
        priority="normal",
        complexity="simple",
        metadata={"domain": "mathematics", "purpose": "calculation"}
    )
    
    print(f"📋 创建任务: {simple_task.content}")
    
    # 3. 执行任务
    result = await cognitive_system.process_task(simple_task)
    
    print(f"✅ 任务执行结果: {result.success}")
    print(f"📊 输出: {result.output}")
    print(f"📈 置信度: {result.confidence:.2f}")
    
    # 4. 查看推理过程
    if result.reasoning_process:
        print(f"🔍 推理步骤数: {len(result.reasoning_process.steps)}")
        for step in result.reasoning_process.steps:
            print(f"   步骤 {step.step_number}: {step.content[:80]}...")
    
    print("\n--- 基础使用示例完成 ---\n")


async def example_complex_reasoning():
    """
    复杂推理示例
    """
    print("🧠=== 复杂推理示例 ===🧠\n")
    
    cognitive_system = CognitiveSystem()
    await cognitive_system.initialize()
    
    # 创建复杂分析任务
    complex_task = CognitiveTask(
        id="complex_analysis_001",
        content="""分析当前人工智能技术发展趋势，重点关注以下几个方面：
        1. 大语言模型的发展现状和局限性
        2. 多模态AI的突破和应用前景
        3. AI安全和伦理问题的挑战
        4. 对个人职业发展的影响和建议""",
        task_type="analysis",
        priority="high",
        complexity="complex",
        metadata={
            "domain": "technology_analysis",
            "depth": "comprehensive",
            "output_format": "structured_analysis"
        }
    )
    
    print(f"📋 复杂分析任务: {complex_task.content[:100]}...")
    
    # 执行复杂推理
    start_time = datetime.now()
    result = await cognitive_system.process_task(complex_task)
    execution_time = (datetime.now() - start_time).total_seconds()
    
    print(f"✅ 推理完成，耗时: {execution_time:.2f}秒")
    print(f"📊 置信度: {result.confidence:.2f}")
    
    if result.success:
        analysis_output = result.output
        print(f"📝 分析结果概要: {analysis_output.get('conclusion', 'N/A')[:200]}...")
        
        # 显示推理过程
        if result.reasoning_process:
            print(f"🔍 推理策略: {result.reasoning_process.reasoning_strategy}")
            print(f"📈 推理步骤数: {len(result.reasoning_process.steps)}")
            
            # 显示关键推理步骤
            for i, step in enumerate(result.reasoning_process.steps[-3:], 1):  # 显示最后3个步骤
                print(f"   推理步骤 {i}: {step.content[:100]}...")
    
    # 检测偏见
    if result.detected_biases:
        print(f"⚠️ 检测到偏见: {len(result.detected_biases)} 个")
        for bias in result.detected_biases:
            print(f"   - {bias.type}: 严重程度 {bias.severity:.2f}")
    
    print("\n--- 复杂推理示例完成 ---\n")


async def example_personalization():
    """
    个性化示例
    """
    print("🧠=== 个性化认知示例 ===🧠\n")
    
    cognitive_system = CognitiveSystem()
    await cognitive_system.initialize()
    
    user_id = "example_user_001"
    
    # 1. 创建个性化任务
    personal_task = CognitiveTask(
        id="personal_task_001",
        content="根据我的技术背景，为我制定一份AI学习计划",
        task_type="planning",
        priority="normal",
        complexity="moderate",
        metadata={
            "user_id": user_id,
            "context": "learning_planning",
            "personalized": True
        }
    )
    
    print(f"📋 个性化任务: {personal_task.content}")
    
    # 2. 执行个性化推理
    result = await cognitive_system.process_task(personal_task)
    
    print(f"✅ 个性化推理完成: {'✅' if result.success else '❌'}")
    if result.success:
        print(f"📝 个性化建议: {result.output.get('recommendation', 'N/A')[:150]}...")
    
    # 3. 获取用户认知画像
    profile = await cognitive_system.get_user_profile(user_id)
    if profile:
        print(f"👤 用户认知画像:")
        print(f"   推理风格: {profile.reasoning_style}")
        print(f"   决策方式: {profile.decision_making}")
        print(f"   学习偏好: {profile.learning_preference}")
        print(f"   注意力跨度: {profile.attention_span}分钟")
        print(f"   处理速度: {profile.processing_speed}")
        
        if profile.bias_tendencies:
            print(f"   偏见倾向: {dict(list(profile.bias_tendencies.items())[:3])}")
    
    print("\n--- 个性化示例完成 ---\n")


async def example_bias_detection():
    """
    偏见检测示例
    """
    print("🧠=== 偏见检测示例 ===🧠\n")
    
    cognitive_system = CognitiveSystem()
    await cognitive_system.initialize()
    
    # 创建可能包含偏见的任务
    bias_task = CognitiveTask(
        id="bias_detection_001",
        content="分析为什么某些科技公司的女性员工比例较低？",
        task_type="analysis",
        priority="normal",
        complexity="moderate",
        metadata={
            "context": "gender_bias_analysis",
            "bias_sensitive": True
        }
    )
    
    print(f"📋 偏见检测任务: {bias_task.content}")
    
    # 执行任务并检测偏见
    result = await cognitive_system.process_task(bias_task)
    
    print(f"✅ 偏见检测执行: {'✅' if result.success else '❌'}")
    
    # 检查检测到的偏见
    if result.detected_biases:
        print(f"⚠️ 检测到偏见: {len(result.detected_biases)} 个")
        for bias in result.detected_biases:
            print(f"   类型: {bias.type}")
            print(f"   严重程度: {bias.severity:.2f}")
            print(f"   建议: {bias.suggestion[:100]}...")
            print(f"   证据: {bias.evidence[:2]}...")  # 只显示前2个证据
            print()
    else:
        print("✅ 未检测到显著偏见")
    
    # 查看推理过程中的偏见纠正
    if result.reasoning_process and result.reasoning_process.bias_indicators:
        print(f"🔄 偏见纠正步骤: {len(result.reasoning_process.bias_indicators)} 个")
        for indicator in result.reasoning_process.bias_indicators:
            print(f"   - {indicator}")
    
    print("\n--- 偏见检测示例完成 ---\n")


async def example_memory_integration():
    """
    记忆集成示例
    """
    print("🧠=== 记忆集成示例 ===🧠\n")
    
    cognitive_system = CognitiveSystem()
    await cognitive_system.initialize()
    
    # 1. 存储一些记忆
    memory_task = CognitiveTask(
        id="memory_store_001",
        content="记住：我偏好使用Python进行AI开发，擅长数据科学，对深度学习有一定了解",
        task_type="memory_operation",
        priority="normal",
        complexity="simple",
        metadata={
            "user_id": "memory_user_001",
            "operation": "store",
            "memory_type": "preference"
        }
    )
    
    print("📋 存储记忆...")
    result = await cognitive_system.process_task(memory_task)
    print(f"✅ 记忆存储: {'✅' if result.success else '❌'}")
    
    # 2. 查询记忆
    query_task = CognitiveTask(
        id="memory_query_001",
        content="关于AI开发，我偏好使用什么编程语言？",
        task_type="memory_operation",
        priority="normal",
        complexity="simple",
        metadata={
            "user_id": "memory_user_001",
            "operation": "query",
            "context": "ai_preferences"
        }
    )
    
    print("📋 查询记忆...")
    result = await cognitive_system.process_task(query_task)
    print(f"✅ 记忆查询: {'✅' if result.success else '❌'}")
    if result.success:
        print(f"🔍 查询结果: {result.output.get('retrieved_content', 'N/A')}")
    
    # 3. 记忆关联分析
    analysis_task = CognitiveTask(
        id="memory_analysis_001",
        content="基于我的AI偏好和技术背景，推荐适合的学习路径",
        task_type="analysis",
        priority="normal",
        complexity="moderate",
        metadata={
            "user_id": "memory_user_001",
            "context": "learning_recommendation",
            "use_memory": True
        }
    )
    
    print("📋 基于记忆的分析...")
    result = await cognitive_system.process_task(analysis_task)
    print(f"✅ 基于记忆的分析: {'✅' if result.success else '❌'}")
    if result.success:
        print(f"🎯 个性化推荐: {result.output.get('recommendation', 'N/A')[:200]}...")
    
    print("\n--- 记忆集成示例完成 ---\n")


async def example_skill_integration():
    """
    技能集成示例
    """
    print("🧠=== 技能集成示例 ===🧠\n")
    
    cognitive_system = CognitiveSystem()
    await cognitive_system.initialize()
    
    # 创建需要使用技能的任务
    skill_task = CognitiveTask(
        id="skill_task_001",
        content="帮我分析这份简历，提取关键技能并给出优化建议",
        task_type="analysis",
        priority="normal",
        complexity="moderate",
        metadata={
            "context": "resume_analysis",
            "required_skills": ["text_analysis", "skill_extraction", "recommendation"]
        }
    )
    
    print(f"📋 技能集成任务: {skill_task.content}")
    
    # 执行需要技能集成的任务
    result = await cognitive_system.process_task(skill_task)
    
    print(f"✅ 技能集成执行: {'✅' if result.success else '❌'}")
    if result.success:
        output = result.output
        print(f"📊 技能分析结果:")
        print(f"   提取技能数: {len(output.get('extracted_skills', []))}")
        print(f"   建议数: {len(output.get('recommendations', []))}")
        
        if output.get('extracted_skills'):
            print(f"   关键技能: {', '.join(output['extracted_skills'][:5])}...")
        
        if output.get('recommendations'):
            print(f"   优化建议: {output['recommendations'][0][:100]}...")
    
    # 查看技能使用情况
    if result.resources_used:
        skills_used = result.resources_used.get('skills_used', [])
        if skills_used:
            print(f"🔧 使用技能: {', '.join(skills_used)}")
    
    print("\n--- 技能集成示例完成 ---\n")


async def example_multimodal_reasoning():
    """
    多模态推理示例
    """
    print("🧠=== 多模态推理示例 ===🧠\n")
    
    cognitive_system = CognitiveSystem()
    await cognitive_system.initialize()
    
    # 创建多模态任务（虽然是模拟，但展示架构设计）
    multimodal_task = CognitiveTask(
        id="multimodal_task_001",
        content="分析一段关于AI技术发展的视频内容，提取关键信息并生成总结",
        task_type="multimodal_analysis",
        priority="high",
        complexity="complex",
        metadata={
            "context": "video_analysis",
            "modalities": ["text", "audio", "visual"],
            "output_type": "structured_summary"
        }
    )
    
    print(f"📋 多模态任务: {multimodal_task.content}")
    
    # 执行多模态推理（模拟）
    result = await cognitive_system.process_task(multimodal_task)
    
    print(f"✅ 多模态推理: {'✅' if result.success else '❌'}")
    if result.success:
        output = result.output
        print(f"📊 分析结果:")
        print(f"   信息维度: {output.get('modalities_analyzed', [])}")
        print(f"   关键信息数: {len(output.get('key_insights', []))}")
        
        if output.get('key_insights'):
            print(f"   关键洞察: {output['key_insights'][0][:150]}...")
    
    print("\n--- 多模态推理示例完成 ---\n")


async def example_meta_cognition():
    """
    元认知示例
    """
    print("🧠=== 元认知示例 ===🧠\n")
    
    cognitive_system = CognitiveSystem()
    await cognitive_system.initialize()
    
    # 创建元认知任务
    metacognitive_task = CognitiveTask(
        id="metacognitive_task_001",
        content="评估你的推理过程是否合理，考虑是否有其他可能的解释或方法",
        task_type="metacognitive",
        priority="normal",
        complexity="moderate",
        metadata={
            "context": "reasoning_evaluation",
            "meta_cognitive": True
        }
    )
    
    print(f"📋 元认知任务: {metacognitive_task.content}")
    
    # 执行元认知推理
    result = await cognitive_system.process_task(metacognitive_task)
    
    print(f"✅ 元认知评估: {'✅' if result.success else '❌'}")
    if result.success:
        output = result.output
        print(f"📊 元认知评估结果:")
        print(f"   推理质量评分: {output.get('reasoning_quality_score', 'N/A')}")
        print(f"   置信度校准: {output.get('confidence_calibration', 'N/A')}")
        print(f"   替代方案数: {output.get('alternative_approaches_considered', 0)}")
        
        if output.get('improvement_suggestions'):
            print(f"   改进建议: {output['improvement_suggestions'][0][:100]}...")
    
    # 查看元认知指标
    if result.reasoning_process:
        meta_cognitive_indicators = result.reasoning_process.metadata.get('meta_cognitive_indicators', {})
        if meta_cognitive_indicators:
            print(f"🔍 元认知指标: {meta_cognitive_indicators}")
    
    print("\n--- 元认知示例完成 ---\n")


async def example_batch_processing():
    """
    批量处理示例
    """
    print("🧠=== 批量处理示例 ===🧠\n")
    
    cognitive_system = CognitiveSystem()
    await cognitive_system.initialize()
    
    # 创建一批任务
    batch_tasks = [
        CognitiveTask(
            id=f"batch_task_{i}",
            content=f"分析任务 {i}: {content}",
            task_type="analysis",
            priority="normal",
            complexity="moderate"
        )
        for i, content in enumerate([
            "分析Python编程语言的优势和劣势",
            "评估机器学习在医疗领域的应用前景", 
            "讨论AI对教育行业的影响",
            "分析区块链技术的发展趋势",
            "评估云计算的安全性挑战"
        ], 1)
    ]
    
    print(f"📋 批量处理任务数: {len(batch_tasks)}")
    
    # 批量处理
    start_time = datetime.now()
    batch_results = await cognitive_system.process_batch(batch_tasks)
    batch_time = (datetime.now() - start_time).total_seconds()
    
    print(f"✅ 批量处理完成，耗时: {batch_time:.2f}秒")
    
    # 统计结果
    success_count = sum(1 for r in batch_results if r.success)
    avg_confidence = sum(r.confidence for r in batch_results if r.confidence) / len(batch_results)
    
    print(f"📊 批量处理统计:")
    print(f"   成功率: {success_count}/{len(batch_tasks)} ({success_count/len(batch_tasks)*100:.1f}%)")
    print(f"   平均置信度: {avg_confidence:.2f}")
    print(f"   平均任务时间: {batch_time/len(batch_tasks):.2f}秒")
    
    # 显示部分结果
    for i, (task, result) in enumerate(zip(batch_tasks, batch_results)[:3]):
        print(f"   任务 {i+1}: {'✅' if result.success else '❌'} - {result.confidence:.2f}")
    
    print("\n--- 批量处理示例完成 ---\n")


async def run_all_examples():
    """
    运行所有示例
    """
    print("🚀 开始运行认知系统使用示例...\n")
    
    examples = [
        ("基础使用", example_basic_usage),
        ("复杂推理", example_complex_reasoning),
        ("个性化", example_personalization),
        ("偏见检测", example_bias_detection),
        ("记忆集成", example_memory_integration),
        ("技能集成", example_skill_integration),
        ("多模态推理", example_multimodal_reasoning),
        ("元认知", example_meta_cognition),
        ("批量处理", example_batch_processing)
    ]
    
    results = {}
    
    for name, example_func in examples:
        try:
            print(f"🔄 运行 {name} 示例...")
            await example_func()
            results[name] = "✅ 成功"
        except Exception as e:
            print(f"❌ {name} 示例失败: {e}")
            import traceback
            traceback.print_exc()
            results[name] = f"❌ 失败: {str(e)}"
    
    # 总结
    print("🎯=== 示例运行总结 ===🎯\n")
    for name, result in results.items():
        print(f"   {name}: {result}")
    
    success_count = sum(1 for r in results.values() if "✅" in r)
    total_count = len(results)
    
    print(f"\n📊 总体成功率: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    if success_count == total_count:
        print("\n🎉 所有示例运行成功！认知系统功能正常！")
    else:
        print(f"\n⚠️  {total_count - success_count} 个示例出现问题，请检查系统配置")


async def demonstrate_cognitive_insights():
    """
    演示认知洞察功能
    """
    print("🧠=== 认知洞察演示 ===🧠\n")
    
    cognitive_system = CognitiveSystem()
    await cognitive_system.initialize()
    
    user_id = "insight_demo_user"
    
    # 为用户执行一系列任务来收集数据
    demo_tasks = [
        CognitiveTask(
            id=f"demo_task_{i}",
            content=content,
            task_type="analysis",
            priority="normal",
            complexity="moderate"
        )
        for i, content in enumerate([
            "分析气候变化对经济的影响",
            "评估新能源技术的发展前景", 
            "讨论远程办公的优缺点",
            "分析人工智能的伦理问题",
            "评估教育数字化的趋势"
        ], 1)
    ]
    
    # 执行任务
    for task in demo_tasks:
        await cognitive_system.process_task(task)
    
    # 生成认知洞察
    insights = await cognitive_system.get_cognitive_insights(user_id)
    
    print("📋 认知洞察报告:")
    if insights:
        print(f"   分析任务数: {insights.get('total_analyzed_tasks', 0)}")
        print(f"   平均置信度: {insights.get('average_confidence', 0.0):.2f}")
        print(f"   常用策略: {insights.get('frequently_used_strategies', [])}")
        
        if 'strengths_identified' in insights:
            print(f"   识别优势: {insights['strengths_identified']}")
        
        if 'improvement_areas' in insights:
            print(f"   改进领域: {insights['improvement_areas']}")
        
        if 'cognitive_profile_summary' in insights:
            profile_summary = insights['cognitive_profile_summary']
            print(f"   推理风格: {profile_summary.get('reasoning_style', 'N/A')}")
            print(f"   学习偏好: {profile_summary.get('learning_preference', 'N/A')}")
            print(f"   注意力跨度: {profile_summary.get('attention_span_minutes', 'N/A')}分钟")
    else:
        print("   无法生成洞察 - 缺乏足够的数据")
    
    print("\n--- 认知洞察演示完成 ---\n")


if __name__ == "__main__":
    # 运行完整示例套件
    asyncio.run(run_all_examples())
    
    # 单独运行认知洞察演示
    print("\n" + "="*50)
    asyncio.run(demonstrate_cognitive_insights())
    
    print(f"\n🎊 认知系统示例演示完成！")
    print(f"灵姬已经展示了认知系统的全部核心功能呢～❤️")
    print(f"夫君可以基于这些示例来开发自己的认知应用哦！💕")