# 认知系统 (Cognitive System) 部署指南

## 📋 部署要求

### 系统要求
- **操作系统**: Linux (Ubuntu 20.04+/CentOS 8+), macOS 10.15+, Windows 10/11 WSL2
- **CPU**: 4 核心以上 (推荐 8 核心)
- **内存**: 16GB 以上 (推荐 32GB)
- **存储**: 50GB 以上可用空间
- **网络**: 稳定的互联网连接 (用于模型下载和API调用)

### 软件要求
- **Python**: 3.8 - 3.11
- **Docker**: 20.10+ (推荐)
- **Node.js**: 16+ (用于前端)
- **Git**: 2.0+

## 🚀 部署方式

### 方式一：Docker 部署（推荐）

#### 1. 克隆项目
```bash
git clone https://github.com/your-repo/Personal-AI-OS.git
cd Personal-AI-OS
```

#### 2. 构建 Docker 镜像
```bash
# 构建认知系统镜像
docker build -f dockerfiles/cognition-system.Dockerfile -t personal-ai/cognition:latest .

# 或者使用预构建镜像
docker pull personal-ai/cognition:latest
```

#### 3. 启动服务
```bash
# 使用 Docker Compose 启动完整服务栈
docker-compose -f docker-compose.cognition.yml up -d

# 或者单独启动认知系统
docker run -d \
  --name cognitive-system \
  -p 8080:8080 \
  -v ./data:/app/data \
  -v ./logs:/app/logs \
  -e OPENAI_API_KEY=your_openai_key \
  -e COGNITIVE_CONFIG_PATH=/app/config/cognition.yaml \
  personal-ai/cognition:latest
```

### 方式二：本地部署

#### 1. 环境准备
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements-cognition.txt
```

#### 2. 配置环境变量
```bash
# 创建 .env 文件
cat > .env << EOF
# API 配置
OPENAI_API_KEY=your_openai_api_key
CLAUDE_API_KEY=your_claude_api_key

# 数据库配置
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=cognition_db
POSTGRES_USER=cognition_user
POSTGRES_PASSWORD=secure_password

# 向量数据库配置
CHROMA_HOST=localhost
CHROMA_PORT=8000

# 缓存配置
REDIS_HOST=localhost
REDIS_PORT=6379

# 系统配置
COGNITIVE_WORKERS=4
COGNITIVE_MAX_CONCURRENT_TASKS=10
COGNITIVE_MEMORY_LIMIT=2048
EOF
```

#### 3. 初始化数据库
```bash
# 初始化向量数据库
python -m src.cognition.init_vector_db

# 初始化关系数据库
python -m src.cognition.init_relational_db
```

#### 4. 启动服务
```bash
# 启动认知系统服务
python -m src.cognition.main --config ./config/cognition.yaml

# 或者使用 Gunicorn (生产环境)
gunicorn src.cognition.main:app --workers 4 --bind 0.0.0.0:8080
```

## ⚙️ 配置管理

### 主要配置文件

#### 1. 系统配置 (cognition.yaml)
```yaml
# 认知系统主配置
system:
  name: "Personal AI Cognitive System"
  version: "1.0.0"
  debug: false
  log_level: "INFO"
  
# 模型配置
model:
  embedding_dim: 768
  hidden_dim: 512
  num_layers: 4
  dropout: 0.1
  learning_rate: 0.001
  
# 推理配置
reasoning:
  max_steps: 10
  confidence_threshold: 0.7
  timeout_seconds: 30
  enable_chain_of_thought: true
  enable_tree_of_thoughts: false
  enable_react: true
  max_branches: 3
  reasoning_temperature: 0.7
  
# 个性化配置
personalization:
  learning_rate: 0.01
  forgetting_factor: 0.95
  adaptation_window: 10
  profile_update_frequency: 10
  enable_adaptive_reasoning: true
  enable_bias_correction: true
  enable_cognitive_adaptation: true
  
# 评估配置
evaluation:
  metrics:
    - "reasoning_quality"
    - "confidence_calibration"
    - "reasoning_efficiency"
    - "bias_detection"
    - "metacognitive_awareness"
  weight_distribution:
    reasoning_quality: 0.25
    confidence_calibration: 0.2
    reasoning_efficiency: 0.2
    bias_detection: 0.2
    metacognitive_awareness: 0.15
  evaluation_frequency: 5
  enable_longitudinal_tracking: true
  enable_cross_domain_analysis: true
  
# 偏见检测配置
bias_detection:
  enabled: true
  sensitivity: 0.6
  correction_enabled: true
  detection_methods:
    - "pattern_matching"
    - "statistical_analysis"
    - "contextual_analysis"
  correction_strategies:
    - "counter_argumentation"
    - "alternative_perspective"
    - "confidence_adjustment"
    
# 性能配置
performance:
  max_concurrent_tasks: 10
  cache_enabled: true
  cache_ttl_seconds: 3600
  cache_size_limit: 1000
  enable_profiling: false
  memory_limit_mb: 1024
  cpu_limit_percent: 80.0
  
# 安全配置
security:
  enable_input_validation: true
  enable_output_sanitization: true
  max_input_length: 10000
  max_output_length: 5000
  enable_sandbox_execution: true
  sandbox_timeout_seconds: 30
  max_memory_per_task_mb: 128
```

#### 2. 环境配置 (.env)
```bash
# API 密钥
OPENAI_API_KEY=sk-...
CLAUDE_API_KEY=sk-ant-...

# 数据库连接
DATABASE_URL=postgresql://user:password@localhost:5432/cognition_db
VECTOR_DB_URL=http://localhost:8000

# 缓存配置
REDIS_URL=redis://localhost:6379/0

# 系统配置
WORKERS=4
MAX_CONCURRENT_TASKS=10
MEMORY_LIMIT=2048

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=cognition.log