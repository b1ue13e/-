---
title: "HW17 - Qlib因子研究与成本敏感回测作业说明书"
type: project
topic: "Qlib因子研究与成本敏感回测"
course: "量化金融"
created: 2026-07-28
updated: 2026-07-31
status: active
progress: 0%
flow: project
kind: project
project_type: homework
asset_eligibility: eligible
eligibility_audited: 2026-07-31
focus: now
domain: quant-finance
sprint_id: 2026-S01-quant
difficulty_tier: T3
source_url: "https://github.com/microsoft/qlib"
source_course: "Microsoft Qlib"
source_version: "commit b87a2c294d364a33fb739359886acffe8ec907d1（与数据manifest对齐）"
source_commit: "b87a2c294d364a33fb739359886acffe8ec907d1"
license: "MIT"
mirror_policy: local-clone
adaptation: adapted
data_source_url: "https://github.com/chenditc/investment_data/releases/tag/2026-07-27"
data_source_release: "2026-07-27"
data_packaging_code_license: "Apache-2.0"
market_data_license: "source-specific"
market_data_terms: "底层行情来自多种数据源，使用范围与再分发条件需按各源条款单独核验"
dataset_version: "investment_data release 2026-07-27；以随包manifest校验"
starter_code: "Qlib官方examples/workflow_by_code.py与LightGBM benchmark配置"
tests: "本地pytest最小测试 + 无泄漏审计清单"
baseline: "朴素时序信号/等权对照 + Qlib LightGBM Alpha158"
acceptance_test: "可复现、无前视、含成本、样本外、能解释失败"
compute_budget: low
solution_visibility: private
tags: [项目, 实战作业, 量化金融, Qlib, 因子研究, 回测, 无泄漏]
---

# HW17：Qlib 因子研究与成本敏感回测

> 目标不是追求一个漂亮的历史收益数字，而是建立一条可复现、无前视、含成本、样本外可解释的量化研究链路。

## 1. 任务定义

使用 Qlib 串联数据、特征、模型、信号、组合、模拟执行和评估，完成：

1. 官方 LightGBM/Alpha158 工作流烟雾测试；
2. 不使用未来信息的朴素信号 Baseline；
3. 固定训练、验证、测试时间切分；
4. 同时报告 gross/net 策略收益、基准与超额收益；
5. 完成成本敏感性、无泄漏和失败案例审计。

## 2. 来源、版本与许可边界

| 项目 | 固定值/要求 |
|:---|:---|
| Qlib 官方仓库 | `https://github.com/microsoft/qlib` |
| Qlib 代码版本 | `b87a2c294d364a33fb739359886acffe8ec907d1` |
| Qlib 许可证 | MIT |
| 数据发布包 | `investment_data` release `2026-07-27` |
| 打包工具许可证 | Apache-2.0 |
| 底层行情 | 按每个原始数据源条款单独核验 |
| 答案可见性 | 只保存自己的代码与报告，不挂载他人完整答案 |

Qlib 的 MIT 许可证只覆盖 Qlib 代码；不自动覆盖底层行情数据的使用和再分发权利。

## 3. 数据协议与无泄漏约束

运行前必须冻结市场、股票池、数据频率、训练/验证/测试区间、基准、成交价格、佣金、印花税、最低费用与数据校验值。

硬约束：

- 三个时间区间不得重叠；
- 测试集不参与特征、模型或参数选择；
- 日期 `t` 形成的信号只能使用当时可得数据，并在预先声明的 `t+1` 或之后执行；
- 预处理、标准化和特征选择不得读取未来统计量；
- 复权、停牌、涨跌停、退市和股票池变更必须记录。

## 4. 执行阶段

| 阶段 | 内容 | 必交证据 |
|:---|:---|:---|
| T1 | 固定 commit、数据 release 和环境，跑通官方工作流 | manifest、lock file、日志 |
| T2 | 建立等权/基准与朴素时序信号 | Baseline 代码、IC/换手/收益证据 |
| T3 | Qlib LightGBM/Alpha158 含成本回测 | 配置、预测、gross/net 序列 |
| T4 | 特征、持仓数、调仓频率或成本的单变量消融 | 对比表、失败案例、结论边界 |

## 5. Baseline 与评价口径

- **E0 组合基准**：等权组合或明确指数基准；
- **E1 朴素信号**：过去收益排序或一个连续估值/质量分数，显式 `shift`；
- **E2 ML Baseline**：Qlib LightGBM/Alpha158；
- 所有方法使用相同测试区间、股票池、成本和组合规则；
- 不设置跨数据集通用的 Sharpe 或收益率通关线。

## 6. 最小测试

```text
test_split_is_disjoint
test_feature_timestamp_precedes_execution
test_no_future_rows_in_transform
test_same_seed_reproduces_predictions
test_cost_is_non_negative
test_net_period_return_equals_gross_minus_cost
test_zero_cost_control_matches_gross
test_buy_and_sell_fee_paths
test_benchmark_and_strategy_share_calendar
test_required_artifacts_exist
```

前三项任一失败，作业直接不通过。

## 7. 报告指标

- 信号：IC、Rank IC、IC 分布与稳定性；
- 组合：累计/年化收益、波动率、最大回撤；
- 相对基准：gross/net excess return；
- 执行：换手率、交易成本、gross/net 差异；
- 稳健性：分时段结果与至少一项参数/数据扰动。

## 8. 验收测试

- [ ] commit、环境、数据 release 与 manifest 可追溯；
- [ ] 时间切分、特征可得时间和执行延迟正确；
- [ ] 朴素 Baseline 与 ML 使用同一评价协议；
- [ ] 同时保留策略 gross、策略 net、基准、gross excess、net excess 五条序列；
- [ ] 成本恒等式、零成本对照与买卖两侧费用通过；
- [ ] 报告含失败案例和适用边界。

## 9. Rubric

| 维度 | 分值 | 通过证据 |
|:---|---:|:---|
| 可复现性 | 20 | commit、环境、配置和数据版本齐全 |
| 无泄漏与时间协议 | 25 | 切分、特征时间和执行延迟通过审计 |
| Baseline 公平性 | 15 | 朴素与 ML 使用同一协议 |
| 回测与成本 | 15 | gross/net 与成本口径可复算 |
| 分析质量 | 15 | 消融、稳健性、失败案例和边界完整 |
| 工程质量 | 10 | 配置化运行、测试、日志和产物索引齐全 |

**通过线**：总分不低于 75；“无泄漏与时间协议”不得低于 20/25；硬测试不得失败。

## 10. 提交物

- [ ] `README.md`
- [ ] `source_commit.txt`
- [ ] 环境锁文件
- [ ] 数据清单、manifest 与时间区间
- [ ] Qlib 工作流配置
- [ ] 朴素 Baseline 代码
- [ ] LightGBM 含成本回测
- [ ] 最小测试与无泄漏审计
- [ ] 实验对比表
- [ ] 局限、失败案例和知识反哺记录

## 11. 失败条件

出现任一项即不通过：

- 使用测试集反复选择特征、模型或参数；
- 特征含未来信息或执行时间早于数据可得时间；
- 只报告不含成本结果；
- 机器学习模型没有朴素对照；
- 只展示最好的一次运行；
- 无法说明数据来源、时间区间或仓库版本；
- 用高历史收益替代可复现性和正确性。

## 12. 复盘与知识反哺

完成后回答：最容易泄漏的环节、加入成本后变化最大的结论、LightGBM 相对朴素 Baseline 的稳定增量、推翻初始直觉的失败案例，以及需要写回概念卡/题型卡/错题卡的经验。

## 13. 当前状态

| 事项 | 状态 |
|:---|:---:|
| 作业规格 | completed |
| 来源与许可边界 | completed |
| commit 与环境冻结 | planned |
| 官方工作流烟雾测试 | planned |
| 朴素 Baseline | planned |
| LightGBM 含成本回测 | planned |
| 审核与复盘 | planned |
