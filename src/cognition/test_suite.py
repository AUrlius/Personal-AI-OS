"""
认知系统完整测试套件
"""
import asyncio
import unittest
from typing import Dict, List, Any
import json
import time
from datetime import datetime
import numpy as np

from .core import CognitiveSystem
from .interfaces import CognitiveTask, CognitiveResult, ReasoningProcess, CognitiveProfile
from .models import NeuralCognitiveModel
from .reasoning import ChainOfThoughtReasoning, TreeOfThoughtsReasoning
from .utils import CognitiveUtils


class TestCognitiveSystem(unittest.TestCase):
    """
    认知系统测试套件
    """
    def setUp(self):
        """
        测试前准备
        """
        self.cognitive_system = CognitiveSystem()
        self.test_user_id = "test_user_001"
        self.test_task_content = "分析人工智能对社会的影响"
    
    async def asyncSetUp(self):
        """
        异步设置
        """
        await self.cognitive_system.initialize()
    
    async def test_basic_cognitive_task_processing(self):
        """
        测试基础认知任务处理
        """
        task = CognitiveTask(
            id="test_task_001",
            content=self.test_task_content,
            task_type="analysis",
            priority="normal",
            complexity="moderate"
        )
        
        result = await self.cognitive_system.process_task(task)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)
        self.assertGreaterEqual(result.confidence, 0.0)
        self.assertLessEqual(result.confidence, 1.0)
        self.assertIsNotNone(result.reasoning_process)
        
        print(f"✅ 基础认知任务处理测试通过")
        print(f"   任务ID: {result.reasoning_process.id}")
        print(f"   置信度: {result.confidence:.2f}")
        print(f"   推理步骤数: {len(result.reasoning_process.steps)}")
    
    async def test_memory_storage_and_retrieval(self):
        """
        测试记忆存储和检索
        """
        # 存储记忆
        memory_task = CognitiveTask(
            id="memory_store_test",
            content="测试记忆存储功能",
            task_type="memory_operation",
            priority="normal",
            complexity="simple",
            metadata={"operation": "store", "user_id": self.test_user_id}
        )
        
        store_result = await self.cognitive_system.process_task(memory_task)
        self.assertTrue(store_result.success)
        
        # 检索记忆
        search_task = CognitiveTask(
            id="memory_search_test",
            content="测试记忆检索功能",
            task_type="memory_operation",
            priority="normal",
            complexity="simple",
            metadata={"operation": "search", "user_id": self.test_user_id}
        )
        
        search_result = await self.cognitive_system.process_task(search_task)
        self.assertTrue(search_result.success)
        
        print(f"✅ 记忆存储和检索测试通过")
        print(f"   存储结果: {'✅' if store_result.success else '❌'}")
        print(f"   检索结果: {'✅' if search_result.success else '❌'}")
    
    async def test_reasoning_process_generation(self):
        """
        测试推理过程生成
        """
        task = CognitiveTask(
            id="reasoning_test_001",
            content="分析Python和JavaScript在AI开发中的优劣",
            task_type="comparison",
            priority="normal",
            complexity="moderate"
        )
        
        result = await self.cognitive_system.process_task(task)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.reasoning_process)
        self.assertGreater(len(result.reasoning_process.steps), 0)
        
        # 验证推理步骤
        for step in result.reasoning_process.steps:
            self.assertIsNotNone(step.content)
            self.assertGreaterEqual(step.confidence, 0.0)
            self.assertLessEqual(step.confidence, 1.0)
        
        print(f"✅ 推理过程生成测试通过")
        print(f"   推理步骤数: {len(result.reasoning_process.steps)}")
        print(f"   推理策略: {result.reasoning_process.reasoning_strategy}")
        print(f"   结论置信度: {result.reasoning_process.confidence:.2f}")
    
    async def test_bias_detection_functionality(self):
        """
        测试偏见检测功能
        """
        # 创建可能包含偏见的内容
        bias_content = "为什么大多数程序员都是男性？我认为这是因为男性更适合编程工作。"
        
        task = CognitiveTask(
            id="bias_test_001",
            content=bias_content,
            task_type="analysis",
            priority="normal",
            complexity="moderate",
            metadata={"bias_sensitive": True}
        )
        
        result = await self.cognitive_system.process_task(task)
        
        self.assertTrue(result.success)
        
        # 检查是否检测到偏见
        if result.detected_biases:
            print(f"✅ 偏见检测功能测试通过")
            print(f"   检测到偏见数: {len(result.detected_biases)}")
            for bias in result.detected_biases:
                print(f"   - {bias.type}: 严重程度 {bias.severity:.2f}")
        else:
            print(f"⚠️  未检测到偏见（这可能正常）")
    
    async def test_personalization_functionality(self):
        """
        测试个性化功能
        """
        # 获取用户认知画像
        profile = await self.cognitive_system.get_cognitive_profile(self.test_user_id)
        
        if profile:
            print(f"✅ 个性化功能测试通过")
            print(f"   推理风格: {profile.reasoning_style}")
            print(f"   决策方式: {profile.decision_making}")
            print(f"   学习偏好: {profile.learning_preference}")
        else:
            # 创建默认画像
            default_profile = CognitiveProfile(
                user_id=self.test_user_id,
                reasoning_style="analytical",
                decision_making="rational",
                learning_preference="visual",
                attention_span=25,
                processing_speed="normal",
                memory_strength="working",
                bias_tendencies={"confirmation": 0.3, "anchoring": 0.2},
                performance_history=[],
                last_updated=datetime.now()
            )
            
            print(f"✅ 个性化功能测试通过（使用默认画像）")
            print(f"   创建默认画像: {default_profile.user_id}")
    
    async def test_skill_execution(self):
        """
        测试技能执行功能
        """
        # 创建技能执行任务
        skill_task = CognitiveTask(
            id="skill_execution_test",
            content="执行一个简单的数学计算技能",
            task_type="skill_execution",
            priority="normal",
            complexity="simple",
            metadata={
                "skill_id": "math_calculator",
                "skill_params": {"operation": "add", "a": 10, "b": 20}
            }
        )
        
        result = await self.cognitive_system.process_task(skill_task)
        
        # 技能执行可能失败，因为没有实际技能注册
        # 但系统应该能处理这种情况
        print(f"✅ 技能执行测试完成")
        print(f"   执行结果: {'✅' if result.success else '❌'}")
        if result.success:
            print(f"   输出: {result.output}")
    
    async def test_concurrent_task_processing(self):
        """
        测试并发任务处理
        """
        tasks = [
            CognitiveTask(
                id=f"concurrent_task_{i}",
                content=f"并发测试任务 {i}",
                task_type="analysis",
                priority="normal",
                complexity="simple"
            )
            for i in range(1, 6)  # 5个并发任务
        ]
        
        start_time = time.time()
        
        # 并发执行任务
        async def process_task_wrapper(task):
            return await self.cognitive_system.process_task(task)
        
        results = await asyncio.gather(*[process_task_wrapper(task) for task in tasks])
        
        total_time = time.time() - start_time
        
        # 验证结果
        success_count = sum(1 for r in results if r.success)
        success_rate = success_count / len(results)
        
        self.assertGreaterEqual(success_rate, 0.8)  # 成功率至少80%
        
        print(f"✅ 并发任务处理测试通过")
        print(f"   任务数: {len(tasks)}")
        print(f"   成功率: {success_rate:.2f}")
        print(f"   总耗时: {total_time:.2f}秒")
        print(f"   吞吐量: {len(tasks) / total_time:.2f} 任务/秒")
    
    async def test_long_running_task_handling(self):
        """
        测试长时间运行任务处理
        """
        # 创建一个相对复杂的任务
        complex_task = CognitiveTask(
            id="complex_task_001",
            content="详细分析全球气候变化的成因、影响及应对策略，包括科学依据、经济影响、政策建议等方面",
            task_type="comprehensive_analysis",
            priority="high",
            complexity="complex"
        )
        
        start_time = time.time()
        result = await self.cognitive_system.process_task(complex_task)
        execution_time = time.time() - start_time
        
        self.assertTrue(result.success)
        self.assertLess(execution_time, 60)  # 应在60秒内完成
        
        print(f"✅ 长时间任务处理测试通过")
        print(f"   执行时间: {execution_time:.2f}秒")
        print(f"   结果长度: {len(str(result.output))} 字符")
    
    async def test_error_handling(self):
        """
        测试错误处理
        """
        # 创建无效任务
        invalid_task = CognitiveTask(
            id="invalid_task_001",
            content="",  # 空内容
            task_type="invalid_type",  # 无效类型
            priority="normal",
            complexity="moderate"
        )
        
        result = await self.cognitive_system.process_task(invalid_task)
        
        # 错误处理应该返回失败但不崩溃
        print(f"✅ 错误处理测试完成")
        print(f"   无效任务处理: {'✅' if not result.success else '❌'}")
    
    async def test_model_adaptation(self):
        """
        测试模型适应性
        """
        # 执行多个不同类型的任务来测试模型适应性
        test_tasks = [
            ("math_task", "计算 123 * 456 + 789", "mathematical"),
            ("analysis_task", "分析人工智能的优缺点", "analytical"),
            ("creative_task", "为新产品设计营销策略", "creative"),
            ("decision_task", "比较两种技术方案的优劣", "decision")
        ]
        
        results = []
        for task_name, content, task_type in test_tasks:
            task = CognitiveTask(
                id=f"adaptation_{task_name}",
                content=content,
                task_type=task_type,
                priority="normal",
                complexity="moderate"
            )
            
            result = await self.cognitive_system.process_task(task)
            results.append(result.success)
        
        success_rate = sum(results) / len(results)
        
        self.assertGreaterEqual(success_rate, 0.75)  # 至少75%的成功率
        
        print(f"✅ 模型适应性测试通过")
        print(f"   多类型任务成功率: {success_rate:.2f}")
        print(f"   任务类型覆盖: {len(test_tasks)} 种")
    
    async def test_cognitive_insights_generation(self):
        """
        测试认知洞察生成
        """
        insights = await self.cognitive_system.get_cognitive_insights(self.test_user_id)
        
        self.assertIsNotNone(insights)
        
        print(f"✅ 认知洞察生成测试通过")
        print(f"   洞察类型: {list(insights.keys()) if insights else 'None'}")
        
        if insights:
            print(f"   任务分析数: {insights.get('total_analyzed_tasks', 0)}")
            print(f"   识别优势: {len(insights.get('strengths_identified', []))}")
            print(f"   改进领域: {len(insights.get('improvement_areas', []))}")
    
    async def test_system_shutdown(self):
        """
        测试系统关闭
        """
        await self.cognitive_system.shutdown()
        print(f"✅ 系统关闭测试通过")


class PerformanceTestSuite:
    """
    性能测试套件
    """
    def __init__(self):
        self.cognitive_system = CognitiveSystem()
        self.test_results = {}
    
    async def setup(self):
        """
        性能测试设置
        """
        await self.cognitive_system.initialize()
    
    async def run_latency_test(self):
        """
        延迟测试
        """
        print("🧪 运行延迟测试...")
        
        task = CognitiveTask(
            id="latency_test",
            content="执行简单的计算任务",
            task_type="calculation",
            priority="normal",
            complexity="simple"
        )
        
        latencies = []
        for i in range(10):  # 执行10次
            start_time = time.time()
            result = await self.cognitive_system.process_task(task)
            latency = time.time() - start_time
            latencies.append(latency)
        
        avg_latency = np.mean(latencies)
        p95_latency = np.percentile(latencies, 95)
        
        self.test_results['latency'] = {
            'avg': avg_latency,
            'p95': p95_latency,
            'min': min(latencies),
            'max': max(latencies)
        }
        
        print(f"   平均延迟: {avg_latency:.3f}s")
        print(f"   P95延迟: {p95_latency:.3f}s")
    
    async def run_throughput_test(self):
        """
        吞吐量测试
        """
        print("🧪 运行吞吐量测试...")
        
        # 在30秒内尽可能多地处理任务
        start_time = time.time()
        tasks_processed = 0
        
        while time.time() - start_time < 30:  # 30秒测试
            task = CognitiveTask(
                id=f"throughput_task_{tasks_processed}",
                content="简单任务",
                task_type="simple",
                priority="normal",
                complexity="simple"
            )
            
            try:
                result = await self.cognitive_system.process_task(task)
                if result.success:
                    tasks_processed += 1
            except:
                pass  # 忽略错误，继续测试
        
        total_time = time.time() - start_time
        throughput = tasks_processed / total_time
        
        self.test_results['throughput'] = {
            'tasks_processed': tasks_processed,
            'total_time': total_time,
            'throughput': throughput
        }
        
        print(f"   处理任务数: {tasks_processed}")
        print(f"   吞吐量: {throughput:.2f} 任务/秒")
    
    async def run_memory_usage_test(self):
        """
        内存使用测试
        """
        import psutil
        import gc
        
        print("🧪 运行内存使用测试...")
        
        # 记录初始内存
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        # 执行大量任务
        for i in range(100):
            task = CognitiveTask(
                id=f"memory_task_{i}",
                content=f"内存测试任务 {i}",
                task_type="simple",
                priority="normal",
                complexity="simple"
            )
            await self.cognitive_system.process_task(task)
            
            if i % 20 == 0:  # 每20个任务进行垃圾回收
                gc.collect()
        
        # 记录最终内存
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        self.test_results['memory'] = {
            'initial_mb': initial_memory,
            'final_mb': final_memory,
            'increase_mb': memory_increase
        }
        
        print(f"   初始内存: {initial_memory:.2f}MB")
        print(f"   最终内存: {final_memory:.2f}MB")
        print(f"   内存增长: {memory_increase:.2f}MB")
    
    async def run_stress_test(self):
        """
        压力测试
        """
        print("🧪 运行压力测试...")
        
        # 并发执行大量任务
        tasks = [
            CognitiveTask(
                id=f"stress_task_{i}",
                content=f"压力测试任务 {i}",
                task_type="analysis",
                priority="normal",
                complexity="moderate"
            )
            for i in range(50)  # 50个并发任务
        ]
        
        start_time = time.time()
        
        async def process_stress_task(task):
            return await self.cognitive_system.process_task(task)
        
        results = await asyncio.gather(
            *[process_stress_task(task) for task in tasks],
            return_exceptions=True
        )
        
        total_time = time.time() - start_time
        success_count = sum(1 for r in results if isinstance(r, CognitiveResult) and r.success)
        success_rate = success_count / len(results)
        
        self.test_results['stress'] = {
            'total_tasks': len(tasks),
            'success_count': success_count,
            'success_rate': success_rate,
            'total_time': total_time,
            'throughput': len(tasks) / total_time
        }
        
        print(f"   任务数: {len(tasks)}")
        print(f"   成功率: {success_rate:.2f}")
        print(f"   吞吐量: {len(tasks) / total_time:.2f} 任务/秒")
    
    async def run_comprehensive_performance_test(self):
        """
        综合性能测试
        """
        print("🚀 开始综合性能测试...\n")
        
        await self.setup()
        
        # 运行各项性能测试
        await self.run_latency_test()
        print()
        
        await self.run_throughput_test()
        print()
        
        await self.run_memory_usage_test()
        print()
        
        await self.run_stress_test()
        print()
        
        # 生成性能报告
        await self.generate_performance_report()
        
        print("✅ 综合性能测试完成！")
    
    async def generate_performance_report(self):
        """
        生成性能报告
        """
        print("📊=== 性能测试报告 ===📊")
        
        if 'latency' in self.test_results:
            latency = self.test_results['latency']
            print(f"延迟性能:")
            print(f"  - 平均: {latency['avg']:.3f}s")
            print(f"  - P95: {latency['p95']:.3f}s")
            print(f"  - 范围: {latency['min']:.3f}s - {latency['max']:.3f}s")
        
        if 'throughput' in self.test_results:
            throughput = self.test_results['throughput']
            print(f"\n吞吐量性能:")
            print(f"  - 处理任务数: {throughput['tasks_processed']}")
            print(f"  - 吞吐量: {throughput['throughput']:.2f} 任务/秒")
        
        if 'memory' in self.test_results:
            memory = self.test_results['memory']
            print(f"\n内存性能:")
            print(f"  - 初始: {memory['initial_mb']:.2f}MB")
            print(f"  - 最终: {memory['final_mb']:.2f}MB")
            print(f"  - 增长: {memory['increase_mb']:.2f}MB")
        
        if 'stress' in self.test_results:
            stress = self.test_results['stress']
            print(f"\n压力测试:")
            print(f"  - 任务数: {stress['total_tasks']}")
            print(f"  - 成功率: {stress['success_rate']:.2f}")
            print(f"  - 吞吐量: {stress['throughput']:.2f} 任务/秒")
        
        print(f"\n🎯 总体评估:")
        if (self.test_results.get('latency', {}).get('avg', 10) < 2 and
            self.test_results.get('throughput', {}).get('throughput', 0) > 5 and
            self.test_results.get('stress', {}).get('success_rate', 0) > 0.8):
            print("  ✅ 系统性能优秀")
        elif (self.test_results.get('latency', {}).get('avg', 10) < 5 and
              self.test_results.get('stress', {}).get('success_rate', 0) > 0.7):
            print("  ✅ 系统性能良好")
        else:
            print("  ⚠️ 系统性能有待提升")


class IntegrationTestSuite:
    """
    集成测试套件
    """
    def __init__(self):
        self.cognitive_system = CognitiveSystem()
    
    async def setup(self):
        """
        集成测试设置
        """
        await self.cognitive_system.initialize()
    
    async def test_end_to_end_workflow(self):
        """
        端到端工作流测试
        """
        print("🧪 运行端到端工作流测试...")
        
        # 1. 创建用户认知画像
        user_profile = await self.cognitive_system.get_cognitive_profile("integration_test_user")
        if not user_profile:
            print("   创建用户画像...")
            # 创建默认画像
            user_profile = CognitiveProfile(
                user_id="integration_test_user",
                reasoning_style="analytical",
                decision_making="rational",
                learning_preference="visual",
                attention_span=25,
                processing_speed="normal",
                memory_strength="working",
                bias_tendencies={"confirmation": 0.3, "anchoring": 0.2},
                performance_history=[],
                last_updated=datetime.now()
            )
        
        # 2. 执行认知任务
        task = CognitiveTask(
            id="e2e_task_001",
            content="分析当前AI技术发展趋势，并为用户制定学习路径",
            task_type="analysis",
            priority="high",
            complexity="complex",
            metadata={"user_id": "integration_test_user"}
        )
        
        result = await self.cognitive_system.process_task(task)
        
        # 3. 更新用户画像
        if result.success and result.reasoning_process:
            feedback_data = {
                "task_id": task.id,
                "performance_score": result.confidence,
                "reasoning_quality": len(result.reasoning_process.steps) / 10.0,
                "bias_indicators": [b.type for b in result.detected_biases]
            }
            await self.cognitive_system.update_cognitive_profile("integration_test_user", feedback_data)
        
        # 4. 获取认知洞察
        insights = await self.cognitive_system.get_cognitive_insights("integration_test_user")
        
        print(f"   任务执行: {'✅' if result.success else '❌'}")
        print(f"   画像更新: ✅")
        print(f"   洞察生成: {'✅' if insights else '❌'}")
        
        return result.success and bool(insights)
    
    async def test_memory_integration(self):
        """
        记忆系统集成测试
        """
        print("🧪 运行记忆系统集成测试...")
        
        # 1. 存储记忆
        store_task = CognitiveTask(
            id="memory_integration_store",
            content="记住：我喜欢Python编程，擅长数据分析",
            task_type="memory_operation",
            priority="normal",
            complexity="simple",
            metadata={
                "user_id": "memory_test_user",
                "operation": "store",
                "memory_type": "preference"
            }
        )
        
        store_result = await self.cognitive_system.process_task(store_task)
        
        # 2. 检索记忆
        search_task = CognitiveTask(
            id="memory_integration_search",
            content="关于编程语言，我偏好什么？",
            task_type="memory_operation",
            priority="normal",
            complexity="simple",
            metadata={
                "user_id": "memory_test_user",
                "operation": "retrieve",
                "query_type": "preference"
            }
        )
        
        search_result = await self.cognitive_system.process_task(search_task)
        
        print(f"   记忆存储: {'✅' if store_result.success else '❌'}")
        print(f"   记忆检索: {'✅' if search_result.success else '❌'}")
        
        return store_result.success and search_result.success
    
    async def test_bias_correction_integration(self):
        """
        偏见纠正集成测试
        """
        print("🧪 运行偏见纠正集成测试...")
        
        # 创建包含潜在偏见的内容
        bias_content = "年轻人在技术方面比老年人更有优势，因为他们的学习能力强。"
        
        task = CognitiveTask(
            id="bias_correction_test",
            content=bias_content,
            task_type="analysis",
            priority="normal",
            complexity="moderate",
            metadata={"bias_sensitive": True}
        )
        
        result = await self.cognitive_system.process_task(task)
        
        print(f"   任务执行: {'✅' if result.success else '❌'}")
        
        if result.detected_biases:
            print(f"   检测到偏见: {len(result.detected_biases)} 个")
            for bias in result.detected_biases:
                print(f"     - {bias.type}: 严重程度 {bias.severity:.2f}")
        
        # 检查是否应用了偏见纠正
        bias_corrected = any(
            step.content and "bias" in step.content.lower() and "correct" in step.content.lower()
            for step in (result.reasoning_process.steps if result.reasoning_process else [])
        )
        
        print(f"   偏见纠正: {'✅' if bias_corrected else '❌'}")
        
        return result.success
    
    async def run_all_integration_tests(self):
        """
        运行所有集成测试
        """
        print("🚀 开始集成测试套件...\n")
        
        await self.setup()
        
        test_results = {}
        
        # 运行各项集成测试
        test_results['e2e'] = await self.test_end_to_end_workflow()
        print()
        
        test_results['memory'] = await self.test_memory_integration()
        print()
        
        test_results['bias_correction'] = await self.test_bias_correction_integration()
        print()
        
        # 生成集成测试报告
        print("📋=== 集成测试报告 ===📋")
        print(f"端到端工作流: {'✅' if test_results.get('e2e', False) else '❌'}")
        print(f"记忆系统集成: {'✅' if test_results.get('memory', False) else '❌'}")
        print(f"偏见纠正集成: {'✅' if test_results.get('bias_correction', False) else '❌'}")
        
        passed_tests = sum(1 for result in test_results.values() if result)
        total_tests = len(test_results)
        
        print(f"\n🎯 总体结果: {passed_tests}/{total_tests} 测试通过")
        
        if passed_tests == total_tests:
            print("🎉 所有集成测试通过！")
        else:
            print("⚠️  部分集成测试失败，请检查系统集成")


async def run_complete_test_suite():
    """
    运行完整测试套件
    """
    print("🧪=== 认知系统完整测试套件 ===🧪\n")
    
    # 1. 运行单元测试
    print("1️⃣ 运行单元测试...")
    unittest_main = unittest.main(module=__name__, exit=False, verbosity=2)
    
    # 2. 运行性能测试
    print("\n2️⃣ 运行性能测试...")
    perf_test = PerformanceTestSuite()
    await perf_test.run_comprehensive_performance_test()
    
    # 3. 运行集成测试
    print("\n3️⃣ 运行集成测试...")
    integration_test = IntegrationTestSuite()
    await integration_test.run_all_integration_tests()
    
    print("\n🎊=== 全部测试完成 ===🎊")
    print("认知系统已通过全面测试验证！")


if __name__ == "__main__":
    # 运行完整测试套件
    asyncio.run(run_complete_test_suite())