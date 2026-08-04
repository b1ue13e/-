---
title: "📝 阶梯作业模板-李宏毅CMU模式"
type: problem-type
kind: problem-type
flow: knowledge
topic: "作业模板"
course: "学习系统"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: active
difficulty: intermediate
importance: A
concept: ["作业模板", "阶梯作业架构"]
prerequisites: []
related: []
upstream: ["[[AGENTS.md]]"]
downstream: []
tags: [模板, 作业, 阶梯作业]
aliases: ["李宏毅CMU作业模板"]
---

# 📝 阶梯作业模板 (李宏毅-CMU 模式)

> 🎯 **作业目标**：通过分级 Baseline 实战与阶梯考题，独立实现或跑通核心算法，并在自动化评测中达到最高标准。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code / 笔记本**：`03-Projects/projects-{{course_id}}/{{hw_id}}_starter.ipynb`
- **数据集 / 样例**：`03-Projects/data/{{hw_id}}_data/`
- **开源标杆仓库**：[{{repo_name}}]({{repo_url}})
- **核心依赖**：`PyTorch` / `scikit-learn` / `numpy` / `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 Metric / 验收标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline (入门基础)** | 跑通流程 / 基础指标达成 | 掌握核心 API，使用 Baseline 模板完成基本预测或手算基础例题。 |
| 🟡 **L2 - Medium Baseline (进阶巩固)** | 指标提升 / 模块推导 | 引入特征工程 / 调参 / 手写核心步序（如前向传播、学习率衰减等）。 |
| 🔴 **L3 - Strong Baseline (高写实战)** | 手撕底层算法 | **从零手撕核心组件**（如手写 Transformer、Malloc、卡尔曼滤波、凸优化内点法）。 |
| 👑 **L4 - Boss Baseline (极客拓展)** | 极致性能 / 形式化证明 | 在 Kaggle / Top 竞赛中冲榜，或在 Lean 4 / Coq 中完成定理形式化证明。 |

---

## 3. 🧪 自动化测试与自测 Harness (Auto-Validation)

### 代码自测 Harness (PyTest)
在项目根目录下运行自测脚本：
```bash
pytest 03-Projects/projects-{{course_id}}/tests/test_{{hw_id}}.py
```

```python
# test_{{hw_id}}.py 校验模板
import pytest
import numpy as np

def test_algorithm_precision():
    # 与 scipy/torch 参考接口做断言比对
    ref_output = reference_solution(inputs)
    my_output = my_solution(inputs)
    np.testing.assert_allclose(my_output, ref_output, atol=1e-5)
```

---

## 4. 📝 错题复盘与误区记录

- **误区 1**：
- **坑点 2**：

---

## 🃏 Anki 卡片 (复盘与卡片导出)

- Q: {{Anki 问题描述}}
- A: {{Anki 答案与核心推导}}
