---
type: study
topic: "PageRank、HITS 与 PPR"
tags: [学习, 01-社交网络挖掘, PageRank, HITS]
created: 2026-08-05
status: completed
difficulty: advanced
concept: [PageRank, HITS, 个性化随机游走]
prerequisites: [有向网络统计与数据清洗, 马尔可夫链, 线性代数]
related: [中心性度量, 链接预测与无泄漏评估]
flow: knowledge
kind: derivation
source: "NCM Chapter 14; Stanford CS224W 2017 HW0-Q3 and HW4-Q1"
anki_deck: "社交网络挖掘::排序预测"
anki_tags: [PageRank, HITS, PPR, HW4]
---

# PageRank、HITS 与 PPR

## 0. 先判断它值不值得深挖
- **类别**：A 类；HW0 与 HW4 直接考查。
## 1. 这个知识点解决什么问题？
> 入度只数票，不考虑投票者质量；随机游走与 hub-authority 递归地传播声望，并用 teleport 解决陷阱和悬挂节点。
## 2. 为什么它重要？它有什么用？
- 网页排序、推荐、局部社区搜索、专家发现。
- PPR 对 teleport 向量线性，是 HW4 组合题核心。
## 3. 学它之前需要哪些前置知识？
1. [[../01-图与网络基础/有向网络统计与数据清洗]]。
2. 随机矩阵、特征向量、幂迭代。
## 4. 用直觉语言解释它
> PageRank 是会偶尔传送的随机浏览者；HITS 把好目录（hub）与好内容（authority）相互定义。
## 5. 正式定义、核心公式、符号解释
### 1. 最核心定义
列随机转移矩阵 $M$ 下：
$$r=\beta Mr+(1-\beta)s.$$
$s=\mathbf1/n$ 是全局 PageRank；任意偏好分布 $s$ 是 PPR。
### 2. 核心公式
HITS：$a=A^Th,\ h=Aa$，故 authority 是 $A^TA$ 主特征向量，hub 是 $AA^T$ 主特征向量。
### 3. 符号说明表
| 符号 | 含义 | 备注 |
| :--- | :--- | :--- |
| $\beta$ | 继续沿边概率 | 常取 0.85 |
| $s$ | teleport 分布 | 和为 1 |
| $r$ | 稳态排名 | 和为 1 |
### 4. 常见变体与适用条件
悬挂列应替换为 $s$ 或统一分布；矩阵行/列约定必须一致。topic-sensitive PageRank 预计算多个 $s$ 的解。
## 6. 推导思路和思想来源
无 teleport 时链可能不可约或周期；加入 $(1-\beta)s$ 保证从任意状态重启。线性方程 $(I-\beta M)r=(1-\beta)s$ 表明 $r$ 对 $s$ 线性，支持 HW4 的加权组合。
## 7. 例子：基础 → 中等 → 实际应用
### 例子 1（手算）
两节点互相指向、$s=(1,0)$、$\beta=0.5$：解 $r_1=0.5r_2+0.5,r_2=0.5r_1$，得 $(2/3,1/3)$。
### 例子 2
星型引用图中中心可能是 authority，指向多个高 authority 的索引页是 hub；两角色不必同一节点。
### 例子 3（代码）
```python
import networkx as nx
g = nx.DiGraph([(0, 1), (1, 0), (2, 1)])
ppr = nx.pagerank(g, alpha=0.85, personalization={0: 1, 1: 0, 2: 0})
hubs, authorities = nx.hits(g, max_iter=1000, normalized=True)
print(round(sum(ppr.values()), 12), max(authorities, key=authorities.get))
# 输出概率和 1；authority 最高节点为 1。
```
## 8. 常见误区和易混概念
- **误区**：PageRank 就是入度。纠正：分数由来源分数按出度分摊并含 teleport。
| 方法 | 递归关系 | 个性化 | 典型角色 |
| :--- | :--- | :--- | :--- |
| PageRank | 单一稳态 | 均匀 $s$ | 全局声望 |
| PPR | 单一稳态 | 任意 $s$ | 用户/主题相关 |
| HITS | hub-authority 双分数 | 查询子图常见 | 目录与内容 |
| 特征向量中心性 | $Ax=\lambda x$ | 否 | 无向/递归声望 |
## 9. 相关知识点与 Obsidian 双链建议
- 上游：[[../01-图与网络基础/有向网络统计与数据清洗]]。
- 下游：[[链接预测与无泄漏评估]]。
- 横向：[[中心性度量]]。
- 应用：HW0-Q3、HW4-Q1。
## 10. 闭卷复现任务
- [ ] 写出 PageRank/PPR 方程。
- [ ] 处理 dangling node。
- [ ] 手算两节点例子。
- [ ] 证明对 $s$ 线性。
- [ ] 写出 HITS 迭代。
- [ ] 区分 hub/authority。
- [ ] 解释 $\beta$。
- [ ] 复现代码。
- [ ] 检查概率和。
- [ ] 说明矩阵约定。
## 11. 自测题：5 道
1. PPR 与 PageRank 的唯一核心差异？ #自测题/基础
   > [!question]- teleport 分布 $s$ 是否个性化。
2. dangling node 是什么？ #自测题/基础
   > [!question]- 出度为 0 的节点，其转移列需补成重启/均匀分布。
3. $\beta$ 越大意味着什么？ #自测题/中等
   > [!question]- 更依赖链接结构、混合更慢且个性化影响相对减弱。
4. HITS authority 为什么对应 $A^TA$？ #自测题/中等
   > [!question]- 代入 $a=A^Th,h=Aa$ 得 $a=A^TAa$。
5. 证明 $r(s_1+s_2)=r(s_1)+r(s_2)$（未归一化线性输入）。 #自测题/较难
   > [!question]- $r=(1-\beta)(I-\beta M)^{-1}s$ 是关于 $s$ 的线性映射。
## 12. 我的主动回忆区
### 我的闭卷复述
> 
### 我的推导复现
> 
### 我的错误与卡点
- 
### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后
## 13. 给 Obsidian 的归档建议
- 文件夹：`04-排序与链接预测/`
- 关联：[[中心性度量]]
- 标签：`#PageRank` `#PPR` `#HITS`
- 拆分：三者同属链接分析并由 HW0/HW4 串联。
## 🃏 Anki 卡片
- PPR 方程是什么？::$r=\beta Mr+(1-\beta)s$。
- HITS 的 hub 与 authority 如何互相定义？::authority 由指向它的 hub 分数累加，hub 由它指向的 authority 分数累加。
