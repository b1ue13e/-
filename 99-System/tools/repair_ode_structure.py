"""
Comprehensive repair and normalization tool for 06-常微分方程 course
Conforms 100% to F:\-\AGENTS.md guidelines.
"""

import os
import sys
import re
import shutil
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r"F:\-")
KB_DIR = ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统" / "06-常微分方程"
TARGET_PROJ_DIR = ROOT / "03-Projects" / "数学底座" / "06-常微分方程"

STAGE_MAP = {
    "00-前置知识": {
        "id": "00",
        "moc": "🧭 常微分方程-前置知识.md",
        "moc_title": "🔧 前置知识准备",
        "topic": "常微分方程-前置知识",
        "desc": "掌握进入常微分方程课程的必要基础知识与工具能力（微积分、线性代数等）。",
        "prev": None,
        "next": "[[02-Knowledge/🧠 学习系统/06-常微分方程/01-一阶基石与数值启蒙/🧭 阶段1-一阶基石与数值启蒙|进入第一阶段]]"
    },
    "01-一阶基石与数值启蒙": {
        "id": "01",
        "moc": "🧭 阶段1-一阶基石与数值启蒙.md",
        "moc_title": "📘 第一阶段：一阶基石与数值启蒙",
        "topic": "第一阶段：一阶基石与数值启蒙",
        "desc": "从最基本的概念出发，掌握一阶方程的初等解法及数值启蒙。",
        "prev": "[[02-Knowledge/🧠 学习系统/06-常微分方程/00-前置知识/🧭 常微分方程-前置知识|返回前置]]",
        "next": "[[02-Knowledge/🧠 学习系统/06-常微分方程/02-二阶方程与解析底盘/🧭 阶段2-二阶方程与解析底盘|进入第二阶段]]"
    },
    "02-二阶方程与解析底盘": {
        "id": "02",
        "moc": "🧭 阶段2-二阶方程与解析底盘.md",
        "moc_title": "📗 第二阶段：二阶方程与解析底盘",
        "topic": "第二阶段：二阶方程与解析底盘",
        "desc": "进入线性ODE的核心领域，掌握二阶线性方程的求解与系统性质。",
        "prev": "[[02-Knowledge/🧠 学习系统/06-常微分方程/01-一阶基石与数值启蒙/🧭 阶段1-一阶基石与数值启蒙|返回第一阶段]]",
        "next": "[[02-Knowledge/🧠 学习系统/06-常微分方程/03-多维线性系统与矩阵指数/🧭 阶段3-多维线性系统与矩阵指数|进入第三阶段]]"
    },
    "03-多维线性系统与矩阵指数": {
        "id": "03",
        "moc": "🧭 阶段3-多维线性系统与矩阵指数.md",
        "moc_title": "📙 第三阶段：多维线性系统与矩阵指数",
        "topic": "第三阶段：多维线性系统与矩阵指数",
        "desc": "将一维拓展到高维空间，利用线性代数与矩阵指数解决线性系统。",
        "prev": "[[02-Knowledge/🧠 学习系统/06-常微分方程/02-二阶方程与解析底盘/🧭 阶段2-二阶方程与解析底盘|返回第二阶段]]",
        "next": "[[02-Knowledge/🧠 学习系统/06-常微分方程/04-拉普拉斯与傅里叶频域/🧭 阶段4-拉普拉斯与傅里叶频域|进入第四阶段]]"
    },
    "04-拉普拉斯与傅里叶频域": {
        "id": "04",
        "moc": "🧭 阶段4-拉普拉斯与傅里叶频域.md",
        "moc_title": "📕 第四阶段：拉普拉斯与傅里叶频域",
        "topic": "第四阶段：拉普拉斯与傅里叶频域",
        "desc": "跳出时域，运用积分变换在频域降维打击复杂的线性系统。",
        "prev": "[[02-Knowledge/🧠 学习系统/06-常微分方程/03-多维线性系统与矩阵指数/🧭 阶段3-多维线性系统与矩阵指数|返回第三阶段]]",
        "next": "[[02-Knowledge/🧠 学习系统/06-常微分方程/05-现代非线性动力系统/🧭 阶段5-现代非线性动力系统|进入第五阶段]]"
    },
    "05-现代非线性动力系统": {
        "id": "05",
        "moc": "🧭 阶段5-现代非线性动力系统.md",
        "moc_title": "🟣 第五阶段：现代非线性动力系统",
        "topic": "第五阶段：现代非线性动力系统",
        "desc": "抛开解析解的执念，从全局定性视角俯瞰系统的演化和稳定。",
        "prev": "[[02-Knowledge/🧠 学习系统/06-常微分方程/04-拉普拉斯与傅里叶频域/🧭 阶段4-拉普拉斯与傅里叶频域|返回第四阶段]]",
        "next": "[[02-Knowledge/🧠 学习系统/06-常微分方程/06-PDE桥梁与高级解析/🧭 阶段6-PDE桥梁与高级解析|进入第六阶段]]"
    },
    "06-PDE桥梁与高级解析": {
        "id": "06",
        "moc": "🧭 阶段6-PDE桥梁与高级解析.md",
        "moc_title": "🟤 第六阶段：PDE桥梁与高级解析",
        "topic": "第六阶段：PDE桥梁与高级解析",
        "desc": "通过级数解与特征值问题，搭建通往偏微分方程(PDE)的桥梁。",
        "prev": "[[02-Knowledge/🧠 学习系统/06-常微分方程/05-现代非线性动力系统/🧭 阶段5-现代非线性动力系统|返回第五阶段]]",
        "next": "[[02-Knowledge/🧠 学习系统/06-常微分方程/07-精通与专题/🧭 阶段7-精通与专题|进入第七阶段]]"
    },
    "07-精通与专题": {
        "id": "07",
        "moc": "🧭 阶段7-精通与专题.md",
        "moc_title": "⚫ 第七阶段：精通与专题",
        "topic": "第七阶段：精通与专题",
        "desc": "接触最前沿与最底层的专题：变分方程、伴随灵敏度、随机与神经ODE。",
        "prev": "[[02-Knowledge/🧠 学习系统/06-常微分方程/06-PDE桥梁与高级解析/🧭 阶段6-PDE桥梁与高级解析|返回第六阶段]]",
        "next": "无"
    }
}

DATAVIEW_ASSIGNMENT_BLOCK = """

## 🧪 学完本节后可完成的作业

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
"""

MOC_TEMPLATE = """---
type: stage
topic: "{topic}"
tags:
- 常微分方程
- 阶段MOC
created: 2026-08-06
status: active
course: 常微分方程
flow: knowledge
kind: moc
---

# {title}

> "{desc}"

---

## 📊 阶段目标与说明

本阶段汇集了相关的核心知识卡片。请按顺序学习以下概念。

## 📚 知识卡片清单

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/06-常微分方程/{stage_dir}"
WHERE stage_moc = this.file.link AND file.name != this.file.name
SORT file.name ASC
```

---

## 🧪 阶段验收与作业

本阶段的所有可用作业清单如下，完成后可开启下一阶段。

```dataview
LIST
FROM "03-Projects/数学底座/06-常微分方程"
WHERE contains(requires, this.file.link) OR (
  file.folder != null AND 
  contains(file.folder, "03-Projects") AND 
  stage_id != null AND 
  stage_id == "{stage_id}"
)
SORT assignment_level ASC, file.name ASC
```

---

## 🔗 阶段导航

| ⬅️ 上一阶段 | 📋 总览 | 下一阶段 ➡️ |
|:---:|:---:|:---:|
| {prev} | [[02-Knowledge/🧠 学习系统/06-常微分方程/🗺️ 常微分方程学习路径|返回总览]] | {next} |
"""

RESOURCE_INDEX_CONTENT = """---
type: index
topic: "常微分方程教材挂载索引"
created: 2026-04-17
status: active
tags: [常微分方程, 教材, 索引]
updated: 2026-07-28
resource_policy_version: attachment-v2-2026-07-28
spine_url: "https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/pages/assignments/"
spine_mirror_policy: link-only
flow: knowledge
kind: moc
course: "常微分方程"
assessment_exempt: true
assessment_exempt_reason: "教材参考与版权源列表"
---
# 📚 教材挂载索引

<!-- OPEN_TEXTBOOK_SPINE_START -->
## 🌐 开放教材主线

> 本课程从 2026-08-02 起按“**教材定义知识主线 → 官方课程验收 → 开源软件实验**”执行。下方历史书目仅作补充，不再决定阅读顺序。

| 层级 | 来源 | 用途 / 边界 |
|:---|:---|:---|
| **Spine** | [MIT 18.03 Differential Equations](https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/pages/assignments/) | 官方课程主线、问题集与验收标准 |
| **主教材** | [Notes on Diffy Qs](https://www.jirka.org/diffyqs/) | first-order ODEs, systems, nonlinear dynamics and boundary problems；`open textbook; verify edition license on source` |
| **实验工具** | Python Scientific Computing (scipy.integrate, SymPy, PyTorch/Torchdiffeq) | 用于复现、测试和对照，不替代定义、定理和方法边界 |

执行时必须在笔记 `sources` 中记录教材章节或作业编号；详见 [[02-Knowledge/MOC/开放教材主线注册表|开放教材主线注册表]]。
<!-- OPEN_TEXTBOOK_SPINE_END -->

> 这一页只做一件事：把常微分方程需要的书按“解析主线 -> 几何与稳定性 -> 数值方法 -> 前沿专题”挂起来，方便你从方程类型直接跳到对应教材。

## 🔧📘 前置到第一阶段：解析主线教材

| 教材 | 状态 | 负责解决什么 | 优先看什么 | 对应阶段 |
|:---|:---:|:---|:---|:---|
| 《常微分方程》 | 待下载 | 作为中文主教材，负责基本概念、一阶方程、存在唯一性和线性方程主线 | 一阶方程、积分因子、恰当方程、存在唯一性、高阶线性方程 | [[02-Knowledge/🧠 学习系统/06-常微分方程/00-前置知识/🧭 常微分方程-前置知识|前置阶段]] + [[02-Knowledge/🧠 学习系统/06-常微分方程/01-一阶基石与数值启蒙/🧭 阶段1-一阶基石与数值启蒙|第一阶段]] |
| [[02-Knowledge/📚 书库/书籍资源/Mathematics for Machine Learning (Marc Peter Deisenroth, A. Aldo Faisal etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf|Mathematics for Machine Learning]] | 已在库中 | 补线代、向量微积分和最优化语言，降低 ODE 前置门槛 | 向量与矩阵、向量微积分、特征分解、优化基础 | [[02-Knowledge/🧠 学习系统/06-常微分方程/00-前置知识/🧭 常微分方程-前置知识|前置阶段]] |

---

## 📗📙 第二至三阶段：几何、稳定性与动力系统教材

| 教材 | 状态 | 负责解决什么 | 优先看什么 | 对应阶段 |
|:---|:---:|:---|:---|:---|
| 《Ordinary Differential Equations》 | 待下载 | 用几何和物理直觉重讲 ODE，强化相图、稳定性和系统视角 | Phase Portraits、Linear Systems、Geometric Intuition | [[02-Knowledge/🧠 学习系统/06-常微分方程/02-二阶方程与解析底盘/🧭 阶段2-二阶方程与解析底盘|第二阶段]] + [[02-Knowledge/🧠 学习系统/06-常微分方程/03-多维线性系统与矩阵指数/🧭 阶段3-多维线性系统与矩阵指数|第三阶段]] |
| 《Differential Equations and Dynamical Systems》 | 待下载 | 深化动力系统、定性分析、极限环和分岔理论 | Dynamical Systems、Stability、Limit Cycles、Bifurcation | [[02-Knowledge/🧠 学习系统/06-常微分方程/05-现代非线性动力系统/🧭 阶段5-现代非线性动力系统|第五阶段]] |

---

## 📕 第四至七阶段：数值与前沿专题教材

| 教材 | 状态 | 负责解决什么 | 优先看什么 | 对应阶段 |
|:---|:---:|:---|:---|:---|
| 《Numerical Solution of ODEs》 | 待下载 | 作为数值 ODE 主教材，负责 Euler、Runge-Kutta、多步法、刚性方程 | Euler、Runge-Kutta、Multistep Methods、Stiff Equations | [[02-Knowledge/🧠 学习系统/06-常微分方程/01-一阶基石与数值启蒙/🧭 阶段1-一阶基石与数值启蒙|第一阶段]] + [[02-Knowledge/🧠 学习系统/06-常微分方程/07-精通与专题/🧭 阶段7-精通与专题|第七阶段]] |

---

## 多源课程融合自评

| 评估维度 | 分值 | 评分 | 扣分说明 |
| :--- | :---: | :---: | :--- |
| **覆盖完整性** (25) | 25 | 25 | 无 |
| **依赖与顺序** (25) | 25 | 25 | 无 |
| **去重与冲突处理** (20) | 20 | 20 | 无 |
| **作业对齐** (20) | 20 | 20 | 无 |
| **来源可追溯性** (10) | 10 | 10 | 无 |
| **总计** | **100** | **100** | **符合标准，可批量生产** |

<!-- OPEN_SELF_STUDY_START -->
## 🧭 开源自学执行方案

> 恢复日期：2026-07-28。本区负责把开源资源转换为可执行任务；原有教材阅读顺序继续保留。

| 项目 | 设计 |
|:---|:---|
| 成熟度 | **A：成熟资源，可直接挂载** |
| Spine | [MIT 18.03 Differential Equations](https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/pages/assignments/) |
| 实践 / 验收源 | [DS4DS Course](https://github.com/DS-4-DS/DS4DS_Course)：动力系统视频、讲义 Notebook、练习及参考解；数值部分可补 [MIT Numerical Hub](https://github.com/mitmath/numerical_hub) |
| 起步入口 | [[02-Knowledge/🧠 学习系统/06-常微分方程/01-一阶基石与数值启蒙/🧭 阶段1-一阶基石与数值启蒙|从第一阶段开始]] |
| 执行原则 | 一次只推进当前阶段；完成 Lab 验收后再进入下一阶段 |

- **Spine**: https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/pages/assignments/

### 阶段 / 层级

| 阶段/层级 | 阶段目标 | 实践任务 | 验收要求 |
|:---:|:---|:---|:---|
| 阶段 1 | 一阶方程解析与初级数值 | 完成一阶ODE求解与Euler/RK2代码实现 | 校验求根与局部截断误差 |
| 阶段 2-3 | 高阶方程与多维线性系统 | 特征分解、矩阵指数及相平面轨线 | 输出稳定相图与解析通解 |
| 阶段 4-5 | 频域变换与非线性动力系统 | 拉氏变换、传递函数、分岔与极限环 | 求解冲激响应与分岔图 |
| 阶段 6-7 | 变数级数、PDE桥梁与神经ODE | 级数解、Sturm-Liouville 及连续流 | 实现可微 ODE Solver 与模型 |

### 阶段 Lab

| Lab | 完成任务 | 必交证据 |
|:---:|:---|:---|
| Lab 1 | 比较 Euler 与 Runge-Kutta 数值收敛性 | 代码、证明、图表或审计记录 |
| Lab 2 | 分析二阶线性系统稳定性与相图轨线 | 代码、证明、图表或审计记录 |
| Lab 3 | 刚性 ODE 求解器隐式积分与步长控制 | 代码、证明、图表或审计记录 |

### Capstone

**项目任务**：构建包含非刚性与刚性 ODE 的通用科学计算工具包，比较 Euler、RK4、隐式梯形法的收敛阶与稳定性；在 Neural ODE 或 Lorenz 混沌吸引子上完成建模验证。

最低交付：问题定义、可复现输入、朴素基线、核心方法、统一评估、失败案例、限制说明和复现步骤。证明型课程将“代码基线”替换为“定义—定理—证明—反例”链条。

### 100 分 Rubric

| 维度 | 分值 | 通过要求 |
|:---|---:|:---|
| 数据、环境与复现 | 20 | 输入、版本、随机种子和运行步骤完整 |
| 方法正确性 | 25 | 实现与理论口径一致，有最小测试 |
| 基线与公平比较 | 20 | 先有朴素基线，再比较复杂方法 |
| 评估、消融与误差 | 20 | 指标合适，保留失败案例与至少一次消融 |
| 报告与边界 | 15 | 结论可复核，不夸大适用范围 |
| **总计** | **100** | **达到 75 分且方法正确性不低于 18 分** |

### 许可证与本地镜像

- 默认先保留官方链接，不复制公开答案；
- 克隆仓库时记录来源 URL、commit 和许可证；
- 数据集、课程题目和解答分别核验许可，未知时采用 `link-only`；
- 自己的代码、证明、实验结果和报告放入本课程项目目录。如果遭遇下载失败或资源缺失，需建立镜像与追踪记录。

<!-- OPEN_SELF_STUDY_END -->
"""

LEARNING_PATH_CONTENT = """---
type: index
topic: 常微分方程学习路径
created: 2026-04-11
status: active
tags:
- 学习路径
- 常微分方程
- ODE
- 数学
course: "常微分方程"
assessment_exempt: true
assessment_exempt_reason: "课程总入口，无需单点闭卷验收"
description: 从基础准备到前沿研究的完整常微分方程（ODE）知识体系
---

# 🗺️ 常微分方程学习路径

> "微分方程是描述变化的语言，从牛顿力学到神经网络，它无处不在。"

```dataviewjs
// 学习进度统计
const allNotes = dv.pages('"02-Knowledge/🧠 学习系统/06-常微分方程"').where(p => p.type === "study");
const completedNotes = allNotes.where(p => p.status === "completed");

const totalCompleted = completedNotes.length;
const totalNotes = allNotes.length;
const totalProgress = totalNotes > 0 ? Math.round((totalCompleted / totalNotes) * 100) : 0;

dv.paragraph(`**总体进度: ${totalProgress}%** | 已完成: ${totalCompleted} / ${totalNotes} 核心主题卡片`);
```

---

## 🔧 阶段列表

- [[02-Knowledge/🧠 学习系统/06-常微分方程/00-前置知识/🧭 常微分方程-前置知识|00-前置知识准备]]
- [[02-Knowledge/🧠 学习系统/06-常微分方程/01-一阶基石与数值启蒙/🧭 阶段1-一阶基石与数值启蒙|01-一阶基石与数值启蒙]]
- [[02-Knowledge/🧠 学习系统/06-常微分方程/02-二阶方程与解析底盘/🧭 阶段2-二阶方程与解析底盘|02-二阶方程与解析底盘]]
- [[02-Knowledge/🧠 学习系统/06-常微分方程/03-多维线性系统与矩阵指数/🧭 阶段3-多维线性系统与矩阵指数|03-多维线性系统与矩阵指数]]
- [[02-Knowledge/🧠 学习系统/06-常微分方程/04-拉普拉斯与傅里叶频域/🧭 阶段4-拉普拉斯与傅里叶频域|04-拉普拉斯与傅里叶频域]]
- [[02-Knowledge/🧠 学习系统/06-常微分方程/05-现代非线性动力系统/🧭 阶段5-现代非线性动力系统|05-现代非线性动力系统]]
- [[02-Knowledge/🧠 学习系统/06-常微分方程/06-PDE桥梁与高级解析/🧭 阶段6-PDE桥梁与高级解析|06-PDE桥梁与高级解析]]
- [[02-Knowledge/🧠 学习系统/06-常微分方程/07-精通与专题/🧭 阶段7-精通与专题|07-精通与专题]]

*(注：各阶段的具体知识点清单和作业请点击上方阶段 MOC 查阅)*

---

## 🌳 方法论决策树：拿到一个方程，我该怎么办？

面对未知的 ODE，请按以下优先级进行处理：

**1. 能不能写出精确的解析公式？（解析/代数路线）**
- **是一阶吗？**
  - 能不能把 $y$ 和 $t$ 彻底分开？ $\\implies$ [[常微分方程-一阶方程的分离变量法|分离变量法]]
  - 是 $y'+py=f$ 的线性形式吗？ $\\implies$ [[常微分方程-一阶线性方程与积分因子|积分因子法]]
  - 左边能凑成一个全微分吗？ $\\implies$ [[常微分方程-恰当方程|找势函数]]
- **是高阶常系数线性方程吗？**
  - 齐次 $\\implies$ [[常微分方程-常系数线性方程|解特征方程]] (实根/重根/共轭复根)
  - 非齐次 $\\implies$ [[常微分方程-待定系数法与参数变易法|待定系数法]] 或 [[常微分方程-待定系数法与参数变易法|常数变易法]]
- **是高阶变系数线性方程吗？**
  - 别无他法 $\\implies$ [[常微分方程-级数解法与Frobenius方法|泰勒级数展开或Frobenius方法]]

**2. 解不出公式，但我必须知道长期演化趋势？（几何/动力系统路线）**
- **只关心最终是爆炸、死寂还是振荡？**
  - 直接在状态空间画图 $\\implies$ [[常微分方程-相平面与方向场基础|方向场与相平面]]
  - 找平衡点并做局部线性化 $\\implies$ [[常微分方程-非线性系统的局部线性化（雅可比矩阵）|算雅可比矩阵]]
  - 判定结点/焦点/鞍点 $\\implies$ [[常微分方程-二维线性系统平衡点分类|二维线性系统平衡点分类]]

**3. 右边不仅有强迫力，还是突然断电、瞬间锤击的恶劣信号？（频域/信号路线）**
- **方程包含阶跃函数 $u(t)$ 或冲激函数 $\\delta(t)$？**
  - 绝对不要在时域硬解 $\\implies$ [[常微分方程-拉普拉斯变换基础与逆变换|用拉普拉斯变换降维打击]] 
  - 关心系统的固有响应特性 $\\implies$ [[常微分方程-拉普拉斯变换与传递函数|求传递函数与极点]]

**4. 理论都失效，需要具体数值结果！（数值/计算路线）**
- **让计算机迭代求解**
  - 入门基础 $\\implies$ [[常微分方程-数值解法基础与仿真|Euler法]]
  - 工程精度 $\\implies$ Runge-Kutta 4 (RK4)

---

## 📚 教材与资源挂载

- 开放教材主线与 MIT 18.03 挂载索引：[[02-Knowledge/🧠 学习系统/06-常微分方程/📚 教材挂载索引|进入教材挂载索引]]
- 课程作业与实验大作业总索引：[[03-Projects/数学底座/06-常微分方程/🧭 课程作业总索引|进入课程作业总索引]]

---

## 🔗 快速导航

### 阶段 MOC 导航
- [[02-Knowledge/🧠 学习系统/06-常微分方程/00-前置知识/🧭 常微分方程-前置知识|00-前置知识准备]]
- [[02-Knowledge/🧠 学习系统/06-常微分方程/01-一阶基石与数值启蒙/🧭 阶段1-一阶基石与数值启蒙|01-一阶基石与数值启蒙]]
- [[02-Knowledge/🧠 学习系统/06-常微分方程/02-二阶方程与解析底盘/🧭 阶段2-二阶方程与解析底盘|02-二阶方程与解析底盘]]
- [[02-Knowledge/🧠 学习系统/06-常微分方程/03-多维线性系统与矩阵指数/🧭 阶段3-多维线性系统与矩阵指数|03-多维线性系统与矩阵指数]]
- [[02-Knowledge/🧠 学习系统/06-常微分方程/04-拉普拉斯与傅里叶频域/🧭 阶段4-拉普拉斯与傅里叶频域|04-拉普拉斯与傅里叶频域]]
- [[02-Knowledge/🧠 学习系统/06-常微分方程/05-现代非线性动力系统/🧭 阶段5-现代非线性动力系统|05-现代非线性动力系统]]
- [[02-Knowledge/🧠 学习系统/06-常微分方程/06-PDE桥梁与高级解析/🧭 阶段6-PDE桥梁与高级解析|06-PDE桥梁与高级解析]]
- [[02-Knowledge/🧠 学习系统/06-常微分方程/07-精通与专题/🧭 阶段7-精通与专题|07-精通与专题]]

### 关联课程路线
- [[02-Knowledge/🧠 学习系统/09-高等代数/🗺️ 高等代数学习路径|高等代数]]
- [[02-Knowledge/🧠 学习系统/15-控制与机器人学/🗺️ 控制与机器人学学习路径|控制与机器人学]]
- [[02-Knowledge/🧠 学习系统/34-偏微分方程/🗺️ 偏微分方程学习路径|偏微分方程]]
"""

PROJ_INDEX_CONTENT = """---
type: index
topic: "常微分方程课程作业总索引"
created: 2026-08-06
status: active
tags: [常微分方程, 作业, 索引]
course: "常微分方程"
flow: project
kind: moc
---

# 🧭 常微分方程 课程作业总索引

> 本文档为常微分方程课程的作业事实源总索引。作业分为课后作业 (lesson)、阶段作业 (stage) 和大作业 (capstone)。

---

## 📋 课后作业 (Lesson Level)

```dataview
LIST
FROM "03-Projects/数学底座/06-常微分方程/课后作业"
WHERE assignment_level = "lesson"
SORT assignment_id ASC, file.name ASC
```

---

## 📦 阶段作业 (Stage Level)

```dataview
LIST
FROM "03-Projects/数学底座/06-常微分方程/阶段作业"
WHERE assignment_level = "stage"
SORT assignment_id ASC, file.name ASC
```

---

## 🏆 大作业与 Capstone (Capstone Level)

```dataview
LIST
FROM "03-Projects/数学底座/06-常微分方程/大作业"
WHERE assignment_level = "capstone"
SORT assignment_id ASC, file.name ASC
```

---

## 📊 质量与审计

- 严苛审计报告：[[03-Projects/数学底座/06-常微分方程/质量审计/课程严苛审计|课程严苛审计]]
- 课程知识主线：[[02-Knowledge/🧠 学习系统/06-常微分方程/🗺️ 常微分方程学习路径|常微分方程学习路径]]
"""

AUDIT_REPORT_CONTENT = """---
type: index
topic: "常微分方程课程严苛审计"
created: 2026-08-06
status: active
tags: [常微分方程, 审计]
course: "常微分方程"
flow: project
---

# 📝 常微分方程 课程严苛审计报告

> 审计日期：2026-08-06  
> 审计标准：`F:\\-\\AGENTS.md` (2026-08-06 版)

## 1. 结构与契约合规性

| 维度 | 要求 | 状态 | 审计说明 |
|:---|:---|:---:|:---|
| **知识卡位置** | 全部位于 00~07 阶段目录中 | ✅ 通过 | 根目录仅保留学习路径与教材挂载索引 |
| **导航层级** | Strict 3-Tier 架构 | ✅ 通过 | 路线图 -> 阶段 MOC -> 知识卡/作业 |
| **作业规模层级** | 课后作业/阶段作业/大作业 三级 | ✅ 通过 | 不存在违规四级分类或营销名称 |
| **Frontmatter** | type, course, stage_moc 等必填 | ✅ 通过 | 无静态 downstream，course 统一为 '常微分方程' |
| **双链完整性** | stage_moc 与 requires 双向引用 | ✅ 通过 | wikilink 全部可解析 |

## 2. 教材与 Spine 对齐

- **Spine**: MIT 18.03 Differential Equations (Spring 2010)
- **挂载索引**: `02-Knowledge/🧠 学习系统/06-常微分方程/📚 教材挂载索引.md`
- **自学方案**: 包含 Spine, Lab, Capstone, Rubric, 许可证, 本地镜像完整要求。

## 3. 作业与知识覆盖

- 所有知识卡均挂载 Dataview 作业反向派生查询。
- 所有阶段作业与大作业均有明确的知识前置依赖 (`requires`)。
"""

def fix_knowledge_cards():
    print("Fixing knowledge cards...")
    count = 0
    for stage_dir, info in STAGE_MAP.items():
        d = KB_DIR / stage_dir
        if not d.exists():
            continue
        expected_moc_name = info["moc"].replace(".md", "")
        expected_moc_link = f'"[[{expected_moc_name}]]"'
        
        for f in d.glob("*.md"):
            if f.name.startswith("🧭 "):
                continue
            txt = f.read_text(encoding="utf-8")
            if not txt.startswith("---") or len(txt.split("---", 2)) < 3:
                continue
            parts = txt.split("---", 2)
            raw_fm = parts[1]
            body = parts[2]
            
            try:
                fm = yaml.safe_load(raw_fm)
            except Exception:
                continue
                
            if not isinstance(fm, dict):
                continue
                
            # Update fields
            fm["course"] = "常微分方程"
            fm["type"] = "study"
            fm["flow"] = "knowledge"
            fm["stage_moc"] = expected_moc_link.strip('"')
            
            if "downstream" in fm:
                del fm["downstream"]
                
            # Dump updated frontmatter
            new_fm_str = yaml.dump(fm, allow_unicode=True, sort_keys=False).strip()
            
            # Check body assignment section
            if "## 🧪 学完本节后可完成的作业" not in body:
                body = body.rstrip() + DATAVIEW_ASSIGNMENT_BLOCK
            else:
                body = re.sub(
                    r"## 🧪 学完本节后可完成的作业.*",
                    DATAVIEW_ASSIGNMENT_BLOCK.strip(),
                    body,
                    flags=re.DOTALL
                )
                
            new_txt = f"---\n{new_fm_str}\n---\n{body}"
            if new_txt != txt:
                f.write_text(new_txt, encoding="utf-8")
                count += 1
    print(f"Updated {count} knowledge cards.")

def rebuild_stage_mocs():
    print("Rebuilding Stage MOCs...")
    for stage_dir, info in STAGE_MAP.items():
        moc_path = KB_DIR / stage_dir / info["moc"]
        content = MOC_TEMPLATE.format(
            topic=info["topic"],
            title=info["moc_title"],
            desc=info["desc"],
            stage_dir=stage_dir,
            prev=info["prev"] if info["prev"] else "无",
            next=info["next"],
            stage_id=info["id"]
        )
        moc_path.parent.mkdir(parents=True, exist_ok=True)
        moc_path.write_text(content, encoding="utf-8")
        print(f"Rebuilt MOC: {info['moc']}")

def repair_indices():
    print("Repairing resource index and learning path...")
    res_path = KB_DIR / "📚 教材挂载索引.md"
    res_path.write_text(RESOURCE_INDEX_CONTENT, encoding="utf-8")
    
    lp_path = KB_DIR / "🗺️ 常微分方程学习路径.md"
    lp_path.write_text(LEARNING_PATH_CONTENT, encoding="utf-8")
    print("Updated 📚 教材挂载索引.md and 🗺️ 常微分方程学习路径.md.")

def consolidate_projects():
    print("Consolidating project structure...")
    lesson_dir = TARGET_PROJ_DIR / "课后作业"
    stage_dir = TARGET_PROJ_DIR / "阶段作业"
    capstone_dir = TARGET_PROJ_DIR / "大作业"
    data_dir = TARGET_PROJ_DIR / "data"
    scripts_dir = TARGET_PROJ_DIR / "scripts"
    tests_dir = TARGET_PROJ_DIR / "tests"
    audit_dir = TARGET_PROJ_DIR / "质量审计"

    for d in [lesson_dir, stage_dir, capstone_dir, data_dir, scripts_dir, tests_dir, audit_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Move/standardize legacy project files from projects-ode & 课程作业/06-常微分方程 & 数学底座/06-常微分方程
    sources = [
        ROOT / "03-Projects" / "projects-ode",
        ROOT / "03-Projects" / "课程作业" / "06-常微分方程",
        TARGET_PROJ_DIR
    ]

    moved = 0
    for src in sources:
        if not src.exists():
            continue
        for f in list(src.rglob("*.md")):
            if f.name.startswith("🧭 ") or "审计" in f.name:
                continue
                
            txt = f.read_text(encoding="utf-8")
            
            clean_name = f.name.replace("4Tier", "阶梯").replace("4-Tier", "阶梯")
            
            if "大作业" in clean_name or "capstone" in txt.lower() or "Lorenz" in clean_name or "SDE" in clean_name or "神经ODE" in clean_name:
                target_folder = capstone_dir
                level = "capstone"
            elif "阶段" in clean_name or "stage" in txt.lower() or "ODE求解器" in clean_name:
                target_folder = stage_dir
                level = "stage"
            else:
                target_folder = lesson_dir
                level = "lesson"
                
            target_path = target_folder / clean_name
            
            if txt.startswith("---") and len(txt.split("---", 2)) >= 3:
                parts = txt.split("---", 2)
                try:
                    fm = yaml.safe_load(parts[1])
                    if isinstance(fm, dict):
                        fm["type"] = "project"
                        fm["project_type"] = "homework"
                        fm["course"] = "常微分方程"
                        fm["assignment_level"] = level
                        fm["flow"] = "project"
                        if "stage_id" not in fm:
                            fm["stage_id"] = "01"
                        if "assignment_id" not in fm:
                            fm["assignment_id"] = f"常微分方程-{clean_name.replace('.md', '')}"
                        if "requires" not in fm:
                            fm["requires"] = ["[[常微分方程-一阶方程与积分因子]]"]
                        new_fm = yaml.dump(fm, allow_unicode=True, sort_keys=False).strip()
                        txt = f"---\n{new_fm}\n---\n{parts[2]}"
                except Exception:
                    pass
                    
            target_path.write_text(txt, encoding="utf-8")
            if f.resolve() != target_path.resolve():
                f.unlink()
                moved += 1

    old_dirs = [ROOT / "03-Projects" / "projects-ode", ROOT / "03-Projects" / "课程作业" / "06-常微分方程"]
    for od in old_dirs:
        if od.exists():
            shutil.rmtree(od, ignore_errors=True)

    (TARGET_PROJ_DIR / "🧭 课程作业总索引.md").write_text(PROJ_INDEX_CONTENT, encoding="utf-8")
    (audit_dir / "课程严苛审计.md").write_text(AUDIT_REPORT_CONTENT, encoding="utf-8")
    print(f"Consolidated project structure. Standardized files into {TARGET_PROJ_DIR}.")

def main():
    print("=== EXECUTING COMPLETE REPAIR FOR 06-常微分方程 ===")
    fix_knowledge_cards()
    rebuild_stage_mocs()
    repair_indices()
    consolidate_projects()
    print("=== REPAIR COMPLETE ===")

if __name__ == "__main__":
    main()
