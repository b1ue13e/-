---
type: study
topic: "核密度估计KDE与带宽选择"
course: "非参数统计"
created: 2026-08-08
status: active
stage_moc: "[[🧭 阶段3-平滑与估计]]"
flow: knowledge
kind: concept
importance: "A"
tags: [学习, 非参数统计, 知识卡]
proof_mode: true
---

# 非参数统计-核密度估计KDE与带宽选择

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（连续密度估计第一核心）**
- **判断理由**：直方图依赖原点与 bin 宽度的选择且处处不连续。核密度估计 (Kernel Density Estimation, KDE / Parzen 窗) 将每个数据点平滑化为对称核函数，是非参数概率建模最基础的工具。其收敛速度 $O(n^{-4/5})$ 展现了非参数估计慢于参数估计（维度诅咒前兆）的根本数学特征。
- **验收模式说明**：KDE 点态偏差与方差泰勒展开推导、MISE 最优带宽闭式解推导、Silverman 经验法则计算。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 给定无标签的样本点，如何绘制出连续光滑、积分为 1 的未知概率密度曲线 $f(x)$？直方图不仅锯齿严重，而且无法求导。
> **核心痛点**：窗宽 $h$ 取太大曲线过度平滑（高偏差，掩盖双峰）；$h$ 取太小曲线布满毛刺（高方差，过拟合）。如何数学上寻找最优平衡点？

---

## 2. 它为什么重要？它有什么用？

- **连接大图景**：它是非参数贝叶斯分类器、Mean-Shift 聚类算法、高维流形密度估计的理论根基。
- **实际应用场景**：金融多峰收益率拟合、生物流式细胞仪荧光密度分布恢复、异常检测中的低密度判别。
- **高频考点**：最优带宽 $h^* = O(n^{-1/5})$ 的渐近阶数与积分均方误差 (MISE) 极小化证明。

---

## 3. 学它之前需要哪些前置知识？

1. **[[非参数统计-经验分布函数与DKW不等式]]**：EDF 导数的平滑化。
2. **泰勒展开与二阶矩积分**：$\int u K(u) du = 0, \int u^2 K(u) du = \mu_2(K) < \infty$。

---

## 4. 定义复述

### 1. 核密度估计量 (KDE) 精确定义

设 $X_1, \dots, X_n \stackrel{i.i.d.}{\sim} f(x)$，定义估计量为：
$$\hat{f}_h(x) = \frac{1}{n h} \sum_{i=1}^n K\left(\frac{x - X_i}{h}\right)$$
其中 $K(u)$ 为满足对称、非负且积分为 1 的**核函数 (Kernel Function)**，满足：
$$\int_{-\infty}^\infty K(u) du = 1, \quad \int_{-\infty}^\infty u K(u) du = 0, \quad \mu_2(K) = \int_{-\infty}^\infty u^2 K(u) du > 0$$
$h > 0$ 称为**带宽 (Bandwidth / 窗宽)**。

---

## 5. 定理陈述与偏差-方差推导

### 1. 点态偏差与方差渐近定理

当 $h \to 0$ 且 $n h \to \infty$ 时：
1. **偏差 (Bias)**：
   $$\text{Bias}(\hat{f}_h(x)) = E[\hat{f}_h(x)] - f(x) = \frac{h^2}{2} \mu_2(K) f''(x) + o(h^2)$$
2. **方差 (Variance)**：
   $$\text{Var}(\hat{f}_h(x)) = \frac{R(K)}{n h} f(x) + o\left(\frac{1}{nh}\right), \quad \text{其中 } R(K) = \int_{-\infty}^\infty K(u)^2 du$$

### 2. 证明主线（骨架）

- **第 1 步：期望表达式换元**：
  $$E[\hat{f}_h(x)] = \frac{1}{h} E\left[K\left(\frac{x - X}{h}\right)\right] = \frac{1}{h} \int K\left(\frac{x - t}{h}\right) f(t) dt$$
  令 $u = \frac{x - t}{h} \implies t = x - h u, dt = -h du$：
  $$E[\hat{f}_h(x)] = \int K(u) f(x - hu) du$$
- **第 2 步：对 $f(x - hu)$ 进行二阶泰勒展开**：
  $$f(x - hu) = f(x) - hu f'(x) + \frac{h^2 u^2}{2} f''(x) + o(h^2)$$
- **第 3 步：逐项积分**：
  $$E[\hat{f}_h(x)] = f(x) \int K(u)du - h f'(x) \int u K(u)du + \frac{h^2}{2} f''(x) \int u^2 K(u)du + o(h^2)$$
  利用 $\int K(u)du=1, \int u K(u)du=0$，即得 $\text{Bias} = \frac{h^2}{2} \mu_2(K) f''(x) + o(h^2)$。
- **第 4 步：方差积分**（同理展开二阶矩 $E[\hat{f}_h(x)^2]$）导出 $\text{Var} \approx \frac{R(K) f(x)}{nh}$。

---

## 6. 最优带宽与 Silverman 经验法则

### 1. 积分均方误差 (MISE)

$$\text{MISE}(h) = \int \text{MSE}(\hat{f}_h(x)) dx = \int [\text{Bias}^2 + \text{Var}] dx \approx \frac{h^4}{4} \mu_2(K)^2 R(f'') + \frac{R(K)}{nh}$$
其中 $R(f'') = \int (f''(x))^2 dx$ 衡量真实密度的弯曲剧烈程度。

### 2. 极小化求导得最优窗宽

对 $h$ 求导令导数为 0：
$$h^* = \left( \frac{R(K)}{\mu_2(K)^2 R(f'') n} \right)^{1/5} = O(n^{-1/5})$$
将 $h^*$ 代入得最优收敛速度 $\text{MISE} = O(n^{-4/5})$。

### 3. Silverman 正态参考法则 (Rule of Thumb)

当使用高斯核 $K(u) = \frac{1}{\sqrt{2\pi}}e^{-u^2/2}$，且真实密度设为 $N(\mu, \sigma^2)$ 时，代入计算得：
$$\hat{h}_{\text{Silverman}} = 0.9 \cdot \min\left( \hat{\sigma}, \frac{\text{IQR}}{1.34} \right) \cdot n^{-1/5}$$

---

## 7. 经典反例与误区

### 误区 1：在有界支撑域 $[0, 1]$ 边缘直接使用标准高斯核
- **问题**：在边界 $x=0$ 处，核函数有一半溢出到无数据的负数区域。
- **后果**：导致 $\hat{f}_h(0) \to \frac{1}{2} f(0)$，产生严重的**边界偏差 (Boundary Bias)**（误差阶数退化为 $O(h)$ 而非 $O(h^2)$）。必须使用反射边界法或局部线性估计修正。

---

## 8. 闭卷验收（数学模式）

- [ ] **偏差推导**：独立写出换元 $t = x - hu$ 与泰勒展开证明 $\text{Bias} \approx \frac{h^2}{2}\mu_2(K)f''(x)$ 的全过程。
- [ ] **窗宽极值**：对 $\text{MISE}(h) = A h^4 + B / (nh)$ 求导解出 $h^* \propto n^{-1/5}$。
- [ ] **公式应用**：写出包含 IQR 的 Silverman 稳健带宽经验公式。

---

## 9. 分级习题

| 题号 | 类型 | 难度 | 来源 | 考查点 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 积分推导 | 基础 | Wasserman Ch.6 Ex.2 | 标准高斯核的 $R(K) = \frac{1}{2\sqrt{\pi}}$ 与 $\mu_2(K) = 1$ 计算 |
| 2 | 带宽分析 | 中等 | IMS Ch.16 Lab | 模拟观察 $h=0.01, h=h^*, h=1.0$ 下的过拟合与欠拟合图形 |

---

## 10. 给 Obsidian 的归档建议
- **归档目录**：`02-Knowledge/🧠 学习系统/32-非参数统计/03-平滑与估计/`
- **标签**：`#学习 #非参数统计 #KDE #核密度估计 #MISE`


---

## 🎯 学完后可以完成

```dataview
LIST
FROM "03-Projects/32-非参数统计"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
