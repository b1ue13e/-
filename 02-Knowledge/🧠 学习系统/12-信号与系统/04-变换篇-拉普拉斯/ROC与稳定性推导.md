---
type: study
topic: "ROC与稳定性推导"
created: 2026-08-06
updated: 2026-08-06
status: completed
difficulty: intermediate
concept: ["ROC与稳定性推导", "ROC稳定性关系证明"]
prerequisites: ["ROC定义", "极点", "稳定系统"]
related: ["ROC定义", "极点", "稳定系统", "稳定性判断", "Z与DTFT"]
tags: ["学习", "信号与系统", "推导"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[🌊 第四阶段：拉普拉斯变换]]"
kind: derivation
sources:
  - "Oppenheim §9.2 / §6.3：ROC and stability"
  - "郑君里《信号与系统》下册 §7.4"
upstream:
  - "[[ROC定义]]"
  - "[[极点]]"
  - "[[稳定系统]]"
---

# ROC 与稳定性关系推导

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🌊 第四阶段：拉普拉斯变换]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]
> 配套概念卡：[[ROC定义]]、[[极点]]、[[稳定系统]]

## 学习定位
- 模块：拉普拉斯 / Z 变换的 ROC 性质
- 这张卡要回答的问题：为什么「系统 BIBO 稳定 $\iff$ ROC 包含 $j\omega$ 轴（连续）/ 单位圆（离散）」？
- 阶段目标：把「稳定性」与「傅里叶变换存在性」用 ROC 统一起来，并推出因果稳定 $\Rightarrow$ 极点全在左半平面。

## 约定与定义
- 双边拉普拉斯：$X(s)=\int_{-\infty}^{\infty}x(t)e^{-st}dt,\;s=\sigma+j\omega$。其 ROC 是使积分绝对收敛的竖条 $\sigma_L<\mathrm{Re}(s)<\sigma_R$。
- BIBO 稳定：$\int_{-\infty}^{\infty}|h(t)|dt<\infty$（连续）；$\sum_n|h[n]|<\infty$（离散）。

## 推导（连续时间）
BIBO 稳定要求 $\int|h(t)|dt<\infty$。而
$$H(j\omega)=\int_{-\infty}^{\infty}h(t)e^{-j\omega t}dt$$
该积分**绝对收敛**的充要条件是
$$\int_{-\infty}^{\infty}|h(t)e^{-j\omega t}|dt=\int_{-\infty}^{\infty}|h(t)|dt<\infty$$
即 $H(j\omega)$（傅里叶变换）存在 $\iff h$ 绝对可积 $\iff$ 可以取 $\mathrm{Re}(s)=0$ 使拉普拉斯积分收敛。

拉普拉斯 ROC 是竖条 $\sigma_L<\mathrm{Re}(s)<\sigma_R$。「能在 $\mathrm{Re}(s)=0$ 处收敛」等价于 $0\in(\sigma_L,\sigma_R)$，即
$$\boxed{\text{BIBO 稳定}\;\iff\;j\omega\text{ 轴}\subset\text{ROC}}$$
对**因果**系统 $h(t)=0\;(t<0)$，ROC 为 $\mathrm{Re}(s)>\sigma_{\max}$（最右极点的实部）。包含 $j\omega$ 轴要求 $\sigma_{\max}<0$，即**全部极点在左半平面（LHP）**。$\blacksquare$

离散时间完全类比：ZT 的 ROC 是圆环 $r_1<|z|<r_2$；BIBO 稳定 $\iff$ 单位圆 $|z|=1\subset$ ROC $\iff r_1<1<r_2$。因果稳定 $\Rightarrow$ 极点全在单位圆内（见 [[Z与DTFT]]）。

## 常见误区
- **「触及」不等于「包含」**：$j\omega$ 轴必须在 ROC **内部**（开集），仅边界经过点不算稳定（例如 $h(t)=e^{0\cdot t}u(t)$ 的 ROC 是 $\mathrm{Re}(s)>0$，不含 $j\omega$ 轴，不稳定）。
- **把信号稳定与系统稳定混为一谈**：结论对两者形式相同（都看傅里叶变换是否绝对收敛），但系统稳定特指冲激响应 $h$。
- **离散情形忘换「单位圆」**：连续看 $j\omega$ 轴，离散看单位圆，二者是 ZT 与 LT 的对应关系（[[Z与DTFT]]）。
- **因果稳定 $\Rightarrow$ 极点全在 LHP，但反过来不成立**：极点全在 LHP 只保证存在某个包含 $j\omega$ 轴的 ROC；若系统非因果（左边信号），即使极点全在 LHP 也可能不稳定——要看 ROC 而非只看极点位置。

## 和其他笔记的关系
- 前置：[[ROC定义]]、[[极点]]、[[稳定系统]]
- 配套：[[稳定性判断]]、[[右边信号ROC]]、[[双边信号ROC]]
- 离散对偶：[[Z与DTFT]]、[[Z变换ROC]]

## 最小自测
> **检索练习 / 通过标准**：能说明「稳定性 = FT 绝对收敛 = $j\omega$ 轴在 ROC 内」，并推出因果稳定的极点条件。

- [ ] 写出连续与离散两种「稳定 $\iff$ ROC 含某条线/圆」的命题。
- [ ] 推导因果稳定 $\Rightarrow$ 极点全在左半平面（连续）/单位圆内（离散）。
- [ ] 举一个「极点全在 LHP 但不稳定」的例子并说明原因（提示：ROC 不取包含 $j\omega$ 轴的那一侧）。

*创建于：2026-08-06 · 更新于：2026-08-06*

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
