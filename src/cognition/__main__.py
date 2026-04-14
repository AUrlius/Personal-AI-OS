"""
认知系统主入口模块
基于 nuwa-skill 的心智模型蒸馏架构
"""
import asyncio
import logging
import argparse
from pathlib import Path
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from .core import CognitiveSystem
from .config_manager import get_config_manager, CognitiveSystemConfig
from .api import create_app


def setup_logging(log_level: str = "INFO"):
    """
    设置日志配置
    """
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('cognitive_system.log'),
            logging.StreamHandler()
        ]
    )


async def initialize_cognitive_system(config_path: str = None) -> CognitiveSystem:
    """
    初始化认知系统
    """
    logger = logging.getLogger(__name__)
    
    # 获取配置管理器
    config_manager = get_config_manager(config_path)
    config = config_manager.get_config()
    
    # 创建认知系统实例
    cognitive_system = CognitiveSystem(config=config)
    
    # 初始化系统
    await cognitive_system.initialize()
    
    logger.info("Cognitive system initialized successfully")
    return cognitive_system


async def run_interactive_mode():
    """
    运行交互模式
    """
    print("🧠=== Personal-AI-OS 认知系统交互模式 ===🧠\n")
    print("输入 'help' 查看命令，'quit' 退出\n")
    
    cognitive_system = await initialize_cognitive_system()
    
    while True:
        try:
            user_input = input("🧠认知系统> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("再见！感谢使用认知系统～")
                break
            elif user_input.lower() == 'help':
                print("""
可用命令:
  help                    - 显示此帮助信息
  quit/exit/q            - 退出系统
  analyze <内容>          - 分析指定内容
  reason <问题>           - 对问题进行推理
  profile <用户ID>        - 查看用户认知画像
  bias-check <内容>       - 检查内容中的偏见
  memory-store <内容>     - 存储记忆
  memory-search <查询>     - 搜索记忆
  status                  - 系统状态
  config                  - 显示当前配置
                """)
            elif user_input.lower().startswith('analyze '):
                content = user_input[8:].strip()
                if content:
                    from .interfaces import CognitiveTask
                    task = CognitiveTask(
                        id=f"interactive_analyze_{int(datetime.now().timestamp())}",
                        content=content,
                        task_type="analysis",
                        priority="normal",
                        complexity="moderate"
                    )
                    result = await cognitive_system.process_task(task)
                    print(f"📊 分析结果: {result.output}")
                    if result.confidence:
                        print(f"📈 置信度: {result.confidence:.2f}")
                    if result.detected_biases:
                        print(f"⚖️ 检测到 {len(result.detected_biases)} 个偏见:")
                        for bias in result.detected_biases:
                            print(f"   - {bias.type}: 严重程度 {bias.severity:.2f}")
                else:
                    print("⚠️  请输入要分析的内容")
            elif user_input.lower().startswith('reason '):
                problem = user_input[7:].strip()
                if problem:
                    from .interfaces import CognitiveTask
                    task = CognitiveTask(
                        id=f"interactive_reason_{int(datetime.now().timestamp())}",
                        content=problem,
                        task_type="reasoning",
                        priority="normal",
                        complexity="moderate"
                    )
                    result = await cognitive_system.process_task(task)
                    print(f"🔍 推理结果: {result.output}")
                    if result.reasoning_process:
                        print(f"📝 推理步骤数: {len(result.reasoning_process.steps)}")
                        print(f"🎯 推理策略: {result.reasoning_process.reasoning_strategy}")
                        print(f"📈 推理置信度: {result.reasoning_process.confidence:.2f}")
                else:
                    print("⚠️  请输入要推理的问题")
            elif user_input.lower().startswith('profile '):
                user_id = user_input[8:].strip()
                if user_id:
                    profile = await cognitive_system.get_cognitive_profile(user_id)
                    if profile:
                        print(f"👤 用户 {user_id} 的认知画像:")
                        print(f"   推理风格: {profile.reasoning_style}")
                        print(f"   决策方式: {profile.decision_making}")
                        print(f"   学习偏好: {profile.learning_preference}")
                        print(f"   注意力跨度: {profile.attention_span} 分钟")
                        print(f"   处理速度: {profile.processing_speed}")
                        print(f"   记忆强度: {profile.memory_strength}")
                        if profile.bias_tendencies:
                            print(f"   偏见倾向: {dict(list(profile.bias_tendencies.items())[:3])}")
                    else:
                        print(f"❌ 未找到用户 {user_id} 的认知画像")
                else:
                    print("⚠️  请输入用户ID")
            elif user_input.lower().startswith('bias-check '):
                content = user_input[11:].strip()
                if content:
                    from .interfaces import CognitiveTask
                    task = CognitiveTask(
                        id=f"interactive_bias_check_{int(datetime.now().timestamp())}",
                        content=content,
                        task_type="bias_detection",
                        priority="normal",
                        complexity="moderate"
                    )
                    result = await cognitive_system.process_task(task)
                    if result.detected_biases:
                        print("⚠️ 检测到认知偏见:")
                        for bias in result.detected_biases:
                            print(f"   - {bias.type}: 严重程度 {bias.severity:.2f}")
                            print(f"     建议: {bias.suggestion[:80]}...")
                    else:
                        print("✅ 未检测到显著认知偏见")
                else:
                    print("⚠️  请输入要检查偏见的内容")
            elif user_input.lower().startswith('memory-store '):
                content = user_input[13:].strip()
                if content:
                    from .interfaces import CognitiveTask
                    task = CognitiveTask(
                        id=f"memory_store_{int(datetime.now().timestamp())}",
                        content=content,
                        task_type="memory_operation",
                        priority="normal",
                        complexity="simple",
                        metadata={"operation": "store"}
                    )
                    result = await cognitive_system.process_task(task)
                    if result.success:
                        print("✅ 记忆存储成功")
                    else:
                        print(f"❌ 记忆存储失败: {result.error}")
                else:
                    print("⚠️  请输入要存储的内容")
            elif user_input.lower().startswith('memory-search '):
                query = user_input[14:].strip()
                if query:
                    from .interfaces import CognitiveTask
                    task = CognitiveTask(
                        id=f"memory_search_{int(datetime.now().timestamp())}",
                        content=query,
                        task_type="memory_operation",
                        priority="normal",
                        complexity="simple",
                        metadata={"operation": "search"}
                    )
                    result = await cognitive_system.process_task(task)
                    if result.success and result.output:
                        print(f"🔍 搜索结果: {result.output}")
                    else:
                        print(f"❌ 记忆搜索失败: {result.error}")
                else:
                    print("⚠️  请输入要搜索的查询")
            elif user_input.lower() == 'status':
                status = await cognitive_system.get_system_status()
                print("📋 系统状态:")
                for key, value in status.items():
                    print(f"   {key}: {value}")
            elif user_input.lower() == 'config':
                config = cognitive_system.config
                print("⚙️ 当前配置:")
                print(f"   模型维度: {config.model.embedding_dim}")
                print(f"   推理最大步数: {config.reasoning.max_steps}")
                print(f"   记忆最大项目数: {config.memory.max_memory_items}")
                print(f"   最大并发任务数: {config.performance.max_concurrent_tasks}")
            else:
                if user_input.strip():
                    # 默认作为分析任务处理
                    from .interfaces import CognitiveTask
                    task = CognitiveTask(
                        id=f"interactive_default_{int(datetime.now().timestamp())}",
                        content=user_input,
                        task_type="analysis",
                        priority="normal",
                        complexity="moderate"
                    )
                    result = await cognitive_system.process_task(task)
                    print(f"📊 结果: {result.output}")
                    if result.confidence:
                        print(f"📈 置信度: {result.confidence:.2f}")
                    if result.detected_biases:
                        print(f"⚠️ 检测到 {len(result.detected_biases)} 个偏见")
                else:
                    print("请输入要处理的内容")
        
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")
            import traceback
            traceback.print_exc()


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description='Personal-AI-OS Cognitive System')
    parser.add_argument('--mode', choices=['interactive', 'api', 'batch'], default='interactive',
                       help='运行模式 (interactive/api/batch)')
    parser.add_argument('--config', type=str, help='配置文件路径')
    parser.add_argument('--port', type=int, default=8000, help='API服务端口')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='API服务主机')
    parser.add_argument('--log-level', type=str, default='INFO', help='日志级别')
    
    args = parser.parse_args()
    
    # 设置日志
    setup_logging(args.log_level)
    
    if args.mode == 'interactive':
        asyncio.run(run_interactive_mode())
    elif args.mode == 'api':
        # 启动API服务
        from .api import create_app
        app = create_app(config_path=args.config)
        
        import uvicorn
        uvicorn.run(
            app, 
            host=args.host, 
            port=args.port,
            log_level=args.log_level.lower()
        )
    elif args.mode == 'batch':
        print("批处理模式尚未实现")
        # 这里可以添加批处理功能
    else:
        print(f"未知模式: {args.mode}")
        parser.print_help()


if __name__ == "__main__":
    main()