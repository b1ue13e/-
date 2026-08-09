---
type: study
topic: "哈密顿蒙特卡洛与无掉头采样NUTS"
course: "贝叶斯统计"
created: 2026-08-08
status: active
stage_moc: "[[🧭 阶段2-计算贝叶斯]]"
flow: knowledge
kind: concept
upstream: ["[[贝叶斯统计-马尔可夫链蒙特卡洛与Metropolis-Hastings算法]]"]
tags: [学习, 贝叶斯统计, HMC, NUTS, 哈密顿力学, 梯度采样]
---

# 贝叶斯统计-哈密顿蒙特卡洛与无掉头采样NUTS

> 所属阶段：[[🧭 阶段2-计算贝叶斯|阶段2：计算贝叶斯]]

---

## 1. 为什么随机游走 M-H 在高维必定失效？

在 $D \ge 50$ 的高维后验分布中，后验概率质量集中在一条狭窄的**典型集 (Typical Set)** 上。
- 随机游走 M-H 是“盲人摸象”式的各向同性探索，绝大多数随机提议都会立刻坠入概率密度极低的空旷区域而被直接拒绝；
- **哈密顿蒙特卡洛 (Hamiltonian Monte Carlo, HMC)** 引入了物理学经典力学的能量守恒机制，利用**后验密度的梯度向量场 $\nabla_\theta \log P(\theta \mid y)$** 引导粒子无摩擦滑行，使得粒子能够在典型集上沿着等能轨道高速滑行，在大跨步位移的同时保持接近 100% 的理论接受率！

---

## 2. 物理相空间与哈密顿动力学方程

### (1) 相空间 (Phase Space) 拓展
引入辅助变量——**动量向量 (Momentum)** $p \sim \mathcal{N}(0, M)$（$M$ 为质量矩阵），将目标参数 $\theta$ 视为质点的**位置 (Position)** $q = \theta$。
定义系统的总能量——**哈密顿量 (Hamiltonian)** $H(q, p)$：
$$H(q, p) \triangleq U(q) + K(p)$$
- **势能 (Potential Energy)**：$U(q) \triangleq -\log P(q, y)$（负对数后验，势能越低概率越高）；
- **动能 (Kinetic Energy)**：$K(p) \triangleq \frac{1}{2} p^T M^{-1} p$。

### (2) 哈密顿正则方程 (Canonical Equations)
系统的连续时间演化由一阶偏微分方程组控制：
$$\frac{dq}{dt} = +\frac{\partial H}{\partial p} = M^{-1} p \quad (\text{动量决定速度})$$
$$\frac{dp}{dt} = -\frac{\partial H}{\partial q} = -\nabla U(q) = \nabla_q \log P(q, y) \quad (\text{后验对数梯度充当恢复力})$$

**核心性质**：
1. **能量守恒**：$\frac{dH}{dt} = \frac{\partial H}{\partial q} \frac{dq}{dt} + \frac{\partial H}{\partial p} \frac{dp}{dt} = -\frac{dp}{dt} \frac{dq}{dt} + \frac{dq}{dt} \frac{dp}{dt} \equiv 0$；
2. **辛几何与相体积保持 (Liouville's Theorem)**：相空间微元体积在演化过程中严格守恒，雅可比行列式 $\lvert \det J \rvert \equiv 1$。

---

## 3. 辛积分器：Leapfrog 蛙跳算法

由于计算机只能离散模拟连续动力学，普通欧拉积分会破坏体积守恒导致轨道发散。HMC 必须采用**辛积分器 (Symplectic Integrator)**——Leapfrog 算法：

给定步长 $\epsilon$，每一步演化分解为三个精巧的半步操作：
1. **动量前半步更新**：
   $$p\left(t + \frac{\epsilon}{2}\right) = p(t) - \frac{\epsilon}{2} \nabla U(q(t))$$
2. **位置完整整步更新**：
   $$q(t + \epsilon) = q(t) + \epsilon M^{-1} p\left(t + \frac{\epsilon}{2}\right)$$
3. **动量后半步更新**：
   $$p(t + \epsilon) = p\left(t + \frac{\epsilon}{2}\right) - \frac{\epsilon}{2} \nabla U(q(t + \epsilon))$$

经过 $L$ 步 Leapfrog 积分后得到提议状态 $(q^*, p^*)$，进行 Metropolis 修正（修正离散积分数值误差）：
$$\alpha = \min\left( 1, \exp\left( -H(q^*, p^*) + H(q, p) \right) \right)$$

---

## 4. 无掉头采样器 (NUTS) 的递归树判据

标准 HMC 需要人工微调步长 $\epsilon$ 与步数 $L$。若 $L$ 设得过大，粒子会在高维流形上绕圈并折返原点（无效计算）。

Hoffman & Gelman (2011) 提出的 **No-U-Turn Sampler (NUTS)** 采用倍增递归二叉树 (Recursive Binary Tree)，沿正反两个时间方向模拟轨迹：
- **U-Turn 停机判据**：当最左端点 $q^-$ 与最右端点 $q^+$ 之间的欧几里得距离开始缩短时，立即终止轨迹延伸：
  $$\frac{d}{dt} \|q^+ - q^-\|^2 < 0 \iff (q^+ - q^-) \cdot p^+ < 0 \quad \text{或} \quad (q^+ - q^-) \cdot p^- < 0$$
- 彻底消除了超参数 $L$ 的人工调试，实现了现代概率编程框架（如 PyMC 5.x、Stan）的核心自动化引擎。

---

## 5. 核心诊断：Divergent Transitions (分歧/散度警告)

当后验几何存在极高曲率区域（如 Neal's Funnel 漏斗颈部）时，Leapfrog 积分步长 $\epsilon$ 无法捕捉剧烈变化的梯度，数值误差瞬间爆炸（$\Delta H = H(q^*, p^*) - H(q, p) > 1000$）。
- **现象**：PyMC 输出红色的 `There were XX divergences after tuning`；
- **含义**：MCMC 链在该区域发生了数值飞逸，导致漏斗尖端的概率质量被系统性漏采，后验推断存在致命偏差；
- **解决策略**：
  1. 提高 `target_accept`（如从 0.8 升到 0.99，强制自适应缩减 $\epsilon$）；
  2. **非中心化参数化 (Non-centered parameterization)**：对模型结构进行重构，将曲率解耦为标准正态分布。

---

## 6. 主动回忆与闭卷自测

- [ ] 默写 Leapfrog 辛积分器的三步代数更新方程；
- [ ] 解释为什么普通 HMC 的雅可比行列式等于 1（Liouville 定理）；
- [ ] 解释 NUTS 算法中“无掉头”判据的点积几何含义与 Divergence 的物理成因。

> [!tip]- 闭卷自测参考答案与思维误区
> 1. **Leapfrog 三步代数**：
>    $p(t + \epsilon/2) = p(t) - \frac{\epsilon}{2} \nabla U(q(t))$；
>    $q(t + \epsilon) = q(t) + \epsilon M^{-1} p(t + \epsilon/2)$；
>    $p(t + \epsilon) = p(t + \epsilon/2) - \frac{\epsilon}{2} \nabla U(q(t + \epsilon))$。
> 2. **Liouville 定理与雅可比**：相空间连续动力学向量场是无散度的（$\nabla_{(q, p)} \cdot (\dot{q}, \dot{p}) = \frac{\partial^2 H}{\partial q \partial p} - \frac{\partial^2 H}{\partial p \partial q} \equiv 0$），保证了体积微元严格守恒。在离散化后，Leapfrog 的每一步剪切变换行列式均为 1，因此提议分布的雅可比因子恒为 1，Metropolis 修正项中无须计算高维体积修正。
> 3. **NUTS 判据与 Divergence 物理**：
>    - **无掉头几何**：$(q^+ - q^-) \cdot p < 0$ 表示轨迹端点间的位移向量与端点动量点积为负，粒子开始向中心折返，此时终止二叉树延伸以节省计算；
>    - **Divergence 成因**：在 Neal 漏斗等高曲率区域，势能梯度 $\nabla U$ 在极短距离内发生跳变，离散 Leapfrog 积分无法拟合真实动力学，能量守恒被破坏导致数值飞逸（$\Delta H \gg 0$）。

---

## 7. 学完后可以完成

> 📌 **实战与作业通道**：NUTS 采样与散度诊断直接对接以下实践任务：
> - 阶段实战：[[贝叶斯统计-阶段作业-01-PyMC层次模型与Eight-Schools收缩效应分析|阶段作业 01：PyMC 层次模型与 Eight-Schools 收缩效应分析]]

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT file.name ASC
```

- [x] 下一步：学习采样质量诊断指标 [[02-计算贝叶斯/贝叶斯统计-MCMC收敛诊断与采样质量评估|MCMC 收敛诊断与采样质量评估]]。

