---
type: project
project_type: homework
course: "22-概率论与数理统计"
assignment_id: "Stat-Stage02"
assignment_level: stage
assignment_format: project
stage_id: "03"
requires: ["[[概率统计-参数区间估计与枢轴量法]]", "[[概率统计-经典参数假设检验：Z检验、t检验、卡方与F检验]]", "[[概率统计-似然比检验与拟合优度检验]]", "[[概率统计-方差分析ANOVA与单因素效应]]"]
source_type: open_textbook_exercise
source_url: "https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/"
created: 2026-08-09
status: completed
flow: project
tags: [作业, 概率论与数理统计, 阶段作业, 假设检验, ANOVA, 推断引擎]
---

# 概率统计-阶段作业-02-统计假设检验与ANOVA推断引擎

## 来源与改编说明

- **source_type**：`open_textbook_exercise` —— 本题依课程双理论 Spine 的习题口径融合改编，非官方原题照抄。
- **可追溯来源**：MIT 6.041SC Probabilistic Systems Analysis（Fall 2013，CC BY-NC-SA 4.0，见 `📚 教材挂载索引`）；对应 茆诗松《概率论与数理统计教程》（第3版）第 7–9 章（参数区间估计、参数假设检验、方差分析与线性回归），并衔接 OpenIntro IMS（2e）Ch 13–17、21–26（假设检验与回归）。
- **题号与页码**：[待验证] —— 具体教材题号/页码未逐题核对，不冒充官方原题；精确出处以对应 Spine 官方习题集为准。
- **本地化适配**：FDR 多重校正与 ANOVA 正交分解引擎为本课程本地设计，用于对齐已教授知识卡与跨阶段验收。

## 🎯 学习目标

整合第三阶段与第四阶段的核心假设检验与方差分析推断技术，从零实现包含单因素方差分析（ANOVA）平方和正交分解、多重假设检验错误发现率（FDR）控制的自动化推断计算引擎，输出标准科研统计报表。

---

## 1. 详细任务说明

### 任务 1（算法实现）：单因素方差分析（One-way ANOVA）推断引擎
- **理论模型**：设共有 $k$ 个处理组，第 $i$ 组观测值为 $Y_{ij} = \mu + \alpha_i + \epsilon_{ij}$，其中 $\epsilon_{ij} \overset{\text{i.i.d.}}{\sim} \mathcal{N}(0, \sigma^2)$，样本容量为 $n_i$（总样本量 $N = \sum n_i$）。
- **要求实现**：
  1. **平方和分解**：总平方和 $SST = \sum_{i=1}^k \sum_{j=1}^{n_i} (Y_{ij} - \bar{Y}_{\cdot\cdot})^2$、组间平方和 $SSB = \sum_{i=1}^k n_i (\bar{Y}_{i\cdot} - \bar{Y}_{\cdot\cdot})^2$、组内误差平方和 $SSW = \sum_{i=1}^k \sum_{j=1}^{n_i} (Y_{ij} - \bar{Y}_{i\cdot})^2$；
  2. **自由度与均方**：$df_B = k - 1, \; df_W = N - k$；$MSB = SSB / df_B, \; MSW = SSW / df_W$；
  3. **检验统计量与效应量**：$F = MSB / MSW \sim F(df_B, df_W)$，计算双侧 $p$ 值与效应量 $\eta^2 = SSB / SST$。

### 任务 2（算法实现）：Benjamini-Hochberg (BH) 多重检验 FDR 控制
- **理论背景**：当同时执行 $m$ 个假设检验时（如 ANOVA 后的各组两两事后对比），若不加控制，至少发生一次假阳性的全国家族错误率（FWER）将随 $m$ 呈指数上升（$1 - (1-\alpha)^m$）。
- **要求实现**：
  1. 输入原始 $p$ 值序列 $p_1, \dots, p_m$；
  2. 按照从小到大排序 $p_{(1)} \le p_{(2)} \le \dots \le p_{(m)}$；
  3. 寻找最大满足 $p_{(k)} \le \frac{k}{m} q^*$ 的秩 $k_{\max}$，拒绝前 $k_{\max}$ 个原假设；
  4. 计算单调保序的调整后 $p$ 值：$\tilde{p}_{(i)} = \min_{j \ge i} \left\{\min\left(1, \frac{m}{j} p_{(j)}\right)\right\}$。

---

## 2. 编程接口与 API 契约

请参考 `scripts/stats_solver.py` 中的函数实现与规范：

```python
def one_way_anova(groups: list[np.ndarray]) -> dict:
    """
    输入 k 个组别的样本数组列表
    返回包含 SST, SSB, SSW, df_between, df_within, MSB, MSW, F_stat, p_val, eta_squared 的字典
    """
    ...

def benjamini_hochberg_fdr(p_values: np.ndarray, alpha: float = 0.05) -> tuple[np.ndarray, np.ndarray]:
    """
    返回: (rejected_mask, adjusted_p_values)
    """
    ...
```

---

## 3. 提交产物清单

1. 包含 ANOVA 平方和正交分解证明（$SST = SSB + SSW$ 交叉项为零）的推导报告；
2. 包含可独立运行并通过 100% 单元测试的 Python 求解引擎源码；
3. 多组真实/模拟试验下的 ANOVA 输出报表与 FDR 事后检验对比。

---

## 4. 阶段验收评分标准（Rubric）

| 评分项 | 分值 | 满分标准 |
| :--- | :---: | :--- |
| **ANOVA 算法正确性** | 40 | 手写矩阵/向量化运算准确，平方和严格守恒，与 Scipy 官方库精度一致（$<10^{-5}$） |
| **FDR 多重校正实现** | 35 | BH 算法排序与调整后 p 值保序无误，有效控制名义错误发现率 |
| **工程质量与健壮性** | 25 | 支持不平衡样本（$n_i$ 不等），具备边界异常处理，通过 PyTest 自动化测试 |

---

## 5. 引导自检与检查点

- [ ] 平方和分解中加权项 $n_i$ 处理无误；
- [ ] 自由度总和满足 $df_{\text{Total}} = df_{\text{Between}} + df_{\text{Within}} = N - 1$；
- [ ] 运行 pytest 确保所有单元测试 100% 通过；
- [ ] 深刻说明 FDR 控制与传统 Bonferroni 控制在多重检验保守性上的核心区别。

## 6. 关联与导航

- 前置卡片：[[概率统计-经典参数假设检验：Z检验、t检验、卡方与F检验]]、[[概率统计-似然比检验与拟合优度检验]]、[[概率统计-方差分析ANOVA与单因素效应]]
- 返回作业索引：[[🧭 课程作业总索引]]
