---
type: study
topic: "文本生成解码与采样策略"
course: "08-NLP全栈"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段6-专业方向深入]]"
upstream: ["[[08-NLP全栈-文本生成]]"]
flow: knowledge
kind: concept
difficulty: intermediate
tags: [NLP, 解码, Sampling, Beam-Search, Top-P, Top-K, Dynamic-Temperature]
---

# 08-NLP全栈-文本生成解码与采样策略

> **一句话总结**：解码算法决定了自回归模型如何根据下一个 Token 的 Logits 概率分布产生最终文本；贪婪搜索和束搜索 (Beam Search) 追求高概率输出，而 Top-K、Top-P (Nucleus Sampling) 与 Temperature 引入受控随机性以提升文本多样性。

---

## 🎯 1. 概念动机与算法分类

自回归模型输出 Softmax 后的 Logits 向量 $z \in \mathbb{R}^{V}$。如何选取下一个 Token？
1. **确定性搜索 (Deterministic Search)**：
   - **Greedy Search**：单步选取最大概率 Token，容易陷入无限死循环与重复。
   - **Beam Search**：维持 $K$ 个全局概率最高的候选 Hypothesis，适合机器翻译和摘要等确定性任务。
2. **随机采样 (Stochastic Sampling)**：
   - **Temperature Scaling**：平滑或陡峭化概率分布。
   - **Top-K Sampling**：保留概率最高的前 $K$ 个 Token 重新归一化采样。
   - **Top-P (Nucleus) Sampling**：保留累积概率达到 $P$ 的动态最小 Token 集合。

---

## 📐 2. 数学公式与概率分布重构

### 2.1 Temperature Scaling
带温度系数 $T > 0$ 的 Logits 概率计算公式：

$$P(x_i) = \frac{\exp(z_i / T)}{\sum_{j=1}^{V} \exp(z_j / T)}$$

- 当 $T \to 0$ 时，分布极度陡峭，等价于 Greedy Search。
- 当 $T \to \infty$ 时，分布趋近于均匀分布，文本充满极大随机性。

### 2.2 Top-P (Nucleus) Sampling 截断
将 Logits 按概率降序排列 $z_{(1)} \ge z_{(2)} \ge \dots \ge z_{(V)}$，找到满足累积概率最小的阈值 $k$：

$$\sum_{i=1}^{k} P(x_{(i)}) \ge P$$

将索引大于 $k$ 的剩余 Token Logits 直接置为 $-\infty$，对前 $k$ 个 Token 进行重新归一化 (Renormalize) 并采样。

---

## 💻 3. PyTorch 解码采样算法手写实现

```python
import torch
import torch.nn.functional as F

def sample_top_k_top_p(logits: torch.FloatTensor, top_k: int = 0, top_p: float = 0.0, temperature: float = 1.0):
    """
    结合 Temperature, Top-K 和 Top-P 的手写解码采样器
    """
    # 1. 应用 Temperature
    logits = logits / max(temperature, 1e-5)
    
    # 2. Top-K 截断
    if top_k > 0:
        top_k = min(top_k, logits.size(-1))
        indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
        logits[indices_to_remove] = -float('Inf')
        
    # 3. Top-P (Nucleus) 截断
    if top_p > 0.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
        
        # 移出累积概率超过 top_p 的 Token
        sorted_indices_to_remove = cumulative_probs > top_p
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0
        
        indices_to_remove = sorted_indices[sorted_indices_to_remove]
        logits[indices_to_remove] = -float('Inf')
        
    # 4. 从截断分布中 Softmax 采样
    probs = F.softmax(logits, dim=-1)
    next_token = torch.multinomial(probs, num_samples=1)
    return next_token

# 运行测试
if __name__ == "__main__":
    logits = torch.tensor([1.0, 2.0, 5.0, 0.5, 4.0, 0.1])
    token = sample_top_k_top_p(logits, top_k=3, top_p=0.9, temperature=0.7)
    print(f"[Sampled Token Index]: {token.item()}")
```

---

## ⚠️ 4. 常见陷阱与避坑指南

1. **Repetition Penalty 惩罚项**：为了防止模型在长文本中重复相同段落，通常在采样前对已生成出现的 Token 进行罚分：$\text{logits}[i] = \text{logits}[i] / \theta$（若 $\text{logits}[i] > 0$）或乘以 $\theta$。
2. **Task-Specific 解码模式选择**：
   - 代码生成/数学推理：首选 $T=0.2$, Top-P=0.95 (接近确定性)。
   - 创意写作/对话系统：首选 $T=0.7 \sim 0.8$, Top-P=0.9。

---

## 🛠️ 5. 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：Beam Search 在寻找全局高概率文本时有什么弊端？为什么开放式对话很少使用 Beam Search？
- [ ] **问题 2**：Top-K Sampling 在概率分布平坦和陡峭两种情况下分别有什么缺点？Top-P 是如何解决的？
- [ ] **问题 3**：如何通过调节 Temperature 参数控制文本生成的创新性与准确性？

---

## 🃏 6. 闭卷提取练习 (Self-Quiz)

1. **代数推导**：给出带有 Repetition Penalty $\theta$ 和 Temperature $T$ 的复合 Logits 变换公式。
2. **代码自测**：使用 PyTorch 实现 Top-P 采样中动态确定截断边界 $k$ 的累积概率矩阵计算。
3. **防错自测**：如果设置 Temperature = 0，程序会出现什么异常？在代码中应如何安全防护？

---

## 🛠️ 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```


---

## 🛠️ 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
