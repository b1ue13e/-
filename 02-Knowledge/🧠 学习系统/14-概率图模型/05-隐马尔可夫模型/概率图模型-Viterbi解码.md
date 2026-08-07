---
type: study
topic: "Viterbi解码"
course: "14-概率图模型"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段5-隐马尔可夫模型]]"
flow: knowledge
kind: derivation
difficulty: intermediate
upstream: ["[[概率图模型-隐马尔可夫模型HMM]]", "[[概率图模型-和积算法与消息传递]]"]
concept: ["Viterbi", "动态规划", "回溯", "最大积"]
related: ["概率图模型-隐马尔可夫模型HMM", "概率图模型-前向后向算法与BaumWelch"]
tags: [概率图模型, HMM, Viterbi]
---

# 概率图模型-Viterbi解码

> **Viterbi 算法**解决 HMM 三大基本问题中的**解码**：给定观测序列与参数，求**最可能的隐状态序列** $\mathbf{q}^* = \arg\max_{\mathbf{q}} P(\mathbf{q} \mid O, \lambda)$。它是动态规划（也是最大积算法在 HMM 链上的特例），复杂度 $O(N^2T)$。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：给定观测 $O = (o_1, \dots, o_T)$ 和 HMM $\lambda$，想知道背后的状态序列（如词性序列、基因结构）。直接枚举 $N^T$ 个状态序列不可行。Viterbi 用动态规划：**到每个时刻、每个状态只保留一条最优路径**，逐步推进，最后回溯整条最优序列。

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：Viterbi 是最大积（Max-Product）消息在 HMM 链上的实现（见 [[概率图模型-和积算法与消息传递]]）；与"前向后向"互补（解码 vs 评估）。
- **实际应用场景**：语音识别（词序列）、词性标注、基因预测（Genscan）、通信（卷积码解码）。
- **高频考点**：递推公式、回溯指针、与最大积的联系、复杂度。

---

## 3. 学它之前需要哪些前置知识？

1. **[[概率图模型-隐马尔可夫模型HMM]]**：五元组、三大问题。
2. **[[概率图模型-和积算法与消息传递]]**：最大积算法框架。
3. **[[概率图模型-前向后向算法与BaumWelch]]**：链上 DP 范式。

---

## 4. 定义与核心公式

### 4.1 Viterbi 变量

**定义**：$\delta_t(i) = \max_{q_1, \dots, q_{t-1}} P(q_1, \dots, q_{t-1}, q_t = s_i, o_1, \dots, o_t \mid \lambda)$——到 $t$ 时刻以 $s_i$ 结尾的最优部分路径的概率。

**回溯指针**：$\psi_t(i) = \arg\max_{j} \delta_{t-1}(j) a_{ji}$——最优路径上 $t-1$ 时刻的状态。

### 4.2 算法步骤

1. **初始化**：$\delta_1(i) = \pi_i b_i(o_1)$，$\psi_1(i) = 0$；
2. **递推**（$t = 2, \dots, T$）：
   $$\delta_t(j) = b_j(o_t) \max_i \left[ \delta_{t-1}(i) a_{ij} \right]$$
   $$\psi_t(j) = \arg\max_i \left[ \delta_{t-1}(i) a_{ij} \right]$$
3. **终止**：$P^* = \max_i \delta_T(i)$，$q_T^* = \arg\max_i \delta_T(i)$；
4. **回溯**（$t = T-1, \dots, 1$）：$q_t^* = \psi_{t+1}(q_{t+1}^*)$。

**输出**：最优状态序列 $\mathbf{q}^* = (q_1^*, \dots, q_T^*)$ 与概率 $P^*$。

### 4.3 与最大积的联系

Viterbi = 最大积消息在 HMM 链上的实现：$\delta_t(j)$ 就是"到状态 $j$ 的最大积消息"，$\max$ 替代了前向算法的 $\sum$。**前向（和）算边缘概率，Viterbi（最大）算 MAP 序列**——这是和积 vs 最大积的本质区别。

---

## 5. 关键推导

**推导：Viterbi 递推的最优子结构**。

若 $\mathbf{q}^*$ 是全局最优路径，则其前缀（到 $t$ 时刻）也必然是"到 $q_t^*$ 的最优路径"——否则替换前缀会得到更优全局路径（矛盾）。故只需对每个 $t, j$ 保留最优前缀 $\delta_t(j)$，递推成立。∎

**推导：为什么用 $\max$ 而非 $\sum$**。
目标是"最可能序列"（联合概率最大），是**乘法链 + 取最大**；前向目标是"总概率"（对序列求和）。两者是同一 DP 框架的和/最大变体（对应和积/最大积算法）。∎

**推导：复杂度 $O(N^2T)$**。
每步每个 $j$ 对 $i$ 取 $N$ 个 max → $N^2$，共 $T$ 步；回溯 $O(T)$。∎

---

## 6. 最小可手算例子

**例**：$N=2$，$\pi = (0.5, 0.5)$，$A = \begin{pmatrix}0.7 & 0.3\\0.4 & 0.6\end{pmatrix}$，$b_1(0)=0.9, b_1(1)=0.1$，$b_2(0)=0.2, b_2(1)=0.8$。观测 $O = (0, 1)$。

**$t=1$**：$\delta_1(1) = 0.5\times0.9 = 0.45$；$\delta_1(2) = 0.5\times0.2 = 0.10$。

**$t=2$**：
- $\delta_2(1) = b_1(1)\max(0.45\times0.7, 0.10\times0.4) = 0.1\times\max(0.315, 0.04) = 0.0315$，$\psi_2(1) = 1$；
- $\delta_2(2) = 0.8\times\max(0.45\times0.3, 0.10\times0.6) = 0.8\times\max(0.135, 0.06) = 0.108$，$\psi_2(2) = 1$。

**终止**：$P^* = \max(0.0315, 0.108) = 0.108$，$q_2^* = 2$。
**回溯**：$q_1^* = \psi_2(2) = 1$。

**输出**：最优状态序列 $(1, 2)$，概率 0.108。

> 对比：前向 $P(O) = 0.1915$（对所有路径求和）> Viterbi 0.108（最优路径）——符合 $P(O) \ge P(\mathbf{q}^*, O)$。

---

## 7. 反例与常见误区

| 误区 | 反例/纠正 |
|:---|:---|
| Viterbi 输出"每时刻最可能状态" | **错**。Viterbi 求**联合最优序列**；逐时刻 argmax（后验模态）可能拼出不合法/次优序列 |
| Viterbi 概率 = $P(O)$ | **错**。Viterbi 是最大联合 $P(\mathbf{q},O)$；$P(O)$ 是求和 |
| 可以用贪心逐时刻选最大 $\delta$ | **错**。必须维护回溯指针做全局最优（贪心会错过后续更好的转移） |
| Viterbi 只用于 HMM | **错**。任何链/树结构的最大积解码都用它（CRF 解码同样） |
| $\delta$ 需要归一化 | **不必须**。Viterbi 用非归一化联合概率取 max；归一化不影响 argmax |

---

## 8. 检索练习（闭卷自检）

### #自测题/基础
1. 写出 Viterbi 递推与回溯公式。
2. Viterbi 与逐时刻 argmax 有何区别？

### #自测题/中等
3. 用 §6 数据完整手算 Viterbi（含回溯）。
4. 说明 Viterbi 与最大积算法的关系。

### #自测题/较难
5. 构造一个例子：逐时刻后验 argmax 序列 ≠ Viterbi 最优序列（提示：利用转移约束）。

<details>
<summary>答案（先闭卷作答再展开）</summary>

1. $\delta_t(j) = b_j(o_t)\max_i[\delta_{t-1}(i)a_{ij}]$；回溯 $q_t^* = \psi_{t+1}(q_{t+1}^*)$。
2. Viterbi 联合最优；逐时刻 argmax 是边缘最优，可能违反转移约束。
3. 见 §6：$(1,2)$，概率 0.108。
4. Viterbi 是最大积消息在 HMM 链的实例（$\max$ 替代 $\sum$）。
5. 例：转移不允许 $s_2\to s_2$（$a_{22}=0$），但逐时刻边缘偏爱 $s_2$——逐时刻拼出 $(2,2)$ 非法，Viterbi 输出 $(1,2)$ 或 $(2,1)$。
</details>

---

## 9. 通过标准

- [ ] 能**默写** Viterbi 递推/回溯与复杂度；
- [ ] 能**独立完成**检索练习 1–5；
- [ ] 能**手算**小 HMM 的 Viterbi；
- [ ] 能**区分**解码（最大）与评估（求和）。

---

## 10. 来源

- Viterbi (1967). Error bounds for convolutional codes. *IEEE Trans. IT*.
- Rabiner (1989). A tutorial on HMMs and speech recognition. *Proc. IEEE*.
- Koller & Friedman (2009). *Probabilistic Graphical Models*, MIT Press. Ch. 10.4. 访问日期：2026-08-07。

---

## 11. 学完后可以完成

```dataview
LIST
FROM "03-Projects/14-概率图模型"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/14-概率图模型"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

> 直接下游：[[概率图模型-CRF推断]]（CRF 解码）、阶段 6 的 [[语音解码]]/[[POS-CRF]]、课程 Capstone。
