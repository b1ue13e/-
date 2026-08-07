---
type: study
topic: "切比雪夫II"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: advanced
concept: ["切比雪夫II", "常用设计方法"]
prerequisites: []
related: []
tags: ["学习", "信号与系统"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[🚀 第八阶段：工程实现]]"
sources:
  - "Think DSP Ch.11"
  - "Oppenheim §7.3：Chebyshev"
  - "scipy.signal.cheby2"
kind: concept

upstream:
  - "[[切比雪夫I]]"
  - "[[巴特沃斯]]"
---
# 切比雪夫II

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🚀 第八阶段：工程实现]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：数字滤波器设计
- 这张卡要回答的问题：切比雪夫 II 型（逆切比雪夫）滤波器特点？
- 阶段目标：掌握 CII：阻带等波纹、通带单调，适合「阻带要严格」的场景，与 CI 通带等波纹相对。

## 对应教材（真实出处）
- Think DSP Ch.11
- Oppenheim §7.3：Chebyshev
- scipy.signal.cheby2

## 一句话定义
> 切比雪夫 II 型：阻带等波纹（统一衰减）、通带单调平滑；零点在单位圆上提供锐阻带；与 I 型（通带波纹）互补，适合对阻带要求严苛的应用。

## 从学习内容上要抓什么
- 阻带等波纹 ⇒ 阻带衰减均匀可控。
- 通带更平（无波纹）。
- 阶数比同指标 I 型略高。

## 核心内容
### 1. 基本定义与直觉
CII 像「阻带装了均匀锯齿的闸门」：该挡的频率一律压得一样低，而通带保持平滑好通过。

### 2. 公式 / 机制 / 流程
$$H(s)=\frac{1}{\sqrt{1+\frac{1}{\varepsilon^2 T_n^2(\Omega_s/\Omega)}}},\quad \text{阻带等波纹}$$

### 3. 一个最小例子
用 signal.cheby2(4,40,0.2) 设计阻带 40dB 衰减。

### 4. 常见误区
- 把 CII 与 CI 的波纹位置搞反。
- 忽略阻带零点在单位圆上（相位影响）。

## 和其他笔记的关系
- 前置：[[巴特沃斯]]
- 前置：[[双线性变换]]
- 相关：[[切比雪夫I]]
- 相关：[[椭圆滤波器]]
- 相关：[[SciPy信号]]
- 返回阶段索引：[[🚀 第八阶段：工程实现]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 切比雪夫 II 型特点？
- [ ] 与 I 型区别？
- [ ] 何时选它？

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
