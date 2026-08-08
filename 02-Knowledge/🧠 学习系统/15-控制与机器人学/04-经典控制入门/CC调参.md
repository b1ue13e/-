---
type: study
topic: "CC调参"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段4-经典控制入门]]"
flow: knowledge
kind: problem-type
concept: ["CC调参", "计算机辅助整定", "仿真整定"]
prerequisites: ["PID公式", "试凑法"]
related: ["ZN调参", "Lambda整定", "主导极点"]
upstream: ["[[PID公式]]"]
source: "Python Control / MATLAB 整定工具实践"
tags: [学习, 控制与机器人学, PID]
---

# CC调参

## 0. 为什么学它

模型已知时，与其手动画图试凑，不如用**计算机辅助（CC，computer-aided）整定**：基于传递函数自动计算 PID 参数（极点配置、最优控制、自动扫参）。它是仿真与实车调参的加速器。

## 1. 核心方法

**方法 1：极点配置（主导极点法）**。指定期望闭环极点（由 $\zeta,\omega_n$ 确定），解出满足主导极点位置的 PID 参数——把设计指标直接变成代数方程。

**方法 2：数值优化扫参**。在仿真中自动扫描参数网格/梯度优化，最小化目标（如 ITAE 指标 $\int t|e|dt$）。

**方法 3：经验公式程序化**。ZN/Lambda 公式写进脚本，一键生成初始值。

**工具**：`python-control`（`control.tf`/`margin`/`rlocus`）、MATLAB `pidtune`、Simulink。

## 2. 最小可手算例子（主导极点法思路）

**题目**：对象 $G=\frac{1}{s(s+4)}$，要求 $\zeta=0.7,\omega_n=2$，设计 PD。

**解**：期望闭环 $s^2+2\zeta\omega_n s+\omega_n^2=s^2+2.8s+4$。PD 控制器 $K_p+K_ds$ 使 $1+CG=0$ 的闭环与期望匹配：特征方程 $s^2+(4+K_d)s+K_p=0$，对比系数：$K_d=-1.2$（负，说明 PD 不够，需 PID 或超前补偿）——计算机辅助可继续自动求解，这里揭示"对比系数"的代数方法。

**易错点**：主导极点近似要求其余极点足够远；参数可能为负（需换控制器结构）。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| CC 参数直接实车可用 | 需仿真验证 + 鲁棒性检查 |
| 忽略模型误差 | 模型不准则参数要留裕度 |
| 自动化取代理解 | 需理解算法原理才能判断结果合理性 |

## 4. 与后续知识连接

- [[主导极点]]：方法 1 依据；
- [[ZN调参]]、[[Lambda整定]]：初值来源；
- [[试凑法]]：仿真后的微调；
- [[根轨迹]]、[[Bode图]]：可视化校验。

## 5. 检索练习（闭卷）

1. 说出 CC 整定的三种方法；
2. 用对比系数法设计 PD；
3. 说明主导极点近似条件；
4. CC 与手动整定的关系。

## 6. 通过标准

- 能执行一种 CC 方法；
- 能校验结果；
- 能理解主导极点假设。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重做设计题；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
