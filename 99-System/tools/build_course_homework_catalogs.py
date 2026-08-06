"""Build complete assignment catalogs for the 33 formal learning paths.

The catalogs enumerate public official assignment units and local original
extensions. Third-party prompts, starter archives, and solutions are not copied:
official material remains link-only unless an activated course performs a
separate license and version freeze.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from build_formal_course_homework_packs import COURSES


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT / "03-Projects" / "课程作业"
STUDY_ROOT = ROOT / "02-Knowledge" / "🧠 学习系统"
DATE = "2026-07-28"
BLOCK_START = "<!-- complete-homework-catalog:start -->"
BLOCK_END = "<!-- complete-homework-catalog:end -->"


@dataclass(frozen=True)
class Unit:
    unit_id: str
    title: str
    unit_type: str
    source: str
    url: str


@dataclass(frozen=True)
class CourseCatalog:
    code: str
    course: str
    role: str
    materials: tuple[tuple[str, str, str], ...]
    official: tuple[Unit, ...]
    local_topics: tuple[str, ...]


def official_series(
    prefix: str,
    numbers,
    source: str,
    url: str,
    *,
    labels: dict[int, str] | None = None,
) -> tuple[Unit, ...]:
    units = []
    for number in numbers:
        label = labels.get(number) if labels else None
        title = label or f"{source} {prefix} {number}"
        units.append(Unit(f"OF-{prefix}{number}", title, "official-link", source, url))
    return tuple(units)


def named_official(
    source: str,
    url: str,
    names: list[str],
    prefix: str = "OF",
) -> tuple[Unit, ...]:
    return tuple(
        Unit(f"{prefix}-{index:02d}", title, "official-link", source, url)
        for index, title in enumerate(names, 1)
    )


def local_units(
    source: str,
    url: str,
    topics: tuple[str, ...],
) -> tuple[Unit, ...]:
    return tuple(
        Unit(f"LOCAL-{index:02d}", title, "local-original", source, url)
        for index, title in enumerate(topics, 1)
    )


CS224W_URL = "https://web.stanford.edu/class/cs224w/"
CS224W_OFFICIAL = named_official(
    "Stanford CS224W 2025",
    CS224W_URL,
    [
        "Homework 1（主题以当期官方 handout 为准）",
        "Homework 2（主题以当期官方 handout 为准）",
        "Homework 3（主题以当期官方 handout 为准）",
        "Colab 0：环境与 PyG 基础",
        "Colab 1：节点嵌入",
        "Colab 2：消息传递 GNN",
        "Colab 3：知识图谱",
        "Colab 4：关系图学习",
        "Colab 5：知识图谱基础模型",
        "课程项目 Proposal",
        "课程项目 Milestone",
        "课程项目 Report",
    ],
)

ML_TOPICS = [
    "Regression", "Classification", "CNN", "Self-Attention", "Transformer",
    "Generative Model / GAN", "BERT", "Autoencoder", "Explainable AI",
    "Adversarial Attack", "Domain Adaptation", "Reinforcement Learning",
    "Network Compression", "Life-Long Learning", "Meta Learning",
]

NAND_NAMES = [
    "Project 1：Boolean Logic",
    "Project 2：Boolean Arithmetic",
    "Project 3：Memory",
    "Project 4：Machine Language",
    "Project 5：Computer Architecture",
    "Project 6：Assembler",
    "Project 7：VM I — Stack Arithmetic",
    "Project 8：VM II — Program Control",
    "Project 9：High-Level Language",
    "Project 10：Compiler I — Parsing",
    "Project 11：Compiler II — Code Generation",
    "Project 12：Operating System",
]

CS188_NAMES = [
    "Project 0：Python、环境与 Autograder",
    "Project 1：Search",
    "Project 2：Multi-Agent Search",
    "Project 3：Reinforcement Learning",
    "Project 4：Bayes Nets and HMMs",
    "Project 5：Machine Learning",
]

COURSE_INFO = {item[0]: (item[1], item[3]) for item in COURSES}
COURSE_INFO["03"] = ("量化金融", "stats")


def make_catalogs() -> tuple[CourseCatalog, ...]:
    specs: dict[str, dict] = {
        "01": {
            "materials": (
                ("Stanford CS224W", CS224W_URL, "public-course/link-only"),
                ("NetworkX", "https://github.com/networkx/networkx", "BSD-3-Clause/repo"),
            ),
            "official": CS224W_OFFICIAL,
            "local": ("网络统计与社区结构", "节点嵌入", "链路预测", "图推荐系统", "GNN 节点分类"),
        },
        "02": {
            "materials": (
                ("Penn State STAT 510", "https://online.stat.psu.edu/stat510/", "public-course/link-only"),
                ("statsmodels", "https://github.com/statsmodels/statsmodels", "BSD-3-Clause/repo"),
            ),
            "local": ("时间序列探索与分解", "平稳性与单位根", "指数平滑 ETS", "ARIMA 建模",
                      "残差诊断", "滚动预测评测", "预测区间覆盖率", "多变量与动态回归"),
        },
        "03": {
            "materials": (
                ("Georgia Tech ML4T", "https://lucylabs.gatech.edu/ml4t/", "public-course/link-only"),
                ("FinRL", "https://github.com/AI4Finance-Foundation/FinRL", "Apache-2.0/repo"),
                ("QuantEcon", "https://quantecon.org/", "public-resource/terms-per-item"),
                ("Microsoft Qlib", "https://github.com/microsoft/qlib", "MIT/repo"),
            ),
            "local": ("市场数据与未来信息审计", "技术指标与朴素信号", "组合优化与基准",
                      "ML4T 策略学习器", "事件驱动回测", "FinRL 环境与奖励审计",
                      "QuantEcon 动态配置实验", "Qlib 成本敏感样本外回测"),
        },
        "04": {
            "materials": (("MIT 6.042", "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/pages/assignments/", "MIT-OCW-CC/link-only"),),
            "official": official_series("PS", range(1, 13), "MIT 6.042", "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/pages/assignments/"),
            "local": ("图论命题与最小反例", "组合计数与生成函数验证"),
        },
        "05": {
            "materials": (("Stanford CS231n 2025", "https://cs231n.stanford.edu/2025/assignments.html", "public-course/Honor-Code/link-only"),),
            "official": named_official(
                "Stanford CS231n 2025",
                "https://cs231n.stanford.edu/2025/assignments.html",
                [
                    "Assignment 1：图像分类、kNN、Softmax 与全连接网络",
                    "Assignment 2：BatchNorm、Dropout、CNN、可视化与 RNN Captioning",
                    "Assignment 3：Transformer Captioning、自监督、Diffusion、CLIP 与 DINO",
                    "Final Project：自选计算机视觉研究项目",
                ],
            ),
            "local": ("CIFAR-10 CNN 失败样本审计",),
        },
        "06": {
            "materials": (("MIT 18.03", "https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/pages/assignments/", "MIT-OCW-CC/link-only"),),
            "official": official_series("PS", range(1, 10), "MIT 18.03", "https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/pages/assignments/"),
            "local": ("Euler/RK4 收敛阶实验", "刚性与稳定域诊断"),
        },
        "07": {
            "materials": (
                ("Stanford EE364A", "https://see.stanford.edu/Course/EE364A", "public-course/textbook-copyright/link-only"),
                ("CVXPY Examples", "https://www.cvxpy.org/examples/", "Apache-2.0/project; examples per-page"),
            ),
            "official": official_series("HW", range(1, 9), "Stanford EE364A", "https://see.stanford.edu/Course/EE364A"),
            "local": ("CVXPY 线性与二次规划", "对偶与 KKT 数值核验", "ISTA/FISTA 稀疏优化", "鲁棒优化与敏感性"),
        },
        "08": {
            "materials": (("Stanford CS224N", "https://web.stanford.edu/class/cs224n/", "public-course/Honor-Code/link-only"),),
            "official": named_official(
                "Stanford CS224N",
                "https://web.stanford.edu/class/cs224n/",
                [
                    "Assignment 1：Word Vectors",
                    "Assignment 2：反向传播、张量导数与依存分析",
                    "Assignment 3：Self-Attention 与 Transformers",
                    "Assignment 4：LLM Benchmarking 与 Evaluation",
                    "Final Project：Minimal GPT-2 或自选 NLP 项目",
                ],
            ),
            "local": ("稀疏检索到 Transformer 的文本误差审计",),
        },
        "09": {
            "materials": (("MIT 18.06SC", "https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/resources/problem-sets/", "MIT-OCW-CC/link-only"),),
            "official": tuple(
                Unit(f"OF-U{unit}-S{session}", f"MIT 18.06SC Unit {unit} Session {session} Problem Set",
                     "official-link", "MIT 18.06SC",
                     "https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/resources/problem-sets/")
                for unit, count in ((1, 12), (2, 11), (3, 8))
                for session in range(1, count + 1)
            ),
            "local": ("矩阵分解与数值稳定性",),
        },
        "10": {
            "materials": (("MIT 6.006", "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/pages/assignments/", "MIT-OCW-CC/link-only"),),
            "official": official_series("PS", range(0, 9), "MIT 6.006", "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/pages/assignments/"),
            "local": ("哈希表", "堆与优先队列", "平衡搜索树", "图搜索与最短路", "动态规划"),
        },
        "11": {
            "materials": (("Nand2Tetris", "https://www.nand2tetris.org/course", "course-material/license-page; link-only"),),
            "official": named_official("Nand2Tetris", "https://www.nand2tetris.org/course", NAND_NAMES),
            "local": (),
        },
        "12": {
            "materials": (("MIT 6.003", "https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/resources/problem-sets/", "MIT-OCW-CC/link-only"),),
            "official": official_series("HW", range(1, 15), "MIT 6.003", "https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/resources/problem-sets/"),
            "local": ("离散/连续信号表示", "LTI 与卷积", "差分/微分方程", "Fourier 表示",
                      "Laplace 与 Z 变换", "采样与混叠", "滤波器设计", "反馈系统"),
        },
        "13": {
            "materials": (
                ("Berkeley CS188 Pacman", "https://inst.eecs.berkeley.edu/~cs188/su25/projects/", "public-course/Honor-Code/link-only"),
                ("Berkeley CS285", "https://rail.eecs.berkeley.edu/deeprlcourse-fa23/", "public-course/link-only"),
            ),
            "official": named_official("Berkeley CS188", "https://inst.eecs.berkeley.edu/~cs188/su25/projects/", CS188_NAMES),
            "local": ("Value Iteration", "Q-Learning", "Policy Gradient", "Actor-Critic", "模型式强化学习"),
        },
        "14": {
            "materials": (
                ("Stanford CS228", "https://cs.stanford.edu/~ermon/cs228/index.html", "public-course/Honor-Code/link-only"),
                ("pgmpy", "https://github.com/pgmpy/pgmpy", "MIT/repo"),
            ),
            "official": official_series("HW", range(1, 6), "Stanford CS228", "https://cs.stanford.edu/~ermon/cs228/index.html"),
            "local": ("变量消元", "近似推断与采样", "参数学习", "结构学习", "因果图与干预查询"),
        },
        "15": {
            "materials": (
                ("Modern Robotics", "https://github.com/NxRLab/ModernRobotics", "MIT/repo"),
                ("python-control", "https://github.com/python-control/python-control", "BSD-3-Clause/repo"),
            ),
            "local": ("刚体运动与坐标变换", "正向运动学", "逆向运动学", "速度运动学与雅可比",
                      "动力学", "轨迹生成", "反馈与状态空间控制", "定位—规划—控制闭环"),
        },
        "16": {
            "materials": (("Penn State STAT 505", "https://online.stat.psu.edu/stat505/", "public-course/link-only"),),
            "local": ("矩阵统计与多元正态", "Hotelling T²", "MANOVA", "主成分分析",
                      "因子分析", "聚类分析", "判别分析"),
        },
        "17": {
            "materials": (
                ("李宏毅 ML 2021 官方仓库", "https://github.com/ga642381/ML2021-Spring", "public-repo/NOASSERTION/link-only"),
                ("李宏毅 ML 2023 官方课程", "https://speech.ee.ntu.edu.tw/~hylee/ml/2023-spring.php", "public-course/Honor-Code/link-only"),
            ),
            "official": tuple(
                Unit(f"OF-2021-HW{index:02d}", f"ML2021 HW{index:02d}：{topic}",
                     "official-link", "李宏毅 ML 2021", "https://github.com/ga642381/ML2021-Spring")
                for index, topic in enumerate(ML_TOPICS, 1)
            ) + tuple(
                Unit(f"OF-2023-HW{index:02d}", f"ML2023 HW{index:02d}：{topic}",
                     "official-link", "李宏毅 ML 2023", "https://speech.ee.ntu.edu.tw/~hylee/ml/2023-spring.php")
                for index, topic in enumerate(ML_TOPICS, 1)
            ),
            "local": ("本地扩展：表格建模、校准与漂移审计",),
        },
        "22": {
            "materials": (("MIT 6.041SC", "https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/resources/problem-sets/", "MIT-OCW-CC/link-only"),),
            "official": official_series("PS", range(1, 12), "MIT 6.041SC", "https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/resources/problem-sets/"),
            "local": ("抽样分布与检验频率性质模拟",),
        },
        "23": {
            "materials": (("Stanford CS224W", CS224W_URL, "public-course/link-only"),),
            "official": CS224W_OFFICIAL,
            "local": ("GCN 节点分类", "GraphSAGE 归纳学习", "异构图建模", "图级表示与池化", "自选图学习项目"),
        },
        "24": {
            "materials": (
                ("MIT 6.011", "https://ocw.mit.edu/courses/6-011-signals-systems-and-inference-spring-2018/resources/assignments/", "MIT-OCW-CC/link-only"),
                ("MIT 6.041SC", "https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/", "MIT-OCW-CC/link-only"),
            ),
            "official": official_series("A", range(1, 12), "MIT 6.011", "https://ocw.mit.edu/courses/6-011-signals-systems-and-inference-spring-2018/resources/assignments/"),
            "local": ("Markov 链稳态与混合", "Poisson 过程", "平稳随机过程与谱", "排队过程模拟"),
        },
        "25": {
            "materials": (("MIT 18.102 Lebesgue/Lp 讲义", "https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2021/pages/lecture-notes-and-readings/", "MIT-OCW-CC/link-only"),),
            "local": ("σ-代数与可测空间", "可测函数与简单函数", "Lebesgue 测度", "Lebesgue 积分",
                      "Fatou 引理", "单调收敛定理", "控制收敛定理", "Lp 空间"),
        },
        "26": {
            "materials": (("MIT 18.100C", "https://ocw.mit.edu/courses/18-100c-real-analysis-fall-2012/pages/assignments/", "MIT-OCW-CC/link-only"),),
            "official": official_series("PS", range(1, 11), "MIT 18.100C", "https://ocw.mit.edu/courses/18-100c-real-analysis-fall-2012/pages/assignments/"),
            "local": (),
        },
        "27": {
            "materials": (("MIT 18.102", "https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2009/pages/assignments/", "MIT-OCW-CC/link-only"),),
            "official": official_series("PS", range(1, 11), "MIT 18.102", "https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2009/pages/assignments/"),
            "local": (),
        },
        "28": {
            "materials": (
                ("MIT 18.100A", "https://ocw.mit.edu/courses/18-100a-real-analysis-fall-2020/pages/assignments-and-exams/", "MIT-OCW-CC/link-only"),
                ("MIT 18.100C", "https://ocw.mit.edu/courses/18-100c-real-analysis-fall-2012/pages/assignments/", "MIT-OCW-CC/reference"),
            ),
            "official": official_series("A", range(1, 13), "MIT 18.100A", "https://ocw.mit.edu/courses/18-100a-real-analysis-fall-2020/pages/assignments-and-exams/") +
                        named_official("MIT 18.100A", "https://ocw.mit.edu/courses/18-100a-real-analysis-fall-2020/pages/assignments-and-exams/", ["Final Assignment"], "OF-FINAL"),
            "local": (),
        },
        "29": {
            "materials": (
                ("MIT 15.053", "https://ocw.mit.edu/courses/15-053-optimization-methods-in-management-science-spring-2013/pages/assignments/", "MIT-OCW-CC/link-only"),
                ("Google OR-Tools", "https://github.com/google/or-tools", "Apache-2.0/repo"),
            ),
            "official": official_series("PS", range(1, 7), "MIT 15.053", "https://ocw.mit.edu/courses/15-053-optimization-methods-in-management-science-spring-2013/pages/assignments/"),
            "local": ("OR-Tools 线性规划", "网络流", "车辆路径", "Job-Shop 排程"),
        },
        "30": {
            "materials": (
                ("Penn State STAT 462", "https://online.stat.psu.edu/stat462/", "public-course/link-only"),
                ("ISLP Labs", "https://intro-stat-learning.github.io/ISLP/labs.html", "public-book-labs/terms-per-item"),
            ),
            "local": ("简单线性回归", "多元回归", "变量选择", "残差诊断",
                      "影响点与共线性", "交互与变换", "正则化回归", "样本外解释"),
        },
        "31": {
            "materials": (("Penn State STAT 504", "https://online.stat.psu.edu/stat504/", "public-course/link-only"),),
            "local": ("列联表与关联", "优势比", "Logistic 回归", "多项 Logistic",
                      "有序响应模型", "对数线性模型", "稀疏单元与分离诊断"),
        },
        "32": {
            "materials": (
                ("Penn State STAT 415 非参数部分", "https://online.stat.psu.edu/stat415/", "public-course/link-only"),
                ("OpenIntro 重采样实验", "https://openintro-ims.netlify.app/", "public-book/terms-per-item"),
            ),
            "local": ("符号检验", "Wilcoxon 符号秩", "秩和检验", "置换检验",
                      "Bootstrap 区间", "核密度估计", "非参数回归"),
        },
        "33": {
            "materials": (
                ("Statistical Rethinking 2024", "https://github.com/rmcelreath/stat_rethinking_2024", "CC0-1.0/repo"),
                ("PyMC Examples", "https://www.pymc.io/projects/examples/en/latest/", "Apache-2.0/project; examples per-page"),
            ),
            "local": ("先验预测检查", "共轭模型", "MCMC 与诊断", "回归模型",
                      "层级模型", "后验预测检查", "模型比较与 LOO", "因果图与贝叶斯建模"),
        },
        "34": {
            "materials": (
                ("MIT 18.152", "https://ocw.mit.edu/courses/18-152-introduction-to-partial-differential-equations-fall-2005/pages/assignments/", "MIT-OCW-CC/link-only"),
                ("MIT 18.303", "https://ocw.mit.edu/courses/18-303-linear-partial-differential-equations-analysis-and-numerics-fall-2014/pages/assignments", "MIT-OCW-CC/link-only"),
            ),
            "official": official_series("A", range(1, 3), "MIT 18.152", "https://ocw.mit.edu/courses/18-152-introduction-to-partial-differential-equations-fall-2005/pages/assignments/") +
                        official_series("PS", range(1, 6), "MIT 18.303", "https://ocw.mit.edu/courses/18-303-linear-partial-differential-equations-analysis-and-numerics-fall-2014/pages/assignments"),
            "local": ("制造解驱动的 PDE 收敛验证",),
        },
        "35": {
            "materials": (("MIT 18.330", "https://ocw.mit.edu/courses/18-330-introduction-to-numerical-analysis-spring-2012/resources/problem-sets/", "MIT-OCW-CC/link-only"),),
            "official": official_series("HW", range(1, 9), "MIT 18.330", "https://ocw.mit.edu/courses/18-330-introduction-to-numerical-analysis-spring-2012/resources/problem-sets/"),
            "local": ("浮点、条件数与稳定性综合实验",),
        },
        "36": {
            "materials": (
                ("Stanford CS246", "https://web.stanford.edu/class/cs246/", "public-course/link-only"),
                ("Stanford CS276", "https://web.stanford.edu/class/cs276/", "public-course/Honor-Code/link-only"),
            ),
            "official": official_series("HW", range(1, 5), "Stanford CS246", "https://web.stanford.edu/class/cs246/") +
                        official_series("Colab", range(0, 10), "Stanford CS246", "https://web.stanford.edu/class/cs246/") +
                        named_official("Stanford CS276", "https://web.stanford.edu/class/cs276/",
                                       ["Programming Assignment 1", "Programming Assignment 2", "Programming Assignment 3",
                                        "Problem Set 1", "Problem Set 2"], "OF-CS276"),
            "local": ("MinHash/LSH", "推荐系统", "PageRank", "倒排索引", "检索评测", "稀疏—稠密—混合检索"),
        },
        "37": {
            "materials": (("MIT 18.04", "https://ocw.mit.edu/courses/18-04-complex-variables-with-applications-spring-2018/resources/problem-sets/", "MIT-OCW-CC/link-only"),),
            "official": official_series("PS", range(1, 10), "MIT 18.04", "https://ocw.mit.edu/courses/18-04-complex-variables-with-applications-spring-2018/resources/problem-sets/"),
            "local": ("解析性、留数与域着色验证",),
        },
    }

    catalogs = []
    for code, spec in specs.items():
        course, role = COURSE_INFO[code]
        materials = tuple(spec["materials"])
        official = tuple(spec.get("official", ()))
        local_topics = tuple(spec.get("local", ()))
        catalogs.append(CourseCatalog(code, course, role, materials, official, local_topics))
    return tuple(sorted(catalogs, key=lambda item: item.code))


CATALOGS = make_catalogs()

ROLE_EVIDENCE = {
    "program": ("README、独立实现、测试、运行日志与失败样本", "固定输入与版本下测试通过；不得复制公开答案"),
    "data": ("数据快照、实现、评价协议、偏差分析与报告", "切分和口径可复核；不得以单次最好结果通关"),
    "stats": ("分析计划、代码/推导、诊断、不确定性与报告", "假设、诊断与结论边界齐全；不得发生数据泄漏"),
    "proof": ("独立证明稿、引理依赖、反例与闭卷订正", "先独立完成再核对解答；抽样命题可闭卷重建"),
    "engineering": ("规格、实现/仿真、单元测试、约束与系统报告", "接口、性能约束和失败模式检查全部通过"),
    "applied": ("推导、数值实现、参考例、误差/稳定性与报告", "解析或独立基准一致；收敛和失败原因可解释"),
}


def capstone_path(catalog: CourseCatalog) -> str:
    if catalog.code == "03":
        return (
            "03-Projects/金融与时序/03-量化金融/"
            "HW17：Qlib 因子研究与成本敏感回测"
        )
    course_dir = PROJECT_ROOT / f"{catalog.code}-{catalog.course}"
    matches = sorted(course_dir.glob("项目-*.md"))
    if not matches:
        matches = sorted(course_dir.glob("大作业/项目-*.md"))
    # If multiple matches (e.g. many project proposals in 大作业/), filter by local topic
    if len(matches) > 1 and catalog.local_topics:
        topic_keywords = catalog.local_topics[0].split()
        filtered = [m for m in matches if any(kw in m.stem for kw in topic_keywords if len(kw) >= 4)]
        if len(filtered) == 1:
            matches = filtered
    if len(matches) != 1:
        raise RuntimeError(f"{course_dir}: expected one capstone, found {len(matches)}")
    return matches[0].relative_to(ROOT).with_suffix("").as_posix()


def all_units(catalog: CourseCatalog) -> tuple[Unit, ...]:
    primary_name, primary_url, _ = catalog.materials[0]
    return catalog.official + local_units(primary_name, primary_url, catalog.local_topics)


def render_catalog(catalog: CourseCatalog) -> str:
    units = all_units(catalog)
    evidence, acceptance = ROLE_EVIDENCE[catalog.role]
    materials = "\n".join(
        f"| [{name}]({url}) | `{policy}` | 不复制第三方答案；未激活时不整仓镜像 |"
        for name, url, policy in catalog.materials
    )
    summary_rows = "\n".join(
        f"| {unit.unit_id} | {unit.title} | `{unit.unit_type}` | planned |"
        for unit in units
    )
    sections = []
    for unit in units:
        if unit.unit_type == "official-link":
            task = (
                "从官方入口定位该作业；本库只记录题号、来源和自己的完成证据，"
                "不复制官方题干、Starter 压缩包或参考解答。"
            )
            source_policy = "官方公开入口，`link-only`；先独立完成，再按课程政策核对允许查看的解答。"
        else:
            task = f"围绕“{unit.title}”完成一份本地原创、可复核的小作业；不得冒充官方题目。"
            source_policy = "本地原创改编；外部来源只用于知识顺序和 API 文档。"
        sections.append(
            f"""### {unit.unit_id} · {unit.title}

- **类型**：`{unit.unit_type}`
- **来源**：[{unit.source}]({unit.url})
- **任务边界**：{task}
- **最低提交**：{evidence}
- **硬验收**：{acceptance}
- **答案策略**：{source_policy}
- **状态**：`planned`
"""
        )
    capstone = capstone_path(catalog)
    return f"""---
title: "{catalog.course}课程作业总表"
type: index
topic: "{catalog.course}完整作业包"
course: "{catalog.course}"
created: {DATE}
updated: {DATE}
status: active
flow: project
kind: moc
official_assignment_count: {len(catalog.official)}
local_extension_count: {len(catalog.local_topics)}
assignment_unit_count: {len(units)}
source_policy: link-only-by-default
solution_visibility: private
tags: [项目, 课程作业, 完整作业包, {catalog.course}]
---

# {catalog.course}课程作业总表

> 本页收齐该课程当前主来源公开列出的作业单元，并补齐本地课程需要的扩展主题。`official-link` 是官方作业入口，不代表材料允许任意复制；`local-original` 是本地原创改编。所有单元保持 `planned`，只有当前 Active Sprint 才进入执行队列。

## 1. 使用规则

1. 官方题目、Starter 和解答默认保持 `link-only`，不把“公开可访问”误写成“开放许可证”。
2. 只保存自己的作答、运行证据和错误订正；答案默认 `private`。
3. 同一时间只激活一个课程 Sprint；不因为作业已经编目就同时开课。
4. 官方解答存在时，必须先独立完成并提交闭卷版本，再按原课程政策核对。
5. 本页的最后一项验收仍由课程 Capstone 承担。

## 2. 开源与公开材料入口

| 来源 | 当前许可/策略 | 本地处理 |
|:---|:---|:---|
{materials}

## 3. 作业序列

| ID | 作业 | 性质 | 状态 |
|:---|:---|:---:|:---:|
{summary_rows}

## 4. 逐项执行卡

{chr(10).join(sections)}
## 5. 期末综合验收

- **Capstone**：[[{capstone}]]
- **通过条件**：Capstone Rubric ≥ 75/100、全部硬验收通过，且本课程被激活时的必做单元均已完成。
- **当前状态**：`planned`；作业编目完成不等于已经执行。

## 6. 完成回填

- 代码、证明、实验和报告进入本课程独立提交目录；
- 错误与失败反哺 `kind: mistake` 或 `problem-type`；
- 概念性结论链接 canonical 主卡，不复制百科式定义；
- 实际分数、运行日志和完成日期只能在真实执行后填写。
"""


def render_central_index() -> str:
    rows = []
    total_official = 0
    total_local = 0
    total_units = 0
    for catalog in CATALOGS:
        official = len(catalog.official)
        local = len(catalog.local_topics)
        units = official + local
        total_official += official
        total_local += local
        total_units += units
        rows.append(
            f"| {catalog.code} | {catalog.course} | [[03-Projects/课程作业/{catalog.code}-{catalog.course}/课程作业总表|作业总表]] "
            f"| {official} | {local} | {units} | planned |"
        )
    return f"""---
title: "33门课程完整作业包索引"
type: index
topic: "33门课程完整作业包"
created: {DATE}
updated: {DATE}
status: active
flow: project
kind: moc
course_count: 33
official_assignment_count: {total_official}
local_extension_count: {total_local}
assignment_unit_count: {total_units}
tags: [项目, 课程作业, 开源作业, MOC]
---

# 33 门课程完整作业包索引

> 每门课程都包含“官方公开作业入口＋本地原创扩展＋期末 Capstone”。官方内容默认只做 `link-only` 编目，不复制题干、Starter 或答案。

## 汇总

- 正式课程：**33**
- 课程内官方公开作业/实验入口条目：**{total_official}**（跨课程复用按课程重复计数）
- 本地原创扩展单元：**{total_local}**
- 作业单元合计：**{total_units}**
- 实际执行状态：除当前 Sprint 外均为 `planned`

## 课程作业包

| 编号 | 课程 | 完整作业包 | 官方入口 | 本地扩展 | 合计 | 状态 |
|:---:|:---|:---|---:|---:|---:|:---:|
{chr(10).join(rows)}

## 边界

- MIT OCW 等页面按其 Creative Commons/课程条款逐项使用；
- Stanford、Penn State、李宏毅课程等未明确允许整库再分发的材料保持 `link-only`；
- GitHub 仓库许可证只覆盖仓库内声明的内容，不自动覆盖数据、模型和第三方素材；
- 完整答案不进入公共知识卡，自己的提交默认 `private`。

## 审计

```powershell
python "99-System/tools/build_course_homework_catalogs.py" --check
python "99-System/tools/audit_course_homework_catalogs.py"
```

相关页面：

- [[03-Projects/课程作业/33门课程正式作业索引]]
- [[33门课程作业来源审计总表]]
- [[正式作业包修复审计-2026-07-28]]
"""


def replace_catalog_block(path: Path, catalog: CourseCatalog) -> None:
    text = path.read_text(encoding="utf-8")
    link = (
        f"[[03-Projects/课程作业/{catalog.code}-{catalog.course}/课程作业总表|"
        f"{catalog.course}完整作业包]]"
    )
    managed = (
        f"{BLOCK_START}\n"
        "## 🧰 完整作业包入口\n\n"
        f"- **官方作业序列＋本地扩展**：{link}\n"
        f"- 作业单元：**{len(all_units(catalog))}**（官方入口 {len(catalog.official)}，"
        f"本地扩展 {len(catalog.local_topics)}）。\n"
        "- 外部题目、Starter 与答案默认 `link-only`；编目完成不等于已经执行。\n"
        f"{BLOCK_END}"
    )
    if BLOCK_START in text and BLOCK_END in text:
        pattern = re.compile(re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END), re.S)
        updated = pattern.sub(managed, text)
    elif "<!-- formal-homework:start -->" in text:
        updated = text.replace("<!-- formal-homework:start -->", managed + "\n\n<!-- formal-homework:start -->", 1)
    elif "## 🧭 开源自学执行方案" in text:
        updated = text.replace("## 🧭 开源自学执行方案", managed + "\n\n---\n\n## 🧭 开源自学执行方案", 1)
    else:
        updated = text.rstrip() + "\n\n---\n\n" + managed + "\n"
    if updated != text:
        path.write_text(updated, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered: dict[Path, str] = {}
    for catalog in CATALOGS:
        path = PROJECT_ROOT / f"{catalog.code}-{catalog.course}" / "课程作业总表.md"
        rendered[path] = render_catalog(catalog)
    index_path = PROJECT_ROOT / "33门课程完整作业包索引.md"
    rendered[index_path] = render_central_index()

    if args.check:
        errors = []
        for path, expected in rendered.items():
            if not path.exists():
                errors.append(f"missing: {path.relative_to(ROOT)}")
            elif path.read_text(encoding="utf-8") != expected:
                errors.append(f"drift: {path.relative_to(ROOT)}")
        if errors:
            print("\n".join(errors))
            return 1
        print(
            f"PASS catalogs=33 official={sum(len(c.official) for c in CATALOGS)} "
            f"local={sum(len(c.local_topics) for c in CATALOGS)}"
        )
        return 0

    for path, content in rendered.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    for catalog in CATALOGS:
        resource = STUDY_ROOT / f"{catalog.code}-{catalog.course}" / "📚 教材挂载索引.md"
        replace_catalog_block(resource, catalog)
    print(
        f"WROTE catalogs=33 official={sum(len(c.official) for c in CATALOGS)} "
        f"local={sum(len(c.local_topics) for c in CATALOGS)} index=1 course_links=33"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
