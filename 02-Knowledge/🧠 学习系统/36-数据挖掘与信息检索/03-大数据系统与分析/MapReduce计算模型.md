---
type: study
topic: "MapReduce计算模型"
course: "数据挖掘与信息检索"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段3-大数据系统与分析]]"
flow: knowledge
kind: concept
upstream: ["[[HDFS与分布式存储]]"]
tags: [学习, 数据挖掘与信息检索]
---
## 💡 直觉与动机

MapReduce 是 Google 2004 年提出的**分布式批处理编程模型**，核心思想：将任意大规模数据处理问题分解为两个阶段——**Map（映射）** 和 **Reduce（归约）**，由框架自动处理分布式调度、容错和网络传输。

与传统单机计算的根本区别：MapReduce 将**计算移到数据侧**（不是把数据传到计算节点），充分利用 HDFS 的数据局部性，最小化网络传输成本。

典型应用：日志分析（词频统计）、倒排索引构建（搜索引擎预处理）、分布式排序、图算法（PageRank 迭代）。

---

## 📐 正式定义与执行流程

### 编程模型

用户只需实现两个函数：

$$\text{Map}: (k_1, v_1) \to \text{list}(k_2, v_2)$$
$$\text{Reduce}: (k_2, \text{list}(v_2)) \to \text{list}(v_3)$$

### 完整执行流程（6阶段）

```
输入分片（Splits）
      │
      ▼
  【Map 阶段】：每个 Mapper 并行处理一个 Split
      │  输出: <key, value> 对，写入本地磁盘（环形缓冲区 100MB）
      ▼
  【Combine 阶段】（可选）：本地预聚合，减少网络传输
      │
      ▼
  【Partition 阶段】：按 hash(key) % numReducers 决定哪个 Reducer 接收
      │
      ▼
  【Shuffle & Sort 阶段】：网络传输 + 按 key 排序（最昂贵的阶段）
      │
      ▼
  【Reduce 阶段】：每个 Reducer 处理一个 key 的所有 values
      │
      ▼
  输出文件（写回 HDFS）
```

### 性能分析

- **Map 阶段**：时间复杂度 $O(n/M)$（$M$ 个 Mapper 并行）
- **Shuffle 阶段**：网络传输量 = $O(n)$，是性能瓶颈
- **Reduce 阶段**：时间复杂度 $O(n \log n / R)$（含排序，$R$ 个 Reducer）

---

## 💻 最小 Python 实现 — 模拟 MapReduce 框架

```python
from collections import defaultdict
from typing import Callable, Iterable

def mapreduce(
    data: list[str],
    mapper: Callable,
    reducer: Callable,
    num_reducers: int = 2
) -> dict:
    """
    简化版 MapReduce 模拟器
    mapper(line) -> list of (key, value)
    reducer(key, values) -> result_value
    """
    # Map 阶段
    map_outputs = []
    for line in data:
        map_outputs.extend(mapper(line))

    # Partition 阶段（按 key 哈希分配给 reducer）
    partitions = defaultdict(list)
    for key, value in map_outputs:
        partition_id = hash(key) % num_reducers
        partitions[partition_id].append((key, value))

    # Shuffle & Sort 阶段（每个分区内按 key 排序）
    reduce_inputs = defaultdict(list)
    for partition in partitions.values():
        for key, value in sorted(partition, key=lambda x: x[0]):
            reduce_inputs[key].append(value)

    # Reduce 阶段
    result = {}
    for key, values in reduce_inputs.items():
        result[key] = reducer(key, values)

    return result

# 经典 WordCount 示例
def wc_mapper(line: str):
    return [(word.lower(), 1) for word in line.split()]

def wc_reducer(key: str, values: list):
    return sum(values)

corpus = [
    "data mining and information retrieval",
    "information retrieval and search engine",
    "data processing with MapReduce",
    "distributed data systems with HDFS"
]
word_counts = mapreduce(corpus, wc_mapper, wc_reducer)
print(dict(sorted(word_counts.items(), key=lambda x: -x[1])[:5]))
# {'data': 3, 'and': 2, 'information': 2, 'retrieval': 2, 'with': 2}
```

---

## ⚠️ 常见误区与避坑指南

1. **数据倾斜（Data Skew）**：若某个 key 对应的数据量极大（如日志中大量 NULL key），会导致一个 Reducer 成为瓶颈。解决方案：**加盐（Salting）**，给热点 key 加随机后缀分散到多个 Reducer，再做二次汇总。

2. **忽略 Combiner 的条件**：Combiner 必须满足**交换律和结合律**（如 sum、max、min），不适用于 mean（均值需要分子和分母分别累加）。

3. **过度追求小文件优化**：HDFS 不擅长处理大量小文件（每个文件占用 NameNode 内存一个 inode），应尽量合并小文件为大 SequenceFile。

4. **Shuffle 阶段不做排序假设**：同一 key 下 values 的顺序**不保证**，Reducer 必须自行处理顺序需求（如时序分析需用二次排序技巧）。

5. **MapReduce 不适合迭代计算**：机器学习中的梯度下降需要多轮迭代，每次迭代读写 HDFS，磁盘 I/O 极其低效。应改用 Spark（基于内存 RDD）。

---

---

## 🔗 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```