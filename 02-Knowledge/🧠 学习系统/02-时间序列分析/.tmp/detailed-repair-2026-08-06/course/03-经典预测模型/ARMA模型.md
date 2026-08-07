---
type: study
topic: "ARMA模型"
created: 2026-04-18
updated: 2026-08-02
status: completed
difficulty: intermediate
concept: ["ARMA", "自回归", "移动平均"]
prerequisites: ["平稳时间序列", "白噪声", "自相关函数ACF"]
related: ["ARIMA模型", "AR模型", "MA模型"]
tags: [学习, 时间序列, ARMA]
flow: knowledge
kind: derivation
sources:
  - title: "Forecasting: Principles and Practice (3e)"
    url: "https://otexts.com/fpp3/arima.html"
    locator: "Chapter 9, Sections 9.2-9.4: backshift notation, AR and MA models"
    source_type: "official-free-textbook"
    license: "official-free online"
    verified_at: 2026-08-02
course: "时间序列分析"
stage_moc: "[[🧭 阶段3-经典预测模型]]"
upstream: ["[[MA模型]]"]
---
# ARMA 模型

ARMA$(p,q)$ 用过去观测值的线性组合与过去创新项的线性组合描述平稳时间序列。AR 部分提供递归记忆，MA 部分描述冲击在有限滞后内的传播。

## 1. 模型定义

对均值已处理的序列 $y_t$：

$$
y_t=\phi_1y_{t-1}+\cdots+\phi_py_{t-p}
+\varepsilon_t+\theta_1\varepsilon_{t-1}+\cdots+\theta_q\varepsilon_{t-q},
$$

其中 $\varepsilon_t$ 是方差为 $\sigma^2$ 的[[白噪声]]。用滞后算子 $B$ 可写为

$$
\phi(B)y_t=\theta(B)\varepsilon_t,
$$

$$
\phi(B)=1-\sum_{i=1}^p\phi_iB^i,
\qquad
\theta(B)=1+\sum_{j=1}^q\theta_jB^j.
$$

MA 多项式的正负号在不同软件和教材中可能不同，解释参数前必须确认约定。

## 2. 平稳性与可逆性

AR 多项式 $\phi(z)=0$ 的根都在单位圆外，是因果平稳 ARMA 的常用条件。MA 多项式 $\theta(z)=0$ 的根都在单位圆外，对应可逆性，使创新项可由当前和过去观测唯一表示。

若原序列需要差分才能平稳，应使用[[ARIMA模型|ARIMA$(p,d,q)$]]，而不是直接对非平稳水平序列套 ARMA。

## 3. ACF/PACF 识别只是候选生成

- 纯 AR$(p)$：PACF 理论上在 $p$ 阶后截尾，ACF 拖尾。
- 纯 MA$(q)$：ACF 理论上在 $q$ 阶后截尾，PACF 拖尾。
- ARMA：ACF 与 PACF 通常都拖尾。

有限样本、接近相消的 AR/MA 参数和异常值都会模糊这些模式。因此应结合[[自相关函数ACF|ACF]]、信息准则、残差诊断和时间外验证，而不是只凭图形定阶。

## 4. 最小模拟与拟合

```python
import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.arima.model import ARIMA

rng = np.random.default_rng(5)
process = ArmaProcess(ar=[1, -0.6], ma=[1, 0.3])
y = process.generate_sample(600, distrvs=rng.normal)
fit = ARIMA(y, order=(1, 0, 1), trend="n").fit()

assert fit.nobs == 600
assert np.isfinite(fit.aic)
```

一次拟合得到有限 AIC 不等于模型正确。还需检查残差 ACF、Ljung–Box 检验、参数稳定性以及留出区间预测误差。

## 5. 一步预测直觉

对 ARMA$(1,1)$：

$$
y_t=\phi y_{t-1}+\varepsilon_t+\theta\varepsilon_{t-1}.
$$

在时刻 $t$ 已知信息下，一步预测为

$$
\hat y_{t+1|t}=\phi y_t+\theta\hat\varepsilon_t,
$$

因为未来创新 $\varepsilon_{t+1}$ 的条件期望为零。多步预测时，未知未来创新都置为零并递归代入预测值。

## 6. 边界与误区

1. ARMA 主要描述线性条件均值相关，不能自动处理波动聚集和结构突变。
2. 阶数越高不一定越好；高阶模型更易过拟合且参数难解释。
3. 残差通过白噪声检验只是必要诊断之一，不证明模型为真实生成机制。
4. 同一序列可能有多个近似等价模型，应比较预测性能与简洁性。
5. 季节性需要显式季节结构或预处理，不能只靠增加普通滞后阶数。

## 🌐 开放教材定位

> 以下条目是本卡的知识主线与定位依据；算法 API 和软件文档只作实现对照。

- [Forecasting: Principles and Practice (3e)](https://otexts.com/fpp3/arima.html) — `Chapter 9, Sections 9.2-9.4: backshift notation, AR and MA models`；官方免费访问，不推定再分发权。

引用时继续保留 `locator`，不把教材首页或搜索摘要当作具体论据。

## 参考资料

- Hyndman & Athanasopoulos, *Forecasting: Principles and Practice*, Chapter 9：https://otexts.com/fpp3/arima.html
- statsmodels, `ARIMA` 官方文档：https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMA.html

## 🔬 深挖推导与自测

> 本节由原“ARMA模型（深挖笔记）”合并而来，保留完整推导、例题和闭卷自测。

> 主卡：[[ARMA模型]]｜本卡为深挖细节版，主线索引请走主卡。

### 0. 学习边界

**结论：A 类知识点，必须深挖。**

**理由：**
ARMA 是经典时间序列建模的核心框架，Box-Jenkins 方法的基石。它统一了 AR 和 MA 两种机制，几乎覆盖了所有平稳时间序列的建模需求。不理解 ARMA，就无法理解 ARIMA（差分后的 ARMA），也无法理解更复杂的 SARIMA、GARCH 等扩展模型。在实际建模和考试中，ARMA 的地位不可替代。

---

### 1. 这个知识点解决什么问题？

**我们遇到了什么麻烦？**

现实中很多时间序列同时表现出两种特征：
1. **惯性/记忆**：当前值与过去的观测值有关（AR 特征）
2. **冲击传递**：当前值受过去意外的影响（MA 特征）

**只用 AR 的问题：**
- 有些序列的 ACF 和 PACF 都拖尾，说明不是纯 AR
- 强行用高阶 AR 拟合，参数多、过拟合风险大

**只用 MA 的问题：**
- 有些序列有长期记忆，MA 需要极高阶才能近似
- 高阶 MA 参数多，估计困难

**为什么必须引入 ARMA？**

ARMA 把两种机制结合起来：
- 用 **AR(p)** 捕捉序列的"记忆"
- 用 **MA(q)** 捕捉冲击的"涟漪"
- 用少量的 $p+q$ 个参数，描述复杂的自相关结构

> **核心直觉：** ARMA 回答的问题是——如果一个序列已经没有趋势和季节性，它的波动能不能用"过去的自己"和"过去的意外"共同解释？

---

### 2. 为什么它重要？它有什么用？

**不学它，后续哪些知识会看不懂？**
- ARIMA 模型 = 差分 + ARMA，ARMA 是核心
- SARIMA 模型 = 季节性扩展的 ARIMA
- GARCH 模型的均值方程常用 ARMA 形式
- 所有基于 Box-Jenkins 框架的建模方法

**它在本课程中处于什么位置？**
- 板块C：经典模型层的**核心**
- AR 和 MA 是其组成部分
- ARIMA 是其非平稳版本

**实际应用场景：**
- **宏观经济建模**：GDP 增速、通胀率、失业率（差分后）
- **金融收益率**：股票、债券、汇率的日收益率
- **气象数据**：温度偏离值、降水量异常
- **工业质量**：生产过程中的波动控制

**考试中最常出现的题型：**
- 根据 ACF/PACF 判断 ARMA 阶数
- 平稳性和可逆性条件
- ARMA 的滞后算子表示
- 信息准则（AIC/BIC）选阶

---

### 3. 学它之前需要哪些前置知识？

| 前置知识 | 用途 | 是否需要补课 |
|---------|------|------------|
| AR 模型 | ARMA 的 AR 部分 | 必须掌握 |
| MA 模型 | ARMA 的 MA 部分 | 必须掌握 |
| 平稳性 | ARMA 要求序列平稳 | 必须掌握 |
| 可逆性 | MA 部分的要求 | 简要了解 |
| 滞后算子 | ARMA 的紧凑表示 | 建议掌握 |
| ACF/PACF | 模型识别 | 必须掌握 |

**最小必要背景补充（若缺）：**

> **滞后算子 $B$：** 定义 $B X_t = X_{t-1}$，$B^k X_t = X_{t-k}$。它就像一个"时间倒退"的开关。ARMA 用滞后算子表示非常简洁：$\phi(B) X_t = c + \theta(B) \varepsilon_t$。

---

### 4. 用直觉语言解释它

**生活类比：开车经过减速带**

想象你开车经过一段颠簸的路：
- **AR 部分** = 车子的悬挂系统（记忆效应）：车身弹起后不会立刻落地，而是会振荡几下
- **MA 部分** = 路面上的减速带（冲击效应）：每个减速带都是一个突发冲击，影响车身的即时反应
- **ARMA** = 车子在颠簸路面上的综合运动：既受悬挂系统惯性影响（AR），又受每个减速带冲击影响（MA）

**更直观的例子：气温**
- 今天温度高，明天大概率也高 → **AR 效应**
- 但昨晚突然来了一股冷锋（意外冲击），今天温度被压低 → **MA 效应**
- 实际温度 = 昨天温度的延续 + 冷锋冲击的残留

**一句话总结直觉本质：**

> ARMA 模型描述的是一个"有记忆的系统"在"持续受到意外冲击"时的动态行为——既记住过去，又受意外扰动。

---

### 5. 正式定义、核心公式、符号解释

#### 5.1 核心定义

**ARMA(p,q) 模型**：

$$X_t = c + \phi_1 X_{t-1} + \cdots + \phi_p X_{t-p} + \varepsilon_t + \theta_1 \varepsilon_{t-1} + \cdots + \theta_q \varepsilon_{t-q}$$

或紧凑形式：

$$X_t = c + \sum_{i=1}^{p} \phi_i X_{t-i} + \varepsilon_t + \sum_{j=1}^{q} \theta_j \varepsilon_{t-j}$$

#### 5.2 滞后算子表示

定义滞后算子多项式：
- AR 多项式：$\phi(B) = 1 - \phi_1 B - \phi_2 B^2 - \cdots - \phi_p B^p$
- MA 多项式：$\theta(B) = 1 + \theta_1 B + \theta_2 B^2 + \cdots + \theta_q B^q$

ARMA(p,q) 可写为：

$$\phi(B) X_t = c + \theta(B) \varepsilon_t$$

#### 5.3 平稳性和可逆性条件

| 条件 | 要求 | 检验方法 |
|------|------|---------|
| 平稳性 | $\phi(z) = 0$ 的所有根在单位圆外 | 看 AR 特征方程 |
| 可逆性 | $\theta(z) = 0$ 的所有根在单位圆外 | 看 MA 特征方程 |

#### 5.4 均值

若平稳，长期均值为：

$$\mu = \frac{c}{1 - \phi_1 - \phi_2 - \cdots - \phi_p} = \frac{c}{1 - \sum_{i=1}^{p} \phi_i}$$

#### 5.5 符号说明表

| 符号 | 含义 | 取值范围/量纲 | 备注 |
|------|------|--------------|------|
| $p$ | AR 阶数 | 正整数 | 自回归部分的滞后阶数 |
| $q$ | MA 阶数 | 正整数 | 移动平均部分的滞后阶数 |
| $\phi_i$ | 自回归系数 | 平稳性约束 | AR 部分的参数 |
| $\theta_j$ | 移动平均系数 | 可逆性约束 | MA 部分的参数 |
| $\phi(B)$ | AR 滞后多项式 | 多项式 | 用于判断平稳性 |
| $\theta(B)$ | MA 滞后多项式 | 多项式 | 用于判断可逆性 |
| $c$ | 常数项 | 实数 | 与均值的关系：$\mu = c / (1-\sum \phi_i)$ |

---

### 6. 推导思路和思想来源

#### 6.1 ARMA 的思想来源

**Wold 分解定理（1938）：**

> 任何弱平稳时间序列都可以表示为一个确定性成分加上一个 MA($\infty$) 过程。

这意味着：从理论上讲，纯 MA 模型足够描述任何平稳序列。但实际中：
- 无限阶 MA 无法估计
- 用有限阶 ARMA(p,q) 来近似 MA($\infty$) 更实用

#### 6.2 滞后算子表示的推导动机

**问题：** ARMA(p,q) 写起来很长，平稳性和可逆性条件也不容易看。

**转念：** 用多项式表示滞后算子！

$$\phi(B) = 1 - \phi_1 B - \cdots - \phi_p B^p$$

把 $B$ 当成一个"形式变量"，那么 $\phi(B) X_t$ 就自动展开了：

$$(1 - \phi_1 B - \cdots - \phi_p B^p) X_t = X_t - \phi_1 X_{t-1} - \cdots - \phi_p X_{t-p}$$

**关键洞见：** 平稳性条件变成了"多项式 $\phi(z)$ 的根都在单位圆外"——这是复分析中的经典问题，有成熟的判定方法。

#### 6.3 ARMA 的 ACF 为什么都拖尾？

**直觉：** 
- AR(p) 的 ACF 拖尾（因为 $\phi^k$ 衰减）
- MA(q) 的 ACF 截尾
- ARMA(p,q) = AR(p) + MA(q) → ACF 是两者的"混合"

由于 AR 部分的存在，即使 MA 部分的 ACF 会截尾，AR 部分的记忆效应会让整体 ACF 持续衰减。因此 ARMA 的 ACF 和 PACF **都拖尾**。

---

### 7. 例子：基础 → 中等 → 实际应用

#### 例子 1：基础例子（手工可算）

**题目：** 考虑 ARMA(1,1) 模型：
$$X_t = 2 + 0.6 X_{t-1} + \varepsilon_t + 0.3 \varepsilon_{t-1}$$

(1) 判断平稳性和可逆性；
(2) 求长期均值。

**解题思路：** 分别检验 AR 和 MA 部分的条件。

**关键步骤：**

(1) **平稳性：** AR 部分系数 $\phi = 0.6$，$|\phi| = 0.6 < 1$，平稳。

**可逆性：** MA 部分系数 $\theta = 0.3$，$|\theta| = 0.3 < 1$，可逆。

(2) **长期均值：**
$$\mu = \frac{c}{1-\phi} = \frac{2}{1-0.6} = \frac{2}{0.4} = 5$$

**容易错的地方：** 混淆平稳性（看 AR）和可逆性（看 MA）的条件。

**追问：** 如果模型变成 $X_t = 2 + 1.2 X_{t-1} + \varepsilon_t + 0.3 \varepsilon_{t-1}$，还能用吗？

> 答：不能直接用。AR 部分不平稳，需要先差分，变成 ARIMA 模型。

#### 例子 2：中等例子（需要判断条件）

**题目：** 某平稳序列的 ACF 和 PACF 如下：

| 滞后 | 1 | 2 | 3 | 4 | 5 | 6 |
|------|---|---|---|---|---|---|
| ACF | 0.65 | 0.42 | 0.28 | 0.18 | 0.12 | 0.08 |
| PACF | 0.65 | 0.18 | 0.10 | 0.05 | 0.03 | 0.02 |

请判断适合的模型。

**解答：**

(1) **ACF 分析：** 从 0.65 逐渐衰减到 0.08，呈拖尾特征。

(2) **PACF 分析：** 从 0.65 下降，但也在缓慢衰减，不是突然截尾。

(3) **判断：** ACF 拖尾 + PACF 拖尾 → **ARMA(p,q)**。

(4) **定阶：** 需要尝试不同的 $(p,q)$ 组合，用 AIC/BIC 选择。例如尝试 ARMA(1,1)、ARMA(1,2)、ARMA(2,1) 等。

#### 例子 3：实际应用例子

**场景：股票日收益率建模**

某股票日收益率序列经检验平稳，ACF 和 PACF 都呈现拖尾特征。尝试建立 ARMA 模型。

**建模过程：**
1. 用 `auto_arima` 或网格搜索遍历 $(p,q)$ 组合
2. 候选模型：ARMA(1,1), ARMA(2,1), ARMA(1,2)
3. 比较 AIC/BIC，选择最小者
4. 假设最终选定 ARMA(1,1)：

$$r_t = 0.001 + 0.12 r_{t-1} + \varepsilon_t + 0.08 \varepsilon_{t-1}$$

**实际价值：**
- $\phi = 0.12$：收益率有微弱的正向惯性
- $\theta = 0.08$：昨天的冲击对今天有微小残留影响
- 模型可用于短期预测（1-5 天）
- 残差诊断：若通过 Ljung-Box 检验，说明模型充分提取了自相关结构

---

### 8. 常见误区和易混概念

#### 误区 1：ARMA 的 ACF 和 PACF 能直接定阶

**错误直觉：** 像 AR 和 MA 一样，看图就能确定 $p$ 和 $q$。

**为什么错：** ARMA(p,q) 的 ACF 和 PACF 都拖尾，无法直接从图中读出 $p$ 和 $q$。

**正确理解：** ARMA 定阶需要结合信息准则（AIC/BIC）和残差诊断，ACF/PACF 只能判断"是不是 ARMA"，不能确定具体阶数。

#### 误区 2：平稳性和可逆性检验混淆

**错误直觉：** 检验了平稳性就不用管可逆性，或者反之。

**为什么错：** 平稳性是针对 AR 部分的（确保序列不爆炸），可逆性是针对 MA 部分的（确保模型唯一）。两者独立，都需要检验。

**正确理解：** 
- AR 系数 → 平稳性
- MA 系数 → 可逆性
- 两者都要满足

#### 误区 3：$p$ 和 $q$ 越大越好

**错误直觉：** 高阶 ARMA 能拟合更复杂的数据。

**为什么错：** 高阶模型参数多，容易过拟合。而且估计困难（MA 部分需要非线性优化）。

**正确理解：** 实践中 $p, q$ 通常不超过 2 或 3，用信息准则惩罚复杂度。

#### 误区 4：ARMA 可以处理有趋势的序列

**错误直觉：** ARMA 是万能模型，什么序列都能拟合。

**为什么错：** ARMA 要求序列平稳。有趋势或季节性的序列需要先差分或分解。

**正确理解：** 非平稳序列 → 差分 → ARIMA；有季节性 → SARIMA。

---

### 9. 相关知识点与 Obsidian 双链建议

#### 上游依赖

- [[AR模型|AR模型]]：ARMA 的 AR 部分，必须完全理解
- [[MA模型|MA模型]]：ARMA 的 MA 部分，必须完全理解
- [[平稳性|平稳性]]：ARMA 建模的前提条件

#### 下游延伸

- [[ARIMA模型]]：非平稳序列通过差分后用 ARMA
- [[SARIMA模型|SARIMA模型]]：带季节性的 ARIMA
- [[L07-模型识别与参数估计|AIC与BIC]]：ARMA 定阶的核心工具
- [[参数估计|参数估计]]：ARMA 的 MLE 估计方法

#### 横向关联

- [[模型识别|模型识别]] ↔ ARMA：ACF/PACF 都拖尾时判断为 ARMA
- [[残差诊断与白噪声检验|残差诊断]] ↔ ARMA：Ljung-Box 检验验证模型充分性

#### 应用场景

- **收益率预测（应用场景）**：金融资产日收益率的经典建模
- **宏观经济预测（应用场景）**：GDP、通胀等指标的短期预测

---

### 10. 闭卷复现任务

看完笔记后，合上笔记，尝试独立回答：

1. **一句话问题：** ARMA 解决什么问题？（同时有记忆效应和冲击传递的平稳序列）
2. **直觉解释：** 用类比说明 ARMA。（车子在颠簸路面行驶）
3. **正式定义：** 写出 ARMA(p,q) 的公式和滞后算子形式。
4. **核心公式：** 平稳条件、可逆条件、长期均值公式。
5. **符号解释：** $\phi(B), \theta(B), p, q$ 各代表什么？
6. **推导主线：** 为什么 ARMA 的 ACF 和 PACF 都拖尾？
7. **基础例子：** 给定 $X_t = 1 + 0.5 X_{t-1} + \varepsilon_t + 0.2 \varepsilon_{t-1}$，判断平稳性、可逆性，求均值。
8. **两个误区：** (1) ARMA 不能直接从 ACF/PACF 定阶；(2) 平稳性 ≠ 可逆性。
9. **三个关系：** ARMA 与 AR 的关系？ARMA 与 MA 的关系？ARMA 与 ARIMA 的关系？
10. **应用场景：** 举一个 ARMA 的实际应用。（股票收益率建模）

---

### 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
|------|------|------|--------|
| 1 | 概念辨析 | 基础 | ARMA 的组成 |
| 2 | 公式运用 | 基础 | 滞后算子表示 |
| 3 | 条件判断 | 中等 | 平稳性和可逆性 |
| 4 | 变式/综合 | 中等 | ACF/PACF 识别 |
| 5 | 开放/证明 | 较难 | ARMA(1,1) 的 ACF 推导 |

#### 题1

**题目：** ARMA(p,q) 模型中的 $p$ 和 $q$ 分别代表什么？

A. $p$ = MA 阶数，$q$ = AR 阶数
B. $p$ = AR 阶数，$q$ = MA 阶数
C. $p$ = 差分阶数，$q$ = 季节阶数
D. $p$ = 样本量，$q$ = 参数个数

> [!question]- 答案解析
> **答案：B**
> 
> **解析：** ARMA(p,q) = AR(p) + MA(q)。$p$ 是自回归阶数（用多少个滞后 $X$），$q$ 是移动平均阶数（用多少个滞后 $\varepsilon$）。
> 
> **最可能做错的原因：** 把 $p$ 和 $q$ 记反了。
> 
> **对应误区：** 基本概念混淆。
> 
> **Obsidian 标签：** #自测/ARMA基础概念

#### 题2

**题目：** 将以下 ARMA(1,1) 模型写成滞后算子形式：
$$X_t = 3 + 0.7 X_{t-1} + \varepsilon_t + 0.4 \varepsilon_{t-1}$$

> [!question]- 答案解析
> **答案：** $(1 - 0.7B) X_t = 3 + (1 + 0.4B) \varepsilon_t$
> 
> **解析：** 
> - AR 多项式：$\phi(B) = 1 - 0.7B$
> - MA 多项式：$\theta(B) = 1 + 0.4B$
> - 常数项 $c = 3$ 保持不变
> 
> **最可能做错的原因：** MA 部分的符号写错（忘记 $\theta(B)$ 中 $B$ 的系数是 $+\theta_1$ 而不是 $-\theta_1$）。
> 
> **Obsidian 标签：** #自测/滞后算子

#### 题3

**题目：** 对于 ARMA(2,1) 模型：
$$X_t = 0.5 + 0.3 X_{t-1} + 0.2 X_{t-2} + \varepsilon_t + 1.5 \varepsilon_{t-1}$$

判断：(1) 是否平稳？(2) 是否可逆？

> [!question]- 答案解析
> **答案：**
> (1) **平稳性：** 需要检验 AR 特征方程 $1 - 0.3z - 0.2z^2 = 0$ 的根。
> 
> 解：$0.2z^2 + 0.3z - 1 = 0$
> 
> $z = \frac{-0.3 \pm \sqrt{0.09 + 0.8}}{0.4} = \frac{-0.3 \pm \sqrt{0.89}}{0.4} = \frac{-0.3 \pm 0.943}{0.4}$
> 
> $z_1 = \frac{0.643}{0.4} \approx 1.61$，$z_2 = \frac{-1.243}{0.4} \approx -3.11$
> 
> $|z_1| = 1.61 > 1$，$|z_2| = 3.11 > 1$，两个根都在单位圆外，**平稳**。
> 
> (2) **可逆性：** MA 部分系数 $\theta = 1.5$，$|\theta| = 1.5 > 1$，**不可逆**。
> 
> **解析：** 平稳性看 AR 特征根，可逆性看 MA 系数。两者独立判断。
> 
> **最可能做错的原因：** 混淆平稳性和可逆性的检验对象。
> 
> **对应误区：** 误区 2。
> 
> **Obsidian 标签：** #自测/平稳性可逆性

#### 题4

**题目：** 某序列的 ACF 和 PACF 都呈现逐渐衰减（拖尾）特征。以下哪个模型最适合？

A. AR(1)
B. MA(2)
C. ARMA(1,1)
D. 白噪声

> [!question]- 答案解析
> **答案：C**
> 
> **解析：**
> - AR(p)：ACF 拖尾，PACF 截尾
> - MA(q)：ACF 截尾，PACF 拖尾
> - ARMA(p,q)：ACF 拖尾，PACF 拖尾
> - 白噪声：ACF 和 PACF 都近似为 0
> 
> 题目说两者都拖尾，所以是 ARMA。
> 
> **最可能做错的原因：** 和 AR 或 MA 的特征记混。
> 
> **对应误区：** 误区 1。
> 
> **Obsidian 标签：** #自测/模型识别

#### 题5

**题目：** 考虑 ARMA(1,1) 模型 $X_t = \phi X_{t-1} + \varepsilon_t + \theta \varepsilon_{t-1}$（零均值形式）。

(1) 推导 $X_t$ 的 MA($\infty$) 表示（假设 $|\phi| < 1$）；
(2) 解释为什么 ARMA(1,1) 的 ACF 拖尾。

> [!question]- 答案解析
> **答案：**
> 
> (1) **MA($\infty$) 表示：**
> 
> 由 $(1 - \phi B) X_t = (1 + \theta B) \varepsilon_t$
> 
> $X_t = (1 - \phi B)^{-1} (1 + \theta B) \varepsilon_t$
> 
> 当 $|\phi| < 1$ 时，$(1 - \phi B)^{-1} = 1 + \phi B + \phi^2 B^2 + \cdots$
> 
> 所以：
> $$X_t = (1 + \phi B + \phi^2 B^2 + \cdots)(1 + \theta B) \varepsilon_t$$
> $$= [1 + (\phi + \theta) B + (\phi^2 + \phi\theta) B^2 + \cdots] \varepsilon_t$$
> $$= \varepsilon_t + (\phi + \theta) \varepsilon_{t-1} + \phi(\phi + \theta) \varepsilon_{t-2} + \cdots$$
> 
> (2) **ACF 拖尾的原因：**
> 
> 从 MA($\infty$) 表示可以看出，$X_t$ 包含了无限多个滞后冲击的线性组合。因此 $X_t$ 与 $X_{t-k}$ 之间通过共同的 $\varepsilon$ 项产生相关，且这种相关随 $k$ 增大而衰减（因为 $\phi^k \to 0$），所以 ACF 拖尾。
> 
> **解析：** 核心是将 ARMA 展开为 MA($\infty$)，然后利用无限阶 MA 的 ACF 性质。
> 
> **最可能做错的原因：** 不会用滞后算子展开，或者不理解为什么 MA($\infty$) 的 ACF 拖尾。
> 
> **Obsidian 标签：** #自测/推导证明

---

### 12. 我的主动回忆区

#### 我的闭卷复述

> 不看上文，用自己的话解释 ARMA 模型：
> 
> 

#### 我的推导复现

> 不看上文，尝试写出以下公式：
> - ARMA(p,q) 的方程：
> - 滞后算子形式：
> - 长期均值：
> - 平稳性条件：
> - 可逆性条件：
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
- **应链接的已有笔记：** AR 模型、MA 模型、ARIMA 模型、AIC/BIC、参数估计
- **建议标签：** #时间序列 #ARMA模型 #Box-Jenkins #经典模型层
- **是否需要拆分：**
  - 当前笔记已整合概念与核心推导
  - 若需更深入，可拆出「ARMA定阶实战」收录 ACF/PACF 图例和 auto_arima 代码
  - 可另建「ARMA与ARIMA衔接笔记」说明差分如何连接两者
- **与其他笔

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


