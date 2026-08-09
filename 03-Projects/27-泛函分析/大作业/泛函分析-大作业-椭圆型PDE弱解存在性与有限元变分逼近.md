---
type: project
project_type: homework
course: "泛函分析"
assignment_id: "泛函分析-CAPSTONE"
assignment_level: capstone
assignment_format: project
stage_id: "04"
requires:
  - "[[泛函分析-弱收敛与Banach-Alaoglu定理]]"
  - "[[泛函分析-Sobolev空间与嵌入定理]]"
  - "[[泛函分析-迹定理与Sobolev边界空间]]"
  - "[[泛函分析-变分方法与椭圆PDE弱解]]"
  - "[[泛函分析-谱理论与紧自伴算子谱定理]]"
  - "[[泛函分析-Fredholm二歧定理]]"
  - "[[泛函分析-Riesz表示定理与Lax-Milgram引理]]"
source_type: local_integration_task
created: 2026-08-09
updated: 2026-08-09
status: active
flow: project
tags: [大作业, 泛函分析, Capstone, 变分法, 谱分解, 积分方程, 椭圆PDE, 有限元, 误差估计, 迹提升, 奇异性, Python仿真]
---

# 泛函分析-大作业-椭圆型PDE弱解存在性与有限元变分逼近

> 对应阶段：[[🧭 阶段3-算子与谱理论]] & [[🧭 阶段4-变分方法与应用]] & 全课程终极验收
> 任务类型：跨阶段综合 Capstone 理论推导与 Python 数值仿真综合大作业

---

## 🎯 学习目标与任务背景

### 1. 学习目标
本大作业是《泛函分析》全课程的终极集大成任务，彻底打通“**算子代数谱论 $\to$ Fredholm 积分可解性 $\to$ Sobolev 空间迹提升 $\to$ 变分直接法 $\to$ 有限元正交投影与角点奇异性**”的全流程理论与数值闭环：
$$\begin{matrix}
\text{【主线 A：谱论与积分方程】} & \text{紧自伴核} \xrightarrow{\text{Hilbert-Schmidt}} \text{谱定理分解} \xrightarrow{\text{Fredholm 二歧}} \text{Nyström 积分方程求解} \\
\text{【主线 B：变分与有限元】} & \text{非齐次边值/角点} \xrightarrow{\text{迹定理边界提升}} \text{Lax-Milgram / 变分直接法} \xrightarrow{\text{Cea 引理}} \text{有限元正交投影与收敛阶}
\end{matrix}$$

### 2. 任务背景与边界
本工程涵盖两个深度模块，既要求给出严密的泛函分析定理推导，又要求运行本地 Python 仿真脚本给出数值证据。

---

## 📋 Capstone 任务全景说明书 (满分 100 分)

### 模块一：紧自伴积分算子谱分解与 Fredholm 积分方程求解 (40 分)

在 Hilbert 空间 $H = L^2[0, 1]$ 上考虑紧自伴积分算子：
$$(T f)(x) = \int_0^1 K(x, y) f(y) dy, \quad \text{其中对称核 } K(x, y) = \min(x, y)$$

1. **谱定理构造推导 (15 分)**：
   - 证明 $T$ 是自伴算子且为紧算子；
   - 证明特征值问题 $T f = \lambda f$ 等价于两点边值微分方程 $-f^{\prime\prime}(x) = \frac{1}{\lambda} f(x)$，边界条件为 $f(0) = 0, f^\prime(1) = 0$；
   - 严格求解全部特征值 $\lambda_n = \frac{1}{(n - 1/2)^2 \pi^2}$ 与标准正交特征函数 $e_n(x) = \sqrt{2}\sin((n - 1/2)\pi x) \ (n \ge 1)$。

2. **Fredholm 积分方程可解性与逆算子 (15 分)**：
   - 考虑第二类 Fredholm 积分方程：$(I - \mu T) u(x) = g(x)$（其中 $g \in L^2[0, 1]$）；
   - 利用 Fredholm 二歧定理与谱定理正交基展开，证明：当 $\mu \ne \lambda_n^{-1} = (n - 1/2)^2 \pi^2$ 时，方程存在唯一强解，其解可显式写为：
     $$u(x) = g(x) + \sum_{n=1}^\infty \frac{\mu \lambda_n}{1 - \mu \lambda_n} \langle g, e_n \rangle e_n(x)$$
   - 分析当 $\mu = \lambda_1^{-1} = \frac{\pi^2}{4}$ 时，解存在的正交相容性条件（$\langle g, e_1 \rangle = 0$）。

3. **Python 谱衰减与 Nyström 积分数值验证 (10 分)**：
   - 运行项目脚本 `scripts/spectral_integral_operator.py`；
   - 记录前 5 个数值特征值与解析特征值的相对误差，数值验证紧自伴算子特征值满足 $\mathcal{O}(1/n^2)$ 严格衰减；
   - 记录非自伴算子 Rayleigh 商失效与数值半径差（Rayleigh Gap）数据。

---

### 模块二：非齐次椭圆边值变分弱解、迹提升与有限元仿真 (60 分)

考虑开区域 $\Omega \subset \mathbb{R}^d$ 上的非齐次椭圆边值问题：
$$\begin{cases} -\Delta u = f(x), & x \in \Omega \\ \gamma(u) = g(x), & x \in \partial \Omega \end{cases}$$

1. **迹算子边界提升 (Lifting) 与齐次化 (15 分)**：
   - 应用 Sobolev 迹定理的右逆提升性质，选取提升函数 $u_g \in H^1(\Omega)$ 使得 $\gamma(u_g) = g$ 且 $\|u_g\|_{H^1(\Omega)} \le C \|g\|_{H^{1/2}(\partial \Omega)}$；
   - 令未知函数分解为 $u = w + u_g$，推导出零迹未知量 $w \in H_0^1(\Omega)$ 满足的等价齐次变分方程：
     $$a(w, v) = \langle f, v \rangle_{L^2} - a(u_g, v), \quad \forall v \in H_0^1(\Omega)$$
   - 给出双线性型 $a(w, v) = \int_\Omega \nabla w \cdot \nabla v dx$ 在 $H_0^1(\Omega)$ 上的连续性与 Poincaré 矫顽性证明。

2. **Lax-Milgram 与变分直接法双重证明 (15 分)**：
   - 分别利用 **Lax-Milgram 定理** 与 **能量泛函变分直接法**（矫顽下有界 $\to$ 弱紧提取 $\to$ 弱下半连续极小），证明弱解 $w \in H_0^1(\Omega)$ 存在且唯一；
   - 给出全解 $u$ 的先验能量稳定估计界：$\|u\|_{H^1(\Omega)} \le C_1 \|f\|_{L^2(\Omega)} + C_2 \|g\|_{H^{1/2}(\partial \Omega)}$。

3. **Galerkin 有限元逼近、Cea 引理与角点奇异性 (15 分)**：
   - 设 $V_h \subset H_0^1(\Omega)$ 为连续分片线性有限元空间，建立离散方程 $a(w_h, v_h) = \langle f, v_h \rangle - a(u_g, v_h) \ (\forall v_h \in V_h)$；
   - 严格证明 **Cea 引理**：$\|w - w_h\|_{H^1} \le \frac{C}{\alpha_0} \inf_{v_h \in V_h} \|w - v_h\|_{H^1}$；
   - 针对 2D L 型非凸区域 $\Omega = (-1, 1)^2 \setminus ([0, 1] \times [-1, 0])$，分析再入角点处的奇异谐波解 $u(r, \theta) = r^{2/3}\sin(2\theta/3)$：说明 $\nabla u \in L^2 \implies u \in H^1$，但 $\nabla^2 u \notin L^2 \implies u \notin H^2$，解释为何此时有限元收敛阶从光滑问题的 $\mathcal{O}(h^1)$ 跌落至 $\mathcal{O}(h^{2/3})$。

4. **Python 有限元求解与收敛阶实测 (15 分)**：
   - 运行项目脚本 `scripts/fem_poisson_solver.py`；
   - 记录 1D 齐次基准问题（$H^1 \approx 1.0, L^2 \approx 2.0$）与非齐次边界提升（Boundary Lifting）的收敛阶；
   - 记录 2D L 型奇异域的有限元收敛率，数值印证 Sobolev 空间对非光滑奇异解的包容性与收敛阶障碍。

---

## 📦 提交产物与交付规范

1. 包含模块一与模块二全部数学证明推导的终极报告（Markdown 或 PDF 格式）。
2. 运行 `python scripts/spectral_integral_operator.py` 的控制台输出与前 5 阶特征值相对误差表。
3. 运行 `python scripts/fem_poisson_solver.py` 的控制台收敛率输出表（含 1D 齐次、1D 非齐次迹提升、2D L型奇异域）。
4. 运行 `pytest tests/test_fem_and_spectral.py` 的 100% 通过测试报告。

---

## 📊 100 分 Capstone Rubric 验收标准

| 模块 | 权重 | 达标考核标准 |
| :--- | :---: | :--- |
| **模块一：谱定理与积分方程** | 40% | 积分核特征值边值转化严谨，Fredholm 逆算子展开式准确，Python 谱衰减与 Rayleigh 差数据无误。 |
| **模块二：迹提升与变分弱解** | 30% | 迹算子右逆边界提升推导无跳步，Lax-Milgram 连续与矫顽常数估计严密，先验界清晰。 |
| **模块三：有限元理论与奇异性** | 15% | Galerkin 误差正交性证明完整，Cea 引理几何意义透彻，L型角点 $r^{2/3}$ 奇异性导致 $H^2$ 崩溃解析准确。 |
| **模块四：Python 仿真与测试** | 15% | 1D/2D FEM 求解器收敛阶实测通过，pytest 8 项自动化单元测试 100% 通过。 |

---

## 🔍 引导自检与检查点

- 💡 **自检 1 (Fredholm 奇异性)**：当参数 $\mu$ 恰好等于某个特征值的倒数 $\lambda_k^{-1}$ 时，算子 $I - \mu T$ 不再可逆，此时方程有解当且仅当右端项 $g$ 正交于特征函数 $e_k$。
- 💡 **自检 2 (Cea 引理与角点奇异性)**：在平滑凸区域上 $u \in H^2$，分片线性有限元可达 $\mathcal{O}(h)$；而在非凸再入角点区域，$u \in H^{1+2/3-\epsilon} \setminus H^2$，Cea 引理下界受最佳逼近误差限制，收敛阶跌落至 $\mathcal{O}(h^{2/3})$，这是 Sobolev 正则性在有限元上的经典印证。
