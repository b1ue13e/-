---
type: study
topic: 迹-行列式平面(Trace-Det)判别法
created: 2026-08-06
status: completed
difficulty: intermediate
concept:
- 迹(Trace)
- 行列式(Det)
prerequisites:
- 常微分方程-二维线性系统平衡点分类
related:
- '[[常微分方程-非线性系统的局部线性化（雅可比矩阵）]]'
tags:
- 学习
- 数学
- 常微分方程
- 计算
course: 常微分方程
flow: knowledge
kind: concept
assessment_exempt: false
stage_moc: '[[🧭 阶段3-多维线性系统与矩阵指数]]'
upstream:
  - '[[常微分方程-二维线性系统平衡点分类]]'
---



# 迹-行列式平面(Trace-Det)判别法

---

## 1. 这个知识点解决什么问题？

上节课我们通过求特征值完成了奇点分类。但是每次都要解一元二次方程 $\lambda^2 - \tau\lambda + \Delta = 0$ 算出具体的特征值，非常麻烦。
有没有一种方法，看一眼矩阵的迹（Trace，记为 $\tau$）和行列式（Det，记为 $\Delta$），就能**直接秒杀**平衡点的类型？
这就是大名鼎鼎的 $\tau-\Delta$ 判别法（源自 MIT 18.03SC）。

## 2. 判别准则表

特征方程为 $\lambda^2 - \tau\lambda + \Delta = 0$。
判别式为 $D = \tau^2 - 4\Delta$。它决定了根是实数（抛物线以外）还是复数（抛物线以内）。

| 判别条件 | 奇点类型 | 几何直觉 |
| :--- | :--- | :--- |
| **$\Delta < 0$** | **鞍点** | 行列式小于0说明特征值异号，直接秒杀鞍点，与 $\tau$ 无关！ |
| $\Delta > 0, D > 0, \tau > 0$ | 不稳定结点 | $\Delta>0$ 且抛物线外，全是实根；$\tau>0$ 总发散。 |
| $\Delta > 0, D > 0, \tau < 0$ | 稳定结点 | 同理，$\tau<0$ 总收缩。 |
| $\Delta > 0, D < 0, \tau > 0$ | 不稳定焦点 | $D<0$ 进入抛物线内部，出现复根（旋转），$\tau>0$ 向外旋。 |
| $\Delta > 0, D < 0, \tau < 0$ | 稳定焦点 | $\tau<0$ 向内旋。 |
| $\Delta > 0, \tau = 0$ | 中心 | 零测度的抛物线中轴线，纯振荡。 |

## 3. 证明主线：为什么 $\tau-\Delta$ 足够？

由韦达定理：$\lambda_1 + \lambda_2 = \tau$，$\lambda_1\lambda_2 = \Delta$。

- $\Delta < 0 \Rightarrow \lambda_1\lambda_2 < 0$：两根异号 → 鞍点（无需 $\tau$）。
- $\Delta > 0$ 且 $\tau^2 - 4\Delta > 0$：两根同号实根，$\tau > 0$ 则同为负（稳定结点），$\tau < 0$ 则同为正（不稳定结点）。
- $\Delta > 0$ 且 $\tau^2 - 4\Delta < 0$：共轭复根，实部 $= \tau/2$，其符号决定稳定/不稳定焦点。
- $\Delta > 0, \tau = 0$：纯虚根 → 中心。

## 4. 反例：判别法的边界条件

**反例**：$\mathbf{x}' = \begin{pmatrix}0&1\\-1&0\end{pmatrix}\mathbf{x}$：$\tau=0, \Delta=1>0$ → 判为中心。这是线性系统，中心确实成立。**但若该系统来自非线性系统的线性化（如无阻尼摆），中心的稳定性是脆弱的**——微小非线性项可把它变成焦点（见「局部线性化」卡反例）。判别法只对线性系统本身严格成立，非线性情形要叠加 Hartman-Grobman 的"双曲"前提。

**反例 2（退化情形）**：$\Delta = 0$（特征值含零）时判别法失效（结点/直线/零特征值退化），需单独处理——此时平衡点非双曲，线性化结论同样不可信。

## 5. 条件变式

| 变式 | 改变什么 | 结果是否改变 | 结论 |
| :--- | :--- | :---: | :--- |
| $\Delta < 0$ | 迹任意 | 鞍点不变 | 无条件成立 |
| $\Delta = 0$ | 判别法 | 需另行判断 | 失效（退化） |
| $\tau^2 = 4\Delta$（抛物线上） | 重根 | 结点（临界结点） | 边界情形，仍稳定/不稳定同号 |
| 非线性系统线性化处 | 中心 | 可能变焦点 | 需 Hartman-Grobman 双曲前提 |

## 6. 常见误区

1. **把中心当稳定焦点**：$\tau = 0$ 是零测度边界，舍入误差都可能改变判定，工程上需谨慎。
2. **忽略 $\Delta = 0$ 退化**：特征值含 0 时平衡点非双曲，稳定性由更高阶项决定。
3. **非线性系统直接套用**：线性化的 $\tau-\Delta$ 只对双曲平衡点可靠。

## 7. 分级习题

#### 1. 综合例题：手算特征值与判别法
> [!question]- 答案与解析
> **题干**：给定 $\mathbf{x}'=\begin{pmatrix}1&2\\4&3\end{pmatrix}\mathbf{x}$，判定奇点类型。
> - **答案/证明**：$\tau=1+3=4,\ \Delta=1\cdot3-2\cdot4=-5<0 \implies$ **鞍点**！
> - **解析**：不需要算特征值！因为 $\Delta<0$，特征值必定一正一负（因为乘积为负），所以绝对是鞍点。

#### 2. 独立练习
- 判定 $\mathbf{x}' = \begin{pmatrix}0&1\\-4&0\end{pmatrix}\mathbf{x}$ 的奇点类型（答案：$\tau=0,\Delta=4$ → 中心）。
- 判定 $\mathbf{x}' = \begin{pmatrix}-1&2\\0&-3\end{pmatrix}\mathbf{x}$（答案：$\tau=-4,\Delta=3$，$D=16-12=4>0$ → 稳定结点）。

## 8. 闭卷验收

- [ ] 合上笔记，默写 $\tau-\Delta$ 判别准则表。
- [ ] 不看笔记，用判别法完成至少 3 个 $2\times2$ 矩阵的类型判定。
- [ ] 解释为什么 $\Delta<0$ 时可以直接判鞍点。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/06-常微分方程"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
