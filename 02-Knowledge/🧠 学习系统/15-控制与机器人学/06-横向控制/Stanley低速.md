---
type: study
topic: "Stanley低速"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段6-横向控制]]"
flow: knowledge
kind: concept
concept: ["Stanley", "低速", "除零处理"]
prerequisites: ["Stanley公式"]
related: ["Stanley公式", "Stanley高速"]
upstream: ["[[Stanley公式]]"]
source: "Stanford Stanley (2006); PythonRobotics"
tags: [学习, 控制与机器人学, 横向控制]
---

# Stanley低速

## 0. 为什么学它

Stanley 公式含 $e_y/v$，**低速/静止时除零**会让转角爆炸。**低速工况处理**是 Stanley 工程化的必修课：限速下限、平滑转角，同时理解低速下"几何法最准"的特性。

## 1. 核心问题与处理

**问题**：$\arctan(k e_y/v)$ 在 $v\to0$ 时趋于 $\pm90°$（无论偏差多小）→ 转角剧烈抖动。

**处理**：
1. **速度下限**：$v=\max(v,\ v_{min})$（如 0.1 m/s）；
2. **转角限幅**：$|\delta|\le\delta_{max}$；
3. **低速改用位置反馈**：低速时 $\arctan$ 项主导（几何法优势区）。

**低速特性**：$v$ 小 → $\arctan(k e_y/v)$ 大 → 强纠偏；无侧偏假设成立 → 几何法在低速最准。

## 2. 最小可手算例子（概念验证）

**题目**：$k=1,\ e_y=0.01,\ v=0.001$，未处理与限速后对比。

**解**：未处理：$\arctan(0.01/0.001)=\arctan10=84.3°$（几乎满转）；限速 $v_{min}=0.1$：$\arctan(0.01/0.1)=5.7°$（合理）✓。

**易错点**：只限幅不保底速度；低速转向饱和导致停摆。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 低速 Stanley 自动工作 | 需速度下限/限幅 |
| 低速转角大就是好 | 过大抖动，需平滑 |
| 低速也用高速参数 | $k$ 或限幅应按速度调整 |

## 4. 与后续知识连接

- [[Stanley公式]]：主律；
- [[Stanley高速]]：对照；
- [[Stanley调参]]：参数匹配。

## 5. 检索练习（闭卷）

1. 解释低速除零问题；
2. 给出三种处理；
3. 说明低速几何法优势；
4. 低速参数注意点。

## 6. 通过标准

- 能处理低速除零；
- 能限幅平滑；
- 能理解低速特性。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重做处理；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
