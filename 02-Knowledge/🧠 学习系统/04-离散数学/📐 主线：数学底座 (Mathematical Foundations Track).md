---
title: "主线-数学底座"
type: moc
kind: moc
flow: knowledge
track: "数学底座"
status: active
created: 2026-07-30
updated: 2026-07-30
tags:
  - MOC
  - 主线
  - 数学底座
  - 知识网络
---

# 📐 主线：数学底座 (Mathematical Foundations Track)

> 🧭 **主线宗旨**：为人工智能、机器学习、控制理论与量化金融提供严密的数学支撑。收拢代数、分析、几何与数值方法，遵循 `AGENTS.md` 唯一主卡规则，建立从离散/连续结构到无限维泛函空间的递进学习路径。

---

## 🗺️ 10 门子线路径逻辑递进图

```mermaid
flowchart TD
    subgraph 基础代数与分析
        L0_1["[[🗺️ 离散数学学习路径|04-离散数学]]<br/>(集合, 逻辑, 图论, 组合)"]
        L0_2["[[🗺️ 高等代数学习路径|09-高等代数]]<br/>(向量空间, 矩阵分解, 线性变换)"]
        L0_3["[[🗺️ 数学分析学习路径\|28-数学分析]]<br/>(极限, 微积分, 级数, 拓扑入门)"]
    end

    subgraph 连续方程与复分析
        L0_1 --> L1_1["[[🗺️ 常微分方程学习路径|06-常微分方程]]<br/>(动力系统, 线性方程组)"]
        L0_3 --> L1_2["[[🗺️ 复变函数学习路径\|37-复变函数]]<br/>(解析函数, 留数定理, 保形映射)"]
        L1_1 --> L2_1["[[🗺️ 偏微分方程学习路径\|34-偏微分方程]]<br/>(波动/热传导/拉普拉斯方程)"]
    end

    subgraph 高级实分析与泛函
        L0_3 --> L1_3["[[🗺️ 实变函数学习路径\|26-实变函数]]<br/>(Lebesgue 积分, 可测函数)"]
        L1_3 --> L2_2["[[🗺️ 测度论学习路径\|25-测度论]]<br/>(测度空间, 概率测度底座)"]
        L2_2 --> L3_1["[[🗺️ 泛函分析学习路径\|27-泛函分析]]<br/>(Hilbert/Banach 空间, 算子理论)"]
    end

    subgraph 计算与数值逼近
        L0_2 & L0_3 --> L2_3["[[🗺️ 数值分析学习路径\|35-数值分析]]<br/>(数值线性代数, 差分法, 误差控制)"]
    end
```

---

## 🔑 全库唯一 Master 概念卡

所有数学定义、定理与推导统一收拢至基础数学路径中的 canonical 主卡，禁止在应用课程中复制大段定义：

1. **特征值与奇异值分解**：[[奇异值分解SVD]] ($\mathbf{A} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T$)
2. **泰勒展开与极值条件**：[[泰勒公式与Hessian矩阵]] ($\mathbf{H}_{ij} = \frac{\partial^2 f}{\partial x_i \partial x_j}$)
3. **Lebesgue 积分与控制收敛**：[[Lebesgue控制收敛定理]]
4. **Hilbert 空间与正交投影**：[[Hilbert空间与内积]] ($\langle f, g \rangle$)
5. **常微分线性系统与矩阵指数**：[[矩阵指数与状态转移矩阵]] ($e^{\mathbf{A}t}$)

---

## 📊 包含子路径看板 (Dataview)

```dataview
TABLE course AS "课程名称", status AS "状态", importance AS "优先级", updated AS "最近更新"
FROM "02-Knowledge/🧠 学习系统"
WHERE type = "index" AND track = "数学底座"
SORT file.name ASC
```

---

*主线更新时间：2026-07-30 | 状态：active*
