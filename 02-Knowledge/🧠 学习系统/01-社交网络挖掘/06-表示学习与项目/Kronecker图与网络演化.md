---
type: study
topic: "随机 Kronecker 图与网络演化"
course: "社交网络挖掘"
tags: [学习, 01-社交网络挖掘, Kronecker图, HW4]
created: 2026-08-05
status: completed
difficulty: advanced
concept: [Kronecker积, bit-vector表示, 图统计期望]
prerequisites: [随机网络模型-ER-WS-BA-配置模型, 矩阵, 二项式定理]
related: [图表示学习-DeepWalk与Node2Vec, 可复现网络挖掘实验]
flow: knowledge
kind: derivation
stage_moc: "[[🧭 阶段6-表示学习与项目]]"
source: "Stanford CS224W 2017 HW4-Q3.1-Q3.5 and lecture 16"
source_url: "https://snap.stanford.edu/class/cs224w-2017/handouts.html"
accessed: 2026-08-06
license: "课程讲义与题面公开访问但未核验开放再分发许可；link-only"
assessment_exempt: false
anki_deck: "社交网络挖掘::表示学习"
anki_tags: [Kronecker, bit-vector, 期望度, 自环, HW4]
---

# 随机 Kronecker 图与网络演化

## 0. 学习边界
- **类别**：**A 类**；HW4-Q3.1–Q3.5 全部依赖同一条 bit-vector 推导链。
- **判断理由**：只记 $(\sum\Theta)^k$ 不足以回答节点边概率、按权重的期望度和自环数。

## 1. 这个知识点解决什么问题？
> **麻烦**：怎样用一个 $2\times2$ 概率模板递归生成 $2^k$ 节点的图，同时闭式计算特定节点的边概率、期望度、总边数和自环数？

## 2. 为什么它重要？它有什么用？
- 把矩阵 Kronecker 积转换为节点地址上的逐位概率乘积。
- 用少量参数构造多尺度、异质的大图基线。
- HW4-Q3 要求逐步推导，不是调用 `np.kron` 即完成。

## 3. 学它之前需要哪些前置知识？
1. **[[随机网络模型-ER-WS-BA-配置模型]]**：生成模型与期望计数。
2. 二项式定理、Kronecker 积和伯努利变量期望。

### 先备诊断
- [ ] 能把整数 0–3 写成长度 2 的 bit-vector。
- [ ] 能用 $(x+y)^r=\sum_j\binom rj x^jy^{r-j}$ 合并一类概率和。
- [ ] 能解释 $E[\sum X_{uv}]=\sum E[X_{uv}]$ 不要求独立。
- **失败补救**：前两项任一失败，先做[[数学与Python前置诊断]]。

## 4. 用直觉语言解释它
> “每个节点是一个长度 $k$ 的二进制地址；两个节点每一位的组合都从小模板取一个概率，整条边的概率是 $k$ 层概率相乘。”
- **一句话本质**：Kronecker 幂把递归矩阵块结构等价成逐位独立的地址匹配规则。

## 5. 正式定义、核心公式、符号解释

### 1. Initiator 与 bit-vector
采用 HW4 的对称 initiator：
$$
\Theta=\begin{bmatrix}\gamma&\beta\\\beta&\alpha\end{bmatrix},
\qquad 0\le\gamma\le\beta\le\alpha\le1.
$$
$k$ 次 Kronecker 幂 $P=\Theta^{\otimes k}$ 有 $2^k\times2^k$ 个元素。把行/列编号写成长度 $k$ 的 bit-vector $u=(u_1,\dots,u_k)$、$v=(v_1,\dots,v_k)$，则
$$
P_{uv}=\prod_{b=1}^k\Theta[u_b,v_b].
$$

### 2. 按位计数得到边概率
设 $u$ 的权重（1 的个数）为 $\ell$；$i$ 是 `u=1,v=1` 的位数，$j$ 是 `u=0,v=1` 的位数。其余两类位数为：
- `u=1,v=0`：$\ell-i$；
- `u=0,v=0`：$k-\ell-j$。

所以
$$
P_{uv}=\alpha^i\beta^{j+\ell-i}\gamma^{k-\ell-j}.
$$

### 3. 权重为 $\ell$ 的节点期望度
对所有 $v$ 求和。$u$ 的 $\ell$ 个 1 位，每位对 $v_b\in\{0,1\}$ 的概率和为 $\beta+\alpha$；其余 $k-\ell$ 个 0 位的概率和为 $\gamma+\beta$。由乘法分配律/二项式定理：
$$
E[d(u)]=\sum_vP_{uv}=(\alpha+\beta)^\ell(\beta+\gamma)^{k-\ell}.
$$
这里是邻接矩阵行和口径，包含 $u\to u$ 的 Bernoulli 项。

### 4. 总边数
所有有序矩阵单元的期望和：
$$
\sum_{u,v}P_{uv}=(\alpha+2\beta+\gamma)^k.
$$
HW4-Q3.4 采用“不特别处理自环”的简化无向边口径：
$$
E[|E|]_{\text{HW4 convention}}=\frac12(\alpha+2\beta+\gamma)^k.
$$
若自环作为一条无向边精确计一次，则应把对角线补回一半：
$$
E[|E|]_{\text{exact}}=\frac12\left[(\alpha+2\beta+\gamma)^k+(\alpha+\gamma)^k\right].
$$
回答作业时遵循题目要求并声明口径。

### 5. 自环数
对 $u=v$，每个 1 位贡献 $\alpha$，每个 0 位贡献 $\gamma$。遍历全部 bit-vector：
$$
E[L]=\sum_uP_{uu}=\sum_{\ell=0}^k\binom{k}{\ell}\alpha^\ell\gamma^{k-\ell}
=(\alpha+\gamma)^k.
$$
也可用 $\operatorname{tr}(\Theta^{\otimes k})=\operatorname{tr}(\Theta)^k$ 快速验证。

### 6. 符号表
| 符号 | 含义 | 范围 |
| :--- | :--- | :--- |
| $\alpha$ | `1-1` 位配对概率 | $[0,1]$ |
| $\beta$ | 异位配对概率 | $[0,1]$ |
| $\gamma$ | `0-0` 位配对概率 | $[0,1]$ |
| $\ell$ | 节点 $u$ 的 Hamming weight | $0,\ldots,k$ |
| $i,j$ | 两类联合位计数 | 受 $\ell,k$ 约束 |

## 6. 推导思路和思想来源
1. **矩阵索引递归**：Kronecker 幂的每层块选择由一对 bit 决定。
2. **逐位乘积**：固定 $u,v$ 后，把每一位的模板概率相乘。
3. **按位类型计数**：四类 `(u_b,v_b)` 次数相加为 $k$，得到 $P_{uv}$。
4. **期望度因式分解**：对所有 $v$ 求和等于每个位上两个选择之和的乘积。
5. **全图统计**：对所有行列求和对应 initiator 全元素和的 $k$ 次方；对角求和对应迹的 $k$ 次方。

## 7. 例子：已解 → 渐隐 → 实际应用

### 例子 1：已解手算
取 $k=3$，$u=101$，所以 $\ell=2$；令 $v=111$，则 $i=2,j=1$。因此
$$P_{uv}=\alpha^2\beta^1\gamma^0.$$
该节点期望度为 $(\alpha+\beta)^2(\beta+\gamma)$。

### 例子 2：渐隐例
令 $u=0101,v=1100$：
1. $\ell=\_\_$；
2. $i=\_\_$，$j=\_\_$；
3. $P_{uv}=\alpha^{\_}\beta^{\_}\gamma^{\_}$。

> [!question]- 核对
> $\ell=2$；$i=1,j=1$；另有一次 `1-0`，一次 `0-0`，所以 $P_{uv}=\alpha\beta^2\gamma$。

### 例子 3：全公式可运行校验
```python
import itertools
import numpy as np

alpha, beta, gamma, k = 0.9, 0.5, 0.2, 3
theta = np.array([[gamma, beta], [beta, alpha]])
probability = theta.copy()
for _ in range(k - 1):
    probability = np.kron(probability, theta)

bits = list(itertools.product([0, 1], repeat=k))
node = bits.index((1, 0, 1))
expected_degree = (alpha + beta) ** 2 * (beta + gamma)
expected_directed_cells = (alpha + 2 * beta + gamma) ** k
expected_loops = (alpha + gamma) ** k
print(probability.shape)
print(round(probability[node].sum(), 10), round(expected_degree, 10))
print(round(probability.sum(), 10), round(expected_directed_cells, 10))
print(round(np.trace(probability), 10), round(expected_loops, 10))
assert np.isclose(probability[node].sum(), expected_degree)
assert np.isclose(probability.sum(), expected_directed_cells)
assert np.isclose(np.trace(probability), expected_loops)
# 输出三组左右相等的数值，逐项验证期望度、总矩阵质量与自环公式。
```

## 8. 常见误区和易混概念
- **误区 1：把概率矩阵当观测邻接矩阵。** 每个允许单元还需进行 Bernoulli 采样。
- **误区 2：只用 $\ell$ 就能决定任意 $P_{uv}$。** 单边概率还需要 $i,j$；$\ell$ 足以决定期望度是因为已经对所有 $v$ 求和。
- **误区 3：总边数忘记无向图除以 2。** 还要声明是否对自环作精确修正。
- **误区 4：自环期望写成 $\alpha^k+\gamma^k$。** 这只数全 1 和全 0 两个节点；所有混合 bit-vector 也可能自环，正确和为 $(\alpha+\gamma)^k$。

| 模型 | 节点地址 | 边概率 | 主要异质来源 |
| :--- | :--- | :--- | :--- |
| 随机 Kronecker | bit-vector | 逐位模板乘积 | 地址权重与递归块 |
| ER | 无角色地址 | 常数 $p$ | 无 |
| BA | 到达时间/度 | 动态优先连接 | 增长与富者愈富 |
| SBM | 社区标签 | 块概率 | 离散群组 |

## 9. 相关知识点与 Obsidian 双链建议
- 上游：[[随机网络模型-ER-WS-BA-配置模型]]。
- 下游：[[可复现网络挖掘实验]]。
- 横向：[[图表示学习-DeepWalk与Node2Vec]]。
- 作业：CS224W 2017 HW4-Q3.1–Q3.5。

## 10. 闭卷复现任务
- [ ] 从 Kronecker 索引推出 bit-vector 乘积。
- [ ] 写出四类位计数并检查和为 $k$。
- [ ] 推出 $P_{uv}=\alpha^i\beta^{j+\ell-i}\gamma^{k-\ell-j}$。
- [ ] 用二项式定理推出期望度。
- [ ] 推出矩阵单元总和。
- [ ] 区分 HW4 简化边数口径与精确无向边口径。
- [ ] 用对角线和推出自环数。
- [ ] 手算第 7.1 节。
- [ ] 独立重写 NumPy 校验。
- [ ] 比较 Kronecker、ER、BA、SBM。

## 11. 自测题：5 道
1. $2\times2$ initiator 的 $k$ 次幂有多少节点？ #自测题/基础
   > [!question]- $2^k$。
2. 节点权重 $\ell$ 表示什么？ #自测题/基础
   > [!question]- 长度 $k$ 的 bit-vector 中 1 的个数。
3. 权重为 $\ell$ 的节点期望度？ #自测题/中等
   > [!question]- $(\alpha+\beta)^\ell(\beta+\gamma)^{k-\ell}$。
4. 为什么期望自环数是 $(\alpha+\gamma)^k$？ #自测题/中等
   > [!question]- 每个位自环只能取 `0-0` 的 $\gamma$ 或 `1-1` 的 $\alpha$，对全部地址求和按二项式展开。
5. 精确无向边期望为何多出一半对角线？ #自测题/较难
   > [!question]- 全矩阵和除以 2 会把自环也减半，但自环作为边应计一次，因此补回 $\tfrac12E[L]$。

## 12. 我的主动回忆区
### 我的闭卷复述
> 不看公式，用“节点地址—逐位概率—按地址求和”解释随机 Kronecker 图。
### 我的推导复现
> 从四类 bit 计数独立推出边概率、期望度、总边数和自环数，不允许直接背最终式。
### 我的错误与卡点
- [ ] $\beta$ 指数写错 → 画四类位计数表。
- [ ] 期望度不会求和 → 对 $u=1$ 位和 $u=0$ 位分别做二项式展开。
- [ ] 边数差半个自环项 → 检查简化/精确口径。
### 失败后的回流
- bit-vector 错：第 5.1–5.2 节；期望度错：第 5.3 节；边/环错：第 5.4–5.5 节；代码错：第 7.3 节。
- [ ] 明天重做 bit 例　[ ] 3 天后四公式闭卷　[ ] 7 天后代码校验　[ ] 14 天后与 ER/BA 混测

## 13. 给 Obsidian 的归档建议
- 文件夹：`06-表示学习与项目/`
- 关联：[[可复现网络挖掘实验]]
- 标签：`#Kronecker` `#bit-vector` `#HW4`
- 拆分建议：Q3.1–3.5 是同一推导链，保持一张完整主题卡。

## 🃏 Anki 卡片
- 随机 Kronecker 的单边概率如何由 bit-vector 得到？::$P_{uv}=\prod_b\Theta[u_b,v_b]=\alpha^i\beta^{j+\ell-i}\gamma^{k-\ell-j}$。
- 权重为 $\ell$ 的节点期望度？::$(\alpha+\beta)^\ell(\beta+\gamma)^{k-\ell}$。
- 随机 Kronecker 的期望自环数？::$(\alpha+\gamma)^k$，等于 $\operatorname{tr}(\Theta^{\otimes k})$。

## 🧪 学完本节后可完成的作业

- **可立即完成**：[[社交网络挖掘-课后作业-05-排序边介数Kronecker与谱聚类#3. 随机 Kronecker 图（20 分，Yokila）|课后作业 05 题 3]]。
- **为什么现在能做**：已覆盖 bit-vector、边概率、期望度、边数与自环的完整推导链。
- **提交产物**：3.1–3.5 推导、小规模枚举校验与公式边界说明。

