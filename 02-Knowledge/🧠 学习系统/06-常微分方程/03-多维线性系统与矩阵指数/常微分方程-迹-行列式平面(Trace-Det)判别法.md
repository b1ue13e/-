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

## 3. 分级习题

#### 1. 综合例题：手算特征值与判别法
> [!question]- 答案与解析
> **题干**：给定 $\mathbf{x}'=\begin{pmatrix}1&2\\4&3\end{pmatrix}\mathbf{x}$，判定奇点类型。
> - **答案/证明**：$\tau=1+3=4,\ \Delta=1\cdot3-2\cdot4=-5<0 \implies$ **鞍点**！
> - **解析**：不需要算特征值！因为 $\Delta<0$，特征值必定一正一负（因为乘积为负），所以绝对是鞍点。


## 🧪 学完本节后可完成的作业

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

 解决经典方法在特定条件下的局限性。

## ⚠️ 常见误区与边界条件

1. **混淆适用范围**: 注意算子有界性与系统线性/非线性前提。
2. **边界条件缺失**: 初值/边值条件不足时解不唯一。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/数学底座/06-常微分方程"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
