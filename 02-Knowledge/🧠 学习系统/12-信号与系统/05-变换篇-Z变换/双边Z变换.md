---
type: study
topic: "双边Z变换"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: intermediate
concept: ["双边Z变换", "Z变换的定义与ROC"]
prerequisites: []
related: ["单边Z变换"]
tags: ["学习", "信号与系统"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[🔢 第五阶段：Z变换]]"
sources:
  - "Think DSP Ch.10-12"
  - "Oppenheim §10.1"
  - "MIT 6.003 Lec 20"
kind: concept

---
# 双边Z变换

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🔢 第五阶段：Z变换]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：Z变换类型
- 这张卡要回答的问题：双边 Z 变换与单边有何区别？
- 阶段目标：掌握双边 ZT 对 n∈(-∞,∞) 求和、ROC 为圆环，单边只 n≥0。

## 对应教材（真实出处）
- Think DSP Ch.10-12
- Oppenheim §10.1
- MIT 6.003 Lec 20

## 一句话定义
> 双边 ZT：X(z)=Σ_{n=-∞}^∞ x[n]z^{-n}，ROC 一般为圆环；单边 ZT 仅 n≥0 求和，常用于因果/初值问题。

## 从学习内容上要抓什么
- 双边覆盖全序列，ROC 可能为空。
- 单边 = 双边对因果序列的特例。
- 初值问题/差分方程多用单边。

## 核心内容
### 1. 基本定义与直觉
双边像看完整历史+未来，单边像只从「开机」后算起；后者更适合实际系统。

### 2. 公式 / 机制 / 流程
$$X(z)=\sum_{n=-\infty}^{\infty}x[n]z^{-n}\ (\text{双边}),\quad \sum_{n=0}^{\infty}(\text{单边})$$

### 3. 一个最小例子
x=a^{|n|} 只有双边 ZT 有 ROC（圆环）；x=a^n u[n] 单边即可。

### 4. 常见误区
- 在含负 n 的信号上用单边而丢信息。
- 忽略双边 ROC 可能为环。

## 和其他笔记的关系
- 前置：[[Z变换ROC]]
- 前置：[[单边Z变换]]
- 相关：[[左边Z变换]]
- 相关：[[离散信号]]
- 相关：[[Z平面]]
- 返回阶段索引：[[🔢 第五阶段：Z变换]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 区分双边与单边 ZT。
- [ ] 双边 ROC 形状？
- [ ] 何时必须用双边？

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
