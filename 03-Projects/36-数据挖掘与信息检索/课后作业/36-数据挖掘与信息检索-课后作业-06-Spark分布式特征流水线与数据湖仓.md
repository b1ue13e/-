---
type: project
project_type: homework
course: "数据挖掘与信息检索"
assignment_id: "36-HW-06"
assignment_level: lesson
assignment_format: lab
stage_id: "03"
requires: ["[[Spark批处理生态]]", "[[Flink流处理基础]]", "[[数据仓库与湖仓一体]]", "[[分布式特征与样本流水线]]", "[[批流一体架构]]"]
source_type: official_assignment
source_url: "https://spark.apache.org/"
created: 2026-08-07
status: completed
flow: project
tags: [作业, Spark, Flink, 数据湖仓]
---

# 36-数据挖掘与信息检索 - 课后作业 06：Spark 分布式特征流水线、Flink 毫秒流处理与数据湖仓

> **名校开源出处**：[Apache Spark MLlib Pipelines & Flink Event-Time Architecture Guide](https://spark.apache.org/)

---

## 🎯 学习目标

1. 掌握 Apache Spark 分布式特征流水线（Pipeline & Transformer/Estimator）；
2. 理解 Apache Flink 核心架构：**事件时间（Event Time）**、**水位线（Watermark）** 与 **滑动/滚动窗口聚合**；
3. 掌握 **Delta Lake / Iceberg** 湖仓一体核心机制：ACID 事务日志（Transaction Log）、元数据版本回溯（Time Travel）与流批一体 Upsert。

---

## 🔒 任务边界与环境约束

- **技术约束**：纯 Python 模拟 Spark 分布式 RDD / DataFrame 流水线与 Flink 滑动窗口状态机；
- **数据集**：带有事件时间戳的实时点击流与用户画像数据；
- **自动化验收**：必须 100% 通过特征流水线与滑窗聚合单元测试。

---

## 📝 题目详细内容

### 任务 1：PySpark 特征转换流水线设计
构建包含以下阶段的端到端特征预处理 Pipeline：
1. **Tokenizer & StopWordsRemover**：文本切词与停用词过滤；
2. **HashingTF & IDF**：将文本映射至定长特征向量并计算逆文档频率；
3. **VectorAssembler**：将数值特征与文本特征拼接为高维训练样本。

### 任务 2：Flink 事件时间滑窗与延迟容忍机制
实现具有 Watermark 机制的滑动事件时间窗口：
- 设定窗口大小 $W = 60\text{s}$，滑动步长 $S = 10\text{s}$，最大乱序允许时间 $T_{\text{late}} = 5\text{s}$；
- 维护窗口状态，触发并在迟到数据到达侧输出流（Side Output）时完成状态更新。

### 任务 3：湖仓一体 ACID 事务日志与 Upsert 回溯
模拟 Delta Lake 的 Parquet + JSON 事务日志，实现原子写入与版本回溯（Time Travel 查询历史快照）。

---

## 💻 Starter Code 骨架

```python
from typing import List, Dict, Any, Tuple
from collections import defaultdict

class MockStreamingWindow:
    def __init__(self, window_size: int = 60, slide_step: int = 10, max_lateness: int = 5):
        self.w_size = window_size
        self.s_step = slide_step
        self.max_lateness = max_lateness
        self.watermark = 0
        self.windows: Dict[Tuple[int, int], List[Dict[str, Any]]] = defaultdict(list)

    def process_event(self, event_time: int, data: Dict[str, Any]) -> List[Tuple[Tuple[int, int], int]]:
        self.watermark = max(self.watermark, event_time - self.max_lateness)
        first_win_start = (event_time - self.w_size) // self.s_step * self.s_step + self.s_step
        triggered_results = []
        for start in range(max(0, first_win_start), event_time + 1, self.s_step):
            end = start + self.w_size
            if start <= event_time < end:
                self.windows[(start, end)].append(data)
                
        closed_windows = []
        for (start, end), events in list(self.windows.items()):
            if end <= self.watermark:
                triggered_results.append(((start, end), len(events)))
                closed_windows.append((start, end))
        for win in closed_windows:
            del self.windows[win]
            
        return triggered_results
```

---

## 📐 评分标准 (Rubric)

- **[35%] 特征流水线设计**：特征转换与装配器无维度偏差；
- **[35%] Flink 状态与 Watermark**：事件时间推进与乱序数据处理逻辑严谨；
- **[15%] 湖仓 ACID 事务日志**：版本回溯与 Upsert 一致性得到保证；
- **[15%] 单元测试**：100% 通过流批一体测试用例。

---

## 📦 提交产物

1. 源码实现：`hw6_spark_flink_pipeline.py`；
2. 单元测试验证：流批流水线及 Watermark 窗口测试通过。

---

## 💡 引导与自检

- **思考 1**：为什么流处理中 Processing Time 无法替代 Event Time？
- **思考 2**：Delta Lake 如何通过 JSON 增量日志解决 Parquet 不支持单条修改的缺陷？
- **自检**：运行流计算单元测试，观察乱序数据是否触发侧输出。
