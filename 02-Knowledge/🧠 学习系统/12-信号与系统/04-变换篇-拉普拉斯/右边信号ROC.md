---
type: study
topic: "右边信号ROC"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: intermediate
concept: ["右边信号ROC", "右边信号"]
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
  - "[[ROC定义]]"
  - "[[因果系统]]"
---
# 右边信号ROC

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🌊 第四阶段：拉普拉斯变换]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：ROC 判定
- 这张卡要回答的问题：右边信号的拉普拉斯 ROC 是什么形状？
- 阶段目标：掌握右边（因果）信号 ROC 为最右极点右侧的半平面 Re(s)>σ_max。

## 对应教材（真实出处）
- Think DSP Ch.10
- Oppenheim §6.1
- MIT 6.003 Lec 15

## 一句话定义
> 右边信号（t<t0 为零）的 ROC 是最右边极点右侧：Re(s)>max{Re(极点)}；若因果则含 ∞。

## 从学习内容上要抓什么
- 右半平面 ROC。
- 与「因果」对应（无左半平面尾巴）。
- 极点实部最大者决定边界。

## 核心内容
### 1. 基本定义与直觉
右边信号从某时刻往右走，要收敛必须选足够大的 σ 把尾压住——所以 ROC 在最右极点右边。

### 2. 公式 / 机制 / 流程
$$\text{右边信号: ROC}=\{\mathrm{Re}(s)>\sigma_{\max}\}$$

### 3. 一个最小例子
x=e^{-2t}u(t) ⇒ ROC Re(s)>-2。

### 4. 常见误区
- 把右边 ROC 写成左半平面（那是左边的）。
- 忽略「严格大于」边界。

## 和其他笔记的关系
- 前置：[[ROC定义]]
- 前置：[[存在条件]]
- 相关：[[左边信号ROC]]
- 相关：[[双边信号ROC]]
- 相关：[[因果系统]]
- 返回阶段索引：[[🌊 第四阶段：拉普拉斯变换]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 说明右边信号 ROC 形状。
- [ ] 为何是右半平面？
- [ ] 因果信号 ROC 含 ∞ 吗？

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

> 暂无直接依赖本卡的知识点作业（可结合「相关」卡或阶段作业做综合训练）。

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
