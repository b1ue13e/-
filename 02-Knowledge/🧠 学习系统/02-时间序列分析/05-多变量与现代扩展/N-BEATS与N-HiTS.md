---
type: study
topic: "N-BEATS 与 N-HiTS"
tags: [学习, 时间序列, N-BEATS, N-HiTS, 深度学习]
created: 2026-04-16
updated: 2026-08-05
status: completed
difficulty: advanced
concept: ["残差堆叠", "基函数展开", "层次插值"]
prerequisites: ["前馈神经网络", "多步预测", "时间序列交叉验证"]
related: ["时间序列分解", "Transformer时序", "滚动回测"]
flow: knowledge
kind: concept
source: "N-BEATS ICLR 2020; N-HiTS AAAI 2023"
anki_deck: "时间序列分析::深度学习"
anki_tags: [时间序列, NBEATS, NHITS]
course: "时间序列分析"
stage_moc: "[[🧭 阶段5-多变量与现代扩展]]"
upstream: ["[[Transformer 时序预测]]"]
---
# N-BEATS 与 N-HiTS

## 0. 它们解决什么问题

两者都是面向多步预测的前馈残差架构，不依赖循环或标准自注意力。模型把历史窗口逐块解释：每个块输出对历史的 **backcast** 与对未来的 **forecast**，未解释的历史残差交给后续块。

N-BEATS 强调基函数展开与残差堆叠；N-HiTS 增加多速率下采样和层次插值，使不同块聚焦不同频率尺度。

## 1. N-BEATS 的残差堆叠

第 $\ell$ 块接收残差 $x_\ell$，输出

$$\hat x_\ell=V^b_\ell\theta^b_\ell,\qquad
\hat y_\ell=V^f_\ell\theta^f_\ell,$$

并更新

$$x_{\ell+1}=x_\ell-\hat x_\ell,\qquad
\hat y=\sum_\ell\hat y_\ell.$$

generic 版本的基展开可学习；interpretable 版本使用趋势多项式和季节 Fourier 基。可解释版本的分量是架构约束下的表示，不自动等于真实因果趋势/季节。

## 2. N-HiTS 的层次思想

N-HiTS 让不同块使用不同下采样率和较少的预测系数，再通过插值恢复完整 horizon：

- 低分辨率块关注慢变化与长尺度；
- 高分辨率块关注局部快速变化；
- 多尺度 forecast 相加形成最终预测。

这降低长 horizon 输出的参数与计算，但具体收益依赖序列平滑度、采样率和数据规模。

## 3. 手算一个残差块

输入窗口 $x=[3,5,4]$。第一块 backcast 为 `[2,4,4]`，forecast 为 `[5,6]`：

$$x_2=x-\hat x_1=[1,1,0].$$

第二块 backcast `[1,1,0]`，forecast `[0.5,0.2]`。最终历史残差为零，预测为 `[5.5,6.2]`。训练时 backcast 与 forecast 由网络共同学习，而不是手工指定。

## 4. 可运行的结构 smoke test

下面只验证“残差递减、预测相加”的核心张量逻辑，不冒充完整 N-BEATS 训练器：

```python
import numpy as np

x = np.array([3.0, 5.0, 4.0])
backcasts = [
    np.array([2.0, 4.0, 4.0]),
    np.array([1.0, 1.0, 0.0]),
]
forecasts = [
    np.array([5.0, 6.0]),
    np.array([0.5, 0.2]),
]

residual = x.copy()
forecast = np.zeros(2)
for backcast, block_forecast in zip(backcasts, forecasts):
    residual = residual - backcast
    forecast = forecast + block_forecast

print("remaining backcast residual:", residual)
print("combined forecast:", forecast)
assert np.allclose(residual, [0, 0, 0])
assert np.allclose(forecast, [5.5, 6.2])
```

真实训练使用经过审计的实现，例如 [Nixtla NeuralForecast](https://github.com/Nixtla/neuralforecast)。运行真实模型时必须记录库版本、输入窗口、horizon、缩放、损失、随机种子和早停规则。

## 5. 何时值得使用

- 有大量相关序列，可训练 global model；
- 预测 horizon 固定且较长；
- 有足够历史覆盖季节与漂移；
- 朴素、ETS/ARIMA 与树模型已经建立；
- 计算预算允许在滚动起点重训或模拟真实更新。

单条短序列、频繁结构突变、强外生驱动但无未来外生预测时，不应仅因架构新而优先使用。

## 6. 公平验证清单

1. 同一训练窗口、预测原点和 horizon。
2. 预处理仅在训练段拟合。
3. 模型调参预算尽量可比，并报告训练成本。
4. 逐 horizon 与 seasonal naïve、ETS/ARIMA、树模型比较。
5. 报告多个随机种子，而不是最好一次。
6. 点损失之外检查区间/分位数校准；所用 loss 与输出分布一致。

## 7. 常见误区

- N-BEATS 的趋势栈自动发现真实趋势：它发现的是预测有用的受约束分量。
- N-HiTS 必然优于 Transformer：论文基准不等于任意新数据。
- 深度模型无需特征与数据审计：时间索引、缺失和信息边界仍是前提。
- 单次 holdout 足够：深度模型对窗口和随机种子可能敏感。
- 只按平均 MAE：长 horizon 可能掩盖近端失败。

## 8. 闭卷验收与自测

1. 解释 backcast 与 forecast。`#自测题/基础`
2. 写出残差更新和预测求和。`#自测题/基础`
3. N-HiTS 比 N-BEATS 增加什么核心思想？`#自测题/中等`
4. 为什么 interpretable stack 不等于因果分解？`#自测题/中等`
5. 设计含多个随机种子的公平对比。`#自测题/较难`

> [!answer]- 自测答案
> 1. backcast 解释输入历史，forecast 给出该块的未来贡献。  
> 2. $x_{l+1}=x_l-\hat x_l$，总预测为各块 forecast 之和。  
> 3. 多速率采样与层次插值，使不同块处理不同频率尺度。  
> 4. 分量由架构和损失识别，不具备外部因果识别假设。  
> 5. 固定数据与预算，对多个种子报告均值/波动，并逐 horizon 比基线。

## 9. 来源与双链

- [N-BEATS, ICLR 2020](https://arxiv.org/abs/1905.10437)
- [N-HiTS, AAAI 2023](https://ojs.aaai.org/index.php/AAAI/article/view/25854)
- 上游：[[时间序列结构-趋势季节噪声与ETS分解]]
- 评估：[[滚动回测与预测区间]]

## 🃏 Anki 卡片

### Card 1
Q: N-BEATS 每个块怎样更新历史与未来预测？
A: 用 backcast 从当前历史残差中扣除已解释部分，并把该块 forecast 加到总预测。
Tags: 时间序列 NBEATS

## 学完后可以完成

完成本卡后，使用下面的派生视图定位下游知识和可执行验收入口；作业关系只维护在作业的 `requires` 字段。

### 派生视图

### 下游知识

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

### 可完成作业

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```





