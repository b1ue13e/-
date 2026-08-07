---
type: study
topic: "sinc插值"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: advanced
concept: ["sinc插值", "信号重建"]
prerequisites: ["截止频率"]
related: ["一阶保持"]
tags: ["学习", "信号与系统"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[🌉 第六阶段：采样定理]]"
kind: concept
sources:
  - "Think DSP Ch.6"
  - "Oppenheim §5.4"
  - "MIT 6.003 Lec 14"
upstream:
  - "[[理想重建]]"
  - "[[矩形变换]]"
---

# sinc插值

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🌉 第六阶段：采样定理]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：重建
- 这张卡要回答的问题：sinc 插值在重建中扮演什么角色？
- 阶段目标：掌握 sinc 是理想低通的冲激响应，是「无混叠精确重建」的数学内核。

## 对应教材（真实出处）
- Think DSP Ch.6
- Oppenheim §5.4
- MIT 6.003 Lec 14

## 一句话定义
> sinc((t-nT)/T) 是理想重建低通的冲激响应；样本值加权求和这些 sinc 即得原信号——每个样本负责「填满」自己的奈奎斯特区间。

## 从学习内容上要抓什么
- sinc 在样本点 nT 处为 1、其余整数样本点为 0（正交）。
- 无限长、非因果，实际用截断/窗近似。
- 零点在其它样本点 ⇒ 不互相干扰。

## 核心内容
### 1. 基本定义与直觉
sinc 像一把只在自己格点「顶到 1」、别处穿过 0 的梳子，多把错位梳子相加正好拼出原曲线。

### 2. 公式 / 机制 / 流程
$$h_r(t)=\mathrm{sinc}(t/T),\quad x(t)=\sum_n x[n]\,h_r(t-nT)$$

### 3. 一个最小例子
两样本间用 sinc 平滑过渡，而非直线连接。

### 4. 常见误区
- 误以为 sinc 可实现（无限长）。
- 忽略需截断引入的误差。

## 推导/证明
**目标**：说明 $h_r(t)=\mathrm{sinc}(t/T)$ 是理想重建低通的冲激响应，并验证样本点正交性。

理想重建低通的频率响应为
$$H_r(\omega)=\begin{cases}T,& |\omega|<\omega_s/2=\pi/T\\ 0,& \text{其它}\end{cases}\quad (\omega_s=2\pi/T)$$
其冲激响应即逆傅里叶变换（归一化 sinc）：
$$h_r(t)=\frac{1}{2\pi}\int_{-\pi/T}^{\pi/T}T\,e^{j\omega t}d\omega=T\cdot\frac{\sin(\pi t/T)}{\pi t/T}=\mathrm{sinc}(t/T)$$

重建信号 $x_r(t)=(x_s*h_r)(t)=\sum_n x(nT)\,h_r(t-nT)$。**正交性**：当 $t=mT$ 时
$$h_r(mT-nT)=\mathrm{sinc}(m-n)=\begin{cases}1,& m=n\\ 0,& m\neq n\end{cases}$$
故 $x_r(mT)=x(mT)$，且各样本项只在自己格点为 1、其余样本点穿过 0，互不干扰 ⇒ 无限长 sinc 求和精确恢复原信号。

**最小手算**：仅两个样本 $x[0]=3,x[1]=5$，在 $t=0$ 处 $x_r(0)=3\cdot\mathrm{sinc}(0)+5\cdot\mathrm{sinc}(-1)=3\cdot1+5\cdot0=3$；在 $t=T$ 处 $=3\cdot0+5\cdot1=5$，精确还原样本值（实际重建需无限项，此处验证正交抽样性质）。

## 和其他笔记的关系
- 前置：[[理想重建]]
- 前置：[[矩形变换]]
- 相关：[[ZOH]]
- 相关：[[加窗]]
- 相关：[[频谱泄漏原因]]
- 返回阶段索引：[[🌉 第六阶段：采样定理]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 说明 sinc 插值的原理。
- [ ] 为何在各样本点正交？
- [ ] 实际为何要截断？

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
