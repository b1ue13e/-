---
type: study
topic: "后续-DSP"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: advanced
concept: ["后续-DSP", "后续学习建议"]
prerequisites: []
related: []
tags: ["学习", "信号与系统"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[🚀 第八阶段：工程实现]]"
sources:
  - "Think DSP 进阶"
  - "Oppenheim《Discrete-Time Signal Processing》"
  - "MIT 6.003→6.008"
kind: concept

upstream:
  - "[[DFT乘积]]"
  - "[[巴特沃斯]]"
---
# 后续-DSP

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🚀 第八阶段：工程实现]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：应用延伸
- 这张卡要回答的问题：学完本课程后，数字信号处理（DSP）方向可深入什么？
- 阶段目标：给出 DSP 进阶地图：多速率、自适应滤波、谱估计、小波等，衔接本课基础。

## 对应教材（真实出处）
- Think DSP 进阶
- Oppenheim《Discrete-Time Signal Processing》
- MIT 6.003→6.008

## 一句话定义
> DSP 进阶：多速率/抽取插值、自适应滤波(LMS)、现代谱估计(AR/ MUSIC)、小波、滤波器组；本课 DFT/FFT/Z 变换是它们的共同底座。

## 从学习内容上要抓什么
- 多速率：高效重采样、滤波器组。
- 自适应：回声消除、信道均衡。
- 现代谱估计超越周期图。

## 核心内容
### 1. 基本定义与直觉
本课是 DSP 的「地基」：FFT、Z、滤波会了，上面还能盖多速率、自适应、压缩等高层楼。

### 2. 公式 / 机制 / 流程
$$\text{基础(本课)}\to\{\text{多速率, 自适应, 谱估计, 小波}\}$$

### 3. 一个最小例子
Echo cancellation 用本课 LTI+自适应拓展。

### 4. 常见误区
- 以为本课结束就是 DSP 全部（仅是基础）。
- 忽略与统计/优化方法的交叉。

## 和其他笔记的关系
- 前置：[[DFT乘积]]
- 前置：[[巴特沃斯]]
- 相关：[[后续-语音]]
- 相关：[[后续-通信]]
- 相关：[[后续-图像]]
- 返回阶段索引：[[🚀 第八阶段：工程实现]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] DSP 有哪些进阶方向？
- [ ] 本课与它们的联系？
- [ ] 举一个应用。

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
