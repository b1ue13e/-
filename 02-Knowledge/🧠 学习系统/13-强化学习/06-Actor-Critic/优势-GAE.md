---
type: study
topic: "优势-GAE"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["优势-GAE", "GAE 广义优势估计"]
upstream: ["[[优势-n步]]", "[[优势-TD]]"]
tags: [学习, 强化学习]
---

# 优势-GAE

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
n-step 优势固定窗；GAE 用指数加权组合多步优势，在偏差/方差上更平滑可控。

## 正式定义 / 公式
GAE(λ) = (1−λ) Σ_{n=1}^∞ λ^{n-1} A_t^{(n)}
等价递推：δ_t = r_{t+1}+γV(s_{t+1})−V(s_t)，A_t^{GAE} = δ_t + γλ A_{t+1}^{GAE}
λ→0 近似 TD（低方差/高偏），λ→1 近似 MC（低偏/高方差）。

## 最小手算例子
γ=0.99,λ=0.95：从末步往前递推，每步把折扣优势与下步 GAE 混合，得平滑优势。

## 对比与常见错误
- 与 n-step：GAE 是无限 n-step 的 λ 加权，无需选固定 n。
- 常见错误：以为 GAE 无偏——它仍依赖 V_φ，且 λ<1 时偏。

## 闭卷自测
1. 写出 GAE 递推式。
2. λ 如何权衡偏差与方差？
## 学完后可以完成

```dataview
TABLE assignment_level, source_type FROM "03-Projects"
WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
```
