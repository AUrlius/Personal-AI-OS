"""
技能验证器
用于验证技能定义的安全性和正确性
"""
import re
import ast
from typing import Dict, Any, List
from ..interfaces import SkillDefinition, SkillInput, SkillStatus, SkillVisibility


class SkillValidator:
    """
    技能验证器
    """
    def __init__(self):
        self.dangerous_patterns = {
            "python": [
                r'import\s+os\b',
                r'import\s+sys\b', 
                r'import\s+subprocess\b',
                r'import\s+shutil\b',
                r'import\s+socket\b',
                r'import\s+urllib\.request\b',
                r'import\s+requests\b',
                r'eval\s*\(',
                r'exec\s*\(',
                r'__import__\s*\(',
                r'compile\s*\(',
                r'open\s*\([^)]*["\'][wWaAtT]["\']',
                r'os\.system\s*\(',
                r'os\.popen\s*\(',
                r'os\.remove\s*\(',
                r'os\.rmdir\s*\(',
                r'os\.mknod\s*\(',
                r'os\.chmod\s*\(',
                r'os\.chown\s*\(',
            ],
            "javascript": [
                r'require\s*\(',
                r'import\s+',
                r'eval\s*\(',
                r'Function\s*\(',
                r'setTimeout\s*\(',
                r'setInterval\s*\(',
                r'process\.',
                r'global\.',
                r'window\.',
                r'document\.',
                r'XMLHttpRequest\.',
                r'fetch\s*\(',
                r'__proto__',
                r'constructor',
                r'prototype',
            ],
            "shell": [
                r'\brm\s+',
                r'\brmdir\s+',
                r'\bmknod\s+',
                r'\bmkdir\s+',
                r'\bchmod\s+',
                r'\bchown\s+',
                r'\bmv\s+',
                r'\bcp\s+',
                r'\bwget\s+',
                r'\bcurl\s+',
                r'\bnc\s+',
                r'\bnetcat\s+',
                r'\bssh\s+',
                r'\bscp\s+',
                r'\bsu\s+',
                r'\bsudo\s+',
                r'\bmount\s+',
                r'\bumount\s+',
                r'\bkill\s+',
                r'\bkillall\s+',
                r'\bpkill\s+',
            ]
        }
    
    async def validate_skill_definition(self, skill_def: SkillDefinition) -> bool:
        """
        验证技能定义
        """
        try:
            # 验证基本字段
            if not self._validate_basic_fields(skill_def):
                return False
            
            # 验证输入参数
            if not self._validate_inputs(skill_def.inputs):
                return False
            
            # 验证输出参数
            if not self._validate_outputs(skill_def.outputs):
                return False
            
            # 验证代码安全性
            if not await self._validate_code_safety(skill_def.code, skill_def.language):
                return False
            
            # 验证依赖
            if not self._validate_dependencies(skill_def.dependencies):
                return False
            
            # 验证权限
            if not self._validate_permissions(skill_def.permissions):
                return False
            
            # 验证元数据
            if not self._validate_metadata(skill_def.metadata):
                return False
            
            return True
            
        except Exception as e:
            print(f"Error validating skill definition: {e}")
            return False
    
    def _validate_basic_fields(self, skill_def: SkillDefinition) -> bool:
        """
        验证基本字段
        """
        # 验证ID格式
        if not skill_def.id or not re.match(r'^[a-zA-Z0-9_-]+$', skill_def.id):
            print(f"Invalid skill ID: {skill_def.id}")
            return False
        
        # 验证名称
        if not skill_def.name or len(skill_def.name.strip()) == 0:
            print("Skill name is required")
            return False
        
        # 验证描述
        if not skill_def.description or len(skill_def.description.strip()) == 0:
            print("Skill description is required")
            return False
        
        # 验证版本格式
        if not re.match(r'^\d+\.\d+\.\d+$', skill_def.version):
            print(f"Invalid version format: {skill_def.version}")
            return False
        
        # 验证作者
        if not skill_def.author or len(skill_def.author.strip()) == 0:
            print("Skill author is required")
            return False
        
        # 验证分类
        if not skill_def.category or len(skill_def.category.strip()) == 0:
            print("Skill category is required")
            return False
        
        # 验证语言
        if skill_def.language not in ["python", "javascript", "shell", "plugin"]:
            print(f"Invalid language: {skill_def.language}")
            return False
        
        # 验证执行类型
        if skill_def.execution_type not in ["function", "script", "api_call", "plugin"]:
            print(f"Invalid execution type: {skill_def.execution_type}")
            return False
        
        # 验证可见性
        if skill_def.visibility not in [SkillVisibility.PRIVATE, SkillVisibility.PUBLIC, SkillVisibility.SHARED]:
            print(f"Invalid visibility: {skill_def.visibility}")
            return False
        
        # 验证状态
        if skill_def.status not in [SkillStatus.DRAFT, SkillStatus.PUBLISHED, SkillStatus.DISABLED, SkillStatus.DEPRECATED]:
            print(f"Invalid status: {skill_def.status}")
            return False
        
        # 验证超时时间
        if skill_def.timeout <= 0 or skill_def.timeout > 300:  # 最大5分钟
            print(f"Invalid timeout: {skill_def.timeout}")
            return False
        
        # 验证内存限制
        if skill_def.max_memory <= 0 or skill_def.max_memory > 1024:  # 最大1GB
            print(f"Invalid memory limit: {skill_def.max_memory}")
            return False
        
        return True
    
    def _validate_inputs(self, inputs: List[SkillInput]) -> bool:
        """
        验证输入参数
        """
        for inp in inputs:
            if not inp.name or not inp.type:
                print(f"Invalid input definition: {inp}")
                return False
            
            # 验证输入类型
            valid_types = ["string", "number", "boolean", "object", "array", "file"]
            if inp.type not in valid_types:
                print(f"Invalid input type: {inp.type}")
                return False
            
            # 验证默认值类型
            if inp.default is not None and not self._validate_type(inp.default, inp.type):
                print(f"Invalid default value type for input {inp.name}")
                return False
        
        return True
    
    def _validate_outputs(self, outputs: List[SkillInput]) -> bool:
        """
        验证输出参数
        """
        for out in outputs:
            if not out.name or not out.type:
                print(f"Invalid output definition: {out}")
                return False
            
            # 验证输出类型
            valid_types = ["string", "number", "boolean", "object", "array", "file"]
            if out.type not in valid_types:
                print(f"Invalid output type: {out.type}")
                return False
        
        return True
    
    async def _validate_code_safety(self, code: str, language: str) -> bool:
        """
        验证代码安全性
        """
        if language == "python":
            return self._validate_python_code_safety(code)
        elif language == "javascript":
            return self._validate_javascript_code_safety(code)
        elif language == "shell":
            return self._validate_shell_code_safety(code)
        else:
            # 对于其他语言，使用通用检查
            return self._validate_generic_code_safety(code)
    
    def _validate_python_code_safety(self, code: str) -> bool:
        """
        验证Python代码安全性
        """
        try:
            # 解析代码为AST
            tree = ast.parse(code)
            
            # 检查危险操作
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    # 检查导入的危险模块
                    for alias in node.names:
                        module_name = alias.name
                        if module_name in ['os', 'sys', 'subprocess', 'shutil', 'socket', 'urllib.request', 'requests']:
                            print(f"Dangerous import detected: {module_name}")
                            return False
                
                elif isinstance(node, ast.ImportFrom):
                    # 检查from导入的危险模块
                    if node.module in ['os', 'sys', 'subprocess', 'shutil', 'socket', 'urllib.request', 'requests']:
                        print(f"Dangerous import detected: {node.module}")
                        return False
                
                elif isinstance(node, ast.Call):
                    # 检查危险函数调用
                    if isinstance(node.func, ast.Name):
                        func_name = node.func.id
                        if func_name in ['eval', 'exec', '__import__', 'compile']:
                            print(f"Dangerous function call detected: {func_name}")
                            return False
                    elif isinstance(node.func, ast.Attribute):
                        # 检查属性访问
                        if isinstance(node.func.value, ast.Name):
                            if node.func.value.id == 'os' and node.func.attr in ['system', 'popen', 'remove', 'rmdir', 'mknod', 'chmod', 'chown']:
                                print(f"Dangerous os call detected: {node.func.attr}")
                                return False
            
            # 检查危险模式
            code_lower = code.lower()
            for pattern in self.dangerous_patterns["python"]:
                if re.search(pattern, code_lower):
                    print(f"Dangerous pattern detected in Python code: {pattern}")
                    return False
            
            return True
            
        except SyntaxError:
            print("Syntax error in Python code")
            return False
    
    def _validate_javascript_code_safety(self, code: str) -> bool:
        """
        验证JavaScript代码安全性
        """
        # 简单的字符串检查
        code_lower = code.lower()
        for pattern in self.dangerous_patterns["javascript"]:
            if re.search(pattern, code_lower):
                print(f"Dangerous pattern detected in JavaScript code: {pattern}")
                return False
        
        return True
    
    def _validate_shell_code_safety(self, code: str) -> bool:
        """
        验证Shell代码安全性
        """
        # 简单的字符串检查
        code_lower = code.lower()
        for pattern in self.dangerous_patterns["shell"]:
            if re.search(pattern, code_lower):
                print(f"Dangerous pattern detected in Shell code: {pattern}")
                return False
        
        return True
    
    def _validate_generic_code_safety(self, code: str) -> bool:
        """
        验证通用代码安全性
        """
        # 对于不支持的语言，进行通用检查
        dangerous_patterns = [
            r'rm\s+', r'rmdir\s+', r'mknod\s+', r'chmod\s+', r'chown\s+',
            r'eval\s*\(', r'exec\s*\(', r'__import__\s*\(',
            r'import\s+os\b', r'import\s+sys\b', r'import\s+subprocess\b'
        ]
        
        code_lower = code.lower()
        for pattern in dangerous_patterns:
            if re.search(pattern, code_lower):
                print(f"Dangerous pattern detected in code: {pattern}")
                return False
        
        return True
    
    def _validate_dependencies(self, dependencies: List[str]) -> bool:
        """
        验证依赖
        """
        for dep in dependencies:
            if not re.match(r'^[a-zA-Z0-9_-]+$', dep):
                print(f"Invalid dependency ID: {dep}")
                return False
        
        return True
    
    def _validate_permissions(self, permissions: List[str]) -> bool:
        """
        验证权限
        """
        valid_permissions = [
            "network", "filesystem", "database", "camera", 
            "microphone", "location", "clipboard", "notifications"
        ]
        
        for perm in permissions:
            if perm not in valid_permissions:
                print(f"Invalid permission: {perm}")
                return False
        
        return True
    
    def _validate_metadata(self, metadata: Dict[str, Any]) -> bool:
        """
        验证元数据
        """
        # 元许任何元数据，但检查是否有潜在的安全问题
        if not isinstance(metadata, dict):
            print("Metadata must be a dictionary")
            return False
        
        # 检查元数据大小（限制为1MB）
        import json
        try:
            metadata_size = len(json.dumps(metadata))
            if metadata_size > 1024 * 1024:  # 1MB
                print("Metadata too large")
                return False
        except TypeError:
            print("Metadata contains non-serializable objects")
            return False
        
        return True
    
    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """
        验证值的类型
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
    
    async def validate_parameters(self, skill_def: SkillDefinition, parameters: Dict[str, Any]) -> bool:
        """
        验证执行参数
        """
        try:
            # 检查所有必需的参数是否存在
            for input_def in skill_def.inputs:
                if input_def.required and input_def.name not in parameters:
                    print(f"Required parameter {input_def.name} is missing")
                    return False
                
                if input_def.name in parameters:
                    param_value = parameters[input_def.name]
                    
                    # 验证参数类型
                    if not self._validate_type(param_value, input_def.type):
                        print(f"Parameter {input_def.name} has invalid type")
                        return False
                    
                    # 验证参数值
                    if input_def.validation:
                        if not self._validate_param_value(param_value, input_def.validation):
                            print(f"Parameter {input_def.name} has invalid value")
                            return False
            
            return True
        except Exception as e:
            print(f"Error validating parameters: {e}")
            return False
    
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