---
type: study
topic: SciPy信号
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: advanced
concept: 
prerequisites: []
related: []
tags: 
course: "信号与系统"
flow: knowledge
stage_moc: "[[🚀 第八阶段：工程实现]]"
kind: concept
assessment_exempt: true
sources:
  - "Think DSP Ch.4-8（scipy.signal）"
  - "SciPy 官方文档：scipy.signal"
  - "MIT 6.003 实验"
assessment_exempt_reason: "软件/环境参考页，非可验收知识点卡"

---
# SciPy信号

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🚀 第八阶段：工程实现]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：Python 工具链
- 这张卡要回答的问题：scipy.signal 在信号处理里能做什么？
- 阶段目标：掌握 scipy.signal 的滤波、频率响应、窗函数、重采样等核心功能，落地课程算法。

## 对应教材（真实出处）
- Think DSP Ch.4-8（scipy.signal）
- SciPy 官方文档：scipy.signal
- MIT 6.003 实验

## 一句话定义
> scipy.signal 提供：filter/bilinear 做滤波器、freqz 看频响、windows 造各类窗、resample 重采样、fftconvolve 快速卷积——把课堂公式变成可跑代码。

## 从学习内容上要抓什么
- 设计：butter/cheby1/cheby2/ellip。
- 分析：freqz 求 H(e^{jΩ})。
- 实践：fftconvolve 用 FFT 做卷积。

## 核心内容
### 1. 基本定义与直觉
scipy.signal 是「信号处理的工具箱」：课堂上的滤波器、窗、卷积，这里都有现成函数直接调用。

### 2. 公式 / 机制 / 流程
$$b,a=signal.butter(4,0.2);\quad w,h=signal.freqz(b,a);\quad y=signal.fftconvolve(x,h)$$

### 3. 一个最小例子
用 signal.butter 设计 4 阶低通，freqz 画出幅频曲线。

### 4. 常见误区
- 模拟/数字滤波器参数(Wn) 约定不同易错。
- 忽略 freqz 返回的 w 已归一化。

## 和其他笔记的关系
- 前置：[[NumPy信号]]
- 前置：[[巴特沃斯]]
- 相关：[[加窗]]
- 相关：[[双线性变换]]
- 相关：[[Matplotlib信号]]
- 返回阶段索引：[[🚀 第八阶段：工程实现]]

## 最小自测
- [ ] 列举 scipy.signal 主要模块。
- [ ] 如何设计巴特沃斯滤波器？
- [ ] fftconvolve 原理？

*创建于：2026-04-18 · 更新于：2026-08-06*
