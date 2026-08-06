---
type: study
topic: "Nyquist判据"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段4-经典控制入门]]"
flow: knowledge
kind: derivation
concept: ["Nyquist判据", "频域稳定性", "围线积分"]
prerequisites: ["Nyquist图", "BIBO稳定"]
related: ["稳定裕度", "Nyquist图", "劳斯判据"]
upstream: ["[[04-经典控制入门/Nyquist图]]"]
source: "Modern Control Engineering (Ogata) Ch.7; Nyquist (1932)"
tags: [学习, 控制与机器人学, 频域分析]
---

# Nyquist判据

## 0. 为什么学它

劳斯判据需要传函解析式，但工程上常只有**实验频率响应**（无法写解析式）。**Nyquist 判据**仅凭开环 $G(j\omega)$ 的 Nyquist 图（可实测）就判断闭环稳定性——频域稳定性分析的基石。

## 1. 核心判据

**闭合曲线**：$\omega$ 从 $-\infty\to+\infty$ 扫过 $1+G(j\omega)$（或 $-1$ 点的 $G(j\omega)$ 曲线）。

**判据**：闭环稳定的充要条件——Nyquist 曲线绕 $(-1, j0)$ 点的**净圈数 $N$** 等于开环右半平面极点数 $P$：

$$N = P \quad(\text{稳定}),$$

其中 $N$ = 顺时针绕 $(-1,0)$ 的圈数 − 逆时针圈数。开环稳定（$P=0$）时，判据简化为"曲线不包围 $(-1,0)$"。

**意义**：$(-1,0)$ 点 = $1+G(j\omega)=0$ 即闭环特征根在虚轴上的临界点——曲线越靠近它，稳定裕度越小。

## 2. 最小可手算例子

**题目**：$G(s)=\dfrac{K}{(s+1)(s+2)}$，开环稳定（$P=0$）。$K=2$ 时闭环稳定吗？

**解**：$G(0)=K/2$。$K=2$：$G(0)=1$，Nyquist 曲线从 $(1,0)$ 出发右移，不包围 $(-1,0)$ → 闭环稳定 ✓。增大 $K$ 至曲线经过 $(-1,0)$ → 临界；$K>4$（$G(0)>2$ 使曲线包住 $-1$ 点）→ 不稳定。可由 $K_c$ 反推临界增益。

**易错点**：绕点计数方向；$P$ 是开环 RHP 极点数；$G$ 在虚轴有极点时需凸出处理。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 只看曲线形状不数圈 | 必须数绕 $(-1,0)$ 的净圈数与 $P$ 比较 |
| 忽略 $P$ | 开环不稳时 $N=P$ 才闭环稳定 |
| 与 Bode 裕度混淆 | 判据是精确判稳，裕度是量化储备 |

## 4. 与后续知识连接

- [[Nyquist图]]：判据载体；
- [[稳定裕度]]：绕点距离量化；
- [[劳斯判据]]：代数方法对比；
- [[Bode图]]：工程实现。

## 5. 检索练习（闭卷）

1. 陈述 Nyquist 判据；
2. 判断 $G=\frac{K}{(s+1)(s+2)}$ 稳定条件；
3. 解释 $(-1,0)$ 点的意义；
4. 虚轴极点的处理。

## 6. 通过标准

- 能用 Nyquist 判据判稳；
- 能数净圈数；
- 能求临界增益。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重判稳定；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
