---
type: study
topic: "ARE"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段5-状态空间与现代控制]]"
flow: knowledge
kind: derivation
concept: ["Riccati方程", "ARE", "LQR"]
prerequisites: ["LQR代价函数", "Lyapunov稳定"]
related: ["LQR增益", "LQR稳定性"]
upstream: ["[[LQR代价函数]]"]
source: "Modern Control Engineering (Ogata) Ch.10; 最优控制经典"
tags: [学习, 控制与机器人学, LQR]
---

# ARE（代数 Riccati 方程）

## 0. 为什么学它

LQR 的最优解由**代数 Riccati 方程（ARE）**给出——它不是"试出来的增益"，而是矩阵方程的解。理解 ARE 才真正理解 LQR 的数学内核（也是 MPC 终端代价的来源）。

## 1. 核心方程

**连续 ARE**（$Q\succeq0,R\succ0$）：

$$A^\top P+PA-PBR^{-1}B^\top P+Q=0.$$

**解的性质**：存在唯一对称正定解 $P$（$(A,B)$ 能控时）。

**最优增益与代价**：$K=R^{-1}B^\top P$；最优代价 $J^*=x_0^\top P x_0$。

**离散 ARE（DARE）**：$P=A^\top PA-A^\top PB(R+B^\top PB)^{-1}B^\top PA+Q$。

## 2. 最小可手算例子

**题目**：$A=0,\ B=1,\ Q=1,\ R=1$，解 ARE。

**解**：$0\cdot P+P\cdot0-P\cdot1^{-1}\cdot1\cdot P+1=0\Rightarrow-P^2+1=0\Rightarrow P=1$（正定）。$K=R^{-1}B^\top P=1$。闭环 $A-BK=-1$ 稳定 ✓。

**易错点**：$P$ 正定选取；DARE 与连续形式勿混；数值求解用 `scipy.linalg.solve_continuous_are`。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| ARE 有多个解随便取 | 取**对称正定**解才是最优 |
| 手解高维 ARE | 高维用数值求解器 |
| 忽略能控前提 | $(A,B)$ 能控保证正定解存在 |

## 4. 与后续知识连接

- [[LQR增益]]：由 $P$ 得 $K$；
- [[LQR稳定性]]：$P$ 同时证稳定；
- [[Lyapunov稳定]]：ARE 与 Lyapunov 方程联系；
- [[终端代价]]：MPC 用 ARE 解作终端权。

## 5. 检索练习（闭卷）

1. 写出连续/离散 ARE；
2. 解一维 ARE；
3. 说明 $P$ 与 $K$ 的关系；
4. 正定解的存在条件。

## 6. 通过标准

- 能写 ARE；
- 能解简单情形；
- 能理解与 Lyapunov/MPC 的联系。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重解 ARE；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
