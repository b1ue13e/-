---
type: study
topic: "LQR伺服"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段5-状态空间与现代控制]]"
flow: knowledge
kind: derivation
concept: ["LQR伺服", "跟踪控制", "积分增广"]
prerequisites: ["LQR增益", "稳态误差"]
related: ["LQI", "参考增益", "LQR伺服"]
upstream: ["[[LQR增益]]"]
source: "Modern Control Engineering (Ogata) Ch.10; 伺服系统教材"
tags: [学习, 控制与机器人学, LQR]
---

# LQR伺服

## 0. 为什么学它

LQR 调节（regulator）只把状态归零；**伺服（servo）**要**跟踪参考**并消除稳态误差。**LQR 伺服**通过状态增广（误差积分）或前馈参考实现跟踪，是自动驾驶跟踪、位置控制的实际形式。

## 1. 核心方法

**方法 1：误差积分增广（LQI 思想）**。引入误差积分状态 $x_I=\int e\,dt$，增广系统 $\begin{pmatrix}\dot x\\\dot x_I\end{pmatrix}$，LQR 设计 → 积分消除稳态误差。

**方法 2：参考前馈 + LQR**。$u=-Kx+K_r r$（$K_r$ 参考增益，见 [[参考增益]]），稳态跟踪参考。

**伺服结构**：$u=-Kx + K_f r$（反馈镇定 + 前馈跟踪）。

## 2. 最小可手算例子（参考增益思路）

**题目**：$\dot x=ax+bu$，LQR 反馈 $u=-kx$，求稳态跟踪常数参考 $r$ 的前馈增益。

**解**：稳态 $\dot x=0$：$0=(a-bk)x_{ss}+bk_f r\Rightarrow x_{ss}=\frac{bk_f}{bk-a}r$。要 $x_{ss}=r$：$k_f=\frac{bk-a}{b}$ ✓。

**易错点**：$k_f$ 依赖模型；模型误差时仍需积分（LQI）兜底。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 调节器可直接跟踪 | 需增广/前馈才能无差跟踪 |
| 前馈免于误差 | 模型不准时需积分项 |
| 忽略参考模型 | 跟踪需参考输入通道 |

## 4. 与后续知识连接

- [[LQI]]：积分增广形式；
- [[参考增益]]：前馈增益；
- [[稳态误差]]：需消除的误差；
- 工程：车辆横向跟踪、位置伺服。

## 5. 检索练习（闭卷）

1. 说明 LQR 调节 vs 伺服；
2. 推导参考前馈增益；
3. 解释积分增广；
4. 何时需要 LQI。

## 6. 通过标准

- 能设计 LQR 伺服；
- 能求参考增益；
- 能理解积分增广。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重推 $k_f$；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
