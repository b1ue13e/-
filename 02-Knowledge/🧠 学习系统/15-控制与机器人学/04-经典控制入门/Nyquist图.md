---
type: study
topic: "Nyquist图"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段4-经典控制入门]]"
flow: knowledge
kind: concept
concept: ["Nyquist图", "极坐标图", "频域分析"]
prerequisites: ["频率响应", "Bode图"]
related: ["Nyquist判据", "稳定裕度", "相位裕度"]
upstream: ["[[Bode图]]"]
source: "Modern Control Engineering (Ogata) Ch.7"
tags: [学习, 控制与机器人学, 频域分析]
---

# Nyquist图

## 0. 为什么学它

**Nyquist 图**把 $G(j\omega)$ 画在复平面（实部-虚部），$\omega$ 从 0 到 ∞ 扫出一条曲线。它比 Bode 更紧凑地呈现增益/相位信息，并直接服务 **Nyquist 判据**（频域稳定性判定）与稳定裕度测量。

## 1. 核心概念

**Nyquist 图**：$G(j\omega)$ 在复平面的轨迹（$\omega:0\to\infty$），每点坐标 $(\text{Re}G,\ \text{Im}G)$。

**关键特征**：
- $\omega=0$：起点（$G(0)$，实轴上）；
- $\omega=\omega_c$：穿越单位圆（$|G|=1$）→ 幅值裕度关键点；
- $\omega\to\infty$：终点（通常趋于原点或常数）；
- 与负实轴交点：相位 −180° → 相位裕度关键点。

**与 Bode 的关系**：Bode 的幅相信息 = Nyquist 曲线（对数 vs 线性、极坐标 vs 直角）。

## 2. 最小可手算例子

**题目**：$G(s)=\dfrac{1}{s+1}$ 的 Nyquist 图。

**解**：$G(j\omega)=\frac{1}{1+j\omega}$。$\omega=0$：$(1,0)$；$\omega=1$：$\frac{1-j}{2}=(0.5,-0.5)$；$\omega\to\infty$：$(0,0)$。曲线为半圆（实部 +1 到 0），位于右半复平面 ✓。

**易错点**：ω 方向（0→∞）；实虚部计算；与负实轴交点识别。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| Nyquist 图只有一半 | 严格判据需含 $\omega\in(-\infty,∞)$ 与围线 |
| 与 Bode 信息不同 | 同一信息的两种表示 |
| 交点识别错误 | 与负实轴交点（相位 −180°）是裕度关键 |

## 4. 与后续知识连接

- [[Nyquist判据]]：稳定性判定；
- [[稳定裕度]]：幅值/相位裕度；
- [[Bode图]]：另一表示；
- [[Nichols图]]：幅相图。

## 5. 检索练习（闭卷）

1. 画 $G=\frac{1}{s+1}$ 的 Nyquist 图；
2. 指出穿越单位圆与负实轴的点；
3. 说明与 Bode 的关系；
4. 为何判据需完整围线。

## 6. 通过标准

- 能画简单系统的 Nyquist 图；
- 能识别关键点；
- 能理解与 Bode 的等价。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重画曲线；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
