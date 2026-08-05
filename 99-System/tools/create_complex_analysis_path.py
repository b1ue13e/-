#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path("02-Knowledge/🧠 学习系统/37-复变函数")
TODAY = "2026-06-12"


STAGES = [
    {
        "dir": "01-复数与复函数直觉",
        "file": "📘 第一阶段：复数与复函数直觉.md",
        "emoji": "📘",
        "heading": "📘 第一阶段：复数与复函数直觉",
        "topic": "第一阶段：复数与复函数直觉",
        "difficulty": "beginner",
        "duration": "2-3周",
        "concept": ["复数", "复平面", "复函数", "Euler公式"],
        "quote": "先把复数看成平面上的缩放、旋转和映射，而不是只看成带 i 的代数符号。",
        "modules": [
            {
                "name": "复数代数与几何",
                "problem": "复数为什么能同时表达长度、角度、旋转和振荡？",
                "source": "Brown & Churchill：Complex Numbers；Needham：Euler's Formula、Transformations and Euclidean Geometry",
                "cards": ["复数的代数表示", "复平面与模辐角", "极形式与Euler公式"],
                "standard": "能在代数形式、极形式和几何图像之间自由转换，并解释乘法为什么对应旋转与缩放。",
            },
            {
                "name": "复函数与映射",
                "problem": "复函数为什么应该被看成平面到平面的变换？",
                "source": "Needham：Complex Functions as Transformations；Brown & Churchill：Functions of a Complex Variable",
                "cards": ["复函数作为平面映射", "初等复变换", "区域与曲线"],
                "standard": "能用最小例子说明平移、旋转、缩放、倒数映射对区域和曲线的影响。",
            },
            {
                "name": "极限连续与分支直觉",
                "problem": "复变量中的极限、连续和多值性和实变量有什么不同？",
                "source": "Brown & Churchill：Limits、Continuity、Branches of Multiple-Valued Functions；Needham：Multifunctions、The Logarithm Function",
                "cards": ["复函数极限", "复函数连续性", "多值性与分支直觉"],
                "standard": "能解释复平面中从任意路径趋近的要求，以及为什么对数、根号需要选择分支。",
            },
            {
                "name": "跨路径直觉",
                "problem": "复变函数为什么会进入信号、控制和概率中的频域语言？",
                "source": "MIT OCW 18.04：Applications overview；Brown & Churchill：Applications of Complex Variables",
                "cards": ["复变函数与傅里叶直觉", "复变函数与控制极点", "复变函数问题类型"],
                "standard": "能把复数、频率、极点和稳定性放到同一张概念图里。",
            },
        ],
    },
    {
        "dir": "02-解析函数与初等函数",
        "file": "📗 第二阶段：解析函数与初等函数.md",
        "emoji": "📗",
        "heading": "📗 第二阶段：解析函数与初等函数",
        "topic": "第二阶段：解析函数与初等函数",
        "difficulty": "intermediate",
        "duration": "3-4周",
        "concept": ["复导数", "Cauchy-Riemann条件", "解析函数", "共形映射"],
        "quote": "复可导比实可导严格得多；一旦处处复可导，函数会被迫拥有非常强的几何和分析结构。",
        "modules": [
            {
                "name": "复可导与解析性",
                "problem": "什么样的复函数真正可导，为什么解析性比逐点可导更重要？",
                "source": "MIT OCW 18.04：Topic 2 Analytic Functions；Brown & Churchill：Analytic Functions、Cauchy-Riemann Equations",
                "cards": ["复导数", "Cauchy-Riemann条件", "解析函数", "调和函数"],
                "standard": "能用 CR 条件判定基本函数的解析性，并说明解析函数和调和函数的关系。",
            },
            {
                "name": "初等解析函数",
                "problem": "指数、对数、三角函数进入复平面后会出现哪些新结构？",
                "source": "Brown & Churchill：Elementary Functions；Needham：The Exponential Function、The Logarithm Function",
                "cards": ["复指数函数", "复对数函数", "复三角函数"],
                "standard": "能解释复指数的周期性、复对数的多值性，以及复三角函数和指数函数的互化。",
            },
            {
                "name": "共形映射",
                "problem": "解析函数在局部为什么保角，分式线性变换为什么特别重要？",
                "source": "MIT OCW 18.04：Topic 10 Conformal Transformations；Needham：Transformations and Geometry",
                "cards": ["共形映射直觉", "Mobius变换", "圆线性质"],
                "standard": "能用一个网格或圆线例子说明共形映射如何保持局部角度。",
            },
            {
                "name": "判定与误区",
                "problem": "解析性题目最常见的判断链条和错误在哪里？",
                "source": "Brown & Churchill：Analytic Functions exercises；MIT OCW 18.04：Problem sets on analytic functions",
                "cards": ["解析函数判定题", "CR条件常见误区"],
                "standard": "能区分实可微、偏导存在、满足 CR 条件和真正解析之间的差别。",
            },
        ],
    },
    {
        "dir": "03-复积分与Cauchy理论",
        "file": "📙 第三阶段：复积分与Cauchy理论.md",
        "emoji": "📙",
        "heading": "📙 第三阶段：复积分与Cauchy理论",
        "topic": "第三阶段：复积分与Cauchy理论",
        "difficulty": "intermediate",
        "duration": "3-5周",
        "concept": ["复路径积分", "Cauchy积分定理", "Cauchy积分公式", "最大模原理"],
        "quote": "复积分真正神奇的地方在于：边界、路径和函数内部结构会被同一套 Cauchy 理论绑在一起。",
        "modules": [
            {
                "name": "复积分基础",
                "problem": "复路径积分如何定义，什么时候积分只和端点有关？",
                "source": "MIT OCW 18.04：Topic 3 Line Integrals and Cauchy's Theorem；Brown & Churchill：Integrals",
                "cards": ["复路径积分", "原函数与路径无关", "ML不等式"],
                "standard": "能参数化一条曲线并计算最小路径积分，知道 ML 不等式如何估计积分大小。",
            },
            {
                "name": "Cauchy理论核心",
                "problem": "为什么解析函数沿闭合曲线积分为零，函数值又能由边界积分恢复？",
                "source": "MIT OCW 18.04：Topic 3 Cauchy's Theorem、Topic 4 Cauchy's Integral Formula；Brown & Churchill：Cauchy-Goursat Theorem、Cauchy Integral Formula",
                "cards": ["Cauchy积分定理", "Cauchy积分公式", "高阶导数公式"],
                "standard": "能写出 Cauchy 积分公式并用它求函数值或导数。",
            },
            {
                "name": "解析函数的后果",
                "problem": "Cauchy理论会推出哪些看起来不像积分定理的强结论？",
                "source": "Brown & Churchill：Liouville's Theorem、Maximum Modulus Principle；MIT OCW 18.04：Consequences of Cauchy's formula",
                "cards": ["Liouville定理", "最大模原理", "Morera定理"],
                "standard": "能说明整函数有界为什么只能是常数，以及最大模原理的边界控制直觉。",
            },
            {
                "name": "边值与题型连接",
                "problem": "复积分理论如何进入调和函数、边值问题和围线积分题？",
                "source": "MIT OCW 18.04：Harmonic functions；Needham：Vector Fields、Physics and Topology",
                "cards": ["解析函数与调和函数边值", "围线积分题型"],
                "standard": "能把一个围线积分题拆成路径、解析区域、奇点和可用定理四个检查项。",
            },
        ],
    },
    {
        "dir": "04-级数奇点留数与应用",
        "file": "📕 第四阶段：级数奇点留数与应用.md",
        "emoji": "📕",
        "heading": "📕 第四阶段：级数奇点留数与应用",
        "topic": "第四阶段：级数奇点留数与应用",
        "difficulty": "advanced",
        "duration": "4-6周",
        "concept": ["Taylor展开", "Laurent展开", "奇点", "留数定理"],
        "quote": "留数把全局积分压缩成局部系数，是复变函数最适合做计算和应用的地方。",
        "modules": [
            {
                "name": "复级数与展开",
                "problem": "解析函数如何通过幂级数、Taylor展开和Laurent展开被局部刻画？",
                "source": "MIT OCW 18.04：Topic 7 Taylor and Laurent Series；Brown & Churchill：Series、Taylor Series、Laurent Series",
                "cards": ["幂级数", "Taylor展开", "Laurent展开"],
                "standard": "能围绕一个中心写出常见函数的 Taylor 或 Laurent 展开，并解释收敛区域。",
            },
            {
                "name": "奇点分类",
                "problem": "函数在坏点附近到底坏到什么程度，如何分类和处理？",
                "source": "Brown & Churchill：Singularities、Zeros and Poles；Needham：Polynomials and the Argument Principle",
                "cards": ["可去奇点", "极点", "本性奇点"],
                "standard": "能根据 Laurent 展开或极限行为区分可去奇点、极点和本性奇点。",
            },
            {
                "name": "留数计算",
                "problem": "留数如何把围线积分变成一个局部系数问题？",
                "source": "MIT OCW 18.04：Topic 8 Residue Theorem；Brown & Churchill：Residues and Poles、Residue Theorem",
                "cards": ["留数定义", "留数计算方法", "留数定理", "实积分的留数法"],
                "standard": "能选择合适方式计算留数，并用留数定理完成一个标准围线积分或实积分。",
            },
            {
                "name": "高阶应用连接",
                "problem": "级数、奇点和留数如何进入零点计数、渐近分析、信号与控制？",
                "source": "MIT OCW 18.04：Definite integrals using residues、Conformal transformations；Needham：Argument Principle、Rouche's Theorem",
                "cards": ["Argument Principle", "Rouche定理", "Laplace与Fourier反演中的复分析", "稳定性与极点"],
                "standard": "能说明零点极点计数、频域反演和系统稳定性为什么都依赖复平面的奇点结构。",
            },
        ],
    },
]


def yaml_list(items: list[str]) -> str:
    return "[" + ", ".join(f'"{item}"' for item in items) + "]"


def wikilinks(cards: list[str]) -> str:
    return "<br>".join(f"[[{card}]]" for card in cards)


def stage_page(stage: dict) -> str:
    table_rows = "\n".join(
        f"| {module['name']} | {module['problem']} | {module['source']} | {wikilinks(module['cards'])} | {module['standard']} |"
        for module in stage["modules"]
    )
    directory = stage["dir"]
    heading = stage["heading"]
    stage_num = STAGES.index(stage) + 1
    prev_link = ""
    next_link = ""
    if stage_num > 1:
        prev = STAGES[stage_num - 2]
        prev_link = f"- [[../{prev['dir']}/{prev['file'].removesuffix('.md')}|返回{prev['topic']}]]\n"
    if stage_num < len(STAGES):
        nxt = STAGES[stage_num]
        next_link = f"- [[../{nxt['dir']}/{nxt['file'].removesuffix('.md')}|进入{nxt['topic']}]]\n"
    return f"""---
type: stage
topic: "{stage['topic']}"
created: {TODAY}
status: planned
difficulty: {stage['difficulty']}
phase: {stage_num}
duration: "{stage['duration']}"
concept: {yaml_list(stage['concept'])}
prerequisites: []
related: ["数学分析", "信号与系统", "控制与机器人学"]
tags: ["复变函数", "教材主线", "阶段"]
---
# {heading}

> {stage['quote']}

## 📊 阶段进度

```dataviewjs
const notes = dv.pages('"02-Knowledge/🧠 学习系统/37-复变函数/{directory}"')
  .where(p => p.file.name !== "{stage['file'].removesuffix('.md')}");
const completed = notes.where(p => p.status === "completed").length;
const total = notes.length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**阶段进度: ${{progress}}%** (${{completed}}/${{total}} 个主题)`);
```

## 🧩 教材对齐索引

| 模块 | 要解决的问题 | 对应教材章节 | 原子卡片 | 完成标准 |
|:---|:---|:---|:---|:---|
{table_rows}

## ✅ 进入下一阶段前要满足

- [ ] 能把本阶段每个模块的核心问题用自己的话说清。
- [ ] 每个模块至少补一张原子卡的最小例子或代表题。
- [ ] 能说明本阶段和数学分析、信号与系统或控制路径的一个连接。

## 🔗 阶段导航

{prev_link}- [[../🗺️ 复变函数学习路径|返回复变函数总索引]]
- [[../📚 教材挂载索引|查看教材挂载索引]]
- [[../知识地图/🗺️ 横向知识地图|查看横向知识地图]]
{next_link}"""


def roadmap_page() -> str:
    stage_totals = "\n    + ".join(
        f'(dv.pages(\'"02-Knowledge/🧠 学习系统/37-复变函数/{stage["dir"]}"\').length - 1)' for stage in STAGES
    )
    stage_completed = "\n    + ".join(
        f'dv.pages(\'"02-Knowledge/🧠 学习系统/37-复变函数/{stage["dir"]}"\').where(p => p.status === "completed").length'
        for stage in STAGES
    )
    stage_rows = "\n".join(
        f"| {stage['emoji']} | **{stage['topic']}** | {stage['duration']} | {stage['quote']} | [[{stage['dir']}/{stage['file'].removesuffix('.md')}|进入]] |"
        for stage in STAGES
    )
    quick_links = "\n".join(
        f"- [[{stage['dir']}/{stage['file'].removesuffix('.md')}|{stage['heading']}]]" for stage in STAGES
    )
    return f"""---
type: index
topic: "复变函数学习路径"
created: 2026-05-08
updated: {TODAY}
status: active
tags: ["学习路径", "复变函数", "基础数学", "信号控制桥梁"]
description: "从复数几何直觉到解析函数、Cauchy理论、级数奇点留数与工程应用的复变函数路线图"
---
# 🗺️ 复变函数学习路径

> "复变函数不是把实函数多加一个 i，而是把几何、级数、积分和频域结构压进同一个平面。"

```dataviewjs
const total =
    {stage_totals};

const completed =
    {stage_completed};

const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**总体进度: ${{progress}}%** | 已完成: ${{completed}} / ${{total}} 主题`);
```

## 📚 主线定位

- 核心问题：把复数、解析性、复积分、级数展开和留数计算组织成一条可用于数学推导与工程频域分析的路径。
- 推荐前置：数学分析中的极限、连续、级数与多元微积分；线性代数中的平面变换直觉。
- 学完后可继续：信号与系统、控制与机器人学、偏微分方程、渐近分析与概率中的复分析工具。
- 教材入口：[[02-Knowledge/🧠 学习系统/37-复变函数/📚 教材挂载索引|进入教材挂载索引]]

## 🧭 四阶段主线

| 阶段 | 名称 | 周期 | 本阶段主问题 | 入口 |
|:---:|:---|:---:|:---|:---|
{stage_rows}

## 🎯 阶段产出

| 阶段 | 学完这一段你应该能做到什么 |
|:---:|:---|
| 📘 | 能把复数的代数形式、极形式和几何变换联系起来。 |
| 📗 | 能用 Cauchy-Riemann 条件和解析性判断基本复函数。 |
| 📙 | 能计算基础复路径积分，并使用 Cauchy 积分公式解决函数值与导数问题。 |
| 📕 | 能分类奇点、计算留数，并把留数定理用于围线积分和工程频域问题。 |

## 🚦 推荐推进顺序

1. 先学 `📘 复数与复函数直觉`，把复数乘法、平面映射和多值分支看明白。
2. 再学 `📗 解析函数与初等函数`，理解复可导为何会带来极强结构。
3. 接着学 `📙 复积分与Cauchy理论`，掌握 Cauchy 积分定理和积分公式。
4. 最后学 `📕 级数奇点留数与应用`，把 Taylor/Laurent 展开、留数和频域应用接起来。

## 🔗 交叉连接

| 路径 | 连接方式 |
|:---|:---|
| [[02-Knowledge/🧠 学习系统/28-数学分析/🗺️ 数学分析学习路径|数学分析]] | 提供极限、连续、级数和积分的前置语言。 |
| [[02-Knowledge/🧠 学习系统/12-信号与系统/🗺️ 信号与系统学习路径|信号与系统]] | Laplace/Fourier 变换、极点和反演公式都需要复平面直觉。 |
| [[02-Knowledge/🧠 学习系统/15-控制与机器人学/🗺️ 控制与机器人学学习路径|控制与机器人学]] | 传递函数、极点零点和稳定性分析依赖复变量表示。 |
| [[02-Knowledge/🧠 学习系统/34-偏微分方程/🗺️ 偏微分方程学习路径|偏微分方程]] | 调和函数、边值问题和解析函数有天然连接。 |

## 🔎 快速导航

{quick_links}
- [[知识地图/🗺️ 横向知识地图|🗺️ 横向知识地图]]
- [[📚 教材挂载索引|📚 教材挂载索引]]
- [[00-计划占位/占位-课程任务挂载|课程任务挂载]]
- [[00-计划占位/占位-错题整理|错题整理]]
- [[🏠 主页|返回主页]]

*路线图更新：{TODAY}*
"""


def textbook_index() -> str:
    return f"""---
type: index
topic: "复变函数教材挂载索引"
created: 2026-05-08
updated: {TODAY}
status: active
tags: ["教材", "索引", "复变函数"]
---
# 📚 复变函数教材挂载索引

> 本页把复变函数的教材顺序挂到 `37-复变函数` 路径。当前本地书库尚未发现正式复变 PDF，因此先采用经典教材/公开课程的章节顺序作为索引，后续下载教材后再把条目替换为书库链接。

## 推荐教材与课程

| 资源 | 状态 | 负责解决什么 | 优先看什么 | 对应阶段 |
|:---|:---:|:---|:---|:---|
| Brown & Churchill, Complex Variables and Applications | 待接入书库 | 工程应用友好的标准复变函数主教材 | Complex Numbers、Analytic Functions、Elementary Functions、Integrals、Series、Residues and Poles | [[01-复数与复函数直觉/📘 第一阶段：复数与复函数直觉|第一阶段]] + [[02-解析函数与初等函数/📗 第二阶段：解析函数与初等函数|第二阶段]] + [[03-复积分与Cauchy理论/📙 第三阶段：复积分与Cauchy理论|第三阶段]] + [[04-级数奇点留数与应用/📕 第四阶段：级数奇点留数与应用|第四阶段]] |
| MIT OCW 18.04 Complex Variables with Applications | 在线课程 | 一学期复变函数课程节奏和题型主线 | Analytic Functions、Cauchy's Theorem、Cauchy's Formula、Taylor/Laurent Series、Residue Theorem、Conformal Transformations | [[02-解析函数与初等函数/📗 第二阶段：解析函数与初等函数|第二阶段]] + [[03-复积分与Cauchy理论/📙 第三阶段：复积分与Cauchy理论|第三阶段]] + [[04-级数奇点留数与应用/📕 第四阶段：级数奇点留数与应用|第四阶段]] |
| Tristan Needham, Visual Complex Analysis | 待接入书库 | 建立几何直觉和映射视角 | Euler's Formula、Complex Functions as Transformations、Multifunctions、Cauchy's Theorem、Residues | [[01-复数与复函数直觉/📘 第一阶段：复数与复函数直觉|第一阶段]] + [[02-解析函数与初等函数/📗 第二阶段：解析函数与初等函数|第二阶段]] + [[04-级数奇点留数与应用/📕 第四阶段：级数奇点留数与应用|第四阶段]] |
| Saff & Snider, Fundamentals of Complex Analysis with Applications | 可选替代 | 更偏工程、科学和应用数学的复分析入门 | Analytic Functions、Complex Integration、Residues、Applications | [[03-复积分与Cauchy理论/📙 第三阶段：复积分与Cauchy理论|第三阶段]] + [[04-级数奇点留数与应用/📕 第四阶段：级数奇点留数与应用|第四阶段]] |

## 阶段阅读顺序

| 阶段 | 核心问题 | 教材抓手 | 当前入口 |
|:---|:---|:---|:---|
| 复数与复函数直觉 | 复数为什么能表示旋转、振荡和频域结构？ | Complex Numbers、Euler's Formula、Complex Functions as Transformations | [[01-复数与复函数直觉/📘 第一阶段：复数与复函数直觉|第一阶段]] |
| 解析函数与初等函数 | 什么样的复函数可导且结构足够强？ | Analytic Functions、Cauchy-Riemann Equations、Elementary Functions、Conformal Mapping | [[02-解析函数与初等函数/📗 第二阶段：解析函数与初等函数|第二阶段]] |
| 复积分与 Cauchy 理论 | Cauchy 理论为什么能把局部解析性和边界积分联系起来？ | Line Integrals、Cauchy's Theorem、Cauchy's Integral Formula、Maximum Modulus Principle | [[03-复积分与Cauchy理论/📙 第三阶段：复积分与Cauchy理论|第三阶段]] |
| 级数、奇点、留数与应用 | 留数如何把复杂积分变成局部系数问题？ | Taylor Series、Laurent Series、Residues and Poles、Residue Theorem、Argument Principle | [[04-级数奇点留数与应用/📕 第四阶段：级数奇点留数与应用|第四阶段]] |

## 横向连接

- [[02-Knowledge/🧠 学习系统/28-数学分析/🗺️ 数学分析学习路径|数学分析]]：极限、级数、积分的前置直觉。
- [[02-Knowledge/🧠 学习系统/12-信号与系统/🗺️ 信号与系统学习路径|信号与系统]]：拉普拉斯变换、频域、系统函数。
- [[02-Knowledge/🧠 学习系统/15-控制与机器人学/🗺️ 控制与机器人学学习路径|控制与机器人学]]：极点、稳定性、传递函数。
- [[02-Knowledge/🧠 学习系统/34-偏微分方程/🗺️ 偏微分方程学习路径|偏微分方程]]：调和函数与边值问题。

## 维护项

- [ ] 下载或挂载一本正式主教材 PDF。
- [ ] 根据实际课程作业补充题型卡和错题卡。
- [ ] 后续把信号、控制中的 Laplace/Fourier 主题回链到第四阶段。

## 导航

- [[🗺️ 复变函数学习路径]]
- [[知识地图/🗺️ 横向知识地图]]
- [[02-Knowledge/🧠 学习系统/📚 教材挂载总索引|教材挂载总索引]]
- [[02-Knowledge/🧠 学习系统/🎓 学习入口|学习入口]]
"""


def knowledge_map() -> str:
    return f"""---
type: index
topic: "复变函数横向知识地图"
created: {TODAY}
status: active
tags: ["复变函数", "知识地图", "索引"]
---
# 🗺️ 复变函数横向知识地图

> 横向地图用于查漏补缺：当你在信号、控制、数学分析或概率里遇到复平面问题时，可以按问题类型反查复变函数主线。

## 五条横向主线

| 主线 | 解决的问题 | 关键卡片 | 关联阶段 |
|:---|:---|:---|:---|
| 复平面几何 | 复数如何表达旋转、缩放、区域和曲线？ | [[复平面与模辐角]]、[[极形式与Euler公式]]、[[复函数作为平面映射]] | [[../01-复数与复函数直觉/📘 第一阶段：复数与复函数直觉|第一阶段]] |
| 解析性 | 什么函数具有强到足以推出积分、级数和几何性质的结构？ | [[复导数]]、[[Cauchy-Riemann条件]]、[[解析函数]]、[[调和函数]] | [[../02-解析函数与初等函数/📗 第二阶段：解析函数与初等函数|第二阶段]] |
| Cauchy理论 | 边界积分如何恢复函数值、导数和整体结构？ | [[复路径积分]]、[[Cauchy积分定理]]、[[Cauchy积分公式]]、[[最大模原理]] | [[../03-复积分与Cauchy理论/📙 第三阶段：复积分与Cauchy理论|第三阶段]] |
| 奇点与留数 | 函数在坏点附近的局部行为如何决定积分结果？ | [[Laurent展开]]、[[极点]]、[[留数定义]]、[[留数定理]] | [[../04-级数奇点留数与应用/📕 第四阶段：级数奇点留数与应用|第四阶段]] |
| 应用连接 | 复分析如何进入频域、稳定性和反演计算？ | [[复变函数与傅里叶直觉]]、[[复变函数与控制极点]]、[[Laplace与Fourier反演中的复分析]]、[[稳定性与极点]] | 第一阶段、第四阶段 |

## 题型入口

| 题型 | 先检查什么 | 常用卡片 |
|:---|:---|:---|
| 解析性判定 | 定义域、偏导连续、CR 条件、是否整个邻域成立 | [[解析函数判定题]]、[[CR条件常见误区]] |
| 路径积分 | 路径参数化、是否有原函数、区域是否单连通、奇点是否被包围 | [[复路径积分]]、[[原函数与路径无关]]、[[Cauchy积分定理]] |
| Cauchy公式 | 被积函数是否能改写为 f(z)/(z-a)，a 是否在围线内 | [[Cauchy积分公式]]、[[高阶导数公式]] |
| 留数计算 | 奇点类型、极点阶数、是否适合展开或极限公式 | [[留数计算方法]]、[[留数定理]] |
| 实积分转围线 | 积分区间、衰减条件、选上半圆还是钥匙孔围线 | [[实积分的留数法]]、[[围线积分题型]] |

## 跨路径回链

- [[02-Knowledge/🧠 学习系统/12-信号与系统/04-变换篇-拉普拉斯/🌊 第四阶段：拉普拉斯变换|信号与系统：拉普拉斯变换]]：重点回查 [[稳定性与极点]] 和 [[Laplace与Fourier反演中的复分析]]。
- [[02-Knowledge/🧠 学习系统/15-控制与机器人学/🗺️ 控制与机器人学学习路径|控制与机器人学]]：传递函数、根轨迹和稳定性判断回查 [[复变函数与控制极点]]。
- [[02-Knowledge/🧠 学习系统/28-数学分析/02-级数理论/📗 第二阶段：级数理论|数学分析：级数理论]]：幂级数和函数项级数回查 [[幂级数]]、[[Taylor展开]]。
- [[02-Knowledge/🧠 学习系统/34-偏微分方程/🗺️ 偏微分方程学习路径|偏微分方程]]：调和函数与边值问题回查 [[解析函数与调和函数边值]]。

## 导航

- [[../🗺️ 复变函数学习路径|复变函数学习路径]]
- [[../📚 教材挂载索引|教材挂载索引]]
- [[../01-复数与复函数直觉/📘 第一阶段：复数与复函数直觉|第一阶段]]
- [[../02-解析函数与初等函数/📗 第二阶段：解析函数与初等函数|第二阶段]]
- [[../03-复积分与Cauchy理论/📙 第三阶段：复积分与Cauchy理论|第三阶段]]
- [[../04-级数奇点留数与应用/📕 第四阶段：级数奇点留数与应用|第四阶段]]
"""


def placeholder(title: str, target: str, note: str) -> str:
    return f"""---
type: study
topic: "{title}"
created: 2026-05-08
updated: {TODAY}
status: planned
difficulty: beginner
domain: "复变函数"
concept: ["{title}"]
prerequisites: []
related: ["37-复变函数/🗺️ 复变函数学习路径"]
tags: ["学习", "占位", "计划挂载", "复变函数"]
---

# {title}

## 正式入口

- {target}

## 用途

{note}

## 关联日计划

- 待自动挂载
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def create_stage_files() -> None:
    for stage in STAGES:
        write(ROOT / stage["dir"] / stage["file"], stage_page(stage))


def create_cards_from_stage_specs() -> None:
    sys.path.insert(0, str(Path("tools").resolve()))
    import repair_learning_system_indexes as repair

    course = repair.build_course(ROOT)
    for stage in course.stages:
        for card in stage.cards:
            path = stage.file.parent / f"{card.title}.md"
            if path.exists():
                existing = path.read_text(encoding="utf-8")
            else:
                existing = ""
            body = repair.make_card_body(card, course, existing)
            write(path, body)


def main() -> int:
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "知识地图").mkdir(parents=True, exist_ok=True)

    create_stage_files()
    write(ROOT / "🗺️ 复变函数学习路径.md", roadmap_page())
    write(ROOT / "📚 教材挂载索引.md", textbook_index())
    write(ROOT / "知识地图" / "🗺️ 横向知识地图.md", knowledge_map())

    write(
        ROOT / "00-计划占位" / "占位-解析函数.md",
        placeholder("解析函数", "[[../02-解析函数与初等函数/解析函数|解析函数]]", "本卡保留给日计划挂载；正式学习内容已迁移到第二阶段主题卡。"),
    )
    write(
        ROOT / "00-计划占位" / "占位-积分公式.md",
        placeholder("积分公式", "[[../03-复积分与Cauchy理论/Cauchy积分公式|Cauchy积分公式]]", "本卡保留给日计划挂载；正式学习内容已迁移到第三阶段主题卡。"),
    )
    write(
        ROOT / "00-计划占位" / "占位-留数.md",
        placeholder("留数", "[[../04-级数奇点留数与应用/留数定义|留数定义]]", "本卡保留给日计划挂载；正式学习内容已迁移到第四阶段主题卡。"),
    )
    write(
        ROOT / "00-计划占位" / "占位-课程任务挂载.md",
        placeholder("课程任务挂载", "[[../🗺️ 复变函数学习路径|复变函数学习路径]]", "用于把日计划、作业、课程任务回挂到正式四阶段学习路径。"),
    )
    write(
        ROOT / "00-计划占位" / "占位-错题整理.md",
        placeholder("错题整理", "[[../知识地图/🗺️ 横向知识地图#题型入口|题型入口]]", "用于集中挂载解析性判定、路径积分、Cauchy公式和留数计算等错题。"),
    )

    create_cards_from_stage_specs()
    print("created complex analysis path")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
