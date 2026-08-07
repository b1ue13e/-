---
type: study
topic: "左边信号ROC"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: intermediate
concept: ["左边信号ROC", "左边信号"]
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
---
# 左边信号ROC

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🌊 第四阶段：拉普拉斯变换]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：ROC 判定
- 这张卡要回答的问题：左边信号的拉普拉斯 ROC 是什么形状？
- 阶段目标：掌握左边信号 ROC 为最左极点左侧半平面 Re(s)<σ_min。

## 对应教材（真实出处）
- Think DSP Ch.10
- Oppenheim §6.1
- MIT 6.003 Lec 15

## 一句话定义
> 左边信号（t>t0 为零）的 ROC 是最左边极点左侧：Re(s)<min{Re(极点)}；对应反因果。

## 从学习内容上要抓什么
- 左半平面 ROC。
- 与右边相对称。
- 反因果信号典型。

## 核心内容
### 1. 基本定义与直觉
左边信号往左延伸，要收敛须 σ 足够小把左尾压住——ROC 在最左极点左边。

### 2. 公式 / 机制 / 流程
$$\text{左边信号: ROC}=\{\mathrm{Re}(s)<\sigma_{\min}\}$$

### 3. 一个最小例子
x=-e^{-2t}u(-t) ⇒ ROC Re(s)<-2。

### 4. 常见误区
- 与右边 ROC 写反。
- 忽略反因果含义。

## 和其他笔记的关系
- 前置：[[ROC定义]]
- 前置：[[右边信号ROC]]
- 相关：[[双边信号ROC]]
- 相关：[[有限时长ROC]]
- 相关：[[因果化]]
- 返回阶段索引：[[🌊 第四阶段：拉普拉斯变换]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 说明左边信号 ROC 形状。
- [ ] 对比右边信号。
- [ ] 它对应因果还是反因果？

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

> 暂无直接依赖本卡的知识点作业（可结合「相关」卡或阶段作业做综合训练）。

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
