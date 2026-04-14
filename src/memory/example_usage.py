"""
记忆系统使用示例
"""
import asyncio
import sys
from datetime import datetime
from typing import List
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from memory.core import MemorySystem
from memory.config import init_config, MemoryConfig
from memory.interfaces import Memory


async def basic_usage_example():
    """
    基本使用示例
    """
    print("=== 记忆系统基本使用示例 ===\n")
    
    # 初始化配置
    config = MemoryConfig(
        persist_directory="./demo_memories",
        collection_name="demo_collection",
        embedding_service_type="mock",  # 使用模拟嵌入服务
        embedding_dimension=1536
    )
    
    # 创建记忆系统实例
    memory_system = MemorySystem(
        persist_directory=config.persist_directory,
        collection_name=config.collection_name,
        embedding_service_type=config.embedding_service_type,
        dimension=config.embedding_dimension
    )
    
    print("1. 存储记忆...")
    
    # 记住一些内容
    memory_id1 = await memory_system.remember(
        content="今天学习了Python的异步编程，async/await关键字非常有用。",
        metadata={"subject": "programming", "difficulty": "beginner", "date": str(datetime.now().date())},
        tags=["python", "async", "programming", "learning"],
        priority=4
    )
    print(f"   存储记忆1，ID: {memory_id1}")
    
    memory_id2 = await memory_system.remember(
        content="Python的装饰器是一种很强大的功能，可以修改函数的行为。",
        metadata={"subject": "programming", "difficulty": "intermediate", "date": str(datetime.now().date())},
        tags=["python", "decorator", "programming"],
        priority=3
    )
    print(f"   存储记忆2，ID: {memory_id2}")
    
    memory_id3 = await memory_system.remember(
        content="机器学习中的梯度下降算法是优化模型参数的核心方法。",
        metadata={"subject": "machine_learning", "difficulty": "advanced", "date": str(datetime.now().date())},
        tags=["machine_learning", "gradient_descent", "optimization"],
        priority=5
    )
    print(f"   存储记忆3，ID: {memory_id3}")
    
    print("\n2. 检索记忆...")
    
    # 搜索相关记忆
    results = await memory_system.recall("Python编程", top_k=5, threshold=0.5)
    print(f"   找到 {len(results)} 个相关记忆:")
    for i, result in enumerate(results, 1):
        print(f"     {i}. {result.memory.content[:60]}... (相似度: {result.similarity_score:.3f})")
    
    print("\n3. 建立记忆关联...")
    
    # 建立关联
    success = await memory_system.associate(memory_id1, memory_id2)
    if success:
        print(f"   成功关联记忆 {memory_id1} 和 {memory_id2}")
    
    print("\n4. 查找关联记忆...")
    
    # 查找关联记忆
    related_memories = await memory_system.find_related_memories(memory_id1, top_k=3)
    print(f"   记忆 {memory_id1[:8]}... 的相关记忆:")
    for i, result in enumerate(related_memories, 1):
        print(f"     {i}. {result.memory.content[:60]}... (相似度: {result.similarity_score:.3f})")
    
    print("\n5. 获取记忆统计...")
    
    # 获取统计信息
    stats = await memory_system.get_memory_statistics()
    print(f"   总记忆数: {stats['total_memories']}")
    print(f"   嵌入维度: {stats['embedding_dimension']}")
    
    print("\n6. 更新记忆优先级...")
    
    # 更新优先级
    update_success = await memory_system.update_memory_priority(memory_id1, 5)
    if update_success:
        print(f"   成功将记忆 {memory_id1[:8]}... 的优先级更新为 5")
    
    print("\n7. 批量存储记忆...")
    
    # 批量存储
    batch_contents = [
        {
            "content": "Python的上下文管理器使用with语句实现资源的自动管理。",
            "metadata": {"subject": "programming", "difficulty": "intermediate"},
            "tags": ["python", "context_manager", "with_statement"],
            "priority": 3
        },
        {
            "content": "深度学习中的反向传播算法用于计算梯度。",
            "metadata": {"subject": "deep_learning", "difficulty": "advanced"},
            "tags": ["deep_learning", "backpropagation", "gradients"],
            "priority": 4
        }
    ]
    
    batch_ids = await memory_system.batch_remember(batch_contents)
    print(f"   批量存储了 {len(batch_ids)} 个记忆: {[id[:8] + '...' for id in batch_ids]}")
    
    print("\n=== 记忆系统基本使用示例完成 ===\n")


async def advanced_usage_example():
    """
    高级使用示例
    """
    print("=== 记忆系统高级使用示例 ===\n")
    
    # 使用更复杂的配置
    config = MemoryConfig(
        persist_directory="./advanced_demo_memories",
        collection_name="advanced_collection",
        embedding_service_type="mock",
        embedding_dimension=1536,
        default_top_k=10,
        default_threshold=0.6
    )
    
    memory_system = MemorySystem(
        persist_directory=config.persist_directory,
        collection_name=config.collection_name,
        embedding_service_type=config.embedding_service_type,
        dimension=config.embedding_dimension
    )
    
    print("1. 存储复杂记忆内容...")
    
    # 存储不同类型的记忆
    complex_memories = [
        {
            "content": "2023年12月15日，我在咖啡馆完成了关于人工智能伦理的报告。讨论了AI偏见、隐私保护和算法透明度等问题。这次经历让我深刻认识到AI发展中的社会责任。",
            "metadata": {
                "date": "2023-12-15",
                "location": "Starbucks Downtown",
                "topic": "AI Ethics",
                "people": ["Alice", "Bob"],
                "emotion": "thoughtful"
            },
            "tags": ["ai_ethics", "report", "coffee_shop", "social_responsibility"],
            "priority": 4
        },
        {
            "content": "Python中的生成器(generator)是一种特殊的函数，使用yield关键字返回值。它允许函数在执行过程中暂停并保存当前状态，下次调用时从暂停处继续执行。这种方法节省内存，特别适合处理大数据集。",
            "metadata": {
                "date": "2023-12-10",
                "source": "Advanced Python Programming Book",
                "difficulty": "intermediate",
                "usefulness": 9
            },
            "tags": ["python", "generator", "yield", "memory_efficiency", "advanced"],
            "priority": 5
        },
        {
            "content": "今天尝试了新的机器学习模型架构，准确率提升了15%，但训练时间增加了30%。需要在准确率和效率之间找到平衡点。考虑使用模型压缩技术来优化性能。",
            "metadata": {
                "date": "2023-12-12",
                "project": "ML Model Optimization",
                "metric": {"accuracy": 0.87, "training_time": "2h 30m"},
                "next_steps": ["model_compression", "pruning", "quantization"]
            },
            "tags": ["ml_optimization", "model_performance", "accuracy", "efficiency"],
            "priority": 5
        }
    ]
    
    stored_ids = []
    for i, memory_data in enumerate(complex_memories, 1):
        memory_id = await memory_system.remember(**memory_data)
        stored_ids.append(memory_id)
        print(f"   存储复杂记忆 {i}，ID: {memory_id[:8]}...")
    
    print(f"\n2. 执行复杂查询...")
    
    # 复杂查询示例
    queries = [
        "关于Python生成器的知识",
        "AI伦理相关的内容", 
        "机器学习模型优化",
        "提升准确率的方法"
    ]
    
    for query in queries:
        print(f"\n   查询: '{query}'")
        results = await memory_system.recall(query, top_k=3, threshold=0.5)
        if results:
            for i, result in enumerate(results, 1):
                print(f"     {i}. {result.memory.content[:80]}... (相似度: {result.similarity_score:.3f})")
        else:
            print("     未找到相关记忆")
    
    print(f"\n3. 执行关联分析...")
    
    # 建立多个关联
    associations = [
        (stored_ids[0], stored_ids[2]),  # AI伦理与ML优化
        (stored_ids[1], stored_ids[2])   # Python生成器与ML优化
    ]
    
    for mem1, mem2 in associations:
        success = await memory_system.associate(mem1, mem2)
        if success:
            print(f"     关联 {mem1[:8]}... ↔ {mem2[:8]}... 成功")
    
    print(f"\n4. 分析关联网络...")
    
    # 分析第一个记忆的关联网络
    main_memory_id = stored_ids[2]  # ML优化记忆
    related = await memory_system.find_related_memories(main_memory_id, top_k=5)
    
    print(f"   记忆 {main_memory_id[:8]}... 的关联网络:")
    for i, result in enumerate(related, 1):
        print(f"     {i}. {result.memory.content[:60]}... (关联度: {result.similarity_score:.3f})")
    
    print(f"\n5. 获取详细统计信息...")
    
    stats = await memory_system.get_memory_statistics()
    print(f"   总记忆数: {stats['total_memories']}")
    print(f"   嵌入维度: {stats['embedding_dimension']}")
    
    print("\n=== 记忆系统高级使用示例完成 ===\n")


async def run_all_examples():
    """
    运行所有示例
    """
    print("🚀 开始运行记忆系统使用示例\n")
    
    try:
        await basic_usage_example()
        await advanced_usage_example()
        print("🎉 所有示例运行完成！")
    except Exception as e:
        print(f"❌ 运行示例时发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 运行示例
    asyncio.run(run_all_examples())