"""
认知系统 API 接口
基于 FastAPI 的 RESTful API 服务
"""
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import asyncio
from datetime import datetime
import uuid

from .core import CognitiveSystem
from .interfaces import (
    CognitiveTask, CognitiveResult, CognitiveProfile, 
    ReasoningProcess, BiasDetectionResult
)
from .config import ConfigManager


# 请求模型
class CognitiveTaskRequest(BaseModel):
    """
    认知任务请求模型
    """
    content: str = Field(..., description="任务内容", max_length=10000)
    task_type: str = Field("analysis", description="任务类型")
    priority: str = Field("normal", description="优先级")
    complexity: str = Field("moderate", description="复杂度")
    user_id: Optional[str] = Field(None, description="用户ID")
    context: Optional[Dict[str, Any]] = Field({}, description="上下文信息")
    metadata: Optional[Dict[str, Any]] = Field({}, description="元数据")


class SkillRegisterRequest(BaseModel):
    """
    技能注册请求模型
    """
    skill_id: str = Field(..., description="技能ID")
    name: str = Field(..., description="技能名称", max_length=200)
    description: str = Field(..., description="技能描述", max_length=2000)
    version: str = Field("1.0.0", description="版本号")
    author: str = Field(..., description="作者")
    category: str = Field(..., description="分类")
    code: str = Field(..., description="技能代码", max_length=50000)
    language: str = Field("python", description="编程语言")
    execution_type: str = Field("function", description="执行类型")
    inputs: List[Dict[str, Any]] = Field([], description="输入参数定义")
    outputs: List[Dict[str, Any]] = Field([], description="输出参数定义")


class SkillExecuteRequest(BaseModel):
    """
    技能执行请求模型
    """
    skill_id: str = Field(..., description="技能ID")
    parameters: Dict[str, Any] = Field({}, description="执行参数")
    user_id: Optional[str] = Field(None, description="用户ID")


# 响应模型
class CognitiveTaskResponse(BaseModel):
    """
    认知任务响应模型
    """
    success: bool
    result: Optional[CognitiveResult] = None
    execution_time: float
    timestamp: str


class UserProfileResponse(BaseModel):
    """
    用户画像响应模型
    """
    success: bool
    profile: Optional[CognitiveProfile] = None
    timestamp: str


class SystemStatusResponse(BaseModel):
    """
    系统状态响应模型
    """
    success: bool
    status: Dict[str, Any]
    timestamp: str


class SkillRegisterResponse(BaseModel):
    """
    技能注册响应模型
    """
    success: bool
    skill_id: Optional[str] = None
    message: str
    timestamp: str


class SkillExecuteResponse(BaseModel):
    """
    技能执行响应模型
    """
    success: bool
    output: Optional[Dict[str, Any]] = None
    execution_time: float
    resources_used: Dict[str, Any]
    detected_biases: List[BiasDetectionResult]
    timestamp: str


# 创建 FastAPI 应用
app = FastAPI(
    title="Personal-AI-OS Cognitive System API",
    description="基于 nuwa-skill 架构的心智模型蒸馏系统 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局认知系统实例
cognitive_system: Optional[CognitiveSystem] = None


@app.on_event("startup")
async def startup_event():
    """
    应用启动事件
    """
    global cognitive_system
    
    # 初始化配置管理器
    config_manager = ConfigManager()
    config = config_manager.get_config()
    
    # 创建认知系统实例
    cognitive_system = CognitiveSystem(config=config)
    
    # 初始化系统
    await cognitive_system.initialize()
    
    print(f"🧠 认知系统已启动，版本: {config.version}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    应用关闭事件
    """
    global cognitive_system
    
    if cognitive_system:
        await cognitive_system.shutdown()
        print("🧠 认知系统已关闭")


@app.get("/")
async def root():
    """
    根路径
    """
    return {
        "message": "Personal-AI-OS Cognitive System API",
        "version": "1.0.0",
        "description": "基于 nuwa-skill 架构的心智模型蒸馏系统",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/v1/cognition/process", response_model=CognitiveTaskResponse)
async def process_cognitive_task(request: CognitiveTaskRequest):
    """
    处理认知任务
    """
    if not cognitive_system:
        raise HTTPException(status_code=503, detail="Cognitive system not initialized")
    
    try:
        start_time = datetime.now()
        
        # 创建认知任务
        task = CognitiveTask(
            id=f"api_task_{uuid.uuid4().hex[:8]}",
            content=request.content,
            task_type=request.task_type,
            priority=request.priority,
            complexity=request.complexity,
            metadata={
                "user_id": request.user_id,
                "context": request.context,
                "source": "api",
                "api_request_time": start_time.isoformat()
            }
        )
        
        # 执行任务
        result = await cognitive_system.process_task(task)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return CognitiveTaskResponse(
            success=result.success,
            result=result if result.success else None,
            execution_time=execution_time,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/users/{user_id}/profile", response_model=UserProfileResponse)
async def get_user_profile(user_id: str):
    """
    获取用户认知画像
    """
    if not cognitive_system:
        raise HTTPException(status_code=503, detail="Cognitive system not initialized")
    
    try:
        profile = await cognitive_system.get_cognitive_profile(user_id)
        
        return UserProfileResponse(
            success=profile is not None,
            profile=profile,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/users/{user_id}/profile/update")
async def update_user_profile(user_id: str, feedback: Dict[str, Any]):
    """
    更新用户认知画像
    """
    if not cognitive_system:
        raise HTTPException(status_code=503, detail="Cognitive system not initialized")
    
    try:
        success = await cognitive_system.update_cognitive_profile(user_id, feedback)
        
        return {
            "success": success,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/memory/store")
async def store_memory(content: str, metadata: Dict[str, Any] = None):
    """
    存储记忆
    """
    if not cognitive_system:
        raise HTTPException(status_code=503, detail="Cognitive system not initialized")
    
    try:
        memory_id = await cognitive_system.store_memory(content, metadata or {})
        
        return {
            "success": memory_id is not None,
            "memory_id": memory_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/memory/search")
async def search_memory(query: str, filters: Dict[str, Any] = None, top_k: int = 5):
    """
    搜索记忆
    """
    if not cognitive_system:
        raise HTTPException(status_code=503, detail="Cognitive system not initialized")
    
    try:
        results = await cognitive_system.search_memory(query, filters or {}, top_k)
        
        return {
            "success": True,
            "results": results,
            "count": len(results),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/system/status", response_model=SystemStatusResponse)
async def get_system_status():
    """
    获取系统状态
    """
    if not cognitive_system:
        raise HTTPException(status_code=503, detail="Cognitive system not initialized")
    
    try:
        status = await cognitive_system.get_system_status()
        
        return SystemStatusResponse(
            success=True,
            status=status,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/system/metrics")
async def get_system_metrics():
    """
    获取系统指标
    """
    if not cognitive_system:
        raise HTTPException(status_code=503, detail="Cognitive system not initialized")
    
    try:
        metrics = await cognitive_system.get_system_metrics()
        
        return {
            "success": True,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/skills/register", response_model=SkillRegisterResponse)
async def register_skill(request: SkillRegisterRequest):
    """
    注册技能
    """
    if not cognitive_system:
        raise HTTPException(status_code=503, detail="Cognitive system not initialized")
    
    try:
        success = await cognitive_system.register_skill(
            skill_id=request.skill_id,
            name=request.name,
            description=request.description,
            version=request.version,
            author=request.author,
            category=request.category,
            code=request.code,
            language=request.language,
            execution_type=request.execution_type,
            inputs=request.inputs,
            outputs=request.outputs
        )
        
        if success:
            message = f"Skill {request.skill_id} registered successfully"
        else:
            message = f"Failed to register skill {request.skill_id}"
        
        return SkillRegisterResponse(
            success=success,
            skill_id=request.skill_id if success else None,
            message=message,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/skills/execute", response_model=SkillExecuteResponse)
async def execute_skill(request: SkillExecuteRequest):
    """
    执行技能
    """
    if not cognitive_system:
        raise HTTPException(status_code=503, detail="Cognitive system not initialized")
    
    try:
        start_time = datetime.now()
        
        result = await cognitive_system.execute_skill(
            skill_id=request.skill_id,
            parameters=request.parameters,
            user_id=request.user_id
        )
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return SkillExecuteResponse(
            success=result.success,
            output=result.output if result.success else None,
            execution_time=execution_time,
            resources_used=result.resources_used,
            detected_biases=result.detected_biases,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/skills/search")
async def search_skills(
    query: Optional[str] = None,
    category: Optional[str] = None,
    author: Optional[str] = None,
    tags: Optional[str] = None,
    top_k: int = 10
):
    """
    搜索技能
    """
    if not cognitive_system:
        raise HTTPException(status_code=503, detail="Cognitive system not initialized")
    
    try:
        filters = {}
        if category:
            filters["category"] = category
        if author:
            filters["author"] = author
        if tags:
            filters["tags"] = tags.split(",")
        
        results = await cognitive_system.search_skills(query or "", filters, top_k)
        
        return {
            "success": True,
            "skills": results,
            "count": len(results),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/bias/detect")
async def detect_bias(content: str, context: Dict[str, Any] = None):
    """
    检测认知偏见
    """
    if not cognitive_system:
        raise HTTPException(status_code=503, detail="Cognitive system not initialized")
    
    try:
        task = CognitiveTask(
            id=f"bias_detect_{uuid.uuid4().hex[:8]}",
            content=content,
            task_type="bias_detection",
            priority="normal",
            complexity="moderate",
            metadata={
                "context": context or {},
                "source": "api_bias_detection"
            }
        )
        
        result = await cognitive_system.process_task(task)
        
        return {
            "success": result.success,
            "detected_biases": result.detected_biases,
            "confidence": result.confidence,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/analysis/reasoning")
async def analyze_reasoning(input_problem: str, context: Dict[str, Any] = None):
    """
    分析推理过程
    """
    if not cognitive_system:
        raise HTTPException(status_code=503, detail="Cognitive system not initialized")
    
    try:
        task = CognitiveTask(
            id=f"reasoning_analysis_{uuid.uuid4().hex[:8]}",
            content=input_problem,
            task_type="reasoning_analysis",
            priority="normal",
            complexity="moderate",
            metadata={
                "context": context or {},
                "source": "api_reasoning_analysis"
            }
        )
        
        result = await cognitive_system.process_task(task)
        
        response = {
            "success": result.success,
            "input_problem": input_problem,
            "timestamp": datetime.now().isoformat()
        }
        
        if result.reasoning_process:
            response["reasoning_analysis"] = {
                "strategy": result.reasoning_process.reasoning_strategy,
                "steps_count": len(result.reasoning_process.steps),
                "steps": [
                    {
                        "step_number": step.step_number,
                        "content": step.content,
                        "reasoning_type": step.reasoning_type,
                        "confidence": step.confidence
                    }
                    for step in result.reasoning_process.steps
                ],
                "conclusion": result.reasoning_process.conclusion,
                "confidence": result.reasoning_process.confidence
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


@app.get("/api/v1/users/{user_id}/insights")
async def get_cognitive_insights(user_id: str):
    """
    获取认知洞察
    """
    if not cognitive_system:
        raise HTTPException(status_code=503, detail="Cognitive system not initialized")
    
    try:
        insights = await cognitive_system.get_cognitive_insights(user_id)
        
        return {
            "success": insights is not None,
            "insights": insights,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/train/model")
async def train_cognitive_model(training_data: List[Dict[str, Any]]):
    """
    训练认知模型
    """
    if not cognitive_system:
        raise HTTPException(status_code=503, detail="Cognitive system not initialized")
    
    try:
        success = await cognitive_system.train_model(training_data)
        
        return {
            "success": success,
            "message": "Cognitive model training completed" if success else "Training failed",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 错误处理
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "success": False,
        "error": "Endpoint not found",
        "timestamp": datetime.now().isoformat()
    }


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "success": False,
        "error": "Internal server error",
        "detail": str(exc),
        "timestamp": datetime.now().isoformat()
    }


def create_app(config_path: Optional[str] = None) -> FastAPI:
    """
    创建应用实例（用于外部导入）
    """
    # 这里可以传入配置路径
    return app


# 用于直接运行的入口点
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)