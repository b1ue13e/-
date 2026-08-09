---
type: project
project_type: homework
course: "数据结构与算法"
assignment_id: "数据结构与算法-Stage01-Harness"
assignment_level: stage
assignment_format: lab
stage_id: "01"
requires:
  - "[[数据结构与算法-二分查找与边界处理]]"
  - "[[数据结构与算法-经典排序算法与复杂度分析]]"
  - "[[数据结构与算法-双指针与滑动窗口]]"
  - "[[数据结构与算法-时间与空间复杂度分析]]"
source_type: official_assignment
created: 2026-08-06
updated: 2026-08-07
status: planned
flow: project
tags:
  - 作业
  - 数据结构与算法
  - 阶段作业
source: "UC Berkeley CS61B Lab3"
---

# 数据结构与算法 - 阶段作业 01：基础算法测试 Harness

> **所属课程**：数据结构与算法  
> **所属阶段**：Stage 01 算法入门与基本分析  
> **学术来源**：UC Berkeley CS61B Lab3 改编  

---

## 🎯 学习目标

1. 建立自动化算法测试 Harness，验证排序与二分查找算法的边界正确性。
2. 自动化基准测试 (Benchmarking)，绘制 $\mathcal{O}(n^2)$ 与 $\mathcal{O}(n \log n)$ 算法实际运行时间对比图。

---

## 🚧 任务边界与假设

- **编程语言**：Python 3.10+ / C++17。
- **验证重点**：覆盖空数组、随机序列、完全有序序列及逆序序列。

---

## 📦 提交产物清单

- `test_harness.py`：测试运行器与耗时统计。
