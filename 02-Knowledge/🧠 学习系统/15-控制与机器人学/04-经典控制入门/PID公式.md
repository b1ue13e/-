---
type: study
topic: "PID公式"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段4-经典控制入门]]"
flow: knowledge
kind: concept
concept: ["PID", "控制器", "反馈控制"]
prerequisites: ["负反馈", "稳态误差", "时域指标"]
related: ["P控制", "I控制", "D控制", "抗饱和"]
upstream: ["[[负反馈]]"]
source: "Modern Control Engineering (Ogata) Ch.6-8; PID 经典文献"
tags: [学习, 控制与机器人学, PID]
---

# PID公式

## 0. 为什么学它

**PID（比例-积分-微分）**是工业控制使用率最高的控制器：P 提供即时响应、I 消除稳态误差、D 增加阻尼。理解三通道的"分工"，才能理解后续所有整定方法（ZN、Lambda）为何这样设计。

## 1. 核心公式

**理想连续 PID**：

$$u(t)=K_p e(t)+K_i\int_0^t e(\tau)d\tau+K_d\frac{de(t)}{dt}.$$

**并联形式**（工程常用）：$u=K_p e + \frac{K_p}{T_i}\int e\,dt + K_p T_d\dot e$（$T_i$ 积分时间、$T_d$ 微分时间）。

**传递函数**：$C(s)=K_p+\dfrac{K_i}{s}+K_d s$。

**离散化（增量式）**：$u_k=u_{k-1}+K_p(e_k-e_{k-1})+K_i e_k\Delta t+K_d\frac{e_k-2e_{k-1}+e_{k-2}}{\Delta t}$。

| 通道 | 作用 | 副作用 |
|:---|:---|:---|
| P | 即时纠偏 | 稳态误差（0 型系统） |
| I | 消除稳态误差 | 超调、积分饱和 |
| D | 阻尼、预测 | 放大噪声 |

## 2. 最小可手算例子

**题目**：$K_p=2,K_i=1,K_d=0.5$，$e(t)=1$（恒定误差），求 1s 后的 $u$。

**解**：$u(1)=2\cdot1+1\cdot\int_0^1 1\,dt+0.5\cdot0=2+1=3$（P+I 贡献；误差恒定 D 为零）。

**易错点**：D 项对恒定误差为零（只响应变化）；积分项持续累积。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| D 能消除稳态误差 | D 只响应变化，消误差靠 I |
| 积分越大越好 | 过强积分引起振荡与饱和 |
| 忽略抗饱和 | 执行器饱和时积分风起（见 [[抗饱和]]） |

## 4. 与后续知识连接

- [[P控制]]、[[I控制]]、[[D控制]]：单通道分析；
- [[ZN调参]]、[[Lambda整定]]、[[试凑法]]：整定方法；
- [[抗饱和]]、[[积分分离]]、[[不完全微分]]：工程改进；
- [[三环控制]]：PID 在串级中的应用；
- [[PID控制器与状态空间法]]：与状态空间的对比。

## 5. 检索练习（闭卷）

1. 写出 PID 公式与传递函数；
2. 说明 P/I/D 各自作用与副作用；
3. 计算恒定误差下的 PID 输出；
4. 解释为何 D 不消稳态误差。

## 6. 通过标准

- 能写出 PID 公式与传递函数；
- 能说明三通道分工；
- 能完成基本计算；
- 能识别常见工程改进需求。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重默公式；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
