---
type: project
project_type: homework
course: "量化金融"
assignment_id: "QF-L09"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[量化金融-随机过程-伊藤引理与随机微分方程]]", "[[量化金融-期权定价-Greeks与动态对冲]]"]
source_type: local_integration_task
source_url: "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/resources/mit18_s096f13_pset9/"
source_locator: "Problem Set 9: verification of SDE solutions and Vasicek model；discrete delta hedging is a local extension"
license: "本地原创题面；仅映射 MIT OCW SDE 能力目标，不复制官方解答"
estimated_hours: "7-9"
fixture_path: "scripts/assignments/lesson_fixtures.py::qf_l09_fixture"
created: 2026-08-07
updated: 2026-08-07
status: planned
flow: project
tags: [作业, 量化金融]
---
# 量化金融-课后作业-09-SDE 与动态对冲

## 作业定位

这是课后作业链的综合收口：先验证 SDE 解析解，再测量 Euler 离散误差，最后把 Delta 对冲写成逐笔现金与库存账本。对冲结果必须拆成离散化、交易成本和模型误设三类来源。

## 学习目标

- 用伊藤引理验证 GBM 与 Vasicek 解析解，并对照 Euler-Maruyama。
- 实现自融资离散 Delta 对冲账本，验证现金和库存更新。
- 用冻结参数比较重平衡频率、成本和波动率误设对终端误差的影响。

## 任务边界

- 使用合成风险中性路径，不使用真实期权或高频行情。
- 只对一份欧式看涨空头头寸做对冲，合约乘数固定为 1。
- 交易成本仅为按成交名义金额计的比例成本，不代表具体市场费率。
- 所有配置在运行前固定；不得根据 P/L 分布反向挑选波动率或频率。

## 固定输入

### SDE 误差实验

```text
GBM: S0=100, mu=0.06, sigma=0.20, T=1
Vasicek: r0=0.03, kappa=1.20, theta=0.04, sigma_r=0.015, T=1
n_paths=20000
steps={12, 52, 252}
seed=909
```

### Delta 对冲实验

```text
S0=100, K=100, r=0.02, q=0.00, sigma_model=0.20, T=1
n_paths=20000
rebalances={12, 52, 252}
cost_rate={0.0, 0.0005, 0.0010}
seed=909
```

模型误设场景固定为 `sigma_realized=0.25`、`sigma_hedger=0.20`；其余参数不变。

## 题目细化

### Q1 解析解与条件矩（20 分）

1. 用伊藤引理验证 GBM 解析解：
   $$
   S_t=S_0\exp((\mu-\tfrac12\sigma^2)t+\sigma W_t).
   $$
2. 推导 $E[S_T]$ 与 $Var(S_T)$。
3. 验证 Vasicek 解：
   $$
   r_t=\theta+(r_0-\theta)e^{-\kappa t}
   +\sigma_r\int_0^t e^{-\kappa(t-s)}dW_s.
   $$
4. 推导 Vasicek 的条件均值与方差，并说明 $\kappa>0$ 的作用。

### Q2 Euler-Maruyama 误差（20 分）

1. 对 GBM 在三种步数下使用相同路径的 Brownian 增量同时计算精确离散解与 Euler 解。
2. 报告终值 strong RMSE、均值误差、方差误差和 Euler 非正价格路径数。
3. 对 Vasicek 报告终值样本均值/方差与解析条件矩的误差。
4. 不要求误差在有限样本中严格单调；若不单调，保留结果并解释蒙特卡洛噪声。

### Q3 自融资 Delta 对冲账本（35 分）

以卖出一份欧式 call 为起点。每个路径必须按以下顺序记账：

1. `t=0`：收到 call 价格 $C_0$，买入 $\Delta_0$ 股，现金为 $B_0=C_0-\Delta_0S_0-cost_0$。
2. 每个重平衡点：先让现金账户按无风险利率增长，再用当前价格调整股票库存，并从现金中扣除交易金额和成本。
3. 到期：现金增长到 $T$，以终值价格计量库存，支付 option payoff。
4. 定义
   $$
   P\&L_T=B_T+\Delta_{T^-}S_T-(S_T-K)^+.
   $$
5. 对三种频率、三种成本共 9 个配置报告 P/L 均值、标准差、5%/50%/95% 分位数、平均换手和平均成本。
6. 至少抽取一条路径输出完整 ledger：`time/spot/delta/delta_trade/cash_before/cash_after/cost`。

### Q4 模型误设与归因（25 分）

1. 以 `sigma_realized=0.25` 生成路径，但所有定价与 delta 继续使用 `sigma_hedger=0.20`。
2. 与正确规格场景使用相同频率和成本表比较，不得重新校准 `sigma_hedger`。
3. 将结果按以下三类归因：离散重平衡、比例交易成本、波动率误设。
4. 写出至少两个无法从本合成实验外推到真实市场的因素，例如跳跃、波动率曲面、流动性或执行延迟。

## 提交产物

```text
submissions/QF-L09/
├── report.md
├── sde.py
├── delta_hedge.py
├── test_delta_hedge.py       # 至少 12 个测试
├── sde_errors.csv
├── hedge_summary.csv         # 9 个基准配置 + 误设配置
├── sample_ledger.csv
└── evidence/
    └── pytest.txt
```

## 公开验收断言

```python
assert set(hedge_summary["rebalances"]) == {12, 52, 252}
assert set(hedge_summary["cost_rate"]) >= {0.0, 0.0005, 0.0010}
assert (sample_ledger["cost"] >= 0).all()
assert np.allclose(
    sample_ledger["delta_trade"],
    sample_ledger["delta"].diff().fillna(sample_ledger["delta"]),
    atol=1e-12,
)
assert np.isfinite(hedge_summary.select_dtypes("number")).all().all()
```

## 引导自检

- [ ] 解析 SDE 条件和 Euler 递推分别写明，没有混用漂移。
- [ ] 精确解与 Euler 解在每条路径上复用同一 Brownian 增量。
- [ ] 对冲账本按“计息 -> 调仓 -> 扣成本”顺序执行。
- [ ] call 空头、股票库存和现金账户的符号保持一致。
- [ ] 误设场景只改变真实路径波动率，没有事后修改对冲模型。

## 失败诊断

| 现象 | 优先检查 |
| :--- | :--- |
| 无成本高频对冲误差很大 | delta 时点、现金计息、payoff 符号 |
| 成本为负 | 交易名义金额是否遗漏绝对值 |
| 频率越高成本反而总为 0 | `delta_trade` 是否被库存覆盖后再计算 |
| Euler 与精确解完全相同 | 是否错误地两次调用了同一精确公式 |
| Vasicek 均值远离解析值 | `theta` 项、指数衰减或噪声尺度 |

## 验收标准

- 两个 SDE 的解析推导与数值条件矩均完整。
- 三种步数的误差表保留全部结果和非正路径计数。
- 9 个对冲配置有完整账本、P/L、换手和成本指标。
- 模型误设结果与基准分开，归因不把合成实验包装为市场结论。

## 失败条件

- 对冲账本无法从逐笔记录复算终端 P/L。
- 在到期后才使用终值信息更新 delta。
- 成本未从现金扣除，或用收益百分比替代交易名义金额。
- 根据测试 P/L 重新选择 `sigma_hedger`、频率或种子。

## 评分量表

| 项目 | 分值 | 满分证据 |
| :--- | ---: | :--- |
| Q1 解析 SDE | 20 | GBM/Vasicek 验证和条件矩完整 |
| Q2 数值误差 | 20 | 三步数、共同噪声、四类误差完整 |
| Q3 对冲账本 | 35 | 9 配置、逐笔 ledger、P/L 和成本守恒完整 |
| Q4 误设归因 | 25 | 冻结模型、同表对照、三类归因和外推边界完整 |

总分 `>= 75`，且 Q3 不低于 `22/35` 才通过。

## 来源与答案边界

- 来源入口：[MIT 18.S096 Problem Set 9: Stochastic Differential Equations](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/resources/mit18_s096f13_pset9/)。
- 官方 Problem Set 9 覆盖 SDE 解验证与 Vasicek；Euler 误差和 Delta 对冲账本为本地课程扩展。
- 固定参数、成本模型、输出协议和 Rubric 为原创，不复制官方题面或答案。
