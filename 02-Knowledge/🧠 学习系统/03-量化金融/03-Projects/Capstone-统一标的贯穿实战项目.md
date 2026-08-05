---
title: "Capstone-统一标的贯穿实战项目"
type: project
topic: "AAPL 贯穿式量化研究"
created: 2026-08-04
updated: 2026-08-05
status: active
progress: 60%
progress_basis: "Phase 1 可执行；Phase 2 CAPM/GARCH/VaR 与 Phase 3 BSM 构件可执行但尚未统一接入 AAPL 数据；Phase 4 未实现"
tags: [项目, 量化金融, 实战, AAPL]
flow: project
kind: moc
prerequisites: ["收益率与对数收益率", "OHLCV字段清洗与复权", "样本泄漏"]
related: ["Black-Scholes 期权定价模型", "量化金融-波动率-GARCH家族模型"]
source: "公开行情数据；来源与下载时间必须由提交者记录"
---

# Capstone：AAPL 贯穿式量化研究

> [!info] 路径位置
> 本项目是 [[🗺️ 量化金融学习路径#Week 0-9 必修路线|Week 9]] 的整合验收；主线未到 Week 9 时只运行当周指定构件，不提前做全项目。

> [!important] 项目目标
> 本项目不是预测 AAPL 下一次涨跌，而是证明你能把同一份研究对象按“数据 → 基线 → 统计模型 → 定价 → 报告”逐步升级，并保证每一步可复现、无前视、可被失败测试推翻。

## 1. 当前可执行状态

| 阶段 | 状态 | 可执行入口 | 完成证据 |
| :--- | :---: | :--- | :--- |
| Phase 1 数据与无泄漏基线 | **可执行** | [[03-Projects/Capstone-AAPL/README]] | 测试、指标 JSON、权益曲线 CSV |
| Phase 2 CAPM、GARCH 与 VaR | **部分可执行** | [[03-Projects/HW01-CAPM/README\|CAPM]]、[[03-Projects/Phase2-GARCH/README\|GARCH]]、[[03-Projects/HW06-DynamicVaR/README\|动态 VaR]] | 各构件可运行；统一 AAPL 数据清单尚待接通 |
| Phase 3 Black–Scholes 与对冲 | **部分可执行** | [[03-Projects/HW05-BSM/README\|HW05 BSM 实验包]] | 定价测试、蒙特卡洛、离散对冲误差 |
| Phase 4 订单簿微观结构 | 选修且数据受限 | 本页任务清单 | 数据许可、字段字典、盘口指标 |

不得把“规格已定义”写成“项目已完成”。只有可执行入口、输入样例、测试与产物齐全后，阶段状态才能改为“可执行”。

## 2. 统一数据协议

所有阶段共享以下研究清单：

| 字段 | 要求 | 拒绝条件 |
| :--- | :--- | :--- |
| `date` | 唯一、严格升序、标明时区或明确为交易日日期 | 重复、倒序、混合时区 |
| `adj_close` | 正数、无缺失、复权口径有来源说明 | 非正数、静默填充、口径不明 |
| 数据来源 | 记录提供方、下载时间、代码或查询参数 | 手工粘贴且无法复现 |
| 研究区间 | 训练、验证、测试边界预先冻结 | 看完测试结果后改边界 |
| 时间协议 | `feature_time <= signal_time < execution_time` | 同一收盘后生成信号又按该收盘成交 |

若在线数据源不可用，Phase 1 使用包内确定性演示数据完成工程验收；演示结果只能证明代码工作，不能写成 AAPL 实证结论。

## 3. Phase 1：数据与无泄漏基线

### 输入

- CSV 至少包含 `date, adj_close`。
- 推荐真实研究区间不少于 5 年；演示模式由脚本生成确定性价格序列。
- 快慢均线窗口、交易成本基点数必须在运行前写入参数。

### 必做任务

- [ ] 运行数据契约检查：缺失、重复、倒序、非正价格均应失败。
- [ ] 用 $t$ 日收盘数据生成信号，持仓至少滞后一交易期。
- [ ] 报告累计收益、最大回撤、年化波动率、换手与成本假设。
- [ ] 修改最后一个未来价格，确认过去持仓与过去收益不变化。
- [ ] 保存 `metrics.json` 和 `equity_curve.csv`。

### 验收

```powershell
cd "03-Projects/Capstone-AAPL"
python -m unittest discover -s tests -v
python src/phase1_baseline.py --output artifacts
```

通过标准：测试全绿；产物存在；能够解释 `position = signal.shift(1)`；演示数据不得冒充真实 AAPL。

## 4. Phase 2：CAPM 与 GARCH

### 输入

- AAPL 与市场代理的同频、同交易日收益率；市场代理选择需说明。
- 时间切分沿用 Phase 1，不得因模型结果重新选择。

### 必做任务与产物

- [ ] OLS 估计 Beta 与 Alpha，报告标准误、残差诊断和样本区间。
- [ ] 明确市场代理不是“真实市场组合”，解释结论边界。
- [ ] 运行 [[03-Projects/HW01-CAPM/README|HW01 CAPM 实验包]]。
- [ ] 运行 [[03-Projects/Phase2-GARCH/README|Phase 2 GARCH 实验包]] 的测试与演示命令。
- [ ] GARCH(1,1) 报告 $\omega,\alpha,\beta$、收敛状态与 $\alpha+\beta$。
- [ ] 只在样本外评价一天期波动率预测，并与滚动标准差基线比较。
- [ ] 运行 [[03-Projects/HW06-DynamicVaR/README|HW06 动态 VaR 实验包]]，比较参数法与历史法覆盖率。
- [ ] 产出 `phase2_metrics.json`、诊断图和一页结论。

失败处理：若残差或模型诊断不通过，保留失败日志，回到 [[单位根检验与 ADF 检验 (Unit Root & Augmented Dickey-Fuller Test)]] 与 [[量化金融-波动率-GARCH家族模型]]，不得只换参数直到结果好看。

## 5. Phase 3：Black–Scholes 与离散对冲

### 输入

- 预先冻结的 $S_0,K,T,r,\sigma$；说明 $\sigma$ 来自历史估计还是市场隐含波动率。
- 欧式期权、分红和交易日计数约定。

### 必做任务与产物

- [ ] 闭卷重建 Delta 对冲到 PDE 的每一步。
- [ ] 用 [[Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)]] 的数值锚点测试公式。
- [ ] 运行 [[03-Projects/HW05-BSM/README|HW05 BSM 实验包]] 的测试与实验命令。
- [ ] 与蒙特卡洛价格比较，报告随机误差和置信区间。
- [ ] 模拟日频与周频离散 Delta 对冲，比较对冲误差。
- [ ] 至少加入一种摩擦：手续费、买卖价差或波动率错设。

失败处理：若闭式解、蒙特卡洛与测试锚点不一致，先冻结随机种子和输入，逐项检查贴现、$d_1/d_2$、到期单位与正态分布参数。

## 6. Phase 4：订单簿微观结构（选修）

只有获得合法、可追溯的逐笔或订单簿数据后才启动。日线 OHLCV 不能伪装为 L2/L3 数据。

- [ ] 记录数据许可、市场、时区、撮合规则与字段字典。
- [ ] 计算买卖价差、盘口不平衡和成交概率，并给出缺失/撤单处理。
- [ ] 比较至少一个朴素基线；禁止从单日样本推断稳定 Alpha。

## 7. 100 分 Rubric

| 维度 | 分值 | 硬性证据 |
| :--- | :---: | :--- |
| 数据可复现 | 20 | 来源、下载参数、数据契约、切分冻结 |
| 方法正确 | 25 | 公式/实现测试、无前视时间协议 |
| 基线比较 | 20 | 简单基线与新增方法同口径比较 |
| 评估与失败案例 | 20 | 样本外结果、至少一个故意失败测试 |
| 报告与边界 | 15 | 一页结论、限制、不可外推范围 |

**通过线**：总分不低于 75，且“方法正确”不低于 18；代码不能运行或存在已知前视时直接不通过。

## 8. 最终提交清单

```text
submission/
├── README.md
├── environment.txt
├── data_manifest.json
├── src/
├── tests/
├── artifacts/
│   ├── metrics.json
│   └── equity_curve.csv
├── failure_log.md
└── report.md
```

- [ ] 新环境可按 README 复现。
- [ ] 测试包含正常案例与失败案例。
- [ ] 结果表区分演示数据、真实数据和样本外数据。
- [ ] 报告说明没有证明未来盈利。
