---
type: study
topic: "HW3 幂律阈值 SIR 与影响力"
tags: [学习, 01-社交网络挖掘]
created: 2026-08-06
status: ongoing
difficulty: intermediate
concept: [HW3 幂律阈值 SIR 与影响力]
prerequisites: [图与网络基础, Python基础]
related: []
flow: knowledge
kind: problem-type
source: "合并自课程内已有笔记；原始来源见各节"
verification_status: "题面与示例代码已合并；原始数据结果需按作业来源复现"
---

# HW3：幂律、阈值、SIR 与影响力实验

> **阅读顺序**：幂律估计、全局阈值、SIR 检验、影响力最大化对应 HW3 的四个独立验收单元。当前保留推导和示例代码，缺失的正式课程数据结果不得用随机图替代。

## 原笔记：HW3-幂律LS-MLE与重复实验

### 0. 先判断它值不值得深挖
- **类别**：A 类统计实验。
- **判断理由**：HW3 不只要求 MLE 公式，还要对取整经验 PDF 做原始/截断 LS，并以 100 份大样本比较偏差与方差。

### 1. 这个知识点解决什么问题？
> 同一幂律样本用 log-PDF 最小二乘和原始数据最大似然估计，为什么结果不同？怎样用重复实验区分偏差、方差和尾部稀疏噪声？

### 2. 为什么它重要？它有什么用？
- 训练“图看起来直”与“估计可靠”的区别。
- 把推导、采样、回归、绘图和 Monte Carlo 汇总连成一条可复现流程。
- 完整覆盖 HW3-Q2.1–Q2.5。

### 3. 学它之前需要哪些前置知识？
1. [[度分布余度与幂律估计]]。
2. `log` 变换、线性回归斜率、样本均值/标准差。

### 4. 用直觉语言解释它
> “LS 把每个非空直方图格子当一个观测，稀疏尾部格子噪声很大；MLE 直接利用每个原始样本的概率模型。”
- **一句话本质**：log-PDF LS 是异方差的二次近似，MLE 与生成分布更直接匹配。

### 5. 正式定义、核心公式、符号解释

#### 1. 连续幂律与 CCDF
对 $x\ge x_{min}$：
$$f(x)=\frac{\alpha-1}{x_{min}}\left(\frac{x}{x_{min}}\right)^{-\alpha}.$$
积分得
$$P(X\ge x)=\left(\frac{x}{x_{min}}\right)^{1-\alpha}.$$

#### 2. 逆变换采样
若 $U\sim U(0,1)$，令 CCDF 值为 $U$：
$$X=x_{min}U^{-1/(\alpha-1)}.$$
用 $1-U$ 等价；必须避免精确 0。

#### 3. PDF 最小二乘
取整后经验频率 $\hat p_k=n_k/n$。由
$$\log f(k)=\log(\alpha-1)+(\alpha-1)\log x_{min}-\alpha\log k$$
设置 $y_k=\log\hat p_k,x_k=\log k$，拟合
$$y_k=c+s x_k+\varepsilon_k,\qquad \hat\alpha_{LS}=-\hat s.$$
只有 $n_k>0$ 才能取对数。原始 LS 对所有非空 bin 等权；截断 LS 仅保留计数不低于阈值 $c_{min}$ 的 bin，以减少极稀疏尾部的高方差。阈值必须预先声明，不可看结果后挑到最接近真值。

#### 4. 最大似然
$$
\ell(\alpha)=n\log(\alpha-1)-n\log x_{min}
-\alpha\sum_i\log(x_i/x_{min}),
$$
$$
\frac{\partial\ell}{\partial\alpha}=\frac n{\alpha-1}-\sum_i\log(x_i/x_{min})=0,
$$
$$\hat\alpha_{MLE}=1+\frac n{\sum_i\log(x_i/x_{min})}.$$

#### 5. 重复实验汇总
对 $R=100$ 份独立数据集，每种估计器得到 $\hat\alpha_r$：
$$\bar\alpha=R^{-1}\sum_r\hat\alpha_r,\qquad
s=\sqrt{\frac1{R-1}\sum_r(\hat\alpha_r-\bar\alpha)^2}.$$
与真值比较偏差 $\bar\alpha-\alpha$，用 $s$ 描述跨数据集波动。

### 6. 推导思路和思想来源
1. CCDF 积分给出可逆单调函数，直接构造采样器。
2. 幂律取对数变线性，但误差结构并未变成等方差高斯。
3. 尾部计数少，$\log\hat p_k$ 变化剧烈；截断换取更低方差但可能引入范围偏差。
4. MLE 不取整、不分箱，保留更多信息。
5. 单数据集优劣可能偶然，重复 100 次才可比较偏差/方差。

### 7. 例子：已解 → 半提示 → 完整代码

#### 例子 1：已解
真值 $\alpha=2,x_{min}=1$，若 $U=1/4$，则 $X=U^{-1}=4$。

#### 例子 2：半提示
回归斜率为 `-1.83` 时 $\hat\alpha_{LS}=\_\_$；MLE 样本对数和为 50、$n=40$ 时 $\hat\alpha=\_\_$。
> [!question]- 核对
> 1.83；$1+40/50=1.8$。

#### 例子 3：可运行端到端比较
```python
import numpy as np

def sample_power_law(size, alpha=2.0, xmin=1.0, rng=None):
    rng = rng or np.random.default_rng(0)
    uniform = np.maximum(rng.random(size), np.finfo(float).tiny)
    return xmin * uniform ** (-1.0 / (alpha - 1.0))

def pdf_ls(samples, min_count=1):
    rounded = np.rint(samples).astype(int)
    values, counts = np.unique(rounded, return_counts=True)
    keep = counts >= min_count
    x = np.log(values[keep].astype(float))
    y = np.log(counts[keep] / counts.sum())
    if len(x) < 2:
        raise ValueError("可用直方图格子不足")
    slope, intercept = np.polyfit(x, y, 1)
    return -slope, (values, counts / counts.sum(), intercept)

def mle(samples, xmin=1.0):
    return 1.0 + len(samples) / np.log(samples / xmin).sum()

def compare(repetitions=20, size=20_000, seed=0):
    rng = np.random.default_rng(seed)
    estimates = {"ls": [], "truncated_ls": [], "mle": []}
    for _ in range(repetitions):
        samples = sample_power_law(size, rng=rng)
        estimates["ls"].append(pdf_ls(samples, min_count=1)[0])
        estimates["truncated_ls"].append(pdf_ls(samples, min_count=20)[0])
        estimates["mle"].append(mle(samples))
    return {name: (float(np.mean(values)), float(np.std(values, ddof=1)))
            for name, values in estimates.items()}

summary = compare()
print({key: tuple(round(x, 3) for x in value) for key, value in summary.items()})
assert all(np.isfinite(value).all() for value in summary.values())
# 输出三种估计器的跨数据集均值与样本标准差。
```

#### 正式作业参数与绘图
- 单数据集：`size=100_000, alpha=2, xmin=1`。
- 重复比较：`repetitions=100, size=100_000`。
- 图上叠加经验 PDF、真 PDF、两种 LS/MLE 拟合；若 LS 得 $\alpha\le1$，仅画斜率线并解释其非正规化性。
- 报告截断规则（如 `count>=20`）及敏感性，而非仅报“改进后更接近”。

### 8. 常见误区和易混概念
- 对 $p_k=0$ 取 log：应排除零频 bin。
- 把 LS 截距强制成理论截距：题目是线性回归，有限取整数据与连续 PDF 不完全一致。
- 用取整后的数据做连续 MLE：MLE 应使用原始连续样本。
- 100 次重复共用完全相同样本：应由同一 RNG 连续生成独立数据集，而非每轮重置 seed。

| 估计器 | 数据输入 | 主要问题 | 优势 |
| :--- | :--- | :--- | :--- |
| 全 PDF-LS | 取整非空 bin | 稀疏尾部高方差 | 直观可视化 |
| 截断 PDF-LS | 高计数 bin | 截断偏差/规则选择 | 方差较低 |
| 连续 MLE | 原始样本 | 模型错设敏感 | 信息利用充分 |

### 9. 相关知识点与 Obsidian 双链建议
- 上游：[[度分布余度与幂律估计]]。
- 实验：[[../06-表示学习与项目/可复现网络挖掘实验]]。
- 横向：[[随机网络模型-ER-WS-BA-配置模型]]。
- 作业：CS224W 2017 HW3-Q2.1–Q2.5。

### 10. 闭卷复现任务
- [ ] 推导 CCDF。
- [ ] 推导逆变换。
- [ ] 建立 log-PDF 回归。
- [ ] 解释斜率与 $\alpha$。
- [ ] 声明截断规则。
- [ ] 推导 MLE。
- [ ] 区分原始/取整样本用途。
- [ ] 运行三估计器。
- [ ] 完成 100 次比较。
- [ ] 报告均值、标准差、偏差。

### 11. 自测题：5 道
1. PDF-LS 的斜率与 $\alpha$ 关系？ #自测题/基础
   > [!question]- 斜率 $s=-\alpha$，所以估计为 $-s$。
2. 为什么零频 bin 不能进入回归？ #自测题/基础
   > [!question]- $\log0$ 不存在。
3. 截断尾部为何可能改进 LS？ #自测题/中等
   > [!question]- 稀疏尾部经验频率相对方差极高，会对等权 log 回归产生强噪声。
4. MLE 为什么用原始样本？ #自测题/中等
   > [!question]- 取整/分箱会丢失连续观测信息并改变似然模型。
5. 只比较单次估计离真值距离为什么不可靠？ #自测题/较难
   > [!question]- 单次误差混合偏差与随机方差；重复实验才能比较估计分布。

### 12. 我的主动回忆区
#### 我的闭卷复述
> 对比全 LS、截断 LS、MLE 的输入、假设与误差来源。
#### 我的推导复现
> 重建 CCDF、逆采样、LS 斜率和 MLE 一阶条件。
#### 我的错误与卡点
- [ ] LS 异常 → 检查零频、取整和截断。
- [ ] MLE 偏离 → 检查是否使用原始样本和相同 $x_{min}$。
- [ ] 重复标准差为 0 → 检查是否每轮重置相同 seed。
#### 失败后的回流
- 推导错：第 5 节；代码错：第 7.3 节；解释错：第 8 节。

### 13. 给 Obsidian 的归档建议
- 文件夹：`02-网络结构与生成模型/`
- 关联：[[度分布余度与幂律估计]]
- 标签：`#HW3` `#幂律估计` `#MonteCarlo`
- 拆分建议：三估计器必须放在同一重复实验协议中比较，保持一张卡。

### 🃏 Anki 卡片
- PDF log-LS 如何估计幂律指数？::回归 $\log\hat p_k=c+s\log k$，取 $\hat\alpha=-s$。
- 连续幂律 MLE？::$1+n/\sum_i\log(x_i/x_{min})$。
- 为什么要比较 100 份数据集？::估计跨样本的均值、偏差和标准差，避免单次随机误差主导结论。

## 原笔记：HW3-全局阈值直方图-不等式与最终规模

### 0. 先判断它值不值得深挖

- **类别**：A 类作业推导，必须闭卷重建。
- **判断理由**：Q1 不是“反复迭代直到不变”的编程题，而是要求把逐层激活条件写成一组不等式，再证明最终人数的 min/max 表达，并从累计直方图直接读答案。

### 1. 这个知识点解决什么问题？

> 已知每种阈值人数，怎样在不逐人模拟的情况下判断阈值为 $\ell$ 的人能否加入，并从一张累计直方图确定最终参与人数？

核心困难是口径：阈值 $t_i$ 表示个体 $i$ 至少看到 $t_i$ 个**其他人**已经参与才加入；参与不可逆。阈值 0 的人最初就参与。

### 2. 为什么它重要？它有什么用？

- 覆盖 Stanford CS224W 2017 HW3-Q1(a-c)。
- 把“级联”转化为累计计数、归纳和固定点三种可互换语言。
- 为采用曲线、银行挤兑、抗议参与和产品扩散提供最小宏观模型。
- 训练识别“过程模拟正确，但没有证明最终表达式”的常见失分。

### 3. 学它之前需要哪些前置知识？

1. [[阈值模型与网络级联]]：知道激活不可逆和阈值的含义。
2. **累计直方图**：$C(k)=\sum_{\ell=0}^{k}N_\ell$。
3. **数学归纳法**：证明阈值组按 $0,1,\ldots$ 的顺序可被激活。

### 4. 用直觉语言解释它

> “过第 $k$ 道门之前，队伍里至少要已有 $k$ 个人；累计曲线高于对角线表示队伍还有足够的人继续推开下一道门，第一次碰到对角线就是停止人数。”

- **一句话本质**：在最终人数 $r$ 之前必须有 $C(k)>k$，第一次出现 $C(r)=r$ 时级联闭合。

### 5. 正式定义、核心公式、符号解释

#### 1. 阈值直方图与累计直方图

有 $n$ 个个体，阈值 $t_i\in\{0,\ldots,n-1\}$。令

$$
N_\ell=|\{i:t_i=\ell\}|,\qquad
C(k)=\sum_{\ell=0}^{k}N_\ell,\quad 0\le k\le n-1.
$$

为统一全员参与情形，扩展定义 $C(n)=n$。必有 $\sum_{\ell=0}^{n-1}N_\ell=n$。

#### 2. Q1(a)：阈值组激活条件

阈值为 $\ell\ge1$ 的个体最终能够激活，当且仅当

$$
C(k-1)\ge k,\qquad k=1,2,\ldots,\ell.
$$

展开就是

$$
N_0\ge1,\quad
N_0+N_1\ge2,\quad\ldots,\quad
\sum_{j=0}^{\ell-1}N_j\ge\ell.
$$

注意右侧是 $k$，左侧只累计阈值小于 $k$ 的人。这正对应“至少有 $k$ 个其他人已经参与”。

#### 3. Q1(b)：首个失败阈值表达

定义

$$
k^\star=\min\{k\in\{1,\ldots,n\}:C(k-1)<k\},
$$

若集合为空则令 $k^\star=n+1$。最终人数为

$$
R=
\begin{cases}
k^\star-1,&k^\star\le n,\\
n,&k^\star=n+1.
\end{cases}
$$

更紧凑的等价形式是

$$
R=\min\{k\in\{0,\ldots,n\}:C(k)=k\}.
$$

$C(n)=n$ 保证集合非空。

#### 4. 迭代固定点表达

最初人数 $a_0=N_0=C(0)$。定义

$$
a_{r+1}=C(a_r),\qquad C(n)=n.
$$

序列单调不减且至多为 $n$，因此有限步停止。停止值就是上面的最小固定点 $R$。

#### 5. 符号表

| 符号 | 含义 | 范围 |
| :--- | :--- | :--- |
| $N_\ell$ | 阈值恰为 $\ell$ 的人数 | 非负整数 |
| $C(k)$ | 阈值不超过 $k$ 的累计人数 | $0,\ldots,n$ |
| $k^\star$ | 第一道无法越过的阈值 | $1,\ldots,n+1$ |
| $R$ | 最终参与人数 | $0,\ldots,n$ |
| $a_r$ | 第 $r$ 轮闭包人数 | 单调不减 |

### 6. 推导思路和完整证明

#### 1. Q1(a) 的必要性

假设阈值为 $\ell$ 的人能够激活。对任意 $k\le\ell$，过程必须先让阈值小于 $k$ 的人形成至少 $k$ 人队伍，否则当前参与人数小于 $k$，阈值 $k$ 及以上的人都不会加入。阈值小于 $k$ 的总人数是 $C(k-1)$，故必须有 $C(k-1)\ge k$。

#### 2. Q1(a) 的充分性：归纳

- **基例 $k=1$**：$C(0)=N_0\ge1$，所以至少一名阈值 0 个体初始参与，阈值 1 组满足条件。
- **归纳假设**：阈值小于 $k$ 的组已经按序完成激活。
- **归纳步**：这些组共有 $C(k-1)\ge k$ 人，因此阈值为 $k$ 的每个个体至少看到 $k$ 个参与者，于是阈值 $k$ 组也能激活。

逐步应用到 $k=\ell$，阈值 $\ell$ 组能够激活。

#### 3. 首个失败点为什么给出最终人数

设 $k^\star$ 是第一个满足 $C(k^\star-1)<k^\star$ 的整数。由于它是第一个失败点，

$$C(k^\star-2)\ge k^\star-1.$$

累计函数单调，所以

$$
k^\star-1\le C(k^\star-2)\le C(k^\star-1)<k^\star.
$$

各量为整数，因此 $C(k^\star-1)=k^\star-1$。前 $k^\star-1$ 道门均能越过，但人数停在 $k^\star-1$；阈值 $k^\star$ 及以上者不再加入。

#### 4. 为什么等于最小固定点

对每个 $k<R$，过程能越过下一道门，所以 $C(k)\ge k+1>k$。在 $k=R$ 时没有更多个体可被激活，因此 $C(R)=R$。所以 $R$ 是第一个满足 $C(k)=k$ 的位置。

反过来，若 $C(r)=r$，则人数不超过 $r$ 时累计映射也不超过 $r$；从 $a_0\le r$ 出发的单调迭代不可能越过 $r$。最小这样的 $r$ 正是实际停止值。

### 7. 例子：已解 → 半提示 → 独立应用

#### 例子 1：已解全级联

阈值为 $[0,1,1,3]$，所以

$$N=(1,2,0,1),\qquad C=(1,3,3,4),\qquad C(4)=4.$$

对 $k=0,1,2,3$ 都有 $C(k)>k$，第一次相等在 $k=4$，故 $R=4$。

#### 例子 2：半提示停止级联

给定 $N=(1,0,3,0)$、$C=(1,1,4,4)$：

1. 第一条失败不等式是 $C(\_\_\,)<\_\_$。
2. $k^\star=\_\_$。
3. 最终人数 $R=\_\_$。

> [!question]- 核对
> $C(1)<2$；$k^\star=2$；$R=1$。图上第一次 $C(k)=k$ 也发生在 $k=1$。

#### 例子 3：可运行读取、证明断言与绘图

```python
from pathlib import Path
import tempfile
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

def load_histogram(path):
    values = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        clean = line.split("#", 1)[0].strip()
        if clean:
            values.extend(int(token) for token in clean.split())
    if any(value < 0 for value in values):
        raise ValueError("直方图计数不能为负")
    if sum(values) != len(values):
        raise ValueError("HW3 直方图必须有 n 个 bin，且计数和为 n")
    return values

def final_rioters(histogram):
    n = sum(histogram)
    cumulative = np.cumsum(histogram).tolist() + [n]
    fixed_points = [k for k in range(n + 1) if cumulative[k] == k]
    final = min(fixed_points)
    active = histogram[0]
    history = [active]
    while True:
        updated = cumulative[active]
        assert updated >= active
        if updated == active:
            break
        active = updated
        history.append(active)
    assert active == final
    first_failure = next(
        (k for k in range(1, n + 1) if cumulative[k - 1] < k),
        n + 1,
    )
    from_failure = n if first_failure == n + 1 else first_failure - 1
    assert from_failure == final
    return final, cumulative, history

def plot_cumulative(histogram, output_path):
    final, cumulative, _ = final_rioters(histogram)
    x = np.arange(len(cumulative))
    plt.figure(figsize=(5, 4))
    plt.step(x, cumulative, where="post", label="C(k)")
    plt.plot(x, x, "--", label="y=k")
    plt.scatter([final], [final], color="red", zorder=3, label="first fixed point")
    plt.xlabel("k")
    plt.ylabel("cumulative count")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return final

assert final_rioters([1, 2, 0, 1])[0] == 4
assert final_rioters([1, 0, 3, 0])[0] == 1
assert final_rioters([0, 4, 0, 0])[0] == 0

with tempfile.TemporaryDirectory() as temp_dir:
    histogram_path = Path(temp_dir) / "thresholds.txt"
    figure_path = Path(temp_dir) / "cumulative.png"
    histogram_path.write_text("1 0 3 0\n", encoding="utf-8")
    histogram = load_histogram(histogram_path)
    assert plot_cumulative(histogram, figure_path) == 1
    assert figure_path.exists() and figure_path.stat().st_size > 0
    print(final_rioters(histogram))
# 输出最终人数、累计数组和迭代历史；正式数据只需替换 thresholds.txt。
```

2017 的 thresholds.txt 原链接当前返回 404。取得课程方合法归档副本后，先记录 SHA-256，再运行同一 loader 和绘图函数；当前不得虚构 Q1(c) 的数值答案。

### 8. 常见误区和易混概念

- **把“其他人”改成“包含自己”**：会把不等式和累计下标整体移动一位。
- **只写 $a_{r+1}=C(a_r)$**：能模拟，但没有回答 Q1(a) 的逐层不等式与 Q1(b) 的显式表达。
- **把最终人数取成最大 $C(k)$**：$C(n-1)=n$ 永远成立，无法描述级联是否到达那里。
- **找任意固定点**：必须找从 $N_0$ 出发可达的最小固定点；等价于第一个 $C(k)=k$。
- **读图找第一次“曲线低于对角线”**：在精确整数模型中停止点是第一次相等；此前应严格高于对角线。
- **把全局阈值模型当网络 LT**：本题每个人观察全体人数，不使用邻接矩阵或邻居比例。

| 对象 | 激活依据 | 最终规模方法 | 是否依赖网络 |
| :--- | :--- | :--- | :--- |
| HW3 全局阈值 | 全体已参与人数 | $C(k)$ 最小固定点 | 否 |
| 网络 LT | 邻居权重和 | 节点级迭代 | 是 |
| HW2 投票 | 邻居 A/B 多数 | 按 ID 原地 10 轮 | 是 |

### 9. 相关知识点与 Obsidian 双链建议

- 上游：[[阈值模型与网络级联]]。
- 横向：[[HW3-幂律-阈值-SIR与影响力实验]]，比较确定性阈值与随机传播。
- 下游：[[影响力最大化与贪心算法]]，从“给定起点求规模”进入“选择起点最大化规模”。
- 作业：Stanford CS224W 2017 HW3-Q1(a-c)。

### 10. 闭卷复现任务

- [ ] 定义 $N_\ell$ 与 $C(k)$。
- [ ] 写出阈值 $\ell$ 组激活的全部不等式。
- [ ] 用归纳法证明充分性。
- [ ] 证明必要性。
- [ ] 定义首个失败阈值 $k^\star$。
- [ ] 证明首个失败点处 $C(k^\star-1)=k^\star-1$。
- [ ] 写最终人数的最小固定点表达。
- [ ] 证明迭代会到达该固定点。
- [ ] 从累计图与对角线交点读最终人数。
- [ ] 运行 loader、断言和绘图，不泄漏/虚构失效数据答案。

### 11. 自测题：5 道

1. 阈值为 3 的人能够激活，需要哪三条不等式？ #自测题/基础
   > [!question]- $C(0)\ge1$、$C(1)\ge2$、$C(2)\ge3$。
2. 为什么累计只到 $k-1$？ #自测题/基础
   > [!question]- 越过阈值 $k$ 前只能依赖阈值小于 $k$ 且已经能激活的人；题面计数的是其他参与者。
3. 首个失败阈值为 $k^\star$ 时，为什么最终恰是 $k^\star-1$？ #自测题/中等
   > [!question]- 前一条件给 $C(k^\star-2)\ge k^\star-1$，失败条件给 $C(k^\star-1)<k^\star$；整数性与单调性迫使 $C(k^\star-1)=k^\star-1$。
4. $N=(2,0,1,2,0)$ 的最终人数是多少？ #自测题/中等
   > [!question]- $C=(2,2,3,5,5)$；对 $k<5$ 均有 $C(k)>k$，扩展 $C(5)=5$，所以最终 5。
5. 为什么 $R=\min\{k:C(k)=k\}$ 而不是最大固定点？ #自测题/较难
   > [!question]- 从 $N_0$ 出发的单调闭包遇到第一个固定点就无法越过；更大的固定点可能存在但不可达。

### 12. 我的主动回忆区

#### 我的闭卷复述
> 不看上文，说明累计曲线为什么在最终人数前高于对角线，并在最终人数处第一次相等。

#### 我的推导复现
> 写出 Q1(a) 必要/充分证明，以及“首个失败阈值 = 最小固定点”的等价证明。

#### 我的错误与卡点
- [ ] 下标偏移 → 明确题面计算“其他人”，越过 $k$ 前累计到 $k-1$。
- [ ] 只会迭代不会证明 → 先写逐层不等式，再做必要性和归纳充分性。
- [ ] 图像交点读错 → 检查第一次 $C(k)=k$，并用迭代 history 交叉验证。

#### 失败后的回流
- 定义/下标错：第 5.1–5.2 节；证明错：第 6 节；图像/代码错：第 7.3 节；模型混淆：第 8 节。

#### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

### 13. 给 Obsidian 的归档建议

- 文件夹：05-传播与影响力。
- 关联：[[阈值模型与网络级联]]、[[影响力最大化与贪心算法]]。
- 标签：#HW3、#全局阈值、#归纳证明。
- 拆分建议：Q1(a-c) 共享同一累计函数与固定点证明，保持一张作业推导卡。

### 🃏 Anki 卡片

- HW3-Q1 阈值 $\ell$ 组激活的条件？::对每个 $k=1,\ldots,\ell$ 都有 $C(k-1)\ge k$。
- 全局阈值最终人数的固定点表达？::$R=\min\{k\in\{0,\ldots,n\}:C(k)=k\}$，扩展 $C(n)=n$。
- 累计直方图怎样读最终人数？::找累计曲线 $C(k)$ 与对角线 $y=k$ 第一次相等的位置；此前必须有 $C(k)>k$。

## 原笔记：HW3-SIR统计检验与种子实验

### 0. 先判断它值不值得深挖
- **类别**：A 类作业实验。
- **判断理由**：只实现一次 SIR 不足以完成 HW3；必须区分疫情发生率、无条件均值、条件均值、显著性和种子策略相对增幅。

### 1. 这个知识点解决什么问题？
> 怎样在 IMDB、ER 与 PA 三张规模/平均度匹配的图上公平比较随机种子、高度种子、单种子和十种子，并避免把“更容易爆发”与“爆发后规模更大”混为一谈？

### 2. 为什么它重要？它有什么用？
- 将随机传播模型升级成可解释统计实验。
- 区分网络结构对“起飞概率”和“条件最终规模”的不同影响。
- 覆盖 HW3-Q3.0–Q3.4 的全部指标与解释。

### 3. 学它之前需要哪些前置知识？
1. [[SIR网络流行病模型]]。
2. [[../06-表示学习与项目/可复现网络挖掘实验]]。
3. $2\times2$ 列联表、卡方近似和相对变化。

### 4. 用直觉语言解释它
> “点火是否成功”和“成功后烧多大”是两件事；hub 像大火种，社区边界像防火带。”
- **一句话本质**：用结果分布而非单轨迹，分解种子、度异质和社区结构的作用。

### 5. 正式定义、核心公式、符号解释

#### 1. 同步 SIR
每轮仅使用轮初状态。易感节点有 $d_I$ 个感染邻居时：
$$P(S\to I)=1-(1-\beta)^{d_I},$$
感染节点以概率 $\delta$ 恢复。终止时累计感染比例 $Y=|R|/|V|$。

#### 2. 三个必须分开的汇总量
设疫情阈值 $\tau=0.5$，共 $R=100$ 次：
$$\widehat p_{epi}=R^{-1}\sum_r\mathbb I[Y_r\ge\tau],$$
$$\bar Y=R^{-1}\sum_rY_r,$$
$$\bar Y_{epi}=\frac{\sum_rY_r\mathbb I[Y_r\ge\tau]}{\sum_r\mathbb I[Y_r\ge\tau]}.$$
若没有疫情，条件均值应报告 `NA`，不能填 0。

#### 3. 两图疫情率的卡方检验
若两图疫情次数为 $e_1,e_2$：
$$
O=\begin{bmatrix}e_1&R-e_1\\e_2&R-e_2\end{bmatrix}.
$$
Pearson 统计量 $\chi^2=\sum_{ij}(O_{ij}-E_{ij})^2/E_{ij}$，自由度 1。期望频数过小或某列全 0 时，卡方近似不可靠；HW3 后续高度种子可能 100/100 疫情，因此题面明确跳过检验。

#### 4. 高度种子的相对影响
随机种子与高度种子的**无条件**平均最终比例分别为 $\bar Y_{random},\bar Y_{target}$：
$$\text{relative increase}=\frac{\bar Y_{target}-\bar Y_{random}}{\bar Y_{random}}.$$
必须声明分母；若分母为 0，改报绝对差。

#### 5. 单种子与十种子
- 单随机节点 vs 最高度节点。
- 十个随机节点 vs 十个最高度节点。
- 度并列时用固定规则（如节点 ID）或记录随机 tie-breaking。
- 比较种子策略时可用共同随机数流降低 Monte Carlo 差异，但每张图仍需独立传播随机性。

### 6. 推导思路和思想来源
1. 传播结果常呈“快速熄灭/大疫情”混合分布，均值无法单独描述。
2. 疫情率回答起飞概率；条件均值回答已经起飞后的严重程度。
3. 卡方检验只比较二元疫情事件，不比较最终比例分布。
4. PA 的 hub 可显著提高点火成功率，但社区结构可能限制跨群扩散。
5. 初始种子从 1 增加到 10 后，随机策略更可能自行命中 hub/多个社区，高度定向的相对增益可能下降；实际结论必须由数据支持。

### 7. 例子：已解 → 半提示 → 可运行实验

#### 例子 1：已解
100 次中 35 次达到 50%，无条件均值 0.31，疫情样本均值 0.72：报告三者分别为 0.35、0.31、0.72，不能说“平均疫情规模 31%”而不注明是否条件化。

#### 例子 2：半提示
随机种子无条件均值 0.20，高度种子 0.35，相对增幅为 `____`。
> [!question]- 核对
> $(0.35-0.20)/0.20=0.75$，即 75%。

#### 例子 3：可运行统计骨架
```python
import random
import math
import networkx as nx
from scipy.stats import chi2_contingency

def sir_once(graph, seeds, beta=0.05, delta=0.5, rng=None):
    rng = rng or random.Random(0)
    infected = set(seeds)
    susceptible = set(graph) - infected
    recovered = set()
    while infected:
        new_infected = set()
        for node in susceptible:
            infected_neighbors = sum(neighbor in infected for neighbor in graph[node])
            if infected_neighbors and rng.random() < 1 - (1 - beta) ** infected_neighbors:
                new_infected.add(node)
        new_recovered = {node for node in infected if rng.random() < delta}
        susceptible -= new_infected
        infected = (infected | new_infected) - new_recovered
        recovered |= new_recovered
    return len(recovered) / graph.number_of_nodes()

def run_trials(graph, seed_sets, random_seed=0):
    rng = random.Random(random_seed)
    return [sir_once(graph, seeds, rng=rng) for seeds in seed_sets]

def summarize(values, threshold=0.5):
    epidemic = [value for value in values if value >= threshold]
    return {
        "epidemics": len(epidemic),
        "epidemic_rate": len(epidemic) / len(values),
        "mean": sum(values) / len(values),
        "conditional_mean": (sum(epidemic) / len(epidemic) if epidemic else math.nan),
    }

def chi_square(first, second, trials):
    table = [[first, trials - first], [second, trials - second]]
    if any(sum(row) == 0 for row in table) or any(sum(table[r][c] for r in range(2)) == 0 for c in range(2)):
        return math.nan, math.nan
    statistic, p_value, _, expected = chi2_contingency(table, correction=False)
    if expected.min() < 5:
        return math.nan, math.nan
    return statistic, p_value

# Unit tests force the statistical branches even if a toy graph has no epidemic.
known = summarize([0.1, 0.6, 0.8, 0.2], threshold=0.5)
assert known == {"epidemics": 2, "epidemic_rate": 0.5,
                 "mean": 0.425, "conditional_mean": 0.7}
known_chi2 = chi_square(30, 50, 100)
assert all(math.isfinite(value) for value in known_chi2)
assert all(math.isnan(value) for value in chi_square(0, 0, 100))

graphs = {
    "ER": nx.gnm_random_graph(80, 160, seed=1),
    "PA": nx.barabasi_albert_graph(80, 2, seed=1),
}
summaries = {}
for name, graph in graphs.items():
    rng = random.Random(7)
    random_seeds = [{rng.choice(list(graph))} for _ in range(40)]
    values = run_trials(graph, random_seeds, random_seed=11)
    summaries[name] = summarize(values)
print(summaries)
print(chi_square(summaries["ER"]["epidemics"], summaries["PA"]["epidemics"], 40))
# 输出每图疫情数/率、无条件/条件均值及 ER-PA 的卡方统计量与 p 值。
```

#### 正式作业协议
- 三图：IMDB、课程提供 ER、课程提供 PA；核对节点数和平均度。
- 2017 题面中的三张图数据 URL 当前返回 404；未取得课程方合法归档副本时，只能验证算法和统计分支，必须把正式图结果标记为“未验证”，不能用本卡 ER/PA 玩具图代替。
- $\beta=0.05,\delta=0.5$，每条件 100 次。
- Q3.1：单随机种子，报告三指标；三图两两卡方检验。
- Q3.2：单最高度种子；不做卡方；对 ER/PA 报无条件均值相对增幅。
- Q3.3：结合 IMDB 社区结构解释疫情率和条件规模，禁止只引用“真实图更复杂”。
- Q3.4：十随机 vs 十最高度，仍报三指标和相对影响变化。

### 8. 常见误区和易混概念
- 新感染者同轮继续感染：改变离散时间模型。
- 只报条件均值：隐藏大量快速熄灭。
- 条件均值分母用 100：应只除以疫情次数。
- 100/100 疫情仍做卡方：期望表退化，题面要求跳过。
- 比较高度种子时用不同 $\beta,\delta$ 或不同图规模：失去可比性。

| 指标 | 回答问题 | 不能替代 |
| :--- | :--- | :--- |
| 疫情率 | 多容易起飞 | 疫情后规模 |
| 无条件均值 | 总体期望负担 | 双峰结构 |
| 条件均值 | 起飞后多严重 | 起飞概率 |
| 卡方 | 疫情率差异证据 | 连续规模差异 |

### 9. 相关知识点与 Obsidian 双链建议
- 上游：[[SIR网络流行病模型]]。
- 横向：[[../03-社会结构与社区/社区发现-模块度与谱松弛]]、[[../04-排序与链接预测/中心性度量]]。
- 实验：[[../06-表示学习与项目/可复现网络挖掘实验]]。
- 作业：CS224W 2017 HW3-Q3.0–Q3.4。

### 10. 闭卷复现任务
- [ ] 写同步状态更新。
- [ ] 推多邻居感染概率。
- [ ] 定义三种汇总量。
- [ ] 构造卡方表。
- [ ] 识别卡方退化。
- [ ] 写相对增幅。
- [ ] 统一随机/高度种子协议。
- [ ] 完成 100 次模拟。
- [ ] 比较单/十种子。
- [ ] 从结果解释社区效应。

### 11. 自测题：5 道
1. 无疫情时条件均值应填什么？ #自测题/基础
   > [!question]- `NA/NaN`，不能填 0。
2. 疫情率和条件均值分别回答什么？ #自测题/基础
   > [!question]- 是否起飞的概率；已起飞时的平均最终规模。
3. 卡方表的两列是什么？ #自测题/中等
   > [!question]- 疫情次数与非疫情次数。
4. 为什么 Q3.2 可能不做卡方？ #自测题/中等
   > [!question]- 高度种子可能使某图 100/100 疫情，列联表退化、近似不适用。
5. 十种子后高度定向相对增益为何可能下降？ #自测题/较难
   > [!question]- 十个随机种子更可能覆盖 hub 与多个社区，缩小与定向策略的差距；需由实验验证。

### 12. 我的主动回忆区
#### 我的闭卷复述
> 用“起飞概率—总体负担—条件严重度—显著性”四层解释 SIR 结果。
#### 我的推导复现
> 写出列联表、条件均值与相对增幅，重建单/十种子协议。
#### 我的错误与卡点
- [ ] 指标混淆 → 回看第 5.2 节。
- [ ] 卡方报错 → 检查退化表与期望频数。
- [ ] 结果不可复现 → 检查 seed、图版本和同步更新。
#### 失败后的回流
- 模型错：[[SIR网络流行病模型]]；统计错：第 5 节；代码错：第 7.3 节。

### 13. 给 Obsidian 的归档建议
- 文件夹：`05-传播与影响力/`
- 关联：[[SIR网络流行病模型]]
- 标签：`#HW3` `#SIR实验` `#卡方`
- 拆分建议：四个子题共享同一模拟与指标协议，保持一张卡。

### 🃏 Anki 卡片
- SIR 作业的三种核心汇总？::疫情率、无条件平均最终感染比例、疫情条件下平均最终感染比例。
- 两图疫情率卡方表？::$\begin{bmatrix}e_1&R-e_1\\e_2&R-e_2\end{bmatrix}$。
- 高度种子相对增幅用哪个均值？::相对随机种子的无条件平均最终感染比例。

## 原笔记：HW3-影响力最大化-反例最优条件与后验界

### 0. 先判断它值不值得深挖
- **类别**：A 类构造题。
- **判断理由**：Q4 要求主动造集合族，不是复述次模近似比；必须控制贪心每步边际、最优集合和上界松弛量。

### 1. 这个知识点解决什么问题？
> 怎样系统构造贪心非最优、预算 3 时不超过最优 80%、贪心必最优的充分条件，以及后验上界任意松的实例族？

### 2. 为什么它重要？它有什么用？
- 训练从算法选择规则反向设计输入。
- 区分“近似保证”“某类实例最优”和“上界紧”。
- 完整覆盖 HW3-Q4.1–Q4.4 的构造能力，不复制作业指定答案。

### 3. 学它之前需要哪些前置知识？
1. [[影响力最大化与贪心算法]]。
2. 集合并、边际覆盖与反证。

### 4. 用直觉语言解释它
> “诱饵集合每一步都比单个正确块多一点，但三步后留下大量分散残余；后验上界则把多个不能同时兑现的未来边际一起相加。”
- **一句话本质**：反例设计要操纵局部边际排序，上界松弛来自把互斥改进当成可同时获得。

### 5. 正式定义、核心公式、符号解释

#### 1. 确定性影响集合
每个候选节点 $u$ 有影响集合 $X_u$，包含自身及最终可达节点：
$$f(S)=\left|\bigcup_{u\in S}X_u\right|,\qquad
\Delta(u\mid S)=|X_u\setminus\cup_{v\in S}X_v|.$$

#### 2. 预算 2 非最优构造原则
设置一个最大单集诱饵 $A$，它分别与两个互补集合 $B,C$ 大量重叠；令 $|A|>|B|,|C|$ 迫使先选 $A$，但 $|B\cup C|>|A\cup B|,|A\cup C|$。

#### 3. 预算 3、比例不超过 0.8 的同构训练族
建立三个互不相交的最优块 $O_1,O_2,O_3$，各 27 个元素。每块划分为大小 `9,6,4,8` 的四层。三个诱饵：
- $D_1$ 覆盖每块第一层，并有 1 个私有元素：边际 28；
- $D_2$ 覆盖每块第二层，并有 1 个私有元素：在 $D_1$ 后边际 19；
- $D_3$ 覆盖每块第三层，并有 1 个私有元素：前两步后边际 13。

贪心被依次诱导选择 $D_1,D_2,D_3$，总覆盖 $28+19+13=60$。最优选 $O_1,O_2,O_3$ 覆盖 81，比例
$$60/81\approx0.741\le0.8.$$
这是独立训练构造；完成官方作业时应自行重新命名/重建并逐步验证所有候选边际。

#### 4. 贪心必最优的充分条件
若所有候选影响集合两两不交：
$$u\ne v\Rightarrow X_u\cap X_v=\varnothing,$$
则 $\Delta(u\mid S)=|X_u|$ 与已选集合无关，贪心选最大的 $k$ 个集合，显然也是最优。该条件充分但不必要。

#### 5. 后验上界任意松的实例族
给定预算 $k\ge1$ 和任意 $M$，构造 $k+1$ 个两两不交、大小均为 $M$ 的根影响集合；其他普通节点仅影响自身。贪心选任意 $k$ 个根，已是最优：
$$f(S_k)=f(T)=kM.$$
但未选的第 $k+1$ 个根在 $S_k$ 后仍有边际 $M$，其余边际非负。若 $\delta_1,\ldots,\delta_k$ 是剩余最大 $k$ 个边际，则
$$f(S_k)+\sum_{i=1}^k\delta_i-f(T)\ge M.$$
取 $M>b$ 即使差值超过任意给定 $b$。因此上界可任意松，即使贪心解本身已经最优。

### 6. 推导思路和思想来源
1. 先写出希望的贪心选择顺序，再为每步设置严格边际不等式。
2. 用互补最优块保存全局价值，用横切诱饵制造局部优势。
3. 私有元素只用于打破平局，数量必须小到不改变最优解。
4. 最优条件证明应直接让边际不依赖历史。
5. 上界松弛不要求贪心差；只需存在一个大剩余边际被上界额外相加。

### 7. 例子：已解 → 半提示 → 可运行验证

#### 例子 1：预算 2 已解
$X_a=\{1,2,3,4\}$，$X_b=\{1,2,5\}$，$X_c=\{3,4,6\}$。贪心先选 $a$，第二步最多加 1，总 5；$b,c$ 联合覆盖 6。

#### 例子 2：半提示
三块各 27，前三层共 `9+6+4=19`。诱饵私有元素共 3 个，贪心覆盖 `3×19+3=____`，最优覆盖 `____`。
> [!question]- 核对
> 60；81。

#### 例子 3：可运行构造验证
```python
def greedy(sets, budget):
    chosen, covered = [], set()
    for _ in range(budget):
        node = max((name for name in sets if name not in chosen),
                   key=lambda name: (len(sets[name] - covered), name))
        chosen.append(node)
        covered |= sets[node]
    return chosen, covered

blocks = {}
for block in range(3):
    universe = [f"b{block}_{index}" for index in range(27)]
    blocks[f"O{block+1}"] = set(universe)

sets = dict(blocks)
cuts = [(0, 9), (9, 15), (15, 19)]
for layer, (left, right) in enumerate(cuts, 1):
    decoy = {f"b{block}_{index}" for block in range(3) for index in range(left, right)}
    decoy.add(f"private_{layer}")
    sets[f"D{layer}"] = decoy

chosen, covered = greedy(sets, 3)
optimal = set().union(*(sets[f"O{index}"] for index in range(1, 4)))
print(chosen, len(covered), len(optimal), round(len(covered) / len(optimal), 3))
assert chosen == ["D1", "D2", "D3"]
assert len(covered) / len(optimal) <= 0.8
# 输出：['D1','D2','D3'] 60 81 0.741
```

### 8. 常见误区和易混概念
- 只比较第一步集合大小：必须验证每一步剩余边际。
- 用平局但未声明 tie-breaking：构造可能不保证贪心走指定路径。
- 给出 0.8 比例却未证明最优值：需排除诱饵混合方案更优。
- 把“两两不交”说成必要条件：它只是一个充分条件。
- 后验上界族只给一个大实例：必须用参数 $M$ 对任意 $b$ 构造。

| 任务 | 设计目标 | 验收 |
| :--- | :--- | :--- |
| 非最优 | 局部最大诱饵 | 贪心值 < 最优值 |
| ≤0.8 | 多步诱饵 | 逐步边际 + 比例 |
| 必最优条件 | 边际历史无关 | 证明选 top-k |
| 任意松上界 | 大剩余边际 | 参数化差值 > b |

### 9. 相关知识点与 Obsidian 双链建议
- 上游：[[影响力最大化与贪心算法]]。
- 横向：[[../03-社会结构与社区/社区发现-模块度与谱松弛]]。
- 应用：CS224W 2017 HW3-Q4.1–Q4.4。

### 10. 闭卷复现任务
- [ ] 写确定性覆盖形式。
- [ ] 构造预算 2 反例。
- [ ] 写预算 3 分层诱饵。
- [ ] 逐步验证三个边际。
- [ ] 证明 60/81≤0.8。
- [ ] 排除混合方案优于三最优块。
- [ ] 给出充分条件并证明。
- [ ] 构造参数化后验界族。
- [ ] 解释为何贪心可最优而界仍松。
- [ ] 用代码验证构造。

### 11. 自测题：5 道
1. 反例构造先控制什么？ #自测题/基础
   > [!question]- 每一步贪心边际的排序，而不只是初始集合大小。
2. 私有元素的用途？ #自测题/基础
   > [!question]- 小幅打破平局，强制贪心顺序。
3. 两两不交为何使贪心最优？ #自测题/中等
   > [!question]- 每个集合边际恒等于自身大小，选择 top-k 即最优。
4. 后验界松是否意味着贪心解差？ #自测题/中等
   > [!question]- 不意味着；给出的实例中贪心本身最优，但上界仍额外计入大剩余边际。
5. 如何让上界差超过任意 $b$？ #自测题/较难
   > [!question]- 将未选独立影响块大小设为参数 $M>b$。

### 12. 我的主动回忆区
#### 我的闭卷复述
> 用“最优块—横切诱饵—私有打破平局”复述预算 3 构造。
#### 我的推导复现
> 独立验证三步边际、最优值和后验界参数族。
#### 我的错误与卡点
- [ ] 贪心顺序不唯一 → 检查私有元素和 tie-breaking。
- [ ] 比例不够低 → 调整层大小但重新证明全局最优。
- [ ] 上界族不参数化 → 显式引入 $M>b$。
#### 失败后的回流
- 定义错：[[影响力最大化与贪心算法]]；构造错：第 5.3 节；上界错：第 5.5 节。

### 13. 给 Obsidian 的归档建议
- 文件夹：`05-传播与影响力/`
- 关联：[[影响力最大化与贪心算法]]
- 标签：`#HW3` `#构造题` `#贪心反例`
- 拆分建议：四类题共享集合覆盖构造语言，保持一张推导卡。

### 🃏 Anki 卡片
- 怎样系统制造贪心反例？::先设计每步边际排序，用跨越多个最优块的诱饵获得局部优势，同时保留互补最优块的全局价值。
- 一个使贪心必最优的充分条件？::所有候选影响集合两两不交，此时边际恒等于集合大小，贪心选择 top-k。
- 后验上界为何可任意松？::未选的大独立影响块仍贡献巨大剩余边际，被上界额外相加，即使贪心解已经最优。
