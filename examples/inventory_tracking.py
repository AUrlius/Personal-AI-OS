#!/usr/bin/env python3
"""
Personal-AI-OS 集成仓库资源清单跟踪脚本

此脚本用于跟踪和验证我们集成的仓库资源
"""

import os
import yaml
from pathlib import Path

class IntegrationInventory:
    def __init__(self, base_dir="./"):
        self.base_dir = Path(base_dir)
        self.integration_dir = self.base_dir / "integration"
        
    def scan_integrated_repos(self):
        """扫描集成的仓库"""
        if not self.integration_dir.exists():
            print(f"集成目录不存在: {self.integration_dir}")
            return {}
            
        repos = {}
        for item in self.integration_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                repos[item.name] = {
                    'path': str(item.absolute()),
                    'exists': item.exists(),
                    'size': self._get_dir_size(item),
                    'files': self._count_files(item)
                }
        return repos
    
    def _get_dir_size(self, path):
        """获取目录大小"""
        total = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    pass
        return total
    
    def _count_files(self, path):
        """统计文件数量"""
        count = 0
        for _, _, filenames in os.walk(path):
            count += len(filenames)
        return count
    
    def generate_report(self):
        """生成集成报告"""
        repos = self.scan_integrated_repos()
        
        print("="*60)
        print("Personal-AI-OS 集成仓库资源清单")
        print("="*60)
        print(f"基础目录: {self.base_dir.absolute()}")
        print(f"集成目录: {self.integration_dir.absolute()}")
        print(f"集成仓库数量: {len(repos)}")
        print()
        
        for name, info in repos.items():
            print(f"📦 {name}")
            print(f"   路径: {info['path']}")
            print(f"   状态: {'✅ 存在' if info['exists'] else '❌ 不存在'}")
            print(f"   大小: {self._format_size(info['size'])}")
            print(f"   文件数: {info['files']}")
            print()
        
        print("="*60)
        print("核心集成模块功能:")
        print("- mempalace: 记忆系统 (AI 记忆管理)")
        print("- khazix-skills: 技能系统 (可扩展技能框架)") 
        print("- career-ops: 职业助手 (求职规划系统)")
        print("- nuwa-skill: 认知模型 (心智蒸馏)")
        print("- gbrain: AI大脑 (OpenClaw/Hermes)")
        print("- graphify: 知识图谱 (关系提取)")
        print("- hermes-agent: Agent框架 (多Agent协作)")
        print("- NLP-notes: NLP资源 (学习和实践)")
        print("="*60)
    
    def _format_size(self, size_bytes):
        """格式化文件大小"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"

def main():
    """主函数"""
    inventory = IntegrationInventory("./")
    inventory.generate_report()

if __name__ == "__main__":
    main()