---
type: study
topic: Matplotlib信号
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
  - "Think DSP（matplotlib 实例）"
  - "Matplotlib 官方文档"
  - "SciPy Lecture Notes"
assessment_exempt_reason: "软件/环境参考页，非可验收知识点卡"

upstream:
  - "[[NumPy信号]]"
---
# Matplotlib信号

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🚀 第八阶段：工程实现]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：Python 工具链
- 这张卡要回答的问题：如何用 Matplotlib 可视化信号与频谱？
- 阶段目标：掌握时域波形、频谱（幅/相）、频谱图的基本画法，把分析结果画出来。

## 对应教材（真实出处）
- Think DSP（matplotlib 实例）
- Matplotlib 官方文档
- SciPy Lecture Notes

## 一句话定义
> plt.plot 画时域；先 fftshift+abs/angle 再 plot 画幅/相频谱；specgram 画语谱图；subplot 并排对比——可视化是验证理解的利器。

## 从学习内容上要抓什么
- 幅谱用 abs(X)，相谱用 angle(X)。
- fftshift 把零频移到中央。
- 语谱图看时频演化。

## 核心内容
### 1. 基本定义与直觉
Matplotlib 是你的「信号眼睛」：看不见的公式，画出来一眼就懂对不对。

### 2. 公式 / 机制 / 流程
$$plt.plot(t,x);\quad plt.plot(f,np.abs(np.fft.fftshift(X)))$$

### 3. 一个最小例子
画出 50Hz 正弦时域与单边幅频谱（尖峰在 50Hz）。

### 4. 常见误区
- 未 fftshift 致频谱左右颠倒。
- 幅谱用错线性/对数刻度掩盖细节。

## 和其他笔记的关系
- 前置：[[NumPy信号]]
- 前置：[[SciPy信号]]
- 相关：[[频谱泄漏原因]]
- 相关：[[加窗]]
- 相关：[[SoundFile]]
- 返回阶段索引：[[🚀 第八阶段：工程实现]]

## 最小自测
- [ ] 如何画幅频谱？
- [ ] 为何用 fftshift？
- [ ] 语谱图用途？

*创建于：2026-04-18 · 更新于：2026-08-06*
