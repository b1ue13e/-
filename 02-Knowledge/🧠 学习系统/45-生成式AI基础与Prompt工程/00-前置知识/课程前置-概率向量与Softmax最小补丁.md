---
type: study
topic: "概率、向量与 Softmax 最小补丁"
course: "生成式AI基础与Prompt工程"
tags: [学习, 45-生成式AI基础与Prompt工程, 数学前置, Softmax]
created: 2026-08-05
status: completed
mastery: not_started
difficulty: beginner
stage_moc: "[[🧭 生成式AI基础与Prompt工程-前置知识]]"
concept: ["条件概率", "向量", "Softmax"]
prerequisites: ["初中代数", "指数函数直觉"]
related: ["生成式AI-基础-概率生成Token与能力边界", "Transformer与大语言模型-架构-Transformer工作原理"]
flow: knowledge
kind: concept
source: "MIT OCW 6.7960 Deep Learning Fall 2024 Homework 1; Stanford CS336 Spring 2025 Assignment 1"
source_url: "https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/"
accessed: 2026-08-09
license: "CC BY-NC-SA 4.0；CS336 A1 仓库为 MIT License"
anki_deck: "45-生成式AI基础与Prompt工程::课程前置"
anki_tags: [概率, 向量, Softmax]
---

# 课程前置：概率、向量与 Softmax 最小补丁

## 0. 学习边界

- **类别**：B 类（刚好够课程作业使用的数学工具）。
- **判断理由**：无需先学完整概率论和线性代数，但必须能读懂 logits、概率分布、点积和张量形状。

## 1. 这个知识点解决什么问题？

> 模型给出的不是“答案”，而是一组候选分数。我们需要知道这些分数如何变成概率，以及注意力为何用向量相似度。

## 2. 为什么它重要？它有什么用？

- 解释 temperature、top-k、交叉熵和困惑度。
- 检查 Transformer 中矩阵形状和注意力权重。
- 手算小例子，防止只会调用库却不理解结果。

## 3. 学它之前需要哪些前置知识？

1. 会做加减乘除和指数的基本比较。
2. 知道函数把输入映射为输出；本卡不要求微积分证明。

## 4. 用直觉语言解释它

> “向量是一排特征刻度；点积看两排刻度是否同向；softmax 把任意分数变成总和为 1 的投票比例。”

## 5. 正式定义、核心公式、符号解释

条件概率满足 $P(y\mid x)\ge0$ 且 $\sum_yP(y\mid x)=1$。对 logits $z_i$：

$$\operatorname{softmax}(z)_i=\frac{e^{z_i}}{\sum_j e^{z_j}},\qquad
\operatorname{softmax}(z/\tau)_i=\frac{e^{z_i/\tau}}{\sum_j e^{z_j/\tau}}.$$

向量点积为 $q\cdot k=\sum_iq_ik_i$；Transformer 用 $QK^\top/\sqrt{d_k}$ 产生注意力分数。

| 符号 | 含义 | 范围 | 备注 |
| :--- | :--- | :--- | :--- |
| $z_i$ | 第 $i$ 个候选的 logit | 实数 | 不是概率 |
| $\tau$ | 温度 | 正数 | 越小分布越尖 |
| $d_k$ | key/query 维度 | 正整数 | 缩放防止分数过大 |

## 6. 推导思路和思想来源

- 指数函数把更大分数变成更大正数。
- 除以总和得到总和为 1 的分布。
- softmax 对所有 logits 同加常数不变，因此实现时减去最大值可避免溢出。
- 低温等价于放大分数差，高温等价于压小分数差。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

logits 为 `[0, 0]` 时，两项指数都为 1，概率为 `[0.5, 0.5]`。logits 为 `[ln 3, 0]` 时，概率为 `[0.75, 0.25]`。

### 例子 2：中等例子

$q=(1,0)$ 与 $k_1=(1,0)$ 的点积为 1，与 $k_2=(0,1)$ 的点积为 0，因此在其他条件相同时更关注 $k_1$。

### 例子 3：实际应用例子（可运行 Python）

```python
# 输入：logits 与温度；输出：数值稳定的概率分布。
import math

def softmax(logits: list[float], temperature: float = 1.0) -> list[float]:
    if temperature <= 0:
        raise ValueError("temperature 必须大于 0")
    scaled = [value / temperature for value in logits]
    maximum = max(scaled)
    weights = [math.exp(value - maximum) for value in scaled]
    total = sum(weights)
    return [weight / total for weight in weights]

for temperature in (0.5, 1.0, 2.0):
    probabilities = softmax([2.0, 1.0, 0.0], temperature)
    print(temperature, [round(value, 3) for value in probabilities])
    assert abs(sum(probabilities) - 1.0) < 1e-9
```

输出显示温度升高时概率更平均。

## 8. 常见误区和易混概念

- **误区**：最高 logit 就是 100% 正确。它只是在当前候选中模型分数最高。
- **误区**：概率代表事实置信度。下一 Token 概率不是命题真实性概率。

| 概念 | 核心问题 | 关键区别 | 场景 |
| :--- | :--- | :--- | :--- |
| logit | 模型给候选多少原始分 | 可为任意实数 | softmax 前 |
| 概率 | 候选如何分配质量 | 非负且总和为 1 | 采样 |
| 校准置信度 | 预测频率是否匹配正确率 | 需要外部标签评估 | 可靠性 |

## 9. 课程连接

- 本卡只补足读取 logits、概率分布、点积和温度公式所需的最小数学，不替代完整概率论或线性代数课程。
- 进入主线后在 [[生成式AI-基础-概率生成Token与能力边界]]、[[生成控制-解码-温度Top-k与Top-p]] 和 [[Transformer与大语言模型-架构-Transformer工作原理]] 中复用这些工具。
- 跨路径：[[🗺️ 概率论与数理统计学习路径|概率论学习路径]]。

## 10. 闭卷复现任务

- [ ] 手算 `[0,0]` 的 softmax。
- [ ] 解释为什么减去最大 logit 不改变结果。
- [ ] 解释温度升高对分布的影响。
- [ ] 计算两个二维向量的点积。
- [ ] 区分 Token 概率与事实置信度。
- [ ] 写出 softmax 数值稳定实现的主线。
- [ ] 说明温度趋近 0 时的极限行为。
- [ ] 检查概率和是否为 1。
- [ ] 解释 $\sqrt{d_k}$ 缩放的直觉。
- [ ] 说出一个 softmax 在生成中的真实应用。

## 11. 自测题：5 道

1. `[ln 3,0]` 的 softmax 是多少？ `#自测题/基础`
2. $q=(1,2),k=(3,4)$ 的点积是多少？ `#自测题/基础`
3. 为什么直接计算 `exp(1000)` 不安全？ `#自测题/中等`
4. 将所有 logits 加 7，概率是否改变？证明。 `#自测题/中等`
5. 设计一个反例说明“最高 Token 概率高”不等于整句事实正确。 `#自测题/较难`

> [!question]- 参考答案与评分点
> 1. `[0.75,0.25]`。2. `11`。3. 可能数值溢出，应先减最大值。4. 不变，分子分母同乘 $e^7$ 后约掉。5. 需指出局部续写概率与外部世界真值不是同一变量。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/45-生成式AI基础与Prompt工程"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 12. 我的主动回忆区

- **闭卷复述**：
- **手算记录**：
- **仍不理解的符号**：
- [ ] 明天  [ ] 3 天后  [ ] 7 天后  [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- 本卡只承担最小数学补丁；完整证明和统计推断回到概率论、线性代数路径。
- 若 5 道自测错 2 道以上，先补本卡再进入 Transformer。

## 🃏 Anki 卡片

Q: Softmax 实现为什么先减最大 logit？
A: Softmax 对整体平移不变；减最大值可避免指数溢出而不改变概率。

Q: temperature 升高通常怎样改变分布？
A: 压小 logit 差异，使分布更平坦、采样更多样。

