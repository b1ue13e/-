---
type: index
topic: "MIT OCW 14.384 Sample Problems 知识点映射"
created: 2026-08-05
status: active
flow: project
kind: moc
tags: [索引, 作业映射, 时间序列分析, MIT OCW]
source: "MIT OCW 14.384 Time Series Analysis, Prof. Anna Mikusheva, Fall 2013 (CC BY-NC-SA 4.0)"
source_url: "https://ocw.mit.edu/courses/14-384-time-series-analysis-fall-2013/pages/assignments-and-exams/"
---

# 🎓 MIT OCW 14.384 Sample Problems 知识点映射

> MIT 14.384 官方 Problem Sets 未公开，OCW 提供 **Sample problems (PDF)** 与 **Sample final exam (PDF)** 供选做。
> 本表把讲义主题与样例题考查点映射到本库知识点笔记卡，作为理论进阶链。

## 来源与许可

- 课程页：https://ocw.mit.edu/courses/14-384-time-series-analysis-fall-2013/
- 讲义 26 讲（Lec 1-26）+ Sample problems + Sample final exam
- License：CC BY-NC-SA 4.0（可引用、需署名、非商用、相同方式共享）
- 使用口径：`link-only` 引用讲义结论，不复制解答；作业独立完成

## 讲义主题 → 知识点映射

| MIT 14.384 讲义 | 主题 | 对应笔记卡 | 前置 |
| :--- | :--- | :--- | :--- |
| Lec 1 | Stationarity, lag operator, ARMA, covariance structure | [[平稳性]]、[[ARMA模型]]、[[自相关函数ACF]] | 随机过程基础 |
| Lec 2-3 | Limit theorems, OLS, HAC | [[时间序列参数估计 (OLS, Yule-Walker, MLE)]]、[[动态回归与ARIMAX]] | 渐近理论 |
| Lec 4-5 | Spectrum, spectrum estimation, information criteria | [[时间序列核心公式清单]]（谱分析为进阶扩展） | 傅里叶基础 |
| Lec 6 | GMM | 广义矩方法（进阶扩展） | 矩条件 |
| Lec 9 | Bootstrap | 自助法（进阶扩展） | 重抽样 |
| Lec 10-11 | Introduction to VARs | [[向量自回归VAR]] | 多元回归 |
| Lec 12-13 | Structural VARs | [[向量自回归VAR]]（结构识别进阶） | 格兰杰因果 |
| Lec 14-15 | Factor models | 因子模型（进阶扩展） | 主成分 |
| Lec 17 | Unit roots | [[单位根检验-ADF-KPSS]]、[[随机游走（深挖笔记）]] | ADF 检验 |
| Lec 18 | More non-stationarity | [[趋势平稳与差分平稳（深挖笔记）]] | 确定性/随机趋势 |
| Lec 19-20 | Breaks and cointegration | [[协整]]、[[误差修正模型]]、[[单位根检验-ADF-KPSS]] | 结构突变、单位根 |
| Lec 21 | Filtering, state space models, Kalman filter | [[状态空间模型与Kalman滤波]] | 状态空间 |
| Lec 22 | State-space ML estimation, DSGE | [[状态空间模型与Kalman滤波]]（DSGE 进阶） | MLE |
| Lec 23-26 | Bayes, MCMC (Metropolis-Hastings, Gibbs) | 贝叶斯时序（进阶扩展） | 贝叶斯推断 |

## Sample Problems 考查点（按主题推断，题目 PDF 需自行下载）

| 考查点 | 对应讲义 | 对应笔记卡 | 难度 |
| :--- | :--- | :--- | :--- |
| 平稳性判定与 ARMA 协方差结构 | Lec 1 | [[平稳性与ACF-PACF]] | ⭐⭐ |
| OLS 在时序中的一致性与 HAC 标准误 | Lec 2-3 | [[时间序列参数估计 (OLS, Yule-Walker, MLE)]] | ⭐⭐⭐ |
| 谱密度与信息准则 | Lec 4-5 | [[时间序列核心公式清单]] | ⭐⭐⭐ |
| VAR 估计与推断 | Lec 10-11 | [[向量自回归VAR]] | ⭐⭐⭐ |
| 单位根检验与大样本性质 | Lec 17 | [[单位根检验-ADF-KPSS]] | ⭐⭐⭐ |
| 协整与误差修正 | Lec 19-20 | [[协整]]、[[误差修正模型]] | ⭐⭐⭐⭐ |
| 状态空间与 Kalman 滤波估计 | Lec 21-22 | [[状态空间模型与Kalman滤波]] | ⭐⭐⭐⭐ |

## 使用建议

1. 完成 FPP3 HW01-05 与本地 HW01-09 后，再进入 MIT 样例题（研究生水平，需数理统计与渐近理论前置）。
2. 样例题作为**理论进阶验收**：能独立完成 Sample problems 中的单位根/协整/状态空间部分，即达到课程理论层验收线。
3. 相关入口：[[🧭 开源作业体系-时间序列分析]]、[[📚 教材挂载索引]]
