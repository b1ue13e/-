---
title: "马尔可夫随机场 MRF (Markov Random Field)"
course: "14-概率图模型"
tags:
  - 概率图模型
  - MRF
  - 马尔可夫随机场
  - 无向图
  - 吉布斯分布
  - Hammersley-Clifford定理
type: knowledge_card
status: completed
created: 2026-08-01
---

# 马尔可夫随机场 MRF (Markov Random Field)

## 1. 马尔可夫随机场 MRF 的定义与无向图条件独立性

**马尔可夫随机场 MRF (Markov Random Field)** 的核心定义 is：一种用无向图 $G = (V, E)$ 表示变量间概率依存关系的**无向概率图模型 (Undirected Graphical Model)**。由 Ising 等人最初在统计物理学中提出，并由 Kindermann, Snell 等人引入概率推理。

**三大无向图条件独立性 (Conditional Independencies)**：
1. **成对马尔可夫性 (Pairwise Markovity)**：任意两个没有边直接相连的节点 $u, v$，在给定所有其他节点观测的条件下条件独立：$P(X_u, X_v \mid X_{V \setminus \{u,v\}}) = P(X_u \mid X_{\dots}) P(X_v \mid X_{\dots})$；
2. **局部马尔可夫性 (Local Markovity)**：节点 $v$ 在给定其邻居节点集合 $N(v)$ 的条件下，与图中其余所有节点条件独立；
3. **全局马尔可夫性 (Global Markovity)**：节点集 $A$ 和 $B$ 被节点集 $C$ 完全分隔（阻断），则在给定 $C$ 的条件下 $A \perp B \mid C$。

---

## 2. Hammersley-Clifford 定理与吉布斯分布形式化推导

**最大团 (Maximal Clique) 因子化推导**：
设无向图 $G$ 的最大团集合为 $\mathcal{C}$，每个团 $C \in \mathcal{C}$ 对应一个非负势函数 (Potential Function) $\psi_C(\mathbf{X}_C)$。

**Hammersley-Clifford 定理 (1971)**：
当联合概率分布 $P(\mathbf{X}) > 0$ 严格正时，分布 $P(\mathbf{X})$ 满足马尔可夫随机场 MRF 的局部独立性的充要条件是：$P(\mathbf{X})$ 可以表示为定义在最大团上的势函数的乘积形式（即**吉布斯分布 Gibbs Distribution**）：

$$P(\mathbf{X}) = \frac{1}{Z} \prod_{C \in \mathcal{C}} \psi_C(\mathbf{X}_C)$$

其中归一化常数（配分函数 Partition Function）$Z$ 形式为：
$$Z = \sum_{\mathbf{X}} \prod_{C \in \mathcal{C}} \psi_C(\mathbf{X}_C)$$

**能量函数 (Energy Function) 形式表达**：
引入势函数的指数能量形式 $\psi_C(\mathbf{X}_C) = \exp(-E_C(\mathbf{X}_C))$，则联合分布转化为玻尔兹曼分布：

$$P(\mathbf{X}) = \frac{1}{Z} \exp\left( -\sum_{C \in \mathcal{C}} E_C(\mathbf{X}_C) 
ight) = \frac{1}{Z} \exp(-E_{\text{total}}(\mathbf{X}))$$

**因此**，最大化联合概率 $P(\mathbf{X})$ 完全等价于最小化系统的总能量 $E_{\text{total}}(\mathbf{X})$，这一推导奠定了图像去噪（Ising 模型）与 CRF 的优化根基。

---

## 3. 马尔可夫随机场 MRF (无向图) 与 贝叶斯网络 (有向图) 的对比

| 维度 | 马尔可夫随机场 MRF (无向图) | 贝叶斯网络 (有向图) |
|:---|:---|:---|
| **边关系** | **无向边** (对称相互关联) | **有向无环边** (因果/因果因关系) |
| **因子化基础** | **最大团势函数乘积** $\frac{1}{Z}\prod \psi_C$ | **条件概率乘积** $\prod P(X_i \mid \text{Pa}(X_i))$ |
| **配分函数 $Z$** | **非局部全图求和 $Z$** (计算极其昂贵) | **$Z=1$ 天然归一化** (无需配分函数) |
| **独立性判定** | 全局图阻断 / 分隔集 | d-分隔 (d-Separation) 规则 |
| **应用场景** | 图像分割、物理点阵、CRF | 专家诊断、因果推断、LDA |

**局限（误区与反例）**：马尔可夫随机场 MRF 的归一化常数 $Z$ 需要对全状态空间所有组合求和，对于稍微复杂的高维无向图，$Z$ 的精准计算属于 NP-Hard 困难问题；实践中必须借助 MCMC 采样或变分推断 (Variational Inference) 进行近似。

关联知识点推荐：[[隐马尔可夫模型HMM]]、[[贝叶斯网络]]、[[凸优化与拉格朗日对偶]]、[[红黑树]]。

---

## 4. Python 手写网格 MRF (Ising 模型) 能量与配分函数自测断言

```python
import numpy as np

def mrf_ising_energy(states: np.ndarray, J: float = 1.0, h: float = 0.0) -> float:
    """
    计算 2D 网格 MRF Ising 模型总能量: E(x) = -J * sum(x_i * x_j) - h * sum(x_i)
    states: 2D array, 取值 in {-1, +1}
    """
    H, W = states.shape
    energy = 0.0

    # 1. 相互作用势能 (相邻节点)
    for r in range(H):
        for c in range(W):
            s = states[r, c]
            if r + 1 < H:
                energy -= J * s * states[r + 1, c]
            if c + 1 < W:
                energy -= J * s * states[r, c + 1]

    # 2. 外场势能
    energy -= h * np.sum(states)
    return float(energy)

if __name__ == "__main__":
    # 2x2 网格同向配置 (全 +1)
    states_same = np.array([[1, 1], [1, 1]])
    e_same = mrf_ising_energy(states_same, J=1.0, h=0.0)
    # 相邻边共有 4 条 (2水平+2垂直), 能量 = -1.0 * 4 = -4.0
    assert abs(e_same - (-4.0)) < 1e-6, f"同向能量错误: {e_same}"

    # 2x2 网格相消配置 (棋盘交叉)
    states_diff = np.array([[1, -1], [-1, 1]])
    e_diff = mrf_ising_energy(states_diff, J=1.0, h=0.0)
    # 相邻边均异号, 能量 = +4.0
    assert abs(e_diff - 4.0) < 1e-6

    # 自测验证: 同向吉布斯概率应远大于异向概率
    assert np.exp(-e_same) > np.exp(-e_diff), "低能量态具备更高的吉布斯分布概率"

    print(f"马尔可夫随机场 MRF Ising 模型同向能量 = {e_same:.1f}, 棋盘相消能量 = {e_diff:.1f}")
    print("马尔可夫随机场 MRF 单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Hammersley, J. M., & Clifford, P. (1971). Markov fields on finite graphs and lattices. *Unpublished manuscript*. URL: https://www.stat.berkeley.edu/~stat260/clifford.pdf
- Kindermann, R., & Snell, J. L. (1980). *Markov Random Fields and Their Applications*. American Mathematical Society. ISBN: 978-0821850015. DOI: https://doi.org/10.1090/conm/001
- Murphy, K. P. (2012). *Machine Learning: A Probabilistic Perspective*. MIT Press. Chapter 19 (Undirected Graphical Models / MRFs). ISBN: 978-0262018029. URL: https://probml.github.io/pml-book/book1.html
