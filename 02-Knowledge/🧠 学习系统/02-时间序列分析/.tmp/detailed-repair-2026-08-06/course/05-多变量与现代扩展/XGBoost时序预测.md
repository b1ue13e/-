---
type: study
topic: "XGBoost 时序预测"
tags: [学习, 时间序列, XGBoost, 机器学习]
created: 2026-04-16
updated: 2026-08-05
status: completed
difficulty: intermediate
concept: ["梯度提升树", "时序监督学习", "滞后特征"]
prerequisites: ["时序特征工程", "滚动回测", "决策树"]
related: ["动态回归与ARIMAX", "时间序列交叉验证", "预测区间"]
flow: knowledge
kind: concept
source: "Chen & Guestrin, XGBoost, KDD 2016"
anki_deck: "时间序列分析::机器学习"
anki_tags: [时间序列, XGBoost, 泄漏]
course: "时间序列分析"
stage_moc: "[[🧭 阶段5-多变量与现代扩展]]"
upstream: ["[[时序特征工程与ML预测]]"]
---
# XGBoost 时序预测

## 0. 它解决什么问题

XGBoost 本身不知道时间顺序。它解决的是表格监督回归：给定特征 $X_t$，拟合非线性函数 $\hat y_{t+h}=f(X_t)$。要用于时序，必须先把历史、日历和外生信息转换成符合预测原点的信息集。

适合：多序列、外生特征丰富、阈值/交互明显。短单序列、长期外推和概率区间不是它的天然优势。

## 1. 正式目标

梯度提升逐轮添加树：

$$
\hat y_i^{(m)}=\hat y_i^{(m-1)}+\eta f_m(x_i),
$$

通过正则化目标平衡损失与树复杂度。时序约束不在目标函数里，而在样本构造和验证协议里。

## 2. 三种多步策略

| 策略 | 做法 | 风险 |
|---|---|---|
| recursive | 训练一步模型，递归使用预测值 | 误差累积、训练部署分布不同 |
| direct | 每个 horizon 单独模型 | 模型多，跨 horizon 不一致 |
| multi-output | 一个模型输出多个 horizon | 标准 XGBoost 需额外封装 |

必须在实验前声明策略。不能在测试期用真实 $y_{t+1}$ 生成预测 $y_{t+2}$，除非任务本来就是每期滚动更新的一步预测。

## 3. 特征边界

- `lag_1 = y.shift(1)`：预测 $y_t$ 时可用；
- `rolling_7 = y.shift(1).rolling(7).mean()`：先移位再滚动；
- 日历特征：未来日期已知，可用于直接多步；
- 促销/天气：只有预测原点已经发布的计划或预报可用；
- 编码、填补和特征筛选：只在训练窗口拟合。

## 4. 可运行的一步滚动例子

先安装：`python -m pip install xgboost`。

```python
import numpy as np
import pandas as pd
from xgboost import XGBRegressor

rng = np.random.default_rng(41)
n = 420
t = np.arange(n)
y = 20 + 2 * np.sin(2 * np.pi * t / 7) + 0.4 * rng.normal(size=n)
frame = pd.DataFrame({"y": y})
frame["lag1"] = frame["y"].shift(1)
frame["lag7"] = frame["y"].shift(7)
frame["mean7"] = frame["y"].shift(1).rolling(7).mean()
frame["dow_sin"] = np.sin(2 * np.pi * t / 7)
frame["dow_cos"] = np.cos(2 * np.pi * t / 7)
frame = frame.dropna()

features = ["lag1", "lag7", "mean7", "dow_sin", "dow_cos"]
split = 320
train, test = frame.iloc[:split], frame.iloc[split:]

model = XGBRegressor(
    n_estimators=120, max_depth=3, learning_rate=0.05,
    subsample=0.9, colsample_bytree=0.9,
    objective="reg:squarederror", random_state=41, n_jobs=1,
)
model.fit(train[features], train["y"])
pred = model.predict(test[features])
naive = test["lag7"].to_numpy()

mae = lambda a, b: float(np.mean(np.abs(np.asarray(a) - np.asarray(b))))
print({"xgboost": round(mae(test["y"], pred), 3),
       "seasonal_naive": round(mae(test["y"], naive), 3)})
# 这是每个预测原点已观察到上一期真实值的一步滚动评估。
```

## 5. 手算基础例子

预测 $y_t$ 时，最近观测为 $y_{t-1}=10$，过去 7 期为 `[8,9,9,10,11,10,10]`：

- `lag1=10`；
- `mean7=67/7\approx9.57`；
- 若目标是 $y_{t+2}$ 且一次性在 $t$ 预测，$y_{t+1}$ 不能用真实值，只能采用 direct 特征或递归预测。

## 6. 常见误区

- 随机 K 折：未来结构进入训练。
- 全样本先造滚动特征：窗口可能跨越切分或混入当前目标。
- 树能自动外推趋势：树主要在训练特征范围内分段预测，长期外推通常弱。
- 特征重要性等于因果：分裂增益只反映模型内关联。
- 只比较另一个 ML 模型：必须含朴素与统计基线。

## 7. 闭卷验收与自测

1. XGBoost 为什么“不懂时间”？`#自测题/基础`
2. 写出无泄漏 7 期滚动均值。`#自测题/基础`
3. direct 与 recursive 多步预测有何差异？`#自测题/中等`
4. 为什么树模型难以外推未见趋势？`#自测题/中等`
5. 设计逐 horizon、公平含基线的验证。`#自测题/较难`

> [!answer]- 自测答案
> 1. 它接收独立表格行，顺序约束来自特征和切分。  
> 2. `y.shift(1).rolling(7).mean()`。  
> 3. direct 每个 horizon 单独学习；recursive 重复一步模型并使用自身预测。  
> 4. 树叶在训练区域给分段常数，缺少参数化趋势外推。  
> 5. 对每个滚动起点重建可得特征，逐 horizon 与 naïve/seasonal naïve/统计模型比较。

## 8. 来源与双链

- 原始算法：[Chen & Guestrin, XGBoost, KDD 2016](https://arxiv.org/abs/1603.02754)
- 上游：[[时序特征工程与ML预测]]
- 下游：[[滚动回测与预测区间]]

## 🃏 Anki 卡片

### Card 1
Q: 用 XGBoost 预测 y_t 时，7 期滚动均值怎样防止当前值泄漏？
A: 先 shift(1) 再 rolling(7)，只聚合 t-1 及更早观测。
Tags: 时间序列 XGBoost 泄漏

## 派生视图

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

