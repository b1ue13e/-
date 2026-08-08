---
type: study
topic: "P控制"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: beginner
stage_moc: "[[🧭 阶段4-经典控制入门]]"
flow: knowledge
kind: concept
concept: ["比例控制", "P控制"]
prerequisites: ["PID公式", "稳态误差"]
related: ["I控制", "D控制", "根轨迹"]
upstream: ["[[PID公式]]"]
source: "Modern Control Engineering (Ogata) Ch.6"
tags: [学习, 控制与机器人学, PID]
---

# P控制

## 0. 为什么学它

**P（比例）控制**是最简单的反馈：输出 = 误差 × 增益。它奠定"增益调大响应快、但过大不稳定"的基本权衡，也是理解根轨迹与稳定裕度的起点。

## 1. 核心模型

$$u=K_p e=K_p(r-y).$$

**闭环传递函数**（对象 $G$，单位反馈）：$\dfrac{Y}{R}=\dfrac{K_p G}{1+K_p G}$。

**特性**：
- 增大 $K_p$：响应加快、稳态误差减小（0 型系统 $e_{ss}=\frac{1}{1+K_pK_{plant}}$）；
- 过大 $K_p$：闭环极点右移 → 振荡/不稳定（见 [[根轨迹]]）。

## 2. 最小可手算例子

**题目**：对象 $G=\frac{1}{s+1}$，$K_p=4$，求闭环传递函数与阶跃稳态误差。

**解**：$\dfrac{Y}{R}=\dfrac{4/(s+1)}{1+4/(s+1)}=\dfrac{4}{s+5}$。
稳态误差 $e_{ss}=\dfrac{1}{1+K_pG(0)}=\dfrac{1}{1+4}=0.2$（20% 残差——比例控制无法消除）。

**易错点**：$K_p\to\infty$ 误差 → 0 但永不消除；对象增益并入 $K_p$。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| P 能消除稳态误差 | 只能减小，0 型系统残差 $\frac{1}{1+KK_p}$ |
| 增益越大越好 | 超过稳定边界系统振荡 |
| 忽略对象增益 | $K_p G(0)$ 乘积决定误差 |

## 4. 与后续知识连接

- [[I控制]]：加入积分消除残差；
- [[D控制]]：加阻尼；
- [[根轨迹]]：$K_p$ 增大如何移动极点；
- [[ZN调参]]：比例增益作为整定起点。

## 5. 检索练习（闭卷）

1. 写出 P 控制律与闭环传递函数；
2. 计算 $G=\frac{2}{s+2}$ 在 $K_p=3$ 的稳态误差；
3. 解释 $K_p$ 与稳定性的权衡；
4. 为什么 P 不能完全消除误差。

## 6. 通过标准

- 能写出 P 控制律并求闭环；
- 能计算稳态误差；
- 能理解增益-稳定性权衡。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重算误差；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
