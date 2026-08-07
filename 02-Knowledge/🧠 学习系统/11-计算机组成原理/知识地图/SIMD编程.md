---
title: "SIMD编程"
type: index
status: completed
flow: knowledge
kind: moc
created: 2026-08-03
tags: [学习, 计算机组成原理, 知识地图]
topic: SIMD编程
description: 知识地图入口卡，指向完整笔记
---

# SIMD编程

> 本页为知识地图入口卡：主题完整笔记已建在知识地图上层目录，点击下方链接直达，不在本卡重复建卡。

## 🔗 完整笔记

- [[SIMD编程|📄 SIMD 向量化编程（完整笔记：向量硬件、Intrinsic、对齐要求）]]

## 📌 核心要点速览

- **定义**：单指令多数据（SIMD），一条指令对宽向量寄存器（SSE/AVX2/AVX-512/NEON）中的多组数据同时运算。
- **加速原理**：$T_{\text{SIMD}} = \dfrac{N}{V} \cdot T_{\text{vec}} + T_{\text{tail}}$，理论加速比接近向量宽度 $V$（AVX2 单精度 8 路）。
- **前提**：AVX2 要求 32 字节对齐；未对齐用 `_mm256_loadu_ps` 损失 5%~15%。
- **局限**：循环含大量分支时触发向量掩码遮蔽，部分通道空转；与 SISD/MIMD/SIMT 的适用场景需分清。

## 🔗 相关入口

- [[流水线技术|流水线技术]]：向量指令在流水线中的吞吐与延迟
- [[Amdahl定律]]：向量化只加速可并行部分，受串行比例约束
- [[Roofline模型|Roofline模型]]：判断向量化后是否撞上内存带宽墙
- [[指令集架构|指令集架构]]：向量扩展是 ISA 的一部分（x86 SSE/AVX、ARM NEON）
