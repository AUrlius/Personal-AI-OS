"""
技能注册表实现
基于 khazix-skills 的注册表架构
"""
import asyncio
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from .interfaces import SkillDefinition, SkillRegistry, SkillStatus, SkillVisibility
import uuid
import re


class InMemorySkillRegistry(SkillRegistry):
    """
    基于内存的技能注册表实现
    """
    def __init__(self):
        self.skills: Dict[str, Dict[str, SkillDefinition]] = {}  # skill_id -> {version -> skill_def}
        self.skill_index: Dict[str, List[str]] = {  # category -> [skill_ids]
            'all': [],
            'productivity': [],
            'development': [],
            'communication': [],
            'utility': [],
            'ai': [],
            'automation': []
        }
        self.tag_index: Dict[str, List[str]] = {}  # tag -> [skill_ids]
        self.author_index: Dict[str, List[str]] = {}  # author -> [skill_ids]
        self.search_index: Dict[str, List[str]] = {}  # keyword -> [skill_ids]
        self.logger = logging.getLogger(__name__)
        
    async def register_skill(self, skill_def: SkillDefinition) -> bool:
        """
        注册技能
        """
        try:
            # 验证技能定义
            if not await self._validate_skill_definition(skill_def):
                self.logger.error(f"Invalid skill definition: {skill_def.id}")
                return False
            
            # 如果技能ID不存在，创建新的版本记录
            if skill_def.id not in self.skills:
                self.skills[skill_def.id] = {}
            
            # 存储技能定义
            self.skills[skill_def.id][skill_def.version] = skill_def
            
            # 更新索引
            await self._update_indexes(skill_def)
            
            self.logger.info(f"Skill registered: {skill_def.id} (v{skill_def.version})")
            return True
            
        except Exception as e:
            self.logger.error(f"Error registering skill {skill_def.id}: {e}")
            return False
    
    async def _validate_skill_definition(self, skill_def: SkillDefinition) -> bool:
        """
        验证技能定义
        """
        # 检查必填字段
        if not skill_def.id or not skill_def.name or not skill_def.code:
            return False
        
        # 检查ID格式（字母数字下划线横线）
        if not re.match(r'^[a-zA-Z0-9_-]+$', skill_def.id):
            return False
        
        # 检查版本格式
        if not re.match(r'^\d+\.\d+\.\d+$', skill_def.version):
            return False
        
        # 检查输入输出参数
        for inp in skill_def.inputs:
            if not inp.name or not inp.type:
                return False
        
        for out in skill_def.outputs:
            if not out.name or not out.type:
                return False
        
        # 检查依赖是否存在
        for dep_id in skill_def.dependencies:
            if dep_id != skill_def.id:  # 不检查自身依赖
                # 检查依赖是否已注册（这里简化处理，实际应该检查依赖是否满足）
                pass
        
        return True
    
    async def _update_indexes(self, skill_def: SkillDefinition):
        """
        更新索引
        """
        skill_id = skill_def.id
        
        # 更新分类索引
        if skill_def.category not in self.skill_index:
            self.skill_index[skill_def.category] = []
        if skill_id not in self.skill_index[skill_def.category]:
            self.skill_index[skill_def.category].append(skill_id)
        
        # 更新所有技能索引
        if skill_id not in self.skill_index['all']:
            self.skill_index['all'].append(skill_id)
        
        # 更新标签索引
        for tag in skill_def.tags:
            if tag not in self.tag_index:
                self.tag_index[tag] = []
            if skill_id not in self.tag_index[tag]:
                self.tag_index[tag].append(skill_id)
        
        # 更新作者索引
        author = skill_def.author
        if author not in self.author_index:
            self.author_index[author] = []
        if skill_id not in self.author_index[author]:
            self.author_index[author].append(skill_id)
        
        # 更新搜索索引
        await self._update_search_index(skill_def)
    
    async def _update_search_index(self, skill_def: SkillDefinition):
        """
        更新搜索索引
        """
        # 提取可搜索的关键字
        keywords = set()
        
        # 从名称提取
        keywords.update(skill_def.name.lower().split())
        
        # 从描述提取
        desc_words = skill_def.description.lower().split()
        keywords.update(desc_words[:20])  # 限制描述中的词数
        
        # 从标签提取
        keywords.update([tag.lower() for tag in skill_def.tags])
        
        # 从分类提取
        keywords.add(skill_def.category.lower())
        
        # 将入搜索索引
        for keyword in keywords:
            if keyword not in self.search_index:
                self.search_index[keyword] = []
            if skill_def.id not in self.search_index[keyword]:
                self.search_index[keyword].append(skill_def.id)
    
    async def get_skill(self, skill_id: str, version: Optional[str] = None) -> Optional[SkillDefinition]:
        """
        获取技能定义
        """
        if skill_id not in self.skills:
            return None
        
        if version is None:
            # 返回最新版本
            versions = list(self.skills[skill_id].keys())
            if not versions:
                return None
            # 按版本号排序，返回最新的
            latest_version = max(versions, key=lambda v: [int(x) for x in v.split('.')])
            return self.skills[skill_id][latest_version]
        else:
            # 返回指定版本
            if version in self.skills[skill_id]:
                return self.skills[skill_id][version]
            return None
    
    async def update_skill(self, skill_def: SkillDefinition) -> bool:
        """
        更新技能
        """
        # 检查技能是否存在
        existing = await self.get_skill(skill_def.id, skill_def.version)
        if existing is None:
            # 如果版本不存在，可能是新版本
            return await self.register_skill(skill_def)
        
        # 验证技能定义
        if not await self._validate_skill_definition(skill_def):
            return False
        
        # 更新技能定义
        self.skills[skill_def.id][skill_def.version] = skill_def
        
        # 重新更新索引
        await self._update_indexes(skill_def)
        
        self.logger.info(f"Skill updated: {skill_def.id} (v{skill_def.version})")
        return True
    
    async def delete_skill(self, skill_id: str) -> bool:
        """
        删除技能
        """
        if skill_id not in self.skills:
            return False
        
        # 从索引中删除
        await self._remove_from_indexes(skill_id)
        
        # 删除技能
        del self.skills[skill_id]
        
        self.logger.info(f"Skill deleted: {skill_id}")
        return True
    
    async def _remove_from_indexes(self, skill_id: str):
        """
        从所有索引中删除技能
        """
        # 从分类索引删除
        for category_skills in self.skill_index.values():
            if skill_id in category_skills:
                category_skills.remove(skill_id)
        
        # 从标签索引删除
        for tag_skills in self.tag_index.values():
            if skill_id in tag_skills:
                tag_skills.remove(skill_id)
        
        # 从作者索引删除
        for author_skills in self.author_index.values():
            if skill_id in author_skills:
                author_skills.remove(skill_id)
        
        # 从搜索索引删除
        for keyword, skill_ids in list(self.search_index.items()):
            if skill_id in skill_ids:
                skill_ids.remove(skill_id)
                if not skill_ids:  # 如果列表为空，删除关键字
                    del self.search_index[keyword]
    
    async def list_skills(self, 
                         category: Optional[str] = None, 
                         tags: Optional[List[str]] = None,
                         status: Optional[SkillStatus] = None,
                         visibility: Optional[SkillVisibility] = None,
                         search_query: Optional[str] = None) -> List[SkillDefinition]:
        """
        列出技能
        """
        # 获取基础技能列表
        if category:
            if category in self.skill_index:
                skill_ids = self.skill_index[category].copy()
            else:
                skill_ids = []
        else:
            skill_ids = self.skill_index['all'].copy()
        
        # 应用标签过滤
        if tags:
            filtered_ids = set(skill_ids)
            for tag in tags:
                if tag in self.tag_index:
                    filtered_ids &= set(self.tag_index[tag])
                else:
                    filtered_ids = set()  # 如果标签不存在，返回空列表
            skill_ids = list(filtered_ids)
        
        # 应用状态过滤
        if status:
            skill_ids = [
                sid for sid in skill_ids 
                if any(s.status == status for s in self.skills[sid].values())
            ]
        
        # 应用可见性过滤
        if visibility:
            skill_ids = [
                sid for sid in skill_ids 
                if any(s.visibility == visibility for s in self.skills[sid].values())
            ]
        
        # 应用搜索查询过滤
        if search_query:
            search_results = await self.search_skills(search_query)
            search_ids = [s.id for s in search_results]
            skill_ids = [sid for sid in skill_ids if sid in search_ids]
        
        # 获取技能定义
        result = []
        for skill_id in skill_ids:
            skill_def = await self.get_skill(skill_id)  # 获取最新版本
            if skill_def:
                result.append(skill_def)
        
        return result
    
    async def search_skills(self, query: str) -> List[SkillDefinition]:
        """
        搜索技能
        """
        query_lower = query.lower()
        matched_ids = set()
        
        # 在搜索索引中查找
        for keyword, skill_ids in self.search_index.items():
            if query_lower in keyword or keyword in query_lower:
                matched_ids.update(skill_ids)
        
        # 也检查技能ID和名称（如果查询不是关键字的一部分）
        for skill_id, versions in self.skills.items():
            latest_version = max(versions.keys(), key=lambda v: [int(x) for x in v.split('.')])
            skill_def = versions[latest_version]
            
            if (query_lower in skill_id.lower() or 
                query_lower in skill_def.name.lower() or
                query_lower in skill_def.description.lower()):
                matched_ids.add(skill_id)
        
        # 返回匹配的技能定义
        result = []
        for skill_id in matched_ids:
            skill_def = await self.get_skill(skill_id)  # 获取最新版本
            if skill_def:
                result.append(skill_def)
        
        # 按相关性排序（简单实现：名称匹配优先）
        result.sort(key=lambda s: (
            2 if query_lower in s.name.lower() else 
            1 if query_lower in s.description.lower() else 
            0
        ), reverse=True)
        
        return result


class PersistentSkillRegistry(InMemorySkillRegistry):
    """
    持久化技能注册表（基于文件存储）
    """
    def __init__(self, storage_path: str = "./skills_data"):
        super().__init__()
        self.storage_path = storage_path
        # TODO: 实现文件存储逻辑
        self.logger.info(f"Persistent skill registry initialized at {storage_path}")


# 工厂函数
def create_registry(registry_type: str = "in_memory", **kwargs) -> SkillRegistry:
    """
    创建技能注册表实例
    """
    if registry_type == "in_memory":
        return InMemorySkillRegistry()
    elif registry_type == "persistent":
        storage_path = kwargs.get("storage_path", "./skills_data")
        return PersistentSkillRegistry(storage_path)
    else:
        raise ValueError(f"Unknown registry type: {registry_type}")