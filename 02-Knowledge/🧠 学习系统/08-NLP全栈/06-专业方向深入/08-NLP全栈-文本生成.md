---
sources: ['Holtzman, A., et al. (2020). The Curious Case of Neural Text Degeneration (Nucleus Sampling). ICLR 2020. arXiv:1904.09751.', 'Jurafsky, D., & Martin, J. H. (2024). Speech and Language Processing (3rd ed. draft). Chapter 10.']
course: "08-NLP全栈"
type: study
flow: knowledge
kind: concept
topic: "文本生成"
created: 2026-08-06
status: completed
assessment_exempt: false
difficulty: intermediate
stage_moc: "[[🧭 阶段6-专业方向深入]]"
upstream: ["[[08-NLP全栈-对话系统]]"]
tags: [学习, NLP, 文本生成, 解码策略, Beam-Search, Top-k, Top-p, 采样]
---

# 08-NLP全栈-文本生成

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 给定语言模型输出的 Token Logits 概率分布，如何挑选并生成最终的文本序列？简单采用贪心搜索 (Greedy Search) 极易陷入重复循环（Degeneration）与死套话；而全局穷举搜索在计算上不可行。文本生成 (Text Generation) 探讨不同的解码策略 (Decoding Strategies) 及其控制效果。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：它是所有自回归大模型（GPT, LLaMA, Mistral）推断控制的最后一道开关。
- **两大类解码策略**：
  1. **确定性搜索 (Deterministic)**：Greedy Search, Beam Search（适合机器翻译、代码生成、摘要）。
  2. **随机采样 (Random Sampling)**：Temperature Scaling, Top-K Sampling, Top-P Nucleus Sampling（适合创意写作、开放对话）。

---

## 3. 正式定义与核心解码算法

### 1. 束搜索 (Beam Search)

维护大小为 $B$ (Beam Width) 的高概率候选项集合。在每一步展开 $B \times |V|$ 个分支，仅保留累计对数概率最高的 $B$ 个序列：

$$\text{Score}(y_1, \dots, y_t) = \frac{1}{t^\alpha} \sum_{i=1}^t \log P(y_i \mid y_{<i})$$

其中 $t^\alpha$ 为长度归一化惩罚因子。

### 2. Nucleus Sampling (Top-P 采样)

动态选择累积概率达到 $p$（如 $p=0.9$）的最少 Token 集合 $V^{(p)} \subset V$：

$$\sum_{w \in V^{(p)}} P(w \mid y_{<t}) \ge p$$

随后仅在该截断集合内重新归一化并进行随机采样，彻底消除极低概率的长尾垃圾词。

---

## 4. Python 代码示例：PyTorch 手写 Top-P 采样截断

```python
import torch
import torch.nn.functional as F

def sample_top_p(logits: torch.Tensor, top_p: float = 0.9, temperature: float = 0.7):
    # 1. 应用 Temperature
    scaled_logits = logits / temperature
    
    # 2. 排序 Logits
    sorted_logits, sorted_indices = torch.sort(scaled_logits, descending=True)
    sorted_probs = F.softmax(sorted_logits, dim=-1)
    
    # 3. 计算累积概率
    cumulative_probs = torch.cumsum(sorted_probs, dim=-1)
    
    # 4. 移除累积概率超过 top_p 的 Token (保留第一个超过的)
    sorted_indices_to_remove = cumulative_probs > top_p
    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
    sorted_indices_to_remove[..., 0] = 0
    
    # 将要移除的位置 Logits 置为 -inf
    indices_to_remove = sorted_indices_to_remove.scatter(1, sorted_indices, sorted_indices_to_remove)
    logits.masked_fill_(indices_to_remove, float('-inf'))
    
    # 5. 采样
    probs = F.softmax(logits, dim=-1)
    return torch.multinomial(probs, num_samples=1)

# 测试采样
dummy_logits = torch.tensor([`[1.0, 5.0, 2.0, 0.1, -2.0]`])
token_id = sample_top_p(dummy_logits, top_p=0.8)
print("Sampled Token Index:", token_id.item())
```

---


## 5. 常见误区与对比矩阵

| 评估维度 / 特性 | 方案 A / 经典范式 | 方案 B / 改进范式 | 权衡与选型建议 (Trade-offs) |
| :--- | :--- | :--- | :--- |
| **计算复杂度** | $\mathcal{O}(N^2)$ 或传统高阶复杂度 | $\mathcal{O}(N \log N)$ 或近似线性复杂度 | 高并发生产环境优先选择低复杂度方案 |
| **显存 / 存储占用** | 占用较高，受限于序列长度/维度 | 优化压缩，支持 Memory-efficient | 边缘设备或资源受限场景推荐优化方案 |
| **表征能力与精度** | 基础表达，易受局部噪声干扰 | 强特征提取，捕捉长距离依赖 | 高精度需求任务（如长文本理解/生成）推荐改进范式 |
| **工程落地门槛** | 开箱即用，工具链极为成熟 | 需特定依赖库 (如 CUDA / Triton) | 开发初期快速原型验证使用经典范式 |


## 5. 原有补全内容与 常见误区与易错点

### 误区：Beam Search 在长文本自由创作中效果最好
- **实证研究**：Beam Search 会严重导致文本重复与死板化（Human Language is not Optimal for Log Likelihood），人类真实文本的概率波动极大。**创意写作应优先选 Top-P (0.9) + Temperature (0.7)**。

---

## 🛠️ 学完后可以完成

### 派生作业与验收入口
```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

### 关联下游知识点
```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/08-NLP全栈"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

---

## 7. 参考文献与延伸阅读

- Holtzman, A., et al. (2020). The Curious Case of Neural Text Degeneration. *ICLR 2020*.
- Jurafsky, D., & Martin, J. H. (2024). *Speech and Language Processing* (3rd ed. draft). Chapter 10.


---

## 🛠️ 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：请不看笔记，口述《文本生成》的核心核心定义与求解动机。
- [ ] **问题 2**：算法或推导的核心计算公式是什么？其中关键变量代表什么物理含义？
- [ ] **问题 3**：在实际工程落地或模型训练中，该方法最常见的 2 个踩坑点或退化场景是什么？


---

## 🃏 闭卷提取练习 (Self-Quiz)

1. **概念自测**：说明《文本生成》的核心机制及其与上下游模块的连接逻辑。
2. **代数/代码自测**：手写关键代数推导步骤或 PyTorch/Python 核心实现伪代码。
3. **防错自测**：如果输入数据出现极小值或极大值离群点，该模块会发生什么异常？如何做数值稳定防护？


---

## 🛠️ 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
