---
type: index
topic: "第二阶段：Hilbert与基本定理"
created: 2026-08-09
status: active
course: "泛函分析"
flow: knowledge
kind: moc
tags: [阶段MOC, 泛函分析, Hilbert空间, 投影定理, Baire纲定理, 基本定理]
assessment_exempt: true
assessment_exempt_reason: "阶段 MOC，作为阶段内知识卡与作业组织入口"
---

# 🏗️ 第二阶段：Hilbert与基本定理

> “如果说 Banach 空间是带有拓扑度量的向量空间，那么 Hilbert 空间就是把欧氏几何的‘垂直与投影’带入无穷维的完美世界。结合 Baire 纲定理，本阶段将建立泛函分析最强大的分析工具骨架。”

```dataviewjs
const notes = dv.pages('"02-Knowledge/🧠 学习系统/27-泛函分析/02-Hilbert与基本定理"').where(p => p.file.name.startsWith("泛函分析-"));
const completed = notes.where(p => p.status === "completed" || p.status === "active").length;
const total = notes.length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**阶段 2 推进进度: ${progress}%** (${completed}/${total} 核心卡已就绪)`);
```

---

## 🎯 阶段目标与核心问题

1. **内积结构带来了什么欧氏几何魔力？** 平行四边形律、闭凸集正交投影与正交补分解 $H = M \oplus M^\perp$。
2. **为什么 Hilbert 空间的对偶就是它自己？** 理解 Riesz-Fréchet 表示定理及变分法核心工具 Lax-Milgram 引理。
3. **完备度量空间中拓扑“稠密性”的力量**：如何从 Baire 纲定理推导出三大基本定理（一致有界原理、开映射定理、闭图像定理）？

---

## 📚 有序知识卡清单

| 顺序 | 知识卡名称 | 核心内容与定理 | 上游前置 |
| :---: | :--- | :--- | :--- |
| 1 | [[泛函分析-Hilbert空间与正交投影定理]] | 内积公理、Cauchy-Schwarz 不等式、平行四边形恒等式、闭凸集唯一极小范数投影定理、正交分解 $H = M \oplus M^\perp$ | [[泛函分析-赋范空间与Banach空间]] |
| 2 | [[泛函分析-Riesz表示定理与Lax-Milgram引理]] | Riesz-Fréchet 等距共轭线性同构 $H^* \cong H$、连续双线性型矫顽性 (Coercivity) 与 Lax-Milgram 变分存在定理 | [[泛函分析-Hilbert空间与正交投影定理]], [[泛函分析-有界线性算子与算子范数]] |
| 3 | [[泛函分析-Baire纲定理与三大基本定理]] | 第一纲/第二纲集、Baire 纲定理、一致有界原理 (Banach-Steinhaus)、开映射定理、逆算子定理、闭图像定理 | [[泛函分析-赋范空间与Banach空间]], [[泛函分析-有界线性算子与算子范数]] |

---

## 🧰 阶段验收与作业

```dataview
LIST
FROM "03-Projects/27-泛函分析"
WHERE stage_id = "02" OR contains(stage_id, "02")
SORT assignment_level ASC, file.name ASC
```

### 阶段完成标准
- [ ] 掌握正交投影定理中利用平行四边形律构造 Cauchy 极小化序列的技巧。
- [ ] 能够闭卷写出 Riesz 表示定理与 Lax-Milgram 引理的完整证明。
- [ ] 熟练运用开映射定理与闭图像定理解决算子逆的连续性问题。

完成后进入：[[03-算子与谱理论/🧭 阶段3-算子与谱理论|第三阶段：算子与谱理论 ➡️]]
