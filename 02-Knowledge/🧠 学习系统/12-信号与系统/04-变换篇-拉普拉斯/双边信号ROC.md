---
type: study
topic: "双边信号ROC"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: intermediate
concept: ["双边信号ROC", "双边信号"]
prerequisites: []
related: []
tags: ["学习", "信号与系统"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[🌊 第四阶段：拉普拉斯变换]]"
sources:
  - "Think DSP Ch.10"
  - "Oppenheim §6.1"
  - "MIT 6.003 Lec 15"
kind: concept

upstream:
  - "[[右边信号ROC]]"
  - "[[左边信号ROC]]"
---
# 双边信号ROC

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🌊 第四阶段：拉普拉斯变换]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：ROC 判定
- 这张卡要回答的问题：双边信号的拉普拉斯 ROC 通常是什么形状？
- 阶段目标：掌握双边信号 ROC 为两极点间的带状区域（若存在）。

## 对应教材（真实出处）
- Think DSP Ch.10
- Oppenheim §6.1
- MIT 6.003 Lec 15

## 一句话定义
> 双边信号（左右都有值）的 ROC 是「左极点右侧、右极点左侧」的有限带：σ_min<Re(s)<σ_max，须存在才收敛。

## 从学习内容上要抓什么
- ROC 为竖直条带。
- 要求 σ_min<σ_max（否则无 ROC）。
- 可拆成左右两部分分别变换再并 ROC。

## 核心内容
### 1. 基本定义与直觉
双边信号两边都要压住：左边要求 σ 小，右边要求 σ 大，折中只能取中间一条带。

### 2. 公式 / 机制 / 流程
$$\text{双边: ROC}=\{\sigma_{\min}<\mathrm{Re}(s)<\sigma_{\max}\}$$

### 3. 一个最小例子
x=e^{-a|t|} ⇒ ROC -a<Re(s)<a。

### 4. 常见误区
- 以为双边总存在 ROC（两端增长冲突时不存在）。
- 边界写成 ≥。

## 和其他笔记的关系
- 前置：[[左边信号ROC]]
- 前置：[[右边信号ROC]]
- 相关：[[有限时长ROC]]
- 相关：[[ROC定义]]
- 相关：[[拉氏傅氏关系]]
- 返回阶段索引：[[🌊 第四阶段：拉普拉斯变换]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 说明双边信号 ROC 形状。
- [ ] 为何可能不存在？
- [ ] 举例一个双边 ROC。

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
