$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$root = "C:\Users\32110\Documents\GitHub\-\02-Knowledge/🧠 学习系统"
$today = "2026-04-12"

function Ensure-Dir([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

function Write-File([string]$Path, [string]$Content) {
    Ensure-Dir (Split-Path -Parent $Path)
    Set-Content -LiteralPath $Path -Value $Content -Encoding utf8
}

function YA($Items) {
    if (-not $Items -or $Items.Count -eq 0) { return "[]" }
    "[" + (($Items | ForEach-Object { '"' + $_ + '"' }) -join ", ") + "]"
}

function Pair([string]$Value) { $Value -split "\|" }

function New-PathFiles($subject) {
    $base = Join-Path $root ("{0}-{1}" -f $subject.id, $subject.name)
    Ensure-Dir $base
    Ensure-Dir (Join-Path $base "知识地图")

    $progressJs = @()
    $stageRows = @()
    $stageLinks = @()
    $dimRows = @()
    $linkRows = @()
    $sumDone = @()
    $sumTotal = @()

    for ($i = 0; $i -lt $subject.stages.Count; $i++) {
        $stage = $subject.stages[$i]
        $dir = Join-Path $base $stage.dir
        Ensure-Dir $dir

        $stageFile = Join-Path $dir ("{0} {1}.md" -f $stage.emoji, $stage.title)
        $progressJs += "const stage$($i+1) = dv.pages('" + '"02-Knowledge/🧠 学习系统/' + $subject.id + '-' + $subject.name + '/' + $stage.dir + '"' + "').where(p => p.status === `"completed`").length;"
        $progressJs += "const stage$($i+1)Total = dv.pages('" + '"02-Knowledge/🧠 学习系统/' + $subject.id + '-' + $subject.name + '/' + $stage.dir + '"' + "').length;"
        $sumDone += "stage$($i+1)"
        $sumTotal += "stage$($i+1)Total"
        $stageRows += "| $($stage.emoji) | **第$($i+1)阶段** | $($stage.duration) | $($stage.summary) | [[{0}/{1} {2}\|进入]] |" -f $stage.dir, $stage.emoji, $stage.title
        $stageLinks += "- [[{0}/{1} {2}\|{1} {2}]]" -f $stage.dir, $stage.emoji, $stage.title

        $topicRows = @()
        foreach ($topic in $stage.topics) {
            $parts = Pair $topic
            $topicRows += "| **$($parts[0])** | $($parts[1]) | ⬜ | [[$($parts[0])]] |"
        }

        $prev = if ($i -eq 0) { "-" } else { "[[$($subject.stages[$i-1].emoji) $($subject.stages[$i-1].title)\|进入上一阶段]]" }
        $next = if ($i -eq $subject.stages.Count - 1) { "-" } else { "[[$($subject.stages[$i+1].emoji) $($subject.stages[$i+1].title)\|进入下一阶段]]" }

        $stageContent = @"
---
tags: [$($subject.name), 阶段$($i+1), $($subject.short)]
created: $today
status: ongoing
phase: $($i+1)
duration: "$($stage.duration)"
topic: "$($subject.name)-$($stage.title)"
concept: $(YA $stage.concepts)
prerequisites: $(YA $stage.prereq)
related: $(YA $stage.related)
---

# $($stage.emoji) $($stage.title)

> $($stage.summary)

## 📊 阶段进度

~~~dataviewjs
const notes = dv.pages('"02-Knowledge/🧠 学习系统/$($subject.id)-$($subject.name)/$($stage.dir)"').where(p => !p.file.path.includes("$($stage.emoji)"));
const completed = notes.where(p => p.status === "completed").length;
const total = notes.length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph("**阶段进度: " + progress + "%** (" + completed + "/" + total + " 主题)");
~~~

## 📖 学习模块

| 主题 | 核心内容 | 状态 | 笔记 |
|:---|:---|:---:|:---|
$($topicRows -join "`n")

## 🎯 阶段任务

- [ ] 完成至少 3 个主题笔记
- [ ] 为本阶段补上 concept 与 related 连接
- [ ] 复盘本阶段与其他路径的交叉知识

## 🔗 阶段导航

| ⬅️ 上一阶段 | 📋 总览 | 下一阶段 ➡️ |
|:---:|:---:|:---:|
| $prev | [[🗺️ $($subject.name)学习路径\|返回总览]] | $next |

*阶段创建：$today*
"@
        Write-File $stageFile $stageContent
    }

    foreach ($dim in $subject.dims) {
        $parts = Pair $dim
        $dimRows += "| **$($parts[0])** | $($parts[1]) | $($parts[2]) |"
    }

    foreach ($link in $subject.links) {
        $parts = Pair $link
        $linkRows += "| [[{0}\|{1}]] | {2} |" -f $parts[1], $parts[0], $parts[2]
    }

    $pathContent = @"
---
tags: $(YA $subject.tags)
created: $today
description: "$($subject.desc)"
---

# 🗺️ $($subject.name)学习路径

> "$($subject.quote)"

~~~dataviewjs
$($progressJs -join "`n")
const totalCompleted = $($sumDone -join " + ");
const totalNotes = $($sumTotal -join " + ");
const totalProgress = totalNotes > 0 ? Math.round((totalCompleted / totalNotes) * 100) : 0;
dv.paragraph("**总体进度: " + totalProgress + "%** | 已完成: " + totalCompleted + " / " + totalNotes + " 主题");
~~~

## 🎯 双索引系统

| 索引类型 | 说明 | 入口 |
|:---|:---|:---|
| **📈 纵向路线** | 四阶段递进，从基础到专题应用 | 见下方阶段导航 |
| **🗺️ 横向知识地图** | 从对象、方法、工具与应用整理知识 | [[知识地图/🗺️ 横向知识地图\|知识地图]] |

## 📈 纵向四阶段

| 阶段 | 周期 | 核心内容 | 入口 |
|:---:|:---:|:---|:---:|
$($stageRows -join "`n")

## 🗺️ 横向知识地图

| 维度 | 核心内容 | 关联阶段 |
|:---|:---|:---:|
$($dimRows -join "`n")

## 🔗 关联路径

| 路径 | 连接说明 |
|:---|:---|
$($linkRows -join "`n")

## 🔗 快速导航

### 纵向路线
$($stageLinks -join "`n")

### 横向知识地图
- [[知识地图/🗺️ 横向知识地图\|🗺️ 横向知识地图总览]]

*路线图更新：$today*
"@
    Write-File (Join-Path $base ("🗺️ {0}学习路径.md" -f $subject.name)) $pathContent

    $mapSections = @()
    foreach ($dim in $subject.dims) {
        $parts = Pair $dim
        $mapSections += "## {0}`n`n- 核心内容：{1}`n- 关联阶段：{2}`n- 建议动作：围绕该维度补全原子笔记与概念连接。`n" -f $parts[0], $parts[1], $parts[2]
    }

    $linkBullets = @()
    foreach ($link in $subject.links) {
        $parts = Pair $link
        $linkBullets += "- [[{0}\|{1}]]：{2}" -f $parts[1], $parts[0], $parts[2]
    }

    $mapContent = @"
---
tags: [$($subject.name), 知识地图, 横向索引]
created: $today
description: "$($subject.name)的横向知识地图"
---

# 🗺️ 横向知识地图

> "$($subject.quote)"

| 维度 | 核心内容 | 关联阶段 |
|:---|:---|:---:|
$($dimRows -join "`n")

$($mapSections -join "`n")

## 🔗 推荐联动路径

$($linkBullets -join "`n")

*知识地图更新：$today*
"@
    Write-File (Join-Path $base "知识地图\🗺️ 横向知识地图.md") $mapContent
}

$subjects = @(
    @{
        id="30"; name="应用回归分析"; short="回归分析"; tags=@("学习路径","应用回归分析","统计建模")
        desc="从经典线性回归到诊断、推广与实践的应用回归分析路线图"
        quote="回归分析的核心不只是拟合一条线，而是解释关系、控制偏差并进行预测。"
        stages=@(
            @{dir="01-线性回归基础"; emoji="📈"; title="第一阶段：线性回归基础"; duration="4-6周"; summary="最小二乘、参数解释、区间推断与 ANOVA"; topics=@("简单与多元线性回归|模型设定、参数含义、拟合目标","最小二乘估计|正规方程、几何解释、方差分解","推断与 ANOVA|t/F 检验、解释度、报告方式"); concepts=@("线性回归","最小二乘","方差分析"); prereq=@("概率论与数理统计","高等代数"); related=@("机器学习","量化金融","多元统计")},
            @{dir="02-诊断与变量选择"; emoji="🔍"; title="第二阶段：诊断与变量选择"; duration="4-6周"; summary="模型诊断、多重共线性与变量筛选"; topics=@("残差诊断|线性性、同方差、正态性、独立性","异常点与影响点|杠杆值、Cook 距离、稳健处理","变量选择|VIF、逐步法、信息准则、交叉验证"); concepts=@("残差诊断","多重共线性","变量选择"); prereq=@("线性回归","最小二乘"); related=@("机器学习","数值分析","非参数统计")},
            @{dir="03-广义与层次扩展"; emoji="🧩"; title="第三阶段：广义与层次扩展"; duration="4-6周"; summary="GLM、混合效应、面板与时序回归"; topics=@("广义线性模型|链接函数、指数族、IRLS 直觉","Logistic/Poisson 回归|分类与计数建模","混合效应与面板扩展|层次结构、随机效应、固定效应"); concepts=@("广义线性模型","Logistic回归","混合效应模型"); prereq=@("残差诊断","变量选择"); related=@("属性数据分析","贝叶斯统计","时间序列分析")},
            @{dir="04-因果与预测实践"; emoji="🚀"; title="第四阶段：因果与预测实践"; duration="4-6周"; summary="因果识别、预测评估与行业案例"; topics=@("因果回归视角|混杂、控制变量、DID 直觉","预测评估|训练验证划分、偏差方差、校准","实践案例|营销、金融、医学与政策评估"); concepts=@("因果推断","预测评估","回归解释"); prereq=@("广义线性模型","Logistic回归"); related=@("机器学习","量化金融","贝叶斯统计")}
        )
        dims=@("📈 经典回归维度|线性回归、最小二乘、ANOVA、推断|1","🔍 诊断选择维度|残差、共线性、异常点、变量筛选|2","🧩 模型扩展维度|GLM、Logistic、混合效应、面板回归|3","🚀 因果实践维度|因果识别、预测评估、行业应用|4")
        links=@("机器学习|02-Knowledge/🧠 学习系统/17-机器学习/🗺️ 机器学习学习路径|监督学习、正则化与泛化评估","属性数据分析|02-Knowledge/🧠 学习系统/31-属性数据分析/🗺️ 属性数据分析学习路径|Logistic/Poisson 与列联表分析","贝叶斯统计|02-Knowledge/🧠 学习系统/33-贝叶斯统计/🗺️ 贝叶斯统计学习路径|层次回归与后验不确定性")
    },
    @{
        id="31"; name="属性数据分析"; short="属性数据"; tags=@("学习路径","属性数据分析","统计建模")
        desc="从列联表到离散响应模型与相关数据分析的属性数据路线图"
        quote="属性数据分析关注的是类别、计数和离散响应，而不是连续数值。"
        stages=@(
            @{dir="01-列联表与二分类"; emoji="📋"; title="第一阶段：列联表与二分类"; duration="3-5周"; summary="列联表、比例比较、优势比与基本检验"; topics=@("列联表基础|频数、边际分布、条件分布","比例比较与卡方检验|独立性检验与拟合优度","优势比与相对风险|二分类响应解释"); concepts=@("列联表","优势比","卡方检验"); prereq=@("概率论与数理统计"); related=@("应用回归分析","贝叶斯统计","非参数统计")},
            @{dir="02-Logistic与Poisson模型"; emoji="📊"; title="第二阶段：Logistic与Poisson模型"; duration="4-6周"; summary="二分类、计数数据与对数线性模型"; topics=@("Logistic 回归|logit 链接、系数解释、拟合","Poisson 回归|计数率、暴露量、过度离散","对数线性模型|多维列联表与交互结构"); concepts=@("Logistic回归","Poisson回归","对数线性模型"); prereq=@("列联表","优势比"); related=@("应用回归分析","机器学习","非参数统计")},
            @{dir="03-多分类与相关响应"; emoji="🔗"; title="第三阶段：多分类与相关响应"; duration="4-6周"; summary="多项响应、序数模型、GEE 与随机效应"; topics=@("多分类 Logit|基线类、嵌套选择","序数响应模型|比例优势与阈值结构","相关离散数据|GEE、重复测量、GLMM 入口"); concepts=@("多分类Logit","序数模型","GEE"); prereq=@("Logistic回归","Poisson回归"); related=@("应用回归分析","贝叶斯统计","时间序列分析")},
            @{dir="04-专题实践与解释"; emoji="🚀"; title="第四阶段：专题实践与解释"; duration="4-5周"; summary="边际效应、抽样加权与分类决策"; topics=@("边际效应与可解释性|OR 转概率、交互项解释","调查与抽样加权|复杂抽样设计处理","分类阈值与实践|ROC、PR、成本敏感分析"); concepts=@("边际效应","抽样加权","分类阈值"); prereq=@("多分类Logit","GEE"); related=@("机器学习","量化金融","贝叶斯统计")}
        )
        dims=@("📋 列联表维度|频数结构、卡方检验、优势比|1","📊 离散响应维度|Logistic、Poisson、对数线性模型|2","🔗 相关响应维度|多分类、序数、GEE、GLMM|3","🚀 实践解释维度|边际效应、加权设计、行业案例|4")
        links=@("应用回归分析|02-Knowledge/🧠 学习系统/30-应用回归分析/🗺️ 应用回归分析学习路径|广义线性模型与诊断基础","贝叶斯统计|02-Knowledge/🧠 学习系统/33-贝叶斯统计/🗺️ 贝叶斯统计学习路径|离散响应的先验建模与层次扩展","机器学习|02-Knowledge/🧠 学习系统/17-机器学习/🗺️ 机器学习学习路径|分类评估、阈值选择与泛化")
    },
    @{
        id="32"; name="非参数统计"; short="非参数统计"; tags=@("学习路径","非参数统计","统计建模")
        desc="从秩统计到核方法与 Bootstrap 的非参数统计路线图"
        quote="非参数统计在更少分布假设下做推断，代价是更依赖样本与算法。"
        stages=@(
            @{dir="01-经验分布与秩统计"; emoji="📏"; title="第一阶段：经验分布与秩统计"; duration="3-5周"; summary="经验分布函数、秩变换与经典检验"; topics=@("经验分布函数|一致收敛与 EDF 直觉","秩统计基础|顺序统计量、分位数、秩和","单样本/两样本检验|符号、Wilcoxon、KS"); concepts=@("经验分布函数","秩统计","Wilcoxon检验"); prereq=@("概率论与数理统计"); related=@("应用回归分析","属性数据分析","贝叶斯统计")},
            @{dir="02-经典非参数推断"; emoji="🧪"; title="第二阶段：经典非参数推断"; duration="4-6周"; summary="多样本检验、相关检验与稳健统计"; topics=@("多样本比较|Kruskal-Wallis、Friedman","相关与趋势检验|Spearman、Kendall","稳健统计视角|中位数、MAD、离群影响"); concepts=@("Kruskal-Wallis","Spearman相关","稳健统计"); prereq=@("经验分布函数","秩统计"); related=@("时间序列分析","量化金融","应用回归分析")},
            @{dir="03-平滑与估计"; emoji="🌿"; title="第三阶段：平滑与估计"; duration="4-6周"; summary="核密度估计、核回归、样条与局部平滑"; topics=@("核密度估计|带宽选择、偏差方差权衡","核回归与局部多项式|非线性关系拟合","样条与光滑惩罚|平滑样条与 GAM 入口"); concepts=@("核密度估计","核回归","样条平滑"); prereq=@("Kruskal-Wallis","稳健统计"); related=@("机器学习","应用回归分析","数值分析")},
            @{dir="04-Bootstrap与现代应用"; emoji="🚀"; title="第四阶段：Bootstrap与现代应用"; duration="4-5周"; summary="Bootstrap、置换检验与半参数模型"; topics=@("Bootstrap 方法|区间估计、偏差校正、稳定性","置换检验|实验设计与无分布假设推断","半参数模型与实践|部分线性模型、金融/医学案例"); concepts=@("Bootstrap","置换检验","半参数模型"); prereq=@("核密度估计","核回归"); related=@("贝叶斯统计","量化金融","机器学习")}
        )
        dims=@("📏 经验分布维度|EDF、秩统计、单样本/两样本检验|1","🧪 推断检验维度|多样本比较、相关检验、稳健统计|2","🌿 平滑估计维度|核方法、局部回归、样条|3","🚀 重抽样应用维度|Bootstrap、置换检验、半参数实践|4")
        links=@("应用回归分析|02-Knowledge/🧠 学习系统/30-应用回归分析/🗺️ 应用回归分析学习路径|模型失配时的稳健替代方案","时间序列分析|02-Knowledge/🧠 学习系统/02-时间序列分析/🗺️ 时间序列分析学习路径|分布检验与重抽样验证","机器学习|02-Knowledge/🧠 学习系统/17-机器学习/🗺️ 机器学习学习路径|核方法与偏差方差权衡")
    },
    @{
        id="33"; name="贝叶斯统计"; short="贝叶斯统计"; tags=@("学习路径","贝叶斯统计","统计建模")
        desc="从先验后验到 MCMC、层次模型与决策分析的贝叶斯统计路线图"
        quote="贝叶斯统计把学习写成更新，把不确定性保留到最后一步决策。"
        stages=@(
            @{dir="01-贝叶斯基础"; emoji="🎲"; title="第一阶段：贝叶斯基础"; duration="4-6周"; summary="先验、后验、共轭族与后验预测"; topics=@("Bayes 公式重述|先验、似然、后验、证据","共轭先验家族|Beta-Binomial、Gamma-Poisson、Normal-Normal","后验预测分布|预测不确定性与模型比较"); concepts=@("先验","后验","共轭先验"); prereq=@("概率论与数理统计"); related=@("概率图模型","应用回归分析","量化金融")},
            @{dir="02-计算贝叶斯"; emoji="⚙️"; title="第二阶段：计算贝叶斯"; duration="4-6周"; summary="MCMC、Gibbs、MH 与变分近似"; topics=@("MCMC 基础|马尔可夫链、平稳分布、收敛诊断","MH/Gibbs 采样|提议分布、条件后验、混合性","变分 Bayes 初步|ELBO 与近似推断直觉"); concepts=@("MCMC","Gibbs采样","变分Bayes"); prereq=@("先验","后验","马尔可夫链"); related=@("概率图模型","随机过程","机器学习")},
            @{dir="03-层次模型与回归"; emoji="🏗️"; title="第三阶段：层次模型与回归"; duration="4-6周"; summary="贝叶斯回归、层次建模与模型比较"; topics=@("贝叶斯线性回归|后验解析与正则化联系","层次模型|部分汇聚、群组效应、超先验","模型比较与平均|Bayes 因子、WAIC、模型平均"); concepts=@("贝叶斯回归","层次模型","Bayes因子"); prereq=@("MCMC","变分Bayes"); related=@("应用回归分析","属性数据分析","机器学习")},
            @{dir="04-决策与实践"; emoji="🚀"; title="第四阶段：决策与实践"; duration="4-6周"; summary="Bayes 决策、时序/金融应用与工具链"; topics=@("Bayes 决策论|损失函数、后验风险、价值信息","贝叶斯时序模型|动态线性模型、状态空间","Stan/PyMC 实践|建模、诊断与报告"); concepts=@("Bayes决策","动态线性模型","Stan/PyMC"); prereq=@("贝叶斯回归","层次模型"); related=@("量化金融","时间序列分析","概率图模型")}
        )
        dims=@("🎲 基础更新维度|先验、后验、共轭族、后验预测|1","⚙️ 计算推断维度|MCMC、Gibbs、MH、变分 Bayes|2","🏗️ 层次建模维度|贝叶斯回归、层次模型、模型比较|3","🚀 决策实践维度|Bayes 风险、动态模型、Stan/PyMC|4")
        links=@("概率图模型|02-Knowledge/🧠 学习系统/14-概率图模型/🗺️ 概率图模型学习路径|图结构上的贝叶斯推断与学习","应用回归分析|02-Knowledge/🧠 学习系统/30-应用回归分析/🗺️ 应用回归分析学习路径|回归模型的不确定性表达","量化金融|02-Knowledge/🧠 学习系统/03-量化金融/🗺️ 量化金融学习路径|贝叶斯资产配置与动态风险更新")
    }
)

foreach ($subject in $subjects) { New-PathFiles $subject }
Write-Output "Generated batch 3."
