---
type: project
project_type: homework
course: "贝叶斯统计"
assignment_id: "贝叶斯统计-02"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires:
  - "[[贝叶斯统计-马尔可夫链蒙特卡洛与Metropolis-Hastings算法]]"
  - "[[贝叶斯统计-MCMC收敛诊断与采样质量评估]]"
source_type: open_textbook_exercise
created: 2026-08-08
status: ongoing
flow: project
tags: [作业, 课后作业, 贝叶斯统计, MCMC, 手写采样器]
---

# 贝叶斯统计-课后作业-02-Metropolis-Hastings采样器手写实现与诊断

> 所属阶段：[[02-计算贝叶斯/🧭 阶段2-计算贝叶斯|阶段2：计算贝叶斯]]

---

## 1. 学习目标与任务定位
1. **纯手写实现** 1 维/多维 Random-Walk Metropolis-Hastings (M-H) 采样器；
2. **深刻掌握细致平衡条件与接受率**在数值代码中的对数空间（Log-space）防溢出处理；
3. **独立实现多链并行运行与收敛诊断**，计算经典 Gelman-Rubin $\hat{R}$ 与现代秩归一化折叠 $\hat{R}$。

---

## 2. 任务边界与依赖环境
- **任务规模**：编程实验题（`lesson` 规模）；
- **执行环境**：Python 3.10+，纯 NumPy 与 SciPy，禁止直接调用 PyMC 或 Stan 的黑盒采样器；
- **核心代码路径**：`03-Projects/33-贝叶斯统计/scripts/mh_sampler.py`；
- **自动化测试路径**：`03-Projects/33-贝叶斯统计/tests/test_mh_sampler.py`。

---

## 3. 详细实验题目

### 实验 1 (目标分布与手写 M-H 采样循环)
目标分布为非对称多峰高斯混合分布：
$$P(\theta) = 0.3 \cdot \mathcal{N}(-2.0, 1.0^2) + 0.7 \cdot \mathcal{N}(3.0, 0.5^2)$$
1. 编写 `target_mixture_gaussian_log_prob(x)` 函数，在对数空间计算目标密度；
2. 编写 `run_mh_chain(init_val, n_iter, proposal_std, seed)`，实现正态提议分布与 Metropolis 接受准则；
3. 统计不同提议步长（$\sigma = 0.1, 1.5, 10.0$）下的接受率，验证步长对链遍历效率的影响。

### 实验 2 (多链运行与严苛收敛诊断)
1. 选取 4 个分散的初始点（如 $[-4.0, -1.0, 2.0, 5.0]$），分别独立运行 4000 步采样；
2. 剔除前 1000 步预热样本，保留后 3000 步；
3. 编写 `compute_rank_normalized_r_hat(chains)` 与 `compute_ess(chains)` 函数；
4. 验证 4 条链混合良好，满足 $\hat{R} < 1.05$。

---

## 4. 提交产物清单
1. 位于 `scripts/mh_sampler.py` 的完整 Python 实现；
2. 位于 `tests/test_mh_sampler.py` 且通过全部断言的单元测试套件；
3. 控制台打印的真实接受率、$\hat{R}$ 与 ESS 输出日志。

---

## 5. 验收标准与 Rubric
- **优秀 (18–20分)**：对数计算防溢出严密，多链并行收敛良好，$\hat{R} < 1.05$，单元测试 100% 通过；
- **合格 (16–17分)**：完成单链与多链采样，正确计算 R-hat 指标；
- **需改进 (<16分)**：未处理对数数值下溢，或 R-hat 判决逻辑错误。

---

## 6. 引导与自检
- [ ] 检查在计算接受对数 `log_alpha = prop_lp - current_lp` 时是否避免了概率的直接相除；
- [ ] 验证 4 条链的初值是否足够分散，以避免所有链陷入同一个局部极值；
- [ ] 运行测试确认：`python -m unittest 03-Projects/33-贝叶斯统计/tests/test_mh_sampler.py`。
