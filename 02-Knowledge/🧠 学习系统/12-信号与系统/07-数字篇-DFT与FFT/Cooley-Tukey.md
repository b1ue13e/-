---
type: study
topic: "Cooley-Tukey"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: beginner
concept: ["Cooley-Tukey"]
prerequisites: []
related: []
tags: ["学习", "信号与系统"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[💻 第七阶段：DFT与FFT|DFT与FFT]]"
kind: concept
sources:
  - "Think DSP Ch.8：The Cooley-Tukey algorithm"
  - "MIT 6.003 Lec 20：Cooley-Tukey"
  - "Oppenheim §9.3：Cooley-Tukey"
upstream:
  - "[[DFT乘积]]"
  - "[[循环卷积]]"
---

# Cooley-Tukey

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[💻 第七阶段：DFT与FFT|DFT与FFT]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：DFT 与 FFT
- 这张卡要回答的问题：Cooley-Tukey 算法具体怎么做（时域抽取 DIT）？
- 阶段目标：掌握最经典 FFT 算法的步骤与蝶形结构。

## 对应教材（真实出处）
- Think DSP Ch.8：The Cooley-Tukey algorithm
- MIT 6.003 Lec 20：Cooley-Tukey
- Oppenheim §9.3：Cooley-Tukey

## 一句话定义
> Cooley-Tukey（radix-2 DIT）把序列按奇偶拆成两半，分别做 N/2 点 DFT，再用旋转因子合成 N 点结果，递归进行，每层为“蝶形运算”。

## 从学习内容上要抓什么
- DIT：先按 n 奇偶分解；$X[k]=E[k]+W_N^k O[k]$，$X[k+N/2]=E[k]-W_N^k O[k]$。
- 蝶形：一对输入经 ±W 组合输出，是基本计算单元。
- 位反转重排使输入输出按自然序。

## 核心内容
### 1. 基本定义与直觉
Cooley-Tukey 像把一排人按“单双号”分成两队分别点名，再合并——每合并一次省掉一半重复计算。一层层拆下去，就是 FFT 的蝶形流程图。

### 2. 公式 / 机制 / 流程
$$X[k]=E[k]+W_N^k O[k],\quad X[k+N/2]=E[k]-W_N^k O[k],\quad W_N=e^{-j2\pi/N}$$

### 3. 一个最小例子
例：N=8 时先拆为偶/奇各 4 点，再各拆为 2 点，最终用 12 个蝶形拼出全部 X[k]。

### 4. 常见误区
- 奇偶分解后忘记用 W_N^k 旋转因子合成上下半支。
- 忽视位反转导致输出顺序错乱。

## 和其他笔记的关系
- 前置：[[FFT分解]]、[[DFT乘积]]
- 相关：[[循环卷积]]、[[NumPy信号]]
- 推导：[[Cooley-Tukey正确性推导]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 写出 radix-2 DIT 的奇偶分解公式。
- [ ] 说明蝶形运算的输入输出关系。
- [ ] 解释为何需要位反转重排。

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
