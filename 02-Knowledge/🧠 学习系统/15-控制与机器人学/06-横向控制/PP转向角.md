---
type: study
topic: "PP转向角"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段6-横向控制]]"
flow: knowledge
kind: derivation
concept: ["Pure Pursuit", "转向角", "控制律"]
prerequisites: ["PP曲率", "自行车模型"]
related: ["PP算法", "PP曲率"]
upstream: ["[[06-横向控制/PP曲率]]"]
source: "Pure Pursuit 文献; PythonRobotics"
tags: [学习, 控制与机器人学, 横向控制]
---

# PP转向角

## 0. 为什么学它

PP 的最终输出是**转向角 $\delta$**——由曲率经自行车运动学反解。本卡给出完整控制律与符号处理，是 PP 代码实现的最后一步。

## 1. 核心公式

**PP 转向角控制律**：

$$\delta=\arctan\left(\frac{2L\sin\alpha}{l_d}\right).$$

**推导**：$\kappa=\frac{2\sin\alpha}{l_d}$，$\delta=\arctan(\kappa L)$（自行车模型）。

**符号约定**：$\alpha>0$（前视点在车辆左侧）→ $\delta>0$（左转）；实现时用 $\text{atan2}$ 处理象限。

## 2. 最小可手算例子

**题目**：$L=2.5,\ l_d=6,\ \alpha=15°$，求 $\delta$。

**解**：$\delta=\arctan\left(\frac{2\times2.5\times\sin15°}{6}\right)=\arctan\left(\frac{5\times0.259}{6}\right)=\arctan(0.216)=12.2°$。

**易错点**：角度/弧度；$\sin\alpha$ 的符号随左右；执行器限幅（$|\delta|\le\delta_{max}$）。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| $\delta$ 与 $\alpha$ 线性 | $\arctan$ 非线性，大角饱和 |
| 忽略限幅 | 执行器有转角上限 |
| 符号处理粗糙 | 用 atan2 + 统一约定 |

## 4. 与后续知识连接

- [[PP算法]]：主流程；
- [[PP曲率]]：中间量；
- [[PP稳定性]]：增益影响。

## 5. 检索练习（闭卷）

1. 写出 PP 控制律；
2. 计算转向角；
3. 说明符号与限幅；
4. 与曲率关系。

## 6. 通过标准

- 能实现转向角计算；
- 能处理符号限幅；
- 能理解非线性。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重算转角；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
