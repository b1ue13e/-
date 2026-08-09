---
type: project
project_type: homework
course: "泛函分析"
assignment_id: "泛函分析-STAGE02"
assignment_level: stage
assignment_format: project
stage_id: "03"
requires:
  - "[[泛函分析-紧算子与有限维逼近]]"
  - "[[泛函分析-自伴算子与正算子]]"
  - "[[泛函分析-谱理论与紧自伴算子谱定理]]"
  - "[[泛函分析-Fredholm二歧定理]]"
source_type: local_integration_task
created: 2026-08-09
status: active
flow: project
tags: [作业, 泛函分析, 阶段作业, 谱理论, 积分方程, 算子代数]
---

# 泛函分析-阶段作业-02-紧算子谱分解与Fredholm积分方程

> 对应阶段：[[🧭 阶段3-算子与谱理论|第三阶段：算子与谱理论]]
> 考核形式：理论推演与积分方程解析求解报告

---

## 🎯 学习目标与任务背景

### 1. 学习目标
本阶段作业全面考核第 3 阶段关于**紧算子、自伴算子、谱分解与 Fredholm 理论**的综合应用能力。学习者需独立完成微分算子逆 Green 函数的紧自伴性证明、特征系谱展开以及奇异/共振积分方程的解结构判定。

### 2. 任务背景与边界
涵盖 Sturm-Liouville 边值问题 Green 函数求解、Fredholm 积分方程共振态分析以及连续函数演算等子任务。要求将 Green 函数分段解析表达式与算子谱分解特征系完整推导。

---

## 📝 阶段综合任务 (满分 100 分)

### 任务 1：Sturm-Liouville 边值问题与 Green 紧积分算子 (35 分)
考虑弦振动微分方程边值问题：
$$\begin{cases} -u^{\prime\prime}(t) = f(t), & t \in (0, \pi) \\ u(0) = 0, \quad u(\pi) = 0 \end{cases}$$
1. 求解该边值问题的 **Green 函数** $G(t, s)$，写出显式分段函数表达式：
   $$G(t, s) = \begin{cases} \frac{s(\pi - t)}{\pi}, & 0 \le s \le t \le \pi \\ \frac{t(\pi - s)}{\pi}, & 0 \le t \le s \le \pi \end{cases}$$
   并将解表示为积分算子 $u(t) = (K f)(t) = \int_0^\pi G(t, s) f(s) ds$。(10 分)
2. 证明积分算子 $K: L^2[0, \pi] \to L^2[0, \pi]$ 是**紧算子**且是**严格自伴正算子**（$K = K^* > 0$）。(10 分)
3. 利用紧自伴谱定理求出算子 $K$ 的全部特征值 $\lambda_n$ 与标准正交特征函数系 $e_n(t)$。(10 分)
4. 将任意 $f \in L^2[0, \pi]$ 按特征基正交展开，写出微分方程弱解的 **Fourier 正弦级数解析解** $u(t) = \sum_{n=1}^\infty c_n \sin(nt)$。(5 分)

---

### 任务 2：Fredholm 积分方程共振态分析 (35 分)
在 $L^2[0, 2\pi]$ 上考虑 Fredholm 积分方程：
$$u(t) - \lambda \int_0^{2\pi} \cos(t - s) u(s) ds = f(t)$$
1. 计算紧自伴算子 $(Ku)(t) = \int_0^{2\pi} \cos(t-s) u(s) ds$ 的非零特征值及其特征子空间维数。(15 分)
2. 当 $\lambda$ 取特征值时（发生共振），运用 **Fredholm 二歧定理** 给出非齐次方程有解的右端项 $f(t)$ 正交相容性充要条件。(10 分)
3. 设 $f(t) = \sin(2t)$，判断共振时方程是否可解并给出通解表达式。(10 分)

---

### 任务 3：C* 代数初阶：连续函数函数演算 (Functional Calculus) (20 分)
设 $H$ 为复 Hilbert 空间，$T \in \mathcal{K}(H)$ 为紧自伴算子，谱分解为 $Tx = \sum_{n=1}^\infty \lambda_n \langle x, e_n \rangle e_n$。
设 $\varphi \in C(\sigma(T))$ 为定义在谱集上的连续复函数。
1. 定义算子 $\varphi(T)x = \sum_{n=1}^\infty \varphi(\lambda_n) \langle x, e_n \rangle e_n$。证明 $\varphi(T) \in \mathcal{B}(H)$ 且算子范数满足保距性质：
   $$\|\varphi(T)\|_{\mathcal{B}(H)} = \max_{\lambda \in \sigma(T)} |\varphi(\lambda)|$$ (10 分)
2. 证明映射 $\varphi \mapsto \varphi(T)$ 保持代数结构（加法、数乘、乘法与伴随共轭：$(\bar{\varphi})(T) = (\varphi(T))^*$）。(10 分)

---

### 任务 4：【数值实验】Volterra 拟幂零性与 Mazur 弱收敛强凸极限实测 (20 分)
运行 `scripts/spectral_integral_operator.py` 中的对应模块或编写 Python 验证脚本：
1. **Volterra 积分算子幂次阶乘衰减**：
   - 验证 $(Vf)(t) = \int_0^t f(s)ds$ 在离散网格上的幂算子范数 $\|V^k\| \le \frac{1}{k!}$；
   - 计算 $k=1, 2, 3, 4, 5$ 时的数值谱半径逼近值，验证 $r(V) = \lim \|V^k\|^{1/k} = 0$（谱集仅含单点 $\{0\}$）。(10 分)
2. **Mazur 凸组合强极限数值实证**：
   - 取弱收敛序列 $f_n(x) = \sqrt{2}\sin(n\pi x)$，数值计算 Mazur 算术平均 $s_N(x) = \frac{1}{N} \sum_{n=1}^N f_n(x)$ 的 $L^2$ 范数；
   - 验证 $\|s_N\|_{L^2} = \frac{1}{\sqrt{N}} \to 0$ 的强收敛速率，直观观察高频震荡在凸组合均值下的相互抵消。(10 分)

---

## 📦 提交产物与交付规范

1. 包含 Green 函数推导、共振态相容性分析与函数演算证明的完整 Markdown 报告。
2. 包含 Volterra 算子幂次衰减与 Mazur 凸组合强极限数值实验输出的日志与收敛率图表数据。
3. 运行并通过单元测试：`pytest 03-Projects/27-泛函分析/tests/test_fem_and_spectral.py -k "volterra or mazur"`。

---

## 📊 100 分 Rubric 验收标准

| 考核维度 | 分值 | 合格标准 (75分通过) |
| :--- | :---: | :--- |
| **Green 算子推导与紧正性** | 30 | Green 函数推导严谨，分部积分验证自伴性与正定性无瑕疵。 |
| **共振态与 Fredholm 条件** | 30 | 特征值 $\lambda = 1/\pi$ 计算准确，正交补相容条件验证完整。 |
| **连续函数演算证明** | 20 | 算子范数等距同构推导严密，代数同态验证无跳步。 |
| **Volterra与Mazur数值实证** | 20 | 准确测得 $\|V^k\| \le 1/k!$ 与 Mazur 均值 $O(1/\sqrt{N})$ 强收敛数据，测试通过。 |

---

## 🔍 引导自检与检查点

- 💡 **自检 1**：在任务 1 中，特征值求解可由常微分方程 $-e_n^{\prime\prime}(t) = \frac{1}{\lambda_n} e_n(t), e_n(0)=e_n(\pi)=0$ 得到 $e_n(t) = \sqrt{\frac{2}{\pi}}\sin(nt)$，特征值 $\lambda_n = 1/n^2$。
- 💡 **自检 2**：在任务 2 中，$\cos(t-s) = \cos(t)\cos(s) + \sin(t)\sin(s)$，非零特征值为 $\pi$，重数为 2。当 $\lambda = 1/\pi$ 时，右端项 $\sin(2t)$ 与 $\sin(t), \cos(t)$ 正交，故方程必有解！
- 💡 **自检 3**：在任务 4 中，因为正交基满足 $\langle f_n, f_m \rangle = \delta_{nm}$，展开得 $\|s_N\|_{L^2}^2 = \frac{1}{N^2} \sum_{n=1}^N \|f_n\|^2 = \frac{N}{N^2} = \frac{1}{N}$，故 $\|s_N\| = 1/\sqrt{N} \to 0$ 强收敛。

