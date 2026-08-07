---
type: study
topic: "Z与DTFT"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: intermediate
concept: ["Z与DTFT", "与Z关系"]
prerequisites: []
related: []
tags: ["学习", "信号与系统"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[🔢 第五阶段：Z变换]]"
sources:
  - "Think DSP Ch.10-12"
  - "Oppenheim §10.2：Relation to DTFT"
  - "MIT 6.003 Lec 20"
kind: concept

upstream:
  - "[[DTFT定义]]"
  - "[[Z变换ROC]]"
  - "[[Z平面]]"
---
# Z与DTFT

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🔢 第五阶段：Z变换]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：z 与 DTFT
- 这张卡要回答的问题：Z 变换与 DTFT 如何对应？
- 阶段目标：掌握「沿单位圆取值」：DTFT = ZT 在 |z|=1 上，当且仅当单位圆在 ROC 内。

## 对应教材（真实出处）
- Think DSP Ch.10-12
- Oppenheim §10.2：Relation to DTFT
- MIT 6.003 Lec 20

## 一句话定义
> 当单位圆 |z|=1 ⊂ ROC 时，DTFT = X(z)|_{z=e^{jΩ}}；DTFT 即 ZT 在单位圆上的那圈。

## 从学习内容上要抓什么
- DTFT 是 ZT 在单位圆上的特例。
- 单位圆不在 ROC（如不稳定）则 DTFT 不存在。
- 与连续 LT-FT 关系完全类比。

## 核心内容
### 1. 基本定义与直觉
z 平面像圆盘，DTFT 只是沿圆周裁下的频谱环；裁得到（ROC 含圆）就有。

### 2. 公式 / 机制 / 流程
$$X(e^{j\Omega})=X(z)\big|_{z=e^{j\Omega}}\quad(|z|=1\in\text{ROC})$$

### 3. 一个最小例子
稳定数字滤波器单位圆在 ROC 内 ⇒ 频率响应 H(e^{jΩ})。

### 4. 常见误区
- 单位圆不在 ROC 时仍取 z=e^{jΩ}。
- 忽略与连续 LT-FT 的类比。

## 和其他笔记的关系
- 前置：[[DTFT定义]]
- 前置：[[Z平面]]
- 相关：[[单位圆上]]
- 相关：[[离散系统函数]]
- 相关：[[Z变换ROC]]
- 推导：[[Z与DTFT关系推导]]
- 返回阶段索引：[[🔢 第五阶段：Z变换]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 说明 ZT 与 DTFT 的关系。
- [ ] 何时 DTFT 不存在？
- [ ] 与 LT-FT 类比？

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
