---
type: project
project_type: homework
course: "随机过程"
assignment_id: "SP-L04"
assignment_level: lesson
assignment_format: problem-set
stage_id: "03"
requires: ["[[随机过程-布朗运动反射原理与二次变差]]", "[[随机过程-鞅停时与可选停止]]", "[[随机过程-鞅不等式与收敛]]"]
source_type: local_integration_task
source: "本地原创题集；知识顺序参考 MIT 15.070J Lectures 6–12"
source_url: "https://ocw.mit.edu/courses/15-070j-advanced-stochastic-processes-fall-2013/pages/lecture-notes/"
license: "本地原创任务；MIT OCW link-only"
created: 2026-08-08
updated: 2026-08-08
status: planned
flow: project
tags: [作业, 随机过程, Brownian运动, 鞅, 停时]
---

# 随机过程｜课后作业 04：Brownian、鞅与停时

## 学习目标

把 Brownian 路径事件、鞅条件和停时条件放在同一份证据链中：先推导，再模拟，最后说明模拟不能替代哪一步证明。

## 任务边界与环境

- Python 3.11+，仅使用标准库；工作目录为 `03-Projects/24-随机过程/`。
- 可导入 `scripts/stochastic_process_lab.py` 的参考函数，但推导必须独立完成。
- 所有模拟记录随机种子、路径数、网格数与阈值；不得通过反复换种子挑选漂亮结果。
- 不使用可选停止时，先写采用的定理版本和逐项条件。

## 题目

### Q1｜Brownian 最大值与二次变差（25 分）

对标准 Brownian 运动和 $T=1$：

1. 从反射原理推导 $P(\sup_{s\le T}W_s\ge a)$，并取 $a=0.75$ 给出数值表达式。
2. 解释离散网格最大值为什么向下偏估连续时间最大值。
3. 计算等距网格平方增量和的期望与方差，并说明其收敛模式。
4. 区分二次变差、总变差和终点方差，分别写出它们的对象与结论。

### Q2｜鞅与可选停止（30 分）

简单对称随机游走从 $i=3$ 出发，在首次到达 $0$ 或 $N=10$ 时停止。

1. 验证 $S_n$ 与 $S_n^2-n$ 都是相对于自然滤过的鞅。
2. 证明停止时间满足本题采用的可选停止条件。
3. 推导命中 10 的概率与期望停止步数。
4. 给出一个条件不成立时不可直接套用结论的反例，并点名失败条件。

### Q3｜最大不等式与收敛条件（20 分）

1. 写出 Doob 非负次鞅最大不等式，并用首次越界停时给出证明骨架。
2. 比较“非负上鞅”“$L^p$ 有界鞅”和“一致可积鞅”的收敛结论。
3. 构造或引用一类 $L^1$ 有界但不一致可积的随机变量族，解释尾部质量如何逃逸。
4. 对每个结论写明 a.s.、$L^1$ 或 $L^p$ 中的哪一种收敛。

### Q4｜理论—模拟双证据（25 分）

调用并审计：

```python
from stochastic_process_lab import simulate_brownian_maximum, simulate_gamblers_ruin
```

1. 对 Brownian 最大值使用网格数 `50, 200, 800`，每档至少 5,000 条路径，比较理论概率和经验概率。
2. 对赌徒破产使用种子 `20260808, 20260809, 20260810`，每个种子至少 10,000 次试验。
3. 报告网格偏差、Monte Carlo 波动和理论公式各自解决的问题。
4. 保存一项与理论偏差最大的真实结果，不得删除。

## 提交产物

```text
submission/SP-L04/
├── answers.md
├── run_brownian_martingale.py
├── reflection-results.csv
├── stopping-results.csv
└── run.log
```

## 100 分 Rubric

| 维度 | 分值 | 通过证据 |
| :--- | ---: | :--- |
| Brownian 路径事件 | 25 | 反射、网格偏差和二次变差无混淆 |
| 鞅与停时证明 | 30 | 滤过、可积性和停止条件完整 |
| 不等式与收敛 | 20 | 定理版本、收敛模式和尾部边界正确 |
| 模拟审计 | 15 | 多网格、多种子和误差来源齐全 |
| 复现与失败记录 | 10 | 命令、原始输出和最大偏差结果保留 |

## 提示、硬失败与自检

- **必要提示**：先在有限停止时间 $n\wedge\tau$ 上使用鞅结论，再说明如何令 $n\to\infty$。
- **硬失败**：不写滤过；把离散最大值当连续最大值；只凭模拟声称证明可选停止；删除异常结果。
- **提交前自检**：每个等号是否有对应条件？每个概率估计是否带路径数、网格和种子？

通过线为 80/100 且无硬失败。完成后进入[[随机过程-阶段作业-03-Brownian鞅与停时双证据]]。

