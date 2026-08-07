---
type: study
topic: "s=jw"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: intermediate
concept: ["s=jw", "特殊关系"]
prerequisites: []
related: []
tags: ["学习", "信号与系统"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[🌊 第四阶段：拉普拉斯变换]]"
sources:
  - "Think DSP Ch.10-11"
  - "Oppenheim §6.3：Relation to FT"
  - "MIT 6.003 Lec 15"
kind: concept

upstream:
  - "[[s域含义]]"
  - "[[拉氏傅氏关系]]"
---
# s=jw

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🌊 第四阶段：拉普拉斯变换]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：拉氏-傅氏联系
- 这张卡要回答的问题：拉普拉斯在 s=jω 时与傅里叶变换有何关系？
- 阶段目标：掌握「沿 jω 轴取值」：若 jω 轴在 ROC 内，LT 在该轴等于 FT。

## 对应教材（真实出处）
- Think DSP Ch.10-11
- Oppenheim §6.3：Relation to FT
- MIT 6.003 Lec 15

## 一句话定义
> 当 jω 轴 ⊂ ROC 时，X(jω)=X(s)|_{s=jω}：傅里叶变换就是拉普拉斯沿虚轴的那一刀。

## 从学习内容上要抓什么
- FT 是 LT 在虚轴上的特例。
- 若 jω 轴不在 ROC（如不稳定），FT 不存在但 LT 仍有。
- 这是「LT 推广 FT」的精确表述。

## 核心内容
### 1. 基本定义与直觉
s 平面像一块布，FT 只是沿中间竖线（虚轴）裁下的那一条；裁得到（ROC 包含）就有 FT。

### 2. 公式 / 机制 / 流程
$$X(j\omega)=X(s)\big|_{s=j\omega}\quad(\text{若 }j\omega\in\text{ROC})$$

### 3. 一个最小例子
稳定因果系统 jω 轴在 ROC 内 ⇒ H(jω) 即频率响应。

### 4. 常见误区
- 在 jω 轴不在 ROC 时仍令 s=jω（得无意义结果）。
- 以为 LT 总包含 FT。

## 推导/证明
**目标**：证明「当 jω 轴 ⊂ ROC 时，$X(j\omega)=X(s)|_{s=j\omega}$」。

由 LT 定义，直接令 $s=j\omega$（即 $\sigma=0$）：
$$X(s)\Big|_{s=j\omega}=\int_{-\infty}^{\infty}x(t)e^{-j\omega t}dt$$
这正是傅里叶变换 $X_{\mathrm{FT}}(\omega)$——**前提**是该积分收敛，而这等价于 $s=j\omega$ 落在 ROC 内。

反例（jω 轴不在 ROC）：单位阶跃 $u(t)$ 的 LT 为 $1/s$，ROC 为 $\mathrm{Re}(s)>0$，jω 轴恰在边界、不在 ROC ⇒ $u(t)$ 的 FT 不存在于普通函数意义（需引入 $\pi\delta(\omega)+1/(j\omega)$ 广义函数）。说明 LT 不总包含 FT。

**最小手算**：$x(t)=e^{-t}u(t)$，LT $=1/(s+1)$，ROC $\mathrm{Re}(s)>-1$ 含 jω 轴。令 $s=j\omega$ 得 $X(j\omega)=1/(j\omega+1)$，与直接算 FT 一致。

## 和其他笔记的关系
- 前置：[[拉氏傅氏关系]]
- 前置：[[s域含义]]
- 相关：[[物理意义]]
- 相关：[[系统函数]]
- 相关：[[系统函数]]
- 返回阶段索引：[[🌊 第四阶段：拉普拉斯变换]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 说明 s=jω 与 FT 的关系。
- [ ] 何时 LT 不能退化为 FT？
- [ ] 为何说 FT 是 LT 的特例？

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

> 暂无直接依赖本卡的知识点作业（可结合「相关」卡或阶段作业做综合训练）。

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
