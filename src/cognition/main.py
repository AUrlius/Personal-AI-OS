"""
认知系统主入口
基于 nuwa-skill 的心智模型蒸馏架构
"""
import asyncio
import logging
import argparse
from typing import Dict, Any, Optional
from datetime import datetime
import json
import os
from .core import CognitiveSystem
from .interfaces import CognitiveTask, CognitiveResult
from .config import CognitiveSystemConfig, ConfigManager


def setup_logging(level: str = "INFO"):
    """
    设置日志配置
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('cognitive_system.log'),
            logging.StreamHandler()
        ]
    )


async def initialize_cognitive_system(config_path: Optional[str] = None) -> CognitiveSystem:
    """
    初始化认知系统
    """
    logger = logging.getLogger(__name__)
    
    # 加载配置
    config_manager = ConfigManager(config_path)
    config = config_manager.get_config()
    
    # 创建认知系统实例
    cognitive_system = CognitiveSystem(config=config)
    
    # 初始化系统
    await cognitive_system.initialize()
    
    logger.info("认知系统初始化完成")
    return cognitive_system


async def process_cognitive_request(content: str, task_type: str = "analysis", user_id: str = "default_user") -> Dict[str, Any]:
    """
    处理认知请求
    """
    cognitive_system = await initialize_cognitive_system()
    
    # 创建认知任务
    task = CognitiveTask(
        id=f"request_{int(datetime.now().timestamp())}",
        content=content,
        task_type=task_type,
        priority="normal",
        complexity="moderate",
        metadata={
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }
    )
    
    # 执行任务
    result = await cognitive_system.process_task(task)
    
    # 格式化结果
    response = {
        "success": result.success,
        "output": result.output,
        "confidence": result.confidence,
        "execution_time": result.execution_time,
        "resources_used": result.resources_used
    }
    
    if result.reasoning_process:
        response["reasoning_steps"] = len(result.reasoning_process.steps)
        response["reasoning_strategy"] = result.reasoning_process.reasoning_strategy
    
    if result.detected_biases:
        response["detected_biases"] = [
            {
                "type": bias.type,
                "severity": bias.severity,
                "suggestion": bias.suggestion
            }
            for bias in result.detected_biases
        ]
    
    return response


async def run_interactive_mode():
    """
    运行交互模式
    """
    print("🧠 欢迎使用 Personal-AI-OS 认知系统!")
    print("输入 'quit' 或 'exit' 退出，输入 'help' 查看帮助")
    
    cognitive_system = await initialize_cognitive_system()
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            elif user_input.lower() == 'help':
                print("""
可用命令:
  help                    - 显示此帮助信息
  quit/exit/q            - 退出系统
  profile <user_id>      - 获取用户认知画像
  analyze <内容>         - 执行分析任务
  reason <问题>          - 执行推理任务
  bias-check <内容>      - 检查偏见
  status                 - 系统状态
                """)
            elif user_input.lower().startswith('analyze '):
                content = user_input[8:].strip()
                if content:
                    task = CognitiveTask(
                        id=f"interactive_analyze_{int(datetime.now().timestamp())}",
                        content=content,
                        task_type="analysis",
                        priority="normal",
                        complexity="moderate"
                    )
                    result = await cognitive_system.process_task(task)
                    print(f"分析结果: {result.output}")
                    if result.confidence:
                        print(f"置信度: {result.confidence:.2f}")
                    if result.detected_biases:
                        print(f"检测到偏见: {len(result.detected_biases)} 个")
                else:
                    print("请提供要分析的内容")
            elif user_input.lower().startswith('reason '):
                content = user_input[7:].strip()
                if content:
                    task = CognitiveTask(
                        id=f"interactive_reason_{int(datetime.now().timestamp())}",
                        content=content,
                        task_type="reasoning", 
                        priority="normal",
                        complexity="moderate"
                    )
                    result = await cognitive_system.process_task(task)
                    print(f"推理结果: {result.output}")
                    if result.reasoning_process:
                        print(f"推理步骤数: {len(result.reasoning_process.steps)}")
                else:
                    print("请提供要推理的问题")
            elif user_input.lower().startswith('bias-check '):
                content = user_input[11:].strip()
                if content:
                    task = CognitiveTask(
                        id=f"interactive_bias_check_{int(datetime.now().timestamp())}",
                        content=content,
                        task_type="bias_detection",
                        priority="normal", 
                        complexity="moderate"
                    )
                    result = await cognitive_system.process_task(task)
                    if result.detected_biases:
                        print("检测到认知偏见:")
                        for bias in result.detected_biases:
                            print(f"  - {bias.type}: 严重程度 {bias.severity:.2f}")
                            print(f"    建议: {bias.suggestion}")
                    else:
                        print("未检测到显著认知偏见")
                else:
                    print("请提供要检查偏见的内容")
            elif user_input.lower() == 'status':
                status = await cognitive_system.get_system_status()
                print(f"系统状态: {status}")
            elif user_input.lower().startswith('profile '):
                user_id = user_input[8:].strip()
                if user_id:
                    profile = await cognitive_system.get_cognitive_profile(user_id)
                    if profile:
                        print(f"用户 {user_id} 的认知画像:")
                        print(f"  推理风格: {profile.reasoning_style}")
                        print(f"  决策方式: {profile.decision_making}")
                        print(f"  学习偏好: {profile.learning_preference}")
                        print(f"  注意力跨度: {profile.attention_span} 分钟")
                        print(f"  处理速度: {profile.processing_speed}")
                        if profile.bias_tendencies:
                            print(f"  偏见倾向: {dict(list(profile.bias_tendencies.items())[:3])}")
                    else:
                        print(f"未找到用户 {user_id} 的认知画像")
                else:
                    print("请提供用户ID")
            else:
                # 默认作为分析任务处理
                if user_input:
                    task = CognitiveTask(
                        id=f"interactive_default_{int(datetime.now().timestamp())}",
                        content=user_input,
                        task_type="analysis",
                        priority="normal",
                        complexity="moderate"
                    )
                    result = await cognitive_system.process_task(task)
                    print(f"结果: {result.output}")
                    if result.confidence:
                        print(f"置信度: {result.confidence:.2f}")
                else:
                    print("请输入要处理的内容")
        
        except KeyboardInterrupt:
            print("\n再见！")
            break
        except Exception as e:
            print(f"错误: {e}")
            import traceback
            traceback.print_exc()


async def run_batch_processing(tasks_file: str, output_file: str):
    """
    运行批量处理
    """
    logger = logging.getLogger(__name__)
    
    cognitive_system = await initialize_cognitive_system()
    
    # 读取任务文件
    with open(tasks_file, 'r', encoding='utf-8') as f:
        tasks_data = json.load(f)
    
    results = []
    
    for i, task_data in enumerate(tasks_data):
        try:
            task = CognitiveTask(**task_data)
            result = await cognitive_system.process_task(task)
            
            result_dict = {
                "task_id": task.id,
                "success": result.success,
                "output": result.output,
                "confidence": result.confidence,
                "execution_time": result.execution_time,
                "resources_used": result.resources_used
            }
            
            if result.reasoning_process:
                result_dict["reasoning_strategy"] = result.reasoning_process.reasoning_strategy
                result_dict["reasoning_steps"] = len(result.reasoning_process.steps)
            
            if result.detected_biases:
                result_dict["detected_biases"] = [
                    {
                        "type": bias.type,
                        "severity": bias.severity,
                        "suggestion": bias.suggestion
                    }
                    for bias in result.detected_biases
                ]
            
            results.append(result_dict)
            
            logger.info(f"批量处理进度: {i+1}/{len(tasks_data)}")
            
        except Exception as e:
            logger.error(f"处理任务 {task_data.get('id', 'unknown')} 时出错: {e}")
            results.append({
                "task_id": task_data.get("id", "unknown"),
                "success": False,
                "error": str(e)
            })
    
    # 保存结果
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    logger.info(f"批量处理完成，结果保存到: {output_file}")


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description='Personal-AI-OS 认知系统')
    parser.add_argument('--mode', choices=['interactive', 'batch', 'api'], default='interactive',
                       help='运行模式 (interactive/batch/api)')
    parser.add_argument('--config', type=str, help='配置文件路径')
    parser.add_argument('--tasks-file', type=str, help='批量任务文件路径')
    parser.add_argument('--output-file', type=str, help='批量处理输出文件路径')
    parser.add_argument('--log-level', type=str, default='INFO', 
                       help='日志级别 (DEBUG/INFO/WARNING/ERROR)')
    
    args = parser.parse_args()
    
    # 设置日志
    setup_logging(args.log_level)
    
    if args.mode == 'interactive':
        asyncio.run(run_interactive_mode())
    elif args.mode == 'batch':
        if not args.tasks_file or not args.output_file:
            print("批量模式需要指定 --tasks-file 和 --output-file")
            return
        asyncio.run(run_batch_processing(args.tasks_file, args.output_file))
    elif args.mode == 'api':
        # API 模式 - 启动 Web 服务
        from .api import create_app
        app = create_app(config_path=args.config)
        
        # 从环境变量或配置获取端口
        port = int(os.getenv('PORT', 8080))
        host = os.getenv('HOST', '0.0.0.0')
        
        import uvicorn
        uvicorn.run(app, host=host, port=port)
    else:
        print(f"未知模式: {args.mode}")
        parser.print_help()


# API 服务入口（如果使用 FastAPI）
def create_api_server(config_path: Optional[str] = None):
    """
    创建 API 服务
    """
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    from typing import Optional
    
    app = FastAPI(title="Personal-AI-OS Cognitive System API", version="1.0.0")
    
    # 全局认知系统实例
    cognitive_system = None
    
    @app.on_event('startup')
    async def startup_event():
        nonlocal cognitive_system
        cognitive_system = await initialize_cognitive_system(config_path)
    
    class CognitiveRequest(BaseModel):
        content: str
        task_type: str = "analysis"
        priority: str = "normal"
        complexity: str = "moderate"
        user_id: Optional[str] = "default_user"
        context: Optional[Dict[str, Any]] = {}
    
    @app.post("/api/v1/cognition/process")
    async def process_cognition(request: CognitiveRequest):
        try:
            task = CognitiveTask(
                id=f"api_task_{int(datetime.now().timestamp())}",
                content=request.content,
                task_type=request.task_type,
                priority=request.priority,
                complexity=request.complexity,
                metadata={
                    "user_id": request.user_id,
                    "context": request.context,
                    "source": "api"
                }
            )
            
            result = await cognitive_system.process_task(task)
            
            response = {
                "success": result.success,
                "output": result.output,
                "confidence": result.confidence,
                "execution_time": result.execution_time,
                "resources_used": result.resources_used
            }
            
            if result.reasoning_process:
                response["reasoning_process"] = {
                    "strategy": result.reasoning_process.reasoning_strategy,
                    "steps_count": len(result.reasoning_process.steps),
                    "conclusion": result.reasoning_process.conclusion
                }
            
            if result.detected_biases:
                response["detected_biases"] = [
                    {
                        "type": bias.type,
                        "severity": bias.severity,
                        "suggestion": bias.suggestion,
                        "confidence": bias.confidence
                    }
                    for bias in result.detected_biases
                ]
            
            return response
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/v1/system/status")
    async def get_system_status():
        try:
            status = await cognitive_system.get_system_status()
            return {"success": True, "status": status}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/v1/users/{user_id}/profile")
    async def get_user_profile(user_id: str):
        try:
            profile = await cognitive_system.get_cognitive_profile(user_id)
            if profile:
                return {"success": True, "profile": profile}
            else:
                raise HTTPException(status_code=404, detail="User profile not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return app


if __name__ == "__main__":
    main()