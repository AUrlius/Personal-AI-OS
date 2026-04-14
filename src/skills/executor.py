"""
技能执行器实现
基于 khazix-skills 的执行器架构
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import subprocess
import tempfile
import os
import json
import time
from .interfaces import (
    SkillDefinition, 
    SkillExecutionRequest, 
    SkillExecutionResult, 
    SkillExecutor,
    SkillInput
)
from .sandbox import SkillSandbox, PythonSandbox, JavaScriptSandbox


class SkillExecutorImpl(SkillExecutor):
    """
    技能执行器实现
    """
    def __init__(self, sandbox: Optional[SkillSandbox] = None):
        self.sandbox = sandbox or PythonSandbox()  # 默认Python沙箱
        self.logger = logging.getLogger(__name__)
    
    async def execute(self, request: SkillExecutionRequest) -> SkillExecutionResult:
        """
        执行技能
        """
        start_time = time.time()
        
        try:
            # 获取技能定义
            from .registry import InMemorySkillRegistry
            registry = InMemorySkillRegistry()  # 这里需要从外部传入或获取
            skill_def = await self._get_skill_definition(request.skill_id)
            
            if not skill_def:
                return SkillExecutionResult(
                    success=False,
                    output=None,
                    error=f"Skill not found: {request.skill_id}",
                    execution_time=(time.time() - start_time) * 1000,
                    resources_used={},
                    logs=[f"Skill {request.skill_id} not found"]
                )
            
            # 验证输入参数
            validation_result = await self.validate_inputs(skill_def, request.parameters)
            if not validation_result:
                return SkillExecutionResult(
                    success=False,
                    output=None,
                    error="Invalid input parameters",
                    execution_time=(time.time() - start_time) * 1000,
                    resources_used={},
                    logs=["Input validation failed"]
                )
            
            # 检查权限
            permission_result = await self.check_permissions(skill_def, request.user_id)
            if not permission_result:
                return SkillExecutionResult(
                    success=False,
                    output=None,
                    error="Insufficient permissions",
                    execution_time=(time.time() - start_time) * 1000,
                    resources_used={},
                    logs=["Permission check failed"]
                )
            
            # 执行技能
            execution_result = await self._execute_skill(skill_def, request.parameters)
            
            # 计算执行时间
            execution_time = (time.time() - start_time) * 1000
            
            # 记录资源使用情况
            resources_used = {
                "execution_time_ms": execution_time,
                "cpu_time": execution_time,  # 简化处理
                "memory_mb": 0  # 简化处理
            }
            
            return SkillExecutionResult(
                success=execution_result["success"],
                output=execution_result.get("output"),
                error=execution_result.get("error"),
                execution_time=execution_time,
                resources_used=resources_used,
                logs=execution_result.get("logs", [])
            )
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self.logger.error(f"Error executing skill {request.skill_id}: {e}")
            return SkillExecutionResult(
                success=False,
                output=None,
                error=str(e),
                execution_time=execution_time,
                resources_used={},
                logs=[f"Execution error: {str(e)}"]
            )
    
    async def _get_skill_definition(self, skill_id: str) -> Optional[SkillDefinition]:
        """
        获取技能定义（这里需要实际实现从注册表获取）
        """
        # 这里需要从实际的注册表获取技能定义
        # 为了演示，返回None，实际实现需要从注册表获取
        return None
    
    async def _execute_skill(self, skill_def: SkillDefinition, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行技能的核心逻辑
        """
        try:
            # 根据技能类型选择执行方式
            if skill_def.execution_type == "function":
                return await self._execute_function(skill_def, parameters)
            elif skill_def.execution_type == "script":
                return await self._execute_script(skill_def, parameters)
            elif skill_def.execution_type == "api_call":
                return await self._execute_api_call(skill_def, parameters)
            else:
                return await self._execute_generic(skill_def, parameters)
        except Exception as e:
            self.logger.error(f"Error executing skill {skill_def.id}: {e}")
            return {
                "success": False,
                "error": str(e),
                "output": None,
                "logs": [f"Execution error: {str(e)}"]
            }
    
    async def _execute_function(self, skill_def: SkillDefinition, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行函数类型的技能
        """
        # 对于Python技能，使用沙箱执行
        if skill_def.language == "python":
            return await self.sandbox.execute_in_sandbox(
                code=skill_def.code,
                language=skill_def.language,
                inputs=parameters,
                timeout=skill_def.timeout,
                max_memory=skill_def.max_memory
            )
        else:
            # 对于其他语言，暂时返回错误
            return {
                "success": False,
                "error": f"Language {skill_def.language} not supported for function execution",
                "output": None,
                "logs": [f"Language {skill_def.language} not supported"]
            }
    
    async def _execute_script(self, skill_def: SkillDefinition, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行脚本类型的技能
        """
        # 对于脚本，同样使用沙箱执行
        return await self.sandbox.execute_in_sandbox(
            code=skill_def.code,
            language=skill_def.language,
            inputs=parameters,
            timeout=skill_def.timeout,
            max_memory=skill_def.max_memory
        )
    
    async def _execute_api_call(self, skill_def: SkillDefinition, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行API调用类型的技能
        """
        # 这里需要实现API调用逻辑
        # 暂时返回模拟结果
        try:
            # 解析API调用参数
            # 这里需要根据技能代码的具体格式来解析
            # 模拟API调用
            import aiohttp
            
            # 假设技能代码包含API端点信息
            # 实际实现需要解析skill_def.code中的API信息
            output = {"result": "API call executed successfully", "parameters": parameters}
            
            return {
                "success": True,
                "output": output,
                "error": None,
                "logs": ["API call executed"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None,
                "logs": [f"API call failed: {str(e)}"]
            }
    
    async def _execute_generic(self, skill_def: SkillDefinition, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行通用类型的技能
        """
        # 默认使用沙箱执行
        return await self.sandbox.execute_in_sandbox(
            code=skill_def.code,
            language=skill_def.language,
            inputs=parameters,
            timeout=skill_def.timeout,
            max_memory=skill_def.max_memory
        )
    
    async def validate_inputs(self, skill_def: SkillDefinition, parameters: Dict[str, Any]) -> bool:
        """
        验证输入参数
        """
        try:
            # 检查所有必需的参数是否存在
            for input_def in skill_def.inputs:
                if input_def.required and input_def.name not in parameters:
                    self.logger.warning(f"Required parameter {input_def.name} is missing")
                    return False
                
                if input_def.name in parameters:
                    param_value = parameters[input_def.name]
                    
                    # 验证参数类型
                    if not self._validate_param_type(param_value, input_def.type):
                        self.logger.warning(f"Parameter {input_def.name} has invalid type")
                        return False
                    
                    # 验证参数值
                    if input_def.validation:
                        if not self._validate_param_value(param_value, input_def.validation):
                            self.logger.warning(f"Parameter {input_def.name} has invalid value")
                            return False
            
            return True
        except Exception as e:
            self.logger.error(f"Error validating inputs: {e}")
            return False
    
    def _validate_param_type(self, value: Any, expected_type: str) -> bool:
        """
        验证参数类型
        """
        type_mapping = {
            "string": str,
            "number": (int, float),
            "boolean": bool,
            "object": dict,
            "array": list,
            "file": str  # 文件路径
        }
        
        expected_python_type = type_mapping.get(expected_type, object)
        return isinstance(value, expected_python_type)
    
    def _validate_param_value(self, value: Any, validation_rules: Dict[str, Any]) -> bool:
        """
        验证参数值
        """
        for rule, rule_value in validation_rules.items():
            if rule == "min":
                if isinstance(value, (int, float)) and value < rule_value:
                    return False
            elif rule == "max":
                if isinstance(value, (int, float)) and value > rule_value:
                    return False
            elif rule == "pattern":
                if isinstance(value, str) and not re.match(rule_value, value):
                    return False
            elif rule == "enum":
                if value not in rule_value:
                    return False
            elif rule == "min_length":
                if isinstance(value, str) and len(value) < rule_value:
                    return False
            elif rule == "max_length":
                if isinstance(value, str) and len(value) > rule_value:
                    return False
        
        return True
    
    async def check_permissions(self, skill_def: SkillDefinition, user_id: Optional[str] = None) -> bool:
        """
        检查权限
        """
        try:
            # 对于公共技能，任何人都可以执行
            if skill_def.visibility == "public":
                return True
            
            # 对于私有技能，只有创建者可以执行
            if skill_def.visibility == "private":
                if user_id == skill_def.author:
                    return True
                else:
                    return False
            
            # 对于共享技能，检查是否在共享列表中
            if skill_def.visibility == "shared":
                # 这里需要实现共享权限逻辑
                # 暂时简化处理
                return True
            
            # 检查特定权限
            required_permissions = skill_def.permissions
            if required_permissions:
                # 这里需要检查用户是否有相应权限
                # 暂时简化处理
                pass
            
            return True
        except Exception as e:
            self.logger.error(f"Error checking permissions: {e}")
            return False


class AdvancedSkillExecutor(SkillExecutorImpl):
    """
    高级技能执行器，支持更多功能
    """
    def __init__(self, sandbox: Optional[SkillSandbox] = None):
        super().__init__(sandbox)
        self.execution_cache = {}  # 执行缓存
        self.rate_limiter = {}     # 速率限制
        self.metrics_collector = {} # 指标收集
    
    async def execute(self, request: SkillExecutionRequest) -> SkillExecutionResult:
        """
        带缓存和监控的执行
        """
        # 检查缓存
        cache_key = self._generate_cache_key(request)
        if cache_key in self.execution_cache:
            cached_result = self.execution_cache[cache_key]
            # 这里可以添加缓存过期逻辑
            return cached_result
        
        # 执行技能
        result = await super().execute(request)
        
        # 缓存结果（如果适合缓存）
        if result.success and self._is_cacheable(request):
            self.execution_cache[cache_key] = result
        
        return result
    
    def _generate_cache_key(self, request: SkillExecutionRequest) -> str:
        """
        生成缓存键
        """
        import hashlib
        cache_string = f"{request.skill_id}:{json.dumps(request.parameters, sort_keys=True)}"
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def _is_cacheable(self, request: SkillExecutionRequest) -> bool:
        """
        检查是否适合缓存
        """
        # 检查技能是否标记为可缓存
        # 这里需要获取技能定义来检查
        # 暂时简化处理
        return True


# 为了支持验证，需要导入re
import re