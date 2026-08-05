﻿﻿﻿$ErrorActionPreference = "Stop"

$baseDir = "f:\-\02-Knowledge\🧠 学习系统\03-量化金融\18-实战作业说明书"
$today = "2026-07-31"

function Format-Bullets {
    param([string[]]$Items)
    return ($Items | ForEach-Object { "- $_" }) -join "`r`n"
}

function Format-Goals {
    param([string[]]$Items)
    $i = 1
    return ($Items | ForEach-Object {
        $line = "$i. $_"
        $i += 1
        $line
    }) -join "`r`n"
}

function Format-Delivery {
    param([string[]]$Items)
    return ($Items | ForEach-Object { "- $_" }) -join "`r`n"
}

function Render-Spec {
    param([hashtable]$Spec)

    $prereqBullets = Format-Bullets $Spec.Prerequisites
    $goalBullets = Format-Goals $Spec.Goals
    $levelBullets = Format-Bullets $Spec.LevelTargets
    $deliveryBullets = Format-Delivery $Spec.Deliverables

    return @"
---
title: "$($Spec.Title)"
date: 2026-07-24
updated: $today
type: homework
course: "量化金融"
status: active
difficulty: "Advanced (4-Tier)"
homework_id: "$($Spec.Id)"
stage: "$($Spec.Stage)"
tags: [实战作业, 量化金融, 正式作业说明书, 老师版]
prerequisites:
$(
($Spec.Prerequisites | ForEach-Object { "  - '$_'" }) -join "`r`n"
)
---

# 🎓 $($Spec.Title)

> **说明书定位**：教师正式发布版  
> **关联主干笔记**：$($Spec.Anchor)  
> **教师视角总设计**：[[🧑‍🏫 量化金融老师视角教学设计与作业节奏]]

---

## 1. 布置时机

$($Spec.Timing)

**教师布置理由：**
$($Spec.TimingReason)

---

## 2. 前置知识

学生在开启本作业前，至少应完成以下知识卡与课上最小示例：

$prereqBullets

**开作业前的教师检查点：**
$($Spec.Checkpoint)

---

## 3. 教学目标

$goalBullets

---

## 4. 作业任务

### 4.1 核心任务

$($Spec.CoreTask)

### 4.2 分层要求

$levelBullets

**统一硬门槛：**
- 必须写清楚数据来源、时间区间、切分方式和成本口径。
- 必须提供最小可运行示例或 smoke test，证明流程能从头到尾跑通。
- 必须说明失败案例、异常结果或方法边界，不能只汇报最好结果。

---

## 5. 评分标准

### 5.1 一票否决项

- 使用未来数据、前视偏差或未说明的数据泄漏处理方式。
- 没有 baseline 或没有与朴素方案做公平对照。
- 代码无法运行，或没有最小复现步骤。
- 报告只给结论，不解释方法、限制和失败案例。

### 5.2 评分维度

| 维度 | 分值 | 评分说明 |
|:---|:---:|:---|
| 问题理解与方法正确性 | 25 | 是否真正理解本作业的金融问题，方法是否与题目匹配 |
| 数据处理与实验设计 | 20 | 数据口径、时间切分、无泄漏设计是否清楚可靠 |
| Baseline 与结果对照 | 20 | 是否有朴素基线、公平对照和合理比较 |
| 分析解释与边界意识 | 20 | 是否能解释结果，是否报告失败案例与局限 |
| 工程质量与复现性 | 15 | 目录结构、脚本可运行性、文档完整性是否达标 |

### 5.3 本作业特别强调

$($Spec.EvaluationEmphasis)

---

## 6. 交付格式

建议按如下结构提交：

~~~text
$($Spec.Id.ToLower())/
  README.md
  data/                # 原始数据说明或下载脚本，不提交受限原始大文件
  src/ 或 notebooks/    # 主要实现
  tests/               # 至少 1 个 smoke test
  results/             # 指标表、导出结果、关键中间产物
  figures/             # 图表
  report.md            # 正式分析报告
~~~

**必交内容：**
$deliveryBullets

---

## 7. 教师备注

$($Spec.TeacherNote)
"@
}

$specs = @(
    @{
        Id = "HW01"
        File = "🎓 HW01 - CAPM 资产定价与单股 Alpha_Beta 归因实战作业说明书.md"
        Title = "HW01 - CAPM 资产定价与单股 Alpha/Beta 归因正式作业说明书"
        Stage = "第一阶段：资产定价与财务量化"
        Anchor = "[[CAPM 资本资产定价模型]]"
        Timing = "在完成收益率、超额收益、基准、无风险利率和 CAPM 基本回归后布置。建议放在 U02 结束后，作为课程第一份正式作业。"
        TimingReason = "这时学生第一次具备了「收益分解 + 基准比较 + 回归解释」的完整能力闭环，适合用作第一份压实金融语言的作业。"
        Prerequisites = @("[[收益率与对数收益率]]","[[无风险资产与资本市场线]]","[[CAPM 资本资产定价模型]]")
        Checkpoint = "学生应能独立解释 alpha、beta、超额收益与 benchmark 的区别，并读懂一份最基本的 OLS 回归输出。"
        Goals = @(
            "会把单只资产收益拆成市场暴露与特异收益。",
            "会使用基准指数和无风险利率构造 CAPM 回归。",
            "能解释 alpha 与 beta 的经济含义，而不只是报数字。",
            "开始建立「量化分析先定义基准，再比较结果」的习惯。"
        )
        CoreTask = "选择一只股票和一个市场指数，完成 CAPM 回归、Alpha/Beta 估计、滚动 Beta 扩展，并分析这只资产在不同市场环境下的风险暴露变化。"
        LevelTargets = @(
            "🟢 Simple：单资产 CAPM 回归跑通，解释 Alpha/Beta 与超额收益。",
            "🟡 Medium：扩展到一组股票，比较不同资产的市场暴露差异。",
            "🔴 Strong：加入滚动窗口，分析 Beta 随时间变化的原因与影响。",
            "🟣 Boss：构造低 Beta / 高 Beta 对照组合，讨论 Beta 中性化与策略含义。"
        )
        EvaluationEmphasis = "重点看收益分解是否正确、基准与无风险利率口径是否合理、统计结论是否支撑金融解释，不以「收益更高」作为主要得分来源。"
        Deliverables = @(
            "README.md：说明数据来源、时间区间、回归口径与运行方法。",
            "src/ 或 notebook：完成 CAPM 回归、滚动 Beta 与图表输出。",
            "tests/：至少 1 个 smoke test，验证收益率计算和回归流程能运行。",
            "report.md：解释 Alpha/Beta 的含义、结果局限与失败案例。"
        )
        TeacherNote = "如果学生在这份作业里仍频繁混淆总收益、超额收益和基准收益，不要急着推进下一份因子作业。"
    }
    @{
        Id = "HW02"
        File = "🎓 HW02 - 马科维茨均值-方差有效前沿与协方差病态求解实战作业说明书.md"
        Title = "HW02 - 马科维茨均值-方差有效前沿正式作业说明书"
        Stage = "第一阶段：资产定价与财务量化"
        Anchor = "[[马科维茨均值-方差模型]]"
        Timing = "在学生学完协方差、相关系数、分散化和均值-方差框架后布置。建议放在 U03 结束后，作为第一阶段压舱石作业。"
        TimingReason = "学生此时刚从「单只资产视角」切换到「组合视角」，最适合通过一份正式作业把协方差结构、风险分散和最优配置语言真正固定下来。"
        Prerequisites = @("[[收益率与对数收益率]]","[[相关系数、协方差与分散化]]","[[马科维茨均值-方差模型]]")
        Checkpoint = "学生应能手算两到三资产组合的预期收益和方差，并解释为什么低相关不等于低风险。"
        Goals = @(
            "理解有效前沿、最小方差组合和切线组合的金融含义。",
            "会从资产收益矩阵构建协方差矩阵并进行基本配置求解。",
            "意识到协方差估计质量会直接影响最优解稳定性。",
            "形成「先做基线配置，再谈更高级方法」的工作顺序。"
        )
        CoreTask = "使用一组真实资产收益率，构建均值-方差配置问题，画出有效前沿，比较等权、最小方差和切线组合，并分析协方差病态对权重的影响。"
        LevelTargets = @(
            "🟢 Simple：三资产手算组合收益、方差和切线组合。",
            "🟡 Medium：在真实资产池上实现无卖空有效前沿。",
            "🔴 Strong：分析协方差病态、权重极值与样本外表现差异。",
            "🟣 Boss：加入收缩估计或稳健约束，比较配置稳定性。"
        )
        EvaluationEmphasis = "重点看协方差处理是否正确、配置问题定义是否清晰、对样本内与样本外差异是否有解释，不奖励只会画漂亮前沿图。"
        Deliverables = @(
            "README.md：说明资产池、样本区间、约束条件与运行命令。",
            "src/optimize.py 或 notebook：完成收益率计算、协方差估计与前沿绘制。",
            "tests/：至少 1 个 smoke test，验证小规模组合计算正确。",
            "report.md：比较不同组合方案并解释样本外表现。"
        )
        TeacherNote = "这份作业如果做扎实，后面的 HRP、风险平价和协方差去噪都会顺很多。"
    }
    @{
        Id = "HW03"
        File = "🎓 HW03 - Fama-MacBeth 跨期横截面风险溢价估计实战作业说明书.md"
        Title = "HW03 - Fama-MacBeth 跨期横截面风险溢价估计正式作业说明书"
        Stage = "第一阶段：资产定价与财务量化"
        Anchor = "[[Fama-MacBeth 两步回归法 (Fama-MacBeth Two-Step Regression)]]"
        Timing = "在完成 CAPM、多因子基本框架和横截面回归直觉后布置。建议放在 U04 结束后。"
        TimingReason = "这时学生已经见过单资产回归，也开始接触因子语言，适合正式进入「因子有效性要靠统计检验」这一层。"
        Prerequisites = @("[[CAPM 资本资产定价模型]]","[[APT套利定价理论]]","[[Fama-French三因子模型]]","[[Fama-MacBeth 两步回归法 (Fama-MacBeth Two-Step Regression)]]")
        Checkpoint = "学生应能解释时间序列回归和横截面回归的区别，并说明因子暴露与风险溢价为何不是同一个对象。"
        Goals = @(
            "理解 Fama-MacBeth 两步法的统计逻辑。",
            "会估计因子暴露并在横截面上估计风险溢价。",
            "能用统计显著性而不是故事描述因子有效性。",
            "建立多因子检验的基本报告习惯。"
        )
        CoreTask = "在多资产数据上完成两步回归：先估计个股因子暴露，再跨期估计风险溢价，并讨论哪些因子具有稳定解释力。"
        LevelTargets = @(
            "🟢 Simple：小样本手算两步回归流程。",
            "🟡 Medium：在真实资产池上批量完成 Fama-MacBeth 回归。",
            "🔴 Strong：加入稳健标准误与时间稳定性分析。",
            "🟣 Boss：比较不同因子集合，并讨论边际风险溢价。"
        )
        EvaluationEmphasis = "重点看两步回归流程是否清楚、横截面与时间维度是否分开处理、统计显著性解释是否谨慎。"
        Deliverables = @(
            "README.md：说明因子定义、样本区间和两步回归流程。",
            "src/ 或 notebook：实现暴露估计、风险溢价估计和显著性检验。",
            "tests/：至少 1 个 smoke test，验证小样本两步法流程。",
            "report.md：讨论因子是否稳定、结果局限和经济含义。"
        )
        TeacherNote = "学生如果还把显著性结果直接等同于可交易 alpha，需要在讲评里重点纠正。"
    }
    @{
        Id = "HW04"
        File = "🎓 HW04 - Beneish M-Score 8 因素财报排雷与做空垃圾股作业说明书.md"
        Title = "HW04 - Beneish M-Score 与财报排雷正式作业说明书"
        Stage = "第一阶段：资产定价与财务量化"
        Anchor = "[[Beneish M-Score 财务造假模型与 Sloan 应计项因子 (Beneish M-Score & Sloan Accruals)]]"
        Timing = "在学生学完三大报表关系、利润质量和应计项直觉后布置。建议放在 U05 结束后。"
        TimingReason = "课程此时要把学生从纯价格世界带到基本面量化世界，让他们第一次把财报字段转成可计算信号。"
        Prerequisites = @("[[三大财务报表钩稽关系 (Interrelationship of Financial Statements)]]","[[ROE 拆解与杜邦分析 (DuPont Analysis)]]","[[利润表与利润质量]]","[[Beneish M-Score 财务造假模型与 Sloan 应计项因子 (Beneish M-Score & Sloan Accruals)]]")
        Checkpoint = "学生应能读懂主要报表字段，并解释利润质量、现金流与应计项之间的关系。"
        Goals = @(
            "会从财报数据中构造结构化风险信号。",
            "理解 Beneish M-Score 和应计项因子的直觉与局限。",
            "学会把基本面信号和市场表现联系起来讨论。",
            "建立财报字段清洗和口径统一的意识。"
        )
        CoreTask = "使用财务报表数据计算 Beneish M-Score 或相关质量信号，对公司进行风险筛查，并分析这些信号在后续收益或风险上的表现。"
        LevelTargets = @(
            "🟢 Simple：单公司手算关键财务比率并验证公式。",
            "🟡 Medium：批量计算一组公司财报风险信号并排序。",
            "🔴 Strong：比较财报信号与后续收益或回撤的关系。",
            "🟣 Boss：将质量因子与其他基本面维度组合成筛选框架。"
        )
        EvaluationEmphasis = "重点看字段口径和财报逻辑是否正确、是否说明 PIT 问题和发布日期滞后，而不是简单拼比率。"
        Deliverables = @(
            "README.md：说明财报字段来源、口径与发布日期处理方式。",
            "src/ 或 notebook：实现信号计算、排序和对照分析。",
            "tests/：至少 1 个 smoke test，验证公式和字段映射。",
            "report.md：说明信号有效性、局限和可能误判案例。"
        )
        TeacherNote = "这份作业要特别强调「财报发布日期」与「研究使用日期」不能混为一谈。"
    }
    @{
        Id = "HW05"
        File = "🎓 HW05 - Black-Scholes 期权定价与动态 Delta 中性对冲作业说明书.md"
        Title = "HW05 - Black-Scholes 定价与动态 Delta 对冲正式作业说明书"
        Stage = "第二阶段：时间序列、期权与风控"
        Anchor = "[[Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)]]"
        Timing = "在完成期权 payoff、BSM 闭式和 Greeks 基础后布置。建议放在 U06 结束后。"
        TimingReason = "学生此时第一次真正同时面对「定价 + 风险暴露 + 对冲误差」，正是理解衍生品课程核心语言的最好时点。"
        Prerequisites = @("[[远期、期货与期权的区别]]","[[二叉树期权定价模型 (Binomial Option Pricing Model)]]","[[Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)]]","[[期权希腊字母 (Option Greeks_ Delta, Gamma, Theta, Vega, Rho)]]")
        Checkpoint = "学生应能解释 call/put payoff、Delta 的方向意义，以及连续对冲与离散对冲为何不同。"
        Goals = @(
            "掌握 BSM 定价和 Greeks 的基础实现。",
            "理解 Delta 对冲的直觉与局限。",
            "能分析离散调仓、波动率误设和摩擦成本带来的误差。",
            "建立「模型价格不等于无风险套利机会」的意识。"
        )
        CoreTask = "实现一个标准的 BSM 定价器，并在历史或模拟路径上做离散 Delta 对冲，分析 PnL、对冲误差和调仓频率。"
        LevelTargets = @(
            "🟢 Simple：完成 BSM 闭式定价与基本 Greeks 计算。",
            "🟡 Medium：在模拟路径上实现离散 Delta 对冲。",
            "🔴 Strong：分析波动率误设、调仓频率与对冲损耗。",
            "🟣 Boss：扩展到 Delta-Vega 或更复杂风险暴露讨论。"
        )
        EvaluationEmphasis = "重点看定价与对冲逻辑是否一致、误差分析是否到位，不以单次 PnL 漂亮作为高分依据。"
        Deliverables = @(
            "README.md：说明模型假设、路径生成方式与运行方法。",
            "src/pricing.py 与 src/hedge.py 或 notebook：完成定价和对冲实验。",
            "tests/：至少 1 个 smoke test，验证 BSM 基本公式与边界情况。",
            "report.md：解释误差来源、对冲效果和方法边界。"
        )
        TeacherNote = "批改时要看学生是否真的理解误差从哪来，而不是只把公式抄出来。"
    }
    @{
        Id = "HW06"
        File = "🎓 HW06 - GARCH(1,1) 动态条件波动率拟合与动态 VaR 作业说明书.md"
        Title = "HW06 - GARCH(1,1) 动态波动率与动态 VaR 正式作业说明书"
        Stage = "第二阶段：时间序列、期权与风控"
        Anchor = "[[GARCH模型]]"
        Timing = "在完成收益率风格化事实、波动率聚集、ARCH/GARCH 直觉后布置。建议放在 U07 结束后，作为第二阶段压舱石作业。"
        TimingReason = "学生此时已经能接受「预测的重点不是价格本身，而是条件风险结构」，适合正式进入风险建模。"
        Prerequisites = @("[[收益率序列的风格化事实]]","[[波动率聚集]]","[[ARCH效应]]","[[GARCH模型]]")
        Checkpoint = "学生应能解释为什么金融序列常见条件异方差，以及 GARCH 的三个核心参数在描述什么。"
        Goals = @(
            "掌握 GARCH(1,1) 的基本拟合与诊断。",
            "能把条件波动率估计连接到动态 VaR。",
            "理解波动率预测与风险管理之间的关系。",
            "建立样本内拟合与样本外风险检验的意识。"
        )
        CoreTask = "对一段真实收益率序列拟合 GARCH(1,1)，输出条件波动率，并基于该波动率构建动态 VaR，检验其风险覆盖表现。"
        LevelTargets = @(
            "🟢 Simple：调用现成库完成 GARCH 拟合与波动率输出。",
            "🟡 Medium：完成动态 VaR 序列并与历史模拟法比较。",
            "🔴 Strong：报告命中率、Kupiec 检验或其他覆盖检验结果。",
            "🟣 Boss：讨论不同分布假设、参数稳定性和风险管理含义。"
        )
        EvaluationEmphasis = "重点看波动率与 VaR 是否真正连起来、风险检验是否到位，而不是只给拟合曲线。"
        Deliverables = @(
            "README.md：说明数据区间、收益率构造方式和 GARCH 参数设置。",
            "src/ 或 notebook：完成拟合、VaR 生成与风险检验。",
            "tests/：至少 1 个 smoke test，验证收益率预处理和基本输出。",
            "report.md：解释波动率预测结果、VaR 命中情况和模型局限。"
        )
        TeacherNote = "如果学生在这份作业里仍把样本内拟合好看当成成功标准，说明风险建模观念还没建立起来。"
    }
    @{
        Id = "HW07"
        File = "🎓 HW07 - EGARCH & GJR-GARCH 杠杆效应与新闻响应曲线作业说明书.md"
        Title = "HW07 - 非对称 GARCH 与杠杆效应正式作业说明书"
        Stage = "第二阶段：时间序列、期权与风控"
        Anchor = "[[非对称 GARCH 模型与杠杆效应 (EGARCH & GJR-GARCH)]]"
        Timing = "在学生完成一次标准 GARCH 作业并理解条件波动率后布置。建议放在 U08 的前半段。"
        TimingReason = "这时学生已经知道标准 GARCH 在金融数据上不够用，正适合推进到好消息与坏消息非对称反应。"
        Prerequisites = @("[[GARCH模型]]","[[非对称 GARCH 模型与杠杆效应 (EGARCH & GJR-GARCH)]]")
        Checkpoint = "学生应能解释什么是杠杆效应，并说明为何负收益冲击往往对应更高波动率反应。"
        Goals = @(
            "理解 EGARCH 或 GJR-GARCH 的非对称结构。",
            "会比较标准 GARCH 与非对称模型的拟合差异。",
            "能用新闻响应曲线解释波动率对冲击的非对称反应。",
            "形成「修正假设比堆模型更重要」的认识。"
        )
        CoreTask = "选择一段带有明显波动聚集的收益序列，比较 GARCH 与非对称 GARCH 模型，并用新闻响应曲线分析其差异。"
        LevelTargets = @(
            "🟢 Simple：完成 EGARCH 或 GJR-GARCH 的基本拟合。",
            "🟡 Medium：比较标准 GARCH 与非对称模型参数和波动率路径。",
            "🔴 Strong：绘制新闻响应曲线并解释经济含义。",
            "🟣 Boss：比较不同分布假设或市场样本下的杠杆效应稳健性。"
        )
        EvaluationEmphasis = "重点看非对称结构是否解释清楚、比较是否公平，不鼓励只追求更高似然值而不解释其含义。"
        Deliverables = @(
            "README.md：说明模型选择、数据样本和比较方案。",
            "src/ 或 notebook：完成模型拟合、对照和曲线绘制。",
            "tests/：至少 1 个 smoke test，验证模型输入输出流程。",
            "report.md：说明杠杆效应是否显著、何处失败、何处有效。"
        )
        TeacherNote = "这份作业重点不在「哪个模型赢」，而在学生能否说清楚为什么要引入非对称。"
    }
    @{
        Id = "HW08"
        File = "🎓 HW08 - EVT 广义帕累托分布 (GPD) 极端黑天鹅尾部外推作业说明书.md"
        Title = "HW08 - EVT 与尾部风险外推正式作业说明书"
        Stage = "第二阶段：时间序列、期权与风控"
        Anchor = "[[极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)]]"
        Timing = "在学生完成历史模拟 VaR、参数法 VaR 并接触尾部风险问题后布置。建议放在 U08 后半段。"
        TimingReason = "此时学生已经体验过常规风险度量的不足，才会真正理解为什么尾部外推是必要而又危险的。"
        Prerequisites = @("[[历史模拟法 VaR 与非参数风险度量 (Historical Simulation VaR)]]","[[参数法VaR（方差-协方差法）.md]]","[[尾部风险]]","[[极值理论 EVT 与 POT 超过门槛模型 (Extreme Value Theory & POT Model)]]")
        Checkpoint = "学生应能解释门槛法、尾部分布和 ES 的基本含义，并理解门槛选择会显著影响结果。"
        Goals = @(
            "理解 EVT/POT 在尾部风险分析中的作用。",
            "会做门槛选择、GPD 拟合和尾部风险外推。",
            "能比较常规 VaR 与尾部外推方法的差异。",
            "形成对极端风险估计不稳定性的敬畏。"
        )
        CoreTask = "对一段收益率序列使用 POT 方法拟合尾部分布，估计极端 VaR/ES，并讨论门槛选择与结果稳定性。"
        LevelTargets = @(
            "🟢 Simple：提取尾部样本并完成基本 GPD 拟合。",
            "🟡 Medium：估计极端 VaR/ES 并与普通方法比较。",
            "🔴 Strong：分析门槛敏感性和尾部样本稳定性。",
            "🟣 Boss：将 EVT 与波动率模型结合，讨论复合风控框架。"
        )
        EvaluationEmphasis = "重点看门槛选择与尾部样本处理是否谨慎，是否报告敏感性，而不是只给出更夸张的风险数字。"
        Deliverables = @(
            "README.md：说明样本区间、门槛规则和分布假设。",
            "src/ 或 notebook：完成 POT 拟合、风险外推和敏感性分析。",
            "tests/：至少 1 个 smoke test，验证尾部样本提取与基本拟合。",
            "report.md：解释尾部估计的边界、敏感性和风险管理含义。"
        )
        TeacherNote = "批改时重点看学生有没有把‘极端样本少’这个事实当成结论解释的一部分。"
    }
    @{
        Id = "HW09"
        File = "🎓 HW09 - Tick 级数据转 Volume Bars & Dollar Bars 采样引擎作业说明书.md"
        Title = "HW09 - Volume Bars 与 Dollar Bars 采样正式作业说明书"
        Stage = "第三阶段：金融 ML、因子与回测"
        Anchor = "[[金融微观结构采样棒 (Financial Data Bars_ Volume, Dollar & Imbalance Bars in AFML)]]"
        Timing = "在学生已经做过日频收益序列分析，并理解采样方式会改变统计性质后布置。建议放在 U09 结束后。"
        TimingReason = "课程从这里开始进入研究工程层，学生必须意识到‘数据怎么切’本身就是研究设计的一部分。"
        Prerequisites = @("[[OHLCV字段清洗与复权]]","[[限价订单簿数据与 L1_L2_L3 盘口重建 (Limit Order Book Data & Reconstructing L1_L2_L3)]]","[[金融微观结构采样棒 (Financial Data Bars_ Volume, Dollar & Imbalance Bars in AFML)]]")
        Checkpoint = "学生应能解释时间 bars 与成交量 bars 的区别，并理解不同采样方式会影响序列分布特征。"
        Goals = @(
            "理解为什么金融数据采样不是中性的。",
            "会从 tick 或成交数据构造 volume bars / dollar bars。",
            "能比较不同采样方式下的统计性质差异。",
            "开始建立金融 ML 之前的数据工程意识。"
        )
        CoreTask = "从更细粒度成交数据出发，实现 volume bars 与 dollar bars 采样流程，并比较不同 bars 下收益分布、峰度或稳定性差异。"
        LevelTargets = @(
            "🟢 Simple：实现 volume bars 基本切分。",
            "🟡 Medium：实现 dollar bars，并输出对照统计结果。",
            "🔴 Strong：分析采样方式对分布、波动率或标签质量的影响。",
            "🟣 Boss：扩展到 imbalance bars 或流式采样。"
        )
        EvaluationEmphasis = "重点看采样规则是否清晰、对照是否公平、统计差异是否有解释，不只是把原始数据切成几段。"
        Deliverables = @(
            "README.md：说明原始数据结构、采样规则和运行步骤。",
            "src/ 或 notebook：实现 bars 构建和统计对照分析。",
            "tests/：至少 1 个 smoke test，验证小样本切分结果正确。",
            "report.md：说明采样方式如何影响后续研究结论。"
        )
        TeacherNote = "这份作业是进入金融 ML 前的数据观念转折点，讲评时值得花时间。"
    }
    @{
        Id = "HW10"
        File = "🎓 HW10 - HRP 层次聚类与免求逆资产配置算法作业说明书.md"
        Title = "HW10 - HRP 分层风险平价正式作业说明书"
        Stage = "第三阶段：金融 ML、因子与回测"
        Anchor = "[[分层风险平价组合 HRP (Hierarchical Risk Parity in AFML)]]"
        Timing = "在学生已经完成均值-方差配置并感受到协方差不稳定问题后布置。建议放在 U10 结束后。"
        TimingReason = "这是课程从‘理论最优’走向‘工程稳健’的关键节点，最适合用 HRP 让学生重新理解配置问题。"
        Prerequisites = @("[[马科维茨均值-方差模型]]","[[相关系数、协方差与分散化]]","[[分层风险平价组合 HRP (Hierarchical Risk Parity in AFML)]]")
        Checkpoint = "学生应能解释为什么样本协方差求逆会不稳定，以及层次聚类为何可能带来更稳健的配置。"
        Goals = @(
            "理解 HRP 的三步流程：聚类、准对角化、递归二分。",
            "会比较 HRP、MPT 和等权配置的差异。",
            "能从样本外稳健性角度评价配置方法。",
            "形成‘稳健不等于保守，稳健是工程要求’的认识。"
        )
        CoreTask = "在一组真实资产上实现 HRP，并与均值-方差配置和等权配置做样本外对照，分析回撤、换手、稳定性和矩阵问题。"
        LevelTargets = @(
            "🟢 Simple：手算相关性距离并理解聚类输入。",
            "🟡 Medium：实现完整 HRP 配置流程。",
            "🔴 Strong：做样本外对照并解释稳定性差异。",
            "🟣 Boss：加入收缩估计、行业约束或更大资产池比较。"
        )
        EvaluationEmphasis = "重点看对照设计是否公平、对样本外稳定性的讨论是否充分，不再把样本内最优权重当成高分答案。"
        Deliverables = @(
            "README.md：说明资产池、再平衡规则与对照配置方法。",
            "src/ 或 notebook：实现聚类、准对角化和权重分配。",
            "tests/：至少 1 个 smoke test，验证小规模 HRP 流程。",
            "report.md：报告样本外对照、失败案例和稳健性分析。"
        )
        TeacherNote = "如果学生做完 HW10 还执着于‘最优权重’而不看稳健性，说明配置思维还没转过来。"
    }
    @{
        Id = "HW11"
        File = "🎓 HW11 - Marchenko-Pastur 法则与高维协方差矩阵降噪作业说明书.md"
        Title = "HW11 - 协方差去噪与随机矩阵理论正式作业说明书"
        Stage = "第三阶段：金融 ML、因子与回测"
        Anchor = "[[协方差去噪与随机矩阵理论 RMT (Covariance Denoising & Marchenko-Pastur Law in AFML)]]"
        Timing = "在学生已经做过 HRP 或协方差配置，且已经感受到高维噪声问题后布置。建议放在 U10-U11 之间。"
        TimingReason = "学生此时已经知道‘矩阵有噪声’会伤害配置结果，正适合进一步理解如何系统去噪。"
        Prerequisites = @("[[相关系数、协方差与分散化]]","[[协方差去噪与随机矩阵理论 RMT (Covariance Denoising & Marchenko-Pastur Law in AFML)]]")
        Checkpoint = "学生应理解特征值、谱分解和噪声主导特征值的基本含义。"
        Goals = @(
            "理解 Marchenko-Pastur 法则和协方差去噪直觉。",
            "会对高维协方差矩阵做基础去噪处理。",
            "能比较原始矩阵和去噪矩阵对配置结果的影响。",
            "形成高维问题先看噪声结构的习惯。"
        )
        CoreTask = "在高维资产收益矩阵上估计协方差矩阵，基于 MP 法则识别噪声主导部分，并比较去噪前后的配置或风险估计差异。"
        LevelTargets = @(
            "🟢 Simple：计算特征值谱并识别 MP 上界。",
            "🟡 Medium：实现基础去噪并重构协方差矩阵。",
            "🔴 Strong：比较去噪前后的样本外配置或风险表现。",
            "🟣 Boss：结合市场因子剥离或更复杂去噪策略。"
        )
        EvaluationEmphasis = "重点看噪声识别和结果解释是否清楚，是否说明去噪为什么可能改善，也为什么可能失败。"
        Deliverables = @(
            "README.md：说明资产维度、样本长度和去噪方法。",
            "src/ 或 notebook：完成谱分析、去噪和前后对照。",
            "tests/：至少 1 个 smoke test，验证小规模矩阵流程。",
            "report.md：解释去噪效果、边界和失败情形。"
        )
        TeacherNote = "这份作业不要求学生把随机矩阵理论讲成纯数学课，但必须能把它和配置稳定性连起来。"
    }
    @{
        Id = "HW12"
        File = "🎓 HW12 - CPCV 组合净化交叉验证与回测过拟合审计作业说明书.md"
        Title = "HW12 - CPCV 与 PBO 过拟合审计正式作业说明书"
        Stage = "第三阶段：金融 ML、因子与回测"
        Anchor = "[[组合过拟合概率 PBO (Probability of Backtest Overfitting & CPCV in AFML)]]"
        Timing = "在学生已经做过至少一种策略、配置或金融 ML 研究，并学完 Purged CV 与 PBO 后布置。建议放在 U11 结束后，作为第三阶段压舱石作业。"
        TimingReason = "只有当学生亲眼见过‘看起来很漂亮的回测结果’后，才会真正理解为什么过拟合审计是硬门槛。"
        Prerequisites = @("[[Purged Group TimeSeries Cross-Validation 净化交叉验证 (Purged Group K-Fold CV)]]","[[Meta-labeling 二级标签与元标注 (Meta-labeling in Financial ML)]]","[[组合过拟合概率 PBO (Probability of Backtest Overfitting & CPCV in AFML)]]")
        Checkpoint = "学生应能解释 leakage、purging、embargo 和普通随机 CV 为什么不适合金融时间序列。"
        Goals = @(
            "理解 CPCV、purging、embargo 和 PBO 的作用。",
            "会对策略或模型进行过拟合审计，而不是只看收益。",
            "能设计公平的样本外与参数对照。",
            "形成‘先审计，再汇报收益’的研究纪律。"
        )
        CoreTask = "选择一份已有策略或模型结果，使用 CPCV / purging / embargo 做过拟合审计，并估计 PBO 或其他稳健性指标。"
        LevelTargets = @(
            "🟢 Simple：构造基本时间块并理解 purging/embargo 规则。",
            "🟡 Medium：在一个已有策略上完成 CPCV 验证流程。",
            "🔴 Strong：估计 PBO 或相关过拟合风险指标，并解释结果。",
            "🟣 Boss：比较多组参数或多模型，提出可执行的准入规则。"
        )
        EvaluationEmphasis = "重点看验证方案是否严谨、参数比较是否公平、审计结果是否真正改变了研究结论。"
        Deliverables = @(
            "README.md：说明被审计策略、时间切分和验证框架。",
            "src/ 或 notebook：实现 CPCV、purging/embargo 与风险估计。",
            "tests/：至少 1 个 smoke test，验证切分和隔离逻辑。",
            "report.md：说明审计结论、失败参数和研究准入建议。"
        )
        TeacherNote = "这份作业是进入 Qlib 或更大 Capstone 前的研究纪律门槛。"
    }
    @{
        Id = "HW13"
        File = "🎓 HW13 - 变分法推导与 Almgren-Chriss 最优拆单轨迹作业说明书.md"
        Title = "HW13 - Almgren-Chriss 最优执行正式作业说明书"
        Stage = "第四阶段：高频交易与强化学习"
        Anchor = "[[Almgren-Chriss 最优算法执行轨迹推导 (Almgren-Chriss Optimal Execution)]]"
        Timing = "在学生学完执行缺口、冲击成本和最优执行直觉后布置。建议放在 U13 开始。"
        TimingReason = "课程此时从‘做什么策略’转入‘如何真实下单’，是进入交易工程问题的第一步。"
        Prerequisites = @("[[买卖价差及其微观结构拆解 (Bid-Ask Spread & Microstructure Decomposition)]]","[[市场冲击成本模型与平方根法则 (Market Impact Models & Square-Root Law)]]","[[Implementation Shortfall 执行缺口与 Almgren-Chriss 最优执行模型.md]]","[[Almgren-Chriss 最优算法执行轨迹推导 (Almgren-Chriss Optimal Execution)]]")
        Checkpoint = "学生应能解释冲击成本、执行风险和 TWAP/VWAP 的基本区别。"
        Goals = @(
            "理解 Almgren-Chriss 的目标函数与风险-成本权衡。",
            "会计算或实现最优拆单轨迹。",
            "能比较匀速执行与最优执行的差异。",
            "开始形成执行层面的量化思维。"
        )
        CoreTask = "实现或推导 Almgren-Chriss 最优执行轨迹，并在给定订单规模与风险厌恶参数下比较执行成本与风险。"
        LevelTargets = @(
            "🟢 Simple：理解并实现风险中性匀速拆单。",
            "🟡 Medium：求解或近似实现 AC 最优轨迹。",
            "🔴 Strong：比较不同风险厌恶参数下的执行路径与成本。",
            "🟣 Boss：扩展到非线性冲击或更复杂约束。"
        )
        EvaluationEmphasis = "重点看成本-风险权衡是否真正讲清楚，不以推导写得多为唯一高分依据。"
        Deliverables = @(
            "README.md：说明模型设定、参数含义和运行方式。",
            "src/ 或 notebook：完成轨迹求解与对照模拟。",
            "tests/：至少 1 个 smoke test，验证小规模参数输入。",
            "report.md：分析执行轨迹、风险偏好和工程含义。"
        )
        TeacherNote = "批改时要看学生是否意识到‘最优执行’是约束条件下的最优，而不是无条件省钱。"
    }
    @{
        Id = "HW14"
        File = "🎓 HW14 - 暗池中点撮合与智能订单路由 (SOR) 延迟对齐作业说明书.md"
        Title = "HW14 - 暗池与智能订单路由正式作业说明书"
        Stage = "第四阶段：高频交易与强化学习"
        Anchor = "[[暗池交易与智能订单路由 SOR (Dark Pools & Smart Order Routing)]]"
        Timing = "在学生已经理解订单簿、执行成本和多交易场所路由问题后布置。建议放在 U13-U14 之间。"
        TimingReason = "学生此时已经知道执行不是单市场单价格问题，适合进一步处理多目的地与延迟对齐。"
        Prerequisites = @("[[限价订单簿数据与 L1_L2_L3 盘口重建 (Limit Order Book Data & Reconstructing L1_L2_L3)]]","[[买卖价差及其微观结构拆解 (Bid-Ask Spread & Microstructure Decomposition)]]","[[暗池交易与智能订单路由 SOR (Dark Pools & Smart Order Routing)]]")
        Checkpoint = "学生应能解释 lit market 与 dark pool 的差别，以及路由决策为什么要考虑延迟与成交概率。"
        Goals = @(
            "理解暗池中点撮合与路由逻辑。",
            "会设计简单的多市场路由规则。",
            "能把延迟、滑点和成交概率纳入执行分析。",
            "形成对交易场所异质性的工程意识。"
        )
        CoreTask = "给定多市场或多目的地报价与延迟信息，设计并评估一个简单的智能订单路由规则，比较不同路由方案的执行质量。"
        LevelTargets = @(
            "🟢 Simple：理解暗池中点撮合和最基本路由决策。",
            "🟡 Medium：实现多目的地路由规则并输出结果。",
            "🔴 Strong：加入延迟、成交概率或成本对照分析。",
            "🟣 Boss：扩展到并发扫单、复杂约束或更真实的路由框架。"
        )
        EvaluationEmphasis = "重点看路由规则是否清楚、假设是否写明、延迟与成本是否被纳入，而不是单纯追求成交量最大。"
        Deliverables = @(
            "README.md：说明市场结构、路由规则和实验设定。",
            "src/ 或 notebook：实现路由逻辑和多方案比较。",
            "tests/：至少 1 个 smoke test，验证小样本路由结果。",
            "report.md：分析路由决策、延迟影响与局限。"
        )
        TeacherNote = "这份作业非常适合老师在讲评时反复强调‘现实摩擦’。"
    }
    @{
        Id = "HW15"
        File = "🎓 HW15 - 盘口队列消耗估计与 Maker 挂单成交概率作业说明书.md"
        Title = "HW15 - 挂单成交概率与队列位置正式作业说明书"
        Stage = "第四阶段：高频交易与强化学习"
        Anchor = "[[跨市场排队优先权与挂单成交概率 (Queue Position & Fill Probability in High-Frequency Trading)]]"
        Timing = "在学生已经理解订单生命周期、价格优先时间优先和盘口消耗逻辑后布置。建议放在 U14 结束后。"
        TimingReason = "这是把学生从‘会看订单簿’推进到‘会推断自己能否成交’的关键一步。"
        Prerequisites = @("[[限价订单簿数据与 L1_L2_L3 盘口重建 (Limit Order Book Data & Reconstructing L1_L2_L3)]]","[[买卖价差及其微观结构拆解 (Bid-Ask Spread & Microstructure Decomposition)]]","[[跨市场排队优先权与挂单成交概率 (Queue Position & Fill Probability in High-Frequency Trading)]]")
        Checkpoint = "学生应能解释队列位置、时间优先规则和盘口消耗为什么决定挂单成交概率。"
        Goals = @(
            "理解队列位置和挂单成交概率的关系。",
            "会构造简单的 fill probability 估计。",
            "能比较挂单与吃单在成本和成交不确定性上的权衡。",
            "建立做市与微观结构研究的基本语言。"
        )
        CoreTask = "基于盘口或事件流数据，估计某档挂单的成交概率，并分析队列位置、撤单行为和盘口消耗对成交的影响。"
        LevelTargets = @(
            "🟢 Simple：解释价格优先时间优先并做简单队列模拟。",
            "🟡 Medium：实现基础成交概率估计流程。",
            "🔴 Strong：比较不同盘口条件下的 fill probability 变化。",
            "🟣 Boss：扩展到做市挂撤单策略或多市场场景。"
        )
        EvaluationEmphasis = "重点看成交概率估计是否有明确假设，是否考虑撤单和队列演化，而不是只做静态比例计算。"
        Deliverables = @(
            "README.md：说明数据结构、队列假设和估计方法。",
            "src/ 或 notebook：完成队列模拟或概率估计流程。",
            "tests/：至少 1 个 smoke test，验证小样本队列逻辑。",
            "report.md：说明成交概率变化、成本权衡和方法局限。"
        )
        TeacherNote = "这份作业如果只停留在静态盘口截图层面，就没有真正进入微观结构研究。"
    }
    @{
        Id = "HW16"
        File = "🎓 HW16 - Gymnasium 金融 MDP 交易环境设计与 PPO 策略作业说明书.md"
        Title = "HW16 - Gymnasium 金融交易环境与 PPO 正式作业说明书"
        Stage = "第四阶段：高频交易与强化学习"
        Anchor = "[[强化学习金融交易环境与 MDP 状态-动作空间设计 (Gym-Finance & MDP in Financial RL)]]"
        Timing = "在学生已经学完状态-动作-奖励设计、仓位控制和金融 RL 环境直觉后布置。建议放在 U15 或 RL 专题启动单元。"
        TimingReason = "只有在学生已经建立了成本、风险和验证意识之后，才适合进入强化学习环境设计，否则很容易把 RL 当作黑箱。"
        Prerequisites = @("[[动态下注规模与凯利公式 (Bet Sizing & Kelly Criterion in AFML)]]","[[动态止损机制与风险平价仓位管理 (Stop-Loss Mechanisms & Risk-Parity Position Sizing)]]","[[强化学习金融交易环境与 MDP 状态-动作空间设计 (Gym-Finance & MDP in Financial RL)]]")
        Checkpoint = "学生应能解释状态、动作、奖励、成本和训练/评估切分各自扮演什么角色。"
        Goals = @(
            "掌握金融交易环境的基本封装方式。",
            "能设计合理的状态、动作和奖励函数。",
            "会把交易成本、滑点和风险惩罚写进环境。",
            "建立对金融 RL 过拟合与不稳定性的基本警觉。"
        )
        CoreTask = "基于 Gymnasium 或兼容接口实现一个金融交易环境，定义状态、动作、奖励和成本处理，并使用 PPO 做最小可运行训练与评估。"
        LevelTargets = @(
            "🟢 Simple：构建状态向量、动作空间和基本 step 流程。",
            "🟡 Medium：封装成标准环境并跑通最小训练。",
            "🔴 Strong：加入成本、风险惩罚和更合理的奖励函数。",
            "🟣 Boss：比较 PPO / SAC 或多种奖励设计，并报告失败案例。"
        )
        EvaluationEmphasis = "重点看环境设计是否合理、训练评估是否分开、成本与风险是否进入奖励，而不是只看策略收益曲线。"
        Deliverables = @(
            "README.md：说明环境定义、状态动作设计和训练命令。",
            "src/env.py 与训练脚本或 notebook：实现环境与最小训练流程。",
            "tests/：至少 1 个 smoke test，验证 reset/step 能正常运行。",
            "report.md：分析奖励设计、训练稳定性、失败案例和局限。"
        )
        TeacherNote = "RL 作业讲评里最重要的是让学生看到：环境设计比模型名字更决定结果。"
    }
)

foreach ($spec in $specs) {
    $content = Render-Spec $spec
    $path = Join-Path $baseDir $spec.File
    Set-Content -Path $path -Value $content -Encoding utf8
}

Write-Host "Rewrote $($specs.Count) quant homework specs."
