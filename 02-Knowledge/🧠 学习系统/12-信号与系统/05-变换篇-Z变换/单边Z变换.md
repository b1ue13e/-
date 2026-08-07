---
type: study
topic: "单边Z变换"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: beginner
concept: ["单边Z变换"]
prerequisites: []
related: []
tags: ["学习", "信号与系统"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[🔢 第五阶段：Z变换]]"
kind: concept
sources:
  - "Oppenheim §10.4：Unilateral Z-Transform"
  - "MIT 6.003 Lec 22：Initial conditions"
upstream:
  - "[[Z变换ROC]]"
  - "[[Z平面]]"
---

# 单边Z变换

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🔢 第五阶段：Z变换]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：Z 变换
- 这张卡要回答的问题：单边 Z 变换与双边有何不同？何时用它？
- 阶段目标：掌握处理含初值/因果系统的单边变换与位移性质。

## 对应教材（真实出处）
- Oppenheim §10.4：Unilateral Z-Transform
- MIT 6.003 Lec 22：Initial conditions

## 一句话定义
> 单边 Z 变换 $X(z)=\sum_{n=0}^{\infty}x[n]z^{-n}$，只对 n≥0 求和；适合因果序列与带初始条件的差分方程。

## 从学习内容上要抓什么
- 默认序列因果（n<0 为 0），便于处理初值。
- 位移性质自动包含初始项，解差分方程方便。
- 双边与单边对因果序列结果相同。

## 核心内容
### 1. 基本定义与直觉
单边 Z 变换像“从 0 时刻才开始看”的 Z 变换，天然适合因果系统和带初值的问题——位移时初值自然进入式子，省去手动补项。

### 2. 公式 / 机制 / 流程
$$X(z)=\sum_{n=0}^{\infty}x[n]z^{-n}$$；位移：$Z\{x[n-1]\}=z^{-1}X(z)+x[-1]$。

### 3. 一个最小例子
例：用单边变换解 $y[n]-ay[n-1]=x[n]$，初值 y[-1] 直接出现在代数方程中。

### 4. 常见误区
- 在含初值的位移性质里漏掉初始项 x[-1]。
- 对非零初值的非因果序列误用单边变换。

## 和其他笔记的关系
- 前置：[[Z变换ROC]]
- 相关：[[离散系统函数]]、[[因果系统]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 说明单边与双边 Z 变换的区别。
- [ ] 写出包含初值的位移性质。
- [ ] 何时优先使用单边 Z 变换？

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

> 以下作业依赖本卡知识点（由作业 `requires` 字段自动派生，可直接点击跳转）：

- [[信号与系统-课后作业-HW06-Z变换与数字滤波器|HW06-Z变换与数字滤波器]]

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
