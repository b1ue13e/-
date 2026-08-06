---
type: study
course: "离散数学"
topic: "欧几里得算法与扩展欧几里得算法"
title: "欧几里得算法与扩展欧几里得算法"
created: 2026-08-05
status: ongoing
difficulty: intermediate
concept: ["欧几里得算法", "扩展欧几里得算法", "最大公约数", "Bézout恒等式", "模逆元"]
prerequisites: ["整除与同余"]
related: ["费马小定理与欧拉定理", "RSA加密的数学基础"]
tags: [学习, 离散数学, 数论, 欧几里得算法]
flow: knowledge
kind: concept
proof_mode: true
sources:
  - title: "Discrete Mathematics: An Open Introduction (4e)"
    url: "https://discrete.openmathbooks.org/dmoi4.html"
    locator: "Chapter 6.2"
    source_type: open-textbook
    license: "CC BY-NC-SA 4.0"
    verified_at: 2026-08-05
  - title: "MIT 6.042J Mathematics for Computer Science"
    url: "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/"
    locator: "Lecture 4-5, PS3"
    source_type: open-courseware
    license: "CC BY-NC-SA 4.0"
    verified_at: 2026-08-05
stage_moc: "[[02-Knowledge/🧠 学习系统/04-离散数学/03-专题进阶/🧭 阶段3-专题进阶]]"
upstream: ["[[02-Knowledge/🧠 学习系统/04-离散数学/03-专题进阶/整除与同余]]"]
---

# 欧几里得算法与扩展欧几里得算法

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类**
- **判断理由**：欧几里得算法是人类最古老的算法之一（~2300年），能在 $O(\log n)$ 时间内求最大公约数。扩展版本（ExGCD）是 RSA 加密中计算模逆元的核心工具——没有它就没有现代公钥加密。

---

## 1. 这个知识点解决什么问题？

> 如何高效地求两个整数的最大公约数？更进一步：能否找到整数 $s,t$ 使 $sa+tb=\gcd(a,b)$（Bézout 恒等式）？这在计算模逆元（$a^{-1} \bmod n$）时至关重要。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：$\gcd \to$ Bézout恒等式 $\to$ 模逆元 $\to$ RSA解密 $\to$ 互联网安全。
- **应用**：RSA密钥生成、Diophantine方程求解、分数化简、中国剩余定理的实现。

---

## 3. 学它之前需要哪些前置知识？

1. **[[整除与同余]]**：$\gcd$ 的定义和除法定理。

---

## 4. 定义复述

**最大公约数 $\gcd(a,b)$**：整除 $a$ 和 $b$ 的最大正整数。约定 $\gcd(0,n)=|n|$。

**欧几里得算法**：$\gcd(a,b) = \gcd(b, a \bmod b)$，递归直到 $b=0$ 返回 $a$。

**Bézout 恒等式**：存在整数 $s,t$ 使 $sa + tb = \gcd(a,b)$。

**扩展欧几里得算法（ExGCD）**：在计算 $\gcd$ 的同时求出 $s,t$。

**模逆元**：若 $\gcd(a,n)=1$，ExGCD 可求出 $a^{-1} \bmod n$（即 $ax \equiv 1 \pmod{n}$ 的解）。

### 算法伪代码
```
ExGCD(a, b):
  if b == 0: return (a, 1, 0)
  (d, x1, y1) = ExGCD(b, a mod b)
  return (d, y1, x1 - (a//b)*y1)
```

---

## 5. 直觉与图像

- **直觉类比**：欧几里得算法像"用短边量长边，取余数后再用余数量短边，反复直到量尽"——这是几何版本的欧几里得算法。ExGCD 则把每次"量"的过程用方程记录，回溯时构造出 Bézout 系数。
- **一句话直觉本质**：ExGCD = "用余数的线性组合表示出原数的线性组合"。

---

## 6. 定理陈述与证明重建

### $\gcd(a,b) = \gcd(b, a \bmod b)$ 的证明

设 $a = bq + r$（$r = a \bmod b$）。
- 若 $d \mid a$ 且 $d \mid b$，则 $d \mid (a - bq) = r$，故 $d$ 也是 $b$ 和 $r$ 的公因数。
- 若 $d \mid b$ 且 $d \mid r$，则 $d \mid (bq + r) = a$。

两集合的公因数完全相同，故最大公因数相同。

**关键"转念"**：余数 $r = a - bq$ 把 $a$ 和 $b$ 的线性关系变成了公因数的传递通道。

---

## 7. 经典反例库

### 反例：不互素时无模逆元

- $\gcd(6, 10) = 2 \ne 1$。$6x \equiv 1 \pmod{10}$ 无解——左边永远是偶数，模10下不可能等于1。

---

## 8. 条件变式

| 变式 | 结论 |
| :--- | :--- |
| $\gcd(a,n)=1$ | $a$ 在模 $n$ 下有唯一乘法逆元 |
| 多项式版本 | 多项式欧几里得算法（域上的多项式环） |

---

## 9. 相关知识点与 Obsidian 双链建议

- **上游**：[[整除与同余]]
- **下游**：[[中国剩余定理]]、[[RSA加密的数学基础]]

---

## 10. 闭卷验收（数学模式）

- [ ] **定义复述**：写出欧几里得算法和 ExGCD 的伪代码
- [ ] **定理陈述**：陈述 Bézout 恒等式
- [ ] **证明重建**：证明 $\gcd(a,b) = \gcd(b, a \bmod b)$
- [ ] **反例复现**：给出一个无模逆元的例子
- [ ] **条件变式**：计算 $\gcd(252, 105)$ 并求出 Bézout 系数

---

## 11. 分级习题

| 题号 | 难度 | 来源 |
| :--- | :--- | :--- |
| 1 | 基础 | DMOI §6.2 |
| 2 | 基础 | MIT PS3 |
| 3 | 中等 | DMOI §6.2 |
| 4 | 中等 | MIT PS3 |
| 5 | 较难 | MIT PS4 |

### 题目与解析

#### 1. 用欧几里得算法求 $\gcd(252, 105)$
> - $252 = 2 \times 105 + 42$; $105 = 2 \times 42 + 21$; $42 = 2 \times 21 + 0$。$\gcd = 21$。

#### 2. 用 ExGCD 求 $s,t$ 使 $252s + 105t = 21$
> - 回溯：$21 = 105 - 2 \times 42 = 105 - 2 \times (252 - 2 \times 105) = -2 \times 252 + 5 \times 105$。$s=-2, t=5$。

---

## 12. 我的主动回忆区

>

### 下次复习日期
- [ ] 明天 · [ ] 3天后 · [ ] 7天后 · [ ] 14天后

---

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/04-离散数学/03-专题进阶/`
- **关联已有笔记**：`[[整除与同余]]` `[[中国剩余定理]]`
- **建议标签**：`#学习` `#离散数学` `#数论` `#欧几里得算法`
