---
type: study
topic: "MA模型"
course: "时间序列分析"
created: 2026-04-18
updated: 2026-08-02
status: completed
difficulty: intermediate
concept: ["移动平均模型", "有限冲击响应", "可逆性"]
prerequisites: ["白噪声", "自相关函数ACF", "滞后算子"]
related: ["AR模型", "ARMA模型", "模型识别"]
tags: [学习, 时间序列, MA模型]
flow: knowledge
kind: derivation
sources:
  - title: "Forecasting: Principles and Practice (3rd ed.)"
    url: "https://otexts.com/fpp3/MA.html"
    locator: "Section 9.4: Moving average models and invertibility"
    source_type: "open-textbook"
    license: "CC BY-NC-SA 4.0"
    verified_at: 2026-08-02
stage_moc: "[[🧭 阶段3-经典预测模型]]"
upstream: ["[[L04-MA模型与有限冲击]]"]
---
# MA模型

> [!tip] 这张卡怎么学（60 分钟）
> 1. 先追踪一个创新在 MA(1)、MA(2) 中分别影响几期。
> 2. 再推导 MA(1) 的方差和一阶 ACF。
> 3. 最后比较 MA 模型与滑动平均平滑，写出两者建模对象的区别。
>
> **过关问题**：为什么 MA 的冲击有限，但还要满足可逆性？

移动平均模型 MA((q)) 把当前值写成当前及过去有限个创新冲击的线性组合：

$$
y_t=c+\varepsilon_t+\theta_1\varepsilon_{t-1}+\cdots+
\theta_q\varepsilon_{t-q},\qquad \varepsilon_t\sim WN(0,\sigma^2).
$$

这里的“移动平均”不是用于平滑趋势的滑动窗口均值。模型中的 (\varepsilon_t) 是不可直接观测的一步预测创新，参数通过整个序列联合估计。用滞后算子可写为 (y_t=c+\theta(B)\varepsilon_t)。

## 1. MA(1) 的性质

对 (y_t=c+\varepsilon_t+\theta\varepsilon_{t-1})，有

$$
\operatorname{Var}(y_t)=(1+\theta^2)\sigma^2,
\qquad
\rho_1=\frac{\theta}{1+\theta^2},
\qquad \rho_k=0\ (k>1).
$$

一次冲击只影响当前和下一期，因此 MA((q)) 的冲击响应在 (q) 期后严格归零。其理论 ACF 在 (q) 阶后截尾，PACF 通常拖尾。这与平稳 AR 模型的无限衰减冲击响应形成对照。

## 2. 可逆性为什么必要

不同 (\theta) 可能产生相同自相关结构。例如 MA(1) 的 (\theta) 与 (1/\theta) 给出相同 (\rho_1)。为获得唯一且稳定的创新表示，通常要求 (\theta(z)=0) 的根在单位圆之外；MA(1) 即 (|\theta|<1)。可逆性允许把创新写成当前和过去观测的收敛组合，便于估计与预测。

```python
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

rng = np.random.default_rng(64)
eps = rng.normal(size=260)
y = eps.copy()
y[1:] += 0.6 * eps[:-1]
y[2:] -= 0.25 * eps[:-2]
train = pd.Series(y[20:])

fit = ARIMA(train, order=(0, 0, 2), trend="c").fit()
pred = fit.get_forecast(steps=12)
interval = pred.conf_int(alpha=0.05)
print("MA parameters:", fit.params.round(3).to_dict())
print("forecast/interval shapes:", pred.predicted_mean.shape, interval.shape)
```

## 3. 识别与验收

1. 确保序列已近似平稳；MA 部分不能替代必要的差分或趋势建模。
2. 用 ACF 的低阶截尾提出候选 (q)，但不要仅凭肉眼定阶。
3. 用最大似然估计后检查可逆根、参数标准误和残差[[纯随机性检验]]。
4. 用 AICc 在**相同差分阶数**的候选中比较，再用滚动样本外误差最终验收。
5. 报告创新方差和预测区间；只报告系数显著性不能证明预测有效。

## 4. 预测直觉与边界

已估计的最近创新会进入短期预测；当预测步长超过 (q) 后，未知未来创新的条件期望为零，点预测回到长期均值。MA 适合描述短暂冲击，但对长持续性往往需要较高阶，此时低阶[[AR模型]]或[[ARMA模型]]更简洁。异常值会被误认为大创新并影响邻近期，结构突变也会破坏固定参数假设。

## 5. 开放教材定位

主线精读 FPP3 §9.4，重点区分 MA 模型和移动平均平滑，推导 MA(1) 方差与 ACF，并解释可逆性。验收标准是能从 ACF 提出候选、检查可逆根，并证明残差不再保留线性结构。

## 参考资料

- Hyndman & Athanasopoulos, [FPP3 §9.4 Moving average models](https://otexts.com/fpp3/MA.html)，MA((q)) 定义、冲击表示与可逆性。

## 🔬 深挖推导与自测

> 本节由原“MA模型（深挖笔记）”合并而来，保留完整推导、例题和闭卷自测。

> 主卡：[[MA模型]]｜本卡为深挖细节版，主线索引请走主卡。

### 0. 学习边界

**结论：A 类知识点，必须深挖。**

**理由：**
MA 模型与 AR 模型并列构成 ARMA 家族的两大基石。不理解 MA，就无法理解 ARMA 中"移动平均部分"的含义。MA 的可逆性、截尾 ACF 等性质是模型识别的关键。虽然单独使用 MA 的场景不如 AR 多，但它与 AR 的对偶关系（ACF 截尾 vs 拖尾）是整个 Box-Jenkins 方法的核心。

---

### 1. 这个知识点解决什么问题？

**我们遇到了什么麻烦？**

现实中有这样一类现象：一个突发事件的影响不会只持续一期，而是会在之后几期内逐渐消散。

- 央行突然降息——影响不止今天，下个月市场还在消化
- 公司发布超预期财报——股价波动可能持续几天
- 突发自然灾害——供应链影响可能持续数周

**以前的方法在哪里卡住？**

AR 模型说"当前值由过去的观测值决定"，但上述场景中，真正驱动序列的不是"过去值"本身，而是"过去的意外冲击"。昨天的高股价可能只是因为昨天的利好消息，而不是因为前天的高股价。

**为什么必须引入 MA 模型？**

MA 模型关注的是**冲击的传递**：当前值不仅受今天的意外影响，还受昨天、前天……意外的"残留影响"。

> **核心区别：** AR 记住过去的状态，MA 记住过去的意外。

---

### 2. 为什么它重要？它有什么用？

**不学它，后续哪些知识会看不懂？**
- ARMA 模型中 MA 部分的含义和作用
- ACF 截尾的识别逻辑（MA(q) 的 ACF 在 q 阶后截尾）
- 可逆性条件的来源和意义
- 为什么 MA 的参数估计比 AR 难（因为 $\varepsilon_{t-1}$ 不可观测）

**它在本课程中处于什么位置？**
- 板块C：经典模型层，与 AR 并列
- AR + MA = ARMA，是时间序列建模的两大基本构件

**实际应用场景：**
- **金融市场**：收益率的短期冲击传递（意外消息的影响在几天内消散）
- **供应链管理**：需求端的突发扰动（促销、天气）对库存的影响
- **信号处理**：噪声滤波中的 MA 滤波器

**考试中最常出现的题型：**
- 根据 ACF 截尾判断 MA 阶数
- MA(1) 的 ACF 计算
- 可逆性条件的判断
- AR 与 MA 的对比辨析

---

### 3. 学它之前需要哪些前置知识？

| 前置知识 | 用途 | 是否需要补课 |
|---------|------|------------|
| 白噪声 | $\varepsilon_t$ 的定义和性质 | 必须掌握 |
| 自协方差/方差 | 推导 MA 的 ACF | 需熟练 |
| 平稳性 | MA 天然平稳，但要理解为什么 | 简要了解即可 |
| AR 模型 | 对比学习 | 建议先学 AR |

**最小必要背景补充（若缺）：**

> **协方差的双线性展开：** 计算 $Cov(A+B, C+D)$ 时，可以像乘法分配律一样展开为四项：$Cov(A,C) + Cov(A,D) + Cov(B,C) + Cov(B,D)$。这是推导 MA ACF 的核心技巧。

---

### 4. 用直觉语言解释它

**生活类比：石头投入池塘的涟漪**

想象你把一块石头扔进平静的池塘：
- 石头入水的那一刻（$t$）产生最大的波纹——这就是 $\varepsilon_t$
- 波纹向外扩散，下一时刻（$t+1$）水面还在振动——这就是 $\theta \varepsilon_t$ 的影响
- 再下一时刻（$t+2$），振动更弱——更高阶的影响
- 最终水面恢复平静

MA 模型描述的就是这种"涟漪效应"：
- **当前冲击**（石头入水）直接影响当前值
- **过去冲击的残留**（扩散的波纹）继续影响当前值
- 超过 $q$ 期后，影响完全消失（水面平静）

**关键直觉：**

> MA 模型不是说"昨天股价高所以今天也高"，而是说"昨天有个意外利好，所以今天股价还受其余波影响"。

**一句话总结直觉本质：**

> MA 模型捕捉的是"意外的涟漪"——随机冲击不会只影响当期，而是会在有限期内持续传递。

---

### 5. 正式定义、核心公式、符号解释

#### 5.1 核心定义

**MA(q) 模型**（q 阶移动平均模型）：

$$X_t = \mu + \varepsilon_t + \theta_1 \varepsilon_{t-1} + \theta_2 \varepsilon_{t-2} + \cdots + \theta_q \varepsilon_{t-q}$$

**MA(1) 模型**（最简单也最重要）：

$$X_t = \mu + \varepsilon_t + \theta \varepsilon_{t-1}$$

#### 5.2 核心公式汇总

| 公式 | 含义 |
|------|------|
| $E(X_t) = \mu$ | MA 的均值就是参数 $\mu$（直接等于） |
| $Var(X_t) = \sigma^2(1 + \theta^2)$ | MA(1) 的方差 |
| $\rho_1 = \frac{\theta}{1+\theta^2}$ | MA(1) 的一阶自相关系数 |
| $\rho_k = 0, \quad k > q$ | MA(q) 的 ACF 在 q 阶后截尾 |

#### 5.3 可逆性条件

**MA(1) 可逆条件：** $|\theta| < 1$

**MA(q) 可逆条件：** 特征方程 $1 + \theta_1 z + \theta_2 z^2 + \cdots + \theta_q z^q = 0$ 的所有根在单位圆外。

#### 5.4 符号说明表

| 符号 | 含义 | 取值范围/量纲 | 备注 |
|------|------|--------------|------|
| $X_t$ | 时刻 $t$ 的序列值 | 实数 | 被建模的随机变量 |
| $\mu$ | 序列长期均值 | 实数 | MA 中直接就是均值（与 AR 不同） |
| $\varepsilon_t$ | 时刻 $t$ 的随机冲击 | 白噪声 | 不可直接观测 |
| $\theta$ | 移动平均系数 | MA(1): 可逆要求 $\|\theta\|<1$ | 决定过去冲击的残留强度 |
| $q$ | MA 阶数 | 正整数 | 冲击影响持续的期数 |
| $\sigma^2$ | 白噪声方差 | 正数 | 冲击的强度 |

---

### 6. 推导思路和思想来源

#### 6.1 MA(1) 方差的推导

**我们想解决什么？** MA(1) 的波动幅度由什么决定。

**推导：**

令 $Y_t = X_t - \mu = \varepsilon_t + \theta \varepsilon_{t-1}$

$$Var(Y_t) = Var(\varepsilon_t + \theta \varepsilon_{t-1}) = Var(\varepsilon_t) + \theta^2 Var(\varepsilon_{t-1}) + 2\theta Cov(\varepsilon_t, \varepsilon_{t-1})$$

由于白噪声不相关，$Cov(\varepsilon_t, \varepsilon_{t-1}) = 0$，且 $Var(\varepsilon_t) = Var(\varepsilon_{t-1}) = \sigma^2$：

$$Var(X_t) = \sigma^2(1 + \theta^2)$$

**关键转念：** 方差由"当前冲击"和"过去冲击残留"共同贡献。

#### 6.2 MA(1) ACF 的推导

**核心技巧：** 协方差的双线性展开。

$Y_t = \varepsilon_t + \theta \varepsilon_{t-1}$，$Y_{t-1} = \varepsilon_{t-1} + \theta \varepsilon_{t-2}$

$$\gamma_1 = Cov(Y_t, Y_{t-1}) = Cov(\varepsilon_t + \theta \varepsilon_{t-1}, \varepsilon_{t-1} + \theta \varepsilon_{t-2})$$

展开四项，只有 $Cov(\theta \varepsilon_{t-1}, \varepsilon_{t-1}) = \theta \sigma^2$ 非零：

$$\gamma_1 = \theta \sigma^2, \quad \gamma_0 = \sigma^2(1+\theta^2)$$

$$\rho_1 = \frac{\theta}{1+\theta^2}, \quad \rho_k = 0 \text{ for } k > 1$$

**思想来源：** MA 的本质是有限个白噪声的线性组合，相隔超过 $q$ 期的两项没有共同的冲击项，因此协方差为零。

#### 6.3 可逆性问题的来源

**核心问题：** 不同的 $\theta$ 可能产生相同的 ACF。

例如 $\theta = 2$ 和 $\theta = 0.5$：
- $\theta = 2$: $\rho_1 = \frac{2}{1+4} = 0.4$
- $\theta = 0.5$: $\rho_1 = \frac{0.5}{1+0.25} = 0.4$

**解决方案：** 要求 $|\theta| < 1$，在 $\theta$ 和 $1/\theta$ 中总是选绝对值小的那个，保证模型唯一可识别。

---

### 7. 例子：基础 → 中等 → 实际应用

#### 例子 1：基础例子（手工可算）

**题目：** 考虑 MA(1) 模型 $X_t = 10 + \varepsilon_t + 0.5 \varepsilon_{t-1}$，其中 $\sigma^2 = 4$。

(1) 求序列的均值；
(2) 求序列的方差；
(3) 求一阶自相关系数 $\rho_1$；
(4) 求 $\rho_2$。

**解题思路：** 直接套用核心公式。

**关键步骤：**

(1) 均值：$E(X_t) = \mu = 10$（MA 的均值直接就是 $\mu$）

(2) 方差：$Var(X_t) = \sigma^2(1+\theta^2) = 4 \times (1+0.25) = 4 \times 1.25 = 5$

(3) 一阶自相关：$\rho_1 = \frac{\theta}{1+\theta^2} = \frac{0.5}{1.25} = 0.4$

(4) $\rho_2 = 0$（MA(1) 的 ACF 在 1 阶后截尾）

**容易错的地方：** 把 MA 当成 AR，试图用 $\rho_k = \phi^k$ 的公式。

**追问：** 如果 $\theta = 2$（不满足可逆性），$\rho_1$ 是多少？

> 答：$\rho_1 = \frac{2}{1+4} = 0.4$，和 $\theta=0.5$ 一样！这就是可逆性问题。

#### 例子 2：中等例子（需要判断条件）

**题目：** 某平稳序列的 ACF 值如下：

| 滞后阶数 $k$ | 1 | 2 | 3 | 4 | 5 |
|-------------|---|---|---|---|---|
| ACF | 0.48 | 0.31 | 0.02 | -0.01 | 0.03 |
| PACF | 0.48 | 0.25 | 0.15 | 0.10 | 0.08 |

请判断这可能是什么模型？并估计参数。

**解答：**

(1) **模型判断：** ACF 在 2 阶后截尾（3 阶及以后接近 0），PACF 拖尾，符合 **MA(2)** 的特征。

(2) **参数估计：** 
- 由 MA(2) 的 ACF 公式，$\rho_1$ 和 $\rho_2$ 非零，$\rho_k=0$（$k>2$）
- 需要用数值方法（如解方程组或 MLE）估计 $\theta_1, \theta_2$
- 粗略判断：$q=2$

(3) **可逆性检验：** 估计后需要验证特征方程的根是否都在单位圆外。

#### 例子 3：实际应用例子

**场景：股市收益率的短期冲击**

假设某股票日收益率服从 MA(1) 过程：

$$r_t = \mu + \varepsilon_t + \theta \varepsilon_{t-1}$$

实证估计得到：
- $\hat{\mu} = 0.02\%$（日均收益率）
- $\hat{\theta} = 0.3$
- $\hat{\sigma}^2 = 4$

**解释：**
- 今天发生一个正向冲击（好消息），不仅今天股价涨，明天还会因为今天的冲击残留再涨一点（$0.3$ 倍的冲击）
- 后天起这个冲击就完全消失了（MA(1) 的 ACF 在 1 阶后截尾）
- 方差 = $4 \times (1+0.09) = 4.36$，比纯白噪声的方差 4 稍大

**实际价值：**
- 理解市场冲击的持续时间
- 量化意外事件对股价的短期影响
- 为高频交易策略提供模型基础

---

### 8. 常见误区和易混概念

#### 误区 1：把 MA 模型当成"移动平均线"

**错误直觉：** 技术分析里的移动平均线 MA 就是时间序列的 MA 模型。

**为什么错：** 技术分析的 MA 是对过去**观测值**取平均：$MA_t = \frac{X_t + X_{t-1} + \cdots}{k+1}$。时间序列的 MA 模型用的是过去**冲击项**：$X_t = \mu + \varepsilon_t + \theta \varepsilon_{t-1}$。两者完全不同！

**正确理解：** MA 模型 = 过去随机冲击的加权平均，不是过去观测值的平均。

#### 误区 2：认为 MA 和 AR 是完全独立的两种模型

**错误直觉：** AR 和 MA 毫不相干。

**为什么错：** 在满足可逆性条件下，MA(q) 可以写成无限阶 AR 形式（AR($\infty$)），反之 AR(p) 也可以写成无限阶 MA 形式。

**正确理解：** AR 和 MA 是同一枚硬币的两面，Wold 分解定理告诉我们任何平稳序列都可以表示为 MA($\infty$)。

#### 误区 3：忽略可逆性条件

**错误直觉：** MA 模型天然平稳，不需要额外条件。

**为什么错：** 虽然有限阶 MA 天然平稳，但可逆性是为了保证模型可以被唯一识别。没有可逆性，多个参数组合会产生相同的 ACF，模型不唯一。

**正确理解：** 平稳性 ≠ 可逆性。MA 总是平稳的，但不一定可逆。建模时通常要求可逆。

#### 误区 4：认为 MA 的参数可以用 OLS 直接估计

**错误直觉：** 像 AR 一样做回归就行。

**为什么错：** MA 模型中的 $\varepsilon_{t-1}, \varepsilon_{t-2}, \ldots$ 是不可观测的！AR 的右边是观测值 $X_{t-1}$，可以用 OLS；MA 的右边是冲击项，需要用 MLE 或条件 MLE。

**正确理解：** MA 估计比 AR 难，因为涉及不可观测变量的迭代估计。

---

### 9. 相关知识点与 Obsidian 双链建议

#### 上游依赖

- [[白噪声|白噪声]]：MA 的"原材料"就是白噪声，不理解白噪声就无法理解 MA
- [[自相关函数ACF|自相关函数ACF]]：MA 的 ACF 截尾特征是识别的核心依据
- [[平稳性|平稳性]]：MA 天然平稳，是理解"为什么 MA 不需要平稳条件"的对比基准

#### 下游延伸

- [[ARMA模型|ARMA模型]]：AR 和 MA 的结合体
- [[ARIMA模型]]：差分 + ARMA
- [[L07-模型识别与参数估计|AIC与BIC]]：用于 MA 定阶的信息准则

#### 横向关联

- [[AR模型|AR模型]] ↔ MA模型：AR 的 ACF 拖尾/PACF 截尾，MA 的 ACF 截尾/PACF 拖尾，形成完美对偶
- [[参数估计|参数估计]] ↔ MA模型：MA 的参数估计不能用 OLS，必须用 MLE

#### 应用场景

- **波动率建模（应用场景）**：GARCH 的均值方程或创新表示可能涉及 MA 思想
- **收益率预测（应用场景）**：短期冲击的传递建模

---

### 10. 闭卷复现任务

看完笔记后，合上笔记，尝试独立回答：

1. **一句话问题：** MA 模型解决什么问题？（冲击的有限期传递）
2. **直觉解释：** 用生活类比说明 MA 模型。（石头入水的涟漪）
3. **正式定义：** 写出 MA(1) 和 MA(q) 的公式。
4. **核心公式：** 写出 MA(1) 的均值、方差、$\rho_1$ 公式。
5. **符号解释：** $\mu, \theta, q, \varepsilon_t$ 各代表什么？
6. **推导主线：** 如何推导 MA(1) 的 ACF？（双线性展开 + 白噪声不相关）
7. **基础例子：** 给定 $X_t = 5 + \varepsilon_t + 0.4 \varepsilon_{t-1}$，$\sigma^2=1$，求均值、方差、$\rho_1$。
8. **两个误区：** (1) MA ≠ 移动平均线；(2) MA 天然平稳但不一定可逆。
9. **三个关系：** MA 与 AR 的对偶关系？MA 与 ARMA 的关系？MA 与可逆性的关系？
10. **应用场景：** 举一个 MA 的实际应用。（股市冲击传递）

---

### 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
|------|------|------|--------|
| 1 | 概念辨析 | 基础 | MA 的核心思想 |
| 2 | 公式运用 | 基础 | 均值、方差、ACF 计算 |
| 3 | 条件判断 | 中等 | 可逆性条件 |
| 4 | 变式/综合 | 中等 | ACF/PACF 识别 |
| 5 | 开放/证明 | 较难 | MA(1) 的 ACF 推导 |

#### 题1

**题目：** 以下哪个选项最准确地描述了 MA(1) 模型的核心思想？

A. 当前值由过去观测值的加权平均决定
B. 当前值由当前冲击和过去冲击共同决定
C. 当前值只由当前冲击决定
D. 当前值由长期趋势和季节成分决定

> [!question]- 答案解析
> **答案：B**
> 
> **解析：** MA(1) $X_t = \mu + \varepsilon_t + \theta \varepsilon_{t-1}$ 的核心是"当前值由当前冲击 $\varepsilon_t$ 和上一期冲击 $\varepsilon_{t-1}$ 共同决定"。
> 
> A 描述的是 AR 模型或技术分析的移动平均线；C 描述的是白噪声；D 描述的是带趋势和季节性的模型。
> 
> **最可能做错的原因：** 混淆 MA 与"移动平均线"的概念。
> 
> **对应误区：** 误区 1（MA ≠ 移动平均线）。
> 
> **Obsidian 标签：** #自测/MA基础概念

#### 题2

**题目：** 对于 MA(1) 模型 $X_t = 8 + \varepsilon_t + 0.6 \varepsilon_{t-1}$，已知 $\sigma^2 = 9$，求：
(1) 序列均值；(2) 序列方差；(3) 一阶自相关系数 $\rho_1$。

> [!question]- 答案解析
> **答案：**
> (1) $\mu = 8$（MA 的均值直接就是 $\mu$）
> 
> (2) $Var(X_t) = \sigma^2(1+\theta^2) = 9 \times (1+0.36) = 9 \times 1.36 = 12.24$
> 
> (3) $\rho_1 = \frac{\theta}{1+\theta^2} = \frac{0.6}{1.36} \approx 0.441$
> 
> **解析：** 直接套用 MA(1) 的核心公式。
> 
> **最可能做错的原因：** 
> - 误用 AR 的均值公式 $\frac{c}{1-\phi}$
> - 计算 $\rho_1$ 时忘记分母是 $1+\theta^2$
> 
> **对应误区：** 混淆 AR 和 MA 的公式。
> 
> **Obsidian 标签：** #自测/公式计算

#### 题3

**题目：** 以下哪个 MA(1) 模型是可逆的？

A. $X_t = \varepsilon_t + 2 \varepsilon_{t-1}$
B. $X_t = \varepsilon_t - 0.8 \varepsilon_{t-1}$
C. $X_t = \varepsilon_t + 1.0 \varepsilon_{t-1}$
D. $X_t = \varepsilon_t + 1.5 \varepsilon_{t-1}$

> [!question]- 答案解析
> **答案：B**
> 
> **解析：** MA(1) 的可逆条件是 $|\theta| < 1$。
> - A: $\theta = 2$，$|2| > 1$，不可逆
> - B: $\theta = -0.8$，$|-0.8| = 0.8 < 1$，可逆
> - C: $\theta = 1.0$，$|1.0| = 1$，边界情况，通常认为不可逆
> - D: $\theta = 1.5$，$|1.5| > 1$，不可逆
> 
> **最可能做错的原因：** 忽略绝对值，认为负系数就不可逆。
> 
> **对应误区：** 误区 3（忽略可逆性）。
> 
> **Obsidian 标签：** #自测/可逆性判断

#### 题4

**题目：** 某序列的 ACF 和 PACF 如下：

| 滞后 | 1 | 2 | 3 | 4 | 5 |
|------|---|---|---|---|---|
| ACF | 0.55 | 0.02 | -0.03 | 0.01 | -0.02 |
| PACF | 0.55 | 0.35 | 0.20 | 0.12 | 0.08 |

请判断适合用什么模型？

> [!question]- 答案解析
> **答案：MA(1)**。
> 
> **解析：**
> - ACF 在 1 阶后截尾（2 阶及以后接近 0）
> - PACF 拖尾（逐渐衰减）
> - 符合 MA(q) 的识别规律：ACF 在 q 阶截尾，PACF 拖尾
> - 这里 $q=1$
> 
> **最可能做错的原因：** 和 AR(1) 搞混（AR(1) 是 ACF 拖尾、PACF 截尾，正好相反）。
> 
> **对应误区：** AR 和 MA 的 ACF/PACF 特征记反了。
> 
> **Obsidian 标签：** #自测/模型识别

#### 题5

**题目：** 证明：对于 MA(1) 模型 $X_t = \mu + \varepsilon_t + \theta \varepsilon_{t-1}$，有 $\rho_1 = \frac{\theta}{1+\theta^2}$，且 $\rho_k = 0$（$k > 1$）。

> [!question]- 答案解析
> **证明：**
> 
> **Step 1：** 令 $Y_t = X_t - \mu = \varepsilon_t + \theta \varepsilon_{t-1}$，则：
> $$\gamma_0 = Var(Y_t) = Var(\varepsilon_t) + \theta^2 Var(\varepsilon_{t-1}) = \sigma^2(1+\theta^2)$$
> （利用了 $Cov(\varepsilon_t, \varepsilon_{t-1}) = 0$）
> 
> **Step 2：** 计算一阶自协方差：
> $$Y_{t-1} = \varepsilon_{t-1} + \theta \varepsilon_{t-2}$$
> $$\gamma_1 = Cov(Y_t, Y_{t-1}) = Cov(\varepsilon_t + \theta \varepsilon_{t-1}, \varepsilon_{t-1} + \theta \varepsilon_{t-2})$$
> 
> 展开四项，由白噪声不相关性质，只有 $Cov(\theta \varepsilon_{t-1}, \varepsilon_{t-1}) = \theta \sigma^2$ 非零。
> 
> 所以 $\gamma_1 = \theta \sigma^2$。
> 
> **Step 3：** 计算 $\rho_1$：
> $$\rho_1 = \frac{\gamma_1}{\gamma_0} = \frac{\theta \sigma^2}{\sigma^2(1+\theta^2)} = \frac{\theta}{1+\theta^2}$$
> 
> **Step 4：** 对于 $k > 1$，$Y_t$ 和 $Y_{t-k}$ 没有共同的 $\varepsilon$ 项，因此 $\gamma_k = 0$，$\rho_k = 0$。
> 
> **解析：** 核心是白噪声的不相关性和协方差的双线性展开。
> 
> **最可能做错的原因：** 展开协方差时遗漏项，或者错误地认为 $Cov(\varepsilon_t, \varepsilon_{t-1}) \neq 0$。
> 
> **Obsidian 标签：** #自测/推导证明

---

### 12. 我的主动回忆区

#### 我的闭卷复述

> 不看上文，用自己的话解释 MA 模型：
> 
> 

#### 我的推导复现

> 不看上文，尝试写出以下公式：
> - MA(1) 模型方程：
> - MA(1) 的均值：
> - MA(1) 的方差：
> - MA(1) 的 ACF：
> 
> 

#### 我的错误与卡点

- 
- 
- 

#### 下次复习日期

- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

### 13. 给 Obsidian 的归档建议

- **归属：** 本卡已归档为对应主卡的深挖支线（经主卡内部导航进入）
- **应链接的已有笔记：** 白噪声、ACF、AR 模型、ARMA 模型
- **建议标签：** #时间序列 #MA模型 #移动平均 #经典模型层
- **是否需要拆分：**
  - 当前笔记已整合概念与基础推导
  - 若需更深入，可拆出「MA可逆性详解」专门讨论滞后算子形式和特征方程
  - 可另建「MA与AR对比笔记」用表格总结两者在定义、ACF/PACF、估计方法上的对偶性
-

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


