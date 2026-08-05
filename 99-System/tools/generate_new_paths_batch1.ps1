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
        id="22"; name="概率论与数理统计"; short="概率统计"; tags=@("学习路径","概率论与数理统计","统计学")
        desc="从概率空间到统计推断的完整概率统计学习路线图"
        quote="概率论负责刻画不确定性，数理统计负责从样本中恢复规律。"
        stages=@(
            @{dir="01-概率基础"; emoji="🎲"; title="第一阶段：概率基础"; duration="4-6周"; summary="概率空间、随机变量、分布与极限定理"; topics=@("概率空间与事件|样本空间、概率公理、条件概率","随机变量与分布|常见分布、CDF/PDF、矩","期望方差与协方差|条件期望、相关与独立"); concepts=@("概率空间","随机变量","期望"); prereq=@("数学分析"); related=@("多元统计","时间序列分析","贝叶斯统计")},
            @{dir="02-抽样与分布理论"; emoji="📊"; title="第二阶段：抽样与分布理论"; duration="4-6周"; summary="抽样分布、估计量性质与经典分布族"; topics=@("抽样分布|样本均值、样本方差、统计量分布","点估计与充分统计量|无偏性、一致性、指数族","正态样本理论|t/F/卡方分布与推导"); concepts=@("抽样分布","点估计","充分统计量"); prereq=@("概率空间","随机变量"); related=@("应用回归分析","多元统计","量化金融")},
            @{dir="03-统计推断"; emoji="📈"; title="第三阶段：统计推断"; duration="5-7周"; summary="区间估计、假设检验、似然方法与线性模型"; topics=@("区间估计|置信区间、枢轴量、误差控制","假设检验|p值、功效、错误类型","极大似然与线性模型|似然函数、最小二乘、ANOVA"); concepts=@("假设检验","极大似然估计","线性模型"); prereq=@("抽样分布","点估计"); related=@("应用回归分析","机器学习","非参数统计")},
            @{dir="04-渐近理论与专题应用"; emoji="🚀"; title="第四阶段：渐近理论与专题应用"; duration="4-6周"; summary="渐近推断、重抽样与跨领域应用"; topics=@("渐近理论|Delta方法、Slutsky、估计渐近性","Bootstrap|重抽样、偏差校正、稳定性","专题应用|金融风险、A/B测试、可靠性分析"); concepts=@("渐近分布","Bootstrap","统计决策"); prereq=@("假设检验","极大似然估计"); related=@("贝叶斯统计","量化金融","机器学习")}
        )
        dims=@("🎲 概率基础维度|概率空间、随机变量、分布族、极限定理|1","📊 抽样理论维度|统计量、抽样分布、充分统计量|2","📈 推断方法维度|估计、检验、似然、线性模型|3","🚀 渐近应用维度|Bootstrap、统计决策、跨领域应用|4")
        links=@("多元统计|02-Knowledge/🧠 学习系统/16-多元统计/🗺️ 多元统计学习路径|多变量分布与协方差结构","时间序列分析|02-Knowledge/🧠 学习系统/02-时间序列分析/🗺️ 时间序列分析学习路径|随机序列建模与统计推断","量化金融|02-Knowledge/🧠 学习系统/03-量化金融/🗺️ 量化金融学习路径|风险建模与回测检验")
    },
    @{
        id="23"; name="图神经网络"; short="GNN"; tags=@("学习路径","图神经网络","深度学习")
        desc="从图结构表示到大规模图学习系统的图神经网络路线图"
        quote="GNN 把结构化关系带入表示学习，让消息沿图边传播。"
        stages=@(
            @{dir="01-图学习基础"; emoji="🕸️"; title="第一阶段：图学习基础"; duration="3-5周"; summary="图表示、谱图基础、图任务与数据管线"; topics=@("图的表示|邻接矩阵、边列表、特征张量","谱图理论|拉普拉斯矩阵、平滑性、特征向量","图学习任务|节点分类、链路预测、图分类"); concepts=@("图表示","图拉普拉斯","图任务"); prereq=@("离散数学","高等代数"); related=@("社交网络挖掘","机器学习","数据结构与算法")},
            @{dir="02-消息传递模型"; emoji="🧠"; title="第二阶段：消息传递模型"; duration="4-6周"; summary="GCN、GraphSAGE、GAT 与消息传递范式"; topics=@("GCN|谱近似、归一化邻接与层传播","GraphSAGE|采样聚合、归纳式学习","GAT|注意力机制与邻域权重学习"); concepts=@("GCN","GraphSAGE","GAT"); prereq=@("图表示","图拉普拉斯"); related=@("社交网络挖掘","NLP全栈","计算机视觉")},
            @{dir="03-任务与训练范式"; emoji="🎯"; title="第三阶段：任务与训练范式"; duration="4-6周"; summary="自监督、异质图、动态图与评估"; topics=@("图自监督学习|对比学习、遮盖任务、预训练","异质图与知识图谱|多类型节点边与关系建模","动态图建模|时序图、事件流、动态图消息传递"); concepts=@("图对比学习","异质图","动态图"); prereq=@("GCN","GraphSAGE","GAT"); related=@("时间序列分析","概率图模型","量化金融")},
            @{dir="04-前沿专题与系统实践"; emoji="🚀"; title="第四阶段：前沿专题与系统实践"; duration="4-6周"; summary="图 Transformer、大规模训练与工业应用"; topics=@("图Transformer|全局注意力与结构偏置","大规模图训练|采样、分布式训练、系统瓶颈","工业应用|推荐系统、风控网络、生物分子图"); concepts=@("图Transformer","大规模图训练","图应用"); prereq=@("图对比学习","异质图"); related=@("推荐系统","量化金融","社交网络挖掘")}
        )
        dims=@("🕸️ 图结构维度|图表示、谱图理论、任务定义|1","🧠 消息传递维度|GCN、GraphSAGE、GAT、MPNN|2","🎯 训练范式维度|自监督、异质图、动态图、评估|3","🚀 系统应用维度|图Transformer、工业落地、论文复现|4")
        links=@("社交网络挖掘|02-Knowledge/🧠 学习系统/01-社交网络挖掘/🗺️ 社交网络挖掘学习路径|图结构数据与社区关系场景","机器学习|02-Knowledge/🧠 学习系统/17-机器学习/🗺️ 机器学习学习路径|表示学习与训练范式基础","离散数学|02-Knowledge/🧠 学习系统/04-离散数学/🗺️ 离散数学学习路径|图论与组合结构基础")
    },
    @{
        id="24"; name="随机过程"; short="随机过程"; tags=@("学习路径","随机过程","概率论")
        desc="从离散随机过程到连续随机分析的系统学习路线图"
        quote="随机过程让我们不只看一个随机变量，而是看它如何随时间演化。"
        stages=@(
            @{dir="01-随机过程基础"; emoji="🎲"; title="第一阶段：随机过程基础"; duration="4-6周"; summary="过程定义、样本轨道、平稳性与滤过"; topics=@("随机过程基本概念|指标集、轨道、有限维分布","平稳性与相关函数|宽平稳、严格平稳、自协方差","滤过与条件期望|信息流、适应性、预测"); concepts=@("随机过程","平稳性","滤过"); prereq=@("概率论与数理统计"); related=@("时间序列分析","信号与系统","量化金融")},
            @{dir="02-马尔可夫与泊松过程"; emoji="🔗"; title="第二阶段：马尔可夫与泊松过程"; duration="4-6周"; summary="马尔可夫链、连续时间链与泊松过程"; topics=@("马尔可夫链|转移矩阵、平稳分布、遍历性","连续时间链|生成元与Kolmogorov方程","泊松过程与排队|独立增量、M/M/1、稳态"); concepts=@("马尔可夫链","泊松过程","排队模型"); prereq=@("随机过程","条件期望"); related=@("强化学习","运筹学","控制与机器人学")},
            @{dir="03-布朗运动与鞅"; emoji="🌊"; title="第三阶段：布朗运动与鞅"; duration="5-7周"; summary="布朗运动、停止时、鞅与二次变差"; topics=@("布朗运动|连续轨道、独立增量、缩放性质","鞅与停止时|Doob 分解、可选停止","二次变差与高斯过程|Itô 直觉与协方差结构"); concepts=@("布朗运动","鞅","二次变差"); prereq=@("马尔可夫链","泊松过程"); related=@("量化金融","贝叶斯统计","偏微分方程")},
            @{dir="04-随机微分与应用"; emoji="🚀"; title="第四阶段：随机微分与应用"; duration="4-6周"; summary="SDE、随机控制、Fokker-Planck 与应用"; topics=@("随机微分方程|Itô 形式、存在唯一性","随机控制|动态规划与 HJB 联系","应用专题|资产价格、扩散模型、状态估计"); concepts=@("随机微分方程","随机控制","Fokker-Planck"); prereq=@("布朗运动","鞅"); related=@("量化金融","控制与机器人学","偏微分方程")}
        )
        dims=@("🎲 基础过程维度|过程定义、平稳性、滤过、轨道视角|1","🔗 跳过程维度|马尔可夫链、泊松过程、排队系统|2","🌊 连续过程维度|布朗运动、鞅、二次变差|3","🚀 随机分析维度|SDE、随机控制、扩散应用|4")
        links=@("时间序列分析|02-Knowledge/🧠 学习系统/02-时间序列分析/🗺️ 时间序列分析学习路径|平稳性、自协方差与动态建模","量化金融|02-Knowledge/🧠 学习系统/03-量化金融/🗺️ 量化金融学习路径|资产价格与随机波动率模型","强化学习|02-Knowledge/🧠 学习系统/13-强化学习/🗺️ 强化学习学习路径|马尔可夫决策过程与随机控制")
    },
    @{
        id="25"; name="测度论"; short="测度论"; tags=@("学习路径","测度论","分析学")
        desc="从 σ 代数到 Lebesgue 积分与概率应用的测度论路线图"
        quote="测度论把长度、面积、概率统一到一个可推广的框架里。"
        stages=@(
            @{dir="01-可测空间基础"; emoji="📐"; title="第一阶段：可测空间基础"; duration="4-6周"; summary="σ代数、外测度、可测集与可测函数"; topics=@("σ代数与可测空间|生成 σ 代数、Borel 集","外测度与可测性|Carathéodory 构造","Lebesgue 测度|零测集、完备化、平移不变性"); concepts=@("σ代数","Lebesgue测度","可测函数"); prereq=@("数学分析","实变函数"); related=@("概率论与数理统计","实变函数","随机过程")},
            @{dir="02-积分与收敛"; emoji="📏"; title="第二阶段：积分与收敛"; duration="4-6周"; summary="Lebesgue 积分、收敛定理与 Fubini"; topics=@("Lebesgue 积分|简单函数逼近与积分定义","收敛定理|单调收敛、Fatou、控制收敛","乘积测度与 Fubini|迭代积分与变量交换"); concepts=@("Lebesgue积分","控制收敛定理","Fubini定理"); prereq=@("可测函数","Lebesgue测度"); related=@("实变函数","偏微分方程","贝叶斯统计")},
            @{dir="03-Lp空间与结构"; emoji="🧮"; title="第三阶段：Lp空间与结构"; duration="4-6周"; summary="Lp 空间、Radon-Nikodym 与条件期望"; topics=@("Lp 空间|范数、完备性、Holder 与 Minkowski","符号测度与 Radon-Nikodym|密度函数与绝对连续","条件期望的测度论视角|投影与信息更新"); concepts=@("Lp空间","Radon-Nikodym","条件期望"); prereq=@("Lebesgue积分","Fubini定理"); related=@("泛函分析","概率论与数理统计","随机过程")},
            @{dir="04-概率与分析应用"; emoji="🚀"; title="第四阶段：概率与分析应用"; duration="4-6周"; summary="概率测度、弱收敛与分析应用"; topics=@("概率测度|分布律与期望的积分表达","弱收敛与紧性|Portmanteau 思想与极限定理准备","分析应用|Fourier、Sobolev、PDE 准备"); concepts=@("概率测度","弱收敛","紧性"); prereq=@("Lp空间","Radon-Nikodym"); related=@("随机过程","贝叶斯统计","泛函分析")}
        )
        dims=@("📐 可测结构维度|σ代数、外测度、Lebesgue测度、可测函数|1","📏 积分收敛维度|Lebesgue积分、收敛定理、Fubini|2","🧮 空间结构维度|Lp空间、Radon-Nikodym、条件期望|3","🚀 概率应用维度|概率测度、弱收敛、分析准备|4")
        links=@("实变函数|02-Knowledge/🧠 学习系统/26-实变函数/🗺️ 实变函数学习路径|Lebesgue 理论与微分积分深化","泛函分析|02-Knowledge/🧠 学习系统/27-泛函分析/🗺️ 泛函分析学习路径|Lp 空间与算子视角","随机过程|02-Knowledge/🧠 学习系统/24-随机过程/🗺️ 随机过程学习路径|条件期望、鞅与概率测度")
    }
)

foreach ($subject in $subjects) { New-PathFiles $subject }
Write-Output "Generated batch 1."
