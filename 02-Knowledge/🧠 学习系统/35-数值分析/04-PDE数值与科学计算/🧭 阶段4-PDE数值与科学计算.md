---
type: study
topic: "阶段4-PDE数值与科学计算"
course: "数值分析"
created: 2026-08-08
updated: 2026-08-08
status: active
flow: knowledge
kind: moc
tags: [MOC, 阶段MOC, 数值分析, 偏微分方程, 科学计算, 稀疏求解]
---

# 🧭 阶段4：偏微分方程有限差分与科学计算

> “偏微分方程离散化是整个连续计算的最高汇合点。空间连续算子的差分格式将问题转化为超大规模稀疏线性代数系统，结合 Krylov 子空间预条件迭代与制造解法（MMS），形成完整的工业级科学计算闭环。”

---

## 📋 本阶段有序知识卡清单

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/35-数值分析/04-PDE数值与科学计算"
WHERE type = "study" AND !contains(file.name, "🧭")
SORT file.name ASC
```

---

## 🎯 阶段目标与能力构建

1. **多维有限差分离散与边界处理**：掌握二维 Poisson / Laplace 方程的五点差分模板，理解 Dirichlet 齐次边界与 Neumann / Robin 虚拟点（Ghost Point）二阶精度边界处理。
2. **大型稀疏 Krylov 预条件迭代**：掌握共轭梯度法（CG）处理对称正定（SPD）系统的最小化变分原理，掌握 GMRES 与 BiCGSTAB 处理非对称系统的 Arnoldi 正交化，理解 ILU(0) 预条件技术对谱聚集的加速作用。
3. **科学计算收敛性与制造解法 MMS**：掌握 Lax 等价定理（相容性 + 稳定性 $\iff$ 收敛性），熟练运用制造解法（Method of Manufactured Solutions）自动化测量时间与空间双对数网格收敛阶。

---

## 🧮 阶段验收与终极大作业

- [[03-Projects/35-数值分析/课后作业/数值分析-课后作业-08-PDE差分离散与椭圆方程|HW08：PDE差分离散与二维Poisson方程]]
- [[03-Projects/35-数值分析/阶段作业/数值分析-阶段作业-04-二维热传导与Krylov稀疏求解|Stage 4 阶段综合大作业：二维热传导与Krylov稀疏求解]]
- [[03-Projects/35-数值分析/大作业/数值分析-大作业-科学计算PDE求解与稳定性综合审计|Capstone 终极大作业：科学计算PDE求解与稳定性综合审计]]

---

## 🔗 课程大闭环

- 完成本阶段与 Capstone 终极大作业后，全面达成数值分析全部核心目标，并具备进入偏微分方程数值解（FEM / FVM）与高性能科学计算的坚实数学与算法底座。
