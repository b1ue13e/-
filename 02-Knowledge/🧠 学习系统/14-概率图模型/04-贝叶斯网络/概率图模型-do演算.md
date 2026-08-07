---
type: study
topic: "do演算"
course: "14-概率图模型"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段4-贝叶斯网络]]"
flow: knowledge
kind: derivation
difficulty: advanced
upstream: ["[[概率图模型-因果推断基础]]", "[[概率图模型-条件独立与d分隔]]"]
concept: ["do演算", "do规则", "干预识别"]
related: ["概率图模型-因果推断基础", "概率图模型-识别性"]
tags: [概率图模型, do演算, 因果推断]
---

# 概率图模型-do演算

> **do-演算（do-calculus）** 是 Pearl 给出的**完整规则系统**：在给定因果图 $G$ 下，判断干预查询 $P(Y \mid do(X))$ 能否仅用观测数据识别，并给出变换步骤。三条规则分别对应"插入/删除观测""干预与观测互换""干预与干预互换"——它把"因果识别"变成形式化推理。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：想从观测数据算 $P(Y\mid do(X))$，但图结构多样，后门准则并不总适用。do-演算提供**三条通用规则**，配合图上的 d-分隔条件，可以机械地尝试把含 $do$ 的表达式化简为纯观测表达式——**可识别性判定**：若化简成功则可识别，否则需要干预数据。

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：do-演算证明"后门/前门/工具变量"都是它的特例；它给出**可识别性的完整刻画**（不满足时任何观测方法都失效）。
- **实际应用场景**：药物效应识别、政策评估、混杂调整的设计。
- **高频考点**：三条规则的适用条件、用 d-分隔验证前提、识别路径的推导。

---

## 3. 学它之前需要哪些前置知识？

1. **[[概率图模型-因果推断基础]]**：do 算子、截断因子化。
2. **[[概率图模型-条件独立与d分隔]]**：d-分隔（判定条件）。
3. **[[概率图模型-图论基础]]**：父/子/祖先、图操作。

---

## 4. 定义与核心公式

### 4.1 记号与图操作

设 $G$ 是因果图。$G_{\overline{X}}$：删除所有指向 $X$ 的边（干预 $X$）；$G_{\underline{X}}$：删除所有从 $X$ 出发的边（"观测 $X$ 但不干预"）；$G_{\overline{X}\underline{Z}}$：同时做两者。

### 4.2 三条 do-演算规则

**规则 1（插入/删除观测）**：若在 $G_{\overline{X}}$ 中 $Y \perp\!\!\!\perp Z \mid (X, W)$，则
$$P(y \mid do(x), z, w) = P(y \mid do(x), w)$$
（$Z$ 在干预 $X$ 后的图中与 $Y$ 条件独立 → 可删去。）

**规则 2（干预与观测互换）**：若在 $G_{\overline{X}\underline{Z}}$ 中 $Y \perp\!\!\!\perp Z \mid (X, W)$，则
$$P(y \mid do(x), do(z), w) = P(y \mid do(x), z, w)$$
（给定 $X, W$ 时 $Z$ 的"干预"与"观测"等价——$Z$ 不是 $Y$ 的原因结构。）

**规则 3（干预与干预互换）**：若在 $G_{\overline{X}\overline{Z(W)}}$ 中 $Y \perp\!\!\!\perp Z \mid (X, W)$（$Z(W)$ 是不含 $Z$ 后代的部分），则
$$P(y \mid do(x), do(z), w) = P(y \mid do(x), w)$$
（$Z$ 对 $Y$ 无因果影响 → 直接删去 $do(z)$。）

> **要点**：每条规则的**前提都是图上的 d-分隔**（在相应修改后的图中验证）；**结论**都是把含 $do$ 的表达式向"更接近观测"的方向简化。

---

## 5. 关键推导

**推导：后门调整是规则 2 的应用**。

目标 $P(y\mid do(x))$。引入混淆 $Z$：$P(y\mid do(x)) = \sum_z P(y\mid do(x), z)P(z\mid do(x))$。规则 2（在 $G_{\overline{X}\underline{Z}}$ 中 $Y\perp Z\mid X$ 时）把 $P(y\mid do(x),z)$ 换为 $P(y\mid x,z)$；规则 3 得 $P(z\mid do(x)) = P(z)$（$X$ 非 $Z$ 祖先）。合起来即后门公式 $\sum_z P(y\mid x,z)P(z)$。∎

**推导：规则 2 的前提直觉**。
$G_{\overline{X}\underline{Z}}$ 中删除指向 $Z$ 的边后，$Z$ 与 $Y$ 仍条件独立——说明 $Z$ 对 $Y$ 的效应完全经由（被 $X,W$ 调整的）观测路径，干预 $Z$ 与观测 $Z$ 无差别。∎

---

## 6. 最小可手算例子

**例（用规则化简）**：图 $X \to Y$，$Z \to Y$，$X$ 与 $Z$ 独立（无混淆）。求 $P(y\mid do(x))$。

- 截断因子化：$P(y\mid do(x)) = P(y\mid x)$（$Z$ 被求和掉且 $Z$ 独立于 $X$）；
- **规则验证**：$P(y\mid do(x)) = \sum_z P(y\mid do(x),z)P(z\mid do(x))$；
  - 规则 2：$G_{\overline{X}\underline{Z}}$ 中 $Y \perp Z \mid X$？图 $X\to Y$、$Z\to Y$，$X\perp Z$——在删 $Z$ 入边后 $Z$ 与 $Y$ 无关（$Y$ 的父只有 $X$），d-分隔成立 → $P(y\mid do(x),z) = P(y\mid do(x))$... 本例 $Z$ 是 $Y$ 的父，需谨慎。简化直觉：$Z\perp X$ 时 $P(y\mid do(x)) = \sum_z P(y\mid x,z)P(z) = P(y\mid x)$（$Z$ 与 $X$ 独立时求和 = 边缘化）。

**例（不可识别）**：图 $X \leftarrow U \to Y$，$X \to Y$（$U$ 隐藏混淆）。$P(y\mid do(x)) = \sum_u P(y\mid x,u)P(u)$——$U$ 未观测无法求和 → **不可识别**（后门条件不满足，规则无法消去 $U$）。

---

## 7. 反例与常见误区

| 误区 | 反例/纠正 |
|:---|:---|
| 三条规则总能化简 | **错**。前提是 d-分隔；不满足时该规则不可用 |
| 可识别性 = 能写出公式 | **不精确**。可识别指"存在仅含观测分布的表达式"；写不出即不可识别 |
| 后门准则是唯一方法 | **错**。前门、工具变量、do-演算都是识别工具 |
| do-演算需要干预数据 | **错**。正是"不用干预数据也能识别"的证明系统 |
| 不可识别 = 无解 | **部分**。不可识别时无法仅靠观测；需干预实验或强假设（单调性等） |

---

## 8. 检索练习（闭卷自检）

### #自测题/基础
1. 写出三条 do-演算规则及其前提。
2. $G_{\overline{X}}$ 与 $G_{\underline{X}}$ 各代表什么图操作？

### #自测题/中等
3. 用后门调整公式推导 $P(y\mid do(x))$（图 $X \leftarrow Z \to Y$，$X \to Y$）。
4. 说明为什么隐藏混淆 $U$（$X\leftarrow U\to Y$）使 $P(y\mid do(x))$ 不可识别。

### #自测题/较难
5. 用 do-演算规则验证：无混淆（$X$ 无父）时 $P(y\mid do(x)) = P(y\mid x)$。

<details>
<summary>答案（先闭卷作答再展开）</summary>

1. 规则 1：$G_{\overline X}$ 中 $Y\perp Z\mid(X,W)$ → 删观测；规则 2：$G_{\overline X\underline Z}$ 中条件独立 → 干预=观测；规则 3：$G_{\overline X\overline{Z(W)}}$ 中条件独立 → 删干预。
2. $G_{\overline X}$ 删指向 $X$ 的边（干预）；$G_{\underline X}$ 删从 $X$ 出发的边（只观测）。
3. $P(y\mid do(x)) = \sum_z P(y\mid x,z)P(z)$。
4. $U$ 未观测且 $X$ 依赖 $U$：后门路径 $X\leftarrow U\to Y$ 无法被观测集阻断（$U$ 不在数据中），截断因子化后 $\sum_u$ 无法计算。
5. $X$ 无父：截断因子化即 $\prod_{V\ne X}P(V\mid Pa(V))$，$P(y\mid do(x)) = P(y\mid x)$（$Y$ 的父含 $X$，且 $P(x)$ 因子被删）。
</details>

---

## 9. 通过标准

- [ ] 能**默写**三条 do-演算规则；
- [ ] 能**独立完成**检索练习 1–5；
- [ ] 能**用规则化简**简单干预查询；
- [ ] 能**判断**给定图下干预的可识别性。

---

## 10. 来源

- Pearl (2009). *Causality* (2nd ed.), Ch. 3.
- Shpitser & Pearl (2008). Complete identification methods for the causal hierarchy. *JMLR*.
- Koller & Friedman (2009). *Probabilistic Graphical Models*, MIT Press. Ch. 21. 访问日期：2026-08-07。

---

## 11. 学完后可以完成

```dataview
LIST
FROM "03-Projects/14-概率图模型"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/14-概率图模型"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

> 直接下游：[[概率图模型-识别性]]（后门/前门/工具变量）、课程 Capstone（因果部分）。
