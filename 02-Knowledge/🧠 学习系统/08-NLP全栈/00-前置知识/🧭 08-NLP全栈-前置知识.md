---
type: study
topic: "08-NLP全栈-前置知识导学"
course: "08-NLP全栈"
created: 2026-08-06
status: active
flow: knowledge
kind: moc
tags: [学习, NLP, 前置知识, MOC]
sources: ['Jurafsky, D., & Martin, J. H. (2024). Speech and Language Processing (3rd ed. draft).']
assessment_exempt: true
assessment_exempt_reason: 阶段 MOC 导航与学习目标总览页
---

# 🧭 08-NLP全栈 - 阶段 0：前置知识导学

> ⏱ **预计完成耗时**：2 小时  
> 🎯 **阶段目标**：掌握进入 NLP 学习所需的数学（线性代数、张量运算、信息论）与 PyTorch 编程底座。

---

## 🧭 为什么现在学 & 学习顺序

本阶段为 NLP 课程的入场券。全栈 NLP 的公式推导（如 Softmax 交叉熵、Attention 点积、RoPE 旋转）与 PyTorch 代码实现依赖张量形状变换和自动求导机制。
按以下顺序学习前置知识：
1. [[08-NLP全栈-前置-线性代数与张量运算|线性代数与张量运算]]：掌握矩阵乘法与 PyTorch 张量 `view`/`permute`
2. [[08-NLP全栈-前置-概率论与信息论基础|概率论与信息论基础]]：掌握条件概率、熵、$KL$ 散度与交叉熵
3. [[08-NLP全栈-前置-PyTorch与NLP编程基础|PyTorch与NLP编程基础]]：掌握 Dataset/DataLoader 与 GPU 训练 Loop

---

## 📚 本阶段有序知识卡清单

- 1️⃣ [[08-NLP全栈-前置-线性代数与张量运算]]
- 2️⃣ [[08-NLP全栈-前置-概率论与信息论基础]]
- 3️⃣ [[08-NLP全栈-前置-PyTorch与NLP编程基础]]

---

## 🧪 阶段验收与作业

学完本阶段后，你应能自检：
- [ ] 能用 Python/PyTorch 手写 3D 张量的 Batch 矩阵乘法 (`torch.bmm`)。
- [ ] 能写出交叉熵 Loss $H(p, q) = -\sum p(x) \log q(x)$ 的展开公式。

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/08-NLP全栈/00-前置知识"
WHERE type = "study" AND file.name != this.file.name
SORT file.name ASC
```

---

## 🔗 阶段导航

| ⬅️ 上一阶段 | 📋 课程主路径 | 下一阶段 ➡️ |
|:---:|:---:|:---:|
| 课程起点 | [[02-Knowledge/🧠 学习系统/08-NLP全栈/🗺️ 08-NLP全栈学习路径\|08-NLP全栈学习路径]] | [[01-基础准备/🧭 阶段1-基础准备\|阶段 1：基础准备]] |
