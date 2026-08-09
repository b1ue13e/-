---
type: project
project_type: homework
course: "偏微分方程"
assignment_id: "PDE-STAGE-02"
assignment_level: stage
assignment_format: project
stage_id: "04"
requires: ["[[偏微分方程-弱导数Sobolev空间与变分形式]]", "[[偏微分方程-Lax-Milgram定理与椭圆弱解存在性]]"]
source_type: official_assignment
created: 2026-08-08
status: completed
flow: project
tags: [阶段作业, 偏微分方程, 弱解, Sobolev空间, Lax-Milgram]
---

# 偏微分方程-阶段作业-02-Sobolev空间变分形式与Lax-Milgram应用

> 所属阶段：[[02-Knowledge/🧠 学习系统/34-偏微分方程/04-现代变分弱解与数值计算/🧭 阶段4-现代变分弱解与数值计算|阶段 4：现代变分弱解与数值计算]]  
> 考查目标：检验 Sobolev 空间 $H^1(\Omega)$、$H_0^1(\Omega)$ 弱导数运算、Poincaré 不等式证明、二阶变系数椭圆型方程弱变分形式推导及基于 Lax-Milgram 定理的存在唯一性证明。

---

## 学习目标
- 掌握在测试函数分布意义下验证弱导数的方法，深刻理解 Sobolev 空间与经典连续函数空间的关系。
- 掌握一维与多维有界区域上 Poincaré 不等式的证明及其最优最佳常数推导。
- 熟练将二阶对流扩散反应偏微分方程转化为 Hilbert 空间上的连续双线性变分形式。
- 掌握应用 Lax-Milgram 定理严格证明椭圆型弱解存在性、唯一性与能量先验估计的完整数学步骤。

---

## 任务背景与边界
本作业涵盖现代偏微分方程弱解与变分理论体系。现代泛函方法将经典的逐点求导转化为无穷维希尔伯特空间上的双线性泛函。作业要求完全摆脱初等试凑，严格运用泛函分析中的 Riesz 空间表示定理、散度定理与等价范数定理完成弱解适定性闭环。

---

## 详细题目清单

### 题目 1（弱导数验证与二维反例：Sobolev 空间不连续函数，30分）
1. **二维对数奇异函数的可积性**：考虑二维开圆盘 $\Omega = B_{1/2}(0) \subset \mathbb{R}^2$。定义对数奇异函数：
   $$u(x) = \ln\left( \ln\left( \frac{1}{|x|} \right) \right)$$
   证明：当 $|x| \to 0$ 时，$u(x) \to +\infty$，因此 $u \notin L^\infty(\Omega)$（函数在原点无界间断）。
2. **弱导数计算与平方可积性**：计算 $u(x)$ 在 $x \neq 0$ 处的经典梯度 $\nabla u(x)$。在极坐标下计算狄利克雷积分：
   $$\int_{B_{1/2}(0)} |\nabla u|^2 dx = \int_0^{2\pi}\int_0^{1/2} |\nabla u(r)|^2 r \, dr d\theta$$
   利用变量代换 $t = \ln(1/r)$ 证明该积分为有限实数，从而严格证明 $u \in H^1(B_{1/2}(0))$。
3. **Sobolev 嵌入反思**：对比一维情况（$H^1(\mathbb{R}) \hookrightarrow C^{0, 1/2}(\mathbb{R})$ 必连续），解释为什么二维空间 $H^1$ 函数允许存在孤立对数奇点。

### 题目 2（一维 Poincaré 不等式常数精准估计与证明，30分）
设 $u \in H_0^1(0, L)$ 为区间 $[0, L]$ 上边界迹为零的 Sobolev 函数。
1. **初等 Cauchy-Schwarz 估计**：从微积分基本定理 $u(x) = \int_0^x u'(s)ds$ 出发，应用 Cauchy-Schwarz 不等式，证明：
   $$|u(x)|^2 \le x \int_0^L |u'(s)|^2 ds$$
   两端对 $x \in (0, L)$ 积分，导出初等界：$\|u\|_{L^2(0, L)} \le \frac{L}{\sqrt{2}} \|u'\|_{L^2(0, L)}$。
2. **正弦特征展开导出最优常数**：将 $u(x)$ 展开为正交正弦基 $u(x) = \sum_{n=1}^\infty c_n \sin\left(\frac{n\pi x}{L}\right)$。计算 $\|u\|_{L^2}^2$ 与 $\|u'\|_{L^2}^2$ 的 Parseval 恒等式，利用最小特征值 $\lambda_1 = (\pi/L)^2$，严格证明最优 Poincaré 不等式：
   $$\|u\|_{L^2(0, L)} \le \frac{L}{\pi} \|u'\|_{L^2(0, L)}$$
   并指出等号成立的极值函数形态。

### 题目 3（变系数非对称对流扩散反应方程弱解适定性证明，40分）
在有界光滑区域 $\Omega \subset \mathbb{R}^n$ 上考虑非对称变系数椭圆边值问题：
$$\begin{cases} -\sum_{i,j=1}^n \frac{\partial}{\partial x_i}\left( A_{ij}(x)\frac{\partial u}{\partial x_j} \right) + \mathbf{b}(x) \cdot \nabla u + c(x)u = f(x), & x \in \Omega \\ u(x) = 0, & x \in \partial \Omega \end{cases}$$
假设系数满足：
- **一致椭圆性**：$\exists \theta > 0, \sum_{i,j=1}^n A_{ij}(x)\xi_i \xi_j \ge \theta |\xi|^2, \forall \xi \in \mathbb{R}^n, \text{a.e. } x \in \Omega$。
- **有界性**：$A_{ij}, \mathbf{b}, c \in L^\infty(\Omega)$ 且 $\|A_{ij}\|_{L^\infty} \le K, \|\mathbf{b}\|_{L^\infty} \le K_b, \|c\|_{L^\infty} \le K_c$。
- **无散与反应条件**：$\nabla \cdot \mathbf{b}(x) = 0$ 且 $c(x) \ge 0$ a.e. in $\Omega$。
1. **推导弱变分形式**：取测试函数 $v \in H_0^1(\Omega)$，严格推导双线性形式 $a(u, v)$ 与载荷泛函 $\ell(v)$。
2. **证明连续性 (Continuity)**：证明存在常数 $M > 0$ 使得 $|a(u, v)| \le M \|u\|_{H_0^1} \|v\|_{H_0^1}$。
3. **证明斜对称性与强制性 (Coercivity)**：利用 Gauss 散度定理证明对流项 $\int_\Omega (\mathbf{b} \cdot \nabla u) u dx = \frac{1}{2}\int_\Omega \mathbf{b} \cdot \nabla(u^2) dx = 0$。结合一致椭圆性与 Poincaré 不等式，证明存在 $\alpha > 0$ 使得：
   $$a(u, u) \ge \alpha \|u\|_{H_0^1}^2$$
4. **Lax-Milgram 定理应用**：完整阐述 Lax-Milgram 定理，给出弱解存在唯一性与连续先验估计 $\|u\|_{H_0^1} \le \frac{1}{\alpha} \|f\|_{H^{-1}}$。

---

## 提交要求
- 提交完整独立手写证明或排版 Markdown 报告。
- 包含极坐标奇异积分换元、Parseval 恒等式推演以及双线性形式有界性与强制性不等式放缩全过程。

---

## 验收标准
- 满分 100 分制，题 1 占 30 分，题 2 占 30 分，题 3 占 40 分。
- **题目 1 (30分)**：对数奇点积分换元有限性证明严密 (15分)，Sobolev 嵌入反思透彻 (15分)。
- **题目 2 (30分)**：初等 Cauchy-Schwarz 证明 (15分)，正交基展开最优常数 $L/\pi$ 证明完整 (15分)。
- **题目 3 (40分)**：双线性变分形式推导正确 (10分)，有界性验证 (10分)，对流项积分为零与强制性证明完整 (10分)，Lax-Milgram 存在唯一性与先验估计闭环 (10分)。

---

## 引导与自检清单
- [ ] 检查题 1 极坐标求导时是否考虑了复合求导 $\frac{d}{dr}\ln(\ln(1/r)) = \frac{1}{\ln(1/r)}\frac{1}{1/r}(-1/r^2) = -\frac{1}{r\ln(1/r)}$。
- [ ] 检查题 2 当 $u(x) = \sin(\pi x/L)$ 时两端是否严格取得等号。
- [ ] 检查题 3 在对流项分部积分时外法向边界积分项是否利用 $u \in H_0^1$ 严格为零。
