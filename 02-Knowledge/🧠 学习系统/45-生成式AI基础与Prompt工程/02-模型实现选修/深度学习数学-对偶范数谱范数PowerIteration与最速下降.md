---
type: study
topic: "对偶范数、谱范数、Power Iteration 与最速下降"
course: "生成式AI基础与Prompt工程"
tags: [学习, 45-生成式AI基础与Prompt工程, 深度学习数学, 优化]
created: 2026-08-05
status: completed
mastery: not_started
difficulty: advanced
stage_moc: "[[🧭 阶段2-模型实现选修]]"
concept: ["对偶范数", "谱范数", "最速下降"]
prerequisites: ["课程前置-神经网络数学-凸性几何链式法则与优化", "线性代数"]
related: ["训练优化-交叉熵AdamW调度梯度裁剪与检查点", "深度学习工程-宽度缩放WeightDecay卷积与受控比较"]
upstream: ["[[课程前置-神经网络数学-凸性几何链式法则与优化]]"]
flow: knowledge
kind: derivation
source: "MIT OCW 6.7960 Deep Learning Fall 2024 Homework 2 Questions 1-8, CC BY-NC-SA 4.0"
source_url: "https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/"
accessed: 2026-08-09
license: "CC BY-NC-SA 4.0"
anki_deck: "45-生成式AI基础与Prompt工程::深度学习数学"
anki_tags: [对偶范数, 谱范数, SVD, PowerIteration, 最速下降]
---

# 深度学习数学：对偶范数、谱范数、Power Iteration 与最速下降

## 0. 学习边界

- **类别**：A 类（MIT HW2 Q1–Q8 的数学主卡）。
- **判断理由**：这些题要求从范数几何推出更新方向，并用谱范数与随机矩阵实验验证尺度；softmax 或 Prompt 评测概览不能替代。

## 1. 这个知识点解决什么问题？

> “最陡”依赖用什么范数测步长。怎样把线性函数在单位球上的最大值写成对偶范数？怎样求矩阵最大放大率，并用迭代算法估计？

## 2. 为什么它重要？它有什么用？

- 对偶范数把 Hölder 上界变成可达到的优化解。
- 最速下降解释 SGD、符号梯度和谱几何更新为何不同。
- 谱范数控制线性层最大放大率、Lipschitz 界和训练稳定性。
- Power iteration 无需完整 SVD 即可估计主奇异值。

## 3. 学它之前需要哪些前置知识？

1. 向量内积、矩阵乘法、特征值与奇异值。
2. [[课程前置-神经网络数学-凸性几何链式法则与优化]]：梯度和一阶近似。

## 4. 用直觉语言解释它

> “范数规定你能走的单位球，对偶范数告诉梯度能在这颗球上赚到多少下降；谱范数则问矩阵最能拉长哪个方向。”

一句话本质：**先选几何，再由对偶几何决定最陡方向。**

## 5. 正式定义、核心公式、符号解释

对偶范数：
$$\|y\|_* = \sup_{\|x\|\le1}\langle x,y\rangle.$$

若 $1/p+1/q=1$，则 $\ell_p$ 的对偶是 $\ell_q$，Hölder 不等式为
$$|x^Ty|\le\|x\|_p\|y\|_q.$$

给定梯度 $g$、半径 $\epsilon$，一阶最速下降解
$$\arg\min_{\|\Delta\|\le\epsilon}g^T\Delta$$
取得值 $-\epsilon\|g\|_*$。特别地：

- $p=2$：$\Delta=-\epsilon g/\|g\|_2$；
- $p=\infty$：$\Delta=-\epsilon\operatorname{sign}(g)$；
- $p=1$：只在 $|g_i|$ 最大坐标上分配步长。

矩阵谱范数：
$$\|A\|_2=\sup_{\|x\|_2=1}\|Ax\|_2=\sigma_{max}(A)=\sqrt{\lambda_{max}(A^TA)}.$$

矩阵谱范数的对偶为核范数 $\|A\|_*=\sum_i\sigma_i(A)$。Power iteration 对 $A^TA$：
$$x_{k+1}=\frac{A^TAx_k}{\|A^TAx_k\|_2},\qquad \|Ax_k\|_2\to\sigma_{max}(A).$$

| 对象 | 几何 | 对偶 | 典型方向 |
| :--- | :--- | :--- | :--- |
| $\ell_2$ | 球 | $\ell_2$ | 负归一化梯度 |
| $\ell_\infty$ | 立方体 | $\ell_1$ | 负 sign |
| $\ell_1$ | 菱形 | $\ell_\infty$ | 最大坐标稀疏步 |
| 谱范数 | 最大奇异值 | 核范数 | 奇异向量外积 |

## 6. 推导思路和思想来源

1. 一阶近似 $L(\theta+\Delta)\approx L(\theta)+g^T\Delta$。
2. 将步长限制在选定范数单位球；对偶范数给出线性项绝对值上界。
3. 找到 Hölder 取等方向，即得最速下降解。
4. 对矩阵，$\|Ax\|_2^2=x^TA^TAx$；Rayleigh quotient 最大值是 $A^TA$ 最大特征值。
5. Power iteration 反复放大最大特征方向；若起点与主方向正交或最大特征值不唯一，收敛结论需调整。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

$g=(3,-4)$，$\epsilon=1$。$\ell_2$ 几何下方向为 $(-3/5,4/5)$；$\ell_\infty$ 下为 $(-1,1)$；$\ell_1$ 下全部预算给第二坐标 $(0,1)$。

### 例子 2：中等例子

正交矩阵 $Q$ 满足 $Q^TQ=I$，所以任意 $x$ 有 $\|Qx\|_2=\|x\|_2$，全部奇异值为 1，谱范数为 1。

### 例子 3：可运行 Python

```python
# 输入：2x2 矩阵；输出：Power iteration 谱范数估计。
import math

def matvec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]

def transpose(matrix):
    return [list(column) for column in zip(*matrix)]

def normalize(vector):
    norm = math.sqrt(sum(value * value for value in vector))
    return [value / norm for value in vector]

def spectral_norm(matrix, steps=30):
    vector = normalize([1.0] * len(matrix[0]))
    transposed = transpose(matrix)
    for _ in range(steps):
        vector = normalize(matvec(transposed, matvec(matrix, vector)))
    return math.sqrt(sum(value * value for value in matvec(matrix, vector)))

estimate = spectral_norm([[3.0, 0.0], [0.0, 1.0]])
print(round(estimate, 6))
assert abs(estimate - 3.0) < 1e-5
```

## 8. 常见误区和易混概念

- 对偶范数不是倒数；它是单位球上线性函数的最大值。
- 元素最大绝对值、Frobenius 范数和谱范数不是同一个量。
- Power iteration 估计主奇异值时应迭代 $A^TA$ 或交替 $A,A^T$，不能只在非方阵上反复乘 $A$。
- 随机高斯矩阵单次实验不是定理；应重复采样并报告尺寸、方差缩放和置信区间。

| 概念 | 定义对象 | 结果 | 区别 |
| :--- | :--- | :--- | :--- |
| 谱范数 | 线性算子 | 最大奇异值 | 最大放大率 |
| Frobenius 范数 | 全部元素 | 奇异值平方和开方 | 易算但非谱上确界 |
| 核范数 | 矩阵 | 奇异值之和 | 谱范数的对偶 |

## 9. 课程连接

- [[课程前置-神经网络数学-凸性几何链式法则与优化]] 提供一阶近似和梯度，本卡进一步说明“最陡”依赖所选几何。
- [[深度学习工程-宽度缩放WeightDecay卷积与受控比较]] 使用谱范数与尺度实验；[[训练优化-交叉熵AdamW调度梯度裁剪与检查点]] 使用全局范数控制更新。
- 完整证明与随机矩阵理论仍回到 [[🗺️ 最优化方法学习路径|最优化路径]]、[[🗺️ 高等代数学习路径|高等代数路径]]。

## 10. 闭卷复现任务

- [ ] 写出对偶范数定义。
- [ ] 写出 Hölder 不等式与 $p/q$ 关系。
- [ ] 推导 $\ell_2$ 最速方向。
- [ ] 推导 $\ell_\infty$ 最速方向。
- [ ] 说明 $\ell_1$ 方向为何稀疏。
- [ ] 写出谱范数三种等价形式。
- [ ] 证明正交矩阵谱范数为 1。
- [ ] 写出 Power iteration。
- [ ] 说明其失败/慢收敛条件。
- [ ] 设计高斯矩阵谱范数受控实验。

## 11. 自测题：5 道

1. $\ell_1$ 的对偶范数是什么？ `#自测题/基础`
2. $g=(1,-2)$ 的 $\ell_\infty$ 最速单位方向是什么？ `#自测题/基础`
3. 对角矩阵 `diag(2,5)` 的谱范数是多少？ `#自测题/中等`
4. 为什么正交矩阵不会放大 $\ell_2$ 长度？ `#自测题/中等`
5. 给出 Power iteration 起点与主特征向量正交时的失败例，并提出随机重启测试。 `#自测题/较难`

> [!question]- 参考答案与评分点
> 1. $\ell_\infty$。2. $(-1,1)$。3. 5。4. $\|Qx\|_2^2=x^TQ^TQx=\|x\|_2^2$。5. 对角矩阵与起点选次特征轴；随机连续起点正交概率为零，多次重启并取最大估计。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/45-生成式AI基础与Prompt工程"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 12. 我的主动回忆区

- **对偶定义**：
- **最速方向**：
- **Power iteration 边界**：
- [ ] 明天  [ ] 3 天后  [ ] 7 天后  [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- 这是一张 HW2 数学工具链；完整随机矩阵理论进入高等代数/概率路径。
- 任何矩阵实验先写尺寸、元素方差和重复次数，再解释结果。

## 🃏 Anki 卡片

Q: 对偶范数的操作性定义是什么？
A: 在原范数单位球上，线性函数与给定向量内积的最大值。

Q: 谱范数与奇异值的关系是什么？
A: 谱范数等于最大奇异值，也等于 A^T A 最大特征值的平方根。

