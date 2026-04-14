"""
技能系统使用示例
"""
import asyncio
import json
from datetime import datetime
from typing import Dict, Any

# 从技能系统导入所需类
from .core import SkillSystem, SkillBuilder, SkillOrchestrator
from .interfaces import SkillInput, SkillOutput, SkillStatus, SkillVisibility


async def basic_skill_system_demo():
    """
    基础技能系统演示
    """
    print("=== 基础技能系统演示 ===\n")
    
    # 创建技能系统实例
    skill_system = SkillSystem()
    
    print("1. 创建和注册技能...")
    
    # 使用技能构建器创建一个简单的数学计算技能
    calculator_skill = (SkillBuilder()
        .id("calculator-add")
        .name("加法计算器")
        .description("执行两个数字的加法运算")
        .version("1.0.0")
        .author("system")
        .category("utility")
        .add_tag("math")
        .add_tag("calculator")
        .add_input("a", "number", "第一个数字", required=True)
        .add_input("b", "number", "第二个数字", required=True)
        .add_output("result", "number", "计算结果")
        .code("""
def execute(a, b):
    '''执行加法运算'''
    return {"result": a + b}
""")
        .language("python")
        .execution_type("function")
        .visibility(SkillVisibility.PUBLIC)
        .status(SkillStatus.PUBLISHED)
        .build())
    
    # 注册技能
    success = await skill_system.register(calculator_skill)
    print(f"   技能注册结果: {success}")
    
    # 创建另一个技能 - 文本处理技能
    text_processor_skill = (SkillBuilder()
        .id("text-processor-uppercase")
        .name("文本转大写")
        .description("将输入文本转换为大写")
        .version("1.0.0")
        .author("system")
        .category("text_processing")
        .add_tag("text")
        .add_tag("string")
        .add_input("text", "string", "输入文本", required=True)
        .add_output("result", "string", "处理后的文本")
        .code("""
def execute(text):
    '''将文本转换为大写'''
    return {"result": text.upper()}
""")
        .language("python")
        .execution_type("function")
        .visibility(SkillVisibility.PUBLIC)
        .status(SkillStatus.PUBLISHED)
        .build())
    
    # 注册第二个技能
    success2 = await skill_system.register(text_processor_skill)
    print(f"   第二个技能注册结果: {success2}")
    
    print("\n2. 执行技能...")
    
    # 执行加法计算技能
    calc_result = await skill_system.execute("calculator-add", {"a": 10, "b": 20})
    print(f"   加法计算结果: {calc_result.output}")
    
    # 执行文本处理技能
    text_result = await skill_system.execute("text-processor-uppercase", {"text": "hello world"})
    print(f"   文本处理结果: {text_result.output}")
    
    print("\n3. 搜索技能...")
    
    # 搜索技能
    search_results = await skill_system.search("calculator")
    print(f"   搜索'calculator'找到 {len(search_results)} 个技能:")
    for skill in search_results:
        print(f"     - {skill.name} ({skill.id})")
    
    print("\n4. 获取技能统计...")
    
    # 获取统计信息
    stats = await skill_system.get_skill_statistics()
    print(f"   总技能数: {stats['total_skills']}")
    print(f"   分类分布: {stats['categories']}")
    print(f"   语言分布: {stats['language_distribution']}")
    
    print("\n=== 基础技能系统演示完成 ===\n")


async def advanced_skill_demo():
    """
    高级技能功能演示
    """
    print("=== 高级技能功能演示 ===\n")
    
    skill_system = SkillSystem()
    
    print("1. 创建复杂技能...")
    
    # 创建一个更复杂的技能 - 数据分析技能
    data_analysis_skill = (SkillBuilder()
        .id("data-analyzer-statistics")
        .name("数据统计分析")
        .description("计算一组数字的基本统计信息")
        .version("1.0.0")
        .author("system")
        .category("data_analysis")
        .add_tag("statistics")
        .add_tag("data")
        .add_input("numbers", "array", "数字列表", required=True)
        .add_output("mean", "number", "平均值")
        .add_output("median", "number", "中位数")
        .add_output("std_dev", "number", "标准差")
        .code("""
import statistics
import math

def execute(numbers):
    '''计算数据的基本统计信息'''
    if not numbers:
        return {"mean": 0, "median": 0, "std_dev": 0}
    
    mean_val = sum(numbers) / len(numbers)
    
    # 计算中位数
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    if n % 2 == 0:
        median_val = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
    else:
        median_val = sorted_nums[n//2]
    
    # 计算标准差
    variance = sum((x - mean_val) ** 2 for x in numbers) / len(numbers)
    std_dev = math.sqrt(variance)
    
    return {
        "mean": mean_val,
        "median": median_val,
        "std_dev": std_dev
    }
""")
        .language("python")
        .execution_type("function")
        .visibility(SkillVisibility.PUBLIC)
        .status(SkillStatus.PUBLISHED)
        .build())
    
    # 注册数据分析技能
    success = await skill_system.register(data_analysis_skill)
    print(f"   数据分析技能注册结果: {success}")
    
    print("\n2. 执行复杂技能...")
    
    # 执行数据分析技能
    data_result = await skill_system.execute("data-analyzer-statistics", {"numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    print(f"   数据分析结果: {json.dumps(data_result.output, indent=2)}")
    
    print("\n3. 使用技能编排器...")
    
    # 创建技能编排器
    orchestrator = SkillOrchestrator(skill_system)
    
    # 定义技能序列
    skill_sequence = [
        {
            "skill_id": "calculator-add",
            "parameters": {"a": 10, "b": 5},
            "output_mapping": {"result": "sum_result"}
        },
        {
            "skill_id": "calculator-add", 
            "parameters": {"a": "{{sum_result}}", "b": 15},  # 使用上一步的结果
            "output_mapping": {"result": "final_result"}
        }
    ]
    
    # 执行技能序列
    sequence_result = await orchestrator.execute_sequence(skill_sequence)
    print(f"   技能序列执行结果: {sequence_result}")
    
    print("\n4. 并行执行技能...")
    
    # 准备并行执行请求
    from .interfaces import SkillExecutionRequest
    
    parallel_requests = [
        SkillExecutionRequest("calculator-add", {"a": 1, "b": 2}),
        SkillExecutionRequest("calculator-add", {"a": 3, "b": 4}),
        SkillExecutionRequest("text-processor-uppercase", {"text": "hello"}),
    ]
    
    # 并行执行
    parallel_results = await orchestrator.execute_parallel(parallel_requests)
    print(f"   并行执行结果数量: {len(parallel_results)}")
    for i, result in enumerate(parallel_results):
        print(f"     请求 {i+1}: {result.output}")
    
    print("\n=== 高级技能功能演示完成 ===\n")


async def skill_management_demo():
    """
    技能管理功能演示
    """
    print("=== 技能管理功能演示 ===\n")
    
    skill_system = SkillSystem()
    
    print("1. 创建和管理技能...")
    
    # 创建一个用于演示管理功能的技能
    management_demo_skill = (SkillBuilder()
        .id("demo-management-skill")
        .name("管理演示技能")
        .description("用于演示技能管理功能的技能")
        .version("1.0.0")
        .author("system")
        .category("demo")
        .add_tag("management")
        .add_input("input_text", "string", "输入文本", required=True)
        .add_output("output_text", "string", "输出文本")
        .code("""
def execute(input_text):
    '''简单的文本处理'''
    return {"output_text": f"Processed: {input_text}"}
""")
        .language("python")
        .execution_type("function")
        .visibility(SkillVisibility.PRIVATE)
        .status(SkillStatus.DRAFT)
        .build())
    
    # 注册技能
    success = await skill_system.register(management_demo_skill)
    print(f"   演示技能注册结果: {success}")
    
    print("\n2. 获取技能详情...")
    
    # 获取技能定义
    skill_def = await skill_system.get_skill("demo-management-skill")
    if skill_def:
        print(f"   技能名称: {skill_def.name}")
        print(f"   技能描述: {skill_def.description}")
        print(f"   技能版本: {skill_def.version}")
        print(f"   技能状态: {skill_def.status.value}")
        print(f"   技能可见性: {skill_def.visibility.value}")
    
    print("\n3. 更新技能...")
    
    # 更新技能状态
    updated_skill = (SkillBuilder()
        .id("demo-management-skill")
        .name("管理演示技能")
        .description("用于演示技能管理功能的技能 - 已更新")
        .version("1.1.0")  # 版本升级
        .author("system")
        .category("demo")
        .add_tag("management")
        .add_tag("updated")  # 添加新标签
        .add_input("input_text", "string", "输入文本", required=True)
        .add_output("output_text", "string", "输出文本")
        .code("""
def execute(input_text):
    '''更新后的文本处理'''
    return {"output_text": f"Updated Processed: {input_text}"}
""")
        .language("python")
        .execution_type("function")
        .visibility(SkillVisibility.PUBLIC)  # 改为公有
        .status(SkillStatus.PUBLISHED)  # 改为已发布
        .build())
    
    # 更新技能
    update_success = await skill_system.update_skill(updated_skill)
    print(f"   技能更新结果: {update_success}")
    
    # 验证更新
    updated_def = await skill_system.get_skill("demo-management-skill", "1.1.0")
    if updated_def:
        print(f"   更新后版本: {updated_def.version}")
        print(f"   更新后状态: {updated_def.status.value}")
        print(f"   更新后可见性: {updated_def.visibility.value}")
        print(f"   更新后标签: {updated_def.tags}")
    
    print("\n4. 执行更新后的技能...")
    
    # 执行更新后的技能
    exec_result = await skill_system.execute("demo-management-skill", {"input_text": "test"})
    print(f"   执行结果: {exec_result.output}")
    
    print("\n5. 批量操作演示...")
    
    # 批量执行
    batch_requests = [
        {"skill_id": "demo-management-skill", "parameters": {"input_text": "batch1"}},
        {"skill_id": "demo-management-skill", "parameters": {"input_text": "batch2"}},
        {"skill_id": "demo-management-skill", "parameters": {"input_text": "batch3"}},
    ]
    
    batch_results = []
    for req in batch_requests:
        result = await skill_system.execute(req["skill_id"], req["parameters"])
        batch_results.append(result)
    
    print(f"   批量执行结果数量: {len(batch_results)}")
    for i, result in enumerate(batch_results):
        print(f"     批次 {i+1}: {result.output}")
    
    print("\n=== 技能管理功能演示完成 ===\n")


async def run_all_demos():
    """
    运行所有演示
    """
    print("🚀 开始技能系统演示\n")
    
    try:
        await basic_skill_system_demo()
        await advanced_skill_demo()
        await skill_management_demo()
        
        print("🎉 所有技能系统演示完成！")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


# 如果直接运行此文件，执行演示
if __name__ == "__main__":
    asyncio.run(run_all_demos())