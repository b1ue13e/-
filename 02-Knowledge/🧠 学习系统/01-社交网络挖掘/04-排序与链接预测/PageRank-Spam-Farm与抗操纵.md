---
type: study
topic: "PageRank Spam Farm 与抗操纵"
course: "社交网络挖掘"
created: 2026-08-06
status: planned
difficulty: advanced
concept: [Spam Farm, PageRank流量方程, 排名鲁棒性]
prerequisites: [PageRank, 线性方程, 出度分摊]
related: [PageRank-HITS与PPR, 链接预测与无泄漏评估]
flow: knowledge
kind: derivation
stage_moc: "[[🧭 阶段4-排序与链接预测]]"
upstream: ["[[PageRank-HITS与PPR]]"]
source: "Stanford CS224W 2017 HW4-Q1.3-Q1.5 and link analysis lecture"
source_url: "https://snap.stanford.edu/class/cs224w-2017/homeworks/hw4/hw4.pdf"
accessed: 2026-08-07
license: "课程题面公开访问但未核验开放再分发许可；本卡使用本地同构例，link-only"
assessment_exempt: false
tags: [学习, 社交网络挖掘, PageRank, SpamFarm, 鲁棒性]
---

# PageRank Spam Farm 与抗操纵

## 问题动机

PageRank 会沿链接传播分数，攻击者因此可以创建助推页，把每页获得的 teleport 质量集中到目标页。核心任务不是背攻击结构，而是把链接结构翻译成守恒方程，并和没有结盟的基线比较。

## 单目标反馈模型

设总页数为 $N$、阻尼为 $\beta$、每页 teleport 注入为 $\tau=(1-\beta)/N$。目标页 $p$ 指向 $k$ 个结构相同的助推页，每个助推页只指回目标。若外部流入 $\lambda$ 已包含阻尼，则

$$
p=\tau+\lambda+\beta k b,
$$

$$
b=\tau+\beta\frac{p}{k}.
$$

消元得到

$$
p=\frac{\tau+\lambda+\beta k\tau}{1-\beta^2}.
$$

分母中的 $\beta^2$ 来自“目标到助推页再回目标”的两次转移。

## 联盟与分流成本

多个目标结盟后可写成

$$
r_C=Cr_C+b,\qquad r_C=(I-C)^{-1}b.
$$

但新增联盟出边会改变原有出度分母。比较联盟时必须同时报告每个目标的增量和联盟总增量；“多一条入边”不保证净收益为正。

## 已解例

取 $N=10,k=2,\beta=1/2,\lambda=0$，则 $\tau=0.05$：

$$
p=\frac{0.05+0.5\times2\times0.05}{1-0.25}=\frac{2}{15},
$$

$$
b=0.05+\frac{0.5p}{2}=\frac1{12}.
$$

回代目标方程可验证两边相等。

## 可运行守恒检查

```python
import numpy as np

beta = 0.5
n_pages = 10
k = 2
tau = (1.0 - beta) / n_pages

feedback = np.array([[0.0, beta * k], [beta / k, 0.0]])
injection = np.array([tau, tau])
target, booster = np.linalg.solve(np.eye(2) - feedback, injection)

assert np.allclose([target, booster], feedback @ [target, booster] + injection)
print(round(target, 6), round(booster, 6))
```

## 常见错误

1. 漏掉每个受控页自己的 teleport 注入。
2. 没声明 $\lambda$ 是否已经包含阻尼，导致重复乘 $\beta$。
3. 只计算联盟结构，不计算独立基线。
4. 忽略新增出边带来的分流成本。
5. 把结构操纵分析误写成可直接部署的攻击方案；本课程只研究方程、检测和防御边界。

## 防御思路与代价

- 可信种子或 TrustRank：降低可疑区域自我强化，但引入种子偏差。
- 链接折损：抑制异常互链，但可能伤害真实小社区。
- 结构与内容联合检测：证据更全面，但需要额外数据并可能误报。

## 渐隐练习

去掉目标到助推页的回边，补全新的 $b$ 和 $p$ 方程，再说明为什么 $\beta^2p$ 项消失。随后增加一条联盟出边，先更新出度分母，再比较净增量。

## 闭卷验收

- 从图结构逐项写出 PageRank 守恒方程。
- 用对称性把 $k$ 个助推页合成一个变量。
- 消元并解释 $\beta^2$ 的来源。
- 区分个人收益与联盟总收益。
- 说明一种防御方法及其误伤代价。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/01-社交网络挖掘"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

