---
type: study
topic: "Spark批处理生态"
course: "数据挖掘与信息检索"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段3-大数据系统与分析]]"
flow: knowledge
kind: concept
upstream: ["[[MapReduce计算模型]]"]
tags: [学习, 数据挖掘与信息检索]
---
## 💡 直觉与动机

Apache Spark 是对 MapReduce 的革命性改进：**基于内存的分布式计算引擎**。MapReduce 每个 Stage 结束必须将中间结果写回 HDFS（磁盘 I/O 极慢），而 Spark 将数据保留在内存中（RDD），迭代计算速度比 MapReduce 快 **10-100 倍**。

Spark 已成为工业界大数据批处理的事实标准，生态涵盖：批处理（Spark Core）、SQL（Spark SQL）、流处理（Spark Structured Streaming）、机器学习（MLlib）、图计算（GraphX）。

---

## 📐 正式定义与核心概念

### RDD（Resilient Distributed Dataset）

RDD 是 Spark 的核心抽象：**不可变、可分区、可并行操作的数据集**，支持容错（基于血缘图 Lineage 重新计算丢失分区）。

**宽依赖 vs 窄依赖**：

| 类型 | 定义 | 代表操作 | Stage 划分 |
|:---|:---|:---|:---|
| **窄依赖** | 父 RDD 每个分区最多被子 RDD 一个分区使用 | `map`, `filter`, `union` | 同一 Stage |
| **宽依赖** | 父 RDD 分区被子 RDD 多个分区使用（需 Shuffle） | `groupByKey`, `join`, `reduceByKey` | 划分新 Stage |

$$\text{DAG} \xrightarrow{\text{Stage 划分（以宽依赖为界）}} \text{Task 集合} \xrightarrow{\text{调度}} \text{Executor 执行}$$

### Spark SQL & Catalyst 优化器

DataFrame/Dataset API 的查询经过 **Catalyst 优化器** 四阶段处理：

1. **分析（Analysis）**：解析列名、类型
2. **逻辑优化（Logical Optimization）**：谓词下推、列剪裁、常量折叠
3. **物理规划（Physical Planning）**：选择 Sort-Merge Join 或 Broadcast Join
4. **代码生成（Code Generation）**：Tungsten 引擎生成 JVM 字节码

### 宽依赖 Shuffle 触发的代价

Shuffle 需要将数据通过网络重新分区：

$$\text{Shuffle Write} = O(n) \quad \text{Shuffle Read} = O(n)$$

实际中 Shuffle 是 Spark 性能瓶颈的第一来源（磁盘 spill + 网络传输）。

---

## 💻 最小 Python 实现（PySpark API 示例）

```python
# 注：实际运行需要安装 pyspark；此处展示 API 语义
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("WordCount") \
    .master("local[*]") \
    .getOrCreate()

# 读取文本文件
df = spark.read.text("hdfs:///data/corpus/*.txt")

# 词频统计（触发 Shuffle 的 groupBy）
word_counts = (df
    .select(F.explode(F.split(F.col("value"), r"\s+")).alias("word"))
    .filter(F.col("word") != "")
    .groupBy("word")                   # 宽依赖：触发 Shuffle
    .count()
    .orderBy(F.col("count").desc())
)

word_counts.show(10)

# Broadcast Join 优化（小表广播，避免 Shuffle）
small_df = spark.read.csv("stop_words.csv", header=True)
result = df.join(F.broadcast(small_df), "word", "left_anti")

spark.stop()
```

---

## ⚠️ 常见误区与避坑指南

1. **groupByKey 而非 reduceByKey**：`groupByKey` 将所有数据拉到 Reduce 端再聚合，网络传输量 = 全量数据；`reduceByKey` 在 Map 端先做本地预聚合（类似 Combiner），大幅减少 Shuffle 量。**始终优先使用 `reduceByKey`/`aggregateByKey`**。

2. **过度使用 collect()**：`df.collect()` 将全部数据拉回 Driver 内存，TB 级数据直接 OOM。应改用 `take(n)` 或 `show(n)` 预览。

3. **不合理的分区数**：分区数过少 → 并行度低；过多 → 大量 Task 调度开销。经验值：分区数 = 核心数 × 2-4，每个分区 128-256MB 数据。

4. **Shuffle OOM 的排查**：`spark.sql.shuffle.partitions`（默认 200）在数据量大时导致每个分区过大。应根据数据量调整为 `输入数据(GB) × 1000` 分区。

5. **广播变量（Broadcast）滥用**：广播变量适合 < 8-10MB 的小表；大表广播会占用大量 Executor 内存，导致 GC 压力。

---

---

## 🔗 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```