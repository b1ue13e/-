---
type: study
topic: "backward stability"
created: 2026-04-17
status: ongoing
difficulty: beginner
concept: ["backward stability", "条件与稳定"]
prerequisites: ["condition number"]
related: ["condition number", "敏感性"]
tags: ["学习", "数值分析", "条件与稳定"]
---
# backward stability

> 所属阶段：[[🧮 第一阶段：误差与数值线代|🧮 第1阶段：误差与数值线代]]

## 学习定位
- 路径：[[../🗺️ 数值分析学习路径|数值分析学习路径]]
- 阶段：[[🧮 第一阶段：误差与数值线代|🧮 第1阶段：误差与数值线代]]
- 模块：条件与稳定
- 建议先学：[[误差与数值线代-条件与稳定-condition number]]

## 一句话定义
> backward stability 表示算法给出的结果等价于某个“略微扰动过的输入”的精确解。 放回这一模块里看，它主要回答的是：backward stability 在 条件与稳定 里的结构、条件与用途。

## 这个知识点要解决什么问题
- backward stability 具体在衡量什么，为什么它会直接影响结果是否可信？
- 一旦 backward stability 变差，误差、解或推断会如何被放大？
- 它和 condition number 之间是什么关系，实际分析里该先看哪一个？

## 核心内容
### 1. 基本定义与直觉
> backward stability 表示算法给出的结果等价于某个“略微扰动过的输入”的精确解。 在这一页里，先把它和“问题条件数、后向稳定与算法鲁棒性”这条模块主线接起来，再谈公式、性质或算法。

### 2. 公式 / 机制 / 流程
> 这一节重点交代 backward stability 的判别方式、它受什么因素影响，以及它变差时会怎样传导到最终结果。

### 3. 一个最小例子
> 最小例子可以放在：输入扰动会如何放大到输出误差。写的时候把“输入是什么、backward stability 在哪一步出现、结论怎么解释”各写一小行。

### 4. 常见误区
- 不要把 backward stability 当成抽象标签，要说明它具体影响哪种误差或判断。
- 不要只做定性描述，最好给出一个会让 backward stability 变差的具体场景。

## 和其他笔记的关系
- 前置：[[误差与数值线代-条件与稳定-condition number]]
- 相关：[[误差与数值线代-条件与稳定-condition number]]、[[误差与数值线代-条件与稳定-敏感性]]
- 返回阶段索引：[[🧮 第一阶段：误差与数值线代]]

## 最小自测
- [ ] 我能用自己的话解释“backward stability”
- [ ] 我能说明它在“条件与稳定”里的作用
- [ ] 我能给出一个例子、公式或应用场景

*创建于：2026-04-17*
