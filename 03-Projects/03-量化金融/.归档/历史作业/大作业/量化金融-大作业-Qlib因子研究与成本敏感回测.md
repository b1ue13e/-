---
type: project
project_type: homework
topic: Qlib因子研究与成本敏感回测
course: "量化金融"
assignment_level: capstone
assignment_format: project
assignment_id: "QF-CAPSTONE-QLIB"
stage_id: "04"
requires: ["[[回测框架与无泄漏实验]]", "[[策略评价指标]]"]
source_type: open_source_project_task
source: "Qlib官方仓库与本地real_assignment_packages/hw17_qlib_factor_research"
accessed: 2026-08-06
created: 2026-07-28
status: active
flow: project
difficulty: advanced
prerequisites:
- 收益率与对数收益率
- 时间序列数据处理
- 策略评价指标
related:
- 最大回撤
- 夏普比率
- 滚动窗口与波动率特征
tags:
- 项目
- 实战作业
- 量化金融
- Qlib
- 因子研究
- 回测
- 无泄漏
eligibility_audited: 2026-07-28
focus: now
domain: quant-finance
difficulty_tier: T3
source_url: https://github.com/microsoft/qlib
source_course: Microsoft Qlib
source_version: pyqlib 0.9.7 / commit da920b7f954f48ab1bb64117c976710de198373e
source_commit: da920b7f954f48ab1bb64117c976710de198373e
data_build_qlib_commit: b87a2c294d364a33fb739359886acffe8ec907d1
license: MIT
mirror_policy: local-clone
adaptation: adapted
data_source_url: https://github.com/chenditc/investment_data/releases/tag/2026-07-27
data_source_release: '2026-07-27'
data_packaging_code_license: Apache-2.0
market_data_license: source-specific
market_data_terms: 底层行情来自多种数据源，使用范围与再分发条件需按各源条款单独核验
dataset_version: investment_data release 2026-07-27；以随包manifest校验
starter_code: Qlib官方examples/workflow_by_code.py与LightGBM benchmark配置
tests: 本地pytest最小测试 + 无泄漏审计清单
baseline: 朴素时序信号/等权对照 + Qlib LightGBM Alpha158
acceptance_test: 可复现、无前视、含成本、样本外、能解释失败
compute_budget: low
solution_visibility: private
---

# HW17：Qlib 因子研究与成本敏感回测

> 这是 [[Quant-Factor-And-Arbitrage-Engine]] 的开源工作流试点。目标不是追求一个漂亮的历史收益数字，而是证明你能建立**可复现、无前视、含成本、样本外可解释**的量化研究流程。

> [!important] 不要直接从本说明书开做
> 从 [[🚀 Qlib项目执行入口|Qlib 项目执行入口]] 进入，按 [[🧩 Qlib 项目知识点—作业—验收路线图|知识点—作业—验收路线图]] 完成 K01–K28 与 A01–A06；本页只用于最后总验收和评分。

## 学习目标

建立可复现、无前视、含成本、样本外可解释的 Qlib 因子研究工作流；工程 smoke 通过不等于研究结论通过。

## 任务边界

- 必须完成数据/环境冻结、E0/E1 基线、Qlib LightGBM 对照、成本敏感回测和无泄漏审计；T4 只作为可选扩展。
- 不分发第三方行情数据，不把 Qlib 代码许可当作行情许可，不使用测试集反复选择。

## 提交产物

- README、源码/配置、环境锁文件、数据 manifest、运行日志、测试结果、gross/net 指标、实验对比表、失败案例和报告。

## 验收标准

- 硬测试全部通过；同一随机种子可复现；特征时间早于执行时间；E0/E1/ML 使用同一测试协议；同时报告 gross/net 和成本。
- 结论必须包含至少一项消融或压力测试，并明确市场数据条款未核验时的限制。

## 引导自检

- [ ] 先按项目执行入口完成 T1 smoke 和数据 manifest。
- [ ] 再完成 E0/E1 基线与时间审计。
- [ ] 最后运行 LightGBM、成本压力和失败复盘，不以最高收益替代证据。

## 1. 任务定义

### 1.1 我们要解决的问题

很多策略 Notebook 可以输出净值曲线，却无法回答：

- 数据和代码能否在另一台机器上复现？
- 特征在交易发生前是否已经可得？
- 模型是否只是在训练区间记住噪声？
- 交易成本加入后，结论是否改变？
- 机器学习模型是否真的优于朴素方法？

本作业使用 Qlib 串联数据、特征、模型、信号、组合、模拟执行和评估，建立一条可以审计的最小研究链路。

### 1.2 输入与输出

**输入**

- Qlib 官方 README 当前推荐的社区 `investment_data` 固定发布包；
- 一个在运行前固定的股票池；
- 一个在运行前固定的训练、验证、测试时间切分；
- 官方 LightGBM/Alpha158 示例作为可运行参考。

**输出**

- 环境与来源清单；
- 朴素 Baseline；
- Qlib LightGBM Baseline；
- 样本外含成本回测；
- 消融与稳健性表；
- 无泄漏审计；
- 失败案例和结论边界。

## 2. 来源、版本与许可证

| 项目 | 要求 |
|:---|:---|
| Qlib 官方仓库 | `https://github.com/microsoft/qlib` |
| Qlib 代码许可证 | MIT；本地克隆时保留许可证和版权声明 |
| Qlib 运行版本 | Windows 官方 wheel `pyqlib 0.9.7`；对应源码 `da920b7f954f48ab1bb64117c976710de198373e` |
| 数据构建版本 | release manifest 的 `qlib_commit` 为 `b87a2c294d364a33fb739359886acffe8ec907d1`；单独记录，不冒充本地运行版本 |
| 数据发布包 | `investment_data` release `2026-07-27` |
| 数据仓库代码与打包工具许可证 | Apache-2.0 |
| 底层行情条款 | 数据来自 Tushare、AkShare、Yahoo、Baostock 等来源；不得用代码许可证代替各数据源条款 |
| 环境冻结 | 保存 Python 版本及 `pip freeze` 或等价锁文件 |
| 数据冻结 | 下载 release archive 与 provenance manifest，并按 manifest 验证归档后记录校验值 |
| 答案可见性 | 只保存自己的代码与报告，不挂载他人完整答案 |

> [!warning]
> Qlib 的 MIT 许可证只覆盖 Qlib 代码；`investment_data` 的 Apache-2.0 许可证覆盖仓库代码与打包工具，但不能自动覆盖归档内底层行情数据的独立使用条款。没有代码 commit、环境锁文件、数据 release 和 manifest 验证的结果，不算可复现证据。

## 3. 前置知识和按需补课

- [[收益率与对数收益率]]：统一预测目标、组合收益和绩效指标的收益率口径。
- [[时间索引与频率（量化）]]：理解时间索引、重采样、缺失值和滚动特征为什么可能泄漏。
- [[策略评价指标]]：避免只展示收益率，不报告风险、成本和基准。
- [[滚动窗口与波动率特征]]：设计 walk-forward 或滚动验证时使用。

这些页面是当前量化 Sprint 的按需依赖，不会成为新的主 Sprint。当前 Sprint 只做 K01–K06 与 A01；A02–A06 按六周路线后续解锁。

## 4. 数据协议与无泄漏约束

运行前填写并冻结：

| 字段 | 值 |
|:---|:---|
| 市场/地区 |  |
| 股票池 |  |
| 数据频率 |  |
| 训练区间 |  |
| 验证区间 |  |
| 测试区间 |  |
| 基准指数 |  |
| 成交价格假设 |  |
| 单边佣金 |  |
| 印花税/其他费用 |  |
| 最小费用 |  |
| 数据快照或校验值 |  |

硬约束：

1. 三个时间区间不得重叠；
2. 测试集只用于最终评价，不反复参与选择；
3. 在日期 $t$ 形成的信号，最早只能使用当时已经可得的数据，并在预先声明的 $t+1$ 或之后执行；
4. 横截面标准化、缺失值填补和特征选择必须只使用当期或训练期信息；
5. 复权方式、停牌、涨跌停、退市和股票池变更必须写入限制说明；
6. 任何手工删除“表现不好”样本的操作都必须记录。

## 5. 难度阶梯

### T1：官方工作流烟雾测试

目标：证明环境和官方示例可以运行。

- 克隆官方 Qlib 仓库并检出本作业固定 commit；
- 下载 `investment_data` 的 `2026-07-27` 归档及 manifest，并完成归档验证；
- 跑通官方 LightGBM/Alpha158 工作流；
- 保存配置、日志和生成的指标；
- 不把官方示例结果当成自己的研究结论。

**通过证据**：环境清单、commit、配置、运行日志、输出目录说明。

完整烟雾测试命令：

```powershell
powershell -ExecutionPolicy Bypass -File "99-System/tools/run_qlib_smoke_test.ps1"
```

脚本会依次完成：固定仓库检出、归档与 manifest 下载、发布包验证、解压到 `provider_uri`、创建独立虚拟环境、安装固定 Qlib commit、生成 `requirements.lock`、执行 LightGBM/Alpha158 `qrun`，并保存日志与退出码。默认运行证据进入 `99-System/tmp/qlib-pilot-runtime/`；若验证器、安装或 `qrun` 任一步失败，脚本立即停止，不自动退回不明来源数据。

### T2：建立朴素 Baseline

目标：给机器学习模型一个公平对照。

本层包含两个不同角色的对照：

- **E0 组合基准**：等权组合或明确的指数基准；它只比较组合收益、波动、回撤、换手和成本，不计算 IC；
- **E1 朴素信号**：过去一段时间收益排序，或一个连续的估值/质量分数；必须在代码中显式 `shift`，并能计算 IC/Rank IC。

要求：

- E1 特征定义不超过三项；
- 不调参或只用训练集内预先声明的少量选择；
- 使用与 ML 模型完全相同的测试区间、股票池、成本和组合规则；
- E1 报告 IC/Rank IC；E0、E1 与 ML 模型共同报告换手率、组合收益、最大回撤及含成本结果。

**通过证据**：可以逐行解释信号在什么时间生成、在什么时间成交。

### T3：Qlib LightGBM 与成本敏感回测

目标：判断复杂模型是否带来可解释的增量。

- 使用 Qlib Dataset/Model/Recorder 完成训练和预测；
- 使用固定策略或明确记录的自定义策略形成组合；
- 同时输出不含成本与含成本结果；
- 与朴素 Baseline 使用同一评价协议；
- 对至少一个关键选择做消融，例如：
  - Alpha158 全特征 vs 精简特征；
  - 不同持仓数量；
  - 不同调仓频率；
  - 有无行业/规模控制；
  - 不同成本假设。

不设置通用的 Sharpe 通关线。复杂模型只有在**同口径、样本外、含成本**条件下表现出稳定增量，才可以说“比 Baseline 更好”。

### T4：可选开放挑战

- 多窗口 walk-forward；
- 不同市场阶段的稳定性；
- 组合约束或风险模型；
- 信号衰减与换手分解；
- 训练区间扰动、股票池扰动和成本压力测试。

T4 不属于当前 Sprint 的必做项。

## 6. 最小测试

至少实现以下自动检查或等价断言：

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

其中前三项任一失败，作业直接判为不通过，不能依靠高回测收益抵消。

## 7. 指标与报告口径

至少报告：

| 层级 | 指标 |
|:---|:---|
| 信号 | IC、Rank IC、IC 分布或稳定性 |
| 组合 | 累计收益、年化收益、波动率、最大回撤 |
| 相对基准 | 超额收益、信息比率或 Alpha/Beta |
| 执行 | 换手率、交易成本、含成本与不含成本差异 |
| 稳健性 | 分时段结果、至少一项参数/数据扰动 |

统一定义：

- `gross strategy return`：策略扣除交易成本前的原始组合收益；
- `net strategy return`：同一策略按已声明的买入、卖出、印花税与最低费用规则扣费后的收益；
- `gross/net excess return`：对应的 gross/net 策略收益减去同一日历、同一收益口径的基准收益。

Qlib 输出中可能同时出现策略收益、基准收益和超额收益，报告必须注明字段映射；不能把超额收益误标为策略净收益。至少保留“策略 gross、策略 net、基准、gross excess、net excess”五条可复核序列。

- [[最大回撤]]：说明历史路径中最深的峰谷损失，而不是未来风险上界。
- [[策略评价指标]]：必须注明频率、无风险收益、年化方法和样本区间。
- [[策略评价指标]]：最终结论必须来自多指标证据，而不是单个分数。

## 8. 实验对比表

| 实验 | 数据/特征 | 模型 | 组合规则 | 成本 | 测试区间 | 关键结果 | 结论 |
|:---|:---|:---|:---|:---:|:---|:---|:---|
| E0 | 统一数据 | 等权/基准 | 固定 | 是 |  |  |  |
| E1 | 简单特征 | 朴素信号 | 与 E2 相同 | 是 |  |  |  |
| E2 | Alpha158 | LightGBM | 固定 | 是 |  |  |  |
| E3 | 单变量消融 | LightGBM | 固定 | 是 |  |  |  |
| E4 | 与 E2 相同 | LightGBM | 固定 | 压力成本 |  |  |  |

一次只改变一个关键变量。若数据、模型、组合规则和成本同时变化，则不能把结果差异归因于模型。

## 9. Rubric

| 维度 | 权重 | 通过标准 | 优秀标准 |
|:---|:---:|:---|:---|
| 可复现性 | 20 | commit、环境、配置和数据版本齐全 | 新环境可按 README 一次复现 |
| 无泄漏与时间协议 | 25 | 切分、特征时间和执行延迟正确 | 有自动测试和逐字段可得时间审计 |
| Baseline 公平性 | 15 | 朴素与 ML 使用同一评价协议 | 能解释复杂模型增量来自哪里 |
| 回测与成本 | 15 | 同时报告 gross/net，成本口径明确 | 有换手分解和成本压力测试 |
| 分析质量 | 15 | 结论与证据一致，包含失败案例 | 分阶段、消融和稳健性结论清楚 |
| 工程质量 | 10 | 目录清晰，关键函数有测试 | 配置化运行、日志和产物索引完整 |

**通过线**：总分不低于 75；“无泄漏与时间协议”不得低于 20/25；硬测试不得失败。

## 10. 提交物

- [ ] `README.md`
- [ ] `source_commit.txt`
- [ ] 环境锁文件
- [ ] 数据清单与时间区间
- [ ] Qlib 工作流配置
- [ ] 朴素 Baseline 代码
- [ ] LightGBM 工作流
- [ ] 最小测试
- [ ] gross/net 回测结果
- [ ] 实验对比表
- [ ] 无泄漏审计
- [ ] 局限、失败案例和知识反哺记录

建议代码目录：

```text
quant-qlib-pilot/
├── README.md
├── configs/
├── data_manifest/
├── src/
├── tests/
├── reports/
├── artifacts/
├── requirements.lock
└── source_commit.txt
```

## 11. 失败条件

出现任一项即不通过：

- 使用测试集反复选择特征、模型或参数；
- 特征含未来信息或执行时间早于数据可得时间；
- 只报告不含成本结果；
- 机器学习模型没有朴素对照；
- 只展示最好的一次随机运行；
- 无法说明数据来源、时间区间或仓库版本；
- 用高历史收益替代可复现性和正确性。

## 12. 复盘与知识反哺

完成后至少回答：

1. 最容易发生泄漏的环节在哪里？
2. 加入成本后，哪个结论变化最大？
3. LightGBM 相对朴素 Baseline 的增量是否稳定？
4. 哪个失败案例推翻了最初直觉？
5. 哪条经验应写回概念卡、题型卡或错题卡？

回填位置：

- 项目证据：[[Quant-Factor-And-Arbitrage-Engine]]
- 课程入口：[[🧭 课程作业总索引|量化金融课程作业总索引]]
- 系统升级项目：[[项目-33门课程开源作业体系升级]]

## 13. 当前状态

| 事项 | 状态 |
|:---|:---:|
| 作业规格 | completed |
| 来源与许可证核验 | completed |
| commit 与环境冻结 | completed（仅工具链证据） |
| 官方工作流烟雾测试 | completed（退出码 `0`，不代表知识已掌握） |
| 朴素 Baseline | planned |
| 自己的 LightGBM 公平对照与含成本结论 | planned |
| 审核与

