---
type: study
topic: "Z与DTFT关系推导"
created: 2026-08-06
updated: 2026-08-06
status: completed
difficulty: intermediate
concept: ["Z与DTFT关系推导", "DTFT是ZT单位圆"]
prerequisites: ["DTFT定义", "Z变换ROC"]
related: ["Z与DTFT", "DTFT定义", "Z变换ROC"]
tags: ["学习", "信号与系统", "推导"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[🔢 第五阶段：Z变换]]"
kind: derivation
sources:
  - "Oppenheim §10.2：Relation to DTFT (proof)"
  - "Think DSP Ch.10：Z transform"
  - "MIT 6.003 Lec 20"
---

# Z 变换与 DTFT 关系推导

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🔢 第五阶段：Z变换]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]
> 配套概念卡：[[Z与DTFT]]、[[DTFT定义]]、[[Z变换ROC]]

## 学习定位
- 模块：Z 变换与 DTFT 的对应
- 这张卡要回答的问题：为什么「DTFT = ZT 在单位圆 $z=e^{j\Omega}$ 上的取值」，且充要条件是单位圆落在 ROC 内？
- 阶段目标：把 DTFT 严格证为 ZT 在单位圆上的特例，并讲清「单位圆不在 ROC 时 DTFT 不存在」的收敛含义。

## 约定
- Z 变换：$X(z)=\sum_{n=-\infty}^{\infty}x[n]z^{-n}$，ROC 为某圆环 $r_1<|z|<r_2$。
- DTFT：$X(e^{j\Omega})=\sum_{n}x[n]e^{-j\Omega n}$，且 $X(e^{j\Omega})$ 是 $2\pi$ 周期的。

## 推导
把 $z=e^{j\Omega}$（即 $|z|=1$）直接代入 ZT 定义：
$$
X(z)\big|_{z=e^{j\Omega}}
=\sum_{n=-\infty}^{\infty}x[n]\,(e^{j\Omega})^{-n}
=\sum_{n=-\infty}^{\infty}x[n]\,e^{-j\Omega n}
=X(e^{j\Omega})
$$
所以形式上 $\boxed{X(e^{j\Omega})=X(z)\big|_{z=e^{j\Omega}}}$。

**关键在收敛性**：该级数绝对收敛当且仅当
$$\sum_{n}|x[n]\,e^{-j\Omega n}|=\sum_{n}|x[n]|\cdot|e^{-j\Omega n}|=\sum_{n}|x[n]|<\infty$$
而在单位圆 $|z|=1$ 上，$|z^{-n}|=1$，故 ZT 在单位圆收敛 $\iff \sum|x[n]|<\infty$。又 ZT 的 ROC 是圆环 $r_1<|z|<r_2$，单位圆落在其内部等价于
$$r_1<1<r_2$$
于是
$$\boxed{\text{DTFT 存在}\;\iff\;\text{单位圆 }|z|=1\subset\text{ROC}\;\iff\;r_1<1<r_2}\qquad\blacksquare$$

这与连续情形完全类比：ZT 单位圆 $\leftrightarrow$ 拉普拉斯 $j\omega$ 轴（见 [[ROC与稳定性推导]]）。

## 常见误区
- **单位圆不在 ROC 仍硬代 $z=e^{j\Omega}$**：此时级数不（普通）收敛，得到的只是形式上的傅里叶**级数**，可能要按分布/主值理解；定理的「$\iff$」指的是通常意义下的收敛。
- **忽略 $2\pi$ 周期性**：DTFT 是 $2\pi$ 周期的，ZT 本身不周期，二者只在单位圆上重合。
- **右单边不稳定序列无 DTFT**：例如 $x[n]=a^n u[n]$ 且 $|a|>1$，ROC 为 $|z|>|a|>1$，单位圆不在 ROC 内，$\Rightarrow$ DTFT 不存在（普通意义）。
- **把 $r_1<1<r_2$ 记成 $r_1<1$ 即可**：必须同时 $r_2>1$（双边信号两边都可能把单位圆排除）。

## 和其他笔记的关系
- 前置：[[DTFT定义]]、[[Z变换ROC]]
- 配套：[[Z与DTFT]]、[[DTFT周期性]]、[[DTFT存在条件]]
- 连续对偶：[[ROC与稳定性推导]]

## 最小自测
> **检索练习 / 通过标准**：能写出「代入 $z=e^{j\Omega}$」的形式等式，并严格论证其收敛等价于单位圆在 ROC 内（$r_1<1<r_2$）。

- [ ] 写出 $X(e^{j\Omega})=X(z)|_{z=e^{j\Omega}}$ 的代入过程。
- [ ] 说明「单位圆收敛 $\iff \sum|x[n]|<\infty$」这一步。
- [ ] 给出「单位圆不在 ROC」导致 DTFT 不存在的例子。
- [ ] 类比说明它与连续 LT–FT 关系的对应。

*创建于：2026-08-06 · 更新于：2026-08-06*
