---
title: "变分推断与MCMC采样求解器"
type: project
project_type: homework
topic: "变分推断与MCMC采样求解器"
course: "14-概率图模型"
assignment_id: "概率图模型-阶段作业-02"
assignment_level: stage
assignment_format: lab
stage_id: "2"
requires:
  - "[[概率图模型-变量消去]]"
  - "[[概率图模型-和积算法与消息传递]]"
  - "[[概率图模型-Gibbs与MH采样]]"
  - "[[概率图模型-MCMC收敛与诊断]]"
  - "[[概率图模型-变分推断与ELBO]]"
  - "[[概率图模型-KL散度]]"
source_type: local_integration_task
created: 2026-07-29
updated: 2026-08-06
date: 2026-07-29
status: planned
flow: project
difficulty: advanced
concept: ["概率图模型", "MCMC采样", "变分推断"]
adapted_from: "Stanford CS228 HW 结构启发（本地原创任务规格）"
source_url: "https://ermongroup.github.io/cs228-notes/"
license: "本地原创改编；外部素材 link-only"
tags: [作业, 14-概率图模型, 推断]
---

# 概率图模型 - 阶段作业 02：变分推断与 MCMC 采样求解器

> 🎯 **作业目标**：手写变量消去法 (Variable Elimination)、Metropolis-Hastings / Gibbs 采样，以及变分自编码器 (VAE) 中的变分推断。

---

## 0. 🎯 学习目标

完成后能够证明：

1. **精确推断**：手写变量消去算法（因子乘积/边际化），并与 pgmpy 复核一致；
2. **采样推断**：实现 Gibbs 与 Metropolis-Hastings 采样器，收敛诊断 $\hat R < 1.05$；
3. **变分推断**（可选挑战）：实现 VAE 的均值场变分推断与重参数化，ELBO 收敛；
4. **一致性**：对同一查询比较精确/采样/变分三种结果，能解释差异来源。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/14-概率图模型/scripts/hw02_verify.py`（本作业最小参考实现/验收脚本；完整任务由学习者独立实现，不提供现成答案）
- **开源标杆仓库**：[ermongroup/cs228-notes](https://github.com/ermongroup/cs228-notes) (Stanford CS228)
- **核心依赖**：`pgmpy`, `torch`, `numpy`, `pytest`

---

## 2. 🎯 基础 / 进阶 / 综合任务设计

| 任务级别 | 目标 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **基础任务** | 条件独立性校验正确 | 构建简单的 Bayesian Network，手算并用 `pgmpy` 验证 $D$-分离 ($d$-separation) 独立性。 |
| 🟡 **进阶任务** | 边缘分布计算无误 | **手写 Variable Elimination (变量消去法)** 算法，计算因子乘积 (Factor Product) 与消去。 |
| 🔴 **综合任务** | 采样收敛 $\hat{R} < 1.05$ | **手写 Gibbs Sampling 与 Metropolis-Hastings 采样器**，求解隐马尔可夫模型 (HMM) 维特比解码。 |
| 👑 **可选挑战** | ELBO 优化收敛 | 手写 Variational Autoencoder (VAE)，实现 Mean-field 变分推断与 Reparameterization Trick 重参数化。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_variable_elimination_marginal():
    from pgm_solvers import factor_product, factor_marginalize
    # 构造测试 Factor
    phi_A = np.array([0.6, 0.4]) # P(A)
    phi_BA = np.array([[0.8, 0.2], [0.3, 0.7]]) # P(B|A)
    
    # 边际化消去 A 得到 P(B)
    P_B = np.dot(phi_A, phi_BA)
    assert np.isclose(P_B.sum(), 1.0)
    assert np.isclose(P_B[0], 0.6*0.8 + 0.4*0.3)
```

---

## 4. 任务背景与边界

- **问题场景**：给定一个固定的离散 Bayesian Network（含 5–8 个节点），你需要分别用精确推断（变量消去）、采样推断（Gibbs / MH）和变分推断（可选 VAE 挑战）求出指定查询的边缘/后验分布，并对三者结果做一致性比较。
- **输入与假设**：网络结构与 CPD 由本作业自带的 Starter 数据提供；所有实现必须支持任意消元顺序输入。
- **禁止事项**：不得直接调用 `pgmpy` 的推断 API 作为主实现（仅用于复核）；不得使用未声明的第三方推断库。
- **环境**：Python 3.11+，依赖 `pgmpy`、`numpy`、`pytest`（VAE 挑战需 `torch`）；随机种子固定为 42。

## 5. 提交产物

1. `pgm_solvers.py`：因子运算（乘积、边际化）与变量消去实现；
2. `samplers.py`：Gibbs 与 Metropolis-Hastings 采样器实现；
3. 自动化测试运行日志（`pytest -v` 输出）；
4. 一致性比较报告：精确 vs 采样（含 $\hat{R}$ 收敛诊断与样本量敏感性）；
5. （可选挑战）VAE 训练曲线与 ELBO 收敛图。

## 6. 验收标准与 Rubric

| 维度 | 分值 | 通过要求 |
|:---|---:|:---|
| 正确性（因子运算与消去） | 30 | 与 `pgmpy` 复核一致，pytest 全绿 |
| 采样器实现与收敛诊断 | 30 | $\hat{R} < 1.05$，稀有证据案例分析 |
| 一致性比较与报告 | 25 | 明确精确/采样差异来源，边界结论 |
| 代码质量与可复现性 | 15 | 种子固定、依赖清单、运行步骤完整 |
| **总计** | **100** | **≥ 75 且正确性 ≥ 24** |

## 7. 引导与自检

- **检查点 1**：手算 2 节点网络（如 $A \to B$）的变量消去结果，再与代码输出比对。
- **检查点 2**：对同一查询分别用拒绝采样和 Gibbs，观察收敛速度差异，记录混合失败的迹象。
- **常见失败模式**：因子乘积忘记归一化、采样链 burn-in 不足、消元顺序导致中间因子过大。
- **提交前清单**：pytest 通过、种子固定、报告含失败案例、依赖版本已记录。

## 8. 知识依赖与后续

- 本作业依赖阶段 2 知识卡：变量消去、和积算法、MH 采样、Gibbs 采样、MCMC 收敛、ELBO、KL 散度（见 frontmatter `requires`）。
- 完成后进入阶段 3（学习算法），并可衔接课程 Capstone「结构、推断与采样一致性审计」。

## 🃏 Anki 卡片

- Q: 在变分推断 (Variational Inference) 中，证据下界 (ELBO) 表达式 $\text{ELBO}(q) = \mathbb{E}_{q(z)}[\log p(x,z)] - \mathbb{E}_{q(z)}[\log q(z)]$ 与真实边缘似然 $\log p(x)$ 之间满足什么几何关系？
- A: $\log p(x) = \text{ELBO}(q) + \text{KL}(q(z) \parallel p(z|x))$。因为 KL 散度是非负的 ($\text{KL} \ge 0$)，所以 ELBO 始终是真实数据边际似然 $\log p(x)$ 的下界。最大化 ELBO 等价于最小化变分后验 $q(z)$ 与真实后验 $p(z|x)$ 之间的 KL 散度。
