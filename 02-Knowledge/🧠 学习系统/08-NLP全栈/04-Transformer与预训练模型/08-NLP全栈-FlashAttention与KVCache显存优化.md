---
type: study
topic: "FlashAttention与KVCache显存优化"
course: "08-NLP全栈"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段4-Transformer与预训练模型]]"
upstream: ["[[08-NLP全栈-Transformer架构]]", "[[08-NLP全栈-Self-Attention自注意力机制]]"]
flow: knowledge
kind: concept
difficulty: advanced
tags: [NLP, Transformer, FlashAttention, KVCache, 显存优化, CUDA, GPU]
---

# 08-NLP全栈-FlashAttention与KVCache显存优化

> **一句话总结**：KV Cache 通过缓存已生成的 Key/Value 向量消除自回归生成的重复计算；FlashAttention 通过 GPU SRAM 分块 (Tiling) 与在线 Softmax (Online Softmax) 重算技术，将注意力机制的 HBM 读写 IO 复杂度从 $\mathcal{O}(N^2)$ 降低至 $\mathcal{O}(N)$。

---

## 🎯 1. 概念动机与 GPU 存储瓶颈

标准 Self-Attention 的 Softmax 矩阵 $S = Q K^T \in \mathbb{R}^{N \times N}$ 必须完整写入 GPU 高带宽显存 (HBM)。长上下文下（如 $N=32K$）：
1. **显存爆满**：$N \times N$ 的注意力中间矩阵产生巨大的 HBM 读写开销。
2. **计算受限于 IO (Memory-Bound)**：GPU CUDA Core 的算力未饱满，绝大部分时间消耗在 HBM 与 SRAM（高速静态缓存）之间传输矩阵 $S, P$ 的数据。

KV Cache 与 FlashAttention 分别从**生成步冗余消除**和**硬件 IO 效率**两个维度解决这一问题。

---

## 📐 2. 数学推导与算法细节

### 2.1 KV Cache 显存占用推导
在自回归 Token 生成 $t$ 步时，先前 $t-1$ 个 Token 的 $K_{1:t-1}, V_{1:t-1}$ 已计算完成。无 Cache 时每生成一个新 Token 都要重算 $1 \dots t$ 的所有 $Q, K, V$。
开辟 KV Cache 保持历史 $K, V$ 后，每步只需计算当前 Token 的 $q_t, k_t, v_t$，并将 $k_t, v_t$ 拼接入 Cache。

对于批大小 $B$、上下文长度 $L$、层数 $L_{layers}$、隐层维度 $d_{model}$、Head 数 $h$：

$$\text{KV Cache 显存 (Bytes)} = 2 \times 2 \times B \times L \times L_{layers} \times h \times d_{head} = 4 \cdot B \cdot L \cdot L_{layers} \cdot d_{model}$$

（使用 FP16/BF16，系数 2 表示 Key 与 Value 两个 Tensor，每个元素 2 字节）。

### 2.2 FlashAttention 在线 Softmax 与 Tiling 推导
设 SRAM 容量为 $M$。将 $Q, K, V$ 划分为大小为 $B_r \times d$ 和 $B_c \times d$ 的 Block。
由于 Softmax $\text{softmax}(x)_i = \frac{e^{x_i - m}}{\sum e^{x_j - m}}$ 依赖全局最大值 $m$，FlashAttention 使用 **Online Softmax** 递推公式：

设已知前局部向量 $x^{(1)}$ 的最大值 $m^{(1)}$ 和分母 $l^{(1)} = \sum e^{x_i^{(1)} - m^{(1)}}$。传入新局部向量 $x^{(2)}$，求总体最大值 $m^{\text{new}} = \max(m^{(1)}, m^{(2)})$：

$$l^{\text{new}} = e^{m^{(1)} - m^{\text{new}}} l^{(1)} + e^{m^{(2)} - m^{\text{new}}} l^{(2)}$$

$$O^{\text{new}} = \text{diag}\left(e^{m^{(1)} - m^{\text{new}}}\right) O^{(1)} + e^{m^{(2)} - m^{\text{new}}} P^{(2)} V^{(2)}$$

通过在 SRAM 中流式更新 $m, l, O$，完全**不将大小为 $N \times N$ 的 $S, P$ 矩阵写回 HBM**，IO 复杂度大幅下降。

---

## 💻 3. PyTorch & FlashAttention 实现

```python
import torch
import torch.nn as nn

def naive_kv_cache_step(q_t, k_t, v_t, past_kv):
    """
    q_t: [B, 1, H, D]
    k_t: [B, 1, H, D]
    v_t: [B, 1, H, D]
    past_kv: (past_k, past_v)
    """
    if past_kv is not None:
        past_k, past_v = past_kv
        k_all = torch.cat([past_k, k_t], dim=1)
        v_all = torch.cat([past_v, v_t], dim=1)
    else:
        k_all, v_all = k_t, v_t
        
    new_kv = (k_all, v_all)
    
    # Compute single-step attention
    scores = torch.matmul(q_t, k_all.transpose(-1, -2)) / (q_t.size(-1) ** 0.5)
    attn = torch.softmax(scores, dim=-1)
    out = torch.matmul(attn, v_all)
    return out, new_kv

def demo_flash_attention_call(q, k, v):
    # PyTorch 2.0+ 内置 scaled_dot_product_attention 自动触发 FlashAttention
    with torch.backends.cuda.sdp_kernel(enable_flash=True, enable_math=False, enable_mem_efficient=False):
        out = torch.nn.functional.scaled_dot_product_attention(q, k, v, is_causal=True)
    return out
```

---

## ⚠️ 4. 常见陷阱与避坑指南

1. **PagedAttention 碎片化**：原生 KV Cache 必须申请连续物理显存，会导致严重显存碎片。vLLM 采用类似操作系统虚拟内存的 PagedAttention 解决此问题。
2. **FlashAttention 硬件要求**：FlashAttention-1 需要 NVIDIA Ampere (A100/3090) 及以上架构，FlashAttention-2 在 Hopper (H100) 进一步优化了 Warp 级并行。

---

## 🛠️ 5. 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：为什么标准 Softmax 无法直接按 Block 分块计算？FlashAttention 如何通过在线 Softmax 解决此问题？
- [ ] **问题 2**：已知一个 70B 模型（80 层，$d_{model}=8192$），Batch Size=8，序列长度=4096，使用 FP16，计算其 KV Cache 占据多少 GB 显存？
- [ ] **问题 3**：GQA (Grouped Query Attention) 如何在不显著损失精度的前提下减少 KV Cache 开销？

---

## 🃏 6. 闭卷提取练习 (Self-Quiz)

1. **代数推导**：给出 Online Softmax 更新局域注意力输出 $O^{\text{new}}$ 的推导步骤与缩放因子。
2. **代码自测**：写出带 KV Cache 的 Transformer Decoder 单层 Forward 伪代码。
3. **防错自测**：在训练阶段是否需要启用 KV Cache？为什么？

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
