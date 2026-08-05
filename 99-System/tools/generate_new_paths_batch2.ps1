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
        id="26"; name="实变函数"; short="实变函数"; tags=@("学习路径","实变函数","分析学")
        desc="从 Lebesgue 理论到函数空间与 Fourier 分析的实变函数路线图"
        quote="实变函数让微积分真正进入严格而强大的现代分析框架。"
        stages=@(
            @{dir="01-实数与点集基础"; emoji="🔍"; title="第一阶段：实数与点集基础"; duration="4-5周"; summary="实数完备性、紧致性与函数列收敛"; topics=@("实数完备性|上确界、Cauchy 列、Bolzano-Weierstrass","点集拓扑基础|开闭集、紧集、完备性","函数列收敛|逐点/一致收敛与极限交换"); concepts=@("完备性","紧致性","一致收敛"); prereq=@("数学分析"); related=@("测度论","数学分析","泛函分析")},
            @{dir="02-Lebesgue理论"; emoji="📏"; title="第二阶段：Lebesgue理论"; duration="4-6周"; summary="可测集、积分与收敛定理"; topics=@("可测集与可测函数|σ代数、简单函数、近似思想","Lebesgue 积分|与 Riemann 积分比较","积分收敛定理|Fatou、控制收敛、Egorov/Lusin"); concepts=@("Lebesgue积分","可测函数","收敛定理"); prereq=@("完备性","一致收敛"); related=@("测度论","概率论与数理统计","偏微分方程")},
            @{dir="03-微分与函数空间"; emoji="📈"; title="第三阶段：微分与函数空间"; duration="4-6周"; summary="BV/AC 函数、弱导数与 Sobolev 初步"; topics=@("有界变差与绝对连续|BV、AC 与微积分联系","Lebesgue 微分定理|几乎处处恢复函数值","Sobolev 初步|弱导数、函数空间与逼近"); concepts=@("绝对连续","弱导数","Sobolev空间"); prereq=@("Lebesgue积分","收敛定理"); related=@("泛函分析","偏微分方程","数值分析")},
            @{dir="04-Fourier与应用"; emoji="🚀"; title="第四阶段：Fourier与应用"; duration="4-6周"; summary="Fourier 级数、卷积与现代分析应用"; topics=@("Fourier 级数|收敛性、Parseval、逼近","卷积与核函数|平滑、逼近恒等式","应用专题|PDE、信号处理、概率中的 Fourier 工具"); concepts=@("Fourier级数","卷积","最大函数"); prereq=@("绝对连续","Sobolev空间"); related=@("信号与系统","偏微分方程","随机过程")}
        )
        dims=@("🔍 点集基础维度|完备性、紧致性、函数列收敛|1","📏 Lebesgue维度|可测集、积分、收敛定理|2","📈 函数空间维度|BV/AC、弱导数、Sobolev|3","🚀 Fourier应用维度|卷积、级数与 PDE/信号应用|4")
        links=@("数学分析|02-Knowledge/🧠 学习系统/28-数学分析/🗺️ 数学分析学习路径|极限、连续与严格证明基础","测度论|02-Knowledge/🧠 学习系统/25-测度论/🗺️ 测度论学习路径|可测与积分框架","偏微分方程|02-Knowledge/🧠 学习系统/34-偏微分方程/🗺️ 偏微分方程学习路径|弱解、Fourier 方法与正则性")
    },
    @{
        id="27"; name="泛函分析"; short="泛函分析"; tags=@("学习路径","泛函分析","分析学")
        desc="从赋范空间到算子理论与变分方法的泛函分析路线图"
        quote="泛函分析把无穷维线性代数变成研究方程和优化的核心工具。"
        stages=@(
            @{dir="01-赋范空间基础"; emoji="📐"; title="第一阶段：赋范空间基础"; duration="4-6周"; summary="赋范空间、Banach 空间、子空间与商空间"; topics=@("赋范线性空间|范数、等价范数、连续性","Banach 空间|完备性、稠密性、典型例子","子空间与商空间|闭子空间、商范数、投影"); concepts=@("赋范空间","Banach空间","商空间"); prereq=@("高等代数","实变函数"); related=@("测度论","最优化方法","数值分析")},
            @{dir="02-Hilbert与基本定理"; emoji="🏗️"; title="第二阶段：Hilbert与基本定理"; duration="4-6周"; summary="Hilbert 空间、投影、Riesz 与三大基本定理"; topics=@("Hilbert 空间|内积、正交分解、完备正交系","Riesz 表示与投影定理|几何最优逼近","Hahn-Banach/开映射/闭图像|连续线性泛函与结构结论"); concepts=@("Hilbert空间","Riesz表示","Hahn-Banach"); prereq=@("赋范空间","Banach空间"); related=@("最优化方法","信号与系统","机器学习")},
            @{dir="03-算子与谱理论"; emoji="🔬"; title="第三阶段：算子与谱理论"; duration="5-7周"; summary="有界算子、紧算子、自伴算子与谱结构"; topics=@("线性算子基础|算子范数、连续性、伴随算子","紧算子与 Fredholm 思想|有限秩逼近与谱离散性","自伴与正规算子|谱分解与函数演算直观"); concepts=@("有界算子","紧算子","谱理论"); prereq=@("Hilbert空间","Riesz表示"); related=@("偏微分方程","控制与机器人学","量化金融")},
            @{dir="04-变分方法与应用"; emoji="🚀"; title="第四阶段：变分方法与应用"; duration="4-6周"; summary="弱收敛、凸泛函、Lax-Milgram 与 PDE/优化应用"; topics=@("弱拓扑与弱收敛|紧性、反身性、存在性框架","凸泛函与最小化|下半连续性与直接方法","Lax-Milgram 与应用|椭圆问题、控制与逆问题"); concepts=@("弱收敛","凸泛函","Lax-Milgram"); prereq=@("有界算子","谱理论","Sobolev空间"); related=@("偏微分方程","最优化方法","控制与机器人学")}
        )
        dims=@("📐 空间结构维度|赋范空间、Banach空间、商空间|1","🏗️ 基本定理维度|Hilbert空间、Riesz、Hahn-Banach|2","🔬 算子谱维度|有界算子、紧算子、自伴谱理论|3","🚀 变分应用维度|弱收敛、Lax-Milgram、优化与 PDE|4")
        links=@("偏微分方程|02-Knowledge/🧠 学习系统/34-偏微分方程/🗺️ 偏微分方程学习路径|弱解、谱与半群方法","最优化方法|02-Knowledge/🧠 学习系统/07-最优化方法/🗺️ 最优化方法学习路径|凸泛函与最小化观点","数值分析|02-Knowledge/🧠 学习系统/35-数值分析/🗺️ 数值分析学习路径|有限维逼近与误差分析")
    },
    @{
        id="28"; name="数学分析"; short="数学分析"; tags=@("学习路径","数学分析","基础数学")
        desc="从严格极限到多元微积分与级数理论的数学分析路线图"
        quote="数学分析训练的不只是计算，而是严密表达、反例意识与极限直觉。"
        stages=@(
            @{dir="01-极限与连续"; emoji="📘"; title="第一阶段：极限与连续"; duration="4-6周"; summary="数列、函数极限、连续性与一元微分"; topics=@("数列与函数极限|夹逼、Cauchy、ε-δ","连续与间断|闭区间性质、连续函数结构","导数与均值定理|单调性、极值、L'Hospital"); concepts=@("极限","连续性","导数"); prereq=@(); related=@("常微分方程","概率论与数理统计","数值分析")},
            @{dir="02-级数理论"; emoji="📗"; title="第二阶段：级数理论"; duration="4-6周"; summary="数项级数、函数项级数、Taylor 与 Fourier 初步"; topics=@("数项级数|敛散判别、绝对收敛、条件收敛","函数项级数|一致收敛与交换极限","幂级数与 Taylor/Fourier 初步|展开、逼近与解析性"); concepts=@("级数","一致收敛","Taylor展开"); prereq=@("极限","连续性","导数"); related=@("实变函数","信号与系统","偏微分方程")},
            @{dir="03-多元微积分"; emoji="📙"; title="第三阶段：多元微积分"; duration="4-6周"; summary="多元极限、梯度、重积分与向量分析基础"; topics=@("多元极限与连续|路径依赖、偏导存在性","梯度与 Jacobian|链式法则、隐函数直观","重积分与变量替换|Fubini、Jacobian、曲面积分初步"); concepts=@("多元微积分","梯度","重积分"); prereq=@("级数","导数"); related=@("最优化方法","常微分方程","机器学习")},
            @{dir="04-严格证明与专题"; emoji="📕"; title="第四阶段：严格证明与专题"; duration="4-6周"; summary="证明组织、反例构造与后续分析课程准备"; topics=@("证明方法专题|反证、构造、归纳、紧致性套路","极限交换专题|积分、求和、微分交换条件","课程衔接|实变、测度、泛函、PDE 准备"); concepts=@("严格证明","紧致性","极限交换"); prereq=@("一致收敛","多元微积分"); related=@("实变函数","测度论","偏微分方程")}
        )
        dims=@("📘 极限基础维度|数列、极限、连续、导数|1","📗 级数维度|数项级数、函数项级数、Taylor/Fourier|2","📙 多元微积分维度|梯度、重积分、向量分析|3","📕 证明训练维度|极限交换、经典定理、后续衔接|4")
        links=@("常微分方程|02-Knowledge/🧠 学习系统/06-常微分方程/🗺️ 常微分方程学习路径|存在唯一性与级数解基础","最优化方法|02-Knowledge/🧠 学习系统/07-最优化方法/🗺️ 最优化方法学习路径|梯度、Hessian 与泰勒展开","数值分析|02-Knowledge/🧠 学习系统/35-数值分析/🗺️ 数值分析学习路径|误差估计与近似展开工具")
    },
    @{
        id="29"; name="运筹学"; short="运筹学"; tags=@("学习路径","运筹学","优化")
        desc="从线性规划到随机优化与决策建模的运筹学路线图"
        quote="运筹学研究的是在资源受限、约束复杂的环境中如何做更好的决策。"
        stages=@(
            @{dir="01-线性规划基础"; emoji="📊"; title="第一阶段：线性规划基础"; duration="4-6周"; summary="建模、单纯形法、对偶理论与敏感性分析"; topics=@("线性规划建模|变量、目标函数、约束表达","单纯形法|基可行解、换基、几何解释","对偶与敏感性分析|影子价格、资源扰动解释"); concepts=@("线性规划","单纯形法","对偶"); prereq=@("高等代数","最优化方法"); related=@("量化金融","控制与机器人学","数值分析")},
            @{dir="02-整数与网络优化"; emoji="🕸️"; title="第二阶段：整数与网络优化"; duration="4-6周"; summary="整数规划、分支定界、最短路与最大流"; topics=@("整数规划|0-1 规划、松弛、割平面直观","分支定界与启发式|搜索树与近似思想","网络优化模型|最短路、最大流、最小费用流"); concepts=@("整数规划","分支定界","网络优化"); prereq=@("线性规划","对偶"); related=@("数据结构与算法","图神经网络","量化金融")},
            @{dir="03-随机与动态决策"; emoji="🧭"; title="第三阶段：随机与动态决策"; duration="4-6周"; summary="排队、库存、MDP 与仿真优化"; topics=@("排队论|到达过程、服务系统、性能指标","库存控制|EOQ、(s,S) 策略、需求不确定性","动态规划与 MDP|Bellman 方程与策略结构"); concepts=@("排队论","库存控制","动态规划"); prereq=@("整数规划","网络优化","随机过程"); related=@("强化学习","控制与机器人学","随机过程")},
            @{dir="04-随机优化与实践"; emoji="🚀"; title="第四阶段：随机优化与实践"; duration="4-6周"; summary="鲁棒优化、随机规划、多目标决策与行业案例"; topics=@("随机规划|场景法、两阶段模型、样本平均近似","鲁棒优化|不确定集合、最坏情形决策","实践专题|供应链、交通调度、投资组合"); concepts=@("随机规划","鲁棒优化","多目标优化"); prereq=@("排队论","动态规划","最优化方法"); related=@("量化金融","最优化方法","控制与机器人学")}
        )
        dims=@("📊 规划建模维度|线性规划、单纯形法、对偶、敏感性|1","🕸️ 离散网络维度|整数规划、网络流、匹配分配|2","🧭 动态决策维度|排队、库存、MDP、仿真|3","🚀 不确定优化维度|随机规划、鲁棒优化、多目标实践|4")
        links=@("最优化方法|02-Knowledge/🧠 学习系统/07-最优化方法/🗺️ 最优化方法学习路径|连续优化与算法基础","控制与机器人学|02-Knowledge/🧠 学习系统/15-控制与机器人学/🗺️ 控制与机器人学学习路径|MPC 与约束优化决策","量化金融|02-Knowledge/🧠 学习系统/03-量化金融/🗺️ 量化金融学习路径|组合优化与执行调度")
    }
)

foreach ($subject in $subjects) { New-PathFiles $subject }
Write-Output "Generated batch 2."
