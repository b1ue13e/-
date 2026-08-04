---
title: "隐马尔可夫模型 HMM (Hidden Markov Model)"
course: "14-概率图模型"
tags:
  - 概率图模型
  - HMM
  - 隐马尔可夫模型
  - 维特比算法
  - 前后向算法
  - Baum-Welch
type: knowledge_card
status: completed
created: 2026-08-01
---

# 隐马尔可夫模型 HMM (Hidden Markov Model)

## 1. 隐马尔可夫模型 HMM 的定义与三大基本问题

**隐马尔可夫模型 HMM (Hidden Markov Model)** 的核心定义是：一种关于时序的生成式双重随机过程概率图模型，由不可观测的隐状态序列（满足一阶马尔可夫链）和可观测的观察序列（状态独立假设）共同构成。由 Baum, Petrie 等人于 1960 年代提出。

**基本性质与三大基本问题**：
隐马尔可夫模型 HMM 由五元组 $\lambda = (S, V, A, B, \pi)$ 参数化表达：
1. **评估概率问题 (Evaluation)**：已知模型 $\lambda$ 与观察序列 $O$，高效计算概率 $P(O|\lambda)$ —— 采用**前向-后向算法 (Forward-Backward Algorithm)**，$O(TN^2)$ 复杂度；
2. **解码问题 (Decoding)**：已知模型 $\lambda$ 与观察序列 $O$，寻找可能性最大的隐状态序列 $Q^*$ —— 采用**维特比算法 (Viterbi Algorithm)** 动态规划求解；
3. **学习问题 (Learning)**：仅已知观察序列 $O$，估计模型参数 $\lambda$ —— 采用无监督 **Baum-Welch 算法 (EM 算法)**。

---

## 2. 维特比算法 (Viterbi) 形式化推导与动态规划递推

**模型假设**：
- 隐状态集合 $Q = \{q_1, \dots, q_N\}$，观察集合 $V = \{v_1, \dots, v_M\}$；
- 状态转移概率矩阵 $A = [a_{ij}]_{N \times N}$，观察概率矩阵 $B = [b_{j}(k)]_{N \times M}$，初始状态分布 $\pi$。

**推导过程（维特比状态变量 $\delta_t(i)$ 与 路径回溯 $\psi_t(i)$）**：
1. 定义时刻 $t$ 状态为 $i$ 的最可能路径最大概率值：
$$\delta_t(i) = \max_{q_1, \dots, q_{t-1}} P(q_1, \dots, q_{t-1}, q_t = i, O_1, \dots, O_t \mid \lambda)$$
2. **初始化 ($t=1$)**：
$$\delta_1(i) = \pi_i b_i(O_1), \quad \psi_1(i) = 0 \quad (i=1,\dots,N)$$
3. **递推 ($t=2,\dots,T$)**：根据马尔可夫性与状态独立性：
$$\delta_t(j) = \max_{1 \le i \le N} \left[ \delta_{t-1}(i) a_{ij} 
ight] \cdot b_j(O_t)$$
$$\psi_t(j) = \arg\max_{1 \le i \le N} \left[ \delta_{t-1}(i) a_{ij} 
ight]$$
4. **终止与路径回溯**：
$$P^* = \max_{1 \le i \le N} \delta_T(i), \quad q_T^* = \arg\max_{1 \le i \le N} \delta_T(i)$$
$$q_t^* = \psi_{t+1}(q_{t+1}^*) \quad (t = T-1, T-2, \dots, 1)$$
5. **因此**，维特比算法利用局部最优路径推导将全路径穷举复杂度从 $O(N^T)$ 骤降至 $O(T N^2)$。

---

## 3. 隐马尔可夫模型 HMM 与 CRF / 朴素贝叶斯的对比

| 维度 | 隐马尔可夫模型 HMM | 条件随机场 CRF | 朴素贝叶斯 Naive Bayes |
|:---|:---|:---|:---|
| **模型类型** | **生成式模型 (Generative)** | 条件判别式模型 (Discriminative) | 生成式模型 (Generative) |
| **拓扑结构** | **有向图 (Directed PGM)** | 无向图 (Undirected PGM) | 有向星形图 |
| **时序依赖** | **一阶马尔可夫链 (序列级)** | 全局无向条件团 | 静态独立 (非时序) |
| **特征工程** | 受限于观测独立假设 | 可任意叠加重叠全局上下文特征 | 独立特征叠加 |
| **解码求解** | **维特比算法 Viterbi** | 维特比算法 Viterbi | 最大后验 MAP |

**局限（误区与反例）**：隐马尔可夫模型 HMM 假设 $O_t$ 仅依赖当前隐状态 $q_t$（观测独立假设），这导致 HMM 无法利用文本中上下文的关联特征（如前后的词性）；这一局限促使了线性链 CRF 的诞生。

关联知识点推荐：[[马尔可夫随机场MRF]]、[[贝叶斯网络]]、[[维特比算法]]、[[二分搜索]]。

---

## 4. Python 手写 HMM 维特比算法解码与概率校验自测断言

```python
import numpy as np

def viterbi_decode(obs: list, pi: np.ndarray, A: np.ndarray, B: np.ndarray) -> tuple:
    """
    手动实现 HMM 维特比算法 (Viterbi Algorithm)
    obs: 观察序列列表 [0, 1, ...]
    pi: (N,) 初始概率
    A: (N, N) 状态转移矩阵
    B: (N, M) 观察发射概率矩阵
    """
    N = len(pi)
    T = len(obs)
    delta = np.zeros((T, N))
    psi = np.zeros((T, N), dtype=int)

    # 1. 初始化
    delta[0] = pi * B[:, obs[0]]

    # 2. 递推
    for t in range(1, T):
        for j in range(N):
            prob = delta[t-1] * A[:, j]
            psi[t, j] = int(np.argmax(prob))
            delta[t, j] = np.max(prob) * B[j, obs[t]]

    # 3. 回溯
    best_path = np.zeros(T, dtype=int)
    best_path[T-1] = int(np.argmax(delta[T-1]))
    best_prob = float(np.max(delta[T-1]))

    for t in range(T-2, -1, -1):
        best_path[t] = psi[t+1, best_path[t+1]]

    return best_path.tolist(), best_prob

if __name__ == "__main__":
    # 经典天气/穿衣模型: 状态 {0:晴, 1:雨}, 观察 {0:T恤, 1:外套}
    pi = np.array([0.6, 0.4])
    A = np.array([[0.7, 0.3], [0.4, 0.6]])
    B = np.array([[0.8, 0.2], [0.2, 0.8]])

    # 连续两天观测到 [T恤(0), 外套(1)]
    obs = [0, 1]
    best_path, max_p = viterbi_decode(obs, pi, A, B)

    # 自测验证 1: 路径为 [0, 1] (第一天晴天穿T恤，第二天雨天穿外套)
    assert best_path == [0, 1], f"维特比解码路径异常: {best_path}"

    # 自测验证 2: 最大概率值 > 0
    assert max_p > 0.0

    # 自测验证 3: 观察概率归一化断言
    assert np.allclose(B.sum(axis=1), 1.0), "发射矩阵每行和必须为 1"

    print(f"隐马尔可夫模型 HMM 维特比解码最可能隐状态路径: {best_path}, 最大概率 = {max_p:.4f}")
    print("隐马尔可夫模型 HMM 单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Rabiner, L. R. (1989). A tutorial on hidden Markov models and selected applications in speech recognition. *Proceedings of the IEEE*, 77(2), 257-286. DOI: https://doi.org/10.1109/5.18626 URL: https://ece.ucsb.edu/Faculty/Rabiner/ece259/Reprints/tutorial%20on%20hmm%20and%20html/tutorial.pdf
- Koller, D., & Friedman, N. (2009). *Probabilistic Graphical Models: Principles and Techniques*. MIT Press. Chapter 12 (Hidden Markov Models). ISBN: 978-0262013192. URL: https://mitpress.mit.edu/9780262013192/
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. Chapter 13 (Sequential Data). ISBN: 978-0387310732.
