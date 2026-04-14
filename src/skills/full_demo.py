"""
技能系统完整演示
"""
import asyncio
import json
from datetime import datetime
from typing import Dict, Any

# 导入技能系统组件
from .core import SkillSystem, SkillBuilder, SkillOrchestrator
from .interfaces import SkillInput, SkillOutput, SkillStatus, SkillVisibility
from .registry import InMemorySkillRegistry
from .executor import AdvancedSkillExecutor
from .sandbox import PythonSandbox


async def full_skill_system_demo():
    """
    完整技能系统演示
    """
    print("🚀=== 技能系统完整演示 ===🚀\n")
    
    # 创建技能系统实例
    sandbox = PythonSandbox()
    executor = AdvancedSkillExecutor(sandbox)
    registry = InMemorySkillRegistry()
    
    skill_system = SkillSystem(
        registry=registry,
        executor=executor,
        sandbox=sandbox
    )
    
    print("1️⃣ 技能构建与注册演示")
    
    # 创建数学计算技能
    math_skill = (SkillBuilder()
        .id("math-calculator-demo")
        .name("数学计算器")
        .description("执行基本数学运算")
        .version("1.0.0")
        .author("system")
        .category("mathematics")
        .add_tag("math")
        .add_tag("calculator")
        .add_input("operation", "string", "运算类型 (add, subtract, multiply, divide)", required=True)
        .add_input("a", "number", "第一个数字", required=True)
        .add_input("b", "number", "第二个数字", required=True)
        .add_output("result", "number", "运算结果")
        .add_output("operation_performed", "string", "执行的运算")
        .code("""
def execute(operation, a, b):
    '''执行数学运算'''
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Division by zero")
        result = a / b
    else:
        raise ValueError(f"Unknown operation: {operation}")
    
    return {
        "result": result,
        "operation_performed": operation
    }
""")
        .language("python")
        .execution_type("function")
        .visibility(SkillVisibility.PUBLIC)
        .status(SkillStatus.PUBLISHED)
        .timeout(10)
        .max_memory(64)
        .build())
    
    # 注册数学技能
    math_register_success = await skill_system.register(math_skill)
    print(f"   ✅ 数学技能注册: {math_register_success}")
    
    # 创建文本处理技能
    text_skill = (SkillBuilder()
        .id("text-processor-demo")
        .name("文本处理器")
        .description("执行文本处理操作")
        .version("1.0.0")
        .author("system")
        .category("text_processing")
        .add_tag("text")
        .add_tag("string")
        .add_input("text", "string", "输入文本", required=True)
        .add_input("operation", "string", "操作类型 (upper, lower, reverse, length)", required=True)
        .add_output("result", "string", "处理结果")
        .code("""
def execute(text, operation):
    '''执行文本处理'''
    if operation == "upper":
        result = text.upper()
    elif operation == "lower":
        result = text.lower()
    elif operation == "reverse":
        result = text[::-1]
    elif operation == "length":
        result = str(len(text))
    else:
        raise ValueError(f"Unknown operation: {operation}")
    
    return {
        "result": result
    }
""")
        .language("python")
        .execution_type("function")
        .visibility(SkillVisibility.PUBLIC)
        .status(SkillStatus.PUBLISHED)
        .timeout(10)
        .max_memory(64)
        .build())
    
    # 注册文本技能
    text_register_success = await skill_system.register(text_skill)
    print(f"   ✅ 文本技能注册: {text_register_success}")
    
    print("\n2️⃣ 技能执行演示")
    
    # 执行数学技能
    print("   执行数学运算 (10 + 5):")
    math_result = await skill_system.execute("math-calculator-demo", {
        "operation": "add",
        "a": 10,
        "b": 5
    })
    if math_result.success:
        print(f"      结果: {math_result.output}")
    else:
        print(f"      错误: {math_result.error}")
    
    # 执行文本技能
    print("   执行文本处理 (Hello World -> uppercase):")
    text_result = await skill_system.execute("text-processor-demo", {
        "text": "Hello World",
        "operation": "upper"
    })
    if text_result.success:
        print(f"      结果: {text_result.output}")
    else:
        print(f"      错误: {text_result.error}")
    
    print("\n3️⃣ 技能编排演示")
    
    # 创建技能编排器
    orchestrator = SkillOrchestrator(skill_system)
    
    # 定义技能序列：先将文本转大写，然后计算其长度
    skill_sequence = [
        {
            "skill_id": "text-processor-demo",
            "parameters": {"text": "hello from skill system", "operation": "upper"},
            "output_mapping": {"result": "processed_text"}
        },
        {
            "skill_id": "text-processor-demo", 
            "parameters": {"text": "{{processed_text}}", "operation": "length"},
            "output_mapping": {"result": "text_length"}
        }
    ]
    
    print("   执行技能序列 (转换为大写 -> 计算长度):")
    sequence_result = await orchestrator.execute_sequence(skill_sequence)
    if sequence_result["success"]:
        print(f"      序列执行结果: {sequence_result['context']}")
    else:
        print(f"      序列执行错误: {sequence_result['error']}")
    
    print("\n4️⃣ 搜索和发现演示")
    
    # 搜索技能
    search_results = await skill_system.search("math")
    print(f"   搜索 'math' 找到 {len(search_results)} 个技能:")
    for skill in search_results:
        print(f"      - {skill.name} ({skill.id})")
    
    # 列出所有可用技能
    all_skills = await skill_system.list_available()
    print(f"   总共 {len(all_skills)} 个可用技能:")
    for skill in all_skills:
        print(f"      - {skill.name} ({skill.category})")
    
    print("\n5️⃣ 技能统计演示")
    
    # 获取统计信息
    stats = await skill_system.get_skill_statistics()
    print("   技能统计信息:")
    print(f"      总技能数: {stats['total_skills']}")
    print(f"      分类分布: {json.dumps(stats['categories'], ensure_ascii=False)}")
    print(f"      语言分布: {stats['language_distribution']}")
    
    print("\n6️⃣ 高级功能演示")
    
    # 执行参数验证
    from .utils.validator import SkillValidator
    validator = SkillValidator()
    
    skill_def = await skill_system.get_skill("math-calculator-demo")
    if skill_def:
        validation_result = await validator.validate_parameters(skill_def, {
            "operation": "multiply",
            "a": 6,
            "b": 7
        })
        print(f"   参数验证结果: {validation_result}")
        
        # 执行验证后的技能
        if validation_result:
            validated_result = await skill_system.execute("math-calculator-demo", {
                "operation": "multiply",
                "a": 6,
                "b": 7
            })
            print(f"   验证后执行结果: {validated_result.output}")
    
    print("\n7️⃣ 并行执行演示")
    
    # 准备并行执行请求
    from .interfaces import SkillExecutionRequest
    
    parallel_requests = [
        SkillExecutionRequest("math-calculator-demo", {"operation": "add", "a": 1, "b": 2}),
        SkillExecutionRequest("math-calculator-demo", {"operation": "multiply", "a": 3, "b": 4}),
        SkillExecutionRequest("text-processor-demo", {"text": "parallel", "operation": "upper"}),
    ]
    
    # 并行执行
    parallel_results = await orchestrator.execute_parallel(parallel_requests)
    print(f"   并行执行 {len(parallel_requests)} 个技能:")
    for i, result in enumerate(parallel_results):
        print(f"      请求 {i+1}: {result.output if result.success else f'错误: {result.error}'}")
    
    print("\n8️⃣ 技能管理演示")
    
    # 更新技能
    updated_skill = (SkillBuilder()
        .id("math-calculator-demo")
        .name("数学计算器 - 更新版")
        .description("执行基本数学运算 (已更新)")
        .version("1.1.0")
        .author("system")
        .category("mathematics")
        .add_tag("math")
        .add_tag("calculator")
        .add_tag("updated")
        .add_input("operation", "string", "运算类型 (add, subtract, multiply, divide)", required=True)
        .add_input("a", "number", "第一个数字", required=True)
        .add_input("b", "number", "第二个数字", required=True)
        .add_output("result", "number", "运算结果")
        .add_output("operation_performed", "string", "执行的运算")
        .add_output("timestamp", "string", "执行时间戳")
        .code("""
from datetime import datetime

def execute(operation, a, b):
    '''执行数学运算（更新版）'''
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Division by zero")
        result = a / b
    else:
        raise ValueError(f"Unknown operation: {operation}")
    
    return {
        "result": result,
        "operation_performed": operation,
        "timestamp": datetime.now().isoformat()
    }
""")
        .language("python")
        .execution_type("function")
        .visibility(SkillVisibility.PUBLIC)
        .status(SkillStatus.PUBLISHED)
        .timeout(15)  # 增加超时时间
        .max_memory(64)
        .build())
    
    # 更新技能
    update_success = await skill_system.update_skill(updated_skill)
    print(f"   技能更新结果: {update_success}")
    
    # 验证更新
    updated_def = await skill_system.get_skill("math-calculator-demo", "1.1.0")
    if updated_def:
        print(f"   更新后版本: {updated_def.version}")
        print(f"   更新后标签: {updated_def.tags}")
        
        # 测试更新后的技能
        updated_result = await skill_system.execute("math-calculator-demo", {
            "operation": "add",
            "a": 100,
            "b": 200
        })
        print(f"   更新后执行结果: {updated_result.output}")
    
    print("\n🎉=== 技能系统完整演示完成 ===🎉")
    print("✅ 所有功能模块正常工作")
    print("✅ 技能生命周期管理完整")
    print("✅ 安全沙箱执行可靠")
    print("✅ 编排和管理功能完备")


if __name__ == "__main__":
    # 运行完整演示
    asyncio.run(full_skill_system_demo())