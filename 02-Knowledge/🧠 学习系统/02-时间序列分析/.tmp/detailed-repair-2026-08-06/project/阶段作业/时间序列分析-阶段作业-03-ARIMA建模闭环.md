---
type: project
project_type: homework
course: "时间序列分析"
assignment_id: "时间序列分析-S03"
assignment_level: stage
assignment_format: project
stage_id: "03"
requires: ["[[L05-ARMA与ARIMA建模闭环]]", "[[ARIMA建模流程-识别-估计-诊断]]", "[[ARIMA模型]]", "[[差分运算]]", "[[参数估计]]"]
source_type: local_integration_task
source: "本地原创综合任务，工作流参考 FPP3 Chapter 9"
source_url: "https://otexts.com/fpp3/arima-r.html"
source_version: "FPP3 3e online, accessed 2026-08-06"
license: "本地原创任务；外部教材仅 link-only。"
created: 2026-08-02
updated: 2026-08-06
status: planned
flow: project
tags: [作业, 时间序列分析, ARIMA, 阶段作业]
---

# 时间序列分析｜阶段作业 03：ARIMA 建模闭环

## 学习目标

把差分、候选识别、估计、根、残差与滚动预测串成一个可复现的阶段闭环，并允许 ARIMA 输给朴素基线。

## 任务边界与协议

- 选择非季节、长度至少 120 的公开序列；记录来源、许可/使用边界与快照版本。
- 保留最后 20% 为最终测试；在模型与协议冻结前不得查看。
- Python 3、`pandas`、`statsmodels`；依赖版本进入 `environment.txt`。
- 手工候选 3–5 个，自动搜索仅作对照；普通 CPU 预计少于 15 分钟。

## 里程碑

1. **差分与还原（15 分）**：对 `[100,102,105,104,108]` 手算一阶差分；未来差分 2、-1 时递归还原两期水平预测。
2. **模型翻译（15 分）**：把 ARIMA$(1,1,1)$ 改写为差分序列的 ARMA 方程，解释 $p,d,q$ 与符号约定。
3. **人工候选台账（25 分）**：原/差分图、变换与 $d$ 证据、候选阶数/趋势/AICc/收敛/根/淘汰理由。
4. **自动与人工对照（15 分）**：记录搜索空间、stepwise 设置、差分/趋势规则；自动结果接受同一诊断。
5. **滚动预测（20 分）**：比较 naïve、最佳人工 ARIMA、自动 ARIMA；报告 horizon 1 和更远 horizon 的 MAE/RMSE。
6. **迷你报告（10 分）**：300–500 字说明差分、胜出证据、残差风险、相对基线价值与失效条件。

## 提交产物与结构

```text
submission/
├── README.md
├── manifest.yml
├── src/
├── artifacts/candidate-ledger.csv
├── artifacts/rolling-metrics.csv
└── report.md
```

`manifest.yml` 至少记录数据 URL/版本、时间范围、最终测试边界、依赖、种子、运行命令和输出清单。

## 验收标准与硬验收

- 变换、差分和逆差分逻辑一致；不跨差分口径机械比较 AICc。
- 失败拟合、警告和根全部保留；残差检查含图与联合检验。
- 滚动评估只使用当时可得信息，所有候选与基线共享窗口和 horizon。
- 报告不把训练残差合格等同于样本外/业务有效。

总分至少 80/100 且无硬失败。通过后进入[[时间序列分析-课后作业-05-SARIMA与季节预测]]。

## 引导与自检

按“差分还原 → 候选台账 → 诊断 → 滚动预测”顺序逐步冻结证据；提交前从空目录执行 README 命令，核对 manifest、CSV 和报告中的测试边界一致。
