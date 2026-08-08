---
type: study
topic: "Stanley前馈"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段6-横向控制]]"
flow: knowledge
kind: derivation
concept: ["Stanley", "前馈", "曲率补偿"]
prerequisites: ["Stanley公式", "曲率控制"]
related: ["Stanley公式", "Stanley高速"]
upstream: ["[[Stanley公式]]"]
source: "Stanford Stanley (2006); 横向控制文献"
tags: [学习, 控制与机器人学, 横向控制]
---

# Stanley前馈

## 0. 为什么学它

纯 Stanley 反馈在弯道会留下**稳态横向偏差**（转弯时需要持续转向，反馈跟不上）。**Stanley 前馈**加入路径曲率项 $\delta_{ff}=\arctan(\kappa L)$，让控制器"预知弯道"，消除弯道稳态误差。

## 1. 核心方法

**加前馈的 Stanley**：

$$\delta = \psi + \arctan\left(\frac{k e_y}{v}\right) + \delta_{ff},\qquad \delta_{ff}=\arctan(\kappa_{path}L).$$

**前馈含义**：$\delta_{ff}$ 是"沿路径曲率 $\kappa$ 转弯所需的稳态转向角"（自行车模型）——弯道里反馈只需纠偏差，不再独自扛曲率。

**收益**：弯道横向误差显著减小（稳态残差被前馈消除）。

## 2. 最小可手算例子

**题目**：$L=2.5,\ \kappa=0.04$，求前馈转向角。

**解**：$\delta_{ff}=\arctan(0.04\times2.5)=\arctan(0.1)=5.7°$——弯道基本转向由前馈承担 ✓。

**易错点**：前馈依赖路径曲率（需路径信息）；曲率与 L 的单位匹配。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 前馈可替代反馈 | 前馈防偏差，反馈纠扰动/模型误差 |
| 曲率恒定假设 | 路径曲率变化时需逐点读取 |
| 忽略 L | 前馈量含轴距 |

## 4. 与后续知识连接

- [[Stanley公式]]：主控制律；
- [[Stanley高速]]：高速弯道更需前馈；
- [[曲率控制]]：曲率来源。

## 5. 检索练习（闭卷）

1. 写出含前馈的 Stanley；
2. 计算前馈转向角；
3. 解释弯道稳态误差来源；
4. 前馈与反馈分工。

## 6. 通过标准

- 能加曲率前馈；
- 能理解稳态误差；
- 能实现完整 Stanley。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重算前馈；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
