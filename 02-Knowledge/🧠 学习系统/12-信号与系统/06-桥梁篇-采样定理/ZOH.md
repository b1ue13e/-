---
type: study
topic: "ZOH"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: advanced
concept: ["ZOH", "实际限制"]
prerequisites: []
related: []
tags: ["学习", "信号与系统"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[🌉 第六阶段：采样定理]]"
sources:
  - "Think DSP Ch.6"
  - "Oppenheim §5.4"
  - "MIT 6.003 Lec 14"
kind: concept

---
# ZOH

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🌉 第六阶段：采样定理]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：重建（实际）
- 这张卡要回答的问题：零阶保持（ZOH）是什么？它如何影响重建？
- 阶段目标：掌握 ZOH=采样间保持上一值（阶梯），等效一个矩形窗 sinc 频响，引入 sinx/x 失真需补偿。

## 对应教材（真实出处）
- Think DSP Ch.6
- Oppenheim §5.4
- MIT 6.003 Lec 14

## 一句话定义
> ZOH 把每个样本保持到下一采样点，输出阶梯波；频响含 sinc 型滚降（sinx/x），高频衰减，实际 DAC 标配，常配补偿滤波器。

## 从学习内容上要抓什么
- ZOH 是最常见物理重建（DAC）。
- 频响 H_ZOH(f)=T·sinc(fT)，有高频衰减。
- 阶梯状，需后续平滑/补偿。

## 核心内容
### 1. 基本定义与直觉
ZOH 像「样本值撑到下一拍才更新」——画出阶梯线，虽不平滑但把点连成了连续信号。

### 2. 公式 / 机制 / 流程
$$H_{\text{ZOH}}(f)=T\,\mathrm{sinc}(fT)\ e^{-j\pi fT}$$

### 3. 一个最小例子
音频 DAC 先 ZOH 再经模拟低通平滑。

### 4. 常见误区
- 以为 ZOH 输出已平滑（其实是阶梯）。
- 忽略 sinc 滚降对高频的压制。

## 和其他笔记的关系
- 前置：[[理想重建]]
- 前置：[[sinc插值]]
- 相关：[[一阶保持]]
- 相关：[[高阶重建]]
- 相关：[[加窗]]
- 返回阶段索引：[[🌉 第六阶段：采样定理]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 说明 ZOH 的工作原理。
- [ ] 它的频响有什么特征？
- [ ] 为何需补偿？

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
