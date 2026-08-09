---
type: study
topic: "DGIM算法与流数据计数"
course: "数据挖掘与信息检索"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段1-数据挖掘基础]]"
flow: knowledge
kind: concept
upstream: ["[[数据挖掘概述]]"]
tags: [学习, 数据挖掘与信息检索]
---
## 💡 动机与直觉

在海量实时流数据（如日志流、网络数据包、交易监控）场景下，假设我们希望维护一个最近 $N$ 个时间步的滑动窗口（Sliding Window），并回答问题：“在过去 $N$ 个二进制比特中，有多少个 $1$？”

- **朴素方案**：将最近 $N$ 个比特全量保存在内存中。存储复杂度为 $\mathcal{O}(N)$。当 $N = 10^9$ 或更大时，内存开销不可接受。
- **DGIM 算法 (Datar-Gionis-Indyk-Motwani)**：使用极其紧凑的指数桶（Exponential Buckets）结构，仅消耗 $\mathcal{O}(\log^2 N)$ 的内存位（Bits），即可在连续二进制数据流中估算最近 $N$ 个时间步内 $1$ 的个数，且相对误差界不超过 50%（经过调优可缩小至任意 $\epsilon > 0$）。

```
时间轴流 (Stream): ... 1 0 1 1 0 1 1 1 0 1 1 0 0 1 0 1 ...
                               └─── 最近 N 个比特滑动窗口 ───┘
DGIM 桶 (Buckets): [桶大小=1] [桶大小=1] [桶大小=2] [桶大小=2] [桶大小=4] ...
```

---

## 📐 算法原理与规约

### 1. DGIM 桶规约 (Bucket Rules)
DGIM 算法将滑动窗口内的 $1$ 划分为若干个**桶 (Bucket)**。每个桶由“最右侧 $1$ 的时间戳（Timestamp）”和“桶的大小（Size，即桶内 $1$ 的数量）”决定。

1. **桶的大小**：每个桶的大小 $S$ 必须是 $2$ 的幂次（即 $S = 2^j, j \ge 0$）。
2. **桶的分布**：对于任意给定的大小 $S$：
   - 最多只能有 **2 个** 大小为 $S$ 的桶。
   - 至少有 **1 个** 大小为 $S$ 的桶（除最大尺寸外）。
3. **桶的时间戳单调性**：桶按时间戳由近到远排序，桶的大小随时间呈非严格单调递增。
4. **窗口过期**：任何最左侧（最老）的桶，若其时间戳落在滑动窗口 $N$ 之外，将被物理剔除。

### 2. 估计公式与误差界

当查询过去 $N$ 个时间步内 $1$ 的总数时：
- **统计方式**：求所有完全包含在窗口内的桶的大小之和，加上**最老（最左侧）的桶的大小的一半**。

$$\hat{c} = \sum_{\text{完全在窗口内}} S_i + \frac{1}{2} S_{\text{oldest}}$$

- **误差分析**：由于最老桶中只有部分 $1$ 可能落入窗口内，最大绝对误差小于等于 $\frac{1}{2} S_{\text{oldest}}$。基于桶尺寸为 2 的幂次约束，其**最大相对误差不超过 50%**。

---

## 💻 最小 Python 实现

```python
import math
from collections import deque

class DGIMBucket:
    def __init__(self, timestamp: int, size: int):
        self.timestamp = timestamp
        self.size = size

class DGIMStreamCounter:
    def __init__(self, window_size: int):
        self.N = window_size
        self.current_time = 0
        self.buckets = deque()  # 存放桶，队头为最新，队尾为最老

    def update(self, bit: int):
        self.current_time += 1
        # 1. 物理过期清理
        while self.buckets and (self.current_time - self.buckets[-1].timestamp >= self.N):
            self.buckets.pop()

        if bit != 1:
            return

        # 2. 插入新元素（大小为 1 的桶）
        new_bucket = DGIMBucket(self.current_time, 1)
        self.buckets.appendleft(new_bucket)

        # 3. 级联合并桶 (Merge Buckets of same size)
        self._check_and_merge()

    def _check_and_merge(self):
        # 从队头开始扫描，若发现有 3 个相同大小的桶，则合并后两个（较老的那两个）
        i = 0
        while i < len(self.buckets) - 2:
            b1 = self.buckets[i]
            b2 = self.buckets[i+1]
            b3 = self.buckets[i+2]
            if b1.size == b2.size == b3.size:
                # 合并 b2 和 b3
                merged_bucket = DGIMBucket(b2.timestamp, b2.size * 2)
                self.buckets[i+1] = merged_bucket
                self.buckets.remove(b3)
                # 重新扫描合并可能引发的连带合并
                i = max(0, i - 1)
            else:
                i += 1

    def count_ones(self) -> int:
        if not self.buckets:
            return 0
        total = 0
        for i in range(len(self.buckets) - 1):
            total += self.buckets[i].size
        # 最老的桶取一半估计
        total += self.buckets[-1].size // 2
        return total

# 单元测试样例
if __name__ == "__main__":
    dgim = DGIMStreamCounter(window_size=10)
    stream = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0]
    for b in stream:
        dgim.update(b)
    print(f"窗口 N=10 估计的 1 的数量: {dgim.count_ones()}")
```

---

## ⚠️ 常见误区与避坑指南

1. **误区 1：认为 DGIM 可以估算任意数值**
   - 避坑：朴素 DGIM 仅适用于二进制流（0 和 1）计数。如需估算正整数之和，需将数值按二进制位分解为 $\log M$ 个独立的 DGIM 实例进行并行计算。
2. **误区 2：合并最新两个桶**
   - 避坑：出现 3 个相同大小的桶时，必须合并**较老的那两个桶**（即时间戳靠前的两个），以保证时间戳的单调性和桶大小的单调递增规律。

---

## 🃏 Anki 卡片

**Q: DGIM 算法核心解决什么问题？时间复杂度与空间复杂度是多少？**
**A**:
- **问题**：在海量二进制数据流中，以极小的空间估算最近 $N$ 个滑动窗口内 $1$ 的个数。
- **空间复杂度**：$\mathcal{O}(\log^2 N)$ Bits（对比朴素保存的 $\mathcal{O}(N)$）。
- **相对误差界**：不超过 50%。

---

---

## 🔗 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```