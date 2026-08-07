#!/usr/bin/env python3
"""Restore the 33-course open self-study layer from the archived survey."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SYSTEM = ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统"
REPORT = ROOT / "99-System" / "🗄️ 归档" / "33门课程开源自学项目调研-2026-07-27.md"
TODAY = "2026-07-31"
START = "<!-- OPEN_SELF_STUDY_START -->"
END = "<!-- OPEN_SELF_STUDY_END -->"

COURSES = [
    ("01", "社交网络挖掘"), ("02", "时间序列分析"), ("03", "量化金融"),
    ("04", "离散数学"), ("05", "计算机视觉"), ("06", "常微分方程"),
    ("07", "最优化方法"), ("08", "NLP全栈"), ("09", "高等代数"),
    ("10", "数据结构与算法"), ("11", "计算机组成原理"), ("12", "信号与系统"),
    ("13", "强化学习"), ("14", "概率图模型"), ("15", "控制与机器人学"),
    ("16", "多元统计"), ("17", "机器学习"), ("22", "概率论与数理统计"),
    ("23", "图神经网络"), ("24", "随机过程"), ("25", "测度论"),
    ("26", "实变函数"), ("27", "泛函分析"), ("28", "数学分析"),
    ("29", "运筹学"), ("30", "应用回归分析"), ("31", "属性数据分析"),
    ("32", "非参数统计"), ("33", "贝叶斯统计"), ("34", "偏微分方程"),
    ("35", "数值分析"), ("36", "数据挖掘与信息检索"), ("37", "复变函数"),
]

B_COURSES = {"14", "16", "24", "27", "32"}
PROOF_COURSES = {"04", "25", "26", "27", "28", "37"}

LABS = {
    "01": ["清洗公开网络并核对节点、边和连通分量", "比较中心性与社区发现算法", "完成链路预测并分析错误边"],
    "02": ["实现 Naive 与季节基线", "拟合 ETS/ARIMA 并做残差诊断", "滚动回测并比较预测区间"],
    "03": ["冻结数据、标签和时间切分", "完成简单因子与成本基线", "用 Qlib 比较模型并审计泄漏"],
    "04": ["完成逻辑、集合与证明练习", "实现递推、计数与图论小实验", "提交证明、反例和复杂度作品集"],
    "05": ["实现 kNN 与线性分类器", "训练 MLP/CNN 并记录曲线", "迁移学习、校准与失败样本分析"],
    "06": ["比较 Euler 与 Runge-Kutta", "分析稳定性、步长和刚性", "对真实动力系统完成参数与误差实验"],
    "07": ["实现 GD、Momentum 与 Nesterov", "完成 Proximal 或 ADMM 实验", "比较收敛、耗时和停止准则"],
    "08": ["建立 TF-IDF/BM25 基线", "微调 Transformer 文本模型", "完成误差分类，再选择是否扩展 RAG"],
    "09": ["实现 LU/QR 并检查数值误差", "完成 SVD/NMF 或特征值实验", "在真实数据上分析稳定性与复杂度"],
    "10": ["实现哈希表、堆和并查集", "实现 BFS/DFS/最短路", "用随机测试和规模实验验证复杂度"],
    "11": ["构造逻辑门与 ALU", "完成内存、CPU 和汇编器", "完成 VM/编译器最小闭环"],
    "12": ["观察时域、频域与卷积", "实现采样、滤波和混叠实验", "在真实音频上完成去噪比较"],
    "13": ["实现动态规划与表格方法", "训练 DQN 或 PPO 基线", "比较多随机种子与样本效率"],
    "14": ["建立小型贝叶斯网并精确推断", "比较结构/参数学习方法", "补做近似推断与自建阶段验收"],
    "15": ["完成定位与地图小实验", "比较两种路径规划或控制器", "在统一仿真中串联系统并分析失败"],
    "16": ["完成标准化、协方差与 PCA", "比较聚类与判别方法", "补做尺度、稳定性和解释性验收"],
    "17": ["建立表格模型朴素基线", "完成特征工程、验证和调参", "补做校准、解释与漂移检查"],
    "22": ["用模拟验证大数定律和中心极限定理", "复现置信区间与假设检验", "比较理论性质与有限样本结果"],
    "23": ["建立 MLP 图任务基线", "比较 GCN、GraphSAGE 与 GAT", "完成深度、采样和特征消融"],
    "24": ["模拟有限 Markov 链与稳态", "完成混合时间或 Monte Carlo 实验", "补做队列、库存或随机波动验收"],
    "25": ["闭卷重建 σ 代数与测度定义", "证明积分与收敛定理链", "提交反例和证明作品集；Lean 仅可选"],
    "26": ["完成极限、连续和紧致性证明", "重建微分与积分定理链", "提交定义、反例和闭卷证明作品集"],
    "27": ["完成 Banach/Hilbert 空间证明", "研究有界、紧算子与对偶", "补做谱理论证明验收"],
    "28": ["闭卷重建实数、序列与连续性", "完成微分、积分和级数证明", "提交反例与定理依赖图"],
    "29": ["建立并验证 LP/MIP 小模型", "完成网络流、调度或路径规划", "分析规模、求解时间和不可行原因"],
    "30": ["建立 OLS 基线并做诊断", "比较变换、正则化与非线性", "完成样本外评估和系数解释"],
    "31": ["分析列联表、卡方和优势比", "拟合二项/多项/有序 Logistic", "比较模型并检查拟合与残差"],
    "32": ["比较参数检验与置换检验", "完成 Bootstrap、秩检验和 KDE", "补做样本量与异常值敏感性验收"],
    "33": ["完成先验预测检查", "拟合分层模型并检查采样诊断", "完成后验预测和敏感性分析"],
    "34": ["用 FEniCS 求解 Poisson 方程", "完成网格细化与收敛验证", "扩展到热方程、弹性或瞬态问题"],
    "35": ["验证浮点误差与条件数", "比较线性求解、QR/SVD 与特征值算法", "完成迭代法稳定性和耗时实验"],
    "36": ["建立 BM25 稀疏检索基线", "比较 Dense 与 Hybrid 检索", "报告 Recall/MRR/nDCG、时延和错误案例"],
    "37": ["用域着色观察复函数并验证 Cauchy-Riemann", "手算路径积分和留数并用数值方法复核", "完成保角映射可视化与证明说明"],
}


def parse_report() -> dict[str, tuple[str, str, str]]:
    records: dict[str, tuple[str, str, str]] = {}
    pattern = re.compile(r"^\| (\d{2}) ([^|]+?) \| (.+?) \| (.+?) \| ([ABC]) \|$")
    for line in REPORT.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            number, _name, source, capstone, maturity = match.groups()
            records[number] = (source.strip(), capstone.strip(), maturity)
    return records


def course_dir(number: str, name: str) -> Path:
    return SYSTEM / f"{number}-{name}"


def first_stage_link(directory: Path) -> str:
    for stage in sorted(p for p in directory.iterdir() if p.is_dir() and re.match(r"^\d{2}-", p.name)):
        pages = sorted(stage.glob("*.md"), key=lambda p: ("阶段" not in p.name and "板块" not in p.name, p.name))
        if pages:
            rel = pages[0].relative_to(SYSTEM).with_suffix("").as_posix()
            return f"[[{rel}|从第一阶段开始]]"
    return "从本课程学习路径的第一项开始"


def rubric(number: str) -> str:
    if number in PROOF_COURSES:
        return """| 维度 | 分值 | 通过要求 |
|:---|---:|:---|
| 定义、正例与反例 | 20 | 能闭卷写出核心定义并给出有效例子 |
| 证明正确性 | 35 | 关键定理证明完整，不跳过必要条件 |
| 分级习题 | 20 | 基础、变式和综合题均有独立作答 |
| 定理依赖与反思 | 15 | 能说明依赖关系、失败条件和反例 |
| 口头验收 | 10 | 5–10 分钟解释核心结论 |
| **总计** | **100** | **达到 75 分且证明正确性不低于 25 分** |"""
    return """| 维度 | 分值 | 通过要求 |
|:---|---:|:---|
| 数据、环境与复现 | 20 | 输入、版本、随机种子和运行步骤完整 |
| 方法正确性 | 25 | 实现与理论口径一致，有最小测试 |
| 基线与公平比较 | 20 | 先有朴素基线，再比较复杂方法 |
| 评估、消融与误差 | 20 | 指标合适，保留失败案例与至少一次消融 |
| 报告与边界 | 15 | 结论可复核，不夸大适用范围 |
| **总计** | **100** | **达到 75 分且方法正确性不低于 18 分** |"""


def execution_block(number: str, source: str, capstone: str, maturity: str, directory: Path) -> str:
    labels = {"A": "成熟资源，可直接挂载", "B": "资源成熟，需补本地阶段验收", "C": "证明优先"}
    lab_rows = "\n".join(
        f"| Lab {idx} | {task} | 代码、证明、图表或审计记录 |"
        for idx, task in enumerate(LABS[number], 1)
    )
    special = ""
    if maturity == "B":
        special = "\n> [!warning] 本课程属于 B 类：开源资源负责讲授，本地 Lab 与 Capstone 是必做验收，不能只看完材料。\n"
    if maturity == "C":
        special = "\n> [!important] 测度论坚持纸笔证明优先。Lean/mathlib 只可验证少量引理，不替代定义、反例和完整证明。\n"
    return f"""
{START}

## 🧭 开源自学执行方案

> 恢复日期：{TODAY}。本区负责把开源资源转换为可执行任务；原有教材阅读顺序继续保留。

| 项目 | 设计 |
|:---|:---|
| 成熟度 | **{maturity}：{labels[maturity]}** |
| 唯一 Spine | {source} |
| 起步入口 | {first_stage_link(directory)} |
| 执行原则 | 一次只推进当前阶段；完成 Lab 验收后再进入下一阶段 |
{special}
### 阶段 Lab

| Lab | 完成任务 | 必交证据 |
|:---:|:---|:---|
{lab_rows}

### Capstone

**项目任务**：{capstone}

最低交付：问题定义、可复现输入、朴素基线、核心方法、统一评估、失败案例、限制说明和复现步骤。证明型课程将“代码基线”替换为“定义—定理—证明—反例”链条。

### 100 分 Rubric

{rubric(number)}

### 许可证与本地镜像

- 默认先保留官方链接，不复制公开答案；
- 克隆仓库时记录来源 URL、commit 和许可证；
- 数据集、课程题目和解答分别核验许可，未知时采用 `link-only`；
- 自己的代码、证明、实验结果和报告放入本课程项目目录。

{END}
"""


def ensure_frontmatter_updated(text: str) -> str:
    if text.startswith("---\n") and "\n---\n" in text[4:]:
        head, body = text[4:].split("\n---\n", 1)
        if re.search(r"^updated:", head, re.MULTILINE):
            head = re.sub(r"^updated:.*$", f"updated: {TODAY}", head, flags=re.MULTILINE)
        else:
            head += f"\nupdated: {TODAY}"
        for key, value in (("flow", "knowledge"), ("kind", "moc")):
            if not re.search(rf"^{key}:", head, re.MULTILINE):
                head += f"\n{key}: {value}"
        return f"---\n{head}\n---\n{body}"
    return text


def restore_mounts(records: dict[str, tuple[str, str, str]]) -> None:
    for number, name in COURSES:
        directory = course_dir(number, name)
        mount = directory / "📚 教材挂载索引.md"
        source, capstone, maturity = records[number]
        text = mount.read_text(encoding="utf-8-sig")
        text = re.sub(rf"\n?{re.escape(START)}.*?{re.escape(END)}\n?", "\n", text, flags=re.DOTALL)
        text = ensure_frontmatter_updated(text.rstrip())
        text += "\n" + execution_block(number, source, capstone, maturity, directory)
        mount.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def create_complex_analysis(records: dict[str, tuple[str, str, str]]) -> None:
    directory = course_dir("37", "复变函数")
    directory.mkdir(parents=True, exist_ok=True)
    stages = [
        ("01-复数与解析函数", "📘 第一阶段：复数与解析函数", "复数几何、极限、连续、复导数、Cauchy-Riemann 方程与解析性。", "完成域着色图，并对三个函数手算和数值检查 Cauchy-Riemann 条件。"),
        ("02-复积分与级数", "📗 第二阶段：复积分与级数", "路径积分、Cauchy 定理、积分公式、Taylor/Laurent 级数。", "手算两条路径积分，验证路径无关条件，并展开至少两个 Laurent 级数。"),
        ("03-奇点与留数", "📙 第三阶段：奇点与留数", "孤立奇点分类、留数定理、实积分计算与辐角原理。", "完成四类留数题，并用数值积分复核至少一个闭路积分。"),
        ("04-保角映射与综合项目", "📕 第四阶段：保角映射与综合项目", "Möbius 变换、保角映射、调和函数与综合可视化。", "建立复函数可视化画廊；每幅图必须附定义、推导或证明说明。"),
    ]
    links = []
    for folder, title, scope, acceptance in stages:
        stage_dir = directory / folder
        stage_dir.mkdir(exist_ok=True)
        page = stage_dir / f"{title}.md"
        page.write_text(f"""---
title: "{title}"
type: index
topic: "{title.split('：', 1)[1]}"
course: "复变函数"
created: {TODAY}
updated: {TODAY}
status: planned
flow: knowledge
kind: moc
tags: [复变函数, 阶段]
---

# {title}

## 学习范围

{scope}

## 学习动作

1. 闭卷写出本阶段核心定义并各给一个正例、反例。
2. 完成主线资源对应章节的基础题和证明题。
3. 用 Python/交互可视化复核几何直觉，但不以图代替证明。
4. 把错误条件、失败证明和修正过程写入阶段记录。

## 阶段作业

{acceptance}

## 通过标准

- 定义和定理条件无误；
- 至少完成 6 道基础题、3 道证明题和 1 个可视化实验；
- 能在 10 分钟内口头解释本阶段主线；
- 阶段作业可复核后才能进入下一阶段。

## 导航

- [[37-复变函数/🗺️ 复变函数学习路径|返回学习路径]]
- [[37-复变函数/📚 教材挂载索引|查看开源资源与验收]]
""", encoding="utf-8", newline="\n")
        links.append((folder, title))

    route_rows = "\n".join(
        f"| {idx} | [[37-复变函数/{folder}/{title}|{title.split('：', 1)[1]}]] | 完成阶段页作业并通过闭卷验收 |"
        for idx, (folder, title) in enumerate(links, 1)
    )
    (directory / "🗺️ 复变函数学习路径.md").write_text(f"""---
title: "复变函数学习路径"
type: index
topic: "复变函数学习路径"
course: "复变函数"
created: {TODAY}
updated: {TODAY}
status: active
flow: knowledge
kind: moc
tags: [复变函数, 学习路径, 开源自学]
---

# 🗺️ 复变函数学习路径

> 唯一顺序：**复数与解析函数 → 复积分与级数 → 奇点与留数 → 保角映射与综合项目**。未通过当前阶段，不进入下一阶段。

| 阶段 | 入口 | 闸门 |
|:---:|:---|:---|
{route_rows}

## 最终能力

你应能从解析性出发推导积分与级数工具，使用留数解决积分问题，并用保角映射解释几何结构；可视化只用于验证直觉，证明仍是核心证据。

## 资源与验收

- [[37-复变函数/📚 教材挂载索引|开源 Spine、Lab、Capstone 与 Rubric]]
- [[33门课程开源自学与验收总索引|返回 33 门课程总索引]]
""", encoding="utf-8", newline="\n")

    source, capstone, maturity = records["37"]
    mount = directory / "📚 教材挂载索引.md"
    mount.write_text(f"""---
title: "复变函数教材挂载索引"
type: index
topic: "复变函数教材挂载索引"
course: "复变函数"
created: {TODAY}
updated: {TODAY}
status: active
flow: knowledge
kind: moc
tags: [复变函数, 教材, 开源自学]
---

# 📚 复变函数教材挂载索引

> 教材和开源项目只服务于 [[37-复变函数/🗺️ 复变函数学习路径|四阶段学习路径]]，不形成第二条路线。
""".rstrip() + "\n" + execution_block("37", source, capstone, maturity, directory).lstrip(), encoding="utf-8", newline="\n")


def create_global_indexes(records: dict[str, tuple[str, str, str]]) -> None:
    rows = []
    for number, name in COURSES:
        _source, capstone, maturity = records[number]
        rows.append(
            f"| {number} | [[{number}-{name}/🗺️ {name}学习路径|{name}]] | "
            f"[[{number}-{name}/📚 教材挂载索引|Spine / Lab / Capstone / Rubric]] | {maturity} | {capstone} |"
        )
    index = SYSTEM / "33门课程开源自学与验收总索引.md"
    index.write_text(f"""---
title: "33门课程开源自学与验收总索引"
type: index
topic: "33门课程开源自学与验收"
created: {TODAY}
updated: {TODAY}
status: active
flow: knowledge
kind: moc
tags: [学习系统, 开源自学, 项目验收, 索引]
---

# 33 门课程开源自学与验收总索引

> 每门课只有一个学习路径入口。教材挂载页负责 Spine、阶段 Lab、Capstone、100 分 Rubric 和许可证规则；本页不生成第二套日程。

## 使用顺序

1. 从 [[01-Active Sprint/🚀 Active Sprint|Active Sprint]] 确定唯一主攻课程。
2. 打开该课程的“学习路径”，只推进当前阶段。
3. 卡住时查看“教材挂载页”的唯一 Spine。
4. 完成阶段 Lab 并通过验收，再进入下一阶段。
5. 最后完成 Capstone，Rubric 达到 75 分后结课。

## 课程总表

| 编号 | 唯一学习路径 | 开源自学设计 | 成熟度 | Capstone |
|:---:|:---|:---|:---:|:---|
{chr(10).join(rows)}

## 成熟度说明

- **A（27 门）**：已有成熟课程、Notebook 或作业，可直接挂载。
- **B（5 门）**：资源成熟，但必须完成本地补充的阶段验收。
- **C（1 门）**：测度论坚持证明优先，Lean 只作为可选验证。

调研证据：[[99-System/🗄️ 归档/33门课程开源自学项目调研-2026-07-27|33门课程开源自学项目调研]]。
""", encoding="utf-8", newline="\n")

    detail = SYSTEM / "🧭 学习路径详细索引.md"
    detail.write_text(f"""---
title: "学习路径详细索引"
type: index
topic: "33门课程学习路径详细索引"
created: {TODAY}
updated: {TODAY}
status: active
flow: knowledge
kind: moc
tags: [学习系统, 学习路径, 详细索引]
---

# 🧭 学习路径详细索引

> 33 条正式学习路径：01–17 与 22–37。18–21 是辅助目录，不计入课程数量。

| 编号 | 课程 | 学习路径 | 教材与开源自学 |
|:---:|:---|:---|:---|
{chr(10).join(f'| {n} | {name} | [[{n}-{name}/🗺️ {name}学习路径|进入路径]] | [[{n}-{name}/📚 教材挂载索引|进入教材与验收]] |' for n, name in COURSES)}

## 总入口

- [[🎓 学习入口|学习入口]]
- [[🧭 学科分组导航|按学科分组选择]]
- [[33门课程开源自学与验收总索引|查看 Spine、Lab、Capstone 与 Rubric]]
""", encoding="utf-8", newline="\n")


def update_navigation() -> None:
    replacements = {
        SYSTEM / "🎓 学习入口.md": [
            ("不要直接翻 32 条路径", "不要直接翻 33 条路径"),
            ("32 条核心学习路径（01-17 原有主路径 + 22-36 扩展学科）", "33 条正式学习路径（01-17 原有主路径 + 22-37 扩展学科）"),
        ],
        SYSTEM / "🧭 学科分组导航.md": [
            ("32 条核心学习路径", "33 条正式学习路径"),
        ],
        SYSTEM / "📚 教材挂载总索引.md": [
            ("`01-17` 与 `22-36` 的 `32` 条核心学术路径", "`01-17` 与 `22-37` 的 `33` 条正式学习路径"),
            ("`32/32` 已覆盖", "`33/33` 已覆盖"),
            ("`01-17` 与 `22-36`", "`01-17` 与 `22-37`"),
        ],
        SYSTEM / "📊 教材挂载覆盖检查.md": [
            ('"34-偏微分方程","35-数值分析","36-数据挖掘与信息检索"', '"34-偏微分方程","35-数值分析","36-数据挖掘与信息检索","37-复变函数"'),
            ("01-17 与 22-36 的 32 条核心学术路径", "01-17 与 22-37 的 33 条正式学习路径"),
            ("`22-36` 扩展学科路径", "`22-37` 扩展学科路径"),
            ("`02-Knowledge/🧠 学习系统/${dir}/📚 教材挂载索引.md`", "`02-Knowledge/🧠 学习系统/${dir}/📚 教材挂载索引.md`"),
        ],
    }
    for path, pairs in replacements.items():
        text = path.read_text(encoding="utf-8-sig")
        for old, new in pairs:
            text = text.replace(old, new)
        text = ensure_frontmatter_updated(text)
        path.write_text(text, encoding="utf-8", newline="\n")

    entry = SYSTEM / "🎓 学习入口.md"
    text = entry.read_text(encoding="utf-8")
    if "37-复变函数/🗺️ 复变函数学习路径" not in text:
        marker = "### 📊 统计建模扩展"
        addition = "\n### 🌀 复变函数\n\n- [[37-复变函数/🗺️ 复变函数学习路径|复变函数四阶段学习路径]]\n- [[37-复变函数/📚 教材挂载索引|开源 Spine、Lab 与 Capstone]]\n\n"
        text = text.replace(marker, addition + marker)
        entry.write_text(text, encoding="utf-8", newline="\n")

    groups = SYSTEM / "🧭 学科分组导航.md"
    text = groups.read_text(encoding="utf-8")
    if "37-复变函数/🗺️ 复变函数学习路径" not in text:
        anchor = "| 方程与数值 |"
        line = "| 复分析 | [[37-复变函数/🗺️ 复变函数学习路径|复变函数]] | 解析函数、留数、保角映射 |\n"
        text = text.replace(anchor, line + anchor)
        groups.write_text(text, encoding="utf-8", newline="\n")

    total = SYSTEM / "📚 教材挂载总索引.md"
    text = total.read_text(encoding="utf-8")
    if "37-复变函数/📚 教材挂载索引" not in text:
        anchor = "---\n\n## 🧭 当前处理规则"
        row = "| 37-复变函数 | 已挂载 | [[37-复变函数/📚 教材挂载索引|进入]] | 解析函数、留数、保角映射与可视化 |\n\n"
        text = text.replace(anchor, row + anchor)
        total.write_text(text, encoding="utf-8", newline="\n")

    course_map = SYSTEM / "🧭 课程挂载索引.md"
    text = course_map.read_text(encoding="utf-8-sig")
    if "37-复变函数/🗺️ 复变函数学习路径" not in text:
        text += "\n## 复变函数补充挂载\n\n| 课程 | 挂载路径 | 入口 | 处理结果 |\n|:---|:---|:---|:---|\n| 复变函数 | 复变函数主路径 | [[37-复变函数/🗺️ 复变函数学习路径|复变函数学习路径]] | 新增正式路径与开源自学设计 |\n"
    text = ensure_frontmatter_updated(text)
    course_map.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    records = parse_report()
    expected = {number for number, _ in COURSES}
    if set(records) != expected:
        raise RuntimeError(f"Survey rows mismatch: missing={sorted(expected - set(records))}")
    create_complex_analysis(records)
    restore_mounts(records)
    create_global_indexes(records)
    update_navigation()
    print("Restored open self-study designs for 33 courses.")


if __name__ == "__main__":
    main()
