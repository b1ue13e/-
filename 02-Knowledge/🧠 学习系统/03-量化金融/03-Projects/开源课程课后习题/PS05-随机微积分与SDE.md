---
type: study
topic: "随机微积分与SDE课后习题"
created: 2026-08-06
status: completed
difficulty: advanced
concept: ["伊藤引理", "随机微分方程", "无套利复制"]
prerequisites: ["概率论", "Black-Scholes 期权定价模型"]
related: ["量化金融-随机过程-伊藤引理与随机微分方程", "期权希腊字母"]
tags: [学习, 开源课程, 课后习题, MIT-OCW]
flow: project
kind: problem-type
source: "MIT18_S096F13_pset8; MIT18_S096F13_pset9"
---

# PS05：随机微积分与 SDE

> **来源改编**：`MIT18_S096F13_pset8`（Stochastic Calculus）与 `MIT18_S096F13_pset9`（Stochastic Differential Equations）。原题链接和许可见 [[README]]。

## 对应知识卡

- [[04-深入精通/量化金融-随机过程-伊藤引理与随机微分方程]]
- [[02-量化核心技能/Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)]]
- [[02-量化核心技能/期权希腊字母 (Option Greeks_ Delta, Gamma, Theta, Vega, Rho)]]

## 作答协议

本练习是进阶区。先记录作答前信心；示例题允许逐行跟随，仿做题只看提示 1，独立题和迁移题必须闭卷。每个等式注明依据；打开答案锚点后记为借助完成。记录错因、重测日期和作答后信心。

### 题 1（示例题）：$B_t^2$ 的微分

设 $B_t$ 为标准布朗运动。使用伊藤引理求 $d(B_t^2)$，解释为什么普通链式法则少一项。

> [!hint]- 提示 1
> 对 $f(x)=x^2$ 写出 $f'$ 和 $f''$。
> [!hint]- 提示 2
> 伊藤引理含 $\frac12f''(B_t)(dB_t)^2$，且 $(dB_t)^2=dt$。
> [!success]- 答案锚点
> $d(B_t^2)=2B_t\,dB_t+dt$。普通链式法则遗漏由二次变差产生的 $dt$。

### 题 2（仿做题）：几何布朗运动的对数

$dS_t=\mu S_tdt+\sigma S_tdW_t$。使用伊藤引理求 $d\log S_t$，指出漂移修正项。

> [!hint]- 提示 1
> $f'(S)=1/S$，$f''(S)=-1/S^2$。
> [!hint]- 提示 2
> 代入 $dS$ 与 $(dS)^2=\sigma^2S^2dt$。
> [!success]- 答案锚点
> $d\log S_t=(\mu-\frac12\sigma^2)dt+\sigma dW_t$；$-\frac12\sigma^2$ 是伊藤修正。

### 题 3（独立题）：指数鞅

验证 $M_t=\exp(\sigma B_t-\frac12\sigma^2t)$ 的漂移项为零，并在可积条件下解释它为何是鞅。

> [!hint]- 提示 1
> 对 $f(t,x)=\exp(\sigma x-\frac12\sigma^2t)$ 使用二维伊藤引理。
> [!hint]- 提示 2
> 检查 $f_t+\frac12f_{xx}$。
> [!success]- 答案锚点
> 两个 $dt$ 项抵消，$dM_t=\sigma M_tdB_t$；在满足相应可积条件时，其条件期望保持当前值。

### 题 4（独立题）：验证 SDE 显式解

令 $S_t=S_0\exp((\mu-\frac12\sigma^2)t+\sigma W_t)$。逐步验证它满足 $dS_t=\mu S_tdt+\sigma S_tdW_t$。

> [!hint]- 提示 1
> 把指数内部记为 $X_t$，先写 $dX_t$ 和 $(dX_t)^2$。
> [!hint]- 提示 2
> 对 $e^{X_t}$ 用伊藤引理，二阶项会补回 $\frac12\sigma^2dt$。
> [!success]- 答案锚点
> $dS_t=S_t[dX_t+\frac12(dX_t)^2]=S_t(\mu dt+\sigma dW_t)$，且 $S_0$ 满足初值。

### 题 5（迁移题）：一期复制与无套利

一期模型中 $S_0=100$，上涨到 110 或下跌到 90，无风险利率为 0，执行价 $K=100$ 的看涨期权到期支付分别为 10 和 0。求风险中性概率、期权价格和复制 Delta。

> [!hint]- 提示 1
> 令风险中性期望的股票终值等于 100。
> [!hint]- 提示 2
> $\Delta=(C_u-C_d)/(S_u-S_d)$。
> [!success]- 答案锚点
> 风险中性概率 $q=0.5$，期权价 5，$\Delta=0.5$。这来自无套利复制，不是对真实上涨概率的预测。

### 题 6（迁移题）：离散对冲误差实验

用代码模拟同一组几何布朗运动路径，分别按 12、52、252 个时间步做 Delta 对冲；报告无交易成本与 10 bps 成本下的误差均值、标准差和 RMSE。解释为什么增加调仓频率不保证含成本 RMSE 单调下降。

> [!hint]- 提示 1
> 固定随机种子和路径，保证比较只改变调仓频率。
> [!hint]- 提示 2
> 更频繁调仓降低离散误差，却增加换手和成本；两者方向相反。
> [!success]- 答案锚点
> 验收不要求固定数值，但要求同路径公平比较、成本从换手扣除、给出三项误差指标。若声称“频率越高必然越好”，结论不通过。

## 错因与重测

| 题号 | 错因 | 作答前信心 | 补救页 | 重测日期 | 作答后信心 |
| :--- | :--- | :---: | :--- | :--- | :---: |
| | 伊藤项 / 条件期望 / 无套利 / 数值实验 | | | 24h / 72h / 7d | |

