---
type: study
topic: "Bode图"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段4-经典控制入门]]"
flow: knowledge
kind: concept
concept: ["Bode图", "频域分析", "对数坐标"]
prerequisites: ["频率响应", "典型环节"]
related: ["Nyquist图", "稳定裕度", "相位裕度"]
upstream: ["[[04-经典控制入门/频率响应]]"]
source: "Modern Control Engineering (Ogata) Ch.7"
tags: [学习, 控制与机器人学, 频域分析]
---

# Bode图

## 0. 为什么学它

**Bode 图**把频率响应画成两幅对数图：幅频（dB）与相频（度），横轴对数频率。它最强大之处是**叠加性**——复杂系统的 Bode 图 = 各典型环节图的叠加，配合渐近线可手绘草图，直观读出带宽、谐振与稳定性信息。

## 1. 核心绘制规则（渐近线）

1. **把 $G$ 分解为典型环节**（比例、积分、一阶惯性、二阶）；
2. **幅频**：各环节斜率叠加——积分 −20dB/dec、惯性 −20dB/dec、微分 +20dB/dec；转折频率处修正（惯性在 $\omega=1/\tau$ 处折点）；
3. **相频**：各环节相位叠加——惯性在折点 ±45°、远处 ±90°。

**dB 定义**：$\lvert G\rvert_{dB}=20\log_{10}\lvert G\rvert$。

**关键读数**：
- 截止/穿越频率 $\omega_c$（幅频 = 0dB）；
- 谐振峰（二阶环节 $\zeta$ 小）→ 超调相关；
- 低频斜率 → 系统型别。

## 2. 最小可手算例子

**题目**：$G(s)=\dfrac{10}{s+1}$，画渐近线并求低频增益与转折频率。

**解**：低频（$\omega\ll1$）：$\lvert G\rvert\approx10\to20$dB（平坦）；转折 $\omega=1$：斜率变 −20dB/dec；相频 0° → −45°(ω=1) → −90°。渐近线快速可得 ✓。

**易错点**：dB 与线性增益换算；转折频率 = $1/\tau$ 而非 $\tau$；二阶谐振峰修正。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 渐近线=精确曲线 | 渐近线是近似，折点处修正 |
| 忘记叠加相位 | 相频也是叠加 |
| 忽略积分环节斜率 | 含 $1/s$ 时低频斜率 −20dB/dec |

## 4. 与后续知识连接

- [[频率响应]]：来源；
- [[稳定裕度]]、[[相位裕度]]：从 Bode 读稳定性；
- [[Nyquist图]]：另一表示；
- [[Nichols图]]：幅相图。

## 5. 检索练习（闭卷）

1. 画 $G=\frac{10}{s(s+1)}$ 的 Bode 渐近线；
2. 解释各环节斜率叠加；
3. 从 Bode 读截止频率；
4. dB 与线性值换算。

## 6. 通过标准

- 能画 Bode 渐近线；
- 能分解典型环节；
- 能读取带宽/裕度信息。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重画 Bode；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
