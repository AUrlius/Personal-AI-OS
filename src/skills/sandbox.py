"""
技能沙箱实现
基于 khazix-skills 的安全执行环境
"""
import asyncio
import logging
import tempfile
import subprocess
import os
import json
import time
from typing import Dict, Any, Optional, List
from .interfaces import SkillExecutionResult, SkillSandbox
import ast
import sys
import io
import contextlib
import resource
import signal


class SkillSandboxImpl(SkillSandbox):
    """
    技能沙箱基类实现
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def execute_in_sandbox(self, 
                                code: str, 
                                language: str, 
                                inputs: Dict[str, Any],
                                timeout: int = 30,
                                max_memory: int = 128) -> SkillExecutionResult:
        """
        在沙箱中执行代码
        """
        start_time = time.time()
        
        try:
            # 根据语言选择执行方式
            if language == "python":
                result = await self._execute_python(code, inputs, timeout, max_memory)
            elif language == "javascript":
                result = await self._execute_javascript(code, inputs, timeout, max_memory)
            elif language == "shell":
                result = await self._execute_shell(code, inputs, timeout, max_memory)
            else:
                return SkillExecutionResult(
                    success=False,
                    output=None,
                    error=f"Unsupported language: {language}",
                    execution_time=(time.time() - start_time) * 1000,
                    resources_used={},
                    logs=[f"Unsupported language: {language}"]
                )
            
            # 计算执行时间
            execution_time = (time.time() - start_time) * 1000
            result.execution_time = execution_time
            
            return result
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self.logger.error(f"Error in sandbox execution: {e}")
            return SkillExecutionResult(
                success=False,
                output=None,
                error=str(e),
                execution_time=execution_time,
                resources_used={},
                logs=[f"Sandbox execution error: {str(e)}"]
            )
    
    async def validate_code_safety(self, code: str, language: str) -> bool:
        """
        验证代码安全性
        """
        try:
            if language == "python":
                return self._validate_python_safety(code)
            elif language == "javascript":
                return self._validate_javascript_safety(code)
            elif language == "shell":
                return self._validate_shell_safety(code)
            else:
                return False
        except Exception:
            return False
    
    def _validate_python_safety(self, code: str) -> bool:
        """
        验证Python代码安全性
        """
        try:
            # 解析代码为AST
            tree = ast.parse(code)
            
            # 检查危险操作
            dangerous_nodes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    # 检查导入的危险模块
                    for alias in node.names:
                        module_name = alias.name
                        if module_name in ['os', 'sys', 'subprocess', 'shutil', 'socket', 'urllib.request', 'requests']:
                            dangerous_nodes.append(f"Dangerous import: {module_name}")
                
                elif isinstance(node, ast.ImportFrom):
                    # 检查from导入的危险模块
                    if node.module in ['os', 'sys', 'subprocess', 'shutil', 'socket', 'urllib.request', 'requests']:
                        dangerous_nodes.append(f"Dangerous import: {node.module}")
                
                elif isinstance(node, ast.Call):
                    # 检查危险函数调用
                    if isinstance(node.func, ast.Name):
                        func_name = node.func.id
                        if func_name in ['eval', 'exec', '__import__', 'compile']:
                            dangerous_nodes.append(f"Dangerous function call: {func_name}")
                    elif isinstance(node.func, ast.Attribute):
                        # 检查属性访问
                        if isinstance(node.func.value, ast.Name):
                            if node.func.value.id == 'os' and node.func.attr in ['system', 'popen', 'remove', 'rmdir', 'mknod', 'chmod', 'chown']:
                                dangerous_nodes.append(f"Dangerous os call: {node.func.attr}")
            
            # 如果发现危险节点，返回False
            if dangerous_nodes:
                self.logger.warning(f"Unsafe Python code detected: {dangerous_nodes}")
                return False
            
            return True
            
        except SyntaxError:
            # 语法错误，认为不安全
            return False
    
    def _validate_javascript_safety(self, code: str) -> bool:
        """
        验证JavaScript代码安全性
        """
        # 简单的字符串检查，实际实现需要更复杂的解析
        dangerous_patterns = [
            'require', 'import', 'eval', 'Function', 'setTimeout', 'setInterval',
            'process', 'global', 'window', 'document', 'XMLHttpRequest', 'fetch',
            '__proto__', 'constructor', 'prototype'
        ]
        
        code_lower = code.lower()
        for pattern in dangerous_patterns:
            if pattern in code_lower:
                self.logger.warning(f"Potentially unsafe JS code: {pattern}")
                return False
        
        return True
    
    def _validate_shell_safety(self, code: str) -> bool:
        """
        验证Shell代码安全性
        """
        dangerous_commands = [
            'rm', 'rmdir', 'mkfifo', 'mknod', 'chmod', 'chown', 'mv', 'cp',
            'wget', 'curl', 'nc', 'netcat', 'ssh', 'scp', 'su', 'sudo',
            'mount', 'umount', 'kill', 'killall', 'pkill'
        ]
        
        code_lower = code.lower()
        for cmd in dangerous_commands:
            # 检查命令是否作为独立词出现
            if f' {cmd} ' in code_lower or f' {cmd};' in code_lower or f'{cmd} ' in code_lower:
                self.logger.warning(f"Potentially unsafe shell command: {cmd}")
                return False
        
        return True
    
    async def _execute_python(self, code: str, inputs: Dict[str, Any], timeout: int, max_memory: int) -> SkillExecutionResult:
        """
        执行Python代码
        """
        # 验证代码安全性
        if not self._validate_python_safety(code):
            return SkillExecutionResult(
                success=False,
                output=None,
                error="Unsafe Python code detected",
                execution_time=0,
                resources_used={},
                logs=["Unsafe Python code blocked"]
            )
        
        try:
            # 创建临时文件执行
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                # 准备输入参数
                inputs_json = json.dumps(inputs)
                
                # 创建安全的执行环境
                safe_code = f"""
import json
import sys
import os

# 阻止危险导入
import builtins
original_import = builtins.__import__

def safe_import(name, *args, **kwargs):
    dangerous_modules = ['os', 'sys', 'subprocess', 'shutil', 'socket', 'urllib.request', 'requests']
    if name in dangerous_modules:
        raise ImportError(f"Import of {{name}} is not allowed")
    return original_import(name, *args, **kwargs)

builtins.__import__ = safe_import

# 输入参数
inputs = json.loads('{inputs_json}')

# 用户代码
{code}

# 假设用户代码定义了一个名为execute的函数
if 'execute' in locals() or 'execute' in globals():
    result = execute(**inputs)
    print(json.dumps({{"result": result}}))
else:
    # 如果没有execute函数，尝试执行整个代码并获取最后一行结果
    pass
"""
                f.write(safe_code)
                temp_file = f.name
            
            # 执行Python代码
            try:
                # 设置资源限制
                def set_limits():
                    # 内存限制（字节）
                    resource.setrlimit(resource.RLIMIT_AS, (max_memory * 1024 * 1024, max_memory * 1024 * 1024))
                
                result = subprocess.run(
                    [sys.executable, temp_file],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    preexec_fn=set_limits
                )
                
                if result.returncode == 0:
                    # 解析输出
                    output_str = result.stdout.strip()
                    try:
                        output = json.loads(output_str)
                    except json.JSONDecodeError:
                        # 如果输出不是JSON，返回原始输出
                        output = {"output": output_str}
                    
                    return SkillExecutionResult(
                        success=True,
                        output=output,
                        error=None,
                        execution_time=0,  # 这里会被上层函数覆盖
                        resources_used={"memory_mb": max_memory},
                        logs=[f"Python execution completed, stdout: {result.stdout}"]
                    )
                else:
                    return SkillExecutionResult(
                        success=False,
                        output=None,
                        error=f"Python execution failed: {result.stderr}",
                        execution_time=0,
                        resources_used={"memory_mb": max_memory},
                        logs=[f"Python execution error: {result.stderr}"]
                    )
            finally:
                # 清理临时文件
                os.unlink(temp_file)
                
        except subprocess.TimeoutExpired:
            return SkillExecutionResult(
                success=False,
                output=None,
                error="Execution timed out",
                execution_time=timeout * 1000,
                resources_used={"memory_mb": max_memory},
                logs=["Execution timed out"]
            )
        except Exception as e:
            return SkillExecutionResult(
                success=False,
                output=None,
                error=str(e),
                execution_time=0,
                resources_used={"memory_mb": max_memory},
                logs=[f"Python execution error: {str(e)}"]
            )
    
    async def _execute_javascript(self, code: str, inputs: Dict[str, Any], timeout: int, max_memory: int) -> SkillExecutionResult:
        """
        执行JavaScript代码
        """
        # 验证代码安全性
        if not self._validate_javascript_safety(code):
            return SkillExecutionResult(
                success=False,
                output=None,
                error="Unsafe JavaScript code detected",
                execution_time=0,
                resources_used={},
                logs=["Unsafe JavaScript code blocked"]
            )
        
        try:
            # 创建临时文件执行
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                inputs_json = json.dumps(inputs)
                
                # 创建安全的JS执行环境
                safe_js = f"""
// 安全的JavaScript执行环境
const inputs = JSON.parse('{inputs_json.replace("'", "\\'")}');

// 模拟安全的全局对象
const safeGlobal = {{
    console: {{
        log: (...args) => console.log(...args),
        error: (...args) => console.error(...args)
    }},
    setTimeout: null,  // 禁用
    setInterval: null, // 禁用
    eval: null,        // 禁用
    Function: null     // 禁用
}};

// 用户代码
{code}

// 假设用户代码定义了一个名为execute的函数
if (typeof execute !== 'undefined') {{
    const result = execute(inputs);
    console.log(JSON.stringify({{result: result}}));
}}
"""
                f.write(safe_js)
                temp_file = f.name
            
            # 使用Node.js执行
            try:
                result = subprocess.run(
                    ['node', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                if result.returncode == 0:
                    output_str = result.stdout.strip()
                    try:
                        output = json.loads(output_str)
                    except json.JSONDecodeError:
                        output = {"output": output_str}
                    
                    return SkillExecutionResult(
                        success=True,
                        output=output,
                        error=None,
                        execution_time=0,
                        resources_used={"memory_mb": max_memory},
                        logs=[f"JS execution completed, stdout: {result.stdout}"]
                    )
                else:
                    return SkillExecutionResult(
                        success=False,
                        output=None,
                        error=f"JS execution failed: {result.stderr}",
                        execution_time=0,
                        resources_used={"memory_mb": max_memory},
                        logs=[f"JS execution error: {result.stderr}"]
                    )
            finally:
                os.unlink(temp_file)
                
        except FileNotFoundError:
            return SkillExecutionResult(
                success=False,
                output=None,
                error="Node.js not found, cannot execute JavaScript",
                execution_time=0,
                resources_used={},
                logs=["Node.js not found"]
            )
        except subprocess.TimeoutExpired:
            return SkillExecutionResult(
                success=False,
                output=None,
                error="JS execution timed out",
                execution_time=timeout * 1000,
                resources_used={"memory_mb": max_memory},
                logs=["JS execution timed out"]
            )
        except Exception as e:
            return SkillExecutionResult(
                success=False,
                output=None,
                error=str(e),
                execution_time=0,
                resources_used={"memory_mb": max_memory},
                logs=[f"JS execution error: {str(e)}"]
            )
    
    async def _execute_shell(self, code: str, inputs: Dict[str, Any], timeout: int, max_memory: int) -> SkillExecutionResult:
        """
        执行Shell代码
        """
        # 验证代码安全性
        if not self._validate_shell_safety(code):
            return SkillExecutionResult(
                success=False,
                output=None,
                error="Unsafe shell code detected",
                execution_time=0,
                resources_used={},
                logs=["Unsafe shell code blocked"]
            )
        
        try:
            # 创建临时文件执行
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
                f.write("#!/bin/bash\n\n")
                
                # 添加输入参数作为环境变量
                for key, value in inputs.items():
                    # 转义特殊字符
                    escaped_value = str(value).replace("'", "'\"'\"'")
                    f.write(f"INPUT_{key.upper()}='{escaped_value}'\n")
                
                f.write("\n")
                f.write(code)
                temp_file = f.name
            
            # 设置执行权限
            os.chmod(temp_file, 0o755)
            
            try:
                result = subprocess.run(
                    ['bash', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                if result.returncode == 0:
                    return SkillExecutionResult(
                        success=True,
                        output={"stdout": result.stdout, "stderr": result.stderr},
                        error=None,
                        execution_time=0,
                        resources_used={"memory_mb": max_memory},
                        logs=[f"Shell execution completed, stdout: {result.stdout}"]
                    )
                else:
                    return SkillExecutionResult(
                        success=False,
                        output=None,
                        error=f"Shell execution failed: {result.stderr}",
                        execution_time=0,
                        resources_used={"memory_mb": max_memory},
                        logs=[f"Shell execution error: {result.stderr}"]
                    )
            finally:
                os.unlink(temp_file)
                
        except subprocess.TimeoutExpired:
            return SkillExecutionResult(
                success=False,
                output=None,
                error="Shell execution timed out",
                execution_time=timeout * 1000,
                resources_used={"memory_mb": max_memory},
                logs=["Shell execution timed out"]
            )
        except Exception as e:
            return SkillExecutionResult(
                success=False,
                output=None,
                error=str(e),
                execution_time=0,
                resources_used={"memory_mb": max_memory},
                logs=[f"Shell execution error: {str(e)}"]
            )


class PythonSandbox(SkillSandboxImpl):
    """
    Python专用沙箱
    """
    def __init__(self):
        super().__init__()
    
    async def execute_in_sandbox(self, 
                                code: str, 
                                language: str, 
                                inputs: Dict[str, Any],
                                timeout: int = 30,
                                max_memory: int = 128) -> SkillExecutionResult:
        """
        专门针对Python的执行
        """
        if language != "python":
            return SkillExecutionResult(
                success=False,
                output=None,
                error=f"Expected Python code, got {language}",
                execution_time=0,
                resources_used={},
                logs=[f"Language mismatch: expected python, got {language}"]
            )
        
        return await self._execute_python(code, inputs, timeout, max_memory)


class JavaScriptSandbox(SkillSandboxImpl):
    """
    JavaScript专用沙箱
    """
    def __init__(self):
        super().__init__()
    
    async def execute_in_sandbox(self, 
                                code: str, 
                                language: str, 
                                inputs: Dict[str, Any],
                                timeout: int = 30,
                                max_memory: int = 128) -> SkillExecutionResult:
        """
        专门针对JavaScript的执行
        """
        if language != "javascript":
            return SkillExecutionResult(
                success=False,
                output=None,
                error=f"Expected JavaScript code, got {language}",
                execution_time=0,
                resources_used={},
                logs=[f"Language mismatch: expected javascript, got {language}"]
            )
        
        return await self._execute_javascript(code, inputs, timeout, max_memory)


class DockerSandbox(SkillSandboxImpl):
    """
    Docker沙箱实现（高级）
    """
    def __init__(self):
        super().__init__()
        self.docker_enabled = self._check_docker_available()
    
    def _check_docker_available(self) -> bool:
        """
        检查Docker是否可用
        """
        try:
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    async def execute_in_sandbox(self, 
                                code: str, 
                                language: str, 
                                inputs: Dict[str, Any],
                                timeout: int = 30,
                                max_memory: int = 128) -> SkillExecutionResult:
        """
        使用Docker容器执行代码
        """
        if not self.docker_enabled:
            return SkillExecutionResult(
                success=False,
                output=None,
                error="Docker not available",
                execution_time=0,
                resources_used={},
                logs=["Docker not available"]
            )
        
        # 这里实现Docker执行逻辑
        # 暂时返回错误，因为Docker实现比较复杂
        return SkillExecutionResult(
            success=False,
            output=None,
            error="Docker sandbox not fully implemented",
            execution_time=0,
            resources_used={},
            logs=["Docker sandbox not implemented"]
        )


# 工厂函数
def create_sandbox(sandbox_type: str = "default", **kwargs) -> SkillSandbox:
    """
    创建沙箱实例
    """
    if sandbox_type == "python":
        return PythonSandbox()
    elif sandbox_type == "javascript":
        return JavaScriptSandbox()
    elif sandbox_type == "docker":
        return DockerSandbox()
    else:
        return SkillSandboxImpl()