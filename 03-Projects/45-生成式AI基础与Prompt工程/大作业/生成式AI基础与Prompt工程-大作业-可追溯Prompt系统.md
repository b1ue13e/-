---
type: project
topic: "生成式AI与Prompt工程结课项目"
project_type: homework
course: "生成式AI基础与Prompt工程"
assignment_id: "生成式AI基础与Prompt工程-capstone"
assignment_level: capstone
assignment_format: project
stage_id: "04"
requires: ["[[生成式AI-基础-概率生成Token与能力边界]]", "[[Prompt工程-需求-任务规格与结构化输出]]", "[[Prompt评测-实验-指标数据集与误差分析]]", "[[Prompt工程-方法-指令示例推理与约束]]", "[[Prompt增强-RAG-检索生成与可追溯回答]]", "[[生成式AI-可靠性-幻觉校准与事实核验]]", "[[Prompt评测-LLMJudge-偏置校准与人工复核]]", "[[Prompt工程-安全-提示注入与分层防护]]"]
source_type: local_integration_task
created: 2026-08-05
status: planned
flow: project
tags: [作业, 45-生成式AI基础与Prompt工程, 结课项目]
source: "Original capstone using MIT 6.7960 and Stanford CS324 project deliverable structure"
source_url: "https://stanford-cs324.github.io/winter2022/"
accessed: 2026-08-09
license: "本地原创结课项目；公开课程页面仅作交付结构参考"
---

# 生成式 AI 与 Prompt 工程结课项目

## 可运行 starter 与起步 Gate

从项目根目录的 `scripts/`、`tests/` 与 `artifacts/` 起步。它提供 40 条 Prompt 分类数据、50 条 RAG 查询、离线/真实模型 adapter、受控实验 runner、引用/拒答 Gate 与自动测试。先运行：

```powershell
cd "F:\-\03-Projects\45-生成式AI基础与Prompt工程"
python -m unittest discover -s tests -v
python scripts/course_lab.py 03 --adapter rule --output artifacts/baseline.json
python scripts/course_lab.py 06 --output artifacts/rag-baseline.json
```

结课项目必须迁移到新用户问题和新数据；只更换标题、标签或 Prompt 不算完成。真实模型结果需使用 `--adapter openai --model "模型ID"` 另行生成，离线 rule 分数只能作为协议回归证据。

## 学习目标

- 独立定义一个有真实用户、数据边界和可观察成功标准的生成式 AI 任务。
- 把 Prompt 基线、RAG 证据、结构化校验、Judge/人工复核和安全策略串成可复现系统。
- 用冻结测试集和逐样本证据比较方案，并对失败做保留、回退或人工接管决策。

## 任务边界

必须更换任务、数据与用户场景，不能只复用课程情感分类或内置 RAG 文档。真实模型调用需要合法密钥和可公开说明的模型标识；不得提交密钥、私有 URL、个人数据或未获许可语料。离线 fixture 只作为起步 Gate。

## 提交产物

1. 可运行代码、环境说明、一键命令和自动测试。
2. 数据卡、任务规格、Prompt 版本、模型/adapter 配置和原始输出。
3. 至少 30 条冻结测试样本的指标、置信区间或方差、错误分类和成本/延迟。
4. 引用/拒答、Judge 校准、红队回归、人工接管与限制说明。
5. 一页复盘：失败根因、舍弃方案、已知风险和下一轮实验。

## 验收标准

复现命令在干净环境可运行；测试和离线 Gate 通过；至少一份真实模型结果有完整 provenance；关键指标可由逐样本记录重算；安全防护同时报告 ASR/TSR/FRR；无法验证的能力明确标记，不能用演示截图替代证据。

## 引导自检

- [ ] 项目是否解决了一个具体用户任务，而不是功能拼盘？
- [ ] 每个系统环节是否有输入、输出、失败模式和验证器？
- [ ] 是否存在只在 dev 上好看、test 上退化的改动？
- [ ] 引用、Judge 或安全结论是否经过人工抽检？
- [ ] README 是否让另一台机器上的学习者知道哪些步骤需要密钥、网络或费用？

## 必交物

1. 问题定义、目标用户、非目标和风险边界。
2. 训练/开发/测试或开发/测试数据集及数据说明。
3. 最弱可行基线、至少三种 Prompt/增强方案。
4. 固定模型、版本、解码参数和 Prompt 版本。
5. 正确性、证据、成本、延迟和安全指标。
6. 至少三项消融、20 个错误样本和失败分类。
7. 红队结果、人工接管条件和残余风险。
8. 可运行代码、README、环境锁定和一页模型/系统卡。
9. 一条端到端验收命令，能从冻结输入生成逐样本输出、指标和非零失败退出码。

## 最小知识点集
- [ ] 课程所有“必需”主题卡闭卷验收通过。
- [ ] 作业 03、05、06、07 至少各复用一项方法。

## 评分

| 维度 | 分值 |
| :--- | :---: |
| 问题与数据 | 15 |
| 基线与方法 | 20 |
| 评测与消融 | 25 |
| 可靠性与安全 | 20 |
| 可复现与表达 | 20 |

## 行为锚点评分量规

| 维度 | 不通过 | 基本通过 | 优秀 |
| :--- | :--- | :--- | :--- |
| 问题与数据 | 目标含糊、测试集参与调参 | 用户/输入/输出明确，开发测试隔离 | 还含非目标、数据偏差与版本说明 |
| 基线与方法 | 只有最佳 Prompt | 有最弱基线与至少 2 个受控方案 | ≥3 个方案，选择理由与替代方案取舍清楚 |
| 评测与消融 | 只展示成功样例 | 固定测试集、主指标、≥2 项消融 | 指标含置信区间/切片，≥3 项消融与 20 个错误分类 |
| 可靠性与安全 | 靠一句“不要幻觉/注入” | 有拒答、引用、红队和人工接管 | 有威胁模型、对抗回归、残余风险与失效演练 |
| 可复现与表达 | 无版本/命令 | README、配置、环境与逐样本结果齐全 | 一键验收、系统卡、成本/延迟与限制表达清晰 |

任一维度为“不通过”则项目不结课；总分 ≥80 且可靠性与安全至少“基本通过”才通过。
