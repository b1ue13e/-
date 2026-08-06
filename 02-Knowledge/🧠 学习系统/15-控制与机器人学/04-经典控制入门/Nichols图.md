---
type: study
topic: "Nichols图"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段4-经典控制入门]]"
flow: knowledge
kind: concept
concept: ["Nichols图", "幅相图", "频域分析"]
prerequisites: ["Bode图", "稳定裕度"]
related: ["Bode图", "Nyquist图", "稳定裕度"]
upstream: ["[[04-经典控制入门/Bode图]]"]
source: "Modern Control Engineering (Ogata) Ch.7"
tags: [学习, 控制与机器人学, 频域分析]
---

# Nichols图

## 0. 为什么学它

**Nichols 图**用"相位（横轴）× 幅值（纵轴，dB）"画开环频率响应，叠加等幅值/等相位（M/N）曲线，直接读出闭环幅值、带宽与稳定裕度——是频域设计查图工具，在 MATLAB 等工具中常用于闭环整形。

## 1. 核心概念

**Nichols 图**：横轴相位（°）、纵轴幅值（dB），曲线为 $G(j\omega)$ 轨迹。

**M/N 曲线**（Nichols 网格）：绘制"闭环幅值 = 常数（M 曲线）"与"闭环相位 = 常数（N 曲线）"的等值线。开环曲线与 M 曲线相切处 → 闭环谐振峰 $M_r$。

**关键读数**：
- 曲线与 0dB、−180° 交点 → PM/GM（同 Bode）；
- 与 M 网格相切 → 闭环谐振峰 $M_r$（与超调相关）；
- 曲线进入 $M=+\infty$ 点附近 → 不稳定。

## 2. 最小可手算例子（概念验证）

**题目**：开环曲线与 $M=1.3$（2.3dB）曲线相切，说明什么？

**解**：闭环谐振峰 $M_r=1.3$ → 对应欠阻尼（$\zeta\approx\frac{1}{M_r+\sqrt{M_r^2-1}}\approx0.43$）→ 阶跃超调约 20%。相切越深（M 越大）阻尼越低。

**易错点**：M 曲线是闭环量（与开环曲线不同坐标系）；相切而非交点。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| Nichols 图是开环图 | 但 M/N 网格读的是闭环量 |
| 交点=谐振峰 | 谐振峰是**相切**处 |
| 与 Bode 完全重复 | Nichols 更便于闭环整形设计 |

## 4. 与后续知识连接

- [[Bode图]]、[[Nyquist图]]：等价表示；
- [[稳定裕度]]：读数一致；
- 工程：MATLAB Nichols 工具。

## 5. 检索练习（闭卷）

1. 说明 Nichols 图坐标；
2. 解释 M/N 曲线作用；
3. 如何读 $M_r$ 与超调；
4. 与 Bode 的互补。

## 6. 通过标准

- 能读 Nichols 图；
- 能理解 M/N 网格；
- 能关联 $M_r$ 与阻尼。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重读图；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
