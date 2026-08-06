---
type: study
topic: "Python 与 NumPy 图像编程基础（CV 前置）"
course: "05-计算机视觉"
created: 2026-08-06
status: completed
difficulty: beginner
concept: ["NumPy 数组", "向量化", "图像张量", "广播", "dtype"]
prerequisites: ["Python 基础语法（循环、函数、列表）"]
related: ["图像表示", "kNN与线性分类器", "数据增强与正则化"]
flow: knowledge
stage_moc: "[[02-Knowledge/🧠 学习系统/05-计算机视觉/00-前置知识/🧭 阶段0-前置知识]]"
kind: concept
source: "NumPy 官方文档（numpy.org/doc/stable/user/absolute_beginners.html）；D2L Ch.2 预备知识"
source_url: "https://numpy.org/doc/stable/user/absolute_beginners.html"
accessed: 2026-08-06
license: "NumPy 文档 BSD-3-Clause；本地仅保存最小原创教学说明"
tags: [学习, 计算机视觉, 前置知识, Python, NumPy]
---

# 计算机视觉｜Python 与 NumPy 图像编程基础

## 0. 先判断它值不值得深挖

这是**前置知识**，不是计算机视觉本身。本卡只讲"把图像当成数字数组来操作"这一件事——它是 HW01-03（kNN、Softmax、两层网络、CNN）所有代码作业的地基。你已经会用 NumPy 切片、广播和向量化的话，直接做卡末的「通过标准」自检，通过即可跳过。

## 1. 这个知识点解决什么问题？

计算机视觉里一切算法最终都在操作**数字数组**：一张图片就是一堆整数/浮点数，一次卷积就是数组乘加，一个 batch 就是多张图叠成的更高维数组。不会 NumPy，就既读不懂课程代码，也无法把公式变成能跑的实验。

## 2. 为什么它重要？它有什么用？

- 课程作业 `real_assignment_packages/hw01_cifar10_knn_softmax` 的 Starter 用 NumPy 实现 kNN 与 Softmax 分类器，禁止用现成库；
- 训练时的数据管线（`DataLoader` 式加载、归一化、增广）本质是 NumPy/PyTorch 张量操作；
- 理解 `(H, W, C)` vs `(C, H, W)` 与 dtype 溢出，能避免 90% 的初学 bug。

## 3. 学它之前需要哪些前置知识？

- Python 基础语法：变量、`for`、`if`、函数、列表推导式（本卡不重复教 Python 语法）；
- 高中数学：坐标系、矩阵乘法概念（可顺带复习 [[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/线性代数基础CV|线性代数基础CV]]）。

## 4. 用直觉语言解释它

把图像想象成一张方格纸：每个格子是一个像素，格子里存三个数（R、G、B）。NumPy 就是把这张方格纸变成可以**整张一起算**的数组——你不需要一个个格子去算，告诉它"整张加 50"，所有格子同时变亮。这种"整张一起算"就是**向量化**。

## 5. 正式定义、核心公式、符号解释

### 5.1 图像 = 三维数组

- 灰度图：`shape = (H, W)`，`dtype` 通常 `uint8`（0-255）；
- 彩色图：`shape = (H, W, C)`，`C = 3`（RGB 或 BGR）；
- 深度学习 batch：`(N, C, H, W)`（PyTorch 约定，通道在前）或 `(N, H, W, C)`（NumPy/OpenCV 约定）。

### 5.2 关键操作速查

| 操作 | 代码 | 含义 |
|:---|:---|:---|
| 创建数组 | `np.zeros((H, W))` | 全零数组 |
| 形状 | `arr.shape` | 返回 `(H, W, C)` 元组 |
| 切片 | `img[:100, :, :]` | 裁掉前 100 行 |
| 翻转 | `img[::-1]` | 上下翻转 |
| 类型 | `arr.astype(np.float32)` | 转浮点 |
| 归一化 | `img / 255.0` | 像素缩放到 [0,1] |
| 广播 | `img + np.array([10, 0, 0])` | 给每个像素的 R 通道加 10 |

### 5.3 广播（Broadcasting）规则

两个数组做运算时，NumPy 从后往前逐维比较：维度相同或其中一个是 1（或缺失）就兼容。例：`img (H,W,3) + shift (3,)` → `(3,)` 补成 `(1,1,3)` → 逐元素相加。这正是"给所有像素的 R 通道加 10"的底层机制。

## 6. 推导思路和思想来源

NumPy 的设计哲学来自"**数组运算代替显式循环**"：Python 的 `for` 逐元素循环每个像素要几百万次解释器调用，而 C 语言实现的内存块运算只启动一次。所以能用广播/切片完成的操作**永远不要写 for 循环**。这一原则从 kNN（算距离矩阵）到卷积（滑动窗口）贯穿整个课程。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础——创建并检查"图像"

```python
import numpy as np
# 模拟一张 4×6 的灰度图（值 0-255）
gray = np.array([
    [10, 20, 30, 40, 50, 60],
    [15, 25, 35, 45, 55, 65],
    [20, 30, 40, 50, 60, 70],
    [25, 35, 45, 55, 65, 75],
], dtype=np.uint8)
print(gray.shape)        # (4, 6)
print(gray[0, 0])        # 10 —— 第 0 行第 0 列像素
print(gray.mean())       # 平均亮度
```

### 例子 2：中等——通道操作与翻转（真实图片用 PIL 读入）

```python
import numpy as np
from PIL import Image

img = np.array(Image.open("F:/-/scratch/example_flower.png"))  # (H, W, 3), uint8
# 上下翻转
flipped = img[::-1]
# 给所有像素 R 通道加 30（广播），并防溢出回绕
img_r = img.astype(np.int16)
img_r[:, :, 0] = np.clip(img_r[:, :, 0] + 30, 0, 255)
brightened = img_r.astype(np.uint8)
print(flipped.shape, brightened.shape)
```

### 例子 3：应用——HW01 里的 kNN 距离矩阵（向量化）

kNN 要算测试集每张图与训练集每张图的欧氏距离。向量化写法：

```python
import numpy as np
X_train = np.random.rand(500, 3072)   # 500 张 32×32×3 拉平图
X_test = np.random.rand(10, 3072)
d2 = (X_test[:, None, :] - X_train[None, :, :]) ** 2   # 广播 (10,1,3072)-(1,500,3072)
dist = d2.sum(axis=2) ** 0.5          # (10, 500)
print(dist.shape)  # (10, 500)：第 i 行 = 测试图 i 到所有训练图的距离
```

`X_test[:, None, :]` 引入新轴后广播，避免三层 for 循环——这就是 HW01 的 Starter 能跑起来的核心技巧。

## 8. 常见误区和易混概念

| 误区 | 正确理解 |
|:---|:---|
| `uint8` 加减会溢出 | 255+10 回绕为 9；先转 `int16`/`float32` 再 `clip` |
| RGB vs BGR | OpenCV 读入是 BGR、PIL 是 RGB；混用会得到颜色错乱的图 |
| `(H,W,C)` vs `(C,H,W)` | PyTorch 模型要 `(N,C,H,W)`；NumPy 图像是 `(H,W,C)`，喂给 PyTorch 前要 `img.transpose(2,0,1)` |
| 用 for 循环逐像素 | 慢几个数量级；用广播/切片/矩阵运算 |
| 忘记归一化 | 网络输入一般要求 `[0,1]` 或标准化，直接喂 0-255 会毁掉初始化假设 |

## 9. 相关知识点与 Obsidian 双链建议

- 下一站：[[02-Knowledge/🧠 学习系统/05-计算机视觉/01-底层基石/图像表示|图像表示]]（图像的数字表示本身）；
- 作业依赖：[[03-Projects/05-计算机视觉/课后作业/05-计算机视觉-课后作业-01-kNN与Softmax线性分类|课后作业-01]] 的 Starter 与本卡例子 3 直接对应；
- 全库参考：[[02-Knowledge/🧠 学习系统/17-机器学习/00-前置知识/🧭 机器学习-前置知识|机器学习前置]]。

## 10. 闭卷复现任务

不查资料，10 分钟内完成：

1. 用 NumPy 创建一张 3×4 的灰度图，把第 2 行全部设为 255；
2. 写一行代码把一张 `(H, W, 3)` 的 `uint8` 图的所有像素加 20 且不溢出；
3. 写出把 `(H, W, C)` 转成 `(C, H, W)` 的 `transpose` 参数。

## 11. 自测题：5 道

1. `np.zeros((3, 4, 5)).shape` 是多少？ #自测题/基础
2. 为什么 `img + 50` 在 `uint8` 下会让暗部变黑？如何修复？ #自测题/基础
3. `A = np.zeros((4, 1, 6))`，`B = np.zeros((3, 6))`，`A + B` 是否合法？结果形状？ #自测题/中等
4. 给 `(H, W, 3)` 图像实现"上下翻转 + 左右翻转"各一行。 #自测题/中等
5. kNN 距离矩阵为什么用 `X_test[:, None, :]` 而不是 `X_test`？ #自测题/较难

## 12. 我的主动回忆区

（学习者自填：学完后合上笔记，用自己的话写"图像数组的维度约定、广播规则、两个常见 bug"。）

## 13. 给 Obsidian 的归档建议

保持在前置知识层（`00-前置知识/`），作为阶段0 的第一张编程前置卡；后续课程若出现"NumPy 图像操作"类提问，链接回本卡，不另建重复卡。

---

## 🔗 知识图谱

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
