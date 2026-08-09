---

type: study

flow: knowledge

kind: concept

topic: "Boosting原理"

course: "机器学习"

module: "模块2：集成学习原理"

created: 2026-04-18

status: ongoing

difficulty: advanced

concept: ["Boosting原理"]

prerequisites: ["Bagging"]

related: ["随机森林", "XGBoost"]

source_textbook: ["机器学习（周志华）"]

source_sections: ["第8章"]

learning_objectives: ["说明 Boosting原理 在“模块2：集成学习原理”里解决的具体问题", "把 Boosting原理 对应回 第8章", "用一个最小例子或代表题解释 Boosting原理 的作用"]

deliverables: ["一句话定义或项目目标", "一个最小例子/代表题/最小实验", "一条易错点或跨路径连接", "能说清 Bagging 与 Boosting 的差异以及“多样性”的作用。"]

tags: ["机器学习", "学习"]

aliases: ["🎯 AdaBoost 算法 (Adaptive Boosting)"]

stage_moc: "[[🧭 阶段4-树与集成]]"

upstream: ["[[机器学习-Bagging]]"]

source: "周志华《机器学习》第4、8章"
source_url: "https://book.douban.com/subject/26708119/"
accessed: 2026-08-07
license: "[待验证]"

---



# Boosting原理



> 所属路径：[[🗺️ 机器学习学习路径|机器学习学习路径]]

> 所属阶段：[[🧭 阶段4-树与集成|返回阶段页]]

> 所属模块：`模块2：集成学习原理`



## 为什么学

- 这张卡位于“模块2：集成学习原理”，用来解决：为什么把弱学习器组合起来，反而能得到更稳更强的模型？

- 它是你从 [[机器学习-Bagging]] 走向 [[机器学习-随机森林]]、[[机器学习-XGBoost]] 的桥梁。



## 教材定位

- 主教材：`机器学习（周志华）`

- 对应章节：第8章

- 阶段入口：[[🧭 阶段4-树与集成|🌲 第四阶段：树与集成]]



## 必须掌握

- 用自己的话定义 `Boosting原理`，并说清它的边界。

- 解释 `Boosting原理` 为什么是“为什么把弱学习器组合起来，反而能得到更稳更强的模型？”这条问题链的一部分。

- 说明它和同阶段相邻概念的区别与联系。



## 关键问题

- Boosting原理 在“模块2：集成学习原理”这条主线里具体负责哪一步？

- 如果忽略 Boosting原理，为什么把弱学习器组合起来，反而能得到更稳更强的模型？ 会在哪一步断掉？

- Boosting原理 和相邻概念的边界是什么？



## 最小例子

- 场景：

- 输入：

- 关键一步：

- 结论：



## 练习与输出

- [ ] 写 3-5 行自己的定义或项目目标。

- [ ] 补一个最小例子、例题、推导片段或实验记录。

- [ ] 记录一个易错点，或补一条跨路径连接。



## 完成标准

- [ ] 能说清 Bagging 与 Boosting 的差异以及“多样性”的作用。

- [ ] 能独立解释这张卡在本阶段中的位置。

- [ ] 能把教材章节和这张卡一一对应。



## 前后连接

- 前置：[[机器学习-Bagging]]

- 相关：[[机器学习-随机森林]]、[[机器学习-XGBoost]]

- 返回阶段页：[[🧭 阶段4-树与集成|🌲 第四阶段：树与集成]]



*创建于：2026-04-18*



---





## 补充代码示例（自旧版合并保留）



```python

import torch



# ---------------------------------------------------------------

# 1. 模拟一维非线性二分类数据集 (Labels y in {-1, +1})

# ---------------------------------------------------------------

torch.manual_seed(42)

N = 100

X = torch.linspace(-3, 3, N).unsqueeze(1) # [100, 1]

# 真实分布：中间为 +1，两边为 -1 (一维非线性切分)

y = torch.ones(N)

y[(X[:, 0] < -1.5) | (X[:, 0] > 1.5)] = -1.0



# ---------------------------------------------------------------

# 2. 弱分类器：一维决策树桩 (Decision Stump)

# ---------------------------------------------------------------

class DecisionStump:

    def __init__(self):

        self.feature_idx = 0

        self.threshold = 0.0

        self.polarity = 1

        self.alpha = 0.0



    def predict(self, X):

        N = X.shape[0]

        preds = torch.ones(N)

        if self.polarity == 1:

            preds[X[:, self.feature_idx] < self.threshold] = -1.0

        else:

            preds[X[:, self.feature_idx] >= self.threshold] = -1.0

        return preds



# ---------------------------------------------------------------

# 3. 手写 AdaBoost 训练循环 (10 个弱树桩集成)

# ---------------------------------------------------------------

M = 10

stumps = []

w = torch.ones(N) / N # 初始均匀样本权重



for m in range(M):

    stump = DecisionStump()

    min_error = float('inf')

    

    # 寻找最佳树桩切分点

    for thresh in torch.linspace(-3, 3, 50):

        for pol in [1, -1]:

            temp_stump = DecisionStump()

            temp_stump.threshold = thresh

            temp_stump.polarity = pol

            preds = temp_stump.predict(X)

            

            # 计算加权误差率 e_m

            err = (w * (preds != y).float()).sum().item()

            if err < min_error:

                min_error = err

                stump.threshold = thresh

                stump.polarity = pol



    # 计算基分类器权重 alpha_m

    e_m = max(min_error, 1e-10) # 避免除零

    alpha_m = 0.5 * torch.log(torch.tensor((1.0 - e_m) / e_m)).item()

    stump.alpha = alpha_m

    stumps.append(stump)

    

    # 更新样本权重 w

    G_pred = stump.predict(X)

    w = w * torch.exp(-alpha_m * y * G_pred)

    w = w / w.sum() # 归一化



# ---------------------------------------------------------------

# 4. 强分类器预测与评估

# ---------------------------------------------------------------

final_scores = torch.zeros(N)

for stump in stumps:

    final_scores += stump.alpha * stump.predict(X)



final_preds = torch.sign(final_scores)

acc = (final_preds == y).float().mean().item()



print("=== PyTorch 手写 AdaBoost 算法训练完毕 ===")

print(f"集成 10 个一维决策树桩后的最终准确率: {acc * 100:.2f}%")

```

## 学完后可以完成



> 下面由作业 `requires` 自动反查：学完本卡后可完成的课后作业、阶段作业与大作业（单一事实源，不手动维护）。



```dataview

LIST

FROM "03-Projects"

WHERE type = "project" AND contains(map(requires, (r) => r.path), this.file.name)

SORT assignment_level ASC, file.name ASC

```

