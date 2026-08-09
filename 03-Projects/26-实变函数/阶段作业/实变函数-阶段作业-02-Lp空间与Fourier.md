---
type: project
project_type: homework
course: "实变函数"
assignment_id: "实变函数-阶段作业-02"
assignment_level: stage
assignment_format: exam
stage_id: "03"
requires: ["[[实变函数-Lp空间与不等式]]", "[[实变函数-L2空间与完备性]]", "[[实变函数-Fourier级数]]", "[[实变函数-Fourier级数与L2收敛]]"]
source_type: local_integration_task
created: 2026-08-09
status: planned
flow: project
tags: [作业, 实变函数]
---

# 实变函数-阶段作业-02-Lp空间与Fourier

> 作业身份:阶段作业 02 · stage · exam(闭卷,150 分钟)· 阶段3-4 综合验收
> 承接历史 HW01 的 L2 完备性主题(原"阶梯作业"已按 §5.5 清退)。

## 学习目标

闭卷重建 Hölder/Minkowski 与 Riesz-Fischer,完成 Fourier 级数的 L2 收敛论证——函数空间理论的综合检验。

## 试题(共 4 大题)

**1. 不等式链(30 分)**
(a)(15 分)证明 Young 不等式 $ab\le\frac{a^p}{p}+\frac{b^q}{q}$($a,b\ge0$,共轭指数)。
(b)(15 分)由 Young 推出 Hölder 不等式 $\int|fg|\le\lVert f\rVert_p\lVert g\rVert_q$(写明归一化步骤)。

**2. Riesz-Fischer 证明重建(40 分)**
陈述并证明:$L^2[0,1]$ 完备。
- 必须包含四步:Cauchy ⟹ 快速子列($\lVert f_{n_{k+1}}-f_{n_k}\rVert_2<2^{-k}$)⟹ 级数 a.e. 收敛定义 $f$ ⟹ Fatou 提升为范数收敛。
- 标注每步使用的工具(三角不等式、Fatou、范数公理)。

**3. Fourier 级数(15 分)**
(a) 计算方波 $f(x)=\mathrm{sgn}(x)$ 于 $[-\pi,\pi]$ 的 Fourier 系数。
(b) 写出 Parseval 恒等式,并用它计算 $\sum_{n=1}^\infty\frac1{n^2}$(可先用 $f(x)=x$ 或 $x^2$)。

**4. 完备正交系(15 分)**
(a) 陈述 $\{e^{inx}\}_{n\in\mathbb{Z}}$ 是 $L^2[-\pi,\pi]$ 的完备正交系(即 $L^2$ 收敛意义)。
(b) 说明"完备性"与"Parseval 恒等式"的等价关系,并解释为何它保证 $L^2$ 收敛而非逐点收敛。

## 任务边界

- 闭卷:不翻书、不查笔记、不使用工具;允许空白纸演算。
- 第 2 题(Riesz-Fischer)必须写出完整证明,不允许跳步。
- 禁止:使用未在知识卡中证明的对偶结论。

## 提交产物

- 闭卷答卷;第 2 题标注每步使用的工具(三角不等式/Fatou/范数公理)。

## 提交与评分

- 提交:闭卷答卷;第 2 题必须写出完整证明,不允许"显然"。
- Rubric:不等式 30 + Riesz-Fischer 40(跳步扣 5)+ Fourier 30。
- 通过:≥75 且第 2 题 ≥28 分。

## 引导与自检(考前)

- 考前检查:能否默写 Young→Hölder→Minkowski 链条?能否默写 Riesz-Fischer 四步?
- 常见失败:Young 的凸性论证不完整;Riesz-Fischer 的 Fatou 提升那步漏掉;Parseval 归一化常数错误。

## 复盘入口

考后:错题回到 [[实变函数-L2空间与完备性]] / [[实变函数-Lp空间与不等式]] 复习。通过后进入 [[🧭 阶段4-Fourier与应用|阶段4]] 剩余部分并准备大作业。
