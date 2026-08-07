---
type: study
topic: "LLM量化算法AWQ与GPTQ"
course: "08-NLP全栈"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段5-大语言模型与前沿技术]]"
upstream: ["[[08-NLP全栈-LLM推理优化]]"]
flow: knowledge
kind: concept
difficulty: advanced
tags: [NLP, LLM, 量化, AWQ, GPTQ, INT4, 推理优化]
---

# 08-NLP全栈-LLM量化算法AWQ与GPTQ

> **一句话总结**：GPTQ 利用二阶泰勒展开与逆黑塞矩阵在 Layer 级别逐列重构权重以补偿量化误差；AWQ (Activation-aware Weight Quantization) 观察到仅约 1% 的显著通道 (Salient Channel) 决定量化精度，通过根据激活值幅度自适应保护这 1% 关键权重，实现了更优的 INT4 保持度。

---

## 🎯 1. 概念动机与量化难题

传统均匀量化（如 RTN - Round To Nearest）在 FP16 转 INT4 时会导致 LLM 困惑度 (Perplexity) 爆炸。原因在于：
1. **激活值离群点 (Outliers)**：随着 LLM 参数增大，某些特定通道的激活幅度极大（达到常态值的数十倍）。
2. **权重敏感度非均一**：并非所有权重同等重要，盲目舍入会破坏模型注意力与表达能力。

---

## 📐 2. 数学推导与算法细节

### 2.1 均匀对称/非对称量化公式
将浮点数 $x \in [x_{\min}, x_{\max}]$ 映射至 $b$-bit 整数 $q \in [-2^{b-1}, 2^{b-1}-1]$：

$$\text{Scale } S = \frac{x_{\max} - x_{\min}}{2^b - 1}, \quad \text{Zero-point } Z = \text{round}\left(-\frac{x_{\min}}{S}\right)$$

$$q = \text{clamp}\left(\text{round}\left(\frac{x}{S}\right) + Z, q_{\min}, q_{\max}\right)$$

$$\hat{x} = (q - Z) \times S$$

### 2.2 GPTQ (二阶导数逆黑塞矩阵误差补偿)
对于一层权重 $W \in \mathbb{R}^{d_{\text{out}} \times d_{\text{in}}}$ 和输入 $X$，目标是最小化二次重构误差：

$$\arg\min_{\hat{W}} \|W X - \hat{W} X\|_2^2$$

设 $H = 2 X X^T$ 为黑塞矩阵 (Hessian Matrix)。若对权重第 $q$ 列进行量化：$w_q \to \hat{w}_q$，为了补偿这一偏差 $\delta_q = \hat{w}_q - w_q$，对剩余尚未量化的权重调整量为：

$$\Delta w = -\frac{w_q - \text{quant}(w_q)}{[H^{-1}]_{qq}} \cdot H^{-1}_{:, q}$$

GPTQ 通过 Cholesky 分解加块并行处理 (Block-wise) 稳定加速了这一过程。

### 2.3 AWQ (激活感知保护)
AWQ 发现：**直接保护包含离群激活的 1% 显著通道，能消解绝大部分量化误差**。
AWQ 不使用混合精度（因为混合精度计算硬件效率低），而是引入按通道缩放因子 $s > 1$：

$$W' = W \cdot \text{diag}(s), \quad X' = \text{diag}(s)^{-1} \cdot X$$

选择最佳缩放向量 $s$ 满足：

$$\arg\min_s \|\text{quant}(W \cdot \text{diag}(s)) \cdot \text{diag}(s)^{-1} X - W X\|$$

通过网格搜索每个通道 $s_x = s_X^\gamma$，既对关键通道缩小了量化步长，又无需改变推理算子逻辑。

---

## 💻 3. PyTorch INT4 模拟量化代码

```python
import torch

def quantize_asymmetric_int4(w: torch.FloatTensor, num_bits: int = 4):
    """
    非对称 INT4 模拟量化
    """
    qmin = 0
    qmax = 2**num_bits - 1
    
    w_min = w.min(dim=-1, keepdim=True)[0]
    w_max = w.max(dim=-1, keepdim=True)[0]
    
    scale = (w_max - w_min) / qmax
    zero_point = torch.round(-w_min / scale)
    
    q_w = torch.clamp(torch.round(w / scale) + zero_point, qmin, qmax)
    w_dequant = (q_w - zero_point) * scale
    return w_dequant, scale, zero_point

# 测试 RTN 量化误差
if __name__ == "__main__":
    w = torch.randn(128, 512)
    w_dequant, scale, zp = quantize_asymmetric_int4(w)
    mse = torch.mean((w - w_dequant)**2).item()
    print(f"[RTN INT4 MSE Loss]: {mse:.6f}")
```

---

## ⚠️ 4. 常见陷阱与避坑指南

1. **W4A16 vs W4A4**：AWQ 和 GPTQ 主要应用于 **W4A16**（权重 4-bit，激活保持 FP16/BF16），适合 Memory-bound 的 Decoder 生成场景；而在 Prefill 阶段（Compute-bound），仍建议使用 SmoothQuant 做 W8A8 量化。
2. **校准集 (Calibration Set)**：GPTQ 和 AWQ 均需要少量校准数据（如 128 条 C4 语料）计算 Hessian 矩阵或激活特征，校准集应尽量覆盖多语言与长上下文。

---

## 🛠️ 5. 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：为什么简单 Round-To-Nearest (RTN) 会导致 INT4 大模型产生严重的文本重复或退化？
- [ ] **问题 2**：GPTQ 如何利用黑塞矩阵 $H^{-1}$ 实现“量化某一列权重后自动更新剩余列”？
- [ ] **问题 3**：AWQ 的核心发现是什么？它是如何通过等价数学变换保护那 1% 的显著通道的？

---

## 🃏 6. 闭卷提取练习 (Self-Quiz)

1. **代数推导**：给出二阶泰勒展开重构误差目标函数，推导 GPTQ 权重更新量 $\Delta w$。
2. **代码自测**：写出非对称量化的 Scale 与 Zero-Point 的计算公式与代码实现。
3. **防错自测**：说明在量化后推理时，权重在显存中以什么格式存储？计算时以什么格式运行？

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
