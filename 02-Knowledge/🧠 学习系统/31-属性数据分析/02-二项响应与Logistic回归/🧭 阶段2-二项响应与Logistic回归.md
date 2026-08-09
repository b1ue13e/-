---
type: index
course: "属性数据分析"
topic: "阶段2-二项响应与Logistic回归"
flow: knowledge
kind: moc
status: completed
stage_id: "02"
created: 2026-08-09
tags: [MOC, 阶段MOC, 属性数据分析, Logistic回归]
---

# 🧭 阶段2：二项响应与Logistic回归

> "Logistic 回归是现代分类预测与风险建模的黄金标准。它完美融合了 Logit 变换的有界概率映射、几率比的乘性解释以及迭代加权最小二乘（IRLS）的高效计算。"

---

## 📌 阶段定位与学习目标

本阶段深入二分类广义线性模型的核心理论与工业诊断。学完本阶段后，你应当能够：
1. 掌握 Logit 模型形式、Sigmoid 逆映射及连续/分类协变量的对数比值（Log-odds）与优势比（OR）解释。
2. 熟练推导对数似然函数、Score 向量与 Fisher 信息矩阵，掌握 Newton-Raphson / IRLS 参数更新算法。
3. 掌握模型偏差（Deviance）与似然比嵌套模型检验，深入理解 Hosmer-Lemeshow 拟合优度检验。
4. 识别完全分离（Complete Separation）与准完全分离现象，掌握 Firth 惩罚似然估计解决方案。

---

## 🧩 知识卡清单与学习顺序

```dataview
TABLE topic AS "主题", kind AS "类型", difficulty AS "难度"
FROM "02-Knowledge/🧠 学习系统/31-属性数据分析/02-二项响应与Logistic回归"
WHERE type = "study"
SORT file.name ASC
```

### 推荐学习顺序：
1. [[属性数据分析-二项Logistic回归模型与参数解释]] —— 模型形式与系数在几率比上的科学解释。
2. [[属性数据分析-Logistic模型参数估计与Fisher得分算法]] —— 深入似然数学与 IRLS 迭代求解算法底层。
3. [[属性数据分析-Logistic模型拟合优度与完全分离诊断]] —— 模型诊断、残差分析与分离极端情况处理。

---

## 🎯 阶段验收与作业

本阶段对应课后作业 HW02：
- [[属性数据分析-课后作业-02-二项Logistic回归与比值比置信区间]] —— 针对真实临床二分类数据集进行完整 Logistic 拟合、系数检验、OR 置信区间计算与模型评估。

```dataview
LIST
FROM "03-Projects/31-属性数据分析"
WHERE stage_id = "02"
SORT assignment_level ASC, file.name ASC
```

---

## 🔗 阶段导航

- ⬅️ 上一阶段：[[01-列联表与关联推断/🧭 阶段1-列联表与关联推断|进入阶段1：列联表与关联推断]]
- 🧭 课程总览：[[🗺️ 属性数据分析学习路径]]
- ➡️ 下一阶段：[[03-计数数据与对数线性模型/🧭 阶段3-计数数据与对数线性模型|进入阶段3：计数数据与对数线性模型]]
