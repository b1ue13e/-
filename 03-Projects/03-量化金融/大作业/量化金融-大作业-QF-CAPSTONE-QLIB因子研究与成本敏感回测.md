---
type: project
project_type: homework
topic: "Qlib 因子研究与成本敏感回测"
course: "量化金融"
assignment_id: "QF-CAPSTONE-QLIB"
assignment_level: capstone
assignment_format: project
stage_id: "04"
requires: ["[[回测框架与无泄漏实验]]", "[[时间序列验证]]", "[[因子预处理：去极值、中性化与标准化 (Factor Preprocessing_ Winsorization, Neutralization & Z-Score)]]", "[[策略评价指标]]", "[[PBO回测过拟合概率与Deflated Sharpe Ratio (Probability of Backtest Overfitting)]]", "[[Qlib回测工作流(Qlib Workflow)]]", "[[Implementation Shortfall 执行缺口与 Almgren-Chriss 最优执行模型]]"]
source_type: open_source_project_task
source_url: "https://github.com/microsoft/qlib"
license: "Qlib 代码 MIT；行情数据按来源单独核验"
package_path: "scripts/assignments/QF-CAPSTONE-QLIB/qlib_factor_research"
contract_data_path: "data/smoke/qlib_factor_research"
environment_path: "Qlib因子研究/environment-qlib.yml"
estimated_hours: "24-40"
created: 2026-08-07
updated: 2026-08-07
status: planned
flow: project
tags: [作业, 项目, 量化金融, Qlib]
---
# 量化金融-大作业-Qlib 因子研究与成本敏感回测

## 学习目标

- 用相同股票池、时间切分、组合规则和成本比较 E0 等权、E1 朴素因子和 E2 Qlib LightGBM Alpha158。
- 把“契约通过”“qrun 执行通过”“样本外研究通过”分成三种证据状态。
- 交付第三方可复跑的环境锁、数据 manifest、配置、日志、测试和失败结果。

## 任务边界

- 项目内 smoke 只验证完整配置模板结构；由于 `provider_uri` 是占位值，必须输出 `contract_template_ready`、`provider_status: placeholder` 和 `qlib_execution_status: blocked_on_provider`。
- 真正执行必须在锁定环境中调用 `qrun`；未安装 Qlib、provider 不存在或数据许可未知时状态为 `blocked`。
- 不提供行情，不把配置文件中的 `LightGBM/Alpha158` 字符串当成模型已经运行。

## 固定入口与环境

```powershell
Set-Location "F:\-\03-Projects\金融与时序\03-量化金融"
python scripts\assignments\generate_smoke_data.py
python scripts\assignments\QF-CAPSTONE-QLIB\qlib_factor_research\starter\run.py --input-dir data\smoke\qlib_factor_research --output-dir submissions\QF-CAPSTONE-QLIB\contract
conda env create -f Qlib因子研究\environment-qlib.yml
conda activate qf-qlib-0.9.7
```

contract preflight 通过后，复制并修改 `workflow_config.yaml`：替换 provider URI、数据 release、许可、市场、基准和真实时间段，再执行：

```powershell
python scripts\assignments\QF-CAPSTONE-QLIB\qlib_factor_research\starter\run_qlib.py --config submissions\QF-CAPSTONE-QLIB\workflow_config.yaml --output-dir submissions\QF-CAPSTONE-QLIB\qrun
```

## 题目细化

### S1 环境与数据契约（15 分）

冻结 Python、pyqlib 版本、Qlib commit、provider URI、数据 release、许可、校验值、股票池和交易日历。任何未知项保持 `blocked`。

### S2 三条可比基线（25 分）

在同一 train/valid/test、标签、股票池、组合规则和成本下运行 E0、E1、E2。保存预测、持仓、gross/net/benchmark 序列和全部失败配置。

### S3 无泄漏与选择审计（25 分）

验证特征可得时间、标签终点、执行延迟和测试集隔离；加入一个故意泄漏负例，并为候选模型提供 PBO/DSR 所需完整矩阵。

### S4 成本、消融与失败复盘（20 分）

至少运行零成本/基准成本/压力成本三档，以及一个特征或模型消融。失败结果不得删除，最佳结果不得单独展示。

### S5 第三方复现与答辩（15 分）

由第三方从环境文件开始复跑，记录命令、退出码、运行时间和产物哈希；完成 10 分钟答辩，解释失败边界而非只报收益。

## 提交产物

```text
submissions/QF-CAPSTONE-QLIB/
├── README.md
├── environment-qlib.yml
├── qlib_manifest.json
├── workflow_config.yaml
├── baseline_protocol.json
├── src/
├── tests/
├── qrun/qrun.evidence.json
├── artifacts/gross_net_benchmark.parquet
├── artifacts/experiment_matrix.csv
└── report.md
```

## 公开验收断言

```python
assert template_contract_status == "contract_template_ready"
assert template_provider_status == "placeholder"
assert template_execution_status == "blocked_on_provider"
assert qrun_execution_status == "passed"
assert qrun_returncode == 0
assert train_end < valid_start <= valid_end < test_start
assert np.allclose(net, gross - cost)
assert negative_leakage_test_failed is True
assert failed_experiments_are_preserved is True
```

## 引导自检

- [ ] 当前证据是 contract、真实 qrun，还是样本外研究？
- [ ] E0/E1/E2 是否共享数据、测试区间、组合和成本？
- [ ] 测试集是否完全未参与模型、阈值和超参数选择？
- [ ] 数据许可、release 和哈希是否与代码许可证分开记录？

## 失败诊断

| 现象 | 优先检查 |
| :--- | :--- |
| contract ready 但没有结果 | 这是正常状态，继续执行 `run_qlib.py`，不得伪报通过 |
| `qrun` 找不到 provider | 环境、provider URI、region 和数据 release |
| E2 结果异常优秀 | 标签泄漏、股票池变化、成本和测试集选择 |
| 第三方无法复跑 | 环境锁、相对路径、数据 manifest 和随机种子 |

## 验收标准

contract 与真实 qrun 两阶段都通过；三条基线同口径；泄漏负例失败；成本压力和消融齐全；第三方复现成功。缺真实 provider 或许可时只能标 `blocked`，不能用 contract smoke 替代。

## 失败条件

- 只检查配置字符串就声称 Qlib 已运行；
- 缺少 qrun 退出码、训练日志、预测或回测产物；
- 测试集参与选择，或只保留最优实验；
- 行情来源、许可、版本或校验值未知却标记完成。

## 评分量表

| 维度 | 分值 | 判据 |
| :--- | ---: | :--- |
| 环境与数据契约 | 15 | 版本、许可、provider、时间和哈希完整 |
| 基线可比性 | 25 | E0/E1/E2 同数据、同成本、同测试段 |
| 泄漏与选择审计 | 25 | 时间协议、负例和候选矩阵完整 |
| 成本与失败复盘 | 20 | 压力、消融和失败结果保留 |
| 第三方复现 | 15 | qrun 证据、环境锁和答辩可复核 |

## 来源与答案边界

Qlib 代码来自 Microsoft Qlib MIT 仓库；workflow 结构遵循官方 `qrun` 文档。本题是本地工程任务，不冒充官方 Qlib 示例或真实市场验证。
