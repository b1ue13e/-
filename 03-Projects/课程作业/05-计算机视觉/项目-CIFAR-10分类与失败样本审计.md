---
title: "CIFAR-10分类与失败样本审计"
type: project
topic: "CIFAR-10分类与失败样本审计"
course: "计算机视觉"
created: 2026-07-28
updated: 2026-07-28
status: planned
progress: 0%
flow: project
kind: project
project_type: homework
asset_eligibility: eligible
eligibility_audited: 2026-07-28
difficulty_tier: T3
source_url: "https://cs231n.stanford.edu/2025/assignments.html"
source_course: "Stanford CS231n 2025"
source_version: "link-only snapshot verified 2026-07-28; exact release/commit must be frozen when activated"
license: "本地原创作业规格；外部课程与素材保持 link-only，并按各自条款使用"
mirror_policy: link-only
adaptation: original
dataset_version: "torchvision CIFAR-10；记录 torchvision 版本、官方 checksum 与固定切分"
starter_code: "03-Projects/课程作业/05-计算机视觉/项目-CIFAR-10分类与失败样本审计.md#5-starter-与提交结构"
tests: "03-Projects/课程作业/05-计算机视觉/项目-CIFAR-10分类与失败样本审计.md#6-验收测试"
baseline: "像素标准化后的线性分类器或小型 CNN"
acceptance_test: "Rubric ≥ 75/100，全部硬验收通过，且无失败条件"
compute_budget: low
solution_visibility: private
tags: [项目, 正式作业, 计算机视觉, 课程验收]
---

# CIFAR-10分类与失败样本审计

> 这是为 `计算机视觉` 编写的**本地原创正式作业**。外部课程只决定知识顺序和参考边界；本页不复制外部题目、Starter 或答案。课程未成为 Active Sprint 前，状态保持 `planned`。

## 1. 任务与学习结果

完成后需要证明：你不仅能复述知识，还能在固定输入、明确协议和失败条件下独立得到可复核结果。

- **输入/数据**：torchvision CIFAR-10；记录 torchvision 版本、官方 checksum 与固定切分。
- **朴素基线**：像素标准化后的线性分类器或小型 CNN。
- **独立实现**：实现训练、验证、checkpoint 和混淆矩阵；比较小型 CNN 与 ResNet-18。
- **强验证**：只改变一个增强/正则因素，报告类别级失败、校准和计算成本。

## 2. 来源与使用边界

- **Spine**：[Stanford CS231n 2025](https://cs231n.stanford.edu/2025/assignments.html)，仅作为学习顺序与公开入口。
- **本地内容**：任务改写、评价协议、Rubric 和提交结构均为原创。
- **镜像策略**：`link-only`；激活课程时再记录精确版本、许可证、数据条款和环境锁文件。
- **答案策略**：只保存自己的实现与摘要；完整解答保持私有，不挂他人答案仓库。

## 2.1 老师版说明书入口

- [[02-Knowledge/🧠 学习系统/05-计算机视觉/18-实战作业说明书/🎓 HW01 - CIFAR-10 kNN 与 Softmax 基线正式作业说明书|HW01 正式作业说明书]]
- [[03-Projects/课程作业/05-计算机视觉/real_assignment_packages/hw01_cifar10_knn_softmax/README|HW01 真实作业包]]

## 3. 执行阶段

| 阶段 | 工作 | 必交证据 |
|:---|:---|:---|
| T1 规格与最小例 | 冻结输入、环境、随机种子和评价口径 | manifest、最小手算/已知答案例 |
| T2 Baseline | 完成朴素方法并逐项解释 | 基线输出、测试与误差记录 |
| T3 独立实现 | 实现训练、验证、checkpoint 和混淆矩阵；比较小型 CNN 与 ResNet-18 | 实现、日志、同口径比较 |
| T4 强验证 | 只改变一个增强/正则因素，报告类别级失败、校准和计算成本 | 敏感性、失败案例与结论边界 |

## 4. 数据、版本与复现清单

- [ ] 记录来源 URL、访问日期和适用条款。
- [ ] 冻结数据快照、生成规则或 `not-applicable` 原因。
- [ ] 记录软件版本、随机种子与运行入口。
- [ ] Baseline 和改进方法使用相同输入与评价口径。
- [ ] 结果表中不预填成绩，不把单次最好结果当结论。

## 5. Starter 与提交结构

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ExperimentConfig:
    seed: int = 42

def load_data(config: ExperimentConfig):
    raise NotImplementedError

def build_baseline(config: ExperimentConfig):
    raise NotImplementedError

def evaluate(model, data) -> dict[str, float]:
    raise NotImplementedError
```

```text
submission/
├── README.md
├── manifest.yml
├── src-or-proofs/
├── tests-or-checks/
├── artifacts/
└── report.md
```

`manifest.yml` 至少记录：来源、版本、数据、环境、种子、运行入口、输出清单和已知限制。

## 6. 验收测试

以下是硬验收，任一项失败都不能依靠总分抵消：

- [ ] `01` 训练与测试变换明确分离
- [ ] `02` 模型在固定小批量上可过拟合
- [ ] `03` checkpoint 重载预测一致
- [ ] `04` 混淆矩阵总数等于测试样本数
- [ ] 所有产出可从 `README.md` 按顺序复核。
- [ ] 报告包含至少一个失败案例和适用边界。

## 7. 100 分 Rubric

| 维度 | 分值 | 通过证据 | 得分 |
|:---|---:|:---|:---:|
| 正确性与测试 | 25 | 证据完整、可复核且没有硬失败 | /25 |
| 公平基线与切分 | 20 | 证据完整、可复核且没有硬失败 | /20 |
| 实验与失败分析 | 20 | 证据完整、可复核且没有硬失败 | /20 |
| 工程与复现 | 20 | 证据完整、可复核且没有硬失败 | /20 |
| 报告与知识反哺 | 15 | 证据完整、可复核且没有硬失败 | /15 |
| **总计** | **100** | **达到 75 分且硬验收全部通过** | **/100** |

## 8. 失败条件

- 使用测试数据、参考答案或未来信息参与方法选择；
- 来源、数据、环境或随机性无法追溯；
- Baseline 与改进方法使用不同评价口径；
- 只展示成功结果，不报告反例、诊断或失败模式；
- 复制外部课程答案，或把公开可见误认为允许再分发；
- 无法从提交物独立复核关键结论。

## 9. 提交物

- [ ] `README.md`：一条从环境到结果的复核路径；
- [ ] `manifest.yml`：版本、数据、条款、环境与种子；
- [ ] 实现、证明或分析计划；
- [ ] 硬验收测试及真实输出；
- [ ] Baseline 与强验证对比；
- [ ] `report.md`：结论、失败案例、限制与知识反哺。

## 10. 知识反哺

完成后至少沉淀一项：

- 概念误解 → `kind: concept`；
- 可复用证明/解法 → `kind: derivation` 或 `problem-type`；
- 失败与漏洞 → `kind: mistake`，必要时设置 `flow: review`。

## 11. 当前状态

| 项目 | 状态 |
|:---|:---:|
| 正式作业规格 | completed |
| 来源与镜像边界 | completed |
| 精确版本与环境冻结 | activation-gated |
| 实际执行与评分 | planned |
