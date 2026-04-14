# graphify 仓库分析报告

## 仓库概述
- **名称**: graphify
- **功能**: 知识图谱构建
- **定位**: 知识图谱构建和可视化工具

## 核心架构

### 1. 知识图谱构建架构
```
┌─────────────────┐    ┌─────────────────┐
│   数据源        │ -> │  实体识别       │
└─────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌─────────────────┐
│  关系抽取       │ -> │  图谱构建       │
└─────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌─────────────────┐
│  图谱存储       │ <- │  可视化展示     │
└─────────────────┘    └─────────────────┘
```

### 2. 技术栈
- **后端**: Python (spaCy, NLTK, Transformers)
- **图数据库**: Neo4j / NetworkX / GraphDB
- **NLP**: spaCy, Hugging Face Transformers
- **可视化**: D3.js, Cytoscape.js
- **前端**: React, Vue.js

## 核心算法

### 1. 实体识别算法 (NER)
```python
import spacy
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

class EntityExtractor:
    def __init__(self):
        # 加载预训练的NER模型
        self.nlp = spacy.load("zh_core_web_sm")  # 或 en_core_web_sm
        self.custom_ner = pipeline(
            "ner", 
            model="dbmdz/bert-large-cased-finetuned-conll03-english",
            aggregation_strategy="simple"
        )
    
    def extract_entities(self, text):
        """
        从文本中提取实体
        """
        # 使用spaCy进行基础NER
        spacy_entities = self.extract_with_spacy(text)
        
        # 使用Transformer模型进行高级NER
        transformer_entities = self.extract_with_transformer(text)
        
        # 合并和去重实体
        merged_entities = self.merge_entities(spacy_entities, transformer_entities)
        
        return merged_entities
    
    def extract_with_spacy(self, text):
        """
        使用spaCy提取实体
        """
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char,
                'confidence': getattr(ent, 'confidence', 0.9)
            })
        
        return entities
    
    def extract_with_transformer(self, text):
        """
        使用Transformer模型提取实体
        """
        results = self.custom_ner(text)
        entities = []
        
        for result in results:
            entities.append({
                'text': result['word'],
                'label': result['entity_group'],
                'start': result['start'],
                'end': result['end'],
                'confidence': result['score']
            })
        
        return entities
    
    def merge_entities(self, spacy_ents, transformer_ents):
        """
        合并来自不同模型的实体
        """
        # 使用IOU (Intersection over Union) 来合并重叠实体
        merged = []
        all_ents = spacy_ents + transformer_ents
        
        # 按位置排序
        all_ents.sort(key=lambda x: x['start'])
        
        for ent in all_ents:
            # 检查是否与已存在的实体重叠
            overlap_found = False
            for existing in merged:
                if self.check_overlap(ent, existing):
                    # 合并重叠实体，保留置信度较高的
                    if ent['confidence'] > existing['confidence']:
                        existing.update(ent)
                    overlap_found = True
                    break
            
            if not overlap_found:
                merged.append(ent)
        
        return merged
    
    def check_overlap(self, ent1, ent2):
        """
        检查两个实体是否重叠
        """
        return not (ent1['end'] <= ent2['start'] or ent2['end'] <= ent1['start'])

def extract_domain_specific_entities(text, domain_model):
    """
    提取特定领域的实体
    """
    # 使用领域特定的NER模型
    domain_entities = []
    
    # 加载领域词典
    domain_keywords = domain_model.get_keywords()
    
    for keyword in domain_keywords:
        # 在文本中查找关键词
        import re
        matches = re.finditer(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE)
        
        for match in matches:
            domain_entities.append({
                'text': match.group(),
                'label': domain_model.get_label(keyword),
                'start': match.start(),
                'end': match.end(),
                'confidence': 0.95
            })
    
    return domain_entities
```

### 2. 关系抽取算法
```python
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RelationExtractor:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.model = AutoModel.from_pretrained('bert-base-uncased')
        self.relation_classifier = self.build_relation_classifier()
    
    def build_relation_classifier(self):
        """
        构建关系分类器
        """
        class RelationClassifier(nn.Module):
            def __init__(self, hidden_size=768, num_relations=10):
                super().__init__()
                self.dropout = nn.Dropout(0.1)
                self.classifier = nn.Linear(hidden_size * 3, num_relations)  # e1_repr + e2_repr + concat
                self.activation = nn.Tanh()
            
            def forward(self, e1_repr, e2_repr, context_repr):
                # 拼接实体表示和上下文表示
                combined = torch.cat([e1_repr, e2_repr, context_repr], dim=-1)
                combined = self.dropout(combined)
                logits = self.classifier(combined)
                return torch.softmax(logits, dim=-1)
        
        return RelationClassifier()
    
    def extract_relations(self, text, entities):
        """
        从文本中提取实体间的关系
        """
        relations = []
        
        # 遍历所有实体对
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                entity1 = entities[i]
                entity2 = entities[j]
                
                # 获取实体间的关系
                relation = self.classify_relation(text, entity1, entity2)
                
                if relation['confidence'] > 0.5:  # 阈值
                    relations.append(relation)
        
        return relations
    
    def classify_relation(self, text, entity1, entity2):
        """
        分类两个实体间的关系
        """
        # 确保实体1在文本中出现在实体2之前
        if entity1['start'] > entity2['start']:
            entity1, entity2 = entity2, entity1
        
        # 提取实体周围的上下文
        context_start = max(0, entity1['start'] - 50)
        context_end = min(len(text), entity2['end'] + 50)
        context = text[context_start:context_end]
        
        # 获取实体表示
        e1_repr = self.get_entity_representation(text, entity1)
        e2_repr = self.get_entity_representation(text, entity2)
        context_repr = self.get_context_representation(context)
        
        # 分类关系
        with torch.no_grad():
            relation_probs = self.relation_classifier(e1_repr, e2_repr, context_repr)
            predicted_relation = torch.argmax(relation_probs, dim=-1)
            confidence = relation_probs[0][predicted_relation].item()
        
        return {
            'entity1': entity1['text'],
            'entity2': entity2['text'],
            'relation': self.get_relation_label(predicted_relation.item()),
            'confidence': confidence,
            'sentence': context
        }
    
    def get_entity_representation(self, text, entity):
        """
        获取实体的向量表示
        """
        entity_text = entity['text']
        inputs = self.tokenizer(entity_text, return_tensors="pt", truncation=True, padding=True)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            # 使用[CLS]标记的表示
            entity_repr = outputs.last_hidden_state[:, 0, :]
        
        return entity_repr
    
    def get_context_representation(self, context):
        """
        获取上下文的向量表示
        """
        inputs = self.tokenizer(context, return_tensors="pt", truncation=True, padding=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            # 使用[CLS]标记的表示
            context_repr = outputs.last_hidden_state[:, 0, :]
        
        return context_repr
    
    def get_relation_label(self, relation_id):
        """
        根据ID获取关系标签
        """
        relation_labels = [
            'no_relation', 'per:employee_of', 'per:cities_of_residence', 
            'per:origin', 'org:city_of_headquarters', 'per:title', 
            'org:country_of_headquarters', 'org:stateorprovince_of_headquarters',
            'per:countries_of_residence', 'per:age'
        ]
        
        if relation_id < len(relation_labels):
            return relation_labels[relation_id]
        else:
            return 'unknown_relation'

def extract_temporal_relations(text, entities):
    """
    提取时间关系
    """
    temporal_relations = []
    
    # 时间表达式识别
    import re
    time_patterns = [
        r'\b\d{4}-\d{2}-\d{2}\b',  # YYYY-MM-DD
        r'\b\d{4}/\d{2}/\d{2}\b',  # YYYY/MM/DD
        r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # MM/DD/YYYY
        r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
    ]
    
    for pattern in time_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            time_expr = {
                'text': match.group(),
                'start': match.start(),
                'end': match.end(),
                'type': 'TIME'
            }
            
            # 查找时间附近的实体
            for entity in entities:
                if abs(entity['start'] - time_expr['end']) < 50:  # 在50字符内
                    temporal_relations.append({
                        'entity': entity['text'],
                        'time': time_expr['text'],
                        'relation': 'time_of_event',
                        'confidence': 0.8
                    })
    
    return temporal_relations
```

### 3. 图谱构建算法
```python
import networkx as nx
from collections import defaultdict
import json

class KnowledgeGraphBuilder:
    def __init__(self):
        self.graph = nx.MultiDiGraph()  # 支持多重边和有向图
        self.entity_types = set()
        self.relation_types = set()
    
    def build_graph(self, entities, relations):
        """
        构建知识图谱
        """
        # 添加实体节点
        for entity in entities:
            self.add_entity_node(entity)
        
        # 添加关系边
        for relation in relations:
            self.add_relation_edge(relation)
        
        return self.graph
    
    def add_entity_node(self, entity):
        """
        添加实体节点
        """
        entity_id = self.normalize_entity_id(entity['text'])
        
        self.graph.add_node(
            entity_id,
            name=entity['text'],
            type=entity['label'],
            start_pos=entity['start'],
            end_pos=entity['end'],
            confidence=entity.get('confidence', 1.0)
        )
        
        self.entity_types.add(entity['label'])
    
    def add_relation_edge(self, relation):
        """
        添加关系边
        """
        source_id = self.normalize_entity_id(relation['entity1'])
        target_id = self.normalize_entity_id(relation['entity2'])
        
        self.graph.add_edge(
            source_id,
            target_id,
            relation_type=relation['relation'],
            confidence=relation['confidence'],
            sentence=relation['sentence'],
            directed=True
        )
        
        self.relation_types.add(relation['relation'])
    
    def normalize_entity_id(self, entity_text):
        """
        标准化实体ID
        """
        import re
        # 移除特殊字符，转换为小写
        normalized = re.sub(r'[^\w\s]', '_', entity_text.lower().strip())
        # 替换空格为下划线
        normalized = '_'.join(normalized.split())
        return normalized
    
    def extract_subgraph(self, seed_entities, depth=2):
        """
        提取以种子实体为中心的子图
        """
        # 找到种子实体对应的节点
        seed_nodes = []
        for entity in seed_entities:
            entity_id = self.normalize_entity_id(entity)
            if self.graph.has_node(entity_id):
                seed_nodes.append(entity_id)
        
        # 提取子图
        subgraph_nodes = set(seed_nodes)
        
        for _ in range(depth):
            new_nodes = set()
            for node in subgraph_nodes:
                # 获取邻居节点
                neighbors = set(self.graph.neighbors(node))
                new_nodes.update(neighbors)
            
            subgraph_nodes.update(new_nodes)
        
        return self.graph.subgraph(subgraph_nodes)
    
    def find_paths(self, source, target, max_length=3):
        """
        查找两个实体间的路径
        """
        source_id = self.normalize_entity_id(source)
        target_id = self.normalize_entity_id(target)
        
        if not self.graph.has_node(source_id) or not self.graph.has_node(target_id):
            return []
        
        # 使用NetworkX查找路径
        try:
            paths = list(nx.all_simple_paths(
                self.graph, 
                source=source_id, 
                target=target_id, 
                cutoff=max_length
            ))
            return paths
        except nx.NetworkXNoPath:
            return []

def enrich_graph_with_external_knowledge(graph, external_kb):
    """
    使用外部知识库丰富图谱
    """
    enriched_graph = graph.copy()
    
    # 遍历图中的每个实体
    for node in graph.nodes():
        node_attrs = graph.nodes[node]
        entity_name = node_attrs.get('name', node)
        
        # 查询外部知识库
        kb_info = external_kb.query(entity_name)
        
        if kb_info:
            # 添加额外的属性
            for attr, value in kb_info.items():
                if attr not in node_attrs:
                    enriched_graph.nodes[node][attr] = value
            
            # 添加额外的关系
            for related_entity, relation in kb_info.get('relations', []):
                related_id = normalize_entity_id(related_entity)
                enriched_graph.add_edge(
                    node, 
                    related_id, 
                    relation_type=relation,
                    source='external_kb',
                    confidence=0.9
                )
    
    return enriched_graph
```

### 4. 图谱嵌入算法 (Graph Embedding)
```python
import numpy as np
from sklearn.decomposition import PCA
from node2vec import Node2Vec
import random

class GraphEmbedder:
    def __init__(self, graph):
        self.graph = graph
        self.embeddings = None
    
    def generate_node2vec_embeddings(self, dimensions=128, walk_length=80, num_walks=10, workers=4):
        """
        使用Node2Vec生成节点嵌入
        """
        # 创建Node2Vec模型
        node2vec = Node2Vec(
            self.graph,
            dimensions=dimensions,
            walk_length=walk_length,
            num_walks=num_walks,
            workers=workers,
            p=1,  # Return hyperparameter
            q=1   # Inout hyperparameter
        )
        
        # 训练模型
        model = node2vec.fit(window=10, min_count=1, batch_words=4)
        
        # 获取嵌入
        embeddings = {}
        for node in self.graph.nodes():
            embeddings[node] = model.wv[node]
        
        self.embeddings = embeddings
        return embeddings
    
    def compute_graph_features(self):
        """
        计算图的拓扑特征
        """
        features = {}
        
        # 节点中心性
        features['degree_centrality'] = nx.degree_centrality(self.graph)
        features['betweenness_centrality'] = nx.betweenness_centrality(self.graph)
        features['closeness_centrality'] = nx.closeness_centrality(self.graph)
        features['pagerank'] = nx.pagerank(self.graph)
        
        # 聚类系数
        features['clustering_coefficient'] = nx.clustering(self.graph)
        
        # 连通分量
        features['connected_components'] = list(nx.connected_components(self.graph.to_undirected()))
        
        return features
    
    def find_communities(self):
        """
        发现图中的社区结构
        """
        # 使用Louvain算法
        try:
            import community as community_louvain
            partition = community_louvain.best_partition(self.graph.to_undirected())
            return partition
        except ImportError:
            # 如果没有community库，使用简单的方法
            return self.simple_community_detection()
    
    def simple_community_detection(self):
        """
        简单的社区检测方法
        """
        # 使用贪婪优化算法
        communities = {}
        for node in self.graph.nodes():
            communities[node] = hash(node) % 10  # 简单哈希分配
        return communities

def compute_similarity_scores(graph, embeddings, entity1, entity2):
    """
    计算两个实体的相似度分数
    """
    entity1_id = normalize_entity_id(entity1)
    entity2_id = normalize_entity_id(entity2)
    
    if entity1_id not in embeddings or entity2_id not in embeddings:
        return 0.0
    
    # 余弦相似度
    emb1 = embeddings[entity1_id]
    emb2 = embeddings[entity2_id]
    
    dot_product = np.dot(emb1, emb2)
    norm1 = np.linalg.norm(emb1)
    norm2 = np.linalg.norm(emb2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    cosine_sim = dot_product / (norm1 * norm2)
    
    # 结合图结构相似性
    structural_sim = compute_structural_similarity(graph, entity1_id, entity2_id)
    
    # 综合相似度
    combined_sim = 0.7 * cosine_sim + 0.3 * structural_sim
    
    return combined_sim

def compute_structural_similarity(graph, node1, node2):
    """
    计算基于图结构的相似性
    """
    if not graph.has_node(node1) or not graph.has_node(node2):
        return 0.0
    
    # 共同邻居相似性
    neighbors1 = set(graph.neighbors(node1))
    neighbors2 = set(graph.neighbors(node2))
    
    if len(neighbors1) == 0 and len(neighbors2) == 0:
        return 1.0 if node1 == node2 else 0.0
    
    common_neighbors = neighbors1.intersection(neighbors2)
    union_neighbors = neighbors1.union(neighbors2)
    
    jaccard_coeff = len(common_neighbors) / len(union_neighbors) if union_neighbors else 0
    
    # Adamic-Adar指数
    aa_index = 0
    for neighbor in common_neighbors:
        degree = graph.degree(neighbor)
        if degree > 1:
            aa_index += 1 / np.log(degree)
    
    return (jaccard_coeff + aa_index) / 2
```

## 关键特性

### 1. 实体识别
- **多模型融合**: 结合多种NER模型提高准确性
- **领域适应**: 支持特定领域的实体识别
- **置信度评估**: 为每个实体提供置信度分数

### 2. 关系抽取
- **上下文感知**: 考虑实体间的上下文关系
- **多关系类型**: 支持多种关系类型的抽取
- **时间关系**: 识别实体间的时间关系

### 3. 图谱构建
- **动态构建**: 支持增量式图谱构建
- **子图提取**: 提取感兴趣的子图结构
- **路径发现**: 发现实体间的连接路径

### 4. 图谱分析
- **拓扑分析**: 分析图的拓扑特征
- **社区发现**: 识别图中的社区结构
- **嵌入学习**: 学习节点的向量表示

## 架构优势

### 1. 可扩展性
- **模块化设计**: 各组件可独立扩展
- **分布式处理**: 支持大规模图谱处理
- **增量更新**: 支持图谱的增量更新

### 2. 准确性
- **多模型融合**: 提高实体和关系识别准确性
- **置信度评估**: 提供可靠性评估
- **质量控制**: 包含质量控制机制

### 3. 可解释性
- **路径追踪**: 可追踪实体间的连接路径
- **特征可视化**: 提供图的拓扑特征
- **决策依据**: 清晰的关系抽取依据

## 技术挑战

### 1. 规模挑战
- **大数据处理**: 处理大规模文本数据
- **图谱存储**: 高效存储大规模知识图谱
- **查询优化**: 优化图谱查询性能

### 2. 质量挑战
- **噪声处理**: 处理文本中的噪声数据
- **歧义消解**: 解决实体和关系的歧义
- **错误传播**: 防止错误在图谱中传播

### 3. 实时性挑战
- **实时更新**: 支持图谱的实时更新
- **快速查询**: 提供快速的图谱查询
- **流式处理**: 支持流式数据处理

## 对 Personal-AI-OS 的启示

### 1. 知识图谱模块
- 实现实体识别和关系抽取
- 构建个人知识图谱
- 提供图谱可视化功能

### 2. 算法应用
- 使用NLP技术提取知识
- 实现图嵌入算法
- 设计社区发现机制

### 3. 用户体验
- 提供直观的图谱可视化
- 实现智能知识推荐
- 设计交互式探索功能