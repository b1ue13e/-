---
title: "主线-金融与时序"
type: moc
kind: moc
flow: knowledge
track: "金融与时序"
status: active
created: 2026-07-30
updated: 2026-07-30
tags:
  - MOC
  - 主线
  - 时间序列
  - 量化金融
  - 最优化方法
  - 运筹学
  - 知识网络
---

# 📈 主线：金融与时序 (Quantitative Finance, Time Series & Optimization Track)

> 🧭 **主线宗旨**：整合时间序列分析、量化金融、最优化方法与运筹学 4 门硬核课程。打通从平稳性检验、ARIMA/GARCH 预测到 Alpha 因子回测、凸优化理论与运筹约束决策的完整闭环。

---

## 🗺️ 4 门子线路径逻辑递进图

```mermaid
flowchart TD
    subgraph 最优化与决策理论
        OPT["[[🗺️ 最优化方法学习路径\|07-最优化方法]]<br/>(凸优化, 梯度下降, KKT 条件, 拟牛顿法)"]
        OR["[[🗺️ 运筹学学习路径\|29-运筹学]]<br/>(线性规划, 整数规划, 动态规划, 网络流)"]
        OPT --> OR
    end

    subgraph 时序预测与量化金融
        TS["[[🗺️ 时间序列分析学习路径|02-时间序列分析]]<br/>(单位根检验, ARIMA, VAR, GARCH, 协整)"]
        QF["[[🗺️ 量化金融学习路径|03-量化金融]]<br/>(CAPM, Alpha 因子, 印花税回测, Qlib 框架)"]
        TS --> QF
    end

    OPT --> QF
```

---

## 🔑 全库唯一 Master 概念卡

时序与量化核心理论统一收拢至基础课程 Master 卡，领域应用建立后缀卡（如 `ARIMA模型-量化应用.md`）：

1. **单位根检验与平稳性**：[[ADF单位根检验]]
2. **ARIMA 模型与 Box-Jenkins 范式**：[[02-Knowledge/🧠 学习系统/02-时间序列分析/03-经典模型层/ARIMA模型]] ($\Phi(B)(1-B)^d X_t = \Theta(B)\epsilon_t$)
3. **凸优化与 KKT 对偶条件**：[[KKT条件与对偶理论]] ($\nabla f_0(x^*) + \sum \lambda_i^* \nabla f_i(x^*) + \sum \nu_i^* \nabla h_i(x^*) = 0$)
4. **夏普比率与因子回测评估**：[[夏普比率与回测指标]] ($\text{Sharpe} = \frac{\mathbb{E}[R_p - R_f]}{\sigma_p}$)
5. **线性规划与单纯形法**：[[单纯形法与线性规划]] ($\max \mathbf{c}^T\mathbf{x} \text{ s.t. } \mathbf{A}\mathbf{x} \le \mathbf{b}$)

---

## 📊 包含子路径看板 (Dataview)

```dataview
TABLE course AS "课程名称", status AS "状态", importance AS "优先级", updated AS "最近更新"
FROM "02-Knowledge/🧠 学习系统"
WHERE type = "index" AND track = "金融与时序"
SORT file.name ASC
```

---

*主线更新时间：2026-07-30 | 状态：active*
