---
type: study
topic: "RMSNorm、SwiGLU、RoPE 与 Transformer 资源核算"
tags: [学习, 45-生成式AI基础与Prompt工程, Transformer工程, CS336]
created: 2026-08-05
status: completed
mastery: not_started
difficulty: advanced
concept: ["RMSNorm", "RoPE", "Transformer核算"]
prerequisites: ["Transformer与大语言模型-架构-Transformer工作原理", "深度学习工程-PyTorch张量自动微分与训练循环"]
related: ["训练优化-交叉熵AdamW调度梯度裁剪与检查点", "Stanford-CS336-A1-逐节知识点映射"]
flow: knowledge
kind: concept
source: "Stanford CS336 Spring 2025 Assignment 1 Basics Section 3, MIT License repository"
anki_deck: "45-生成式AI基础与Prompt工程::Transformer工程"
anki_tags: [RMSNorm, SwiGLU, RoPE, 参数量, FLOPs]
---

# Transformer 工程：RMSNorm、SwiGLU、RoPE 与资源核算

## 0. 学习边界

- **类别**：A 类（CS336 A1 §3 架构补丁）。
- **判断理由**：通用 Transformer 卡解释大图景，本卡负责官方实现实际要求的 RMSNorm、SwiGLU、RoPE、因果 MHA、参数/FLOP/激活核算。

## 1. 这个知识点解决什么问题？

> 现代 decoder-only Transformer 如何稳定归一化、注入相对位置、提高 FFN 表达，并在写代码前算清 shape、参数、注意力复杂度和显存？

## 2. 为什么它重要？它有什么用？

- RMSNorm 是现代 LLM 常用归一化，和 LayerNorm 不同。
- SwiGLU 用门控分支替代简单 ReLU FFN。
- RoPE 在 Q/K 二维子空间旋转，使点积包含相对位置信息。
- 核算能在运行前发现 shape/预算不可能，支撑 CS336 accounting 和 scaling 实验。

## 3. 学它之前需要哪些前置知识？

1. [[Transformer与大语言模型-架构-Transformer工作原理]]：Q/K/V、mask、残差、Pre-Norm。
2. [[深度学习工程-PyTorch张量自动微分与训练循环]]：tensor shape、module 与测试。

## 4. 用直觉语言解释它

> “RMSNorm 调整整体音量但不减均值；SwiGLU 用一支内容、一支门控制信息；RoPE 给每对坐标按位置转角；核算表则是施工前的材料清单。”

## 5. 正式定义、核心公式、符号解释

RMSNorm：
$$\operatorname{RMSNorm}(x)=\frac{x}{\sqrt{\frac1d\sum_i x_i^2+\epsilon}}\odot g.$$
它不减均值，通常只有 scale $g$。

SwiGLU：
$$\operatorname{SwiGLU}(x)=\big(\operatorname{SiLU}(xW_1)\odot xW_3\big)W_2,$$
$$\operatorname{SiLU}(a)=a\sigma(a).$$

RoPE 对每对坐标使用旋转矩阵：
$$R_{p,\theta}=\begin{bmatrix}\cos(p\theta)&-\sin(p\theta)\\\sin(p\theta)&\cos(p\theta)\end{bmatrix},$$
$$q_p'=R_pq_p,\quad k_s'=R_sk_s,\quad q_p'^Tk_s'=q_p^TR_{s-p}k_s.$$

Decoder block 典型 shape：输入 `[B,T,d]`，Q/K/V reshape 为 `[B,h,T,d_h]`，scores `[B,h,T,T]`，输出回 `[B,T,d]`。

忽略 bias 的主要参数：embedding $Vd$；每层 attention 约 $4d^2$；SwiGLU 约 $3dd_{ff}$；RMSNorm 约 $2d$。训练 FLOPs 常由矩阵乘与注意力主导，注意力 scores/softmax 随 $T^2$ 增长。

| 组件 | 参数量级 | 激活/计算瓶颈 |
| :--- | :---: | :--- |
| embedding | $Vd$ | logits 可大 |
| QKV+O | $4d^2$ | QK/AV 为 $O(BT^2d)$ |
| SwiGLU | $3dd_{ff}$ | 通常是每 token 主 FLOP |
| RoPE | 0 | sin/cos 或缓存 |
| RMSNorm | $d$ 每个 | $O(BTd)$ |

## 6. 推导思路和思想来源

1. RMSNorm 保留缩放归一化的主要稳定作用，省去均值中心化。
2. 门控 FFN 让一支特征选择另一支内容，提升参数利用。
3. 对 Q/K 同时按绝对位置旋转，点积中的旋转合并为位置差，得到相对位置结构。
4. 因果 mask 应在 softmax 前加到 scores；padding/causal mask 的广播 shape 必须测试。
5. 核算先按每层参数与 activation shape 分项，再乘层数；参数、梯度、优化器状态和激活不可混为一项。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

$x=(3,4)$，RMS 为 $\sqrt{(9+16)/2}=\sqrt{12.5}$；无 scale 时输出约 `(0.849,1.131)`，其均方为 1，但均值不必为 0。

### 例子 2：中等例子

$d=512,h=8$，则 $d_h=64$。若 `T=1024`，单层每头 score 有 $1024^2$ 个元素，8 头约 8.4M 元素/样本；增加上下文会平方放大。

### 例子 3：可运行 Python

```python
# 输入：二维向量与位置；输出：RMSNorm 和 RoPE 旋转，验证范数保持。
import math

def rmsnorm(vector, epsilon=1e-8):
    rms = math.sqrt(sum(value * value for value in vector) / len(vector) + epsilon)
    return [value / rms for value in vector]

def rotate(pair, position, theta=0.25):
    angle = position * theta
    cosine, sine = math.cos(angle), math.sin(angle)
    return [cosine * pair[0] - sine * pair[1], sine * pair[0] + cosine * pair[1]]

normalized = rmsnorm([3.0, 4.0])
rotated = rotate([3.0, 4.0], position=7)
print([round(value, 4) for value in normalized], [round(value, 4) for value in rotated])
assert abs(sum(value * value for value in normalized) / 2 - 1.0) < 1e-7
assert abs(sum(value * value for value in rotated) - 25.0) < 1e-9
```

## 8. 常见误区和易混概念

- RMSNorm 不等于 LayerNorm；前者不减均值。
- RoPE 通常作用在 Q/K，不是直接旋转 token ID 或 V。
- 对比学习温度、解码温度和 RoPE 频率不是同一概念。
- 参数显存不等于训练总显存；还要计梯度、Adam 状态、激活和临时 buffer。

| 概念 | 是否中心化 | 是否有参数 | 作用 |
| :--- | :---: | :---: | :--- |
| LayerNorm | 是 | scale+bias 常见 | 均值/方差归一 |
| RMSNorm | 否 | scale 常见 | 均方根缩放 |
| RoPE | 不适用 | 通常 0 | Q/K 位置旋转 |
| learned position | 不适用 | $T_{max}d$ | 位置向量相加 |

## 9. 相关知识点与 Obsidian 双链建议

- 作业：[[Stanford-CS336-A1-逐节知识点映射]] §3。
- 上游：[[Transformer与大语言模型-架构-Transformer工作原理]]。
- 训练：[[训练优化-交叉熵AdamW调度梯度裁剪与检查点]]。

## 10. 闭卷复现任务

- [ ] 写出 RMSNorm。
- [ ] 区分 RMSNorm 与 LayerNorm。
- [ ] 写出 SiLU 与 SwiGLU。
- [ ] 画出 Q/K/V shape。
- [ ] 写出二维 RoPE 旋转。
- [ ] 解释相对位置点积。
- [ ] 说明 causal mask 添加位置。
- [ ] 核算 attention 参数。
- [ ] 核算 SwiGLU 参数。
- [ ] 区分参数、激活和优化器状态内存。

## 11. 自测题：5 道

1. RMSNorm 是否减均值？ `#自测题/基础`
2. $d=768,h=12$ 时每头维度多少？ `#自测题/基础`
3. RoPE 为什么不增加 learned position 参数？ `#自测题/中等`
4. 序列长度翻倍时 attention score 元素数怎样变化？ `#自测题/中等`
5. 为 $L,d,d_{ff},V,T,B$ 写一张参数/激活/Adam 状态核算表，并指出哪个随 $T^2$。 `#自测题/较难`

> [!question]- 参考答案与评分点
> 1. 否。2. 64。3. 旋转角由固定频率/位置计算，可缓存。4. 约四倍。5. 参数主要 $Vd+L(4d^2+3dd_{ff})$；Adam 矩状态按参数线性；attention score activation 随 $BLhT^2$。

## 12. 我的主动回忆区

- **三组件公式**：
- **shape 流**：
- **资源表**：
- [ ] 明天  [ ] 3 天后  [ ] 7 天后  [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- 本卡是 CS336 §3 实现补丁；完整 CUDA/FlashAttention 和分布式核算进入系统课程。
- 实现前先写 shape 与参数表，单元测试通过后再拼 block。

## 🃏 Anki 卡片

Q: RMSNorm 与 LayerNorm 的核心区别是什么？
A: RMSNorm 只按均方根缩放，不减均值；LayerNorm 同时中心化并按方差缩放。

Q: RoPE 怎样引入相对位置？
A: 按绝对位置旋转 Q/K，而两者点积中的旋转合并为位置差对应的旋转。

