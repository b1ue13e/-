---
type: stage
cssclasses:
  - atlas-page
  - atlas-stage
topic: 第三阶段：进阶 (Advanced)
tags:
- 常微分方程
- 进阶
- 稳定性
- 定性理论
- 边值问题
created: 2026-04-11
status: learning
difficulty: intermediate
concept: []
prerequisites: []
related: []
phase: 3
---

# 📙 第三阶段：进阶 (Advanced)

> "从定量求解走向定性分析，探索非线性系统的丰富行为。"

---

## 📊 阶段进度

```dataviewjs
const notes = dv.pages('"02-Knowledge/🧠 学习系统"')
  .where(p => p.type === "study"
    && !p.template
    && (p.note_role ?? "concept") === "concept"
    && p.course === "常微分方程"
    && p.stage === "第三阶段：进阶 (Advanced)");
const completed = notes.where(p => p.status === "completed").length;
const total = notes.length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**阶段进度: ${progress}%** (${completed}/${total} 概念卡)`);
```

---

## ⚖️ 稳定性理论

### Lyapunov稳定性

| 概念 | 定义 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **Lyapunov稳定** | 初值小扰动→解小扰动 | ⬜ | [[02-Knowledge/🧠 学习系统/06-常微分方程/03-进阶/Lyapunov稳定\|Lyapunov稳定]] |
| **渐近稳定** | 稳定且趋于平衡点 | ⬜ | [[渐近稳定]] |
| **不稳定** | 不满足稳定条件 | ⬜ | [[不稳定]] |
| **指数稳定** | 以指数速度收敛 | ⬜ | [[指数稳定]] |

### Lyapunov函数

| 方法 | 核心思想 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **Lyapunov直接法** | 构造V(x)判定稳定性 | ⬜ | [[Lyapunov直接法]] |
| **V函数构造** | 能量函数、二次型 | ⬜ | [[V函数构造]] |
| **LaSalle原理** | 不变集原理 | ⬜ | [[LaSalle原理]] |

### 线性化判别法

| 定理 | 内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **Lyapunov第一方法** | 线性化系统的特征值决定局部稳定性 | ⬜ | [[线性化判别]] |
| **Hartman-Grobman** | 双曲平衡点附近，非线性系统等价于线性化 | ⬜ | [[HartmanGrobman]] |

---

## 🌀 非线性系统定性理论

### 极限环

| 概念 | 定义 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **极限环** | 孤立闭轨线 | ⬜ | [[极限环]] |
| **稳定性** | 稳定/不稳定/半稳定 | ⬜ | [[极限环稳定性]] |
| **Bendixson准则** | 排除极限环的条件 | ⬜ | [[Bendixson准则]] |
| **Poincaré映射** | 分析极限环稳定性 | ⬜ | [[Poincaré映射]] |

### Poincaré-Bendixson定理

| 内容 | 意义 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **定理陈述** | 平面有界区域内的渐近行为 | ⬜ | [[PB定理]] |
| **应用** | 证明极限环存在 | ⬜ | [[PB应用]] |
| **高维限制** | 仅适用于二维系统 | ⬜ | [[PB限制]] |

### 分岔理论初步

| 类型 | 特征 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **鞍结分岔** | 平衡点产生/消失 | ⬜ | [[鞍结分岔]] |
| **Hopf分岔** | 平衡点→极限环 | ⬜ | [[Hopf分岔]] |
| **叉式分岔** | 对称性破缺 | ⬜ | [[叉式分岔]] |
| **跨临界分岔** | 平衡点交换稳定性 | ⬜ | [[跨临界分岔]] |

---

## 📏 边值问题

### Sturm-Liouville理论

| 形式 | (p(x)y')' + [λw(x) - q(x)]y = 0 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **自伴算子** | Sturm-Liouville算子 | ⬜ | [[自伴算子]] |
| **边界条件** | 分离/周期/混合 | ⬜ | [[SL边界条件]] |
| **特征值性质** | 可数、单重、趋于无穷 | ⬜ | [[SL特征值]] |
| **特征函数正交性** | 关于权函数w(x)正交 | ⬜ | [[特征函数正交]] |

### 特征值问题

| 例子 | 方程 | 特征值/函数 | 状态 | 笔记 |
|:---|:---|:---|:---:|:---|
| **简单谐振子** | y'' + λy = 0 | sin(nx), cos(nx) | ⬜ | [[谐振子特征值]] |
| **Legendre方程** | 球谐函数基础 | Legendre多项式 | ⬜ | [[Legendre特征值]] |
| **Bessel方程** | 柱坐标分离 | Bessel函数 | ⬜ | [[Bessel特征值]] |

### 正交函数系

| 应用 | 内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
| **广义Fourier级数** | 按特征函数展开 | ⬜ | [[广义Fourier]] |
| **Green函数** | 边值问题的核函数 | ⬜ | [[Green函数]] |
| **特征函数展开法** | 求解非齐次边值问题 | ⬜ | [[特征函数展开]] |

---

## 🛠️ 阶段练习

| 练习 | 内容 | 目标 | 状态 | 笔记 |
|:---|:---|:---|:---:|:---|
| **稳定性分析** | 构造Lyapunov函数 | 定性判断 | ⬜ | [[练习-稳定性]] |
| **相图分析** | 非线性系统相图 | 极限环识别 | ⬜ | [[练习-非线性相图]] |
| **分岔分析** | 单参数系统 | 分岔图绘制 | ⬜ | [[练习-分岔]] |
| **边值问题** | S-L问题求解 | 特征值计算 | ⬜ | [[练习-边值]] |

---

<!-- curriculum-repair:start -->
## 🧩 教材对齐索引

| 模块 | 要解决的问题 | 教材定位 | 原子卡片 | 完成标准 |
|:---|:---|:---|:---|:---|
| Lyapunov稳定性 | 理解“Lyapunov稳定性”中的“Lyapunov稳定”，并能说明它在“📙 第三阶段：进阶 (Advanced)”中的作用。 | Phase Portraits、Linear Systems、Geometric Intuition、Stability；Dynamical Systems、Stability、Limit Cycles、Bifurcation；线性方程组、边值问题、特殊函数 | [[02-Knowledge/🧠 学习系统/06-常微分方程/03-进阶/Lyapunov稳定]]<br>[[渐近稳定]]<br>[[不稳定]]<br>[[指数稳定]] | 能用自己的话解释“Lyapunov稳定”，给出一个最小例子，并说明它与本模块相邻概念的关系。 |
| Lyapunov函数 | 理解“Lyapunov函数”中的“Lyapunov直接法”，并能说明它在“📙 第三阶段：进阶 (Advanced)”中的作用。 | Phase Portraits、Linear Systems、Geometric Intuition、Stability；Dynamical Systems、Stability、Limit Cycles、Bifurcation；线性方程组、边值问题、特殊函数 | [[Lyapunov直接法]]<br>[[V函数构造]]<br>[[LaSalle原理]] | 能用自己的话解释“Lyapunov直接法”，给出一个最小例子，并说明它与本模块相邻概念的关系。 |
| 线性化判别法 | 理解“线性化判别法”中的“线性化判别”，并能说明它在“📙 第三阶段：进阶 (Advanced)”中的作用。 | Phase Portraits、Linear Systems、Geometric Intuition、Stability；Dynamical Systems、Stability、Limit Cycles、Bifurcation；线性方程组、边值问题、特殊函数 | [[线性化判别]]<br>[[HartmanGrobman]] | 能用自己的话解释“线性化判别”，给出一个最小例子，并说明它与本模块相邻概念的关系。 |
| 极限环 | 理解“极限环”中的“极限环”，并能说明它在“📙 第三阶段：进阶 (Advanced)”中的作用。 | Phase Portraits、Linear Systems、Geometric Intuition、Stability；Dynamical Systems、Stability、Limit Cycles、Bifurcation；线性方程组、边值问题、特殊函数 | [[极限环]]<br>[[极限环稳定性]]<br>[[Bendixson准则]]<br>[[Poincaré映射]] | 能用自己的话解释“极限环”，给出一个最小例子，并说明它与本模块相邻概念的关系。 |
| Poincaré-Bendixson定理 | 理解“Poincaré-Bendixson定理”中的“PB定理”，并能说明它在“📙 第三阶段：进阶 (Advanced)”中的作用。 | Phase Portraits、Linear Systems、Geometric Intuition、Stability；Dynamical Systems、Stability、Limit Cycles、Bifurcation；线性方程组、边值问题、特殊函数 | [[PB定理]]<br>[[PB应用]]<br>[[PB限制]] | 能用自己的话解释“PB定理”，给出一个最小例子，并说明它与本模块相邻概念的关系。 |
| 分岔理论初步 | 理解“分岔理论初步”中的“鞍结分岔”，并能说明它在“📙 第三阶段：进阶 (Advanced)”中的作用。 | Phase Portraits、Linear Systems、Geometric Intuition、Stability；Dynamical Systems、Stability、Limit Cycles、Bifurcation；线性方程组、边值问题、特殊函数 | [[鞍结分岔]]<br>[[Hopf分岔]]<br>[[叉式分岔]]<br>[[跨临界分岔]] | 能用自己的话解释“鞍结分岔”，给出一个最小例子，并说明它与本模块相邻概念的关系。 |
| Sturm-Liouville理论 | 理解“Sturm-Liouville理论”中的“自伴算子”，并能说明它在“📙 第三阶段：进阶 (Advanced)”中的作用。 | Phase Portraits、Linear Systems、Geometric Intuition、Stability；Dynamical Systems、Stability、Limit Cycles、Bifurcation；线性方程组、边值问题、特殊函数 | [[自伴算子]]<br>[[SL边界条件]]<br>[[SL特征值]]<br>[[特征函数正交]] | 能用自己的话解释“自伴算子”，给出一个最小例子，并说明它与本模块相邻概念的关系。 |
| 特征值问题 | 理解“特征值问题”中的“谐振子特征值”，并能说明它在“📙 第三阶段：进阶 (Advanced)”中的作用。 | Phase Portraits、Linear Systems、Geometric Intuition、Stability；Dynamical Systems、Stability、Limit Cycles、Bifurcation；线性方程组、边值问题、特殊函数 | [[谐振子特征值]]<br>[[Legendre特征值]]<br>[[Bessel特征值]] | 能用自己的话解释“谐振子特征值”，给出一个最小例子，并说明它与本模块相邻概念的关系。 |
| 正交函数系 | 理解“正交函数系”中的“广义Fourier”，并能说明它在“📙 第三阶段：进阶 (Advanced)”中的作用。 | Phase Portraits、Linear Systems、Geometric Intuition、Stability；Dynamical Systems、Stability、Limit Cycles、Bifurcation；线性方程组、边值问题、特殊函数 | [[广义Fourier]]<br>[[Green函数]]<br>[[特征函数展开]] | 能用自己的话解释“广义Fourier”，给出一个最小例子，并说明它与本模块相邻概念的关系。 |
| 🛠️ 阶段练习 | 理解“🛠️ 阶段练习”中的“练习-稳定性”，并能说明它在“📙 第三阶段：进阶 (Advanced)”中的作用。 | Phase Portraits、Linear Systems、Geometric Intuition、Stability；Dynamical Systems、Stability、Limit Cycles、Bifurcation；线性方程组、边值问题、特殊函数 | [[练习-稳定性]]<br>[[练习-非线性相图]]<br>[[练习-分岔]]<br>[[练习-边值]] | 能用自己的话解释“练习-稳定性”，给出一个最小例子，并说明它与本模块相邻概念的关系。 |

<!-- curriculum-repair:end -->

## 🔗 阶段导航

| ⬅️ 上一阶段 | 📋 总览 | 下一阶段 ➡️ |
|:---:|:---:|:---:|
| [[02-Knowledge/🧠 学习系统/06-常微分方程/03-进阶/📗 第二阶段：中级\|返回第二阶段]] | [[🗺️ 常微分方程学习路径|返回总览]] | [[02-Knowledge/🧠 学习系统/06-常微分方程/03-进阶/📕 第四阶段：精通与专题\|进入第四阶段]] |

---

*阶段创建：2026-04-11*

---

## 🃏 间隔复习卡片

> 用 **Spaced Repetition** 插件复习。
> 格式：单行卡 `问题 :: 答案`；多行卡：问题 → 空行 → `?` → 空行 → 答案。
> 写卡原则：用自己的话，答案不超过 3 句，每张卡只考一件事。

#flashcard

这个概念解决的核心问题是什么？ :: （填写）

最关键的公式/定义是什么？ :: （填写）

最容易混淆的概念是什么？区别在哪？ ::
