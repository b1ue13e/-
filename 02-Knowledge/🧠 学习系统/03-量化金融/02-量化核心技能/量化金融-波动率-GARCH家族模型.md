---
title: "GARCH 族波动率模型"
type: study
topic: "GARCH 族波动率模型"
created: "2026-08-03"
status: ongoing
difficulty: advanced
course: "量化金融"
importance: "A"
stage: "📘 第二阶段：量化核心技能"
tags: [学习, 量化金融]
concept: ["GARCH", "EGARCH", "杠杆效应"]
prerequisites: ["收益率定义与对数收益", "时间序列分析（GARCH 基础）"]
related: ["EVT极值理论与VaR-CVaR", "HW06-GARCH波动率与动态VaR", "HW07-非对称GARCH杠杆效应"]
upstream: ["Black-Scholes期权定价模型"]
downstream: ["EVT极值理论与VaR-CVaR"]
flow: knowledge
kind: concept
sources: 
- title: "Analysis of Financial Time Series (Tsay)"
url: "书库本地资源"
locator: "Chapter 3"
source_type: textbook
license: "local"
verified_at: 2026-08-03
nav_level: 8
nav_prev: "回测框架与无泄漏实验"
nav_next: "CAPM 资本资产定价模型"
---


# GARCH 族波动率模型

> [!info] 主线导航
> [[🗺️ 量化金融学习路径|返回路径]] · **Week 5** · 前置 [[单位根检验与 ADF 检验 (Unit Root & Augmented Dickey-Fuller Test)]] · 练习 [[03-Projects/开源课程课后习题/PS03-时间序列与波动率|PS03]] · 实验 [[03-Projects/Phase2-GARCH/README|GARCH]]

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：HW06/HW07 直接对象；动态 VaR 的波动率引擎，金融风险管理标配。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：收益波动聚集（大波动跟大波动），常数方差假设失效；且"利空比利好更吓人"（杠杆效应）——需要**不对称、时变**的方差模型。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：GARCH 提供时变 $\sigma_t$ → 动态 VaR、期权 IV 预测、风险调整。
- **实际应用场景**：VaR/CVaR、波动率交易、风险预算。
- **高频题型/任务**：GARCH(1,1) 方程；EGARCH 的杠杆项；$\alpha+\beta$ 持续性。

---

## 3. 学它之前需要哪些前置知识？

1. **[[收益率定义与对数收益]]**。
2. ARCH 效应检验（平方残差自相关）。

---

## 4. 用直觉语言解释它

> «"方差也有记忆：今天的震荡程度由昨天的震荡和昨天的冲击共同决定；利空冲击的'后劲'还更大。"»

**从散户心理学看波动率（电梯 vs 过山车）**
想象你和朋友各拿 1 万元，买入两只股票，连续 5 天：
- **股票 A（电梯型）**：`100 → 105 → 110 → 115 → 120`
- **股票 B（过山车型）**：`100 → 80 → 130 → 70 → 120`
第 5 天，你们账户都是 12,000 元（+20%）。但 B 中途经历了 -46% 的大回撤。
**量化研究员不仅看「赚多少」，还要看「中间有多颠」**。因为很多散户不是在终点卖出的，是在中途恐慌时割肉的。GARCH 就是用来度量和预测这种“颠簸（波动率）”在未来几天会如何演变的终极模型。

- **直觉类比/几何图像**：余震模型——大震后余震不断衰减。
- **为什么很自然**：波动聚集（大波动跟大波动）+ 杠杆效应（暴跌比暴涨更吓人）是金融数据的两条铁律。
- **核心代码实现**：计算历史波动率最核心的代码其实只有两行：
  
### 💡 公式与代码的“滴血认亲” (深度绑定)

GARCH 模型的极大似然估计看起来像天书，但它在实战中的落脚点非常简单。请对比下方的学术公式与 Pandas 代码：

| 学术公式符号 | 公式含义 | Python/Arch 变量名 | 实战物理意义 |
| :--- | :--- | :--- | :--- |
| **$y_t = \mu + \epsilon_t$** | 均值方程 (收益率) | `df['return']` | **【目标序列】** 这是你要算波动率的原始数据序列（比如 AAPL 每日收益率）。 |
| **$\epsilon_t^2$** | 过去的残差平方 | `resid**2` (Arch库底座) | **【历史震感】** 昨天这只股票震得厉不厉害？对应直觉中的“昨天的过山车幅度”。 |
| **$\sigma_{t-1}^2$** | 过去的条件方差 | `volatility**2` | **【历史惯性】** 之前一直以来的震荡惯性有多大？ |
| **$\omega, \alpha, \beta$** | GARCH 权重参数 | `res.params` | **【模型学习结果】** 电脑通过“极大似然估计”算出来的最佳配比。$\alpha$ 大说明受突发消息影响大；$\beta$ 大说明波动记忆长。 |

```python
import numpy as np
import pandas as pd

# 最小可运行输入；Capstone 中应替换为经过复权审计的 AAPL 收盘价。
df = pd.DataFrame({'Close': [100.0, 101.0, 99.5, 102.0, 101.5, 103.0]})
df['return'] = df['Close'].pct_change()
annual_vol = df['return'].std(ddof=1) * np.sqrt(252)

assert np.isfinite(annual_vol) and annual_vol > 0
print(f'annualized_volatility={annual_vol:.4f}')
```

> **边界说明**：这段代码只计算历史样本波动率，不是在拟合 GARCH。真正的 GARCH 作业必须继续估计 $\omega,\alpha,\beta$，并报告收敛状态与样本外预测误差。
- **一句话直觉本质**：**GARCH 族 = 把条件方差建成自回归过程；EGARCH 用对数形式捕捉非对称冲击。**

---

## 5. 正式定义、核心公式、符号解释

### 1. 最核心定义

GARCH(1,1)：$\sigma_t^2=\omega+\alpha\varepsilon_{t-1}^2+\beta\sigma_{t-1}^2$；EGARCH(1,1)：$\ln\sigma_t^2=\omega+\alpha(|z_{t-1}|-E|z_{t-1}|)+\gamma z_{t-1}+\beta\ln\sigma_{t-1}^2$。

### 2. 核心公式

长期方差：$\sigma^2=\omega/(1-\alpha-\beta)$；$\gamma<0$ 表示利空（$z<0$）冲击更大。

### 3. 符号说明表

| 符号 | 含义 | 备注 |
| :--- | :--- | :--- |
| $\alpha$ | 冲击项 | 新信息 |
| $\beta$ | 记忆项 | 持续性 |
| $\gamma$ | 杠杆系数 | EGARCH 独有 |
| $z_t$ | 标准化残差 | 分布假设 t/正态 |

### 4. 常见变体与适用条件

- **适用条件**：日频收益最典型；GJR-GARCH 与 EGARCH 二选一（杠杆效应）。
- **限制条件**：$\alpha+\beta\to1$ 时方差高度持续；分布假设影响 VaR 尾部（用 t 分布）。

---

## 6. 推导思路和思想来源

- **最初困难**：ARCH(q) 参数多。
- **直接方法局限**：高 q 过拟合。
- **关键"转念"**：Bollerslev 把 $\sigma_{t-1}^2$ 加入方程（方差自回归），ARCH 无限阶压缩为 (1,1)；Nelson (1991) 用 $\ln\sigma^2$ + 符号项实现非对称。
- **推导主线与动机**：MLE 估计；EGARCH 的对数形式保证方差为正（无需约束）。
- **为什么自然得到此结论**：方差与收益一样需要"记忆"，符号项区分好坏消息。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

- **题目**：$\omega=0.01,\alpha=0.1,\beta=0.85,\varepsilon_{t-1}^2=4,\sigma_{t-1}^2=1$，$\sigma_t^2$？
- **解题思路**：$0.01+0.4+0.85=1.26$。
- **最终答案**：1.26。
- **易错点**：$\varepsilon$ 是残差不是收益。
- **🤔 追问**：长期方差？（$0.01/0.05=0.2$）

### 例子 2：中等例子（条件判断与多步推理）

- **题目**：为什么 HW07 用 EGARCH 而非 GARCH？
- **完整解答**：GARCH 只对 $\varepsilon^2$ 敏感（对称），无法区分涨跌；EGARCH 的 $\gamma z_{t-1}$ 项让"下跌冲击"放大波动——符合杠杆效应实证。

### 例子 3：实际应用例子（真实场景/代码）

> [!important] 可执行实验
> [[03-Projects/Phase2-GARCH/README|Phase 2 GARCH 实验包]] 已实现 GARCH(1,1) 极大似然估计、冻结时间切分、一步样本外预测、滚动方差基线与 QLIKE，并提供自动测试和产物。

- **实际价值与转化**：先完成实验包中的 Gaussian QMLE 基线，再使用 `arch` 包扩展到 EGARCH、GJR-GARCH 与 t 分布；任何扩展都必须保持同一冻结测试集和基线口径。

---

## 8. 常见误区和易混概念

### 误区 1："GARCH 预测收益率"
- **错误直觉**：波动模型预测方向。
- **为什么错**：GARCH 只建模方差。
- **正确理解**：用于风险与期权，不用于方向。

### 概念对比表

| 模型 | 特征 | 场景 |
| :--- | :--- | :--- |
| GARCH | 对称 | 基础 VaR |
| EGARCH | 杠杆效应 | 股票指数 |
| GJR | 阈值非对称 | 同 EGARCH |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)|Black-Scholes期权定价模型]]（σ 输入）

### 下游延伸
- [[EVT极值理论与VaR-CVaR]]：尾部修正

### 横向关联
- [[[支线任务] HW06-GARCH波动率与动态VaR]] [[[支线任务] HW07-非对称GARCH]] ↔ 本卡：作业

### 应用场景
- HW06/07

---

## 10. 闭卷复现任务

合上笔记后，请独立回答以下 10 个问题：
- [ ] 1. GARCH 解决什么问题
- [ ] 2. 直觉：余震
- [ ] 3. 写出 GARCH(1,1)
- [ ] 4. 写出 EGARCH 对数式
- [ ] 5. 符号：$\alpha,\beta,\gamma$
- [ ] 6. 推导主线：方差自回归
- [ ] 7. 手算一步方差
- [ ] 8. 预测收益误区
- [ ] 9. 与 VaR 关系
- [ ] 10. 一个应用

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 杠杆效应 |
| 2 | 公式运用 | 基础 | 长期方差 |
| 3 | 条件判断 | 中等 | 持续性 |
| 4 | 变式/综合 | 中等 | 分布选择 |
| 5 | 开放 | 较难 | 动态 VaR |

### 题目与解析

#### 1. 杠杆效应指什么？
> [!question]- 答案解析
> - **答案**：利空冲击对波动的放大大于利好。
> - **解析**：$\gamma<0$。
> - **易错原因**：以为对称。

#### 2. $\omega=0.02,\alpha=0.08,\beta=0.9$ 长期方差？
> [!question]- 答案解析
> - **答案**：$0.02/0.02=1$。
> - **解析**：$\omega/(1-\alpha-\beta)$。
> - **易错原因**：分母错。

#### 3. $\alpha+\beta$ 接近 1 的含义？
> [!question]- 答案解析
> - **答案**：波动冲击高度持续（近似 IGARCH）。
> - **解析**：记忆长。
> - **易错原因**：以为不平稳不可用。

#### 4. VaR 计算为何常用 t 分布？
> [!question]- 答案解析
> - **答案**：收益尾部厚于正态，t 分位数更准。
> - **解析**：正态低估尾部。
> - **易错原因**：一律正态。

#### 5. 动态 VaR 流程？
> [!question]- 答案解析
> - **答案**：GARCH 估计 → $\hat\sigma_{t+1}$ → $\text{VaR}=\mu+z_\alpha\hat\sigma_{t+1}$ → Kupiec 回测。
> - **解析**：估计-预测-回测。
> - **易错原因**：跳过回测。

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

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/03-量化金融/`
- **关联已有笔记**：[[EVT极值理论与VaR-CVaR]] [[[支线任务] HW06-GARCH波动率与动态VaR]]
- **建议标签**：`#学习` `#量化金融`
- **拆分建议**：不拆分


---

## 🎮 交互实验室 (HTML) 与 实战靶场 (Jupyter)

光看公式没用，跑通代码才是真的！利用下方组件进行交互或直接跑通实盘代码：

### 🧪 交互实验室
> 拖动下方滑块，亲手感受公式中各个参数是如何改变结果的。
> **样本标准差 (Sample Std Dev)**
> [标准差交互实验源码](https://github.com/datawhalechina/quant-for-beginners/blob/main/assets/interactive/std-dev-demo.html)

> **总体方差 (Population Variance)**
> [总体方差交互实验源码](https://github.com/datawhalechina/quant-for-beginners/blob/main/assets/interactive/population-variance-demo.html)

> **方差修正公式**
> [方差公式交互实验源码](https://github.com/datawhalechina/quant-for-beginners/blob/main/assets/interactive/variance-formulas-demo.html)（扩展材料，见 [[📦 外部实验资产索引]]）

### 💻 实战靶场
- [打开 Notebook：理解波动率](https://github.com/datawhalechina/quant-for-beginners/blob/main/notebooks/phase2_intro/01_理解波动率.ipynb)


---

## 🖼️ 量化名人堂 (Hall of Fame)

> 在这冰冷的公式背后，是这些天才数学家用一生在华尔街厮杀出来的智慧结晶：

**ARCH模型发明者、诺贝尔奖得主：Robert Engle**
![Robert Engle](https://raw.githubusercontent.com/datawhalechina/quant-for-beginners/main/notebooks/phase2_intro/Robert%20Engle.jpg)

\n

---
\n\n> ⚔️ **支线实战任务 (Side Quest)**：👉 点击进入 [[[支线任务] HW06-GARCH波动率与动态VaR]] 刷怪通关！\n\n> 🧭 **自动导航 (Dataview Engine)**

```dataview
TABLE WITHOUT ID 
  "⬅️ [[" + nav_prev + "]]" AS "上一课", 
  "🏠 [[🗺️ 量化金融全栈终极框架 (Academic + AFML + HFT)|回到主干]]" AS "主菜单", 
  "➡️ [[" + nav_next + "]]" AS "下一课"
WHERE file.path = this.file.path
```
