"""
技能系统接口定义
基于 khazix-skills 的技能框架架构
"""
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, Optional, List, Dict, Any, Union, Awaitable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import json


class SkillStatus(Enum):
    """
    技能状态枚举
    """
    DRAFT = "draft"           # 草稿状态
    PUBLISHED = "published"   # 已发布
    DISABLED = "disabled"     # 已禁用
    DEPRECATED = "deprecated" # 已废弃


class SkillVisibility(Enum):
    """
    技能可见性
    """
    PRIVATE = "private"     # 私有
    PUBLIC = "public"       # 公开
    SHARED = "shared"       # 共享


@dataclass
class SkillInput:
    """
    技能输入参数定义
    """
    name: str
    type: str  # "string", "number", "boolean", "object", "array", "file"
    description: str
    required: bool = True
    default: Optional[Any] = None
    validation: Optional[Dict[str, Any]] = None  # 如: {"min": 0, "max": 100, "pattern": r"^[\w]+$"}


@dataclass
class SkillOutput:
    """
    技能输出定义
    """
    name: str
    type: str
    description: str
    required: bool = True


@dataclass
class SkillDefinition:
    """
    技能定义
    """
    id: str
    name: str
    description: str
    version: str
    author: str
    category: str
    tags: List[str]
    
    inputs: List[SkillInput]
    outputs: List[SkillOutput]
    dependencies: List[str]  # 依赖的其他技能ID
    
    code: str  # 技能代码
    language: str  # "python", "javascript", "shell", "plugin"
    execution_type: str  # "function", "script", "api_call", "plugin"
    
    visibility: SkillVisibility
    status: SkillStatus
    
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    # 权限相关
    permissions: List[str]  # ["network", "filesystem", "database"]
    timeout: int = 30  # 执行超时时间（秒）
    max_memory: int = 128  # 最大内存使用（MB）


@dataclass
class SkillExecutionRequest:
    """
    技能执行请求
    """
    skill_id: str
    parameters: Dict[str, Any]
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None  # 执行上下文


@dataclass
class SkillExecutionResult:
    """
    技能执行结果
    """
    success: bool
    output: Optional[Dict[str, Any]]
    error: Optional[str]
    execution_time: float  # 执行时间（毫秒）
    resources_used: Dict[str, Any]  # 资源使用情况
    logs: List[str]


@runtime_checkable
class SkillRegistry(Protocol):
    """
    技能注册表接口
    """
    async def register_skill(self, skill_def: SkillDefinition) -> bool:
        """注册技能"""
        ...
    
    async def get_skill(self, skill_id: str, version: Optional[str] = None) -> Optional[SkillDefinition]:
        """获取技能定义"""
        ...
    
    async def update_skill(self, skill_def: SkillDefinition) -> bool:
        """更新技能"""
        ...
    
    async def delete_skill(self, skill_id: str) -> bool:
        """删除技能"""
        ...
    
    async def list_skills(self, 
                         category: Optional[str] = None, 
                         tags: Optional[List[str]] = None,
                         status: Optional[SkillStatus] = None,
                         visibility: Optional[SkillVisibility] = None,
                         search_query: Optional[str] = None) -> List[SkillDefinition]:
        """列出技能"""
        ...
    
    async def search_skills(self, query: str) -> List[SkillDefinition]:
        """搜索技能"""
        ...


@runtime_checkable
class SkillExecutor(Protocol):
    """
    技能执行器接口
    """
    async def execute(self, request: SkillExecutionRequest) -> SkillExecutionResult:
        """执行技能"""
        ...
    
    async def validate_inputs(self, skill_def: SkillDefinition, parameters: Dict[str, Any]) -> bool:
        """验证输入参数"""
        ...
    
    async def check_permissions(self, skill_def: SkillDefinition, user_id: Optional[str] = None) -> bool:
        """检查权限"""
        ...


@runtime_checkable
class SkillSandbox(Protocol):
    """
    技能沙箱接口
    """
    async def execute_in_sandbox(self, 
                                code: str, 
                                language: str, 
                                inputs: Dict[str, Any],
                                timeout: int = 30,
                                max_memory: int = 128) -> SkillExecutionResult:
        """在沙箱中执行代码"""
        ...
    
    async def validate_code_safety(self, code: str, language: str) -> bool:
        """验证代码安全性"""
        ...


class SkillSystemABC(ABC):
    """
    技能系统抽象基类
    """
    @abstractmethod
    async def register(self, skill_def: SkillDefinition) -> bool:
        """注册技能"""
        pass
    
    @abstractmethod
    async def execute(self, skill_id: str, parameters: Dict[str, Any], user_id: Optional[str] = None) -> SkillExecutionResult:
        """执行技能"""
        pass
    
    @abstractmethod
    async def search(self, query: str) -> List[SkillDefinition]:
        """搜索技能"""
        pass
    
    @abstractmethod
    async def list_available(self) -> List[SkillDefinition]:
        """列出可用技能"""
        pass