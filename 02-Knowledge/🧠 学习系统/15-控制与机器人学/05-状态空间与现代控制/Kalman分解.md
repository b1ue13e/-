---
type: study
topic: "Kalman分解"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段5-状态空间与现代控制]]"
flow: knowledge
kind: derivation
concept: ["Kalman分解", "可控可观分解", "最小实现"]
prerequisites: ["能控性定义", "能观性定义"]
related: ["最小实现", "能控标准型", "能观标准型"]
upstream: ["[[能观性定义]]"]
source: "Modern Control Engineering (Ogata) Ch.10"
tags: [学习, 控制与机器人学, 能控能观]
---

# Kalman分解

## 0. 为什么学它

一般系统的状态可分成四类：**可控可观、可控不可观、不可控可观、不可控不可观**。**Kalman 分解**通过相似变换把这些子空间分离出来——它是理解传递函数为何"丢模态"、构造最小实现的理论基础。

## 1. 核心分解

通过相似变换 $z=Tx$ 把系统分解为四块结构：

$$\dot z=\begin{pmatrix}A_{co}&0&A_{13}&0\\A_{21}&A_{\bar co}&A_{23}&A_{24}\\0&0&A_{\bar c o}&0\\0&0&A_{43}&A_{\bar c \bar o}\end{pmatrix}z+\begin{pmatrix}B_{co}\\B_{\bar co}\\0\\0\end{pmatrix}u,\qquad y=\begin{pmatrix}C_{co}&0&C_{\bar co}&0\end{pmatrix}z.$$

**四块**：可控可观（co，可测可控）、可控不可观（cō）、不可控可观（c̄o）、不可控不可观（c̄ō）。

**传递函数只含 co 块**：$G(s)=C_{co}(sI-A_{co})^{-1}B_{co}$——其余模态被"隐藏"。

## 2. 最小可手算例子（概念验证）

**题目**：零极点对消系统如何体现 Kalman 分解？

**解**：$G(s)=\frac{s+1}{(s+1)(s+2)}=\frac{1}{s+2}$ 对消了 $s=-1$ 模态。状态空间中该模态落在"不可控或不可观"子空间——分解后 $G(s)$ 只剩 $A_{co}$ 部分，与对消结果一致 ✓。

**易错点**：分解的变换矩阵 $T$ 由可控/可观子空间基构造；对角块顺序随构造而异。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 分解唯一 | 四子空间唯一，坐标表示不唯一 |
| 传递函数包含全部信息 | 只含可控可观子空间 |
| 与能控标准型混淆 | 标准型是可控子空间的规范形，分解是全体分割 |

## 4. 与后续知识连接

- [[最小实现]]：删去不可控/不可观子空间；
- [[能控性定义]]、[[能观性定义]]：判据；
- [[SS与TF转换]]：对消的来源。

## 5. 检索练习（闭卷）

1. 画出四块分解结构；
2. 说明各子空间含义；
3. 解释对消与分解的关系；
4. 最小实现如何得到。

## 6. 通过标准

- 能理解四子空间分解；
- 能解释对消来源；
- 能理解最小实现。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重述分解；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
