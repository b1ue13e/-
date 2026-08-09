---
type: project
project_type: homework
course: "数据挖掘与信息检索"
assignment_id: "36-HW-03"
assignment_level: lesson
assignment_format: lab
stage_id: "03"
requires: ["[[MapReduce计算模型]]", "[[HDFS与分布式存储]]", "[[大数据系统导论]]", "[[大数据分析与处理]]"]
source_type: official_assignment
source_url: "https://inst.eecs.berkeley.edu/~cs61c/"
created: 2026-08-07
status: completed
flow: project
tags: [作业, 大数据, UC-Berkeley-CS61C]
---

# 36-数据挖掘与信息检索 - 课后作业 03：分布式 MapReduce 归约计算与 HDFS 存储仿真

> **名校开源出处**：[UC Berkeley CS61C: Great Ideas in Computer Architecture - MapReduce Lab](https://inst.eecs.berkeley.edu/~cs61c/)

---

## 🎯 学习目标

1. 深入理解 Google MapReduce / Hadoop 计算架构的核心语义；
2. 实现完整的 **Map $\to$ Combine $\to$ Partition $\to$ Shuffle/Sort $\to$ Reduce** 全链路数据流驱动引擎；
3. 模拟 HDFS 分布式分块存储、NameNode 块元数据映射与机架感知副本容灾。

---

## 🔒 任务边界与环境约束

- **技术约束**：纯 Python 3 实现分布式多线程/协程仿真，严禁使用黑盒 Spark 单机脚本；
- **数据集**：海量分布式网页文本碎片文件；
- **自动化验收**：必须 100% 通过分布式词频与倒排表归约单元测试。

---

## 📝 题目详细内容

### 任务 1：Map 映射与 Combiner 局部聚合
实现自定义 `mapper` 函数，将输入文本流分割为 `(term, 1)` 键值对，并在各分片本地调用 `combiner` 完成局部求和，减少网络 Shuffle 传输开销。

### 任务 2：Partitioner 分区与 Hash Shuffle
根据键的哈希值对中间数据进行分区：
$$\text{PartitionID} = \text{Hash}(key) \pmod R$$
其中 $R$ 为 Reduce 节点总数。将相同分区的键值对聚集并按字典序排序后分发给对应的 Reduce 实例。

### 任务 3：Reducer 全局归约与 HDFS 输出持久化
实现 `reducer` 函数汇总全局词频，并将最终结果按 64KB 分块策略持久化至模拟的 HDFS DataNode 节点上。

---

## 💻 Starter Code 骨架

```python
from typing import List, Tuple, Dict, Callable
from collections import defaultdict
import hashlib

class MapReduceEngine:
    def __init__(self, num_reducers: int = 3):
        self.num_reducers = num_reducers

    def partition(self, key: str) -> int:
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16) % self.num_reducers

    def run_pipeline(
        self,
        docs: List[Tuple[int, str]],
        mapper_fn: Callable[[int, str], List[Tuple[str, int]]],
        reducer_fn: Callable[[str, List[int]], Tuple[str, int]]
    ) -> Dict[str, int]:
        # 1. Map 阶段
        intermediate = []
        for doc_id, text in docs:
            intermediate.extend(mapper_fn(doc_id, text))

        # 2. Shuffle / Partition 阶段
        buckets: Dict[int, Dict[str, List[int]]] = defaultdict(lambda: defaultdict(list))
        for key, val in intermediate:
            part_id = self.partition(key)
            buckets[part_id][key].append(val)

        # 3. Reduce 阶段
        output = {}
        for part_id in range(self.num_reducers):
            for key, val_list in buckets[part_id].items():
                k, v = reducer_fn(key, val_list)
                output[k] = v
        return output
```

---

## 📐 评分标准 (Rubric)

- **[40%] Map-Reduce 计算模型**：Shuffle 排序与分区哈希正确无冲突；
- **[30%] Combiner 局部聚合优化**：有效压减中间传输键值对数量；
- **[30%] HDFS 分布式存储模拟**：元数据块映射与文件读写无损校验。

---

## 📦 提交产物

1. 源码实现：`hw3_mapreduce.py`；
2. 单元测试验证：词频统计与倒排表归约正确。

---

## 💡 引导与自检

- **思考 1**：在 MapReduce 中，Combiner 的执行是否得到绝对保证？为什么 Combiner 的输入输出类型必须与 Reducer 一致？
- **思考 2**：HDFS 为什么采用 3 副本机架感知策略？
- **自检**：运行测试验证多 Reduce 节点分区结果一致性。
