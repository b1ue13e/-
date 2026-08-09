---
type: project
project_type: homework
course: "机器学习"
assignment_id: "机器学习-07"
assignment_level: lesson
assignment_format: lab
stage_id: "05"
requires: ["[[机器学习-K-means++]]", "[[机器学习-主成分分析]]"]
source_type: official_assignment
source: "改编自 MIT 6.036 Introduction to Machine Learning (Fall 2020, MIT OpenCourseWare, CC BY-NC-SA 4.0) Problem Set 3：K-means / 高斯混合与 EM / PCA 降维（保留原题号与公式语义，非商用翻译改编）"
created: 2026-08-06
status: ongoing
flow: project
tags: [作业, 机器学习, 聚类, PCA, 降维]
license: "CC BY-NC-SA 4.0 (MIT OpenCourseWare)"
source_license_status: verified
source_verified_at: 2026-08-07

---

# 机器学习 · 课后作业 07：聚类与 PCA 降维

> 难度递进：基础 → 进阶 → 综合。本题不提供可直接提交的完整解答，只给检查点与 Rubric。

---

## 1. 作业身份

| 项 | 值 |
| :--- | :--- |
| 课程 | 机器学习 |
| 规模层级 | `lesson`（课后作业） |
| 任务形态 | `lab` |
| 编号 | 机器学习-07 |
| 所属阶段 | 05 · 其他方法 |
| 来源类型 | `local_integration_task` |
| 许可证 | 本地学习用途 |
| 版本 | v1 · 2026-08-06 |

---

## 名校作业来源（MIT 6.036）

> 本题主体改编自 **MIT 6.036 Introduction to Machine Learning（Fall 2020, MIT OpenCourseWare, CC BY-NC-SA 4.0）**，保留原题号与公式语义，依 CC BY-NC-SA 4.0 翻译/改编，非商用，出处标注 MIT OpenCourseWare。下列为该来源 Problem Set 3 的真实题型映射；环境/产物/Rubric 为本课程本地补充。

**改编题号与问题：**
- **K-means**：Lloyd 算法迭代、收敛性证明要点与 k 的选择（肘部法）。
- **高斯混合与 EM**：E 步责任度、M 步参数更新，对比 K-means 的软分配。
- **PCA**：协方差矩阵特征分解、主成分投影与白化。


## 2. 学习目标

完成本题后，你应当能够：

- **解释**：说明 K-means 的代价函数与 Lloyd 迭代，以及 PCA 如何找最大方差投影方向。
- **实现/分析**：用代码做无监督聚类与降维，并用肘部法/解释方差比选择超参。
- **诊断**：理解聚类对初始化与尺度的敏感性、PCA 的线性局限。

---

## 3. 所需知识

- [[机器学习-K-means|K-means]]：簇中心、Lloyd 算法、惯性（inertia）。
- [[机器学习-主成分分析|主成分分析]]：协方差矩阵、特征值分解、投影。

**允许工具**：`numpy`、`scikit-learn`、`matplotlib`。

---

## 4. 任务背景与边界

**场景**：你拿到一份无标签数据，需要先"看懂结构"（降维可视化）再"分组"（聚类）。

**输入/输出**：给定特征矩阵 $X$（无标签）；输出聚类标签、簇中心、降维散点图、指标。
**限制**：必须做标准化（聚类对尺度敏感）；禁止用标签作弊评估（除对照）。
**禁止**：直接提交第三方完整答案；使用历史改编标签命名。

---

## 5. 详细题目

### P1（基础 · K-means）聚类

用 `make_blobs(n_samples=300, centers=3, cluster_std=0.6, random_state=0)`：

1. 标准化后跑 `KMeans(n_clusters=3, random_state=0)`，报告惯性（inertia）与轮廓系数。
2. 画肘部图：扫描 $k\in\{2,3,4,5,6\}$ 的 inertia，标出肘点。
3. 用不同 `random_state` 跑 3 次，说明结果是否稳定（初始化敏感性）。

### P2（进阶 · PCA）降维与可视化

用 `load_iris()`（4 维）：

1. 标准化后做 PCA，报告前 2 个主成分的解释方差比（累计）。
2. 把数据投影到前 2 主成分，按真实类别上色画散点图。
3. 说明"为何降维后类别更可分"以及 PCA 的线性假设局限。

### P3（综合 · 流水线）聚类 + 降维结合

对 `make_moons(n_samples=300, noise=0.1, random_state=0)`（非线性结构）：

1. 直接 K-means（$k=2$）效果差，说明为何（非线性结构）。
2. 先用核 PCA（`KernelPCA(kernel='rbf')`）映射到高维再聚类，观察改善。
3. 对比"线性 PCA + K-means"与"核 PCA + K-means"在 moons 上的聚类纯度。

---

## 6. 环境与复现

- **语言/版本**：Python ≥ 3.11；`numpy`、`scikit-learn`、`matplotlib`。
- **随机种子**：固定 `random_state=0`。
- **硬件**：CPU 即可；预计运行 < 20s。

---

## 7. 提交产物

- `hw07_cluster_pca.py`：含 K-means/肘部/PCA/核PCA 实现与绘图。
- `hw07_elbow.png`、`hw07_pca_scatter.png`、`hw07_moons.png`。
- `机器学习-课后作业-07-解答.md`：指标、肘点判断、降维结论。

文件名前缀统一为 `机器学习-课后作业-07-`。

---

## 8. 验收标准与 Rubric（100 分）

| 维度 | 分值 | 正确性 / 完整性 / 解释质量 / 可复现 |
| :--- | :--- | :--- |
| P1 K-means | 30 | 惯性/轮廓正确、肘部图清晰、稳定性分析合理 |
| P2 PCA | 30 | 解释方差比正确、投影图正确、局限说明成立 |
| P3 流水线 | 25 | moons 对比合理、核 PCA 改善有证据 |
| 表达与可复现 | 15 | 种子固定、图清晰、交付物齐全 |
| **合计** | **100** | 指标与任务匹配 |

硬失败：未标准化、无肘部图或 PCA 投影图、种子未记录。

---

## 9. 引导与自检（不泄露答案）

- **P1 提示**：肘点是 inertia 下降"变缓"的拐点；随机初始化可能陷局部最优，多跑几次。
- **P2 调试**：若前两主成分累计方差比很低，说明数据本就高维分散。
- **P3 自检**：moons 是经典非线性，线性方法救不了——这正是核方法的用武之地。
- **提交前清单**：标准化做了？图含坐标轴/颜色条？

---

## 10. 知识依赖与后续

- 共同依赖见 frontmatter `requires`（K-means / 主成分分析）。
- **完成后进入**：阶段作业 05（其他方法综合）、课后作业 08（朴素贝叶斯与 EM）。
- 本作业"学完后可以完成"入口由 Dataview 反向查询自动生成。
