---
type: study
topic: "PBH能控"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段5-状态空间与现代控制]]"
flow: knowledge
kind: concept
concept: ["PBH判据", "能控性", "特征向量"]
prerequisites: ["能控性定义", "特征值分析"]
related: ["能控性定义", "能观性定义"]
upstream: ["[[05-状态空间与现代控制/能控性定义]]"]
source: "Modern Control Engineering (Ogata) Ch.10; Popov-Belevitch-Hautus"
tags: [学习, 控制与机器人学, 能控能观]
---

# PBH能控

## 0. 为什么学它

能控性矩阵判据在数值上可能病态。**PBH（Popov-Belevitch-Hautus）判据**从特征向量角度给出等价且更直观的判定：不可控模态 = 与输入正交的特征向量——还能定位"哪个模态不可控"。

## 1. 核心判据

**PBH 判据**：$(A,B)$ 能控 ⟺ 对 $A$ 的**每个特征值** $\lambda_i$，

$$\text{rank}\begin{bmatrix}\lambda_i I-A & B\end{bmatrix}=n\quad(\text{行满秩}).$$

**等价形式**：不存在 $A$ 的**左特征向量** $w\ne0$ 满足

$$w^\top A=\lambda w^\top,\qquad w^\top B=0.$$

**含义**：若某模态的特征向量与输入"正交"（$w^\top B=0$），则该模态不被输入激励 → 不可控。

## 2. 最小可手算例子

**题目**：$A=\begin{pmatrix}1&1\\0&1\end{pmatrix},\ B=(1,0)^\top$，用 PBH 判能控。

**解**：特征值 $\lambda=1$（重根）。$\text{rank}[\lambda I-A\ |\ B]=\text{rank}\begin{pmatrix}0&-1&1\\0&0&0\end{pmatrix}=1<2$ → 不可控 ✓（与能控性矩阵判据一致）。几何：特征向量 $(1,0)$ 方向的状态与输入 $B=(1,0)$ 平行——无法独立激励 $x_2$。

**易错点**：左特征向量（$w^\top$ 而非 $w$）；每个特征值都要检查。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 只查一个特征值 | 每个特征值都须满秩 |
| 用右特征向量 | PBH 用左特征向量（行空间） |
| 与能观 PBH 混淆 | 能观版是 $\begin{bmatrix}\lambda I-A\\C\end{bmatrix}$ 列满秩 |

## 4. 与后续知识连接

- [[能控性定义]]：基本概念；
- [[能观性定义]]：对偶 PBH；
- [[Kalman分解]]：不可控模态的分解。

## 5. 检索练习（闭卷）

1. 陈述 PBH 判据；
2. 用 PBH 判定给定系统；
3. 解释左特征向量条件；
4. 与矩阵判据的等价性。

## 6. 通过标准

- 能用 PBH 判能控；
- 能定位不可控模态；
- 能理解与矩阵判据等价。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重判 PBH；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
