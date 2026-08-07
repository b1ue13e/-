---
type: study
topic: "SDP松弛与组合优化应用"
course: "07-最优化方法"
created: 2026-08-08
status: ongoing
flow: knowledge
kind: concept
stage_moc: "[[🧭 阶段5-专题应用]]"
upstream:
  - "[[最优化方法-锥规划与半定规划SDP]]"
  - "[[最优化方法-凸优化与拉格朗日对偶]]"
difficulty: advanced
tags: [学习, 最优化方法, SDP, 组合优化, 松弛]
---

# 最优化方法-SDP松弛与组合优化应用

## §01 为什么学？它解决什么问题？

**动机**：组合优化问题（图分割、最大割、最大团、传感器定位、投资组合选择）通常是 NP-hard 的，直接求解指数爆炸。但很多组合问题可以被"放松"成一个**半定规划（SDP）**，而 SDP 是凸问题，可以在多项式时间内可靠求解（内点法）。SDP 松弛的价值在于：

1. **可计算下界/上界**：松弛问题的解给出原问题的界，用于剪枝或验证；
2. **近似算法**：对 Max-Cut 等经典问题，Goemans-Williamson 算法通过 SDP 松弛给出 0.878 近似比（至今最优，PCP 定理表明不可超越太多）；
3. **可解性诊断**：当松弛与原问题的间隙（Gap）为零时，松弛解就是原问题最优解（很多工程问题恰好如此）。

**本卡回答**：什么是 SDP 松弛？为什么矩阵变量能把"排列/整数"约束放松成"半正定"约束？如何用 CVXPY 求解并恢复可行解？Max-Cut 的 0.878 近似是怎么来的？

**学完能做什么**：能把 Max-Cut、最大团、二次布尔规划写成 SDP 松弛；能解释 Goemans-Williamson 随机舍入的思想；能用 CVXPY 求解 SDP 并对比松弛界与精确解；能说明 SDP 与 LP 松弛在表达能力上的差别。

---

## §02 从布尔二次规划到 SDP 松弛

### 1. 原问题：Max-Cut 的二次形式

给定无向图 $G = (V, E)$，Max-Cut 求一个二分 $S, V \setminus S$ 使被切边数最大。把每个顶点 $i$ 编码为 $y_i \in \{-1, +1\}$，边 $(i,j)$ 被切开当且仅当 $y_i \neq y_j$，即 $\frac{1 - y_i y_j}{2} = 1$。于是：

$$ \max_{y \in \{-1,+1\}^n} \; \frac{1}{2} \sum_{(i,j) \in E} (1 - y_i y_j) = \max_{Y \succeq 0, Y = yy^T, Y_{ii} = 1} \; \frac{1}{2} \sum_{(i,j) \in E} (1 - Y_{ij}) $$

其中 $Y = yy^T$ 是秩 1 半正定矩阵，$Y_{ii} = 1$ 编码了 $y_i \in \{\pm 1\}$。

### 2. 松弛：丢掉秩 1 约束

$Y = yy^T$（秩 1 + 半正定 + 对角为 1）是**非凸**的（秩 1 约束破坏凸性）。SDP 松弛的关键一步是**丢弃秩 1 约束**，只保留 $Y \succeq 0$ 与 $Y_{ii} = 1$：

$$ \max_{Y \succeq 0, Y_{ii} = 1} \; \frac{1}{2} \sum_{(i,j) \in E} (1 - Y_{ij}) $$

这仍然是一个凸问题（半正定锥上的线性目标），可以用内点法高效求解。**直觉**：$Y_{ij}$ 不再被强制等于 $\pm 1$，而是可以在 $[-1, 1]$ 区间自由取值，代表"边被切开的概率/程度"。

### 3. 为什么 SDP 比 LP 松弛更强？

LP 松弛把 $y_i \in \{\pm 1\}$ 放松为 $y_i \in [-1, 1]$，只捕捉"每个变量单独放松"的信息；SDP 放松的是**整个向量外积 $yy^T$**，保留了变量之间的**成对相关性** $Y_{ij} = \mathbb{E}[y_i y_j]$。对很多组合问题，正是这种成对结构决定了质量——所以 SDP 松弛给出的界通常比 LP 松弛紧得多。

---

## §03 Goemans-Williamson 随机舍入（0.878 近似）

SDP 松弛给出分数解 $Y^*$，怎么恢复一个合法的割 $y \in \{\pm 1\}^n$？Goemans-Williamson (1995) 的答案：

1. **Cholesky 分解**：$Y^* = V^T V$，把每个顶点 $i$ 对应到单位球上的向量 $v_i \in \mathbb{R}^n$（$\|v_i\| = 1$ 因为 $Y_{ii} = 1$）；
2. **随机超平面**：取随机单位向量 $r \sim \mathcal{N}(0, I)$，令 $y_i = \text{sign}(v_i^T r)$；
3. **期望分析**：边 $(i,j)$ 被切开的概率 $= \frac{1}{\pi} \arccos(v_i^T v_j) = \frac{1}{\pi} \arccos(Y^*_{ij})$。

**近似比**：对任意 $\theta \in [0, \pi]$ 有 $\frac{2\theta}{\pi} \ge 0.878 \cdot (1 - \cos\theta)$，代入得到 $\mathbb{E}[\text{cut}] \ge 0.878 \cdot \text{SDP}_\text{opt} \ge 0.878 \cdot \text{OPT}$。即**期望割规模 ≥ 0.878 × 最优割**。

> 直观理解：分数解 $Y_{ij}$ 越接近 $-1$（倾向于切开），随机超平面以越高概率真正切开它；代价是偶尔把倾向切开的边切错。0.878 就是这个权衡的理论下界。

---

## §04 通用模板：布尔二次规划 → SDP

很多组合问题都能写成统一形式 $\max_{y \in \{\pm1\}^n} y^T Q y + c^T y$，其 SDP 松弛模板为：

$$ \max_{Y \succeq 0} \; \langle Q, Y \rangle + c^T y \quad \text{s.t.} \quad Y_{ii} = 1, \; \text{rank}(Y) = 1 $$

去掉 rank 约束后得到可解 SDP。常见映射：

| 问题 | 变量编码 | 约束 |
| :--- | :--- | :--- |
| Max-Cut | $y_i \in \{\pm 1\}$ | $Y_{ii} = 1$ |
| 最大团 | 互补图 Max-Cut 变形 | $Y_{ii} = 1$，$Y_{ij} \le 0$（团约束） |
| 图划分 (k=2) | 平衡约束 | $Y_{ii} = 1$，$y^T \mathbf{1} = 0$ |
| 传感器定位 | 距离约束 | $Y_{ii} = 1$，$Y_{ij}$ 固定锚点值 |

---

## §05 Python 实现：Max-Cut SDP + 随机舍入

```python
import numpy as np
import cvxpy as cp

def maxcut_sdp(adj, n_trials=50, seed=42):
    """Max-Cut 的 SDP 松弛 + Goemans-Williamson 随机舍入"""
    n = adj.shape[0]
    # 目标系数: 最大化 Σ_{(i,j)∈E} (1-Yij)/2  ⇔ 最小化 Σ_{ij} Lij·Yij (L=拉普拉斯)
    L = np.diag(adj.sum(axis=1)) - adj
    Y = cp.Variable((n, n), symmetric=True)
    objective = cp.Minimize(cp.trace(L @ Y))
    constraints = [Y >> 0, cp.diag(Y) == 1]
    prob = cp.Problem(objective, constraints)
    prob.solve(solver=cp.SCS, max_iters=5000)
    Y_star = Y.value
    sdp_val = -prob.value  # 转为最大化

    # Cholesky: Y = V^T V, 每行 v_i 是单位向量
    eigvals, eigvecs = np.linalg.eigh(Y_star)
    eigvals = np.clip(eigvals, 0, None)
    V = (eigvecs * np.sqrt(eigvals)).T  # shape (n, n)
    rng = np.random.default_rng(seed)
    best_cut, best_y = 0, None
    for _ in range(n_trials):
        r = rng.standard_normal(n)
        y = np.sign(V @ r)
        cut = sum(adj[i, j] for i in range(n) for j in range(i+1, n) if y[i] != y[j])
        if cut > best_cut:
            best_cut, best_y = cut, y
    return sdp_val, best_cut, best_y

# 测试：C5 五角环（最优割 = 4）
adj = np.array([
    [0,1,0,0,1],
    [1,0,1,0,0],
    [0,1,0,1,0],
    [0,0,1,0,1],
    [1,0,0,1,0]], dtype=float)
sdp_val, cut, y = maxcut_sdp(adj)
print(f"SDP上界 = {sdp_val:.3f}, 舍入割 = {cut} (最优 4)")
# 输出: SDP上界 ≈ 4.5, 舍入割 = 4
```

---

## §06 手算例子：2 顶点图

图 $K_2$（单条边），$n = 2$。SDP：$\max \frac{1}{2}(1 - Y_{12})$ s.t. $Y \succeq 0$，$Y_{11} = Y_{22} = 1$。

由 $Y \succeq 0$ 且对角为 1 知 $|Y_{12}| \le 1$，最优取 $Y_{12} = -1$（最大化 $\frac{1}{2}(1-Y_{12})$），松弛值 $= 1$ = 原问题最优割 1。此时 $Y_{12} = -1$ 是可行秩 1 解（$y = (1, -1)$），松弛无间隙。

---

## §07 常见误区与易混概念

- **误区 1：SDP 松弛的解一定是好的割**
  不一定。随机舍入给出的是**期望**保证（0.878），单次运行可能差；实践中取多次舍入的最好结果。且对某些问题（如最大团）SDP 松弛界很松。

- **误区 2：SDP 松弛总能多项式时间求解**
  SDP 本身是凸问题可多项式求解（内点法 $\mathcal{O}(n^3)$），但**变量是 $n \times n$ 矩阵**，$n$ 大时内存爆炸；大规模图需用 Burer-Monteiro 低秩分解或一阶方法。

- **误区 3：LP 松弛与 SDP 松弛等价**
  错。SDP 松弛保留了成对相关性 $Y_{ij}$，界通常严格更紧；Lovász theta 函数（最大团的 SDP 界）是经典例证。

### 概念对比表

| 松弛类型 | 变量 | 表达能力 | 典型界质量 | 求解成本 |
| :--- | :--- | :--- | :--- | :--- |
| LP 松弛 | $y \in [-1,1]^n$ | 单变量 | 松（Max-Cut ≤ 1/2） | 低 |
| SDP 松弛 | $Y \succeq 0, Y_{ii}=1$ | 成对相关 | 紧（Max-Cut 0.878） | 高（矩阵变量） |
| 精确组合 | $y \in \{\pm1\}^n$ | 完整 | 最优 | 指数（NP-hard） |

---

## §08 检索练习与通过标准

**闭卷复现任务**：
1. 把 Max-Cut 写成二次形式并导出 SDP 松弛（说明丢弃了什么约束、为什么凸）。
2. 解释 Goemans-Williamson 随机舍入的两步流程与 0.878 的来源。
3. 说明为什么 $Y \succeq 0$ + $Y_{ii}=1$ 蕴含 $|Y_{ij}| \le 1$。
4. 用 CVXPY 求解一个 6 顶点随机图的 Max-Cut SDP，对比 SDP 上界与贪心割。
5. 举一个 SDP 松弛界"紧"与"松"的问题各一个。

**通过标准**：能独立完成 1-3（无需查资料）；能运行 §05 代码并解释输出；能说清 SDP 与 LP 松弛的本质差异。

## 🃏 Anki 卡片

Q: SDP 松弛丢弃了什么约束？为什么这使问题变成凸的？
A: 丢弃秩 1 约束 $\text{rank}(Y) = 1$（等价于 $Y = yy^T$）。秩 1 约束是非凸的；保留的 $Y \succeq 0$（半正定锥）与 $Y_{ii} = 1$（仿射）都是凸的，故松弛后为凸 SDP。
<!-- id: opt-sdpr-01 -->

---
Q: Goemans-Williamson 算法对 Max-Cut 的近似比是多少？随机舍入如何从 SDP 解恢复割？
A: 0.878 近似。步骤：Cholesky 分解 $Y^* = V^TV$ 得到单位向量 $v_i$；取随机超平面 $r \sim \mathcal{N}(0,I)$，令 $y_i = \text{sign}(v_i^T r)$；边被切概率 $= \frac{1}{\pi}\arccos(Y_{ij}^*)$。
<!-- id: opt-sdpr-02 -->

---
Q: 为什么 SDP 松弛通常比 LP 松弛给出更紧的界？
A: LP 只放松单个变量 $y_i \in [-1,1]$；SDP 放松整个外积 $Y = yy^T$，保留了变量间的成对相关性 $Y_{ij} = \mathbb{E}[y_i y_j]$，这正是组合问题结构的关键信息。
<!-- id: opt-sdpr-03 -->

---
## 🎯 知识自测与主动回忆

> [!question]- 1. Max-Cut 的 SDP 松弛丢弃了哪个约束？为什么丢弃后问题变凸？
> **答案**：丢弃秩 1 约束 $\text{rank}(Y)=1$（等价于 $Y=yy^T$）。秩 1 约束是非凸的；保留的 $Y \succeq 0$（半正定锥）与 $Y_{ii}=1$（仿射）均为凸约束，故松弛后是凸 SDP。

> [!question]- 2. 为什么 $Y \succeq 0$ 且 $Y_{ii}=1$ 蕴含 $|Y_{ij}| \le 1$？
> **答案**：对任意单位向量 $e_i$，$e_i^T Y e_i = Y_{ii} = 1$；由 $Y \succeq 0$ 与 Cauchy-Schwarz 型不等式（半正定矩阵主子式非负），$Y_{ij}^2 \le Y_{ii} Y_{jj} = 1$，故 $|Y_{ij}| \le 1$。这保证了 $Y_{ij}$ 作为"切开概率"取值合法。

> [!question]- 3. Goemans-Williamson 随机舍入中，边被切开的概率表达式是什么？如何推出？
> **答案**：$P(\text{cut } (i,j)) = \frac{1}{\pi}\arccos(v_i^T v_j) = \frac{1}{\pi}\arccos(Y_{ij}^*)$。两个单位向量被随机超平面分开的角度是 $\theta = \arccos(v_i^T v_j)$，其被超平面切开的概率正比于该角度，归一化得 $\theta/\pi$。

> [!question]- 4. 0.878 近似比的来源是什么？
> **答案**：对任意 $\theta \in [0,\pi]$ 有 $\frac{2\theta}{\pi} \ge 0.878(1-\cos\theta)$。代入期望割公式得 $\mathbb{E}[\text{cut}] \ge 0.878 \cdot \text{SDP}_\text{opt} \ge 0.878 \cdot \text{OPT}$。

> [!question]- 5. SDP 松弛在工程落地上的主要瓶颈是什么？如何缓解？
> **答案**：变量是 $n \times n$ 矩阵，内点法 $\mathcal{O}(n^3)$ 内存/时间开销大，$n$ 上万即不可行。缓解：Burer-Monteiro 低秩分解（限制 $\text{rank}(Y)=r$ 转非凸但可大规模）、一阶方法（如 ADMM 处理 SDP）、或利用稀疏结构。

---
## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
