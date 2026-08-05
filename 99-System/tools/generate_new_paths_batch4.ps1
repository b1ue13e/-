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
        id="34"; name="偏微分方程"; short="PDE"; tags=@("学习路径","偏微分方程","分析学")
        desc="从经典模型到弱解、谱方法与数值求解的偏微分方程路线图"
        quote="PDE 是连续世界的语言，扩散、波动、场和价格演化都写在里面。"
        stages=@(
            @{dir="01-基础模型与分类"; emoji="🌊"; title="第一阶段：基础模型与分类"; duration="4-6周"; summary="一阶 PDE、特征线与椭圆抛物双曲分类"; topics=@("PDE 基本概念|阶、线性性、边界与初值问题","一阶方程与特征线|守恒律直观与几何解释","二阶方程分类|椭圆、抛物、双曲与经典模型"); concepts=@("特征线","方程分类","热方程"); prereq=@("数学分析","常微分方程"); related=@("信号与系统","控制与机器人学","量化金融")},
            @{dir="02-Fourier与Green方法"; emoji="🔍"; title="第二阶段：Fourier与Green方法"; duration="4-6周"; summary="分离变量、Fourier 变换、Green 函数与能量法"; topics=@("分离变量法|边界条件与特征值问题","Fourier 方法|变换域求解与卷积表示","Green 函数与能量法|基本解、稳定性、唯一性"); concepts=@("分离变量","Fourier变换","Green函数"); prereq=@("热方程","波方程","Fourier级数"); related=@("实变函数","信号与系统","随机过程")},
            @{dir="03-弱解与函数空间"; emoji="📐"; title="第三阶段：弱解与函数空间"; duration="5-7周"; summary="Sobolev 空间、弱解、变分法与正则性"; topics=@("Sobolev 空间|弱导数、嵌入与迹直观","弱解框架|测试函数、分布观点、积分分部","Lax-Milgram 与正则性|存在唯一性与最大值原理"); concepts=@("弱解","Sobolev空间","Lax-Milgram"); prereq=@("测度论","实变函数","泛函分析"); related=@("泛函分析","数值分析","量化金融")},
            @{dir="04-数值与应用专题"; emoji="🚀"; title="第四阶段：数值与应用专题"; duration="4-6周"; summary="有限差分、有限元、控制/金融/物理应用"; topics=@("有限差分法|稳定性、收敛性、网格设计","有限元法入口|弱形式、基函数、稀疏矩阵","应用专题|Black-Scholes、控制、流体与图像处理"); concepts=@("有限差分","有限元","Black-Scholes方程"); prereq=@("弱解","Sobolev空间","Green函数"); related=@("数值分析","量化金融","控制与机器人学")}
        )
        dims=@("🌊 模型分类维度|特征线、方程分类、经典模型|1","🔍 解析求解维度|分离变量、Fourier、Green函数|2","📐 弱解空间维度|Sobolev、弱解、正则性、变分法|3","🚀 数值应用维度|有限差分、有限元、控制/金融应用|4")
        links=@("实变函数|02-Knowledge/🧠 学习系统/26-实变函数/🗺️ 实变函数学习路径|Sobolev 与积分工具基础","泛函分析|02-Knowledge/🧠 学习系统/27-泛函分析/🗺️ 泛函分析学习路径|弱解存在唯一性框架","量化金融|02-Knowledge/🧠 学习系统/03-量化金融/🗺️ 量化金融学习路径|Black-Scholes 与随机控制联系")
    },
    @{
        id="35"; name="数值分析"; short="数值分析"; tags=@("学习路径","数值分析","科学计算")
        desc="从误差分析到 ODE/PDE 数值求解的数值分析路线图"
        quote="数值分析研究的是怎样让计算机近似地、稳定地、可信地解决数学问题。"
        stages=@(
            @{dir="01-误差与数值线代"; emoji="🧮"; title="第一阶段：误差与数值线代"; duration="4-6周"; summary="误差来源、条件数、线性方程组与特征值计算"; topics=@("误差与稳定性|舍入误差、截断误差、病态性","线性方程组求解|LU、QR、迭代法","条件数与特征值计算|预处理、幂法、QR 算法"); concepts=@("条件数","QR分解","数值稳定性"); prereq=@("高等代数","数学分析"); related=@("机器学习","量化金融","运筹学")},
            @{dir="02-插值积分与逼近"; emoji="📏"; title="第二阶段：插值积分与逼近"; duration="4-6周"; summary="插值、多项式逼近、数值积分与误差估计"; topics=@("插值方法|Lagrange、Newton、样条插值","逼近理论|最小二乘逼近与 Chebyshev 观点","数值积分|Newton-Cotes、Gauss 积分、误差估计"); concepts=@("插值","数值积分","逼近误差"); prereq=@("条件数","数值稳定性","Taylor展开"); related=@("应用回归分析","机器学习","偏微分方程")},
            @{dir="03-非线性与ODE数值解"; emoji="⚙️"; title="第三阶段：非线性与ODE数值解"; duration="4-6周"; summary="求根、优化迭代与常微分方程数值方法"; topics=@("非线性方程求根|二分、牛顿、拟牛顿","优化迭代的数值视角|步长、终止准则、病态问题","ODE 数值解|Euler、Runge-Kutta、多步法与刚性"); concepts=@("牛顿法","Runge-Kutta","刚性方程"); prereq=@("插值","数值积分","常微分方程"); related=@("最优化方法","常微分方程","控制与机器人学")},
            @{dir="04-PDE数值与科学计算"; emoji="🚀"; title="第四阶段：PDE数值与科学计算"; duration="4-6周"; summary="有限差分、有限元、并行计算与科学计算实践"; topics=@("PDE 离散化|有限差分、稳定性与网格设计","有限元基础|弱形式、基函数、稀疏矩阵","科学计算实践|并行思路、实验报告、可复现流程"); concepts=@("有限差分","有限元","科学计算"); prereq=@("Runge-Kutta","刚性方程","偏微分方程"); related=@("偏微分方程","量化金融","计算机组成原理")}
        )
        dims=@("🧮 误差线代维度|误差、条件数、线性方程组、特征值|1","📏 插值逼近维度|插值、积分、逼近与误差估计|2","⚙️ ODE数值维度|求根、迭代、Runge-Kutta、刚性|3","🚀 科学计算维度|PDE 离散、有限元、并行与实验|4")
        links=@("常微分方程|02-Knowledge/🧠 学习系统/06-常微分方程/🗺️ 常微分方程学习路径|ODE 结构与数值求解对象","偏微分方程|02-Knowledge/🧠 学习系统/34-偏微分方程/🗺️ 偏微分方程学习路径|差分/有限元求解目标","最优化方法|02-Knowledge/🧠 学习系统/07-最优化方法/🗺️ 最优化方法学习路径|牛顿迭代与数值稳定性")
    }
)

foreach ($subject in $subjects) { New-PathFiles $subject }
Write-Output "Generated batch 4."
