---
type: study
topic: "Stanley调参"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段6-横向控制]]"
flow: knowledge
kind: problem-type
concept: ["Stanley", "调参", "增益"]
prerequisites: ["Stanley公式"]
related: ["Stanley公式", "Stanley低速", "Stanley高速"]
upstream: ["[[Stanley公式]]"]
source: "Stanford Stanley (2006); PythonRobotics"
tags: [学习, 控制与机器人学, 横向控制]
---

# Stanley调参

## 0. 为什么学它

Stanley 的主要参数是**横向增益 $k$**（及前馈/符号约定）。**Stanley 调参**说明 $k$ 对收敛速度与稳定性的影响，并给出系统化整定流程——"调一个旋钮就能得到想要的跟踪手感"。

## 1. 核心参数与影响

**控制律**：$\delta=\psi+\arctan(k e_y/v)$。

**增益 $k$ 的影响**：
- $k$ 大：横向收敛快，但**易振荡**（偏差大时转角大）；
- $k$ 小：平滑稳定，但收敛慢、弯道误差大；
- $k$ 通常随速度调整（$k$ 与 $v$ 的比值决定偏差项强度）。

**整定流程**：
1. 固定 $v$，从较小 $k$ 开始；
2. 增大 $k$ 至误差快速收敛且无振荡；
3. 弯道测试：过大 $k$ 或缺少前馈则弯道偏差大 → 加 [[Stanley前馈]]；
4. 多速度测试：必要时 $k$ 随 $v$ 调度。

## 2. 最小可手算例子（决策练习）

**题目**：低速测试振荡明显，如何调 $k$？

**解**：降低 $k$（偏差项增益），若仍要快收敛则同时考虑加前馈（把曲率工作交给前馈，反馈专注纠偏）→ 振荡通常缓解。

**易错点**：只调 $k$ 不配合前馈/速度匹配；忽略 $v$ 变化时 $k/v$ 比。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| $k$ 越大跟踪越准 | 过大振荡，收敛与稳定权衡 |
| $k$ 与速度无关 | $k/v$ 决定偏差项强度 |
| 不测弯道 | 弯道是 $k$ 与前馈的试金石 |

## 4. 与后续知识连接

- [[Stanley公式]]：主律；
- [[Stanley前馈]]：弯道补强；
- [[Stanley低速]]、[[Stanley高速]]：工况。

## 5. 检索练习（闭卷）

1. 说明 $k$ 的影响；
2. 给出整定流程；
3. 振荡时如何调；
4. 弯道误差如何处理。

## 6. 通过标准

- 能整定 Stanley；
- 能处理振荡/弯道；
- 能配合前馈。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重调参数；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
