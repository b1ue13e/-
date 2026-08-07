---
type: study
topic: "锥规划与半定规划SDP"
course: "07-最优化方法"
created: 2026-08-06
status: completed
flow: knowledge
kind: concept
stage_moc: "[[🧭 阶段2-凸分析与最优性条件]]"
upstream:
  - "[[最优化方法-凸优化问题标准形式]]"
  - "[[最优化方法-强对偶与Slater条件]]"
---

# 最优化方法-锥规划与半定规划SDP

## 1. 这个知识点解决什么问题？
> **我们遇到了什么麻烦**：
> LP 只能表达仿射约束（$\mathbf{A}\mathbf{x} \le \mathbf{b}$），但大量真实问题的约束是"向量长度不超过某值"（鲁棒优化、投资组合）、"矩阵必须半正定"（最大割松弛、矩阵补全、控制系统的 LMI）。以前的方法是把它们强行线性化/近似，要么保守、要么失真。因此需要一个**统一且可高效求解的框架**：用"广义不等式 $\preceq_K$"把 LP/SOCP/SDP 装进同一个"锥规划"语言，而锥的结构（凸性）保证了多项式时间可解。

---
## 2. 为什么它重要？它有什么用？
- **连接大图景**：锥规划位于 Boyd 教材 Ch.4.5-4.6，是"最优化方法-凸优化问题标准形式"的收尾；对偶锥直接进入 Ch.5 的对偶理论（广义不等式约束的乘子 $\boldsymbol{\lambda} \succeq_{K^*} \mathbf{0}$），并给 HW04 提供素材。
- **实际应用场景**：最大割的 Goemans-Williamson 0.878 近似、低秩矩阵补全（核范数）、传感器网络定位、SVM 对偶中的核矩阵学习、鲁棒最小二乘——SDP/SOCP 是这些问题的标准求解格式。
- **高频题型/任务**：把问题改写成 SOCP/SDP 标准形；用 Schur 补把二次约束写成 LMI；判定矩阵 PSD；计算简单锥的对偶锥；用 CVXPY 的 `PSD=True` 与 `norm(..., "nuc")` 建模。

---
## 3. 学它之前需要哪些前置知识？

1. **[[最优化方法-凸集与凸函数]]**：凸锥是对凸集的加细（还要求对正数缩放封闭）；广义不等式依赖锥的凸性。
2. **[[最优化方法-凸优化与拉格朗日对偶]]**：对偶锥 $K^*$ 的动机来自对偶函数中乘子 $\boldsymbol{\lambda} \succeq_{K^*} \mathbf{0}$ 的可行性条件；HW04 直接复用。
3. **线性代数**：半正定矩阵、特征值、$\mathrm{tr}$ 内积 $\langle X, Y \rangle = \mathrm{tr}(X^T Y)$、Schur 补。

---
## 4. 用直觉语言解释它
> «"锥"就是一把从原点出发、无限张开的"手电筒光束"：里面任意一点乘上任意正数还在光束里。"对偶锥"则是另一把光束——它与原光束的任意方向夹角都不超过 90°（内积非负）。而"半正定矩阵锥"就是把"非负数"这个概念升级到矩阵：一个矩阵"非负"当且仅当它对任何方向都给出非负的二次型 $v^T X v \ge 0$——就像一只碗，从任何角度压它都不会凹下去。"»
- **直觉类比/几何图像**：$\mathbb{R}^n_+$（非负卦限）是"第一象限"；二阶锥 $\{(x,t): \|x\|_2 \le t\}$ 是"冰淇淋筒"；PSD 锥是"矩阵版第一象限"。
- **为什么很自然**：因为"优化"最关心"序关系"，而锥恰好定义了一种与加法、正数乘法兼容的偏序 $\preceq_K$；把"$\le$"推广到向量与矩阵，LP 的整套理论（对偶、内点法）就自动搬过来了。
- **一句话直觉本质**：**锥规划 = 用"广义不等式 $\preceq_K$"统一 LP（$K=\mathbb{R}^n_+$）、SOCP（$K=$ 二阶锥）、SDP（$K=\mathbb{S}^n_+$），使三者共享同一套凸性与对偶理论。**

---
## 5. 正式定义、核心公式、符号解释
### 1. 最核心定义
- **凸锥**：$K$ 是凸集且 $\theta K \subseteq K,\ \forall \theta \ge 0$（对加法与正数缩放封闭）。
- **对偶锥**：$K^* = \{\mathbf{y} : \mathbf{y}^T\mathbf{x} \ge 0,\ \forall \mathbf{x} \in K\}$。
- **广义不等式**：$\mathbf{x} \preceq_K \mathbf{y} \iff \mathbf{y} - \mathbf{x} \in K$。
- **SDP（标准形）**：$\min_{\mathbf{x}} \mathbf{c}^T\mathbf{x}\ \ \text{s.t.}\ \ F_0 + \sum_{i=1}^n x_i F_i \succeq 0$（LMI 形式），等价矩阵形式 $\min \mathrm{tr}(\mathbf{C}\mathbf{X})$ s.t. $\mathrm{tr}(\mathbf{A}_i\mathbf{X}) = b_i,\ \mathbf{X} \succeq 0$。
- **SOCP**：$\min \mathbf{c}^T\mathbf{x}$ s.t. $\|\mathbf{A}_i\mathbf{x} + \mathbf{b}_i\|_2 \le \mathbf{c}_i^T\mathbf{x} + d_i$。
### 2. 核心公式
自对偶锥（三个最重要例子）：
$$(\mathbb{R}^n_+)^* = \mathbb{R}^n_+, \qquad (\mathcal{Q}^n)^* = \mathcal{Q}^n, \qquad (\mathbb{S}^n_+)^* = \mathbb{S}^n_+$$

其中二阶锥 $\mathcal{Q}^n = \{(\mathbf{x}, t) \in \mathbb{R}^{n} : \|\mathbf{x}\|_2 \le t\}$，$\mathbb{S}^n_+$ 为半正定矩阵锥。双对偶定理（闭凸锥）：$(K^*)^* = K$。

Schur 补（把二次约束写成 LMI 的关键）：
$$\begin{pmatrix} \mathbf{A} & \mathbf{B} \\ \mathbf{B}^T & \mathbf{C} \end{pmatrix} \succeq 0 \iff \mathbf{C} \succ 0 \ \text{且}\ \mathbf{A} - \mathbf{B}\mathbf{C}^{-1}\mathbf{B}^T \succeq 0$$
### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $K$ | 凸锥 | $\mathbb{R}^n$ 子集 | 定义广义不等式 |
| $K^*$ | 对偶锥 | $\mathbb{R}^n$ 子集 | $\mathbf{y}^T\mathbf{x} \ge 0$ |
| $\preceq_K$ | 广义不等式 | 锥诱导的偏序 | $\mathbf{y}-\mathbf{x} \in K$ |
| $\mathbb{S}^n_+$ | 半正定矩阵锥 | $n \times n$ 对称阵 | $\mathbf{v}^T\mathbf{X}\mathbf{v} \ge 0$ |
| $\mathbf{X} \succeq 0$ | PSD | 对称矩阵 | 特征值 $\ge 0$ |

### 4. 常见变体与适用条件
- **变体**：SOCP 可嵌入 SDP（$\|\mathbf{x}\|_2 \le t \iff \begin{pmatrix} t\mathbf{I} & \mathbf{x} \\ \mathbf{x}^T & t \end{pmatrix} \succeq 0$）；LP ⊂ SOCP ⊂ SDP 严格包含。
- **适用条件**：目标与约束能写成关于锥的线性/仿射形式；求解器（SDPT3/MOSEK/SCS/CLARABEL）要求问题可被识别为锥标准形。
- **限制条件**：SDP 规模受限（$n$ 维矩阵变量，内点法每步 $O(n^3)$）；大规模 SDP 通常用一阶方法（SCS）或利用结构（低秩分解）。

---
## 6. 推导思路和思想来源
- **最初困难**：LP 理论漂亮但表达力不足；非线性约束（范数、PSD）各自为政、没有统一算法。
- **直接方法局限**：对每个新约束类型单独设计算法（序列二次规划、罚函数）——无法共享收敛性保证。
- **关键"转念"**：观察 LP 的全部理论只依赖两个事实——可行域是"凸集"、序关系"$\le$"与加法/缩放兼容。把"$\le$"换成任意**闭凸锥**诱导的 $\preceq_K$，Farkas 引理、强对偶、内点法全部照搬——**LP 不是特例，而是锥规划在 $K = \mathbb{R}^n_+$ 的特例**。
- **推导主线与动机**：凸锥定义 → 对偶锥（由分离超平面定理自然导出"乘子必须落在 $K^*$"）→ 广义不等式 → 锥规划标准形 → SOCP/SDP 作为锥规划实例 → 自对偶锥使对偶问题保持同类型。
- **为什么自然得到此结论**：因为"内积非负"是"序"的线性化表达；对偶锥 $K^*$ 就是"所有与 $K$ 夹角不超过 90° 的方向"，它自动出现在对偶可行性条件里。

---
## 7. 例子：基础 → 中等 → 实际应用
### 例子 1：基础例子（可手算）
- **题目**：证明 $K = \{(\mathbf{x}, t) : \|\mathbf{x}\|_2 \le t\}$ 是凸锥，并写出其（自）对偶锥。
- **解题思路与关键步骤**：① 对 $\theta \ge 0$，$\|\theta\mathbf{x}\|_2 = \theta\|\mathbf{x}\|_2 \le \theta t$，缩放封闭；② 对 $(\mathbf{x},t),(\mathbf{y},s)$，由三角不等式 $\|\mathbf{x}+\mathbf{y}\|_2 \le \|\mathbf{x}\|_2 + \|\mathbf{y}\|_2 \le t+s$，加法封闭；③ 对偶：对任意 $(\mathbf{u}, v) \in K^*$ 与 $(\mathbf{x}, t) \in K$ 需 $\mathbf{u}^T\mathbf{x} + vt \ge 0$，取 $\mathbf{x} = -t\mathbf{u}/\|\mathbf{u}\|_2$ 得 $\|\mathbf{u}\|_2 \le v$，故 $K^* = K$。
- **最终答案**：$K$ 是凸锥且自对偶（二阶锥）。
- **易错点**：忘记凸锥还要求"锥"本身是凸集（加法封闭），只验证缩放。
- **🤔 追问**：换成 $K = \{(x_1, x_2) : x_2 \ge |x_1|\}$（二维冰淇淋筒）？——同样自对偶，它是 $\mathcal{Q}^2$ 的旋转形式。
### 例子 2：中等例子（条件判断与多步推理）
- **题目**：求 $x$ 使 $\begin{pmatrix} x & 1 \\ 1 & x \end{pmatrix} \succeq 0$，并解释与 Schur 补的关系。
- **解题思路与完整解答**：对 $2\times 2$ 对称矩阵，PSD $\iff$ 主子式非负：$x \ge 0$ 且 $\det = x^2 - 1 \ge 0$，联立得 $x \ge 1$。**Schur 补视角**：$\mathbf{A}=[x], \mathbf{B}=[1], \mathbf{C}=[x]$，条件等价于 $x > 0$ 且 $x - 1\cdot x^{-1}\cdot 1 = x - \tfrac{1}{x} \ge 0$，即 $x^2 \ge 1$ 且 $x>0$ ⟹ $x \ge 1$。**关键推理**：这正是把二次不等式 $x \ge 1/x$ 线性化为 LMI 的技巧——鲁棒最小二乘、$\|Ax+b\|_2 \le c^Tx+d$ 的 SOCP 化都靠它。
- **易错点**：只检查 $\det \ge 0$ 忘记主元 $x \ge 0$（如 $x = -1$ 时 $\det=0$ 但矩阵非 PSD）。
### 例子 3：实际应用例子（真实场景/代码）
- **实际价值与转化**：最大割问题 $\max \sum w_{ij}(1 - z_i z_j)/2$ 是 NP-hard 的；Goemans-Williamson 把 $z_i z_j$ 松弛为内积 $\langle \mathbf{v}_i, \mathbf{v}_j \rangle$，得 SDP：$\max \mathrm{tr}(\mathbf{W}\mathbf{X})$ s.t. $\mathrm{diag}(\mathbf{X}) = \mathbf{1}, \mathbf{X} \succeq 0$，再随机舍入，保证 0.878 近似比。矩阵补全则用核范数 $\|\mathbf{X}\|_*$（PSD 锥上的凸包）最小化。
```python
import cvxpy as cp, numpy as np
n = 5
np.random.seed(0)
W = np.random.randn(n, n); W = (W + W.T) / 2        # 对称权重
X = cp.Variable((n, n), PSD=True)                    # PSD 变量 = 锥约束
prob = cp.Problem(cp.Maximize(cp.trace(W @ X)),
                  [cp.diag(X) == 1])
prob.solve(solver=cp.CLARABEL)                       # 内点法
L = np.linalg.cholesky(X.value + 1e-8 * np.eye(n))
z = np.sign(L @ np.random.randn(n, 1)).flatten()     # 随机舍入
print("SDP 上界:", prob.value, "| 割值:", 0.25 * (W.sum() - z @ W @ z))
```

---
## 8. 常见误区和易混概念
### 误区 1：以为"SDP 是让矩阵每个元素非负"
- **错误直觉**：$\mathbf{X} \succeq 0$ 就是逐元素 $\ge 0$。
- **为什么错**：PSD 是"所有二次型 $v^T X v \ge 0$"，是**整体**性质；逐元素非负矩阵未必 PSD（如 $\begin{pmatrix} 1 & 2 \\ 2 & 1 \end{pmatrix}$ 行列式为负）。
- **正确理解**：PSD $\iff$ 特征值全非负 $\iff$ 主子式全非负（Sylvester）；逐元素非负叫"非负矩阵"，是完全不同的锥。
### 误区 2：以为"SOCP 与 SDP 可以互相转化，所以等价"
- **错误直觉**：反正都能转，类别的区分没有意义。
- **为什么错**：SOCP ⊂ SDP（单向）；反过来一般不行（SDP 含 SOCP 无法表达的约束，如 $\mathrm{diag}(\mathbf{X})=\mathbf{1}$）。求解器与复杂度不同：SOCP 内点法更便宜。
- **正确理解**：包含链 LP ⊂ SOCP ⊂ SDP 是**严格**的；建模时优先用最"便宜"的类别（能用 LP 就不用 SOCP，能用 SOCP 就不用 SDP）。
### 概念对比表

| 概念 | 核心问题 | 关键区别 | 典型使用场景 |
| :--- | :--- | :--- | :--- |
| LP | 仿射约束 + $\ge 0$ | 锥 $=\mathbb{R}^n_+$ | 运输、调度 |
| SOCP | 范数约束 | 锥 $=$ 二阶锥 | 鲁棒优化、投资组合 |
| SDP | 矩阵 PSD/LMI | 锥 $=\mathbb{S}^n_+$ | 最大割松弛、矩阵补全 |
| 对偶锥 $K^*$ | 与 $K$ 内积非负 | 广义不等式的"乘子域" | 对偶可行性（HW04） |

---
## 9. 相关知识点与 Obsidian 双链建议
### 上游依赖
- [[最优化方法-凸集与凸函数]]：凸锥是凸集的推广，广义不等式依赖锥的凸性。
- [[最优化方法-凸优化与拉格朗日对偶]]：对偶锥 $K^*$ 给出广义不等式约束的乘子可行域（$\boldsymbol{\lambda} \succeq_{K^*} \mathbf{0}$）。
### 下游延伸
- [[最优化方法-CVXPY建模与求解器]]：`PSD=True`、`norm(...,"nuc")`、锥求解器（SCS/CLARABEL/MOSEK）的底层对象就是本笔记的锥。
- [[07-最优化方法-大作业-大规模优化与ADMM并行求解器]]：ADMM 的算子分裂天然处理锥投影（SOC 投影有闭式解）。
### 横向关联
- [[最优化方法-分离超平面与Farkas引理]] ↔ 本知识点：对偶锥 $K^*$ 的定义本质上是"分离超平面垂直于 $K$ 的支撑方向"。
- [[最优化方法-分离超平面与Farkas引理]] ↔ 本知识点：Farkas 引理是锥对偶（$K$ 与 $K^*$ 不相交）在 LP 中的体现。
### 应用场景
- [[🧭 课程作业总索引]]：HW04（对偶锥/灵敏度）与 HW06（最大割/矩阵补全）的核心工具。
- [[项目-组合求解器]]：投资组合的 SOC 约束（$\|\Sigma^{1/2}w\|_2 \le \sigma$）是 SOCP 直接应用。

---
## 10. 闭卷复现任务

合上笔记后，请独立回答以下 10 个问题：
- [ ] 1. 用一句话说清楚锥规划解决什么问题。
- [ ] 2. 用直觉语言解释锥/对偶锥/PSD 锥（«"手电筒光束"»）。
- [ ] 3. 写出对偶锥与广义不等式的定义。
- [ ] 4. 写出三个自对偶锥与 $(K^*)^* = K$。
- [ ] 5. 解释 $\mathbb{S}^n_+$、$\preceq_K$、Schur 补的角色。
- [ ] 6. 讲出"LP 是锥规划特例"的推导主线。
- [ ] 7. 手算 $\begin{pmatrix} x & 1 \\ 1 & x \end{pmatrix} \succeq 0$ 的解。
- [ ] 8. 说出两个误区（逐元素 PSD、SOCP↔SDP 等价）。
- [ ] 9. 说出最大割 SDP 松弛的建模三要素。
- [ ] 10. 说出一个 CVXPY 中 PSD 变量的真实场景。

---
## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 对偶锥定义与自对偶 |
| 2 | 公式运用 | 基础 | 2×2 矩阵 PSD 判定 |
| 3 | 条件判断 | 中等 | SOCP → SDP 转化方向 |
| 4 | 变式/综合 | 中等 | Schur 补把二次约束写为 LMI |
| 5 | 开放/证明/建模 | 较难 | 证明 PSD 锥是凸锥 |

### 题目与解析
#### 1. 写出 $\mathbb{R}^2_+$ 的对偶锥，并说明"自对偶"是什么意思。
> [!question]- 答案解析
> - **答案**：$(\mathbb{R}^2_+)^* = \mathbb{R}^2_+$；自对偶即 $K^* = K$。
> - **解析**：若 $\mathbf{y} = (y_1, y_2)$ 满足对一切 $x_1, x_2 \ge 0$ 有 $y_1 x_1 + y_2 x_2 \ge 0$，取 $\mathbf{x} = \mathbf{e}_1, \mathbf{e}_2$ 得 $y_1, y_2 \ge 0$，故 $K^* = K$。二阶锥与 PSD 锥同样自对偶，这使对偶问题保持同类型。
> - **易错原因**：忘记对偶锥要求"对所有 $\mathbf{x} \in K$"成立，只检验个别方向。
> - **Obsidian 标签建议**：`#自测题/基础`
#### 2. 判定 $\mathbf{X} = \begin{pmatrix} 1 & 2 \\ 2 & 1 \end{pmatrix}$ 是否 PSD。
> [!question]- 答案解析
> - **答案**：不是。
> - **解析**：$\det = 1 - 4 = -3 < 0$，存在负特征值（特征值为 $3, -1$）；Sylvester 判据要求所有主子式非负。
> - **易错原因**：看到对角元为正就下结论；PSD 是整体性质（误区 1）。
> - **对应误区**：误区 1（逐元素非负）。
#### 3. 下面哪句正确：A. SOCP 可化为 SDP；B. SDP 可化为 SOCP；C. 两者互相可化。
> [!question]- 答案解析
> - **答案**：A 正确（SOCP ⊂ SDP，单向包含）。
> - **解析**：$\|\mathbf{x}\|_2 \le t \iff \begin{pmatrix} t\mathbf{I} & \mathbf{x} \\ \mathbf{x}^T & t \end{pmatrix} \succeq 0$；反向不成立（如 $\mathrm{diag}(\mathbf{X}) = \mathbf{1}$ 约束无法用 SOC 表达）。
> - **易错原因**：把"可嵌入"误当"等价"（误区 2）。
#### 4. 把二次约束 $\mathbf{x}^T\mathbf{P}\mathbf{x} + 2\mathbf{q}^T\mathbf{x} + r \le 0$（$\mathbf{P} \succ 0$）写成 LMI。
> [!question]- 答案解析
> - **答案**：$\begin{pmatrix} \mathbf{I} & \mathbf{P}^{1/2}\mathbf{x} \\ (\mathbf{P}^{1/2}\mathbf{x})^T & -\mathbf{q}^T\mathbf{x} - r \end{pmatrix} \succeq 0$（等价形式：令 $\mathbf{y}=\mathbf{P}^{1/2}\mathbf{x}$ 后 $\begin{pmatrix} \mathbf{I} & \mathbf{y} \\ \mathbf{y}^T & -\mathbf{q}^T\mathbf{x}-r \end{pmatrix} \succeq 0$）。
> - **解析**：由 Schur 补，该 LMI 等价于 $-\mathbf{q}^T\mathbf{x} - r \ge \mathbf{x}^T\mathbf{P}\mathbf{x}$，正是原约束。这是 QCQP → SDP/SOCP 标准化的核心步骤。
> - **易错原因**：符号方向写反（Schur 补要求右下角标量块为正才有 $\mathbf{A} - \mathbf{B}\mathbf{C}^{-1}\mathbf{B}^T \succeq 0$ 的等价）。
#### 5. 证明半正定矩阵锥 $\mathbb{S}^n_+$ 是凸锥。
> [!question]- 答案解析
> - **答案**：对 $\mathbf{X}, \mathbf{Y} \succeq 0$ 与 $\theta \in [0,1]$，任意 $\mathbf{v}$：$\mathbf{v}^T(\theta\mathbf{X} + (1-\theta)\mathbf{Y})\mathbf{v} = \theta \mathbf{v}^T\mathbf{X}\mathbf{v} + (1-\theta)\mathbf{v}^T\mathbf{Y}\mathbf{v} \ge 0$；缩放封闭同理。
> - **解析**：凸性来自"PSD 是无穷多个线性不等式 $v^T X v \ge 0$ 的交集"，而线性不等式的交集必为凸集——这同时解释了为何 SDP 可行域是凸的、内点法适用。
> - **易错原因**：试图用特征值证明而绕远路；线性不等式视角一步到位。
> - **Obsidian 标签建议**：`#自测题/较难`

---
## 12. 学完后可以完成

完成本卡后，你能：把矩阵变量约束写成 PSD 广义不等式；判断问题属于 LP/SOCP/SDP 哪一层；理解 SDP 松弛在最大割、矩阵补全中的作用；在 CVXPY 中用 PSD=True 与锥约束建模。以下作业直接验收本卡知识：

```dataview
LIST
FROM "03-Projects/07-最优化方法"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

---

## 🃏 Anki 卡片

Q: 半定规划（SDP）的标准形式？与 SOCP/LP 的关系？
A: $\min \mathrm{tr}(CX)$ s.t. $\mathrm{tr}(A_i X) = b_i,\ X \succeq 0$。SDP 以半定锥为约束，LP ⊂ SOCP ⊂ SDP，是凸优化中最广的多项式可解类之一。
<!-- id: opt-sdp-01 -->

---
Q: 为什么最大割问题可以用 SDP 松弛求解？
A: 最大割是 NP-hard 的组合问题；将其整数变量松弛为 PSD 矩阵变量后得到 SDP（Goemans-Williamson），最优值给出割值的上界，随机舍入保证 0.878 近似比。
<!-- id: opt-sdp-02 -->

---
Q: CVXPY 中如何声明半定变量与锥约束？
A: $X = cp.Variable((n,n), PSD=True)$ 声明 PSD 变量；约束可直接写 $X >> 0$ 或 $X >> np.zeros((n,n))$（广义不等式），求解器（SCS/CLARABEL/MOSEK）内部转锥标准形。
<!-- id: opt-sdp-03 -->
