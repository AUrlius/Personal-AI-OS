# 认知系统 API 文档

## 📖 概述

认知系统提供基于 nuwa-skill 架构的心智模型蒸馏功能，支持推理、记忆、偏见检测和个性化认知服务。

### 基础信息
- **基础URL**: `http://localhost:8080/api/v1`
- **认证**: Bearer Token
- **内容类型**: `application/json`

### 认知任务类型
- `analysis` - 分析任务
- `reasoning` - 推理任务  
- `planning` - 规划任务
- `evaluation` - 评估任务
- `synthesis` - 综合任务
- `decision` - 决策任务
- `memory_operation` - 记忆操作

## 🔐 认证

所有 API 端点都需要认证头：

```
Authorization: Bearer <your-api-token>
```

## 🧠 认知服务 API

### POST /cognition/process
处理认知任务

#### 请求
```json
{
  "task_id": "string",
  "content": "需要处理的认知任务内容",
  "task_type": "analysis|reasoning|planning|evaluation|synthesis|decision|memory_operation",
  "priority": "low|normal|high|critical",
  "complexity": "simple|moderate|complex|very_complex",
  "context": {
    "user_profile": "user_id",
    "previous_interactions": [],
    "domain_context": "specific_domain"
  },
  "metadata": {
    "timeout": 60,
    "max_steps": 10,
    "enable_bias_detection": true
  }
}
```

#### 响应
```json
{
  "success": true,
  "result": {
    "task_id": "string",
    "output": {
      "conclusion": "string",
      "details": "string",
      "steps": ["string"],
      "confidence": 0.8
    },
    "reasoning_process": {
      "id": "string",
      "input_problem": "string",
      "steps": [
        {
          "step_number": 1,
          "content": "string",
          "reasoning_type": "string",
          "confidence": 0.8,
          "supporting_evidence": ["string"],
          "alternatives_considered": ["string"],
          "timestamp": "2026-04-12T20:00:00Z"
        }
      ],
      "conclusion": "string",
      "confidence": 0.8,
      "reasoning_strategy": "chain_of_thought|tree_of_thoughts|react|plan_and_execute",
      "bias_indicators": [],
      "timestamp": "2026-04-12T20:00:00Z",
      "metadata": {}
    },
    "detected_biases": [
      {
        "type": "confirmation|anchoring|availability|hindsight|overconfidence",
        "severity": 0.6,
        "evidence": ["string"],
        "suggestion": "string",
        "confidence": 0.7
      }
    ],
    "cognitive_patterns": [
      {
        "pattern_type": "string",
        "description": "string",
        "applicability": 0.8
      }
    ],
    "execution_time": 1.23,
    "resources_used": {
      "memory_mb": 128,
      "processing_time_seconds": 1.23
    }
  },
  "timestamp": "2026-04-12T20:00:00Z"
}
```

#### 错误响应
```json
{
  "error": {
    "code": "PROCESSING_ERROR",
    "message": "错误信息",
    "details": "详细错误信息"
  }
}
```

### GET /cognition/profile/{user_id}
获取用户认知画像

#### 路径参数
- `user_id` (string, required): 用户ID

#### 响应
```json
{
  "success": true,
  "profile": {
    "user_id": "string",
    "reasoning_style": "analytical|intuitive|balanced|creative",
    "decision_making": "rational|emotional|balanced|cautious|risky",
    "learning_preference": "visual|auditory|kinesthetic|reading|balanced",
    "attention_span": 25,
    "processing_speed": "slow|normal|fast",
    "memory_strength": "working|long_term|episodic|strong|weak",
    "bias_tendencies": {
      "confirmation": 0.3,
      "anchoring": 0.2,
      "availability": 0.1
    },
    "performance_history": [
      {
        "task_type": "string",
        "performance_score": 0.8,
        "timestamp": "2026-04-12T20:00:00Z"
      }
    ],
    "last_updated": "2026-04-12T20:00:00Z"
  }
}
```

### POST /cognition/personalize/{user_id}
更新用户认知画像

#### 路径参数
- `user_id` (string, required): 用户ID

#### 请求
```json
{
  "feedback": {
    "task_performance": {
      "task_id": "string",
      "accuracy": 0.9,
      "confidence": 0.8,
      "processing_time": 2.5
    },
    "bias_feedback": {
      "confirmation": 0.4,
      "anchoring": 0.1
    },
    "preference_updates": {
      "learning_style": "visual",
      "reasoning_preference": "analytical"
    }
  }
}
```

#### 响应
```json
{
  "success": true,
  "updated_profile": {
    "user_id": "string",
    "reasoning_style": "analytical",
    "updated_fields": ["bias_tendencies", "preferences"],
    "last_updated": "2026-04-12T20:00:00Z"
  }
}
```

## 🧠 记忆服务 API

### POST /memory/store
存储记忆

#### 请求
```json
{
  "content": "需要存储的内容",
  "metadata": {
    "user_id": "string",
    "category": "string",
    "tags": ["string"],
    "priority": 1,
    "expires_at": "2026-04-12T20:00:00Z"
  }
}
```

#### 响应
```json
{
  "success": true,
  "memory_id": "string",
  "timestamp": "2026-04-12T20:00:00Z"
}
```

### POST /memory/search
搜索记忆

#### 请求
```json
{
  "query": "搜索查询",
  "filters": {
    "user_id": "string",
    "category": "string",
    "tags": ["string"],
    "date_range": {
      "start": "2026-01-01T00:00:00Z",
      "end": "2026-12-31T23:59:59Z"
    }
  },
  "top_k": 10,
  "threshold": 0.7
}
```

#### 响应
```json
{
  "success": true,
  "results": [
    {
      "memory_id": "string",
      "content": "string",
      "metadata": {},
      "similarity_score": 0.9,
      "timestamp": "2026-04-12T20:00:00Z"
    }
  ],
  "total_found": 5
}
```

### DELETE /memory/{memory_id}
删除记忆

#### 路径参数
- `memory_id` (string, required): 记忆ID

#### 响应
```json
{
  "success": true,
  "deleted_id": "string"
}
```

## 🤖 技能服务 API

### POST /skills/register
注册技能

#### 请求
```json
{
  "skill_id": "string",
  "name": "技能名称",
  "description": "技能描述",
  "version": "1.0.0",
  "author": "string",
  "category": "string",
  "tags": ["string"],
  "inputs": [
    {
      "name": "input_name",
      "type": "string|number|boolean|object|array|file",
      "description": "输入描述",
      "required": true,
      "default": "default_value"
    }
  ],
  "outputs": [
    {
      "name": "output_name",
      "type": "string|number|boolean|object|array|file",
      "description": "输出描述",
      "required": true
    }
  ],
  "code": "技能执行代码",
  "language": "python|javascript|shell|plugin",
  "execution_type": "function|script|api_call|plugin",
  "visibility": "private|public|shared",
  "status": "draft|published|disabled|deprecated",
  "permissions": ["network", "filesystem", "database"],
  "timeout": 30,
  "max_memory": 128,
  "dependencies": ["dependency_id"]
}
```

#### 响应
```json
{
  "success": true,
  "skill_id": "string",
  "registered_version": "1.0.0",
  "validation_result": {
    "valid": true,
    "warnings": [],
    "errors": []
  }
}
```

### POST /skills/execute
执行技能

#### 请求
```json
{
  "skill_id": "string",
  "parameters": {
    "param1": "value1",
    "param2": "value2"
  },
  "user_id": "string",
  "context": {
    "session_id": "string",
    "task_context": "string"
  }
}
```

#### 响应
```json
{
  "success": true,
  "output": {
    "result": "execution_result"
  },
  "execution_time": 0.5,
  "resources_used": {
    "memory_mb": 64,
    "cpu_time_seconds": 0.5
  },
  "detected_biases": [
    {
      "type": "string",
      "severity": 0.6,
      "evidence": ["string"],
      "suggestion": "string",
      "confidence": 0.7
    }
  ]
}
```

### GET /skills/search
搜索技能

#### 查询参数
- `query` (string): 搜索查询
- `category` (string): 分类过滤
- `tags` (string): 标签过滤
- `author` (string): 作者过滤
- `status` (string): 状态过滤
- `visibility` (string): 可见性过滤

#### 响应
```json
{
  "success": true,
  "skills": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "version": "string",
      "author": "string",
      "category": "string",
      "tags": ["string"],
      "rating": 4.5,
      "downloads": 1234,
      "visibility": "public",
      "status": "published",
      "created_at": "2026-04-12T20:00:00Z",
      "updated_at": "2026-04-12T20:00:00Z"
    }
  ],
  "total_count": 10
}
```

## 📊 分析服务 API

### POST /analysis/evaluate-reasoning
评估推理质量

#### 请求
```json
{
  "reasoning_process": {
    "input_problem": "string",
    "steps": [
      {
        "step_number": 1,
        "content": "string",
        "reasoning_type": "string",
        "confidence": 0.8,
        "supporting_evidence": ["string"],
        "alternatives_considered": ["string"],
        "timestamp": "2026-04-12T20:00:00Z"
      }
    ],
    "conclusion": "string",
    "confidence": 0.8,
    "reasoning_strategy": "string",
    "metadata": {}
  }
}
```

#### 响应
```json
{
  "success": true,
  "evaluation": {
    "coherence": 0.85,
    "completeness": 0.78,
    "logical_flow": 0.82,
    "evidence_support": 0.80,
    "creativity": 0.75,
    "critical_thinking": 0.85,
    "overall_quality": 0.81,
    "suggestions": ["string"],
    "detected_issues": [
      {
        "type": "logical_inconsistency",
        "severity": "high",
        "description": "string",
        "suggestion": "string"
      }
    ]
  }
}
```

### POST /analysis/detect-bias
检测认知偏见

#### 请求
```json
{
  "content": "需要分析的内容",
  "context": {
    "user_id": "string",
    "task_type": "string",
    "reasoning_process": {}
  }
}
```

#### 响应
```json
{
  "success": true,
  "detected_biases": [
    {
      "type": "confirmation",
      "severity": 0.6,
      "evidence": ["string"],
      "suggestion": "Consider alternative viewpoints and seek disconfirming evidence",
      "confidence": 0.7,
      "timestamp": "2026-04-12T20:00:00Z"
    }
  ],
  "bias_summary": {
    "total_detected": 1,
    "average_severity": 0.6,
    "types_found": ["confirmation"]
  }
}
```

### GET /analysis/insights/{user_id}
获取认知洞察

#### 路径参数
- `user_id` (string, required): 用户ID

#### 查询参数
- `time_range` (string): 时间范围 (day|week|month|quarter|year)
- `include_details` (boolean): 是否包含详细信息

#### 响应
```json
{
  "success": true,
  "insights": {
    "user_id": "string",
    "period": "string",
    "cognitive_profile_summary": {
      "reasoning_style": "analytical",
      "attention_span_minutes": 25,
      "processing_speed": "normal",
      "memory_strength": "working"
    },
    "performance_metrics": {
      "total_tasks_processed": 123,
      "average_confidence": 0.78,
      "success_rate": 0.85,
      "average_execution_time": 1.23
    },
    "trend_analysis": {
      "confidence_trend": "improving",
      "success_trend": "stable",
      "complexity_handling": "improving"
    },
    "strengths_identified": ["analytical_thinking", "systematic_approach"],
    "improvement_areas": ["creative_thinking", "bias_awareness"],
    "bias_patterns": {
      "confirmation": 0.3,
      "anchoring": 0.2
    },
    "recommendations": [
      "Practice considering alternative viewpoints",
      "Engage in more creative problem-solving exercises"
    ],
    "generated_at": "2026-04-12T20:00:00Z"
  }
}
```

## 📈 系统状态 API

### GET /system/status
获取系统状态

#### 响应
```json
{
  "success": true,
  "status": {
    "system": "healthy",
    "timestamp": "2026-04-12T20:00:00Z",
    "uptime": 3600,
    "version": "1.0.0",
    "services": {
      "cognition_engine": "running",
      "memory_system": "running", 
      "skill_registry": "running",
      "bias_detector": "running",
      "personalization": "running"
    },
    "performance": {
      "active_sessions": 5,
      "concurrent_tasks": 3,
      "queue_size": 0,
      "avg_response_time": 1.23,
      "success_rate": 0.98
    },
    "resources": {
      "memory_usage_mb": 1024,
      "cpu_usage_percent": 45.6,
      "disk_usage_percent": 67.8
    }
  }
}
```

### GET /system/metrics
获取系统指标

#### 查询参数
- `time_range` (string): 时间范围 (hour|day|week|month)
- `metrics` (string): 指标类型 (performance|usage|errors|latency)

#### 响应
```json
{
  "success": true,
  "metrics": {
    "time_range": "day",
    "period_start": "2026-04-12T00:00:00Z",
    "period_end": "2026-04-12T23:59:59Z",
    "performance": {
      "requests_total": 1234,
      "requests_per_minute": 0.86,
      "avg_response_time_ms": 1234,
      "p95_response_time_ms": 2500,
      "success_rate": 0.98,
      "error_rate": 0.02
    },
    "usage": {
      "active_users": 45,
      "tasks_processed": 678,
      "memory_operations": 123,
      "skill_executions": 456
    },
    "errors": {
      "total_errors": 24,
      "error_types": {
        "validation_error": 12,
        "execution_error": 8,
        "timeout_error": 4
      }
    }
  }
}
```

## 🔧 配置管理 API

### GET /config/system
获取系统配置

#### 响应
```json
{
  "success": true,
  "config": {
    "model": {
      "embedding_dim": 768,
      "hidden_dim": 512,
      "num_layers": 4
    },
    "reasoning": {
      "max_steps": 10,
      "confidence_threshold": 0.7,
      "timeout_seconds": 30
    },
    "personalization": {
      "learning_rate": 0.01,
      "forgetting_factor": 0.95,
      "adaptation_window": 10
    },
    "evaluation": {
      "metrics": ["reasoning_quality", "confidence_calibration"],
      "weight_distribution": {
        "reasoning_quality": 0.25
      }
    }
  }
}
```

### PUT /config/system
更新系统配置

#### 请求
```json
{
  "updates": {
    "reasoning": {
      "max_steps": 15,
      "timeout_seconds": 60
    },
    "performance": {
      "max_concurrent_tasks": 20
    }
  }
}
```

#### 响应
```json
{
  "success": true,
  "updated_config": {
    "reasoning": {
      "max_steps": 15,
      "timeout_seconds": 60
    },
    "performance": {
      "max_concurrent_tasks": 20
    }
  },
  "restart_required": false
}
```

## 🚨 错误码

| 错误码 | 描述 | 解决方案 |
|--------|------|----------|
| `AUTHENTICATION_FAILED` | 认证失败 | 检查API密钥 |
| `INVALID_INPUT` | 输入无效 | 检查请求格式 |
| `PROCESSING_ERROR` | 处理错误 | 检查内容和上下文 |
| `RESOURCE_LIMIT_EXCEEDED` | 资源超限 | 降低请求复杂度 |
| `TIMEOUT_ERROR` | 超时错误 | 增加超时时间或简化任务 |
| `BIAS_DETECTED` | 检测到偏见 | 考虑偏见纠正建议 |
| `CONFIG_VALIDATION_ERROR` | 配置验证错误 | 检查配置参数 |

## 📝 示例代码

### Python 客户端示例
```python
import requests
import json

class CognitiveClient:
    def __init__(self, base_url, api_token):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
    
    def process_cognitive_task(self, content, task_type='analysis'):
        url = f'{self.base_url}/cognition/process'
        payload = {
            'content': content,
            'task_type': task_type,
            'priority': 'normal',
            'complexity': 'moderate'
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()
    
    def search_memory(self, query, user_id):
        url = f'{self.base_url}/memory/search'
        payload = {
            'query': query,
            'filters': {'user_id': user_id},
            'top_k': 5
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

# 使用示例
client = CognitiveClient('http://localhost:8080/api/v1', 'your-api-token')

# 处理认知任务
result = client.process_cognitive_task(
    '分析人工智能对教育行业的影响',
    'analysis'
)
print(result)

# 搜索记忆
memory_result = client.search_memory('我的学习计划', 'user123')
print(memory_result)
```

### JavaScript 客户端示例
```javascript
class CognitiveAPI {
  constructor(baseUrl, apiKey) {
    this.baseUrl = baseUrl;
    this.headers = {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    };
  }
  
  async processTask(content, taskType = 'analysis') {
    const response = await fetch(`${this.baseUrl}/cognition/process`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({
        content,
        task_type: taskType,
        priority: 'normal',
        complexity: 'moderate'
      })
    });
    
    return await response.json();
  }
  
  async searchMemory(query, userId) {
    const response = await fetch(`${this.baseUrl}/memory/search`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({
        query,
        filters: { user_id: userId },
        top_k: 5
      })
    });
    
    return await response.json();
  }
}

// 使用示例
const cognitiveAPI = new CognitiveAPI('http://localhost:8080/api/v1', 'your-api-key');

// 处理任务
cognitiveAPI.processTask('分析气候变化的解决方案').then(result => {
  console.log(result);
});

// 搜索记忆
cognitiveAPI.searchMemory('我的研究笔记', 'user123').then(result => {
  console.log(result);
});
```

## 🚀 性能优化建议

### 请求优化
1. **批量处理**: 对于多个相似任务，使用批量接口
2. **缓存策略**: 对于重复查询，实现客户端缓存
3. **异步处理**: 对于长时间任务，使用异步接口

### 错误处理
1. **重试机制**: 实现指数退避重试
2. **降级策略**: 在服务不可用时提供降级方案
3. **监控告警**: 实现请求成功率和延迟监控

## 🔐 安全注意事项

1. **API密钥保护**: 不要在客户端代码中暴露API密钥
2. **输入验证**: 始终验证用户输入
3. **权限控制**: 根据用户权限限制访问
4. **数据加密**: 敏感数据传输和存储加密
5. **速率限制**: 实现请求速率限制防止滥用

---
*文档版本: 1.0*  
*最后更新: 2026-04-12*  
*基于 nuwa-skill 架构设计*