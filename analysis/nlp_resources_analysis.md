# NLP 学习资源分析报告

## 仓库概述
- **名称**: NLP-notes (整合多个NLP学习仓库)
- **功能**: NLP 学习和实践资源合集
- **包含仓库**:
  - course: HuggingFace 官方课程
  - d2l-zh: 动手学深度学习中文版
  - jalammar.github.io: Jay Alammar 可视化教程
  - nlp_notes: 中文 NLP 笔记
  - notebooks: HuggingFace 官方示例
  - NLP-progress: NLP 进展追踪

## 核心架构

### 1. NLP 学习路径架构
```
┌─────────────────┐    ┌─────────────────┐
│   基础理论      │ -> │  实践项目       │
└─────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌─────────────────┐
│  模型理解       │ -> │  应用开发       │
└─────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌─────────────────┐
│  最新技术       │ <- │  工程实践       │
└─────────────────┘    └─────────────────┘
```

### 2. 技术栈
- **深度学习框架**: PyTorch, TensorFlow
- **NLP库**: Transformers, Tokenizers, Datasets
- **可视化**: Matplotlib, Seaborn, Plotly
- **开发环境**: Jupyter Notebooks, Colab
- **模型托管**: HuggingFace Hub

## 核心算法和概念

### 1. Transformer 架构分析
```python
import torch
import torch.nn as nn
import math

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super(MultiHeadAttention, self).__init__()
        assert d_model % num_heads == 0
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # 线性变换
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        
        self.dropout = nn.Dropout(0.1)
    
    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        """
        缩放点积注意力机制
        """
        # 计算注意力分数
        matmul_qk = torch.matmul(Q, K.transpose(-2, -1))
        
        # 缩放
        dk = K.size()[-1]
        scaled_attention_logits = matmul_qk / math.sqrt(dk)
        
        # 应用掩码
        if mask is not None:
            scaled_attention_logits += (mask * -1e9)
        
        # Softmax获得注意力权重
        attention_weights = torch.softmax(scaled_attention_logits, dim=-1)
        attention_weights = self.dropout(attention_weights)
        
        # 与V相乘
        output = torch.matmul(attention_weights, V)
        
        return output, attention_weights
    
    def split_heads(self, x, batch_size):
        """
        将头分离
        """
        x = x.view(batch_size, -1, self.num_heads, self.d_k)
        return x.transpose(1, 2)
    
    def forward(self, Q, K, V, mask=None):
        batch_size = Q.size(0)
        
        # 线性变换
        Q = self.W_q(Q)
        K = self.W_k(K)
        V = self.W_v(V)
        
        # 分离头
        Q = self.split_heads(Q, batch_size)
        K = self.split_heads(K, batch_size)
        V = self.split_heads(V, batch_size)
        
        # 缩放点积注意力
        scaled_attention, attention_weights = self.scaled_dot_product_attention(
            Q, K, V, mask)
        
        # 合并头
        scaled_attention = scaled_attention.transpose(1, 2).contiguous()
        scaled_attention = scaled_attention.view(
            batch_size, -1, self.d_model)
        
        # 最终线性变换
        output = self.W_o(scaled_attention)
        
        return output, attention_weights

class PositionWiseFeedForward(nn.Module):
    def __init__(self, d_model, d_ff):
        super(PositionWiseFeedForward, self).__init__()
        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.1)
    
    def forward(self, x):
        x = self.relu(self.linear1(x))
        x = self.dropout(x)
        x = self.linear2(x)
        return x

class EncoderLayer(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super(EncoderLayer, self).__init__()
        
        self.multi_head_attention = MultiHeadAttention(d_model, num_heads)
        self.ffn = PositionWiseFeedForward(d_model, d_ff)
        
        self.layernorm1 = nn.LayerNorm(d_model)
        self.layernorm2 = nn.LayerNorm(d_model)
        
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # 多头注意力
        attn_output, _ = self.multi_head_attention(x, x, x, mask)
        attn_output = self.dropout1(attn_output)
        out1 = self.layernorm1(x + attn_output)
        
        # 前馈网络
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output)
        out2 = self.layernorm2(out1 + ffn_output)
        
        return out2

class DecoderLayer(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super(DecoderLayer, self).__init__()
        
        self.masked_multi_head_attention = MultiHeadAttention(d_model, num_heads)
        self.multi_head_attention = MultiHeadAttention(d_model, num_heads)
        self.ffn = PositionWiseFeedForward(d_model, d_ff)
        
        self.layernorm1 = nn.LayerNorm(d_model)
        self.layernorm2 = nn.LayerNorm(d_model)
        self.layernorm3 = nn.LayerNorm(d_model)
        
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)
        self.dropout3 = nn.Dropout(dropout)
    
    def forward(self, x, enc_output, look_ahead_mask=None, padding_mask=None):
        # 遮蔽多头注意力
        attn1, attn_weights_block1 = self.masked_multi_head_attention(
            x, x, x, look_ahead_mask)
        attn1 = self.dropout1(attn1)
        out1 = self.layernorm1(attn1 + x)
        
        # 多头注意力 (enc_output as K and V)
        attn2, attn_weights_block2 = self.multi_head_attention(
            out1, enc_output, enc_output, padding_mask)
        attn2 = self.dropout2(attn2)
        out2 = self.layernorm2(attn2 + out1)
        
        # 前馈网络
        ffn_output = self.ffn(out2)
        ffn_output = self.dropout3(ffn_output)
        out3 = self.layernorm3(ffn_output + out2)
        
        return out3, attn_weights_block1, attn_weights_block2

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super(PositionalEncoding, self).__init__()
        
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        
        div_term = torch.exp(torch.arange(0, d_model, 2).float() *
                            -(math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)
    
    def forward(self, x):
        return x + self.pe[:, :x.size(1)]

class Transformer(nn.Module):
    def __init__(self, src_vocab_size, tgt_vocab_size, d_model=512, 
                 num_heads=8, num_layers=6, d_ff=2048, max_seq_len=100, dropout=0.1):
        super(Transformer, self).__init__()
        
        self.encoder_embedding = nn.Embedding(src_vocab_size, d_model)
        self.decoder_embedding = nn.Embedding(tgt_vocab_size, d_model)
        
        self.positional_encoding = PositionalEncoding(d_model, max_seq_len)
        
        self.encoder_layers = nn.ModuleList([
            EncoderLayer(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        
        self.decoder_layers = nn.ModuleList([
            DecoderLayer(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        
        self.fc_out = nn.Linear(d_model, tgt_vocab_size)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, src, tgt, src_mask=None, tgt_mask=None, src_padding_mask=None, tgt_padding_mask=None):
        # 编码器
        src_emb = self.dropout(self.positional_encoding(self.encoder_embedding(src)))
        
        enc_output = src_emb
        for layer in self.encoder_layers:
            enc_output = layer(enc_output, src_mask)
        
        # 解码器
        tgt_emb = self.dropout(self.positional_encoding(self.decoder_embedding(tgt)))
        
        dec_output = tgt_emb
        for layer in self.decoder_layers:
            dec_output, _, _ = layer(dec_output, enc_output, tgt_mask, tgt_padding_mask)
        
        # 输出层
        output = self.fc_out(dec_output)
        
        return output
```

### 2. BERT 模型实现
```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class BertEmbeddings(nn.Module):
    def __init__(self, vocab_size, hidden_size, max_position_embeddings, 
                 type_vocab_size, hidden_dropout_prob=0.1):
        super(BertEmbeddings, self).__init__()
        
        self.word_embeddings = nn.Embedding(vocab_size, hidden_size, padding_idx=0)
        self.position_embeddings = nn.Embedding(max_position_embeddings, hidden_size)
        self.token_type_embeddings = nn.Embedding(type_vocab_size, hidden_size)
        
        self.LayerNorm = nn.LayerNorm(hidden_size, eps=1e-12)
        self.dropout = nn.Dropout(hidden_dropout_prob)
        
    def forward(self, input_ids, token_type_ids=None):
        seq_length = input_ids.size(1)
        position_ids = torch.arange(seq_length, dtype=torch.long, device=input_ids.device)
        position_ids = position_ids.unsqueeze(0).expand_as(input_ids)
        
        if token_type_ids is None:
            token_type_ids = torch.zeros_like(input_ids)
        
        words_embeds = self.word_embeddings(input_ids)
        position_embeds = self.position_embeddings(position_ids)
        token_type_embeds = self.token_type_embeddings(token_type_ids)
        
        embeddings = words_embeds + position_embeds + token_type_embeds
        embeddings = self.LayerNorm(embeddings)
        embeddings = self.dropout(embeddings)
        
        return embeddings

class BertSelfAttention(nn.Module):
    def __init__(self, hidden_size, num_attention_heads, attention_probs_dropout_prob=0.1):
        super(BertSelfAttention, self).__init__()
        if hidden_size % num_attention_heads != 0:
            raise ValueError(
                f"hidden_size {hidden_size} is not a multiple of num_attention_heads {num_attention_heads}"
            )
        
        self.num_attention_heads = num_attention_heads
        self.attention_head_size = int(hidden_size / num_attention_heads)
        self.all_head_size = self.num_attention_heads * self.attention_head_size
        
        self.query = nn.Linear(hidden_size, self.all_head_size)
        self.key = nn.Linear(hidden_size, self.all_head_size)
        self.value = nn.Linear(hidden_size, self.all_head_size)
        
        self.dropout = nn.Dropout(attention_probs_dropout_prob)
    
    def transpose_for_scores(self, x):
        new_x_shape = x.size()[:-1] + (self.num_attention_heads, self.attention_head_size)
        x = x.view(*new_x_shape)
        return x.permute(0, 2, 1, 3)
    
    def forward(self, hidden_states, attention_mask=None):
        mixed_query_layer = self.query(hidden_states)
        mixed_key_layer = self.key(hidden_states)
        mixed_value_layer = self.value(hidden_states)
        
        query_layer = self.transpose_for_scores(mixed_query_layer)
        key_layer = self.transpose_for_scores(mixed_key_layer)
        value_layer = self.transpose_for_scores(mixed_value_layer)
        
        # 计算注意力分数
        attention_scores = torch.matmul(query_layer, key_layer.transpose(-1, -2))
        attention_scores = attention_scores / math.sqrt(self.attention_head_size)
        
        if attention_mask is not None:
            attention_scores = attention_scores + attention_mask
        
        attention_probs = nn.Softmax(dim=-1)(attention_scores)
        attention_probs = self.dropout(attention_probs)
        
        context_layer = torch.matmul(attention_probs, value_layer)
        context_layer = context_layer.permute(0, 2, 1, 3).contiguous()
        new_context_layer_shape = context_layer.size()[:-2] + (self.all_head_size,)
        context_layer = context_layer.view(*new_context_layer_shape)
        
        return context_layer

class BertLayer(nn.Module):
    def __init__(self, hidden_size, intermediate_size, num_attention_heads, 
                 hidden_dropout_prob=0.1, attention_probs_dropout_prob=0.1):
        super(BertLayer, self).__init__()
        
        self.attention = BertSelfAttention(hidden_size, num_attention_heads, 
                                        attention_probs_dropout_prob)
        self.output = BertOutput(hidden_size, hidden_dropout_prob)
        
        self.intermediate = BertIntermediate(hidden_size, intermediate_size)
        self.output = BertOutput(hidden_size, hidden_dropout_prob)
    
    def forward(self, hidden_states, attention_mask=None):
        attention_output = self.attention(hidden_states, attention_mask)
        attention_output = self.output(attention_output, hidden_states)
        
        intermediate_output = self.intermediate(attention_output)
        layer_output = self.output(intermediate_output, attention_output)
        
        return layer_output

class BertModel(nn.Module):
    def __init__(self, config):
        super(BertModel, self).__init__()
        
        self.embeddings = BertEmbeddings(
            config.vocab_size, 
            config.hidden_size, 
            config.max_position_embeddings,
            config.type_vocab_size
        )
        
        self.encoder = nn.ModuleList([
            BertLayer(
                config.hidden_size,
                config.intermediate_size,
                config.num_attention_heads,
                config.hidden_dropout_prob,
                config.attention_probs_dropout_prob
            ) for _ in range(config.num_hidden_layers)
        ])
        
        self.pooler = nn.Linear(config.hidden_size, config.hidden_size)
        self.pooler_activation = nn.Tanh()
    
    def forward(self, input_ids, attention_mask=None, token_type_ids=None):
        embedding_output = self.embeddings(input_ids, token_type_ids)
        
        extended_attention_mask = attention_mask.unsqueeze(1).unsqueeze(2)
        extended_attention_mask = extended_attention_mask.to(dtype=next(self.parameters()).dtype)
        extended_attention_mask = (1.0 - extended_attention_mask) * -10000.0
        
        encoder_output = embedding_output
        for layer in self.encoder:
            encoder_output = layer(encoder_output, extended_attention_mask)
        
        pooled_output = self.pooler(encoder_output[:, 0])
        pooled_output = self.pooler_activation(pooled_output)
        
        return encoder_output, pooled_output
```

### 3. 词嵌入算法 (Word Embeddings)
```python
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import Counter, defaultdict
import random

class Word2Vec:
    def __init__(self, embedding_dim=100, window_size=5, negative_samples=5):
        self.embedding_dim = embedding_dim
        self.window_size = window_size
        self.negative_samples = negative_samples
        self.word2idx = {}
        self.idx2word = {}
        self.vocab_size = 0
        self.embeddings = None
        
    def build_vocab(self, sentences):
        """
        构建词汇表
        """
        word_counts = Counter()
        for sentence in sentences:
            word_counts.update(sentence)
        
        # 过滤低频词
        words = [word for word, count in word_counts.items() if count >= 2]
        
        self.word2idx = {word: idx for idx, word in enumerate(words)}
        self.idx2word = {idx: word for word, idx in self.word2idx.items()}
        self.vocab_size = len(words)
        
        # 初始化嵌入矩阵
        self.embeddings = {
            'input': np.random.normal(0, 0.1, (self.vocab_size, self.embedding_dim)),
            'output': np.random.normal(0, 0.1, (self.vocab_size, self.embedding_dim))
        }
    
    def get_context_words(self, sentence, pos, window_size):
        """
        获取上下文单词
        """
        start = max(0, pos - window_size)
        end = min(len(sentence), pos + window_size + 1)
        
        context = []
        for i in range(start, end):
            if i != pos:
                if sentence[i] in self.word2idx:
                    context.append(self.word2idx[sentence[i]])
        
        return context
    
    def negative_sampling(self, target_idx, k=5):
        """
        负采样
        """
        neg_samples = []
        for _ in range(k):
            while True:
                neg_idx = random.randint(0, self.vocab_size - 1)
                if neg_idx != target_idx:
                    neg_samples.append(neg_idx)
                    break
        return neg_samples
    
    def train(self, sentences, epochs=10, lr=0.01):
        """
        训练Word2Vec模型
        """
        for epoch in range(epochs):
            total_loss = 0
            
            for sentence in sentences:
                for pos, word in enumerate(sentence):
                    if word not in self.word2idx:
                        continue
                    
                    center_idx = self.word2idx[word]
                    context_words = self.get_context_words(sentence, pos, self.window_size)
                    
                    for context_idx in context_words:
                        # 正样本
                        positive_loss = self.update_positive_sample(center_idx, context_idx, lr)
                        
                        # 负样本
                        negative_indices = self.negative_sampling(context_idx, self.negative_samples)
                        negative_loss = 0
                        for neg_idx in negative_indices:
                            negative_loss += self.update_negative_sample(center_idx, neg_idx, lr)
                        
                        total_loss += positive_loss + negative_loss
            
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss}")
    
    def update_positive_sample(self, center_idx, context_idx, lr):
        """
        更新正样本
        """
        center_vec = self.embeddings['input'][center_idx]
        context_vec = self.embeddings['output'][context_idx]
        
        # 计算得分
        score = np.dot(center_vec, context_vec)
        sigmoid_score = self.sigmoid(score)
        
        # 计算梯度
        grad = (1 - sigmoid_score)
        loss = -np.log(sigmoid_score)
        
        # 更新嵌入向量
        self.embeddings['input'][center_idx] += lr * grad * context_vec
        self.embeddings['output'][context_idx] += lr * grad * center_vec
        
        return loss
    
    def update_negative_sample(self, center_idx, neg_idx, lr):
        """
        更新负样本
        """
        center_vec = self.embeddings['input'][center_idx]
        neg_vec = self.embeddings['output'][neg_idx]
        
        # 计算得分
        score = np.dot(center_vec, neg_vec)
        sigmoid_score = self.sigmoid(score)
        
        # 计算梯度
        grad = sigmoid_score
        loss = -np.log(1 - sigmoid_score)
        
        # 更新嵌入向量
        self.embeddings['input'][center_idx] -= lr * grad * neg_vec
        self.embeddings['output'][neg_idx] -= lr * grad * center_vec
        
        return loss
    
    def sigmoid(self, x):
        """
        Sigmoid激活函数
        """
        return 1 / (1 + np.exp(-np.clip(x, -250, 250)))
    
    def get_embedding(self, word):
        """
        获取单词嵌入
        """
        if word in self.word2idx:
            idx = self.word2idx[word]
            return self.embeddings['input'][idx]
        return None
    
    def find_similar_words(self, word, top_k=5):
        """
        查找相似单词
        """
        if word not in self.word2idx:
            return []
        
        word_vec = self.get_embedding(word)
        similarities = []
        
        for other_word, idx in self.word2idx.items():
            if other_word != word:
                other_vec = self.embeddings['input'][idx]
                similarity = np.dot(word_vec, other_vec) / (
                    np.linalg.norm(word_vec) * np.linalg.norm(other_vec)
                )
                similarities.append((other_word, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

def preprocess_text(text):
    """
    文本预处理
    """
    import re
    import string
    
    # 转换为小写
    text = text.lower()
    
    # 移除标点符号
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # 分词
    words = text.split()
    
    # 移除停用词 (简单示例)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    words = [word for word in words if word not in stop_words]
    
    return words

class GloVe:
    def __init__(self, embedding_dim=100, x_max=100, alpha=0.75):
        self.embedding_dim = embedding_dim
        self.x_max = x_max
        self.alpha = alpha
        self.word2idx = {}
        self.idx2word = {}
        self.vocab_size = 0
        self.word_vectors = None
        self.context_vectors = None
        self.word_biases = None
        self.context_biases = None
        
    def build_cooccurrence_matrix(self, sentences, window_size=5):
        """
        构建共现矩阵
        """
        cooccurrence = defaultdict(lambda: defaultdict(float))
        word_counts = Counter()
        
        # 统计词频和共现
        for sentence in sentences:
            for i, word in enumerate(sentence):
                if word not in self.word2idx:
                    idx = len(self.word2idx)
                    self.word2idx[word] = idx
                    self.idx2word[idx] = word
                
                word_counts[word] += 1
                
                # 统计窗口内的共现
                start = max(0, i - window_size)
                end = min(len(sentence), i + window_size + 1)
                
                for j in range(start, end):
                    if i != j:
                        context_word = sentence[j]
                        cooccurrence[word][context_word] += 1.0 / abs(i - j)
        
        self.vocab_size = len(self.word2idx)
        
        # 转换为矩阵
        matrix = np.zeros((self.vocab_size, self.vocab_size))
        for word1, context_dict in cooccurrence.items():
            idx1 = self.word2idx[word1]
            for word2, count in context_dict.items():
                idx2 = self.word2idx[word2]
                matrix[idx1][idx2] = count
        
        return matrix, dict(word_counts)
    
    def weighting_function(self, x):
        """
        权重函数
        """
        if x < self.x_max:
            return (x / self.x_max) ** self.alpha
        else:
            return 1.0
    
    def train(self, sentences, epochs=100, learning_rate=0.01):
        """
        训练GloVe模型
        """
        cooccurrence_matrix, word_counts = self.build_cooccurrence_matrix(sentences)
        
        # 初始化参数
        self.word_vectors = np.random.normal(0, 0.1, (self.vocab_size, self.embedding_dim))
        self.context_vectors = np.random.normal(0, 0.1, (self.vocab_size, self.embedding_dim))
        self.word_biases = np.zeros(self.vocab_size)
        self.context_biases = np.zeros(self.vocab_size)
        
        for epoch in range(epochs):
            total_loss = 0
            
            for i in range(self.vocab_size):
                for j in range(self.vocab_size):
                    if cooccurrence_matrix[i][j] > 0:
                        X_ij = cooccurrence_matrix[i][j]
                        log_X_ij = np.log(X_ij)
                        
                        # 计算预测值
                        prediction = np.dot(self.word_vectors[i], self.context_vectors[j]) + \
                                   self.word_biases[i] + self.context_biases[j]
                        
                        # 计算权重
                        weight = self.weighting_function(X_ij / self.x_max)
                        
                        # 计算误差
                        error = prediction - log_X_ij
                        
                        # 计算损失
                        loss = weight * (error ** 2)
                        total_loss += loss
                        
                        # 更新参数
                        grad_word = weight * error * self.context_vectors[j]
                        grad_context = weight * error * self.word_vectors[i]
                        
                        self.word_vectors[i] -= learning_rate * grad_word
                        self.context_vectors[j] -= learning_rate * grad_context
                        self.word_biases[i] -= learning_rate * weight * error
                        self.context_biases[j] -= learning_rate * weight * error
            
            print(f"GloVe Epoch {epoch + 1}/{epochs}, Loss: {total_loss}")
```

### 4. 文本预处理和 Tokenization
```python
import re
import unicodedata
from typing import List, Tuple

class TextPreprocessor:
    def __init__(self):
        self.stop_words = self.load_stop_words()
        self.stemmer = PorterStemmer()  # 或其他词干提取器
    
    def clean_text(self, text: str) -> str:
        """
        清理文本
        """
        # 标准化Unicode字符
        text = unicodedata.normalize('NFKD', text)
        
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        
        # 移除URL
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # 移除邮箱
        text = re.sub(r'\S+@\S+', '', text)
        
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def tokenize(self, text: str) -> List[str]:
        """
        分词
        """
        # 基本的分词 (对于英文)
        tokens = re.findall(r'\b\w+\b', text.lower())
        
        # 移除停用词
        tokens = [token for token in tokens if token not in self.stop_words]
        
        # 词干提取
        tokens = [self.stemmer.stem(token) for token in tokens]
        
        return tokens
    
    def preprocess(self, text: str) -> List[str]:
        """
        完整的预处理流程
        """
        cleaned_text = self.clean_text(text)
        tokens = self.tokenize(cleaned_text)
        return tokens

class BytePairEncoder:
    def __init__(self):
        self.vocab = {}
        self.merges = {}
        self.pat = re.compile(r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""")
    
    def get_stats(self, ids):
        """
        获取字符对统计
        """
        counts = {}
        for pair in zip(ids, ids[1:]):
            counts[pair] = counts.get(pair, 0) + 1
        return counts
    
    def merge(self, ids, pair, idx):
        """
        合并字符对
        """
        newids = []
        i = 0
        while i < len(ids):
            if i < len(ids) - 1 and ids[i] == pair[0] and ids[i+1] == pair[1]:
                newids.append(idx)
                i += 2
            else:
                newids.append(ids[i])
                i += 1
        return newids
    
    def train(self, texts, vocab_size, verbose=False):
        """
        训练BPE分词器
        """
        # 将文本转换为初始ID序列
        merged_ids = []
        for text in texts:
            text_ids = [ord(c) for c in text]
            merged_ids.extend(text_ids)
            merged_ids.append(256)  # 分隔符
        
        # 初始化词汇表
        vocab = {idx: bytes([idx]) for idx in range(256)}
        merges = {}
        
        # 执行BPE合并
        num_merges = vocab_size - 256
        for i in range(num_merges):
            # 获取统计信息
            stats = self.get_stats(merged_ids)
            if not stats:
                break
                
            # 找到最频繁的对
            pair = max(stats, key=stats.get)
            idx = 256 + i
            print(f"merge {i+1}/{num_merges}: {pair} -> {idx}" if verbose else "", end='\r')
            
            # 合并
            merged_ids = self.merge(merged_ids, pair, idx)
            
            # 更新词汇表
            vocab[idx] = vocab[pair[0]] + vocab[pair[1]]
            merges[pair] = idx
        
        self.vocab = vocab
        self.merges = merges
    
    def encode(self, text):
        """
        编码文本
        """
        # 初始转换为字节
        raw_bytes = text.encode("utf-8")
        ids = list(raw_bytes)
        
        # 应用合并
        while len(ids) >= 2:
            stats = self.get_stats(ids)
            if not stats:
                break
            # 找到第一个可用的合并
            pair = min(stats.keys(), key=lambda p: self.merges.get(p, float('inf')))
            if pair not in self.merges:
                break  # 没有更多合并
            idx = self.merges[pair]
            ids = self.merge(ids, pair, idx)
        
        return ids
    
    def decode(self, ids):
        """
        解码ID序列
        """
        # 将ID转换回字节
        raw_bytes = b""
        for idx in ids:
            raw_bytes += self.vocab[idx]
        
        # 解码字节为文本
        text = raw_bytes.decode("utf-8", errors="replace")
        return text

class CustomTokenizer:
    def __init__(self, vocab_size=10000):
        self.bpe = BytePairEncoder()
        self.vocab_size = vocab_size
        self.special_tokens = {
            '<|endoftext|>': vocab_size,
            '<|pad|>': vocab_size + 1,
            '<|unk|>': vocab_size + 2
        }
    
    def train(self, texts):
        """
        训练分词器
        """
        self.bpe.train(texts, self.vocab_size - len(self.special_tokens))
    
    def encode(self, text):
        """
        编码文本
        """
        return self.bpe.encode(text)
    
    def decode(self, ids):
        """
        解码ID序列
        """
        return self.bpe.decode(ids)
```

### 5. 序列标注算法 (Sequence Labeling)
```python
import numpy as np
from scipy.special import softmax

class CRF:
    def __init__(self, num_labels):
        self.num_labels = num_labels
        self.transitions = np.random.randn(num_labels, num_labels)  # 转移矩阵
        self.start_transitions = np.random.randn(num_labels)       # 开始转移
        self.end_transitions = np.random.randn(num_labels)         # 结束转移
    
    def forward(self, emissions, mask=None):
        """
        前向算法计算所有路径的总得分
        """
        batch_size, seq_length, num_labels = emissions.shape
        
        if mask is None:
            mask = np.ones((batch_size, seq_length), dtype=bool)
        
        # 初始化前向变量
        alpha = self.start_transitions + emissions[:, 0]  # [batch_size, num_labels]
        
        # 递推计算
        for i in range(1, seq_length):
            # 计算从前一个位置到当前位置的转移
            emit_scores = emissions[:, i].reshape(batch_size, 1, num_labels)
            trans_scores = self.transitions.reshape(1, num_labels, num_labels)
            prev_alpha = alpha.reshape(batch_size, num_labels, 1)
            
            # 当前位置的得分
            curr_alpha = prev_alpha + trans_scores + emit_scores
            
            # 使用log-sum-exp稳定数值计算
            alpha = self.logsumexp(curr_alpha, axis=1)
            
            # 只在未被mask的位置更新
            mask_i = mask[:, i].reshape(batch_size, 1)
            alpha = np.where(mask_i, alpha, alpha)
        
        # 添加结束转移
        alpha += self.end_transitions
        
        # 计算最终得分
        total_score = self.logsumexp(alpha, axis=1)
        
        return total_score
    
    def viterbi_decode(self, emissions, mask=None):
        """
        Viterbi算法解码最优路径
        """
        batch_size, seq_length, num_labels = emissions.shape
        
        if mask is None:
            mask = np.ones((batch_size, seq_length), dtype=bool)
        
        # 初始化
        score = self.start_transitions + emissions[:, 0]
        history = []
        
        # 递推
        for i in range(1, seq_length):
            # 计算转移得分
            prev_score = score.reshape(batch_size, num_labels, 1)
            trans_scores = self.transitions.reshape(1, num_labels, num_labels)
            emit_score = emissions[:, i].reshape(batch_size, 1, num_labels)
            
            # 总得分
            total_score = prev_score + trans_scores + emit_score
            
            # 选择最优前驱
            new_score = np.max(total_score, axis=1)
            new_history = np.argmax(total_score, axis=1)
            
            # 只在未被mask的位置更新
            mask_i = mask[:, i].reshape(batch_size, 1)
            score = np.where(mask_i, new_score, score)
            history.append(new_history)
        
        # 添加结束转移
        score += self.end_transitions
        
        # 回溯最优路径
        sequences = []
        for i in range(batch_size):
            # 最后一个标签
            last_tag = np.argmax(score[i])
            sequence = [last_tag]
            
            # 回溯
            for hist in reversed(history):
                last_tag = hist[i][last_tag]
                sequence.append(last_tag)
            
            sequence.reverse()
            sequences.append(sequence)
        
        return sequences, score[np.arange(batch_size), [seq[-1] for seq in sequences]]
    
    def logsumexp(self, x, axis=-1):
        """
        数值稳定的log-sum-exp
        """
        max_x = np.max(x, axis=axis, keepdims=True)
        return max_x + np.log(np.sum(np.exp(x - max_x), axis=axis))

class NERModel:
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_labels):
        self.embedding = np.random.randn(vocab_size, embedding_dim) * 0.1
        self.lstm_w = np.random.randn(embedding_dim + hidden_dim, 4 * hidden_dim) * 0.1
        self.lstm_u = np.random.randn(hidden_dim, 4 * hidden_dim) * 0.1
        self.lstm_b = np.zeros(4 * hidden_dim)
        self.hidden_dim = hidden_dim
        self.num_labels = num_labels
        self.crf = CRF(num_labels)
        
        # 输出层权重
        self.output_w = np.random.randn(hidden_dim, num_labels) * 0.1
        self.output_b = np.zeros(num_labels)
    
    def lstm_forward(self, embeddings):
        """
        LSTM前向传播
        """
        batch_size, seq_len, embedding_dim = embeddings.shape
        hidden_dim = self.hidden_dim
        
        # 初始化隐藏状态
        h = np.zeros((batch_size, hidden_dim))
        c = np.zeros((batch_size, hidden_dim))
        
        # 存储所有时间步的隐藏状态
        hidden_states = np.zeros((batch_size, seq_len, hidden_dim))
        
        for t in range(seq_len):
            x = embeddings[:, t, :]  # [batch_size, embedding_dim]
            
            # 拼接输入和前一时刻的隐藏状态
            combined_input = np.concatenate([x, h], axis=1)  # [batch_size, embedding_dim + hidden_dim]
            
            # 计算门和候选值
            gates = np.dot(combined_input, self.lstm_w) + self.lstm_b  # [batch_size, 4 * hidden_dim]
            gates = gates.reshape(batch_size, 4, hidden_dim)
            
            i_gate = self.sigmoid(gates[:, 0, :])  # 输入门
            f_gate = self.sigmoid(gates[:, 1, :])  # 遗忘门
            o_gate = self.sigmoid(gates[:, 2, :])  # 输出门
            c_candidate = np.tanh(gates[:, 3, :])  # 候选细胞状态
            
            # 更新细胞状态
            c = f_gate * c + i_gate * c_candidate
            
            # 更新隐藏状态
            h = o_gate * np.tanh(c)
            
            hidden_states[:, t, :] = h
        
        return hidden_states
    
    def forward(self, input_ids):
        """
        前向传播
        """
        # 词嵌入
        embeddings = self.embedding[input_ids]  # [batch_size, seq_len, embedding_dim]
        
        # LSTM
        hidden_states = self.lstm_forward(embeddings)  # [batch_size, seq_len, hidden_dim]
        
        # 输出层
        batch_size, seq_len, hidden_dim = hidden_states.shape
        emissions = np.dot(hidden_states.reshape(-1, hidden_dim), self.output_w) + self.output_b
        emissions = emissions.reshape(batch_size, seq_len, self.num_labels)
        
        return emissions
    
    def predict(self, input_ids):
        """
        预测标签序列
        """
        emissions = self.forward(input_ids)
        predictions, scores = self.crf.viterbi_decode(emissions)
        return predictions
    
    def sigmoid(self, x):
        """
        Sigmoid激活函数
        """
        return 1 / (1 + np.exp(-np.clip(x, -250, 250)))

def prepare_ner_data(texts, labels, tokenizer, label2id):
    """
    准备NER数据
    """
    input_ids = []
    label_ids = []
    
    for text, label_seq in zip(texts, labels):
        tokens = tokenizer.tokenize(text)
        token_ids = [tokenizer.convert_tokens_to_ids(token) for token in tokens]
        
        # 对齐标签
        aligned_labels = []
        for token, label in zip(tokens, label_seq[:len(tokens)]):
            aligned_labels.append(label2id.get(label, label2id['O']))
        
        # 填充到相同长度
        max_len = 128
        if len(token_ids) < max_len:
            token_ids.extend([0] * (max_len - len(token_ids)))
            aligned_labels.extend([0] * (max_len - len(aligned_labels)))
        else:
            token_ids = token_ids[:max_len]
            aligned_labels = aligned_labels[:max_len]
        
        input_ids.append(token_ids)
        label_ids.append(aligned_labels)
    
    return np.array(input_ids), np.array(label_ids)
```

## 关键特性

### 1. 模型架构
- **Transformer**: 注意力机制和并行处理
- **BERT**: 双向上下文理解和预训练
- **GPT**: 单向生成和自回归训练

### 2. 训练方法
- **自监督学习**: 利用无标签数据预训练
- **微调**: 在特定任务上微调预训练模型
- **知识蒸馏**: 小模型学习大模型知识

### 3. 应用场景
- **文本分类**: 情感分析、主题分类
- **序列标注**: NER、词性标注
- **文本生成**: 机器翻译、摘要生成

### 4. 优化技术
- **注意力机制**: 捕捉长距离依赖
- **位置编码**: 保留位置信息
- **残差连接**: 促进梯度流动

## 架构优势

### 1. 表征能力
- **上下文理解**: 深刻理解词语上下文
- **迁移学习**: 预训练模型广泛适用
- **多语言支持**: 支持多种语言处理

### 2. 泛化能力
- **领域适应**: 适用于多个领域
- **任务通用**: 一套模型多任务适用
- **数据高效**: 少量数据即可微调

### 3. 可扩展性
- **模型规模**: 支持不同规模模型
- **分布式训练**: 支持大规模训练
- **推理优化**: 高效推理部署

## 技术挑战

### 1. 计算资源
- **训练成本**: 大模型训练资源需求高
- **推理延迟**: 高质量生成需要时间
- **内存占用**: 模型和数据内存需求大

### 2. 数据质量
- **偏见问题**: 训练数据中的偏见
- **数据稀缺**: 特定领域数据不足
- **标注成本**: 高质量标注成本高

### 3. 可解释性
- **黑盒模型**: 模型决策过程不透明
- **错误分析**: 难以分析错误原因
- **调试困难**: 模型行为难以预测

## 对 Personal-AI-OS 的启示

### 1. NLP 功能实现
- 集成预训练模型
- 实现文本理解和生成
- 提供多语言支持

### 2. 模型应用
- 用于记忆内容理解
- 实现智能对话
- 提供内容分析

### 3. 学习资源
- 提供NLP学习路径
- 实现实践项目
- 持续技术更新