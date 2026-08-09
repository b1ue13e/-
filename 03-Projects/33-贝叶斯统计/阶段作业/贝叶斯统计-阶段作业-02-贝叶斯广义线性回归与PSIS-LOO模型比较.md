---
type: project
project_type: homework
course: "贝叶斯统计"
assignment_id: "贝叶斯统计-阶段02"
assignment_level: stage
assignment_format: project
stage_id: "04"
requires:
  - "[[贝叶斯统计-广义线性回归与先验正则化]]"
  - "[[贝叶斯统计-信息准则与模型比较]]"
source_type: local_integration_task
created: 2026-08-08
status: ongoing
flow: project
tags: [作业, 阶段作业, 贝叶斯统计, GLM, PSIS-LOO, WAIC]
---

# 贝叶斯统计-阶段作业-02-贝叶斯广义线性回归与PSIS-LOO模型比较

> 所属阶段：[[04-决策与实践/🧭 阶段4-决策与实践|阶段4：决策与实践]]

---

## 1. 学习目标与任务定位
1. **构建二项 Logit / 泊松贝叶斯广义线性模型 (GLM)**，接入多维业务特征；
2. **应用高斯先验与马蹄先验正则化**，控制高维参数估计方差；
3. **实现 PSIS-LOO-CV 与 WAIC 信息准则比较**，诊断帕累托形态参数 $\hat{k}$ 离群点。

---

## 2. 任务边界与真实数据源
- **任务规模**：阶段综合实验（`stage` 规模）；
- **数据源路径**：`03-Projects/33-贝叶斯统计/data/marketing_sales.csv`；
- **核心实现代码**：`03-Projects/33-贝叶斯统计/scripts/bayes_glm_loo.py`；
- **自动化测试代码**：`03-Projects/33-贝叶斯统计/tests/test_bayes_glm_loo.py`。

---

## 3. 详细实验任务清单

### 任务 1：贝叶斯 Logistic 回归拟合
加载 `data/marketing_sales.csv`，以 `conversions` 为分子、`trials` 为总试验次数：
1. 选取 `channel_spend` 与 `traffic_quality` 为协变量，构建设计矩阵 $X$；
2. 设定先验分布 $\boldsymbol{\beta} \sim \mathcal{N}(0, 2.5^2 I)$；
3. 通过 MAP 估计与拉普拉斯逆海森矩阵获得后验均值与协方差，抽取 500 个后验参数样本。

### 任务 2：逐点对数似然矩阵与 WAIC 计算
1. 编写向量化函数计算逐点对数似然矩阵 `log_lik[S, N]`；
2. 计算对数后验预测密度 $\text{lppd}$ 与有效参数惩罚项 $p_{\text{WAIC}}$；
3. 给出模型的最终 $\text{WAIC} = -2(\text{lppd} - p_{\text{WAIC}})$ 得分。

### 任务 3：PSIS-LOO 帕累托平滑与 $\hat{k}$ 诊断
1. 对每个观测样本点计算留一重要性权重 $r_i^{(s)} = \exp(-\text{log\_lik}[s, i])$；
2. 拟合广义帕累托分布估计各样本点的 $\hat{k}$ 值；
3. 检查是否有 $\hat{k} > 0.7$ 的高杠杆离群点，并输出 `elpd_loo` 估计值。

### 任务 4：先验敏感性分析与稳健性压力测试 (Prior Sensitivity Analysis)
1. 对比三种先验假设：**弱信息先验 $\mathcal{N}(0, 2.5^2)$** vs **过度扩散先验 $\mathcal{N}(0, 100^2)$** vs **强正则化先验 $\mathcal{N}(0, 0.5^2)$**；
2. 观察极宽先验在小样本高维特征下是否触发 Logistic 分离 (Separation) 现象；
3. 记录不同先验下后验几率比 (Odds Ratio) 与 `elpd_loo` 的波动幅度，撰写 200 字先验稳健性诊断总结。

---

## 4. 提交产物清单
1. `scripts/bayes_glm_loo.py` 中模块化的高效 GLM、WAIC 与 PSIS-LOO 实现；
2. `tests/test_bayes_glm_loo.py` 自动化单元测试执行通过日志；
3. 包含模型参数不确定性区间与样本外泛化能力对比的完整评估报告。

---

## 5. 验收标准与 Rubric
- **优秀 (18–20分)**：GLM 构建标准，逐点对数似然矩阵计算精确，PSIS-LOO 与 WAIC 结果一致，$\hat{k}$ 诊断结论明确；
- **合格 (16–17分)**：完成回归拟合与基本 WAIC 计算；
- **需改进 (<16分)**：逐点似然维度混淆，或未完成 PSIS-LOO 帕累托平滑。

---

## 6. 引导与自检
- [ ] 检查 `sigmoid` 函数是否加入对数值截断（如 `np.clip(z, -30, 30)`）以防止 `exp` 溢出；
- [ ] 验证所有样本点的帕累托形态参数 $\hat{k}$ 是否均满足 $\hat{k} \le 0.7$；
- [ ] 运行测试确认：`python -m unittest 03-Projects/33-贝叶斯统计/tests/test_bayes_glm_loo.py`。
