---
tags: [实变函数, 阶段4, Fourier与应用]
created: 2026-04-12
updated: 2026-08-09
status: ongoing
type: study
kind: moc
course: "实变函数"
stage_id: "04"
flow: knowledge
topic: "第4阶段:Fourier 与应用"
concept: ["Fourier级数", "Fourier变换", "卷积", "逼近"]
upstream: ["[[🧭 阶段3-微分与函数空间]]"]
---

# 🚀 第4阶段:Fourier 与应用

> 阶段目标:用 L2 完备性建立 Fourier 级数与 Fourier 变换理论,理解卷积与逼近,并连接热方程、波动方程与信号处理。**为什么现在学**:Fourier 级数在 L2 中的收敛(Fischer-Riesz 意义)是阶段 3 完备性定理的直接应用,是实变函数"毕业作品"。

## 有序知识卡清单(按学习顺序)

| 顺序 | 知识卡 | 直接前置 | 学完能做什么 |
| :-- | :-- | :-- | :-- |
| 1 | [[实变函数-Fourier级数]] | 阶段3 卡2 | 计算 Fourier 系数;判断收敛类型 |
| 2 | [[实变函数-Fourier级数与L2收敛]] | 阶段3 卡3 | 证明 $\{e^{inx}\}$ 完备;Plancherel 恒等式 |
| 3 | [[实变函数-Fourier变换]] | 卡 2 | 掌握 L1 变换的平移/缩放/卷积性质 |
| 4 | [[实变函数-卷积定理]] | 卡 3 | 证明 $\widehat{f*g}=\hat f\hat g$ 并应用 |
| 5 | [[实变函数-mollifier与正则化]] | 卡 4 | 用磨光子构造光滑逼近;理解稠密性 |
| 6 | [[实变函数-Fourier应用专题]] | 卡 5 | 用 Fourier 方法解热方程/波动;解释滤波与频谱 |

## 学习顺序说明

1-2 是级数(离散):正交系 → 完备性 → L2 收敛;3-5 是变换(连续):基本性质 → 卷积 → 磨光逼近;6 是应用整合。mollifier 是"函数空间的稠密子集"思想的具体工具,也是 Sobolev 空间的伏笔。

## 阶段验收与作业

完成全部 6 张卡后,完成以下作业并通过**终局验收**:

```dataview
LIST
FROM "03-Projects/26-实变函数"
WHERE contains(requires, this.file.link) OR stage_id = "04"
SORT assignment_level ASC, file.name ASC
```

- 作业入口:[[实变函数-阶段作业-02-Lp空间与Fourier|阶段作业-02:Lp 空间与 Fourier]]、[[实变函数-大作业-Cantor型反例作品集|大作业:Cantor 型反例作品集]]
- **闭卷验收清单(终局)**:
  - [ ] 陈述 Riemann-Lebesgue 引理并证明(用阶梯函数逼近或分部积分)
  - [ ] 证明 $\{e^{inx}\}_{n\in\mathbb{Z}}$ 是 $L^2[-\pi,\pi]$ 的完备正交系
  - [ ] 默写 Plancherel 恒等式 $\lVert f\rVert_2^2=\frac{1}{2\pi}\lVert\hat f\rVert_2^2$
  - [ ] 用热核(高斯函数)解一维热方程初值问题
  - [ ] 解释:为什么 mollifier 能把 $L^1$ 函数光滑逼近且保持范数

## 全课程出口

- 完成大作业作品集(3 个反例:处处连续处处不可导、Cantor 函数、零测不可数集)并通过口试(每题 5 分钟:条件哪些不能省?反例长什么样?证明关键转念?)
- 出口衔接:[[🗺️ 泛函分析学习路径|泛函分析]](Hilbert 空间算子)、PDE(弱解与 Sobolev 空间)。

## 复习与复盘

- 阶段 4 的定理(Plancherel、卷积定理、Riemann-Lebesgue)建议进 Anki。
- 课程终局复盘:用大作业作品集回答"实变函数教会了你什么分析直觉"。

*更新:2026-08-09(补阶段验收与作业区块,规范 stage_moc)*
