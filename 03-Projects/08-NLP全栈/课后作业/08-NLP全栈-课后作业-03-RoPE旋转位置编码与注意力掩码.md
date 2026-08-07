---
type: project
kind: project
track: 机器学习与AI应用
project_type: homework
course: "08-NLP全栈"
assignment_id: "08-NLP全栈-HW03"
assignment_level: lesson
assignment_format: lab
stage_id: "04"
requires: ["[[08-NLP全栈-RoPE旋转位置编码]]", "[[08-NLP全栈-Self-Attention自注意力机制]]"]
source_type: open_source_project_task
source: "Meta LLaMA Architecture & RoPE Reference Repo"
source_url: "https://github.com/meta-llama/llama"
created: 2026-08-07
status: planned
flow: project
tags: [作业, NLP, RoPE, Transformer, Attention, 位置编码]
assessment_exempt: false
---

# 08-NLP全栈-课后作业-03-RoPE旋转位置编码与注意力掩码

> ⏱ **预计完成耗时**：2.5 小时  
> 🎯 **对应阶段**：阶段 4 - Transformer 与预训练模型

---

## 🎯 学习目标

1. 理解现代大模型（LLaMA 2/3, Qwen 2, Mistral）普遍采用的旋转位置编码（Rotary Position Embedding, RoPE）数学理论。
2. 掌握二维复数平面旋转在高维张量分割与成对变换中的 PyTorch 实现方式。
3. 动手实现支持绝对位置感知的相对位置衰减性质，并融合 Causal (Autoregressive) Mask 完成 Self-Attention 分数计算。

---

## 🚧 任务边界

- **包含**：使用 PyTorch 手写 `RotaryEmbedding` 模块、`apply_rotary_pos_emb` 算子、频次向量 $\theta_i = 10000^{-2(i-1)/d}$ 预计算，以及带 Causal Mask 的 Attention 算子。
- **不包含**：FlashAttention CUDA Kernel 手写、长上下文外推（NTK-aware Scaled RoPE / YaRN）实现。

---

## 📋 详细题目与实施步骤

### 任务 1：RoPE 频次矩阵与 Sin/Cos 缓存构建
定义旋转频率：
$$\theta_i = 10000^{-2(i-1)/d}, \quad i \in \left[1, 2, \dots, \frac{d}{2}\right]$$
根据序列最大长度 $S$，预计算位置矩阵 $m \in [0, S-1]$ 与 $\theta_i$ 的外积：
$$\mathbf{R}_{m, i} = m \cdot \theta_i$$
生成形态为 $[S, d/2]$ 的 `cos` 与 `sin` 缓存张量，并扩维匹配 Multi-Head Attention 张量形状 $[B, N, S, d]$。

### 任务 2：旋转变换算子实现 (`apply_rotary_pos_emb`)
对 Query ($Q$) 与 Key ($K$) 张量按特征维度拆分为偶数项与奇数项 $[x_1, x_2, x_3, x_4, \dots]$：
$$\mathbf{R}_{\Theta, m}^d \mathbf{x}_m = \begin{pmatrix} x_1 \cos m\theta_1 - x_2 \sin m\theta_1 \\ x_1 \sin m\theta_1 + x_2 \cos m\theta_1 \\ \vdots \end{pmatrix}$$
利用 PyTorch 张量广播与旋转交替技巧（如 `rotate_half(x)`）无缝应用 RoPE。

### 任务 3：结合 Causal Mask 验证相对位置保真度
证明并验证内积关系：
$$\langle \mathbf{R}_m \mathbf{q}, \mathbf{R}_n \mathbf{k} \rangle = \mathbf{q}^\top \mathbf{R}_{n-m} \mathbf{k}$$
仅与相对距离 $(n-m)$ 有关。加入下三角 Causal Mask 后计算注意力权重矩阵 $\mathbf{A} = \text{softmax}\left(\frac{Q K^\top}{\sqrt{d_k}} + M\right)$。

---

## 📦 提交产物

1. `scripts/rope_attention.py`：包含 `RotaryEmbedding` 类与带 RoPE 的 `CausalSelfAttention` 模块。
2. `reports/hw03_rope_report.md`：相对位置内积衰减曲线图表与数理解释。

---

## ⚖️ 验收标准 (Rubric)

| 评分项 | 权重 | 通过标准 |
| :--- | :--- | :--- |
| **RoPE 旋转算子** | 40% | 正确实现 `rotate_half` 与 Sin/Cos 广播相乘，与 HuggingFace `LlamaAttention` 对齐 |
| **相对位置不变性**| 30% | 实验验证平移变换下 $Q, K$ 内积仅依赖相对偏移 $(n-m)$ |
| **单元测试** | 30% | 运行 `pytest 03-Projects/08-NLP全栈/tests/test_rope.py` 100% 通过 |

---

## 🔍 引导与自检

- [ ] 是否正确处理了特征维度 $d$ 为奇数或非偶数时的断言提示？
- [ ] 旋转计算时 `sin` 和 `cos` 是否设置了 `requires_grad=False` 避免无谓梯度计算？
- [ ] 在 `rotate_half` 逻辑中，偶数项与奇数项的拼接顺序与符号取反（$-x_2, x_1$）是否正确？

---

## 🧪 验证与测试

```bash
pytest 03-Projects/08-NLP全栈/tests/test_rope.py
```
