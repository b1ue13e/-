---
type: study
topic: "Allan方差"
course: "控制与机器人学"
created: 2026-08-07
updated: 2026-08-09
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段10-状态估计]]"
flow: knowledge
kind: concept
concept: ["Allan方差", "IMU标定"]
prerequisites: ["噪声模型"]
related: ["噪声模型", "导航定位", "协方差矩阵"]
upstream: ["[[噪声模型]]"]
source: "IEEE Std 952-1997（Allan 方差方法）；Groves, Principles of GNSS, Inertial, and Multisensor Navigation Ch.4"
tags: [学习, 控制与机器人学, 状态估计]
---

# Allan方差

## 0. 为什么学它

IMU 的噪声不是简单白噪声，而是**多种成分的叠加**：角度随机游走、零偏不稳定性、速率随机游走、量化噪声……普通方差只能给出一个"总抖动"数字，无法区分成分——但 $Q$ 矩阵需要按成分分别标定。**Allan 方差是 IMU 噪声的"化验单"**：通过不同平均时间下的方差曲线，把各噪声成分逐项分离，是工程上标定 $Q$ 的标准工具。

## 1. 为什么需要它

| 噪声成分 | 来源 | 特征 |
|:---|:---|:---|
| 角度随机游走（ARW） | 高频白噪声积分 | 短平均时间主导 |
| 零偏不稳定性（BI） | 电子/机械漂移 | 中频平台 |
| 速率随机游走 | 低频环境扰动 | 长平均时间主导 |
| 量化噪声 | 采样量化 | 极短时间主导 |

单一统计量无法区分这些成分；Allan 方差通过不同平均时间 $\tau$ 的方差曲线识别各自斜率。

## 2. 定义

$$
\sigma^2(\tau) = \frac{1}{2} \left\langle \left(\bar{\Omega}_{k+1}(\tau) - \bar{\Omega}_k(\tau)\right)^2 \right\rangle
$$

把连续数据按平均时间 $\tau$ 切成簇，取相邻簇均值之差的方差，画 $\log\sigma(\tau)$ vs $\log\tau$ 曲线。

## 3. 曲线解读（斜率识别）

| 区域 | 斜率 | 对应噪声 | 读出参数 |
|:---|:---|:---|:---|
| 短 $\tau$ | $-1/2$ | 角度随机游走 | ARW 系数（deg/√h） |
| 中 $\tau$ | $0$（平台） | 零偏不稳定性 | BI（deg/h） |
| 长 $\tau$ | $+1/2$ | 速率随机游走 | RRW 系数 |

## 4. 最小可手算例子（读数）

**题目**：某陀螺 Allan 曲线在 $\tau=1$ s 处 $\sigma=0.05$ deg/s，斜率为 $-1/2$。估计 ARW 系数。

**解**：ARW 区域满足 $\sigma(\tau) = \text{ARW} \cdot \tau^{-1/2}$（deg/s 单位）。取 $\tau=1$ s：

$$
\text{ARW} = \sigma(1) \times 1^{1/2} = 0.05 \ \text{deg/s} = 0.05 \ \text{deg}/\sqrt{\text{s}}
$$

换算为常用单位：$0.05 \times 60 = 3.0 \ \text{deg}/\sqrt{\text{h}}$。

**解读**：该系数直接进入 $Q$ 矩阵的对角元（角速度随机游走强度）；若在 $\tau=100$ s 处出现平台 $\sigma=0.01$ deg/s，则零偏不稳定性约为 0.01 deg/s = 36 deg/h（消费级 IMU 典型量级）。

## 5. 工程应用

- 从曲线读出各噪声系数 → 换算成 $Q$ 输入滤波器（见 [[控制与机器人学-协方差矩阵|协方差矩阵]]）；
- 比较 IMU 器件等级（消费级 / 工业级 / 光纤级）——零偏不稳定性和 ARW 是核心指标；
- 温度、批次、老化下的器件评估；
- 注意：Allan 曲线需要**长时静置数据**（数小时），动态数据无法直接使用。

## 6. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 把 Allan 方差当瞬时指标 | 它统计的是长时间序列，静置采集不足时长会失真 |
| 只看平台（BI）不看 ARW | 高动态场景 ARW 主导误差，两者都要 |
| 单位换算错 | ARW 常用 deg/√h，读曲线时注意 $\tau$ 单位（s vs h） |
| 直接用 Allan 结果做 $Q$ | 需按离散化步长换算（$Q = \text{系数}^2 \cdot dt$ 之类），不可照抄 |

## 7. 检索练习（闭卷）

1. 写出 Allan 方差定义式，解释 $\tau$ 的作用；
2. 说出三个斜率区域对应的噪声成分；
3. 给定 $\tau=1$ s 处 $\sigma=0.1$ deg/s，估算 ARW；
4. 为什么 Allan 标定需要长时静置数据？

## 8. 通过标准

- 能画出并解读 Allan 方差曲线的三个特征区域；
- 能从曲线读出 ARW / BI / RRW 系数并换算单位；
- 能把 Allan 结果换算为滤波器 $Q$ 的输入；
- 能说明 Allan 标定的数据采集要求与局限。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：给定一条完整 Allan 曲线数据，独立读出三个系数；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；
- 关联：[[导航定位\|导航定位]]、[[噪声模型\|噪声模型]]。
