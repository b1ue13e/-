---
type: project
topic: "生成式AI与Prompt工程结课项目"
created: 2026-08-05
status: active
progress: 0%
flow: project
kind: problem-type
tags: [项目, 45-生成式AI基础与Prompt工程, 结课项目]
source: "Original capstone using MIT 6.7960 and Stanford CS324 project deliverable structure"
---

# 生成式 AI 与 Prompt 工程结课项目

## 可运行 starter 与起步 Gate

从 `03-Projects/45-生成式AI基础与Prompt工程/starter/` 起步。它提供 40 条 Prompt 分类数据、50 条 RAG 查询、离线/真实模型 adapter、受控实验 runner、引用/拒答 Gate 与自动测试。先运行：

```powershell
cd "F:\-\03-Projects\45-生成式AI基础与Prompt工程\starter"
python -m unittest -v
python course_lab.py 03 --adapter rule --output baseline.json
python course_lab.py 06 --output rag-baseline.json
```

结课项目必须迁移到新用户问题和新数据；只更换标题、标签或 Prompt 不算完成。真实模型结果需使用 `--adapter openai --model "模型ID"` 另行生成，离线 rule 分数只能作为协议回归证据。

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
