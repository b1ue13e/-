---
type: study
topic: "Frenet曲率"
course: "控制与机器人学"
created: 2026-08-07
updated: 2026-08-08
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段8-轨迹与路径跟踪]]"
flow: knowledge
kind: concept
concept: ["曲率传递", "横向导数", "合成曲率"]
prerequisites: ["Frenet转换"]
related: ["曲率约束", "Frenet横向", "轨迹可行性"]
upstream: ["[[Frenet转换]]"]
source: "Werling et al. Frenet 框架论文；PythonRobotics（MIT）"
tags: [学习, 控制与机器人学, Frenet]
---

# Frenet曲率

> **一句话**：车辆实际行驶轨迹的曲率 = 参考线曲率 + 横向运动的贡献——在 Frenet 系里精确表达横向运动对转向的影响。

## 0. 为什么学它

横向规划输出的是 $d(s)$ 曲线，但执行器（转向角）消费的是**曲率**。合成曲率公式把 $d(s)$ 变成可执行的转向指令，也是可行性检查（$|\kappa| \le \kappa_{max}$）的依据——不掌握它，换道轨迹"画得出来"但"转不过来"。

## 1. 轨迹曲率公式

车辆轨迹曲率 $\kappa$（由 $d(s)$ 及其导数表达）：

$$\kappa(s) = \frac{\kappa_r(s) + \frac{d''(s)}{(1 - \kappa_r d)^2}}{\sqrt{1 + (d'(s)/\dot{s})^2}}$$

常见简化（横向速度小、$\kappa_r d \ll 1$）：

$$\kappa \approx \kappa_r + d''$$

**直觉：横向加速度由 $d''$ 提供，换道轨迹的曲率 = 参考线曲率 + 自身横向弯曲**。

## 2. 曲率受限速度

转向角上限 $\delta_{max}$ → 曲率上限 $\kappa_{max} = \tan\delta_{max}/L$ → 速度上限：

$$v_{max}(s) = \sqrt{\frac{a_{lat,max}}{\kappa(s)}}$$

## 3. 最小可手算例子（简化曲率）

**题目**：参考线为 x 轴（$\kappa_r = 0$），换道轨迹 $d(s) = \tfrac{1}{20}(s-10)^2$（抛物线），求 $s=10$ 处合成曲率（简化式）。

**步骤**：
1. $d'(s) = \tfrac{1}{10}(s-10)$，$d''(s) = \tfrac{1}{10}$；
2. 简化式 $\kappa \approx \kappa_r + d'' = 0 + 0.1 = 0.1\ \text{m}^{-1}$；
3. 含义：该点曲率半径 10 m——若转向角上限对应 $\kappa_{max} = 0.08$，则此轨迹不可行，需增大换道纵向跨度（减小 $d''$）。

**易错点**：用简化式前必须确认 $\kappa_r d \ll 1$ 与横向速度小；急弯+大偏移场景要用完整公式。

## 4. Frenet 中曲率的影响

| 影响 | 说明 |
|:---|:---|
| 坐标转换 | 参考线曲率进入 $\dot{s}$ 分解（见[[Frenet转换]]） |
| 可行性 | 横向多项式生成的 $d(s)$ 可能使 $\kappa$ 超限 |
| 限速 | 弯道按 $\kappa(s)$ 限速 |
| 奇异性 | $1-\kappa_r d \to 0$ 时公式失效 |

## 5. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 曲率只看参考线 | 合成曲率含横向贡献 $d''$，换道时横向项可能主导 |
| 无条件用简化式 | 高速/大偏移/急弯必须用完整公式 |
| 忽略转向角上限 | 曲率必须换算回转向角 $\delta = \arctan(L\kappa)$ 检查 |

## 6. 工程要点

- 换道轨迹验证必须检查合成曲率 $\kappa(s) \le \kappa_{max}$（见[[轨迹可行性]]）；
- 高速换道：横向加速度约束自动限制换道速度；
- 曲率突变点（参考线急弯）要降低纵向速度。

## 7. 检索练习（闭卷）

1. 写出合成曲率公式与简化条件；
2. 手算：$\kappa_r=0,\ d''=0.1$ 的 $\kappa$ 与曲率半径；
3. 说明曲率 → 转向角的换算。

## 8. 通过标准

- 能写出并解释合成曲率公式；
- 能判断简化式适用条件；
- 能完成曲率 → 转向角 → 限速链路。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；下次复习：重做一次曲率手算。
