---
type: study
topic: "二次规划与CVXPY"
course: "07-最优化方法"
created: 2026-08-06
status: completed
flow: knowledge
kind: concept
stage_moc: "[[🧭 阶段1-数学基础]]"
difficulty: beginner
concept: ["二次规划", "凸优化", "CVXPY"]
prerequisites: ["线性规划", "正定矩阵"]
related: ["最优化方法-二次型与特征值变分性", "最优化方法-CVXPY建模与求解器", "最优化方法-凸优化问题标准形式"]
upstream:
  - "[[最优化方法-多元梯度与海森矩阵]]"
  - "[[最优化方法-二次型与特征值变分性]]"
tags: [学习, 07-最优化方法, 二次规划, QP, CVXPY]
---

# 最优化方法-二次规划与CVXPY

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：线性规划（LP）很好解，但目标函数只能是线性的。现实中大量成本或风险是**二次**的——方差、平方误差、范数平方。当约束仍是线性、目标变成开口向上的"碗"（凸二次函数）时，就得到**二次规划（QP）**。我们需要：① 一种标准数学语言写清 QP；② 一个可靠工具把它扔给求解器，并保证得到全局最优。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：QP 是从线性优化跨向非线性凸优化的第一步，也是 SQP、内点法等许多高级算法内部反复求解的子问题。
- **实际应用场景**：
  - **金融**：马科维茨组合优化，最小化方差 $w^T \Sigma w$（二次），约束收益达标、权重和为 1（线性）。
  - **机器学习**：硬间隔 SVM 原问题，最小化 $\|w\|^2$（二次），约束样本分类正确（线性）。
  - **控制**：LQR、MPC 的每步子问题都是 QP（见 15-控制与机器人学 的 MPC 路径）。
- **高频题型/任务**：把业务问题抽象成标准形式 $\min \frac12 x^T P x + q^T x$，用 CVXPY 5-10 行代码求解。

---

## 3. 学它之前需要哪些前置知识？

1. **[[最优化方法-二次型与特征值变分性]]**：矩阵 $P \succeq 0$ 保证二次项凸；正定性判定。
2. **[[最优化方法-多元梯度与海森矩阵]]**：QP 目标的海森矩阵 $\nabla^2(\frac12 x^T P x) = P$。
3. **基础线性规划**：约束集 $\{x : Gx \le h, Ax = b\}$ 是多面体。

---

## 4. 用直觉语言解释它

> «在一个由几面平直围墙围成的院子里，找那个抛物面碗的最低点»

- **直觉类比/几何图像**：线性约束像在地上画的直线围成的多边形院子（可行域）；目标函数是抛物面大碗。你要找的是院子内部或边界上碗最低的点。由于碗是凸的、院子是凸的，局部最低就是全局最低。
- **一句话直觉本质**：在多面体（线性约束）上极小化凸二次函数。

---

## 5. 正式定义、核心公式、符号解释

### 1. 标准数学形式

$$
\begin{aligned}
\min_x \quad & \frac{1}{2} x^T P x + q^T x \\
\text{s.t.} \quad & G x \le h \\
& A x = b
\end{aligned}
$$

$P$ 必须对称半正定（$P \succeq 0$），否则问题非凸、无法保证全局最优。

### 2. 符号说明表

| 符号 | 含义 | 备注 |
| :--- | :--- | :--- |
| $x$ | 决策变量 | $n \times 1$ |
| $P$ | 二次项系数矩阵 | 对称半正定 $P \succeq 0$ |
| $q$ | 一次项系数 | $n \times 1$ |
| $G, h$ | 不等式约束 | $Gx \le h$ |
| $A, b$ | 等式约束 | $Ax = b$ |

### 3. 与 LP / QCQP 的关系

- $P = 0$ 时退化为 LP；
- 约束含二次不等式 $x^T P_i x + q_i^T x + r_i \le 0$ 时是 QCQP（凸时仍可解）。

---

## 6. 推导思路和思想来源（CVXPY 的 DCP 规则）

- **最初困难**：目标写成 $x^3$ 或 $P$ 非正定时，求解器无法保证全局最优。即便数学上正确的写法，通用矩阵乘法 `x.T @ P @ x` 也无法被自动判定为凸。
- **关键"转念"**：CVXPY 引入 **DCP（Disciplined Convex Programming，规范凸编程）**——把问题限制在一组可证明保持凸性的原子函数与组合规则内。只要代码通过 DCP 检查，CVXPY 保证能转成标准凸问题并求全局最优。二次型必须用原子函数 `cp.quad_form(x, P)` 显式声明，`P` 需可验证半正定。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：CVXPY 实现马科维茨组合优化

3 个资产，预期收益 $\mu$、协方差 $\Sigma$；要求 $w \ge 0$、$\sum w_i = 1$、收益 $\ge R$，最小化方差：

```python
import cvxpy as cp
import numpy as np

mu = np.array([0.10, 0.12, 0.15])
Sigma = np.array([[0.1, 0.02, 0.01],
                  [0.02, 0.2, 0.03],
                  [0.01, 0.03, 0.3]])
R = 0.12

w = cp.Variable(3)
objective = cp.Minimize(cp.quad_form(w, Sigma))
constraints = [w >= 0, cp.sum(w) == 1, mu @ w >= R]

prob = cp.Problem(objective, constraints)
prob.solve()
print("最优权重:", w.value, "方差:", prob.value)
```

### 例子 2：等式约束 QP 的解析解（KKT 系统）

无不等式约束时，KKT 给出线性方程组：

$$ \begin{bmatrix} P & A^T \\ A & 0 \end{bmatrix} \begin{bmatrix} x^* \\ \nu^* \end{bmatrix} = \begin{bmatrix} -q \\ b \end{bmatrix} $$

KKT 矩阵可逆时直接解出 $x^*$ 与对偶变量 $\nu^*$——这是二次规划"解析可解"的一面，也是 SQP 每步子问题的解法。

---

## 8. 常见误区与相近概念对比

- **误区 1：CVXPY 里直接写 `w.T @ Sigma @ w`。** 数学上正确但过不了 DCP 检查（无法确认凸性）。必须用原子函数 `cp.quad_form(w, Sigma)`。
- **误区 2：$P$ 有微小负特征值仍当凸问题提交。** 数值误差（如 $-10^{-9}$）会使 CVXPY 拒绝识别为凸。先对称化 $Q = (Q+Q^T)/2$，再特征值截断或加 $\epsilon I$ 扰动。
- **误区 3：把 QP 与 QCQP 混为一谈。** QP 约束线性、目标二次；QCQP 允许约束本身二次（$x^T P_i x \le 1$），可解性要求所有 $P_i \succeq 0$。

| 模型 | 目标 | 约束 | 可解性 |
| :--- | :--- | :--- | :--- |
| LP | 线性 | 线性 | 多项式时间 |
| QP | 二次（$P \succeq 0$） | 线性 | 多项式时间 |
| QCQP | 二次（$P \succeq 0$） | 二次 | 凸时多项式，否则 NP-hard |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[最优化方法-二次型与特征值变分性]]：$P \succeq 0$ 判据与正定矩阵。
- [[最优化方法-多元梯度与海森矩阵]]：QP 梯度 $Px + q$、海森 $P$。
### 下游延伸
- [[最优化方法-CVXPY建模与求解器]]：DCP 规则、求解器选型。
- [[最优化方法-凸优化问题标准形式]]：QP 是 LP/SOCP/SDP 家族一员。
- [[最优化方法-凸优化与拉格朗日对偶]]：QP 的 KKT 与对偶理论。
### 横向关联
- 15-控制与机器人学：MPC 每步 QP 求解。

---

## 10. 检索练习与闭卷通过标准

- [ ] 默写 QP 标准形式并解释 $P \succeq 0$ 的必要性。
- [ ] 写一个马科维茨模型的 CVXPY 完整求解代码。
- [ ] 推导等式约束 QP 的 KKT 线性方程组。
- [ ] 解释为什么 `cp.quad_form` 而非 `x.T @ P @ x`。
- [ ] 说明 QP 在 SQP/MPC 内部如何作为子问题出现。

通过标准：五项闭卷全部正确；任一卡壳回到对应前置卡补学。

---

## 11. 自测题

> [!question]- 1.（定义复述）QP 的标准形式？$P$ 需要满足什么条件、为什么？
> **答案**：$\min \frac12 x^T P x + q^T x$ s.t. $Gx \le h, Ax = b$。$P \succeq 0$ 保证目标凸，局部最优即全局最优；否则问题 NP-hard 级别。

> [!question]- 2.（应用）马科维茨模型为什么是 QP？
> **答案**：目标 $\min w^T \Sigma w$（$\Sigma$ 半正定）为二次凸函数，约束 $1^T w = 1$、$w \ge 0$、$\mu^T w \ge R$ 均为线性，符合 QP 标准形式。

> [!question]- 3.（反例）$P$ 存在负特征值时 QP 会怎样？
> **答案**：目标在对应特征向量方向上无下界或非凸，局部极小不再全局；求解器无法保证收敛到全局最优。

> [!question]- 4.（条件变式）$P = 0$ 时 QP 退化成什么？约束含二次不等式时又是什么？
> **答案**：$P=0$ 退化为 LP；约束含 $x^T P_i x \le 1$（$P_i \succeq 0$）时为凸 QCQP。

> [!question]- 5.（推导）等式约束 QP 的解析解怎么求？
> **答案**：KKT 条件导出 $\begin{bmatrix} P & A^T \\ A & 0 \end{bmatrix}\begin{bmatrix} x^* \\ \nu^* \end{bmatrix} = \begin{bmatrix} -q \\ b \end{bmatrix}$，矩阵可逆时解出 $x^*$ 与乘子 $\nu^*$。

---

## 12. 学完后可以完成

完成本卡后，你能：识别并写出实际问题的 QP 标准形式；用 CVXPY 建模求解凸 QP；推导等式约束 QP 的 KKT 解析解；为 SQP、MPC 等后续算法提供 QP 子问题求解能力。以下作业直接验收本卡知识：

```dataview
LIST
FROM "03-Projects/07-最优化方法"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

---

## 🃏 Anki 卡片

Q: 标准二次规划（QP）的数学形式与可解条件？
A: $\min_x \frac12 x^T P x + q^T x$ s.t. $Gx \le h, Ax = b$。$P$ 对称半正定（$P \succeq 0$）保证凸性，可多项式时间全局求解。
<!-- id: opt-qp-01 -->

---
Q: 为什么 CVXPY 必须用 `cp.quad_form(x, P)` 而非 `x.T @ P @ x`？
A: DCP 规则无法从通用矩阵乘法推断二次型的凸性；`quad_form` 显式声明二次原子且要求 $P \succeq 0$ 可验证，通过检查即保证凸。
<!-- id: opt-qp-02 -->

---
Q: 等式约束 QP 的解析解来自什么？写出 KKT 系统。
A: KKT 条件：$\begin{bmatrix} P & A^T \\ A & 0 \end{bmatrix}\begin{bmatrix} x^* \\ \nu^* \end{bmatrix} = \begin{bmatrix} -q \\ b \end{bmatrix}$；KKT 矩阵可逆时直接求解。
<!-- id: opt-qp-03 -->
