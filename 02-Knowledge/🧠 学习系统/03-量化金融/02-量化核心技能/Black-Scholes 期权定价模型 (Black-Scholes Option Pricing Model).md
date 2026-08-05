---
title: "Black-Scholes 期权定价模型"
type: study
topic: "Black-Scholes 期权定价模型"
created: "2026-08-03"
status: ongoing
difficulty: advanced
course: "量化金融"
importance: "A"
stage: "📘 第二阶段：量化核心技能"
tags: [学习, 量化金融]
concept: ["期权定价", "Black-Scholes", "Greeks", "风险中性"]
prerequisites: ["收益率定义与对数收益", "随机过程（几何布朗运动）"]
related: ["量化金融-波动率-GARCH家族模型", "[支线任务] HW05-BSM期权定价与对冲"]
upstream: ["收益率定义与对数收益"]
downstream: ["量化金融-波动率-GARCH家族模型"]
flow: knowledge
kind: concept
source: "Hull, Options, Futures, and Other Derivatives, Chapters 13-19"
anki_deck: "量化金融::衍生品定价"
anki_tags: [量化金融, Black-Scholes, 期权定价]
sources: 
- title: "Options, Futures, and Other Derivatives (Hull)"
url: "书库本地资源"
locator: "Chapters 13-19"
source_type: textbook
license: "local"
verified_at: 2026-08-03
---

# Black-Scholes 期权定价模型

> [!info] 主线导航
> [[🗺️ 量化金融学习路径|返回路径]] · **Week 7** · 前置 [[量化金融-随机过程-伊藤引理与随机微分方程]] · 练习 [[03-Projects/开源课程课后习题/PS05-随机微积分与SDE|PS05]] · 实验 [[03-Projects/HW05-BSM/README|HW05]]

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：HW05 直接对象；衍生品定价的基准模型，Greeks 是风险管理的日常工具。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：期权价格取决于未来波动，无法直接观测。需要"不依赖个人风险偏好"的定价——**风险中性定价**。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：BS 是"无套利+对冲"范式的巅峰；隐含波动率（由市场价反解）成为市场情绪指标。
- **实际应用场景**：期权报价、对冲（Delta/Gamma）、波动率交易。
- **高频题型/任务**：写出 BS 公式与 5 个假设；计算 Delta/Gamma；解释风险中性测度。

---

## 3. 学它之前需要哪些前置知识？

1. **[[收益率定义与对数收益]]**。
2. 几何布朗运动与伊藤引理（直觉级）。

---

## 4. 用直觉语言解释它

> «"只要能用股票+债券'复制'出期权，期权价格就是复制成本——市场怎么想不重要。"»

- **直觉类比/几何图像**：期权 = 可复制的"组合产品"，价格 = 复制成本。
- **为什么很自然**：无套利下复制品与被复制品必须同价。
- **一句话直觉本质**：**BS = 在几何布朗运动假设下，用动态对冲消除风险，再求复制组合的价格。**

---

## 5. 正式定义、核心公式、符号解释

### 1. 最核心定义

欧式看涨：$C = S_0 N(d_1) - K e^{-rT}N(d_2)$，其中 $d_1=\dfrac{\ln(S_0/K)+(r+\sigma^2/2)T}{\sigma\sqrt{T}}$，$d_2=d_1-\sigma\sqrt{T}$。

### 2. 核心公式

BS PDE：$\dfrac{\partial V}{\partial t}+\frac{1}{2}\sigma^2 S^2\dfrac{\partial^2 V}{\partial S^2}+rS\dfrac{\partial V}{\partial S}-rV=0$。

### 3. 符号说明表

| 符号 | 含义 | 备注 |
| :--- | :--- | :--- |
| $S_0,K,T$ | 标的价格/行权价/期限 | 可观测 |
| $\sigma$ | 波动率 | 唯一"隐藏"输入 |
| $N(\cdot)$ | 标准正态 CDF | |
| $r$ | 无风险利率 | 常数假设 |

### 4. 常见变体与适用条件

- **适用条件**：欧式期权、无分红、常数 $\sigma,r$、连续交易。
- **限制条件**：真实市场有波动率微笑（$\sigma$ 随 K/T 变化）、跳变、分红——需用隐含波动率曲面或随机波动率模型（Heston）。

---

## 6. 推导思路和思想来源

### 6.1 从标的随机过程出发

假设无分红股票满足几何布朗运动：

$$
dS=\mu S\,dt+\sigma S\,dW,
$$

其中 $\mu$ 是真实世界预期收益率。设期权价值为 $V(S,t)$，且 $V$ 对 $t$ 一阶可微、对 $S$ 二阶可微。由伊藤引理：

$$
dV=\left(V_t+\mu S V_S+\frac12\sigma^2S^2V_{SS}\right)dt
+\sigma S V_S\,dW.
$$

这里的困难是 $dW$ 带来随机风险，而 $\mu$ 也不能从无套利条件直接观察。

### 6.2 构造 Delta 对冲组合

构造持有一份期权、做空 $\Delta$ 股股票的自融资组合：

$$
\Pi=V-\Delta S,\qquad d\Pi=dV-\Delta\,dS.
$$

在一次无穷小再平衡区间内取 $\Delta=V_S$。代入 $dV$ 与 $dS$：

$$
\begin{aligned}
d\Pi
&=\left(V_t+\mu S V_S+\frac12\sigma^2S^2V_{SS}\right)dt
  +\sigma S V_SdW \\
&\quad -V_S\left(\mu Sdt+\sigma SdW\right) \\
&=\left(V_t+\frac12\sigma^2S^2V_{SS}\right)dt.
\end{aligned}
$$

$\mu$ 项和 $dW$ 项同时被消掉，因此组合在该瞬间无风险。无套利要求它只能赚取无风险利率：

$$
d\Pi=r\Pi\,dt=r(V-SV_S)dt.
$$

比较两个 $d\Pi$，移项得到 Black–Scholes PDE：

$$
\boxed{V_t+\frac12\sigma^2S^2V_{SS}+rSV_S-rV=0}.
$$

**关键转念**：不是先猜投资者要求多少风险溢价，而是先用 $\Delta=V_S$ 消掉风险。正因为 $\mu$ 被消去，定价公式不依赖个人风险偏好。

### 6.3 加入终值条件并得到闭式解

欧式看涨期权到期支付为：

$$
V(S,T)=\max(S-K,0).
$$

同一 PDE 也可写成风险中性期望：

$$
C_0=e^{-rT}\mathbb E^{\mathbb Q}[\max(S_T-K,0)],
$$

且风险中性测度下

$$
\ln S_T\sim\mathcal N\left(\ln S_0+\left(r-\frac12\sigma^2\right)T,\;\sigma^2T\right).
$$

令

$$
X=\frac{\ln(S_T/S_0)-(r-\sigma^2/2)T}{\sigma\sqrt T}\sim\mathcal N(0,1).
$$

事件 $S_T>K$ 等价于 $X>-d_2$。把支付拆成两项：

$$
\begin{aligned}
C_0
&=e^{-rT}\mathbb E^{\mathbb Q}[(S_T-K)\mathbf 1_{\{S_T>K\}}]\\
&=e^{-rT}\left(
\mathbb E^{\mathbb Q}[S_T\mathbf 1_{\{S_T>K\}}]
-K\mathbb Q(S_T>K)
\right).
\end{aligned}
$$

第二项直接由标准正态分布得到：

$$
\mathbb Q(S_T>K)=\mathbb Q(X>-d_2)=N(d_2).
$$

第一项写成标准正态密度 $\phi(x)$ 的积分：

$$
\mathbb E^{\mathbb Q}[S_T\mathbf 1_{\{S_T>K\}}]
=S_0e^{(r-\sigma^2/2)T}
\int_{-d_2}^{\infty}e^{\sigma\sqrt T x}\phi(x)\,dx.
$$

利用配方恒等式

$$
e^{ax}\phi(x)=e^{a^2/2}\phi(x-a),\qquad a=\sigma\sqrt T,
$$

可得

$$
\begin{aligned}
\mathbb E^{\mathbb Q}[S_T\mathbf 1_{\{S_T>K\}}]
&=S_0e^{rT}\int_{-d_2}^{\infty}\phi(x-\sigma\sqrt T)\,dx\\
&=S_0e^{rT}N(d_2+\sigma\sqrt T)\\
&=S_0e^{rT}N(d_1).
\end{aligned}
$$

代回两项并贴现，得到：

$$
C_0=S_0N(d_1)-Ke^{-rT}N(d_2),
$$

其中

$$
d_1=\frac{\ln(S_0/K)+(r+\sigma^2/2)T}{\sigma\sqrt T},
\qquad
d_2=d_1-\sigma\sqrt T.
$$

$N(d_2)$ 可解释为风险中性测度下到期价内概率；$N(d_1)$ 是看涨期权 Delta，不应把两者混为一谈。

### 6.4 推导成立的边界

- 连续对冲、无交易成本与无限流动性是理想化假设；离散调仓会留下 Gamma 风险。
- 若标的连续分红率为 $q$，公式需改为 $S_0e^{-qT}N(d_1)-Ke^{-rT}N(d_2)$。
- 美式看跌可能提前行权，不能直接套用欧式闭式解。
- 波动率微笑说明常数 $\sigma$ 与对数正态尾部在真实市场中并不充分。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

- **题目**：$S_0=100,K=100,T=1,r=5\%,\sigma=20\%$，求 $d_1$。
- **解题思路**：$d_1=[\ln1+(0.05+0.02)\times1]/(0.2)=0.35$。
- **最终答案**：$d_1=0.35$，$d_2=0.15$，$N(0.35)\approx0.637$。
- **易错点**：$\sigma^2/2$ 项漏掉。
- **🤔 追问**：$\sigma$ 增大时 $d_1$ 一定增大吗？不一定；但在其他输入固定时，欧式看涨期权的 Vega 为正，所以期权价格随 $\sigma$ 增大。

### 例子 2：中等例子（条件判断与多步推理）

- **题目**：隐含波动率微笑说明什么？
- **完整解答**：同一到期日的不同行权价反解出不同隐含波动率，说明常数波动率假设不能同时解释全部报价。对股票指数，常见的是低行权价隐含波动率更高的偏斜。这里比较的是**相对 Black–Scholes 基准的隐含波动率**；欧式看涨期权的绝对价格在其他条件固定时仍随行权价上升而不增，不能说“越虚值绝对价格越贵”。

### 例子 3：实际应用例子（真实场景/代码）

```python
from math import exp, log, sqrt

from scipy.stats import norm


def black_scholes_call(spot, strike, maturity, rate, volatility):
    """无分红欧式看涨期权；rate 和 volatility 使用小数。"""
    if min(spot, strike, maturity, volatility) <= 0:
        raise ValueError('spot、strike、maturity、volatility 必须为正')

    d1 = (
        log(spot / strike)
        + (rate + 0.5 * volatility**2) * maturity
    ) / (volatility * sqrt(maturity))
    d2 = d1 - volatility * sqrt(maturity)
    price = spot * norm.cdf(d1) - strike * exp(-rate * maturity) * norm.cdf(d2)
    return price, d1, d2


price, d1, d2 = black_scholes_call(
    spot=100.0,
    strike=110.0,
    maturity=1.0,
    rate=0.05,
    volatility=0.20,
)

assert abs(d2 - (-0.326551)) < 1e-6
print(f'call={price:.4f}, d1={d1:.6f}, d2={d2:.6f}')
# 输出：call=6.0401, d1=-0.126551, d2=-0.326551
```

- **实际价值与转化**：这段代码给出可复核的基准价格。生产系统还必须加入分红、交易日历、报价清洗、隐含波动率反解和数值容差测试。

---

## 8. 常见误区和易混概念

### 误区 1："BS 价格就是市场价"
- **错误直觉**：公式给出精确价格。
- **为什么错**：假设不成立（波动率随机、跳变、交易成本）。
- **正确理解**：BS 是"基准+语言"（用 IV 报价），不是事实。

### 概念对比表

| 概念 | 用途 | 区别 |
| :--- | :--- | :--- |
| BS 公式 | 欧式定价 | 常数 σ |
| 二叉树 | 美式/离散 | 数值法 |
| Heston | 随机波动率 | σ 随机 |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[收益率定义与对数收益]]、随机过程

### 下游延伸
- [[量化金融-波动率-GARCH家族模型]]：$\sigma$ 的时变建模

### 横向关联
- [[[支线任务] HW05-BSM期权定价与对冲]] ↔ 本卡：作业实操

### 应用场景
- HW05

---

## 10. 闭卷复现任务

合上笔记后，请独立回答以下 10 个问题：
- [ ] 1. BS 解决什么问题
- [ ] 2. 直觉：复制组合
- [ ] 3. 写出看涨公式
- [ ] 4. 写出 BS PDE
- [ ] 5. 符号：$d_1,N,K$
- [ ] 6. 推导主线：Delta 对冲
- [ ] 7. 手算 $d_1$
- [ ] 8. IV 微笑误区
- [ ] 9. 与 Heston 关系
- [ ] 10. 一个应用

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 风险中性 |
| 2 | 公式运用 | 基础 | $d_1$ |
| 3 | 条件判断 | 中等 | Greeks |
| 4 | 变式/综合 | 中等 | 微笑 |
| 5 | 开放 | 较难 | 对冲 |

### 题目与解析

#### 1. 为什么 BS 定价不含风险偏好？
> [!question]- 答案解析
> - **答案**：Delta 对冲消除风险，价格由无套利唯一决定。
> - **解析**：可复制性。
> - **易错原因**：以为含真实概率。
> - **Obsidian 标签建议**：`#自测题/基础`

#### 2. $S=100,K=110,T=1,r=5\%,\sigma=20\%$ 的 $d_2$？
> [!question]- 答案解析
> - **答案**：$d_1=[\ln(100/110)+(0.05+0.20^2/2)]/0.20\approx-0.1266$，所以 $d_2=d_1-0.20\approx-0.3266$。
> - **解析**：也可直接使用 $d_2=[\ln(S/K)+(r-\sigma^2/2)T]/(\sigma\sqrt T)$ 交叉检查。
> - **易错原因**：公式记忆错。
> - **Obsidian 标签建议**：`#自测题/基础`

#### 3. Delta 的用途？
> [!question]- 答案解析
> - **答案**：标的价格变动 1 单位时期权价格变动量；对冲比率。
> - **解析**：$N(d_1)$。
> - **易错原因**：与 Gamma 混淆。
> - **Obsidian 标签建议**：`#自测题/中等`

#### 4. 波动率微笑说明？
> [!question]- 答案解析
> - **答案**：不同行权价反解出的隐含波动率不同，说明常数波动率 BSM 无法同时解释全部报价。
> - **解析**：这不能单独识别真实分布一定“厚尾”；还可能来自随机波动率、跳跃、流动性和报价摩擦。IV 曲面仍可作为相对定价与风险管理工具。
> - **易错原因**：以为模型错即无用。
> - **Obsidian 标签建议**：`#自测题/中等`

#### 5. Delta 对冲为何需动态调整？
> [!question]- 答案解析
> - **答案**：Delta 随 $S,t,\sigma$ 变化，需再平衡。
> - **解析**：离散对冲有误差。
> - **易错原因**：以为对冲一次完成。
> - **Obsidian 标签建议**：`#自测题/较难`

---

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，用自己的话解释这个知识点：

### 我的推导复现
> 不看上文，尝试写出核心公式或推导主线：

### 我的错误与卡点
-

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 🃏 Anki 卡片

- Black-Scholes PDE 如何由 Delta 对冲得到？ :: 对 $V(S,t)$ 使用伊藤引理，构造 $\Pi=V-V_SS$ 消掉 $dW$ 与真实收益率 $\mu$，令无风险组合满足 $d\Pi=r\Pi dt$，整理得 $V_t+\frac12\sigma^2S^2V_{SS}+rSV_S-rV=0$。
- $N(d_1)$ 与 $N(d_2)$ 分别表示什么？ :: $N(d_1)$ 是无分红欧式看涨期权的 Delta；$N(d_2)$ 可解释为风险中性测度下到期价内概率。
- Black-Scholes 模型的三个关键失效边界是什么？ :: 离散对冲与交易成本、波动率非常数或价格跳跃、美式期权提前行权。

---

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/03-量化金融/`
- **关联已有笔记**：[[[支线任务] HW05-BSM期权定价与对冲]] [[量化金融-波动率-GARCH家族模型]]
- **建议标签**：`#学习` `#量化金融`
- **拆分建议**：不拆分
