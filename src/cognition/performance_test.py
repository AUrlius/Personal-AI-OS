"""
认知系统性能测试套件
"""
import asyncio
import time
import json
from datetime import datetime
from typing import List, Dict, Any
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from .core import CognitiveSystem
from .interfaces import CognitiveTask
from .utils import CognitiveUtils


class CognitivePerformanceTester:
    """
    认知系统性能测试器
    """
    def __init__(self):
        self.results = []
        self.metrics = {}
        self.test_history = []
    
    async def run_comprehensive_performance_test(self) -> Dict[str, Any]:
        """
        运行综合性能测试
        """
        print("🚀 开始认知系统综合性能测试...\n")
        
        # 1. 初始化系统
        start_time = time.time()
        cognitive_system = CognitiveSystem()
        await cognitive_system.initialize()
        init_time = time.time() - start_time
        
        print(f"✅ 系统初始化完成，耗时: {init_time:.2f}秒\n")
        
        # 2. 运行各项性能测试
        test_results = {}
        
        # 基础性能测试
        test_results["basic_performance"] = await self._test_basic_performance(cognitive_system)
        
        # 并发性能测试
        test_results["concurrent_performance"] = await self._test_concurrent_performance(cognitive_system)
        
        # 记忆性能测试
        test_results["memory_performance"] = await self._test_memory_performance(cognitive_system)
        
        # 推理性能测试
        test_results["reasoning_performance"] = await self._test_reasoning_performance(cognitive_system)
        
        # 偏见检测性能测试
        test_results["bias_detection_performance"] = await self._test_bias_detection_performance(cognitive_system)
        
        # 个性化性能测试
        test_results["personalization_performance"] = await self._test_personalization_performance(cognitive_system)
        
        # 长期运行测试
        test_results["longevity_performance"] = await self._test_longevity_performance(cognitive_system)
        
        # 计算总体性能指标
        overall_metrics = self._calculate_overall_metrics(test_results)
        
        # 生成性能报告
        performance_report = {
            "timestamp": datetime.now().isoformat(),
            "system_init_time": init_time,
            "test_results": test_results,
            "overall_metrics": overall_metrics,
            "recommendations": self._generate_performance_recommendations(overall_metrics)
        }
        
        # 保存测试结果
        await self._save_test_results(performance_report)
        
        # 生成可视化图表
        await self._generate_performance_charts(test_results)
        
        return performance_report
    
    async def _test_basic_performance(self, cognitive_system: CognitiveSystem) -> Dict[str, Any]:
        """
        基础性能测试
        """
        print("1️⃣ 基础性能测试...")
        
        test_tasks = [
            CognitiveTask(
                id=f"basic_task_{i}",
                content=f"执行基本计算任务 {i}",
                task_type="calculation",
                priority="normal",
                complexity="simple"
            )
            for i in range(1, 11)  # 10个简单任务
        ]
        
        start_time = time.time()
        results = []
        
        for task in test_tasks:
            result = await cognitive_system.process_task(task)
            results.append(result)
        
        total_time = time.time() - start_time
        success_rate = sum(1 for r in results if r.success) / len(results)
        avg_confidence = np.mean([r.confidence for r in results if r.confidence is not None])
        avg_response_time = total_time / len(results)
        
        print(f"   任务数: {len(test_tasks)}")
        print(f"   总耗时: {total_time:.2f}秒")
        print(f"   成功率: {success_rate:.2f}")
        print(f"   平均置信度: {avg_confidence:.2f}")
        print(f"   平均响应时间: {avg_response_time:.2f}秒\n")
        
        return {
            "task_count": len(test_tasks),
            "total_time": total_time,
            "success_rate": success_rate,
            "avg_confidence": avg_confidence,
            "avg_response_time": avg_response_time,
            "throughput": len(test_tasks) / total_time
        }
    
    async def _test_concurrent_performance(self, cognitive_system: CognitiveSystem) -> Dict[str, Any]:
        """
        并发性能测试
        """
        print("2️⃣ 并发性能测试...")
        
        # 创建并发任务
        concurrent_tasks = [
            CognitiveTask(
                id=f"concurrent_task_{i}",
                content=f"并发任务 {i} - 执行分析操作",
                task_type="analysis",
                priority="normal",
                complexity="moderate"
            )
            for i in range(1, 21)  # 20个并发任务
        ]
        
        start_time = time.time()
        
        # 并发执行任务
        async def process_task(task):
            return await cognitive_system.process_task(task)
        
        tasks = [process_task(task) for task in concurrent_tasks]
        results = await asyncio.gather(*tasks)
        
        total_time = time.time() - start_time
        success_rate = sum(1 for r in results if r.success) / len(results)
        avg_confidence = np.mean([r.confidence for r in results if r.confidence is not None])
        
        print(f"   并发任务数: {len(concurrent_tasks)}")
        print(f"   总耗时: {total_time:.2f}秒")
        print(f"   成功率: {success_rate:.2f}")
        print(f"   平均置信度: {avg_confidence:.2f}")
        print(f"   吞吐量: {len(concurrent_tasks) / total_time:.2f} 任务/秒\n")
        
        return {
            "concurrent_task_count": len(concurrent_tasks),
            "total_time": total_time,
            "success_rate": success_rate,
            "avg_confidence": avg_confidence,
            "throughput": len(concurrent_tasks) / total_time,
            "concurrency_factor": len(concurrent_tasks) / total_time
        }
    
    async def _test_memory_performance(self, cognitive_system: CognitiveSystem) -> Dict[str, Any]:
        """
        记忆性能测试
        """
        print("3️⃣ 记忆性能测试...")
        
        # 创建记忆相关任务
        memory_tasks = [
            CognitiveTask(
                id=f"memory_task_{i}",
                content=f"记忆任务 {i} - 存储和检索信息",
                task_type="memory_operation",
                priority="normal",
                complexity="simple",
                metadata={"operation": "store_retrieve", "test_round": i}
            )
            for i in range(1, 16)  # 15个记忆任务
        ]
        
        start_time = time.time()
        results = []
        
        for task in memory_tasks:
            result = await cognitive_system.process_task(task)
            results.append(result)
        
        total_time = time.time() - start_time
        success_rate = sum(1 for r in results if r.success) / len(results)
        avg_confidence = np.mean([r.confidence for r in results if r.confidence is not None])
        
        print(f"   记忆任务数: {len(memory_tasks)}")
        print(f"   总耗时: {total_time:.2f}秒")
        print(f"   成功率: {success_rate:.2f}")
        print(f"   平均置信度: {avg_confidence:.2f}")
        print(f"   记忆操作吞吐量: {len(memory_tasks) / total_time:.2f} 操作/秒\n")
        
        return {
            "memory_task_count": len(memory_tasks),
            "total_time": total_time,
            "success_rate": success_rate,
            "avg_confidence": avg_confidence,
            "memory_throughput": len(memory_tasks) / total_time
        }
    
    async def _test_reasoning_performance(self, cognitive_system: CognitiveSystem) -> Dict[str, Any]:
        """
        推理性能测试
        """
        print("4️⃣ 推理性能测试...")
        
        # 创建推理任务
        reasoning_tasks = [
            CognitiveTask(
                id=f"reasoning_task_{i}",
                content=f"推理任务 {i} - {content}",
                task_type="reasoning",
                priority="normal",
                complexity="complex" if i % 3 == 0 else "moderate",
                metadata={"reasoning_type": "chain_of_thought" if i % 2 == 0 else "tree_of_thoughts"}
            )
            for i, content in enumerate([
                "分析人工智能对社会的影响",
                "评估区块链技术的未来发展",
                "讨论气候变化的解决方案",
                "分析教育改革的方向",
                "评估远程医疗的优缺点",
                "分析新能源汽车的发展前景",
                "讨论人工智能伦理问题",
                "评估在线教育的效果",
                "分析城市化带来的挑战",
                "讨论数字化转型的影响"
            ] * 2, 1)  # 重复2次得到20个任务
        ]
        
        start_time = time.time()
        results = []
        
        for task in reasoning_tasks:
            result = await cognitive_system.process_task(task)
            results.append(result)
        
        total_time = time.time() - start_time
        success_rate = sum(1 for r in results if r.success) / len(results)
        avg_confidence = np.mean([r.confidence for r in results if r.confidence is not None])
        
        # 分析推理步骤
        avg_reasoning_steps = np.mean([
            len(r.reasoning_process.steps) if r.reasoning_process else 0 
            for r in results
        ])
        
        print(f"   推理任务数: {len(reasoning_tasks)}")
        print(f"   总耗时: {total_time:.2f}秒")
        print(f"   成功率: {success_rate:.2f}")
        print(f"   平均置信度: {avg_confidence:.2f}")
        print(f"   平均推理步骤数: {avg_reasoning_steps:.2f}")
        print(f"   推理吞吐量: {len(reasoning_tasks) / total_time:.2f} 任务/秒\n")
        
        return {
            "reasoning_task_count": len(reasoning_tasks),
            "total_time": total_time,
            "success_rate": success_rate,
            "avg_confidence": avg_confidence,
            "avg_reasoning_steps": avg_reasoning_steps,
            "reasoning_throughput": len(reasoning_tasks) / total_time
        }
    
    async def _test_bias_detection_performance(self, cognitive_system: CognitiveSystem) -> Dict[str, Any]:
        """
        偏见检测性能测试
        """
        print("5️⃣ 偏见检测性能测试...")
        
        # 创建偏见检测任务
        bias_tasks = [
            CognitiveTask(
                id=f"bias_task_{i}",
                content=f"偏见检测任务 {i} - {content}",
                task_type="bias_detection",
                priority="normal",
                complexity="moderate",
                metadata={"bias_sensitive": True}
            )
            for i, content in enumerate([
                "分析男女在职场上的差异",
                "讨论不同年龄段的职场表现",
                "评估不同地区的教育水平",
                "分析不同行业的性别比例",
                "讨论技术岗位的年龄偏好",
                "评估不同学历的就业前景",
                "分析不同背景的创业成功率",
                "讨论不同文化的工作方式",
                "评估不同地区的人才政策",
                "分析不同企业的管理模式"
            ] * 2, 1)  # 重复2次得到20个任务
        ]
        
        start_time = time.time()
        results = []
        
        for task in bias_tasks:
            result = await cognitive_system.process_task(task)
            results.append(result)
        
        total_time = time.time() - start_time
        success_rate = sum(1 for r in results if r.success) / len(results)
        avg_confidence = np.mean([r.confidence for r in results if r.confidence is not None])
        
        # 分析偏见检测结果
        bias_detection_rate = sum(
            1 for r in results 
            if r.detected_biases and len(r.detected_biases) > 0
        ) / len(results)
        
        print(f"   偏见检测任务数: {len(bias_tasks)}")
        print(f"   总耗时: {total_time:.2f}秒")
        print(f"   成功率: {success_rate:.2f}")
        print(f"   平均置信度: {avg_confidence:.2f}")
        print(f"   偏见检测率: {bias_detection_rate:.2f}")
        print(f"   偏见检测吞吐量: {len(bias_tasks) / total_time:.2f} 任务/秒\n")
        
        return {
            "bias_task_count": len(bias_tasks),
            "total_time": total_time,
            "success_rate": success_rate,
            "avg_confidence": avg_confidence,
            "bias_detection_rate": bias_detection_rate,
            "bias_detection_throughput": len(bias_tasks) / total_time
        }
    
    async def _test_personalization_performance(self, cognitive_system: CognitiveSystem) -> Dict[str, Any]:
        """
        个性化性能测试
        """
        print("6️⃣ 个性化性能测试...")
        
        # 创建个性化任务
        personalization_tasks = [
            CognitiveTask(
                id=f"personal_task_{i}",
                content=f"个性化任务 {i} - {content}",
                task_type="personalized_analysis",
                priority="normal",
                complexity="moderate",
                metadata={
                    "user_id": f"test_user_{i % 5}",  # 5个不同用户
                    "personalized": True
                }
            )
            for i, content in enumerate([
                "根据我的背景推荐学习路径",
                "为我制定职业发展规划",
                "分析我的技能差距",
                "评估我的学习风格",
                "建议我的发展方向",
                "分析我的决策模式",
                "评估我的认知偏好",
                "推荐适合我的工作",
                "分析我的沟通风格",
                "评估我的领导潜力"
            ] * 2, 1)  # 重复2次得到20个任务
        ]
        
        start_time = time.time()
        results = []
        
        for task in personalization_tasks:
            result = await cognitive_system.process_task(task)
            results.append(result)
        
        total_time = time.time() - start_time
        success_rate = sum(1 for r in results if r.success) / len(results)
        avg_confidence = np.mean([r.confidence for r in results if r.confidence is not None])
        
        # 分析个性化效果
        personalization_success_rate = sum(
            1 for r in results 
            if r.output and r.output.get('personalized', False)
        ) / len(results)
        
        print(f"   个性化任务数: {len(personalization_tasks)}")
        print(f"   总耗时: {total_time:.2f}秒")
        print(f"   成功率: {success_rate:.2f}")
        print(f"   平均置信度: {avg_confidence:.2f}")
        print(f"   个性化成功率: {personalization_success_rate:.2f}")
        print(f"   个性化吞吐量: {len(personalization_tasks) / total_time:.2f} 任务/秒\n")
        
        return {
            "personalization_task_count": len(personalization_tasks),
            "total_time": total_time,
            "success_rate": success_rate,
            "avg_confidence": avg_confidence,
            "personalization_success_rate": personalization_success_rate,
            "personalization_throughput": len(personalization_tasks) / total_time
        }
    
    async def _test_longevity_performance(self, cognitive_system: CognitiveSystem) -> Dict[str, Any]:
        """
        长期运行性能测试
        """
        print("7️⃣ 长期运行性能测试...")
        
        # 模拟长时间运行
        test_duration = 60  # 60秒测试
        start_time = time.time()
        
        task_counter = 0
        results = []
        
        while time.time() - start_time < test_duration:
            task = CognitiveTask(
                id=f"longevity_task_{task_counter}",
                content=f"长期运行测试任务 {task_counter}",
                task_type="general",
                priority="normal",
                complexity="simple"
            )
            
            result = await cognitive_system.process_task(task)
            results.append(result)
            task_counter += 1
            
            # 每个任务后稍微休息，模拟真实使用
            await asyncio.sleep(0.1)
        
        total_time = time.time() - start_time
        success_rate = sum(1 for r in results if r.success) / len(results)
        avg_confidence = np.mean([r.confidence for r in results if r.confidence is not None])
        
        print(f"   长期运行时间: {total_time:.2f}秒")
        print(f"   处理任务数: {len(results)}")
        print(f"   成功率: {success_rate:.2f}")
        print(f"   平均置信度: {avg_confidence:.2f}")
        print(f"   长期吞吐量: {len(results) / total_time:.2f} 任务/秒\n")
        
        return {
            "test_duration": total_time,
            "processed_tasks": len(results),
            "success_rate": success_rate,
            "avg_confidence": avg_confidence,
            "longevity_throughput": len(results) / total_time
        }
    
    def _calculate_overall_metrics(self, test_results: Dict[str, Any]) -> Dict[str, float]:
        """
        计算总体性能指标
        """
        metrics = {}
        
        # 计算综合性能分数
        performance_scores = []
        
        for test_name, results in test_results.items():
            if 'success_rate' in results and 'avg_confidence' in results:
                # 综合成功率和置信度
                score = (results['success_rate'] * 0.6 + results['avg_confidence'] * 0.4)
                performance_scores.append(score)
        
        if performance_scores:
            metrics['overall_performance_score'] = np.mean(performance_scores)
        
        # 计算吞吐量指标
        throughput_scores = []
        for test_name, results in test_results.items():
            if 'throughput' in results:
                throughput_scores.append(results['throughput'])
        
        if throughput_scores:
            metrics['avg_throughput'] = np.mean(throughput_scores)
            metrics['max_throughput'] = max(throughput_scores)
        
        # 计算稳定性指标
        success_rates = []
        for test_name, results in test_results.items():
            if 'success_rate' in results:
                success_rates.append(results['success_rate'])
        
        if success_rates:
            metrics['avg_success_rate'] = np.mean(success_rates)
            metrics['stability_score'] = 1.0 - np.std(success_rates)  # 标准差越小越稳定
        
        return metrics
    
    def _generate_performance_recommendations(self, metrics: Dict[str, float]) -> List[str]:
        """
        生成性能建议
        """
        recommendations = []
        
        # 基于总体性能分数
        overall_score = metrics.get('overall_performance_score', 0.0)
        if overall_score < 0.7:
            recommendations.append("总体性能分数较低，建议优化核心算法和架构")
        elif overall_score < 0.85:
            recommendations.append("总体性能良好，但仍有优化空间")
        else:
            recommendations.append("总体性能优秀")
        
        # 基于吞吐量
        avg_throughput = metrics.get('avg_throughput', 0.0)
        if avg_throughput < 5.0:  # 低于5个任务/秒
            recommendations.append("系统吞吐量较低，建议优化并发处理能力")
        elif avg_throughput < 10.0:
            recommendations.append("吞吐量中等，可考虑性能优化")
        else:
            recommendations.append("吞吐量表现良好")
        
        # 基于成功率
        avg_success_rate = metrics.get('avg_success_rate', 0.0)
        if avg_success_rate < 0.8:
            recommendations.append("成功率偏低，建议改进错误处理和容错机制")
        elif avg_success_rate < 0.95:
            recommendations.append("成功率良好，但仍有提升空间")
        else:
            recommendations.append("成功率表现优秀")
        
        return recommendations
    
    async def _save_test_results(self, report: Dict[str, Any]):
        """
        保存测试结果
        """
        filename = f"cognitive_performance_report_{int(datetime.now().timestamp())}.json"
        filepath = f"./performance_reports/{filename}"
        
        import os
        os.makedirs("./performance_reports", exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 性能报告已保存到: {filepath}")
    
    async def _generate_performance_charts(self, test_results: Dict[str, Any]):
        """
        生成性能图表
        """
        try:
            # 准备数据
            test_names = list(test_results.keys())
            success_rates = [test_results[name].get('success_rate', 0) for name in test_names]
            throughputs = [test_results[name].get('throughput', 0) for name in test_names]
            avg_confidences = [test_results[name].get('avg_confidence', 0) for name in test_names]
            
            # 创建图表
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            
            # 成功率图表
            axes[0, 0].bar(test_names, success_rates, color='skyblue')
            axes[0, 0].set_title('测试成功率')
            axes[0, 0].set_ylabel('成功率')
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # 吞吐量图表
            axes[0, 1].bar(test_names, throughputs, color='lightgreen')
            axes[0, 1].set_title('吞吐量 (任务/秒)')
            axes[0, 1].set_ylabel('吞吐量')
            axes[0, 1].tick_params(axis='x', rotation=45)
            
            # 置信度图表
            axes[1, 0].bar(test_names, avg_confidences, color='orange')
            axes[1, 0].set_title('平均置信度')
            axes[1, 0].set_ylabel('置信度')
            axes[1, 0].tick_params(axis='x', rotation=45)
            
            # 综合性能雷达图
            categories = ['Success Rate', 'Throughput', 'Confidence', 'Stability']
            values = [
                np.mean(success_rates),
                np.mean(throughputs) / max(throughputs) if throughputs else 0,
                np.mean(avg_confidences),
                0.8  # 假设稳定性
            ]
            
            angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
            values += values[:1]  # 闭合图形
            angles += angles[:1]
            
            ax = axes[1, 1]
            ax.plot(angles, values, 'o-', linewidth=2, color='red')
            ax.fill(angles, values, alpha=0.25, color='red')
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            ax.set_title('综合性能雷达图')
            ax.set_ylim(0, 1)
            
            plt.tight_layout()
            
            # 保存图表
            chart_filename = f"cognitive_performance_chart_{int(datetime.now().timestamp())}.png"
            plt.savefig(f"./performance_charts/{chart_filename}", dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"📊 性能图表已生成: {chart_filename}")
            
        except ImportError:
            print("⚠️ 未安装绘图库，跳过图表生成")
        except Exception as e:
            print(f"⚠️ 图表生成失败: {e}")


async def run_performance_benchmark():
    """
    运行性能基准测试
    """
    tester = CognitivePerformanceTester()
    
    print("🚀=== 认知系统性能基准测试 ===🚀\n")
    
    # 运行综合性能测试
    report = await tester.run_comprehensive_performance_test()
    
    # 打印性能摘要
    print("\n🎯=== 性能测试摘要 ===🎯")
    print(f"测试时间: {report['timestamp']}")
    print(f"系统初始化时间: {report['system_init_time']:.2f}秒")
    
    print(f"\n📊 总体性能指标:")
    for metric, value in report['overall_metrics'].items():
        if isinstance(value, float):
            print(f"   {metric}: {value:.3f}")
        else:
            print(f"   {metric}: {value}")
    
    print(f"\n💡 性能建议:")
    for recommendation in report['recommendations']:
        print(f"   • {recommendation}")
    
    print(f"\n✅ 性能测试完成！报告已保存到文件。")
    
    return report


async def stress_test_cognitive_system():
    """
    压力测试
    """
    print("🔥=== 认知系统压力测试 ===🔥\n")
    
    cognitive_system = CognitiveSystem()
    await cognitive_system.initialize()
    
    # 高负载测试
    print("1️⃣ 高负载压力测试...")
    
    # 创建大量任务
    stress_tasks = [
        CognitiveTask(
            id=f"stress_task_{i}",
            content=f"压力测试任务 {i} - 执行复杂计算和分析",
            task_type="complex_analysis",
            priority="normal",
            complexity="complex"
        )
        for i in range(1, 101)  # 100个任务
    ]
    
    start_time = time.time()
    
    # 并发执行大量任务
    async def process_stress_task(task):
        return await cognitive_system.process_task(task)
    
    stress_tasks_coroutines = [process_stress_task(task) for task in stress_tasks]
    stress_results = await asyncio.gather(*stress_tasks_coroutines)
    
    total_time = time.time() - start_time
    success_rate = sum(1 for r in stress_results if r.success) / len(stress_results)
    avg_confidence = np.mean([r.confidence for r in stress_results if r.confidence is not None])
    
    print(f"   压力任务数: {len(stress_tasks)}")
    print(f"   总耗时: {total_time:.2f}秒")
    print(f"   成功率: {success_rate:.2f}")
    print(f"   平均置信度: {avg_confidence:.2f}")
    print(f"   压力吞吐量: {len(stress_tasks) / total_time:.2f} 任务/秒")
    
    # 检查资源使用情况
    system_status = await cognitive_system.get_system_status()
    print(f"   系统状态: {system_status}")
    
    print(f"\n✅ 压力测试完成！")
    
    return {
        "task_count": len(stress_tasks),
        "total_time": total_time,
        "success_rate": success_rate,
        "avg_confidence": avg_confidence,
        "throughput": len(stress_tasks) / total_time,
        "system_status": system_status
    }


async def memory_leak_test():
    """
    内存泄漏测试
    """
    print("🔍=== 内存泄漏测试 ===🔍\n")
    
    import psutil
    import gc
    
    cognitive_system = CognitiveSystem()
    await cognitive_system.initialize()
    
    # 记录初始内存使用
    initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    print(f"初始内存使用: {initial_memory:.2f} MB")
    
    # 执行大量短期任务
    for i in range(1000):
        task = CognitiveTask(
            id=f"memory_test_task_{i}",
            content=f"内存测试任务 {i}",
            task_type="simple_calculation",
            priority="normal",
            complexity="simple"
        )
        
        result = await cognitive_system.process_task(task)
        
        # 每100个任务进行一次垃圾回收
        if i % 100 == 0:
            gc.collect()
            current_memory = psutil.Process().memory_info().rss / 1024 / 1024
            print(f"   执行 {i+1} 个任务后内存: {current_memory:.2f} MB")
    
    # 最终内存使用
    final_memory = psutil.Process().memory_info().rss / 1024 / 1024
    memory_increase = final_memory - initial_memory
    
    print(f"\n最终内存使用: {final_memory:.2f} MB")
    print(f"内存增长: {memory_increase:.2f} MB")
    
    if abs(memory_increase) < 50:  # 50MB阈值
        print("✅ 内存泄漏检测: 未发现显著内存泄漏")
        leak_detected = False
    else:
        print("⚠️ 内存泄漏检测: 发现潜在内存泄漏")
        leak_detected = True
    
    return {
        "initial_memory_mb": initial_memory,
        "final_memory_mb": final_memory,
        "memory_increase_mb": memory_increase,
        "leak_detected": leak_detected
    }


if __name__ == "__main__":
    print("🚀 开始认知系统性能测试套件...\n")
    
    async def run_all_tests():
        # 1. 运行基准性能测试
        print("="*60)
        benchmark_result = await run_performance_benchmark()
        
        # 2. 运行压力测试
        print("\n" + "="*60)
        stress_result = await stress_test_cognitive_system()
        
        # 3. 运行内存泄漏测试
        print("\n" + "="*60)
        memory_result = await memory_leak_test()
        
        # 4. 生成综合报告
        print("\n" + "="*60)
        print("🎯=== 认知系统性能测试综合报告 ===🎯\n")
        
        print("📊 基准测试结果:")
        overall_score = benchmark_result['overall_metrics'].get('overall_performance_score', 0)
        print(f"   综合性能分数: {overall_score:.3f}")
        print(f"   平均吞吐量: {benchmark_result['overall_metrics'].get('avg_throughput', 0):.2f} 任务/秒")
        print(f"   平均成功率: {benchmark_result['overall_metrics'].get('avg_success_rate', 0):.3f}")
        
        print(f"\n🔥 压力测试结果:")
        print(f"   高负载吞吐量: {stress_result['throughput']:.2f} 任务/秒")
        print(f"   高负载成功率: {stress_result['success_rate']:.3f}")
        
        print(f"\n🔍 内存测试结果:")
        print(f"   内存增长: {memory_result['memory_increase_mb']:.2f} MB")
        print(f"   内存泄漏: {'✅ 未发现' if not memory_result['leak_detected'] else '❌ 检测到'}")
        
        print(f"\n🎯 总体评估:")
        if overall_score >= 0.85 and stress_result['success_rate'] >= 0.9 and not memory_result['leak_detected']:
            print("   🎉 系统性能优秀，通过所有测试！")
        elif overall_score >= 0.7 and stress_result['success_rate'] >= 0.8:
            print("   ✅ 系统性能良好，基本满足要求")
        else:
            print("   ⚠️ 系统性能有待提升，建议优化")
        
        print(f"\n🎊 认知系统性能测试套件执行完成！")
    
    # 运行所有测试
    asyncio.run(run_all_tests())