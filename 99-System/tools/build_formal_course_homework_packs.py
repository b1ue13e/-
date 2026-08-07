"""Build and maintain one formal, original capstone assignment for each course.

The generated notes are deliberately local specifications. External courses remain
link-only references; no third-party assignment text or solution is copied.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT / "03-Projects" / "课程作业"
STUDY_ROOT = ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统"
DATE = "2026-07-28"
BLOCK_START = "<!-- formal-homework:start -->"
BLOCK_END = "<!-- formal-homework:end -->"


# code, course, title, role, source name, source URL, dataset/input,
# baseline, independent work, robustness/advanced work, acceptance checks
COURSES = [
    ("01", "社交网络挖掘", "开放网络结构与链路预测审计", "data",
     "Stanford CS224W", "https://web.stanford.edu/class/cs224w/",
     "NetworkX `karate_club_graph()`；固定 NetworkX 版本并导出节点、边清单",
     "度数、连通分量、三角形和三种中心性；随机猜测链路作为下界",
     "实现共同邻居、Jaccard 与一个嵌入式链路预测器，使用固定负采样和时间/边切分",
     "比较社区算法与链路预测误差，分析高度节点、跨社区边和采样偏差",
     ["节点边数与 NetworkX 基准一致", "训练边与测试正边不重叠", "负样本不包含真实边", "固定种子可复现指标"]),
    ("02", "时间序列分析", "滚动预测与区间覆盖率审计", "stats",
     "Penn State STAT 510", "https://online.stat.psu.edu/stat510/",
     "statsmodels `sunspots` 内置数据；记录 statsmodels 版本和观测区间",
     "最后值 Naive 与季节 Naive；只使用历史窗口逐步预测",
     "比较 ETS 与 ARIMA，训练期选阶，测试期只做一次滚动评价",
     "检查残差、预测区间覆盖率、不同窗口和异常值处理的敏感性",
     ["所有预测只使用预测时点之前的数据", "Naive 与模型使用相同测试区间", "区间上下界顺序正确", "MAE 可由逐期误差复算"]),
    ("04", "离散数学", "图论命题证明与反例作品集", "proof",
     "MIT 6.042", "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/",
     "本地原创的 6 个有限图实例；邻接表直接写入提交物，不复制课程题目",
     "重建握手定理、树的等价刻画与一个归纳证明",
     "完成连通性、匹配或图着色命题的完整证明，并标注使用的引理",
     "为两个被削弱条件的命题构造最小反例，用穷举程序核验有限规模",
     ["每个量词和条件均被显式使用", "反例同时满足前提并否定结论", "穷举仅作核验而非替代证明", "闭卷可重建核心证明"]),
    ("05", "计算机视觉", "CIFAR-10分类与失败样本审计", "program",
     "Stanford CS231n 2025", "https://cs231n.stanford.edu/2025/assignments.html",
     "torchvision CIFAR-10；记录 torchvision 版本、官方 checksum 与固定切分",
     "像素标准化后的线性分类器或小型 CNN",
     "实现训练、验证、checkpoint 和混淆矩阵；比较小型 CNN 与 ResNet-18",
     "只改变一个增强/正则因素，报告类别级失败、校准和计算成本",
     ["训练与测试变换明确分离", "模型在固定小批量上可过拟合", "checkpoint 重载预测一致", "混淆矩阵总数等于测试样本数"]),
    ("06", "常微分方程", "ODE求解器误差与刚性诊断", "applied",
     "MIT 18.03", "https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/pages/assignments/",
     "指数衰减、受迫振子、Lotka–Volterra 与一个刚性线性系统；参数写入配置表",
     "显式 Euler 与解析解可得问题的误差对照",
     "实现 RK4，并与 `solve_ivp` 在相同步长/容差下比较",
     "用步长减半估计收敛阶，解释刚性系统上显式方法的失败",
     ["初值在首个网格点精确满足", "解析问题误差随步长缩小", "RK4 观察阶接近理论阶", "刚性失败可由稳定域解释"]),
    ("07", "最优化方法", "一阶与近端优化收敛审计", "applied",
     "Stanford EE364A", "https://see.stanford.edu/Course/EE364A",
     "固定种子生成的最小二乘与 Lasso；保存矩阵维度、条件数和生成参数",
     "固定步长梯度下降与 CVXPY 最优值对照",
     "实现回溯线搜索、加速梯度与 ISTA 中至少两种",
     "比较目标间隙、梯度/近端残差、时间和病态矩阵敏感性",
     ["目标值在接受步上不异常上升", "解与 CVXPY 目标间隙可复算", "Lasso 近端算子通过标量测试", "停止条件不读取参考最优解"]),
    ("08", "NLP全栈", "稀疏检索到Transformer的文本误差审计", "program",
     "Stanford CS224N", "https://web.stanford.edu/class/cs224n/",
     "scikit-learn 20 Newsgroups 固定四类子集；记录下载版本、类别和切分",
     "TF-IDF + Logistic Regression",
     "实现分词、训练、验证和 macro-F1；再比较一个小型 Transformer 或冻结嵌入模型",
     "按长度、类别、置信度和词汇漂移分析失败；RAG 不作为基础作业",
     ["词表只在训练集拟合", "macro-F1 可由混淆矩阵复算", "padding 不参与注意力", "相同切分用于所有模型"]),
    ("09", "高等代数", "矩阵分解与数值稳定性闭环", "applied",
     "MIT 18.06SC", "https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/",
     "固定的满秩、秩亏和 Hilbert 型矩阵；矩阵值与生成规则随报告提交",
     "高斯消元、正规方程最小二乘与 NumPy 对照",
     "实现 QR 最小二乘、幂法和截断 SVD 中至少两项",
     "报告分解残差、正交误差、条件数和病态输入上的误差放大",
     ["PA≈LU 或 A≈QR 的残差受控", "QᵀQ≈I", "秩亏输入不会静默给出错误结论", "SVD 重构误差随秩单调不增"]),
    ("10", "数据结构与算法", "算法实现、复杂度与随机测试", "program",
     "MIT 6.006", "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
     "固定种子生成数组、哈希键和带权图；同时保存小型手工反例",
     "线性扫描、标准库排序与邻接表 BFS",
     "独立实现哈希表、堆和 Dijkstra；不得调用同功能成品实现",
     "随机差分测试、复杂度斜率实验，并分析冲突和不可达节点",
     ["堆操作持续满足堆序", "Dijkstra 与 Bellman–Ford 在非负图上一致", "负权边被拒绝", "随机测试固定种子可复现"]),
    ("11", "计算机组成原理", "从逻辑门到CPU的分层规格测试", "engineering",
     "Nand2Tetris", "https://www.nand2tetris.org/",
     "Nand2Tetris 官方项目骨架与测试脚本；外部内容保持 link-only",
     "基础门、ALU 子功能和一个手写汇编程序",
     "完成 ALU、CPU、Assembler 与 VM Translator 的分层实现",
     "逐层回归测试，记录接口假设、边界输入和上层失败如何定位到底层",
     ["官方测试脚本全部保留原样运行", "ALU 状态位覆盖零/负边界", "汇编器符号表两遍处理正确", "VM 输出在小程序上与手工轨迹一致"]),
    ("12", "信号与系统", "采样、卷积与滤波器验证", "engineering",
     "MIT 6.003", "https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/",
     "本地合成正弦、脉冲、扫频和含噪信号；记录采样率、时长与随机种子",
     "直接卷积、FFT 频谱和移动平均滤波",
     "实现快速卷积与 FIR 设计，比较时域/频域解释",
     "改变采样率展示混叠，检查 Parseval、群延迟和边界填充影响",
     ["直接卷积与 FFT 卷积在容差内一致", "频率轴单位正确", "混叠频率可由公式预测", "滤波前后长度与延迟有明确定义"]),
    ("13", "强化学习", "价值学习与策略优化多种子审计", "program",
     "Berkeley CS188 Projects", "https://inst.eecs.berkeley.edu/~cs188/su25/projects/",
     "Gymnasium FrozenLake-v1 与 CartPole-v1；固定环境版本、终止语义和种子列表",
     "随机策略、Value Iteration 和表格 Q-learning",
     "实现 DQN 或 PPO，并与成熟实现按相同步数预算比较",
     "至少 5 个种子报告均值/离散度、样本效率、失败轨迹和奖励敏感性",
     ["terminated 与 truncated 分开处理", "Bellman 更新通过小 MDP 手算", "评估阶段关闭探索", "所有方法使用相同环境步数预算"]),
    ("14", "概率图模型", "结构、推断与采样一致性审计", "stats",
     "Stanford CS228", "https://cs.stanford.edu/~ermon/cs228/index.html",
     "本地原创的 5 节点离散 Bayesian Network；CPD 完整写入提交物",
     "枚举联合分布得到精确边缘",
     "实现变量消元，并用 pgmpy 复核；再实现拒绝采样或 Gibbs",
     "比较不同消元顺序和采样量，分析稀有证据与混合失败",
     ["每个 CPD 按父配置归一化", "枚举与变量消元一致", "无证据时采样边缘收敛", "D-separation 判断有图结构依据"]),
    ("15", "控制与机器人学", "移动机器人定位规划控制闭环", "engineering",
     "Modern Robotics", "https://github.com/NxRLab/ModernRobotics",
     "二维差速机器人仿真；固定地图、车辆参数、传感噪声和参考轨迹",
     "开环轨迹与 P 控制器",
     "实现位姿估计、路径规划和 PID/LQR 跟踪闭环",
     "扰动噪声、模型参数和执行延迟，检查碰撞、饱和、稳态误差与失败模式",
     ["坐标系和角度单位统一", "无障碍路径不穿越障碍", "控制输出遵守饱和约束", "相同扰动种子可重放轨迹"]),
    ("16", "多元统计", "高维结构与判别稳定性审计", "stats",
     "Penn State STAT 505", "https://online.stat.psu.edu/stat505/",
     "scikit-learn Wine 数据；记录数据版本、特征单位和固定分层切分",
     "原始变量 Logistic/LDA 与标准化 PCA",
     "比较 PCA、聚类、LDA/QDA，所有预处理只在训练折拟合",
     "bootstrap 检查载荷/聚类稳定性，分析尺度、异常值和类别不平衡",
     ["标准化不使用测试统计量", "PCA 方差比例总和合法", "聚类标签置换后再比较", "混淆矩阵与样本数一致"]),
    ("17", "机器学习", "表格建模、校准与漂移审计", "program",
     "李宏毅 ML 2021", "https://github.com/ga642381/ML2021-Spring",
     "scikit-learn Breast Cancer 数据；本作业为本地原创，不冒充官方 HW16",
     "Logistic Regression 与 Decision Tree",
     "比较 Random Forest/Gradient Boosting/MLP 中至少两种并做嵌套验证",
     "报告校准、特征重要性稳定性、阈值敏感性和合成分布漂移",
     ["预处理封装在 Pipeline", "测试集不参与模型选择", "概率位于 [0,1]", "漂移数据生成规则固定"]),
    ("22", "概率论与数理统计", "抽样分布与检验频率性质模拟", "stats",
     "MIT 6.041SC", "https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/",
     "固定种子生成 Bernoulli、Poisson、Normal 与重尾样本；参数写入预注册表",
     "大数定律与中心极限定理的蒙特卡洛验证",
     "实现置信区间与两类检验，比较理论与模拟覆盖率/错误率",
     "改变样本量、偏态和重尾程度，解释方法何时失效",
     ["概率和频率均在合法范围", "模拟重复次数独立于样本量", "零假设下 I 类错误可复算", "区间覆盖率按重复实验计算"]),
    ("23", "图神经网络", "节点分类与消息传递消融", "program",
     "Stanford CS224W", "https://web.stanford.edu/class/cs224w/",
     "PyTorch Geometric KarateClub；记录 PyG/PyTorch 版本、掩码与种子",
     "多数类、特征 MLP 与标签传播",
     "实现 GCN 与 GraphSAGE，固定切分和参数预算",
     "消融自环、层数、邻居采样和节点特征；分析过平滑和小样本方差",
     ["消息传递张量形状正确", "训练掩码与测试掩码不重叠", "无边图仍能前向", "多种子报告而非最佳单次"]),
    ("24", "随机过程", "Markov稳态、混合与队列模拟", "stats",
     "MIT 6.011", "https://ocw.mit.edu/courses/6-011-signals-systems-and-inference-spring-2018/resources/assignments/",
     "本地固定的有限状态转移矩阵与 M/M/1 参数组；全部参数写入提交物",
     "矩阵幂计算有限步分布和解析稳态",
     "实现 Markov 链与队列事件模拟，比较理论稳态和经验频率",
     "改变初始分布、谱隙和负载率，分析混合慢与队列不稳定",
     ["转移矩阵每行归一化", "稳态满足 πP≈π", "事件时间单调递增", "负载率≥1 时不误报稳定均值"]),
    ("25", "测度论", "可测性与收敛定理证明档案", "proof",
     "MIT 18.102", "https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2021/pages/lecture-notes-and-readings/",
     "本地原创的集合列、简单函数和函数列；不复制课程习题或答案",
     "从定义证明一个 σ-代数闭包性质和简单函数积分性质",
     "完成 Fatou、单调收敛或控制收敛中的一条证明依赖图及关键引理重建",
     "对缺少关键条件的版本构造反例，并说明逐点/a.e./依测度收敛差异",
     ["所有“几乎处处”例外集被说明", "极限与积分交换有定理条件", "反例满足其余条件", "闭卷能陈述并重建依赖链"]),
    ("26", "实变函数", "极限、连续与一致收敛证明作品集", "proof",
     "MIT 18.100C", "https://ocw.mit.edu/courses/18-100c-real-analysis-fall-2012/pages/assignments/",
     "本地原创序列、函数列和紧致性命题；官方题目仅作为阅读入口",
     "用 ε–N/ε–δ 语言重建序列极限与连续性证明",
     "完成一致收敛、紧致性或度量空间完备性的两条证明",
     "为交换极限、积分或连续性结论构造最小反例并画依赖图",
     ["量词顺序正确", "使用紧致性处明确指出", "反例逐项验证", "闭卷口述不依赖计算图"]),
    ("27", "泛函分析", "Banach与Hilbert空间定理链", "proof",
     "MIT 18.102", "https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2009/pages/assignments/",
     "本地原创的 ℓp、C[0,1] 和有限维算子例子；外部题目 link-only",
     "证明一个范数空间完备性或有界线性泛函性质",
     "完成 Hahn–Banach、统一有界或开映射定理的依赖链重建与一个应用",
     "构造有限维直觉失效的无限维反例，用矩阵截断仅作现象验证",
     ["空间、范数和拓扑均明确", "定理前提逐项核对", "反例说明失败结论", "计算验证不替代无限维证明"]),
    ("28", "数学分析", "核心定理与反例闭卷重建", "proof",
     "MIT 18.100A", "https://ocw.mit.edu/courses/18-100a-real-analysis-fall-2020/",
     "本地原创的实数、序列、级数、连续与微分命题组",
     "重建上确界性质、单调收敛和介值定理中的两条",
     "完成紧致性、Riemann 可积性或一致连续性的证明组合",
     "削弱条件并构造反例，制作定义—引理—定理依赖图和闭卷抽测",
     ["定义无循环依赖", "每个存在性结论给出依据", "反例满足保留条件", "随机抽题可在限定时间重建"]),
    ("29", "运筹学", "排程与资源分配求解器报告", "engineering",
     "MIT 15.053", "https://ocw.mit.edu/courses/15-053-optimization-methods-in-management-science-spring-2013/pages/assignments/",
     "固定的 10 作业×3 机器 Job-Shop 实例和小型手算实例；数据随报告提交",
     "贪心排程与线性松弛下界",
     "使用 OR-Tools CP-SAT 建模，显式写出变量、约束和目标",
     "规模扩展、时间上限、最优间隙与不可行实例诊断",
     ["无任务在同一机器重叠", "前后约束满足", "小实例达到已知最优", "超时结果标注 bound 与 gap"]),
    ("30", "应用回归分析", "回归诊断与样本外解释", "stats",
     "Penn State STAT 462", "https://online.stat.psu.edu/stat462/",
     "statsmodels Longley 数据；记录版本、变量定义与固定留出方案",
     "均值预测、单变量 OLS 与全变量 OLS",
     "完成残差、影响点、共线性和变换诊断，再比较 Ridge/Lasso",
     "bootstrap 系数稳定性、异常点敏感性与样本外误差分析",
     ["设计矩阵含截距且维度正确", "诊断只解释不自动删点", "变换后预测正确还原", "测试集不参与变量筛选"]),
    ("31", "属性数据分析", "列联表到多类响应建模", "stats",
     "Penn State STAT 504", "https://online.stat.psu.edu/stat504/",
     "本地固定的三张列联表与一个合成二项/多项数据集；生成参数随报告提交",
     "比例差、优势比、卡方独立性检验",
     "实现二项 Logistic，再扩展到多类或有序响应模型",
     "检查稀疏单元、完全分离、过度离散与不同编码的敏感性",
     ["列联表总数与原始记录一致", "优势比方向解释正确", "预测概率按行归一化", "完全分离被检测并报告"]),
    ("32", "非参数统计", "重采样、秩检验与核方法比较", "stats",
     "Penn State STAT 415", "https://online.stat.psu.edu/stat415/",
     "固定种子生成正态、偏态、重尾和含离群点样本；参数写入预注册表",
     "t 检验/参数区间作为对照，置换检验与 bootstrap 区间",
     "实现 Wilcoxon/秩和检验和核密度估计，统一评价协议",
     "比较不同分布、样本量、带宽与异常值下的功效、覆盖率和稳定性",
     ["置换保持零假设交换性", "bootstrap 按样本为单位重采样", "p 值计算包含观测统计量", "带宽敏感性有多档结果"]),
    ("33", "贝叶斯统计", "层级模型与后验预测审计", "stats",
     "Statistical Rethinking 2024", "https://github.com/rmcelreath/stat_rethinking_2024",
     "本地固定的多组二项数据；组大小、成功数与生成参数随报告提交",
     "共轭 Beta-Binomial 与完全池化模型",
     "使用 PyMC 建立部分池化层级模型并完成采样诊断",
     "先验敏感性、后验预测检查、LOO/预测比较和弱识别讨论",
     ["先验预测在观测尺度上可解释", "R-hat/ESS/发散均报告", "后验预测维度正确", "不把后验概率误写为频率 p 值"]),
    ("34", "偏微分方程", "制造解驱动的PDE收敛验证", "applied",
     "MIT 18.152", "https://ocw.mit.edu/courses/18-152-introduction-to-partial-differential-equations-fall-2005/pages/assignments/",
     "单位区间/方形域上的 Poisson 与热方程制造解；边界和源项由解析解导出",
     "一维有限差分 Poisson 与显式热方程",
     "扩展到二维或隐式时间推进，并与解析制造解比较",
     "网格细化估计收敛阶，检查稳定性条件、边界误差和求解成本",
     ["边界值精确施加", "离散算子符号正确", "误差随网格细化下降", "显式热方程违反 CFL 时能识别失败"]),
    ("35", "数值分析", "浮点、线性系统与迭代稳定性", "applied",
     "MIT 18.330", "https://ocw.mit.edu/courses/18-330-introduction-to-numerical-analysis-spring-2012/resources/problem-sets/",
     "固定的消去误差表达式、Hilbert 矩阵和稀疏 SPD 系统；生成规则随报告提交",
     "直接公式、LU 与 Jacobi 迭代",
     "实现稳定改写、QR/Cholesky 和 CG 中至少两项",
     "精度、条件数、残差与前向误差分离；规模和容差敏感性",
     ["稳定改写在小参数下优于直接公式", "残差不被误当作前向误差", "SPD 检查先于 Cholesky/CG", "停止条件使用可解释范数"]),
    ("36", "数据挖掘与信息检索", "稀疏、稠密与混合检索评测", "program",
     "Stanford CS246", "https://web.stanford.edu/class/cs246/",
     "自建 30—100 篇可再分发短文档与 15 条查询；提交文档来源、相关性标注和版本",
     "Boolean、TF-IDF 与 BM25",
     "实现倒排索引、BM25，再比较一个稠密检索器和混合融合",
     "报告 Recall@k、MRR/nDCG、时延、索引大小和逐查询失败类型",
     ["倒排表文档频率正确", "训练/调参查询与测试查询分离", "nDCG 可由标注复算", "所有方法使用相同语料快照"]),
    ("37", "复变函数", "解析性、留数与域着色验证", "applied",
     "MIT 18.04", "https://ocw.mit.edu/courses/18-04-complex-variables-with-applications-spring-2018/resources/problem-set-solutions/",
     "本地原创的多项式、有理函数、指数函数和保角映射参数组",
     "Cauchy–Riemann 手算与复平面网格可视化",
     "完成留数积分、零极点分析和域着色实现",
     "比较解析/非解析函数、绕数与映射边界；用数值围道积分核验而非替代证明",
     ["CR 条件与定义域同时检查", "零极点位置与阶数正确", "围道避开奇点或明确主值", "数值积分随离散加密收敛"]),
]


ROLE_RUBRICS = {
    "program": [("正确性与测试", 25), ("公平基线与切分", 20), ("实验与失败分析", 20), ("工程与复现", 20), ("报告与知识反哺", 15)],
    "data": [("数据与口径", 20), ("算法正确性", 25), ("评价协议", 20), ("稳健性与偏差", 20), ("复现与报告", 15)],
    "stats": [("数据与分析计划", 20), ("模型与估计", 20), ("诊断与假设", 20), ("稳健性与不确定性", 20), ("复现与解释", 20)],
    "proof": [("定义与命题", 20), ("证明链正确性", 30), ("反例与条件辨析", 20), ("闭卷重建与口试", 15), ("表达与依赖图", 15)],
    "engineering": [("规格与接口", 20), ("正确性与分层测试", 25), ("仿真与性能约束", 20), ("失败模式与安全边界", 20), ("复现与系统报告", 15)],
    "applied": [("数学建模与推导", 25), ("数值正确性", 20), ("收敛/稳定性证据", 25), ("敏感性与失败分析", 15), ("复现与报告", 15)],
}

ROLE_STARTERS = {
    "program": """```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ExperimentConfig:
    seed: int = 42

def load_data(config: ExperimentConfig):
    raise NotImplementedError

def build_baseline(config: ExperimentConfig):
    raise NotImplementedError

def evaluate(model, data) -> dict[str, float]:
    raise NotImplementedError
```""",
    "data": """```python
def load_snapshot():
    \"\"\"Return immutable raw data plus a version manifest.\"\"\"
    raise NotImplementedError

def make_split(data, seed=42):
    raise NotImplementedError

def evaluate_predictions(y_true, y_score):
    raise NotImplementedError
```""",
    "stats": """```text
analysis-plan.md
├── estimand / research question
├── data-generating assumptions
├── split or resampling protocol
├── primary model and baseline
├── diagnostics
└── robustness checks
```""",
    "proof": """```text
proof-portfolio.md
├── definitions
├── proposition
├── dependency graph
├── proof
├── condition audit
├── counterexample
└── closed-book reconstruction log
```""",
    "engineering": """```python
class SystemUnderTest:
    def reset(self, config):
        raise NotImplementedError

    def step(self, input_):
        raise NotImplementedError

    def diagnostics(self) -> dict:
        raise NotImplementedError
```""",
    "applied": """```python
def reference_case():
    \"\"\"Small case with an analytic or independently verified answer.\"\"\"
    raise NotImplementedError

def solve(problem, resolution_or_tolerance):
    raise NotImplementedError

def error_metrics(reference, estimate) -> dict[str, float]:
    raise NotImplementedError
```""",
}


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_assignment(item: tuple) -> str:
    code, course, title, role, source_course, source_url, dataset, baseline, independent, robustness, checks = item
    path_name = f"{code}-{course}"
    rubric = ROLE_RUBRICS[role]
    rubric_rows = "\n".join(
        f"| {name} | {score} | 证据完整、可复核且没有硬失败 | /{score} |"
        for name, score in rubric
    )
    check_rows = "\n".join(f"- [ ] `{index + 1:02d}` {check}" for index, check in enumerate(checks))
    return f"""---
title: {yaml_quote(title)}
type: project
topic: {yaml_quote(title)}
course: {yaml_quote(course)}
created: {DATE}
updated: {DATE}
status: planned
progress: 0%
flow: project
kind: project
project_type: homework
asset_eligibility: eligible
eligibility_audited: {DATE}
difficulty_tier: T3
source_url: {yaml_quote(source_url)}
source_course: {yaml_quote(source_course)}
source_version: {yaml_quote(f"link-only snapshot verified {DATE}; exact release/commit must be frozen when activated")}
license: {yaml_quote("本地原创作业规格；外部课程与素材保持 link-only，并按各自条款使用")}
mirror_policy: link-only
adaptation: original
dataset_version: {yaml_quote(dataset)}
starter_code: {yaml_quote(f"03-Projects/课程作业/{path_name}/{Path('项目-' + title + '.md').name}#5-starter-与提交结构")}
tests: {yaml_quote(f"03-Projects/课程作业/{path_name}/{Path('项目-' + title + '.md').name}#6-验收测试")}
baseline: {yaml_quote(baseline)}
acceptance_test: {yaml_quote("Rubric ≥ 75/100，全部硬验收通过，且无失败条件")}
compute_budget: low
solution_visibility: private
tags: [项目, 正式作业, {course}, 课程验收]
---

# {title}

> 这是为 `{course}` 编写的**本地原创正式作业**。外部课程只决定知识顺序和参考边界；本页不复制外部题目、Starter 或答案。课程未成为 Active Sprint 前，状态保持 `planned`。

## 1. 任务与学习结果

完成后需要证明：你不仅能复述知识，还能在固定输入、明确协议和失败条件下独立得到可复核结果。

- **输入/数据**：{dataset}。
- **朴素基线**：{baseline}。
- **独立实现**：{independent}。
- **强验证**：{robustness}。

## 2. 来源与使用边界

- **Spine**：[{source_course}]({source_url})，仅作为学习顺序与公开入口。
- **本地内容**：任务改写、评价协议、Rubric 和提交结构均为原创。
- **镜像策略**：`link-only`；激活课程时再记录精确版本、许可证、数据条款和环境锁文件。
- **答案策略**：只保存自己的实现与摘要；完整解答保持私有，不挂他人答案仓库。

## 3. 执行阶段

| 阶段 | 工作 | 必交证据 |
|:---|:---|:---|
| T1 规格与最小例 | 冻结输入、环境、随机种子和评价口径 | manifest、最小手算/已知答案例 |
| T2 Baseline | 完成朴素方法并逐项解释 | 基线输出、测试与误差记录 |
| T3 独立实现 | {independent} | 实现、日志、同口径比较 |
| T4 强验证 | {robustness} | 敏感性、失败案例与结论边界 |

## 4. 数据、版本与复现清单

- [ ] 记录来源 URL、访问日期和适用条款。
- [ ] 冻结数据快照、生成规则或 `not-applicable` 原因。
- [ ] 记录软件版本、随机种子与运行入口。
- [ ] Baseline 和改进方法使用相同输入与评价口径。
- [ ] 结果表中不预填成绩，不把单次最好结果当结论。

## 5. Starter 与提交结构

{ROLE_STARTERS[role]}

```text
submission/
├── README.md
├── manifest.yml
├── src-or-proofs/
├── tests-or-checks/
├── artifacts/
└── report.md
```

`manifest.yml` 至少记录：来源、版本、数据、环境、种子、运行入口、输出清单和已知限制。

## 6. 验收测试

以下是硬验收，任一项失败都不能依靠总分抵消：

{check_rows}
- [ ] 所有产出可从 `README.md` 按顺序复核。
- [ ] 报告包含至少一个失败案例和适用边界。

## 7. 100 分 Rubric

| 维度 | 分值 | 通过证据 | 得分 |
|:---|---:|:---|:---:|
{rubric_rows}
| **总计** | **100** | **达到 75 分且硬验收全部通过** | **/100** |

## 8. 失败条件

- 使用测试数据、参考答案或未来信息参与方法选择；
- 来源、数据、环境或随机性无法追溯；
- Baseline 与改进方法使用不同评价口径；
- 只展示成功结果，不报告反例、诊断或失败模式；
- 复制外部课程答案，或把公开可见误认为允许再分发；
- 无法从提交物独立复核关键结论。

## 9. 提交物

- [ ] `README.md`：一条从环境到结果的复核路径；
- [ ] `manifest.yml`：版本、数据、条款、环境与种子；
- [ ] 实现、证明或分析计划；
- [ ] 硬验收测试及真实输出；
- [ ] Baseline 与强验证对比；
- [ ] `report.md`：结论、失败案例、限制与知识反哺。

## 10. 知识反哺

完成后至少沉淀一项：

- 概念误解 → `kind: concept`；
- 可复用证明/解法 → `kind: derivation` 或 `problem-type`；
- 失败与漏洞 → `kind: mistake`，必要时设置 `flow: review`。

## 11. 当前状态

| 项目 | 状态 |
|:---|:---:|
| 正式作业规格 | completed |
| 来源与镜像边界 | completed |
| 精确版本与环境冻结 | activation-gated |
| 实际执行与评分 | planned |
"""


def replace_managed_block(path: Path, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    managed = f"{BLOCK_START}\n{block.rstrip()}\n{BLOCK_END}"
    if BLOCK_START in text and BLOCK_END in text:
        pattern = re.compile(re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END), re.S)
        updated = pattern.sub(managed, text)
    elif "## 🧭 开源自学执行方案" in text:
        # Keep the formal assignment entry outside the execution-plan section so
        # route-audit similarity checks continue to measure only course content.
        updated = text.replace(
            "## 🧭 开源自学执行方案",
            managed + "\n\n---\n\n## 🧭 开源自学执行方案",
            1,
        )
    else:
        updated = text.rstrip() + "\n\n---\n\n" + managed + "\n"
    if updated != text:
        path.write_text(updated, encoding="utf-8")


def build_index(rows: list[tuple[str, str, str, str]]) -> str:
    table = "\n".join(
        f"| {code} | {course} | [[03-Projects/课程作业/{code}-{course}/{file_stem}|{title}]] | planned | eligible |"
        for code, course, title, file_stem in rows
    )
    return f"""---
title: "33门课程正式作业索引"
type: index
topic: "33门课程正式作业"
created: {DATE}
updated: {DATE}
status: active
flow: project
kind: moc
tags: [项目, 正式作业, 课程验收, MOC]
---

# 33 门课程正式作业索引

> 每门正式课程至少有一份可执行、可验收的本地原创作业。`planned` 表示作业包已经准备好但尚未成为当前 Sprint；不表示已经完成作业。

## 使用规则

1. 同一时间只执行 Active Sprint 对应的作业。
2. 外部课程保持 `link-only`，不复制或分发课程答案。
3. 激活时冻结精确 commit/release、数据条款和环境锁文件。
4. `asset_eligibility: eligible` 只表示规格完整，不表示已经运行或通过。
5. 旧项目继续作为 `reference-only`，不会自动升级。

## 正式作业

| 编号 | 课程 | 正式作业 | 状态 | 资格 |
|:---:|:---|:---|:---:|:---:|
{table}

## 审计入口

```powershell
python "99-System/tools/audit_formal_homework_packs.py"
python "99-System/tools/audit_homework_assets.py"
```

相关页面：

- [[03-Projects/课程作业/33门课程完整作业包索引]]
- [[02-Knowledge/MOC/33门课程开源自学与验收总索引]]
- [[33门课程作业来源审计总表]]
- [[正式作业包修复审计-2026-07-28]]
- [[旧项目与作业资产资格审计-2026-07-28]]
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify generated files without writing")
    args = parser.parse_args()

    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    rows: list[tuple[str, str, str, str]] = []
    errors: list[str] = []
    rendered: dict[Path, str] = {}

    for item in COURSES:
        code, course, title = item[:3]
        course_dir = PROJECT_ROOT / f"{code}-{course}"
        file_stem = f"项目-{title}"
        path = course_dir / f"{file_stem}.md"
        content = render_assignment(item)
        rendered[path] = content
        rows.append((code, course, title, file_stem))

    # Quant finance already has the fully specified Qlib HW17; keep a single canonical assignment.
    qlib_path = (
        ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统" / "03-量化金融"
        / "18-实战作业说明书" / "HW17-Qlib因子研究与成本敏感回测作业说明书.md"
    )
    rows.insert(2, (
        "03", "量化金融", "Qlib因子研究与成本敏感回测",
        "__QLIB_HW17__",
    ))

    index_path = PROJECT_ROOT / "33门课程正式作业索引.md"
    index_content = build_index(rows).replace(
        "[[03-Projects/课程作业/03-量化金融/__QLIB_HW17__",
        "[[02-Knowledge/🧠 学习系统/03-量化金融/18-实战作业说明书/"
        "HW17-Qlib因子研究与成本敏感回测作业说明书",
    )
    rendered[index_path] = index_content

    if args.check:
        for path, expected in rendered.items():
            if not path.exists():
                errors.append(f"missing: {path.relative_to(ROOT)}")
            elif path.read_text(encoding="utf-8") != expected:
                errors.append(f"drift: {path.relative_to(ROOT)}")
        if errors:
            print("\n".join(errors))
            return 1
        print(f"PASS generated packs={len(COURSES)} index=1")
        return 0

    for path, content in rendered.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    for item in COURSES:
        code, course, title = item[:3]
        resource_path = STUDY_ROOT / f"{code}-{course}" / "📚 教材挂载索引.md"
        link = f"[[03-Projects/课程作业/{code}-{course}/项目-{title}|{title}]]"
        replace_managed_block(
            resource_path,
            "## ✅ 正式作业入口\n\n"
            f"- **课程正式作业**：{link}\n"
            "- `eligible` 表示规格、验收和来源边界完整；课程激活前仍保持 `planned`。\n"
            "- 旧项目只作参考，不能替代本作业的独立提交与验收。",
        )

    quant_resource = STUDY_ROOT / "03-量化金融" / "📚 教材挂载索引.md"
    replace_managed_block(
        quant_resource,
        "## ✅ 正式作业入口\n\n"
        "- **课程正式作业**：[[02-Knowledge/🧠 学习系统/03-量化金融/18-实战作业说明书/"
        "HW17-Qlib因子研究与成本敏感回测作业说明书|Qlib因子研究与成本敏感回测]]\n"
        "- 该作业是当前 Active Sprint 的唯一合格作业；旧 HW01—HW16 继续作为参考。",
    )

    print(f"WROTE formal_packs={len(COURSES)} course_links=33 index=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
