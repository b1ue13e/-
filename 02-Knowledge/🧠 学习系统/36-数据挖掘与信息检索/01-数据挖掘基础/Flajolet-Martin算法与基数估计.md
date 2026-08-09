---
type: study
topic: "Flajolet-Martin算法与基数估计"
course: "数据挖掘与信息检索"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段1-数据挖掘基础]]"
flow: knowledge
kind: concept
upstream: ["[[DGIM算法与流数据计数]]"]
tags: [学习, 数据挖掘与信息检索, 流数据]
---
## 💡 动机与直觉

在海量流数据场景中（例如统计网站在过去一个月内的独立访客数 UV、IP 去重数、搜索词去重数），假设流中包含 $N$ 个元素，其中非重复元素（Distinct Elements）的数量为 $V$。

- **朴素方案**：使用哈希表 (HashSet) 记录所有见过的元素。空间复杂度为 $\mathcal{O}(V)$，当 $V = 10^9$ 时需要数十 GB 内存。
- **Flajolet-Martin (FM) 算法**：利用均匀哈希函数的尾随零（Trailing Zeros）几何分布特性，仅需 $\mathcal{O}(\log V)$ 比特内存即可估算基数 $V$。现代可扩展改进版即为广泛应用于 Redis、ClickHouse 和 Apache Spark 中的 **HyperLogLog (HLL)**。

```
输入流 x ──▶ [哈希映射 h(x)] ──▶ [二进制尾随零计数 ρ(h(x))] ──▶ 更新位图/最大值 R ──▶ 估计 V = 2^R / 0.77351
```

---

## 📐 算法原理与严密数学推导

### 1. 尾随零函数 $\rho(y)$ 与几何分布
定义一个将流数据元素无偏映射到 $L$ 位二进制整数的哈希函数 $h(x) \in [0, 2^L - 1]$。
定义函数 $\rho(y)$ 为二进制数 $y$ 末尾连续 $0$ 的个数：
- 例如：$\rho(010100_2) = 2$，$\rho(110000_2) = 4$。

对于任意输入元素 $x$，若哈希函数具有强随机均匀性，其哈希值每一位产生 0 或 1 的概率独立且为 $1/2$。
末尾恰好出现 $r$ 个 0（即末尾形式为 $1\underbrace{00\dots0}_{r\text{个}}$）的概率服从几何分布：
$$P(\rho(h(x)) = r) = \left(\frac{1}{2}\right)^{r+1}$$

### 2. 极值 $R = \max \rho(h(x))$ 的期望分析
设流中共有 $V$ 个互不相同的元素。定义指示变量：
$$P(\rho(h(x)) \ge r) = \left(\frac{1}{2}\right)^r = 2^{-r}$$

对于全部 $V$ 个元素，**没有任何一个元素**产生 $\ge r$ 个尾随零的概率为：
$$P(\text{all } \rho(h(x_i)) < r) = \left(1 - 2^{-r}\right)^V \approx e^{-V \cdot 2^{-r}}$$

令 $t = V \cdot 2^{-r}$：
- 当 $2^r \ll V$ 时，$t \to \infty$，$e^{-t} \approx 0$，即几乎必然会出现至少一个元素的尾随零 $\ge r$；
- 当 $2^r \gg V$ 时，$t \to 0$，$e^{-t} \approx 1$，即几乎必然没有任何元素的尾随零能达到 $r$；
- **转折相变点**（Inflection Point）发生在 $2^r \approx V$，即 $r \approx \log_2 V$。

### 3. 偏差修正常数 $\phi \approx 0.77351$ 的推导来源
Philippe Flajolet 和 G. Nigel Martin 在 1985 年的原论文中通过泊松发生函数与 Mellin 变换积分证明：
$$\mathbb{E}[R] = \log_2(\phi V) + \mathcal{O}(1)$$
其中常数因子 $\phi$ 严格满足：
$$\phi = e^{-\gamma} \sqrt{2} \prod_{k=1}^\infty \left(\frac{2k+1}{2k}\right)^{(-1)^k} \approx 0.77351$$
（其中 $\gamma \approx 0.57721566$ 为欧拉-马歇罗尼常数）。
因此，无偏基数估计量公式为：
$$\hat{V} = \frac{2^R}{\phi} \approx \frac{2^R}{0.77351}$$

### 4. 减小方差：分组调和平均 (Bucket Averaging to HyperLogLog)
单哈希估计方差过大（标准差 $\sigma \approx 1.12$），直接算术平均容易受极端大尾随零干扰。
- **LogLog 方案**：将哈希空间划分为 $m$ 个分桶（利用哈希前 $p$ 位作为桶编号 $m = 2^p$），对各桶的 $R_j$ 取算术平均。
- **HyperLogLog (HLL) 方案**：改用**调和平均数（Harmonic Mean）**抑制极端异常值：
$$\hat{V}_{\text{HLL}} = \alpha_m \cdot m^2 \cdot \left( \sum_{j=1}^m 2^{-R_j} \right)^{-1}$$
标准差大幅下降至 $\sigma \approx \frac{1.04}{\sqrt{m}}$。

---

## 💻 生产级 Python 模块实现

在工程模块 `src/stream_mining.py` 中，实现了多哈希分组调和平均的基数估计器：

```python
import math
from typing import List

class FlajoletMartinEstimator:
    PHI = 0.77351

    def __init__(self, num_hashes: int = 16, num_groups: int = 4):
        self.num_hashes = num_hashes
        self.num_groups = num_groups
        self.p = 2147483647  # 梅森素数
        self.hash_params = []
        for i in range(num_hashes):
            a = (i * 10007 + 3) % (self.p - 1) + 1
            b = (i * 20011 + 7) % self.p
            self.hash_params.append((a, b))
        self.max_trailing_zeros = [0] * num_hashes

    @staticmethod
    def trailing_zeros(val: int) -> int:
        if val == 0:
            return 32
        count = 0
        while (val & 1) == 0:
            count += 1
            val >>= 1
        return count

    def add(self, item: str):
        raw_hash = hash(item) & 0x7FFFFFFF
        for i, (a, b) in enumerate(self.hash_params):
            h_val = (a * raw_hash + b) % self.p
            tz = self.trailing_zeros(h_val)
            if tz > self.max_trailing_zeros[i]:
                self.max_trailing_zeros[i] = tz

    def estimate_cardinality(self) -> float:
        hashes_per_group = self.num_hashes // self.num_groups
        group_estimates = []
        for g in range(self.num_groups):
            group_r = self.max_trailing_zeros[g * hashes_per_group:(g + 1) * hashes_per_group]
            avg_r = sum(group_r) / len(group_r)
            group_estimates.append((2.0 ** avg_r) / self.PHI)
            
        group_estimates.sort()
        mid = len(group_estimates) // 2
        return group_estimates[mid]
```

---

## ⚠️ 工业避坑指南与四大基数估计结构对比

| 数据结构 | 解决问题 | 空间复杂度 | 查询误差 | 支持操作 | 工业应用场景 |
|:---|:---|:---|:---|:---|:---|
| **Flajolet-Martin / HLL** | 唯一基数估计 (UV/Distinct Count) | $\mathcal{O}(\log \log V)$ (1.5KB/百万) | $1.04/\sqrt{m} \approx 1\%$ | 插入, 合并 (Bitwise OR), 估计 | Redis `PFADD/PFCOUNT`, ClickHouse |
| **Bloom Filter** | 集合成员存在性判断 (Membership) | $\mathcal{O}(V)$ 比特 | 存在假阳性 (False Positive)，无假阴性 | 插入, 查询 (不可删除) | 爬虫 URL 去重, LSM 树读过滤 |
| **Count-Min Sketch** | 元素频次估计 (Frequency/Top-K) | $\mathcal{O}(w \times d)$ | 估计值 $\ge$ 真实值 (单向过估计) | 插入, 点查询, 内积 | 网络流量大象流 (Heavy Hitters) |
| **DGIM** | 滑动窗口内二进制 1 计数 | $\mathcal{O}(\log^2 N)$ | 相对误差 $\le 50\%$ | 插入, 滑窗求和 | 流计算风控近期交易频次 |

---

## 🃏 Anki 卡片

**Q: 为什么 Flajolet-Martin 估计基数时需要除以常数 $\phi \approx 0.77351$？**
**A**:
- 几何分布末尾零极大值 $R = \max \rho(h(x))$ 的期望并非直接等于 $\log_2 V$，而是 $\mathbb{E}[R] \approx \log_2(\phi V)$；
- 常数 $\phi = e^{-\gamma} \sqrt{2} \prod_{k=1}^\infty (\frac{2k+1}{2k})^{(-1)^k} \approx 0.77351$ 是通过泊松化极限修正离散跳跃偏差的无偏因子。

---

## 🔗 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```