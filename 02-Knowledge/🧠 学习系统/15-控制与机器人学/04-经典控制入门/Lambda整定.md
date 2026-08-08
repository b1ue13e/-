---
type: study
topic: "Lambda整定"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段4-经典控制入门]]"
flow: knowledge
kind: problem-type
concept: ["Lambda整定", "PID整定", "鲁棒整定"]
prerequisites: ["PID公式", "一阶系统"]
related: ["ZN调参", "试凑法"]
upstream: ["[[PID公式]]"]
source: "Lambda tuning (Dahlin); 工业整定文献"
tags: [学习, 控制与机器人学, PID]
---

# Lambda整定

## 0. 为什么学它

ZN 法超调大、激进；**Lambda 整定**通过指定期望闭环时间常数 $\lambda$ 直接反解控制器参数，超调可控、鲁棒性好，是过程控制（温控、液位）的主流方法——"先定期望速度，再算参数"。

## 1. 核心思想

对象近似一阶惯性 + 滞后：$G(s)=\dfrac{K e^{-Ls}}{\tau s+1}$。

指定期望闭环时间常数 $\lambda$，设计控制器使闭环极点位于 $-\frac{1}{\lambda}$（把对象的 $\tau$ "替换"为 $\lambda$）。

**PI 参数公式**（$\lambda$ 为主调参数）：

$$K_p=\frac{\tau}{K(\lambda+L)},\qquad T_i=\tau.$$

**工程选择**：$\lambda$ 越大越慢越鲁棒；常用 $\lambda=1\sim3$ 倍对象时间常数。

## 2. 最小可手算例子

**题目**：对象 $K=2,\ \tau=10$ s（无滞后），取 $\lambda=10$，求 PI 参数。

**解**：$K_p=\dfrac{10}{2(10+0)}=0.5$；$T_i=10$ s。闭环时间常数 = $\lambda=10$（与原对象 $\tau$ 相同 → 不激进）。

**易错点**：$\lambda$ 太小会导致控制输入过大；滞后 $L$ 不可忽略时公式含 $L$。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| $\lambda$ 是对象参数 | 是**设计者指定**的期望闭环时间常数 |
| Lambda 只适合快系统 | 越慢越稳，适合过程控制 |
| 与 ZN 结果一样 | Lambda 通常更保守、超调更小 |

## 4. 与后续知识连接

- [[ZN调参]]：激进法的对比；
- [[试凑法]]：后续微调；
- [[一阶系统]]：模型基础；
- 工程：温控、液位、压力回路整定。

## 5. 检索练习（闭卷）

1. 写出 Lambda 整定公式；
2. 计算给定对象与 $\lambda$ 的 PI 参数；
3. 解释 $\lambda$ 的物理含义；
4. 对比 ZN 与 Lambda 的取舍。

## 6. 通过标准

- 能按 Lambda 法计算参数；
- 能解释 $\lambda$ 选择；
- 能对比不同整定法。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重算参数；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
