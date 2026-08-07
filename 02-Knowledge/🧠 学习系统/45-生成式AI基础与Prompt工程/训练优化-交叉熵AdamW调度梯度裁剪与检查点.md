---
type: study
topic: "交叉熵、AdamW、学习率调度、梯度裁剪与检查点"
tags: [学习, 45-生成式AI基础与Prompt工程, 训练优化, AdamW]
created: 2026-08-05
status: completed
mastery: not_started
difficulty: intermediate
concept: ["交叉熵", "AdamW", "训练状态"]
prerequisites: ["深度学习工程-PyTorch张量自动微分与训练循环", "课程前置-概率向量与Softmax最小补丁"]
related: ["Transformer与大语言模型-训练-GPT与自回归语言模型", "Stanford-CS336-A1-逐节知识点映射"]
flow: knowledge
kind: concept
source: "Stanford CS336 Spring 2025 Assignment 1 Basics optimizer and training sections, MIT License"
anki_deck: "45-生成式AI基础与Prompt工程::训练优化"
anki_tags: [交叉熵, AdamW, Warmup, 梯度裁剪, Checkpoint]
---

# 训练优化：交叉熵、AdamW、调度、裁剪与检查点

## 0. 学习边界

- **类别**：A 类（CS336 A1 §4–5 的训练工程主卡）。
- **判断理由**：CS336 要求的不只是调用优化器，还包括数值稳定交叉熵、AdamW 状态内存、warmup/cosine、全局梯度裁剪、批采样和保存恢复。

## 1. 这个知识点解决什么问题？

> 下一 token 训练怎样把 logits 变成稳定损失？为什么同一个梯度要经过动量、自适应缩放、权重衰减、学习率调度和裁剪？中断后怎样从同一状态继续？

这些组件共同定义训练动力学。只保存模型参数或只记录最终 loss，都不足以复现实验。

## 2. 为什么它重要？它有什么用？

- **数值稳定**：直接 `exp(logit)` 可能溢出，log-sum-exp 消去公共大常数。
- **优化稳定**：AdamW 为不同参数维度自适应缩放，并把权重衰减与损失梯度解耦。
- **训练控制**：warmup 避免初期大更新，cosine 平滑衰减，裁剪控制异常梯度范数。
- **可恢复性**：checkpoint 必须保存参数之外的优化器、调度器、步数和随机状态。

## 3. 学它之前需要哪些前置知识？

1. [[课程前置-概率向量与Softmax最小补丁]]：softmax、log 概率和类别索引。
2. [[深度学习工程-PyTorch张量自动微分与训练循环]]：batch 损失、梯度累积和参数更新。

## 4. 用直觉语言解释它

> “交叉熵告诉模型正确 token 的惊讶程度；AdamW 为每个参数维护速度表和路况表；调度器控制油门；裁剪器限制突发冲击；checkpoint 保存整辆车的行驶状态。”

- 一句话本质：**一个可复现训练 step 是从 batch 与完整状态到新状态的确定变换。**

## 5. 正式定义、核心公式、符号解释

### 1. 数值稳定交叉熵

对 logits $z\in\mathbb{R}^{V}$ 和正确类别 $y$：

$$\ell(z,y)=-z_y+\log\sum_{j=1}^{V}e^{z_j}
=-z_y+m+\log\sum_j e^{z_j-m},\quad m=\max_j z_j.$$

减去 $m$ 不改变 softmax，却使最大指数为 1，避免溢出。

### 2. AdamW

$$m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,$$
$$v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2,$$
$$\hat m_t=\frac{m_t}{1-\beta_1^t},\qquad
\hat v_t=\frac{v_t}{1-\beta_2^t},$$
$$\theta_t=(1-\eta_t\lambda)\theta_{t-1}
-\eta_t\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}.$$

“解耦”指权重衰减直接作用于参数，而不是先把 $\lambda\theta$ 混进梯度再由自适应分母缩放。

### 3. Warmup + Cosine

$$\eta_t=\eta_{max}\frac{t}{T_w},\quad t<T_w,$$
$$\eta_t=\eta_{min}+\frac12(\eta_{max}-\eta_{min})
\left[1+\cos\left(\pi\frac{t-T_w}{T-T_w}\right)\right],\quad T_w\le t\le T.$$

### 4. 全局范数裁剪

$$G=\sqrt{\sum_k\|g_k\|_2^2},\qquad
g_k\leftarrow g_k\min\left(1,\frac{c}{G+\epsilon}\right).$$

| 符号 | 含义 | 关键边界 |
| :--- | :--- | :--- |
| $V$ | 词表大小 | logits 最后一维 |
| $m_t,v_t$ | 一、二阶矩状态 | 每个参数各两份 |
| $\beta_1,\beta_2$ | 指数衰减系数 | 常接近 1 |
| $\lambda$ | 权重衰减 | 常不用于 bias/norm 参数 |
| $c$ | 裁剪阈值 | 只在全局范数超过时缩放 |

### 5. 状态内存与 checkpoint

若参数使用 FP32，AdamW 参数、梯度、$m$、$v$ 的核心存储约为每参数 16 bytes，尚未计激活和框架开销。checkpoint 至少保存：模型、优化器、调度器、当前 step、数据迭代位置、配置和随机数状态。

## 6. 推导思路和思想来源

1. 负对数似然把“提高正确类别概率”变成可加损失。
2. log-sum-exp 用平移不变性解决指数溢出。
3. 一阶矩平滑方向，二阶矩按历史平方梯度缩放步长；偏置修正补偿初始零状态。
4. 独立权重衰减避免自适应预条件器扭曲正则化强度。
5. warmup、cosine 与裁剪分别控制训练早期、全程和异常 batch 的更新幅度。
6. 完整 checkpoint 使下一 step 的输入状态与不中断训练一致。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

logits `[1000, 999]` 若直接指数会溢出。减去最大值得 `[0,-1]`，正确类别 0 的损失为 $\log(1+e^{-1})\approx0.3133$。

### 例子 2：中等例子

两个梯度向量范数分别为 3 和 4，全局范数为 5。若阈值 $c=2.5$，所有梯度统一乘 0.5；不能分别把两组裁到 2.5，否则方向改变。

### 例子 3：实际应用例子（可运行 Python）

```python
# 输入：logits、标量参数梯度；输出：稳定 CE、调度学习率与 AdamW 更新。
import math

def cross_entropy(logits: list[float], target: int) -> float:
    maximum = max(logits)
    log_sum_exp = maximum + math.log(sum(math.exp(x - maximum) for x in logits))
    return log_sum_exp - logits[target]

def schedule(step: int, warmup: int, total: int, maximum: float, minimum: float) -> float:
    if step < warmup:
        return maximum * step / warmup
    ratio = min(1.0, (step - warmup) / (total - warmup))
    return minimum + 0.5 * (maximum - minimum) * (1 + math.cos(math.pi * ratio))

def adamw_step(theta, grad, first, second, step, lr, beta1=0.9, beta2=0.999,
               weight_decay=0.01, epsilon=1e-8):
    first = beta1 * first + (1 - beta1) * grad
    second = beta2 * second + (1 - beta2) * grad * grad
    first_hat = first / (1 - beta1 ** step)
    second_hat = second / (1 - beta2 ** step)
    theta = theta * (1 - lr * weight_decay) - lr * first_hat / (math.sqrt(second_hat) + epsilon)
    return theta, first, second

loss = cross_entropy([1000.0, 999.0], 0)
lr = schedule(step=10, warmup=5, total=100, maximum=1e-3, minimum=1e-5)
theta, first, second = adamw_step(1.0, 0.25, 0.0, 0.0, 1, lr)
print(round(loss, 4), lr, theta)
assert abs(loss - 0.3132616875) < 1e-8
assert theta < 1.0
```

## 8. 常见误区和易混概念

- **误区 1**：softmax 后再取 log 与稳定 CE 等价于数值实现。数学等价，浮点稳定性不同。
- **误区 2**：AdamW 就是 Adam 的梯度加 L2。自适应缩放下二者更新不同。
- **误区 3**：梯度裁剪是逐参数截断。常用方法按所有参数的全局 $L_2$ 范数同比缩放。
- **误区 4**：checkpoint 只保存权重。缺优化器和 RNG 会改变恢复后的轨迹。

| 概念 | 核心问题 | 关键区别 | 场景 |
| :--- | :--- | :--- | :--- |
| L2 正则 | 在目标中惩罚大参数 | 梯度进入预条件器 | SGD 常见 |
| AdamW 衰减 | 更新时直接缩小参数 | 与梯度预条件解耦 | Transformer 训练 |
| 梯度裁剪 | 限制当前更新冲击 | 不等于参数截断 | 异常梯度 |
| 学习率调度 | 改变基础步长 | 不直接改梯度方向 | 全程训练 |

## 9. 相关知识点与 Obsidian 双链建议

- 上游：[[深度学习工程-PyTorch张量自动微分与训练循环]]。
- 下游：[[Transformer与大语言模型-训练-GPT与自回归语言模型]]。
- 横向：[[Prompt评测-实验-指标数据集与误差分析]]，训练实验也必须受控和逐样本保存。
- 作业：[[Stanford-CS336-A1-逐节知识点映射]]。

## 10. 闭卷复现任务

- [ ] 从负对数似然写出交叉熵。
- [ ] 推出稳定 log-sum-exp 形式。
- [ ] 写出 AdamW 的 $m,v$ 与偏置修正。
- [ ] 解释解耦权重衰减。
- [ ] 手算一次全局范数裁剪。
- [ ] 写出 warmup/cosine 分段式。
- [ ] 估算 FP32 AdamW 核心状态内存。
- [ ] 列出 checkpoint 必需字段。
- [ ] 设计保存/恢复等价测试。
- [ ] 区分 loss spike、梯度爆炸和数据异常。

## 11. 自测题：5 道

1. 为什么 logits 同减常数不改变 softmax？ `#自测题/基础`
2. logits `[0,0]` 对类别 1 的交叉熵是多少？ `#自测题/基础`
3. 梯度范数为 10、阈值为 2 时缩放系数是多少？ `#自测题/中等`
4. AdamW 为什么需要偏置修正？ `#自测题/中等`
5. 设计一个中断/恢复回归测试，要求恢复后连续三步参数逐元素相同。 `#自测题/较难`

> [!question]- 参考答案与评分点
> 1. 分子分母同乘 $e^{-c}$ 抵消。2. $\log2$。3. 0.2。4. 初始矩状态为零，使早期指数均值偏向零。5. 固定 batch 顺序与所有 RNG；保存模型/优化器/调度器/step/RNG；在相同后续 batch 上比较 loss、梯度和参数。

## 12. 我的主动回忆区

- **稳定 CE**：
- **AdamW 更新**：
- **恢复状态清单**：
- [ ] 明天  [ ] 3 天后  [ ] 7 天后  [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- 本卡承担 CS336 优化与训练状态主线；模型架构仍回到 Transformer 卡。
- 真实作业必须使用官方 tests/adapters 和环境；本卡标准库代码只验数学与状态转换。

## 🃏 Anki 卡片

Q: AdamW 与把 L2 项加进 Adam 梯度的核心区别是什么？
A: AdamW 直接衰减参数，不让权重衰减项经过自适应矩估计和分母缩放。

Q: 一个可恢复 checkpoint 至少保存什么？
A: 模型、优化器、调度器、step、数据位置、配置及所有相关随机数状态。

