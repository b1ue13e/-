---

type: study

flow: knowledge

kind: concept

topic: "支持向量机SVM"

course: "机器学习"

module: "模块1：支持向量机与核方法"

created: 2026-04-18

status: ongoing

difficulty: advanced

concept: ["支持向量机SVM"]

prerequisites: []

related: ["软间隔SVM", "核方法"]

source_textbook: ["机器学习（周志华）", "Hands-on Machine Learning"]

source_sections: ["第6章", "SVM"]

learning_objectives: ["说明 支持向量机SVM 在“模块1：支持向量机与核方法”里解决的具体问题", "把 支持向量机SVM 对应回 第6章", "用一个最小例子或代表题解释 支持向量机SVM 的作用"]

deliverables: ["一句话定义或项目目标", "一个最小例子/代表题/最小实验", "一条易错点或跨路径连接", "能解释间隔、核函数和软间隔之间的关系。"]

tags: ["机器学习", "学习"]

aliases: ["SVM支持向量机"]

stage_moc: "[[🧭 阶段5-其他方法]]"

upstream: ["[[机器学习-感知机]]"]

source: "周志华《机器学习》第6–10、13–16章"
source_url: "https://book.douban.com/subject/26708119/"
accessed: 2026-08-07
license: "[待验证]"

---



---type: study

flow: knowledge

kind: concept

topic: "支持向量机SVM"

course: "机器学习"

stage: "🧭 阶段5-其他方法"

module: "模块1：支持向量机与核方法"

created: 2026-04-18

status: ongoing

difficulty: advanced

concept: ["支持向量机SVM"]

prerequisites: []

related: ["软间隔SVM", "核方法"]

source_textbook: ["机器学习（周志华）", "Hands-on Machine Learning"]

source_sections: ["第6章", "SVM"]

learning_objectives: ["说明 支持向量机SVM 在“模块1：支持向量机与核方法”里解决的具体问题", "把 支持向量机SVM 对应回 第6章", "用一个最小例子或代表题解释 支持向量机SVM 的作用"]

deliverables: ["一句话定义或项目目标", "一个最小例子/代表题/最小实验", "一条易错点或跨路径连接", "能解释间隔、核函数和软间隔之间的关系。"]

tags: ["机器学习", "学习"]

aliases: ["SVM支持向量机"]

stage_moc: "[[🧭 阶段5-其他方法]]"

---

# 支持向量机SVM



> 所属路径：[[🗺️ 机器学习学习路径|机器学习学习路径]]

> 所属阶段：[[🧭 阶段5-其他方法|返回阶段页]]

> 所属模块：`模块1：支持向量机与核方法`



## 为什么学

- 这张卡位于“模块1：支持向量机与核方法”，用来解决：为什么最大间隔和核技巧能把线性方法扩展到更复杂的边界？

- 它是你从 无 走向 [[机器学习-软间隔SVM]]、[[机器学习-核方法]] 的桥梁。



## 教材定位

- 主教材：`机器学习（周志华）`、`Hands-on Machine Learning`

- 对应章节：第6章；SVM

- 阶段入口：[[🧭 阶段5-其他方法|🧭 阶段5-其他方法]]



## 必须掌握

- 用自己的话定义 `支持向量机SVM`，并说清它的边界。

- 解释 `支持向量机SVM` 为什么是“为什么最大间隔和核技巧能把线性方法扩展到更复杂的边界？”这条问题链的一部分。

- 说明它和同阶段相邻概念的区别与联系。



## 关键问题

- 支持向量机SVM 在“模块1：支持向量机与核方法”这条主线里具体负责哪一步？

- 如果忽略 支持向量机SVM，为什么最大间隔和核技巧能把线性方法扩展到更复杂的边界？ 会在哪一步断掉？

- 支持向量机SVM 和相邻概念的边界是什么？



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

- [ ] 能解释间隔、核函数和软间隔之间的关系。

- [ ] 能独立解释这张卡在本阶段中的位置。

- [ ] 能把教材章节和这张卡一一对应。



## 前后连接

- 前置：无

- 相关：[[机器学习-软间隔SVM]]、[[机器学习-核方法]]

- 返回阶段页：[[🧭 阶段5-其他方法|🧭 阶段5-其他方法]]



*创建于：2026-04-18*



---



## 学完后可以完成



> 下面由作业 `requires` 自动反查：学完本卡后可完成的课后作业、阶段作业与大作业（单一事实源，不手动维护）。



```dataview

LIST

FROM "03-Projects"

WHERE type = "project" AND contains(map(requires, (r) => r.path), this.file.name)

SORT assignment_level ASC, file.name ASC

```

