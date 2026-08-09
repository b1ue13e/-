---
type: project
project_type: homework
course: "30-应用回归分析"
assignment_id: "REG-L03"
assignment_level: lesson
assignment_format: lab
stage_id: "03"
requires: ["[[岭回归]]", "[[应用回归分析-Lasso回归与坐标下降]]", "[[应用回归分析-广义线性模型框架]]", "[[Logistic回归模型]]", "[[中心化和标准化]]"]
source_type: local_integration_task
source: "依据 ISLP Ch. 4 与 Ch. 6 学习目标自编"
source_url: "https://www.statlearning.com/"
license: "本地原创；外部来源 link-only，具体许可 [待验证]"
created: 2026-08-09
status: planned
flow: project
tags: [作业, 应用回归分析, 正则化, GLM]
---

# 应用回归分析课后作业 03：正则化与 GLM

## 学习目标

- 手算一次 Ridge/Lasso 更新并理解惩罚效果。
- 将标准化和超参数选择放进训练折。
- 区分异方差 WLS 与 GLM IRLS 的权重来源。

## 任务边界

只比较线性预测子下的 Ridge、Lasso 与 Binomial-logit GLM。Poisson、Elastic Net 和选择后推断属于可选延伸，不得成为主任务的隐藏前置；外部求解器只能作为对照，软阈值步骤必须手算。

## 题目

### A. 正则化

1. 对给定二变量标准化数据，推导 Ridge 闭式解。
2. 对给定部分残差和 $\lambda$，手算一次 Lasso 软阈值更新。
3. 用 diabetes 数据在同一外层 CV 下比较 OLS、Ridge 与 Lasso。
4. 报告 Lasso 非零系数在五个重抽样种子下的稳定性。

### B. Logistic GLM

1. 用固定种子生成二分类数据，规定正系数对应风险上升或下降并检查方向一致。
2. 拟合 Binomial-logit GLM，报告优势比、置信区间和 deviance。
3. 写出一次 IRLS 更新所需的工作响应和权重，不要求从零实现完整求解器。
4. 在独立测试集报告 ROC AUC 与校准信息；阈值准确率只能作补充。

## 禁止事项

- 不得在交叉验证前全量标准化。
- 不得使用测试集选择 $\lambda$ 或分类阈值。
- 不得把非零 Lasso 系数写成因果变量。

## 提交产物

- regularization.py
- logistic_glm.py
- report.md
- tests/：至少测试软阈值边界、概率范围和同种子复现

## Rubric

| 维度 | 分值 | 通过要求 |
| :--- | ---: | :--- |
| 推导 | 20 | Ridge 与软阈值步骤正确 |
| 无泄漏实现 | 30 | 预处理、调参、测试边界正确 |
| GLM 解释 | 25 | 优势比、IRLS、deviance 口径正确 |
| 稳定性与误差 | 15 | 保留选择不稳定或失败证据 |
| 复现 | 10 | 测试和命令可运行 |

总分至少 75，无泄漏实现不少于 22。

## 提交前自检

- [ ] Pipeline 包含全部数据依赖的预处理。
- [ ] 测试集只评价一次。
- [ ] Logistic 生成公式、事件定义和解释方向一致。
- [ ] 没有把 IRLS 权重解释成样本重要性。

完成后进入 [[应用回归分析-阶段作业-03-候选模型比较]]。
