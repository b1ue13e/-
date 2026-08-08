---
type: study
topic: "I控制"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段4-经典控制入门]]"
flow: knowledge
kind: concept
concept: ["积分控制", "消除稳态误差"]
prerequisites: ["PID公式", "P控制"]
related: ["D控制", "抗饱和", "稳态误差"]
upstream: ["[[P控制]]"]
source: "Modern Control Engineering (Ogata) Ch.6"
tags: [学习, 控制与机器人学, PID]
---

# I控制

## 0. 为什么学它

P 控制永远留残差，**I（积分）控制**通过对误差的累积"持续施压"，直到误差为零——这是消除稳态误差的唯一机制，也是 90% 工业回路必须含积分的原因。

## 1. 核心模型

$$u=K_i\int_0^t e(\tau)d\tau.$$

**频域**：$C(s)=\dfrac{K_i}{s}$——含积分环节，把系统型别 +1：0 型 → I 型，阶跃误差归零。

**闭环**（对象 $G$）：$\dfrac{Y}{R}=\dfrac{K_i G/s}{1+K_i G/s}$。

**代价**：积分累积导致超调增大、响应变慢；执行器饱和时积分"风起"（见 [[抗饱和]]）。

## 2. 最小可手算例子

**题目**：对象 $G=\frac{1}{s+1}$，PI 控制 $C(s)=K_p+K_i/s$，取 $K_p=1,K_i=1$，验证阶跃稳态误差为零。

**解**：开环 $L(s)=(\frac{s+1}{s})\frac{1}{s+1}=\frac{1}{s}$（I 型）。阶跃输入 $e_{ss}=\lim_{s\to0}\frac{s\cdot(1/s)}{1+1/s}=\lim_{s\to0}\frac{1}{s+1}=0$ ✓。

**易错点**：积分增益过大 → 振荡；$K_i$ 与积分时间 $T_i=K_p/K_i$ 的关系。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| I 越大收敛越快越好 | 过大会振荡甚至失稳 |
| I 对噪声也累积 | 传感器噪声会被积分放大，需滤波 |
| 积分消除一切误差 | 对斜坡/抛物线仍需更高型别 |

## 4. 与后续知识连接

- [[P控制]]：组合为 PI；
- [[D控制]]：组合为 PID；
- [[抗饱和]]、[[积分分离]]：积分风起处理；
- [[稳态误差]]：型别提升原理。

## 5. 检索练习（闭卷）

1. 写出 I 控制律与传递函数；
2. 说明 I 如何提升型别消除误差；
3. 解释积分风起；
4. PI 控制为何是工业默认。

## 6. 通过标准

- 能写 I 控制律并分析型别提升；
- 能计算 PI 闭环稳态误差；
- 能识别积分副作用。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重算 PI 误差；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
