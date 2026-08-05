---
title: "perf工具"
type: index
status: completed
flow: knowledge
kind: moc
created: 2026-08-03
tags: [学习, 计算机组成原理, 知识地图]
topic: perf工具
description: 知识地图入口卡，指向完整笔记
---

# perf工具

> 本页为知识地图入口卡：主题完整笔记已建在知识地图上层目录，点击下方链接直达，不在本卡重复建卡。

## 🔗 完整笔记

- [[../perf工具|📄 perf 性能分析工具（完整笔记：PMU 计数器、五子命令、IPC 诊断）]]

## 📌 核心要点速览

- **定位**：Linux 内核官方性能分析框架，通过 PMU 硬件计数器以采样方式（开销 <1%）采集真实硬件指标。
- **核心指标**：$\text{IPC} = \text{instructions} / \text{cycles}$；IPC < 1.0 通常意味着 Cache Miss / 分支预测失败 / 访存延迟瓶颈。
- **五大子命令**：`perf stat`（聚合统计）、`perf record`+`report`（热点采样）、`perf top`（实时）、`perf annotate`（指令级注解）。
- **局限**：虚拟机未透传 PMU 时 cycles/instructions 为 0 或虚假；高频 I/O 场景需配合轮询分析。

## 🔗 相关入口

- [[Roofline模型|Roofline模型]]：用 perf 数据定位是内存受限还是算力受限
- [[../分支预测|分支预测]]：`branch-misses` 事件直指预测器失效
- [[../缓存一致性|缓存一致性]]：`cache-misses` 事件与缓存行无效化开销
- [[../SIMD编程|SIMD编程]]：向量化后的 IPC 与吞吐验证
