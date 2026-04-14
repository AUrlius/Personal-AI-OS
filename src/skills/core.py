"""
技能系统核心实现
基于 khazix-skills 的完整技能框架
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import uuid
from .interfaces import (
    SkillDefinition, 
    SkillExecutionRequest, 
    SkillExecutionResult, 
    SkillSystemABC,
    SkillInput,
    SkillOutput,
    SkillStatus,
    SkillVisibility
)
from .registry import InMemorySkillRegistry, SkillRegistry
from .executor import SkillExecutorImpl, AdvancedSkillExecutor
from .sandbox import SkillSandboxImpl, create_sandbox
from .utils.validator import SkillValidator


class SkillSystem(SkillSystemABC):
    """
    技能系统核心实现
    基于 khazix-skills 架构设计
    """
    def __init__(self, 
                 registry: Optional[SkillRegistry] = None,
                 executor: Optional[SkillExecutorImpl] = None,
                 sandbox: Optional[SkillSandboxImpl] = None):
        self.registry = registry or InMemorySkillRegistry()
        self.executor = executor or AdvancedSkillExecutor()
        self.sandbox = sandbox or create_sandbox()
        self.logger = logging.getLogger(__name__)
        self.validator = SkillValidator()
        
        # 初始化默认技能
        self._initialize_default_skills()
    
    def _initialize_default_skills(self):
        """
        初始化默认技能
        """
        # 这里可以注册一些内置技能
        pass
    
    async def register(self, skill_def: SkillDefinition) -> bool:
        """
        注册技能
        """
        try:
            # 验证技能定义
            if not await self.validator.validate_skill_definition(skill_def):
                self.logger.error(f"Skill validation failed: {skill_def.id}")
                return False
            
            # 注册到注册表
            success = await self.registry.register_skill(skill_def)
            
            if success:
                self.logger.info(f"Skill registered successfully: {skill_def.id} (v{skill_def.version})")
                
                # 触发注册后事件
                await self._on_skill_registered(skill_def)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error registering skill {skill_def.id}: {e}")
            return False
    
    async def _on_skill_registered(self, skill_def: SkillDefinition):
        """
        技能注册后事件
        """
        # 可以在这里触发通知、缓存更新等操作
        pass
    
    async def execute(self, skill_id: str, parameters: Dict[str, Any], user_id: Optional[str] = None) -> SkillExecutionResult:
        """
        执行技能
        """
        try:
            # 创建执行请求
            request = SkillExecutionRequest(
                skill_id=skill_id,
                parameters=parameters,
                user_id=user_id
            )
            
            # 通过执行器执行
            result = await self.executor.execute(request)
            
            self.logger.info(f"Skill execution completed: {skill_id}, success: {result.success}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error executing skill {skill_id}: {e}")
            return SkillExecutionResult(
                success=False,
                output=None,
                error=str(e),
                execution_time=0,
                resources_used={},
                logs=[f"Execution error: {str(e)}"]
            )
    
    async def search(self, query: str) -> List[SkillDefinition]:
        """
        搜索技能
        """
        try:
            results = await self.registry.search_skills(query)
            self.logger.info(f"Search completed for '{query}', found {len(results)} skills")
            return results
        except Exception as e:
            self.logger.error(f"Error searching skills for '{query}': {e}")
            return []
    
    async def list_available(self) -> List[SkillDefinition]:
        """
        列出可用技能
        """
        try:
            # 获取所有已发布的公共技能
            available_skills = await self.registry.list_skills(status=SkillStatus.PUBLISHED)
            self.logger.info(f"Listed {len(available_skills)} available skills")
            return available_skills
        except Exception as e:
            self.logger.error(f"Error listing available skills: {e}")
            return []
    
    async def update_skill(self, skill_def: SkillDefinition) -> bool:
        """
        更新技能
        """
        try:
            # 验证技能定义
            if not await self.validator.validate_skill_definition(skill_def):
                self.logger.error(f"Skill validation failed: {skill_def.id}")
                return False
            
            # 更新注册表
            success = await self.registry.update_skill(skill_def)
            
            if success:
                self.logger.info(f"Skill updated successfully: {skill_def.id} (v{skill_def.version})")
                
                # 触发更新后事件
                await self._on_skill_updated(skill_def)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error updating skill {skill_def.id}: {e}")
            return False
    
    async def _on_skill_updated(self, skill_def: SkillDefinition):
        """
        技能更新后事件
        """
        # 可以在这里触发通知、缓存清除等操作
        pass
    
    async def delete_skill(self, skill_id: str) -> bool:
        """
        删除技能
        """
        try:
            success = await self.registry.delete_skill(skill_id)
            
            if success:
                self.logger.info(f"Skill deleted successfully: {skill_id}")
                
                # 触发删除后事件
                await self._on_skill_deleted(skill_id)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error deleting skill {skill_id}: {e}")
            return False
    
    async def _on_skill_deleted(self, skill_id: str):
        """
        技能删除后事件
        """
        # 可以在这里触发通知、依赖检查等操作
        pass
    
    async def get_skill(self, skill_id: str, version: Optional[str] = None) -> Optional[SkillDefinition]:
        """
        获取技能定义
        """
        try:
            skill_def = await self.registry.get_skill(skill_id, version)
            if skill_def:
                self.logger.info(f"Retrieved skill definition: {skill_id}")
            else:
                self.logger.warning(f"Skill not found: {skill_id}")
            return skill_def
        except Exception as e:
            self.logger.error(f"Error retrieving skill {skill_id}: {e}")
            return None
    
    async def batch_execute(self, requests: List[SkillExecutionRequest]) -> List[SkillExecutionResult]:
        """
        批量执行技能
        """
        results = []
        
        for request in requests:
            result = await self.execute(request.skill_id, request.parameters, request.user_id)
            results.append(result)
        
        return results
    
    async def get_skill_statistics(self) -> Dict[str, Any]:
        """
        获取技能统计信息
        """
        try:
            all_skills = await self.list_available()
            
            stats = {
                "total_skills": len(all_skills),
                "categories": {},
                "authors": {},
                "status_distribution": {},
                "language_distribution": {},
                "average_rating": 0.0  # 简化处理
            }
            
            # 统计分类分布
            for skill in all_skills:
                # 分类统计
                category = skill.category
                if category not in stats["categories"]:
                    stats["categories"][category] = 0
                stats["categories"][category] += 1
                
                # 作者统计
                author = skill.author
                if author not in stats["authors"]:
                    stats["authors"][author] = 0
                stats["authors"][author] += 1
                
                # 状态统计
                status = skill.status.value
                if status not in stats["status_distribution"]:
                    stats["status_distribution"][status] = 0
                stats["status_distribution"][status] += 1
                
                # 语言统计
                language = skill.language
                if language not in stats["language_distribution"]:
                    stats["language_distribution"][language] = 0
                stats["language_distribution"][language] += 1
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting skill statistics: {e}")
            return {}
    
    async def validate_and_execute(self, skill_id: str, parameters: Dict[str, Any], user_id: Optional[str] = None) -> SkillExecutionResult:
        """
        验证并执行技能
        """
        # 获取技能定义
        skill_def = await self.get_skill(skill_id)
        if not skill_def:
            return SkillExecutionResult(
                success=False,
                output=None,
                error=f"Skill not found: {skill_id}",
                execution_time=0,
                resources_used={},
                logs=[f"Skill {skill_id} not found"]
            )
        
        # 验证参数
        if not await self.executor.validate_inputs(skill_def, parameters):
            return SkillExecutionResult(
                success=False,
                output=None,
                error="Invalid input parameters",
                execution_time=0,
                resources_used={},
                logs=["Input validation failed"]
            )
        
        # 执行技能
        return await self.execute(skill_id, parameters, user_id)


class SkillBuilder:
    """
    技能构建器 - 简化技能创建过程
    """
    def __init__(self):
        self.reset()
    
    def reset(self):
        """
        重置构建器
        """
        self._id = None
        self._name = ""
        self._description = ""
        self._version = "1.0.0"
        self._author = ""
        self._category = "utility"
        self._tags = []
        self._inputs = []
        self._outputs = []
        self._dependencies = []
        self._code = ""
        self._language = "python"
        self._execution_type = "function"
        self._visibility = SkillVisibility.PRIVATE
        self._status = SkillStatus.DRAFT
        self._metadata = {}
        self._permissions = []
        self._timeout = 30
        self._max_memory = 128
    
    def id(self, skill_id: str):
        """
        设置技能ID
        """
        self._id = skill_id
        return self
    
    def name(self, name: str):
        """
        设置技能名称
        """
        self._name = name
        return self
    
    def description(self, description: str):
        """
        设置技能描述
        """
        self._description = description
        return self
    
    def version(self, version: str):
        """
        设置技能版本
        """
        self._version = version
        return self
    
    def author(self, author: str):
        """
        设置技能作者
        """
        self._author = author
        return self
    
    def category(self, category: str):
        """
        设置技能分类
        """
        self._category = category
        return self
    
    def tags(self, tags: List[str]):
        """
        设置技能标签
        """
        self._tags = tags
        return self
    
    def add_tag(self, tag: str):
        """
        添加技能标签
        """
        if tag not in self._tags:
            self._tags.append(tag)
        return self
    
    def inputs(self, inputs: List[SkillInput]):
        """
        设置技能输入
        """
        self._inputs = inputs
        return self
    
    def add_input(self, name: str, type: str, description: str, required: bool = True, default: Optional[Any] = None):
        """
        添加技能输入
        """
        input_def = SkillInput(
            name=name,
            type=type,
            description=description,
            required=required,
            default=default
        )
        self._inputs.append(input_def)
        return self
    
    def outputs(self, outputs: List[SkillOutput]):
        """
        设置技能输出
        """
        self._outputs = outputs
        return self
    
    def add_output(self, name: str, type: str, description: str):
        """
        添加技能输出
        """
        output_def = SkillOutput(
            name=name,
            type=type,
            description=description
        )
        self._outputs.append(output_def)
        return self
    
    def code(self, code: str):
        """
        设置技能代码
        """
        self._code = code
        return self
    
    def language(self, language: str):
        """
        设置技能语言
        """
        self._language = language
        return self
    
    def execution_type(self, execution_type: str):
        """
        设置执行类型
        """
        self._execution_type = execution_type
        return self
    
    def visibility(self, visibility: SkillVisibility):
        """
        设置可见性
        """
        self._visibility = visibility
        return self
    
    def status(self, status: SkillStatus):
        """
        设置状态
        """
        self._status = status
        return self
    
    def permissions(self, permissions: List[str]):
        """
        设置权限
        """
        self._permissions = permissions
        return self
    
    def timeout(self, timeout: int):
        """
        设置超时时间
        """
        self._timeout = timeout
        return self
    
    def max_memory(self, max_memory: int):
        """
        设置最大内存
        """
        self._max_memory = max_memory
        return self
    
    def build(self) -> SkillDefinition:
        """
        构建技能定义
        """
        if not self._id:
            self._id = str(uuid.uuid4())
        
        if not self._author:
            self._author = "system"
        
        skill_def = SkillDefinition(
            id=self._id,
            name=self._name,
            description=self._description,
            version=self._version,
            author=self._author,
            category=self._category,
            tags=self._tags,
            inputs=self._inputs,
            outputs=self._outputs,
            dependencies=self._dependencies,
            code=self._code,
            language=self._language,
            execution_type=self._execution_type,
            visibility=self._visibility,
            status=self._status,
            metadata=self._metadata,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            permissions=self._permissions,
            timeout=self._timeout,
            max_memory=self._max_memory
        )
        
        # 重置构建器
        self.reset()
        
        return skill_def


class SkillOrchestrator:
    """
    技能编排器 - 管理多个技能的协同执行
    """
    def __init__(self, skill_system: SkillSystem):
        self.skill_system = skill_system
        self.logger = logging.getLogger(__name__)
    
    async def execute_sequence(self, 
                              skill_sequence: List[Dict[str, Any]], 
                              initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        执行技能序列
        skill_sequence: [
            {"skill_id": "...", "parameters": {...}, "output_mapping": {...}},
            ...
        ]
        """
        context = initial_context or {}
        
        for i, step in enumerate(skill_sequence):
            skill_id = step["skill_id"]
            parameters = step.get("parameters", {})
            output_mapping = step.get("output_mapping", {})
            
            # 将参数中的变量替换为上下文值
            resolved_params = self._resolve_variables(parameters, context)
            
            # 执行技能
            result = await self.skill_system.execute(skill_id, resolved_params)
            
            if not result.success:
                self.logger.error(f"Skill sequence failed at step {i}: {skill_id}, error: {result.error}")
                return {
                    "success": False,
                    "error": f"Step {i} failed: {result.error}",
                    "context": context,
                    "step": i
                }
            
            # 将输出映射到上下文
            if result.output:
                for output_key, context_key in output_mapping.items():
                    if output_key in result.output:
                        context[context_key] = result.output[output_key]
            
            self.logger.info(f"Completed step {i}: {skill_id}")
        
        return {
            "success": True,
            "context": context,
            "final_output": context
        }
    
    def _resolve_variables(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析参数中的变量
        支持 {{variable_name}} 格式
        """
        import re
        
        def replace_vars(obj):
            if isinstance(obj, str):
                # 匹配 {{variable_name}} 格式
                pattern = r'\{\{([^}]+)\}\}'
                matches = re.findall(pattern, obj)
                
                result = obj
                for var_name in matches:
                    if var_name in context:
                        # 简单替换
                        result = result.replace(f"{{{{{var_name}}}}}", str(context[var_name]))
                
                return result
            elif isinstance(obj, dict):
                return {k: replace_vars(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_vars(item) for item in obj]
            else:
                return obj
        
        return replace_vars(parameters)
    
    async def execute_parallel(self, skill_requests: List[SkillExecutionRequest]) -> List[SkillExecutionResult]:
        """
        并行执行多个技能
        """
        tasks = []
        for request in skill_requests:
            task = self.skill_system.execute(request.skill_id, request.parameters, request.user_id)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理可能的异常
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append(SkillExecutionResult(
                    success=False,
                    output=None,
                    error=str(result),
                    execution_time=0,
                    resources_used={},
                    logs=[f"Execution exception: {str(result)}"]
                ))
            else:
                processed_results.append(result)
        
        return processed_results


# 为了支持JSON序列化，添加必要的导入
import re