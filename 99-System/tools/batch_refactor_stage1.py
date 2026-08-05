import os

base_dir = r'f:\-\02-Knowledge\🧠 学习系统\10-数据结构与算法\01-算法入门与基本分析'

# 定义阶段 1 各文件的硬核 Markdown 内容映射
stage1_data = {
    "冒泡排序.md": """---
title: "冒泡排序"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "B类：基础排序算法"
tags:
  - 学习
  - 数据结构与算法
  - 冒泡排序
  - 排序算法
upstream:
  - "[[排序概述]]"
downstream:
  - "[[快速排序]]"
status: learning
topic: "冒泡排序"
created: 2026-07-28
updated: 2026-07-28
difficulty: beginner
concept:
  - "冒泡排序"
prerequisites:
  - "[[数组基础]]"
related:
  - "[[选择排序]]"
  - "[[插入排序]]"
flow: knowledge
kind: concept
aliases:
  - "Bubble Sort"
---

# 冒泡排序

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🌱 第一阶段：算法入门与基本分析]]  
> **学习定位**：B类：基础排序算法

---

### 0. 先判断它值不值得深挖

- **类别**：B类：基础排序算法
- **分类理由**：冒泡排序（Bubble Sort）是最直观的基于比较的交换排序算法。虽然其平均与最坏时间复杂度均为 $O(n^2)$，在工程中很少直接用于大规模数据排序，但它是理解**算法稳定性（Stability）**、**逆序对（Inversion Pair）消除**以及早期算法优化（如提前终止标志位）的经典教学范例。

---

### 1. 这个知识点解决什么问题？

#### 我们遇到了什么麻烦
如何在一个无序数组中，仅通过相邻元素的局部比较与交换，逐步恢复全局的有序性？

#### 核心解决原理
冒泡排序模拟了气泡在水中上浮的过程：
- 每一轮从头到尾遍历数组，比较相邻的两个元素 $A[j]$ 与 $A[j+1]$；
- 若 $A[j] > A[j+1]$ 则交换它们，将当前未排序区域的最大值像气泡一样“推”到最右端；
- 经过 $n-1$ 轮沉淀，整组数据完全有序。

---

### 2. 核心 C++ 代码与优化

```cpp
#include <vector>
#include <algorithm>

using namespace std;

// 带提前终止标志位的优化冒泡排序
void bubbleSort(vector<int>& nums) {
    int n = nums.size();
    for (int i = 0; i < n - 1; i++) {
        bool swapped = false; // 交换标记
        for (int j = 0; j < n - 1 - i; j++) {
            if (nums[j] > nums[j + 1]) {
                swap(nums[j], nums[j + 1]);
                swapped = true;
            }
        }
        // 若一整轮比较中没有发生任何交换，说明数组已经完全有序，提前退出
        if (!swapped) break;
    }
}
```

---

### 3. 复杂度与稳定性分析

- **时间复杂度**：
  - 最坏情况（逆序）：$O(n^2)$
  - 最好情况（已有序 + 提前终止优化）：$O(n)$
  - 平均情况：$O(n^2)$
- **空间复杂度**：$O(1)$ 原地排序
- **稳定性**：**稳定**（相等的元素不会发生交换）

---

### 4. 自测题：2 道

#### 1. [概念辨析] 为什么冒泡排序是一种稳定的排序算法？
A. 因为它的时间复杂度是 $O(n^2)$  
B. 因为当相邻两个元素数值相等时，算法不会触发交换，相对顺序保持不变  
C. 因为它使用了额外的辅助数组  
D. 因为它支持二分查找  

> [!question]- 答案解析
> **答案**：B  
> **解析**：冒泡排序仅在 $nums[j] > nums[j+1]$ 时才进行交换。对于相等的元素，不会发生交换，因此相同元素的相对顺序在排序前后保持不变，属于稳定排序。  
> **Obsidian 标签**：`#自测题 #概念辨析`

#### 2. [代码优化] 增加 `swapped` 标志位后，冒泡排序在什么输入下的时间复杂度会降低至 $O(n)$？

> [!question]- 答案解析
> **答案**：在**完全升序（已排序）**的输入数组下。第一轮扫描完后 `swapped` 依然为 `false`，算法直接提前终止，仅耗时 $O(n)$。  
> **Obsidian 标签**：`#自测题 #代码优化`

---

### 5. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/10-数据结构与算法/01-算法入门与基本分析`
- **双链推荐**：`[[排序概述]]`、`[[选择排序]]`、`[[插入排序]]`
- **建议标签**：`#学习 #数据结构与算法 #冒泡排序 #排序算法 #B类`
""",

    "选择排序.md": """---
title: "选择排序"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "B类：基础排序算法"
tags:
  - 学习
  - 数据结构与算法
  - 选择排序
  - 排序算法
upstream:
  - "[[排序概述]]"
downstream:
  - "[[堆排序]]"
status: learning
topic: "选择排序"
created: 2026-07-28
updated: 2026-07-28
difficulty: beginner
concept:
  - "选择排序"
prerequisites:
  - "[[数组基础]]"
related:
  - "[[冒泡排序]]"
  - "[[堆排序]]"
flow: knowledge
kind: concept
aliases:
  - "Selection Sort"
---

# 选择排序

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🌱 第一阶段：算法入门与基本分析]]  
> **学习定位**：B类：基础排序算法

---

### 0. 先判断它值不值得深挖

- **类别**：B类：基础排序算法
- **分类理由**：选择排序（Selection Sort）是一种直观的原地比较排序算法。它的核心思想是每一轮在未排序区域中找到极值（最小值/最大值），将其交换放至已排序区域的末尾。虽然它的比较次数恒为 $O(n^2)$，但它的**交换次数最多只有 $n-1$ 次**，这一特点在写入操作开销极高的存储介质（如 Flash 闪存）中具有独特意义。

---

### 1. 核心原理与 C++ 代码

```cpp
#include <vector>
#include <algorithm>

using namespace std;

void selectionSort(vector<int>& nums) {
    int n = nums.size();
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        // 在未排序区间 [i, n-1] 中寻找最小值索引
        for (int j = i + 1; j < n; j++) {
            if (nums[j] < nums[minIdx]) {
                minIdx = j;
            }
        }
        // 将最小值交换到已排序区间的末尾 i 处
        if (minIdx != i) {
            swap(nums[i], nums[minIdx]);
        }
    }
}
```

---

### 2. 复杂度与稳定性分析

- **时间复杂度**：比较次数恒为 $\frac{n(n-1)}{2} = O(n^2)$（无论原数组是否有序）。
- **空间复杂度**：$O(1)$ 原地排序
- **稳定性**：**不稳定**！例如数组 `[5, 8, 5, 2, 9]`，第一轮选择最小值 `2` 与第一个 `5` 交换后，两个 `5` 的相对位置被破坏。

---

### 3. 自测题：2 道

#### 1. [概念辨析] 相比于冒泡排序，选择排序的最大优势在于？
A. 比较次数更少  
B. 算法是稳定的  
C. 交换元素的总次数最多只有 $n-1$ 次（$O(n)$ 级别交换）  
D. 支持并行计算  

> [!question]- 答案解析
> **答案**：C  
> **解析**：选择排序每轮只进行一次交换，全过程最多交换 $n-1$ 次。而冒泡排序最坏需要 $O(n^2)$ 次交换。  
> **Obsidian 标签**：`#自测题 #概念辨析`

#### 2. [稳定性] 为什么选择排序是非稳定的排序算法？请举例说明。

> [!question]- 答案解析
> **答案**：因为长距离的交换会破坏相同元素的相对位置。例如序列 `[5, 5', 2]`，第一轮会将 `2` 与第一个 `5` 交换，变为 `[2, 5', 5]`，原本在前方的 `5` 被换到了 `5'` 的后方，破坏了稳定性。  
> **Obsidian 标签**：`#自测题 #稳定性`

---

### 4. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/10-数据结构与算法/01-算法入门与基本分析`
- **双链推荐**：`[[排序概述]]`、`[[冒泡排序]]`、`[[堆排序]]`
- **建议标签**：`#学习 #数据结构与算法 #选择排序 #排序算法 #B类`
""",

    "插入排序.md": """---
title: "插入排序"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "A类：核心基础算法"
tags:
  - 学习
  - 数据结构与算法
  - 插入排序
  - 排序算法
upstream:
  - "[[排序概述]]"
downstream:
  - "[[希尔排序]]"
  - "[[归并排序]]"
status: learning
topic: "插入排序"
created: 2026-07-28
updated: 2026-07-28
difficulty: beginner
concept:
  - "插入排序"
prerequisites:
  - "[[数组基础]]"
related:
  - "[[选择排序]]"
  - "[[冒泡排序]]"
flow: knowledge
kind: concept
aliases:
  - "Insertion Sort"
---

# 插入排序

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🌱 第一阶段：算法入门与基本分析]]  
> **学习定位**：A类：核心基础算法

---

### 0. 先判断它值不值得深挖

- **类别**：A类：核心基础算法
- **分类理由**：插入排序（Insertion Sort）是小规模数据（$n \le 16$）或近乎有序数据下实际运行速度最快的排序算法。工业级混合排序算法（如 C++ `std::sort` 的 Introsort 和 Python 的 Timsort）在递归底层均切换为插入排序。它的核心思想类似于抓扑克牌，将新元素插入到左侧已排好序的序列中。

---

### 1. 核心原理与 C++ 代码

```cpp
#include <vector>

using namespace std;

void insertionSort(vector<int>& nums) {
    int n = nums.size();
    for (int i = 1; i < n; i++) {
        int key = nums[i];
        int j = i - 1;
        // 将大于 key 的元素向右平移
        while (j >= 0 && nums[j] > key) {
            nums[j + 1] = nums[j];
            j--;
        }
        nums[j + 1] = key; // 插入 key 到正确位置
    }
}
```

---

### 2. 复杂度与工业界价值

- **时间复杂度**：
  - 最坏情况（逆序）：$O(n^2)$
  - 最好情况（基本有序）：**$O(n)$**
- **空间复杂度**：$O(1)$ 原地排序
- **稳定性**：**稳定**
- **工业界应用**：
  - **Timsort / Introsort 底座**：分治算法（如快排、归并）在子数组较小时，递归开销占比过高，直接调用插入排序效率最高。

---

### 3. 自测题：2 道

#### 1. [应用场景] 为什么 C++ `std::sort` 在递归区间长度小于 16 时，会切换为插入排序？
A. 因为插入排序的内存开销更大  
B. 因为在小规模数据下，插入排序的代码常数项极其微小，且没有函数递归栈开销，实际运行速度超越快排  
C. 因为插入排序是 $O(\log n)$ 算法  
D. 因为插入排序支持多线程  

> [!question]- 答案解析
> **答案**：B  
> **解析**：快速排序和归并排序有递归调用的压栈开销，且 CPU 缓存命中率在小规模时优势不明显。插入排序代码极其精简、常数极小，在小数组上性能冠绝所有算法。  
> **Obsidian 标签**：`#自测题 #工业应用`

#### 2. [复杂度分析] 如果一个数组中只有 $K$ 个元素位置错乱（其余元素均已排序），插入排序的时间复杂度是？

> [!question]- 答案解析
> **答案**：$O(n + K^2)$ 或 $O(n)$（当 $K$ 为常数时）。插入排序对于近乎有序的数据具有天然的 $O(n)$ 线性效率。  
> **Obsidian 标签**：`#自测题 #复杂度分析`

---

### 4. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/10-数据结构与算法/01-算法入门与基本分析`
- **双链推荐**：`[[排序概述]]`、`[[快速排序]]`、`[[归并排序]]`
- **建议标签**：`#学习 #数据结构与算法 #插入排序 #排序算法 #A类`
""",

    "计数排序.md": """---
title: "计数排序"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "B类：非比较排序算法"
tags:
  - 学习
  - 数据结构与算法
  - 计数排序
  - 非比较排序
upstream:
  - "[[排序概述]]"
downstream:
  - "[[基数排序]]"
status: learning
topic: "计数排序"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "计数排序"
prerequisites:
  - "[[数组基础]]"
related:
  - "[[桶排序]]"
  - "[[基数排序]]"
flow: knowledge
kind: concept
aliases:
  - "Counting Sort"
---

# 计数排序

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🌱 第一阶段：算法入门与基本分析]]  
> **学习定位**：B类：非比较排序算法

---

### 0. 先判断它值不值得深挖

- **类别**：B类：非比较排序算法
- **分类理由**：计数排序（Counting Sort）打破了基于比较的排序算法时间复杂度下界 $O(n \log n)$ 的限制。它通过利用数组下标来统计每个数值出现的频次，实现了 **线性时间 $O(n + k)$** 的极速排序（其中 $k$ 为数据范围）。它要求输入数据必须是有确定范围的整数。

---

### 1. 核心 C++ 代码（前缀和保证稳定性）

```cpp
#include <vector>
#include <algorithm>

using namespace std;

void countingSort(vector<int>& nums) {
    if (nums.empty()) return;

    int minVal = *min_element(nums.begin(), nums.end());
    int maxVal = *max_element(nums.begin(), nums.end());
    int range = maxVal - minVal + 1;

    vector<int> count(range, 0);
    for (int num : nums) {
        count[num - minVal]++;
    }

    // 计算前缀和，确定每个元素在输出数组中的最终位置（保证稳定性）
    for (int i = 1; i < range; i++) {
        count[i] += count[i - 1];
    }

    vector<int> output(nums.size());
    // 从后往前遍历保证稳定性
    for (int i = nums.size() - 1; i >= 0; i--) {
        output[count[nums[i] - minVal] - 1] = nums[i];
        count[nums[i] - minVal]--;
    }

    nums = output;
}
```

---

### 2. 复杂度与适用边界

- **时间复杂度**：$O(n + k)$（$n$ 为元素个数，$k$ 为数值范围 $max - min$）
- **空间复杂度**：$O(n + k)$
- **缺点**：若数据范围 $k$ 极大（如排序 `[1, 1000000000]`），空间开销不可接受。

---

### 3. 自测题：2 道

#### 1. [概念辨析] 计数排序能突破 $O(n \log n)$ 下界的原因是？
A. 使用了分治法  
B. 计数排序不是基于元素间两两比较的算法，而是利用数值映射到数组下标  
C. 使用了递归  
D. 空间复杂度为 $O(1)$  

> [!question]- 答案解析
> **答案**：B  
> **解析**：基于比较的排序下界 $O(n \log n)$ 建立在决策树比较模型上。计数排序是非比较排序，通过哈希/下标计数直接确定位置，因而可达到 $O(n+k)$ 线性时间。  
> **Obsidian 标签**：`#自测题 #概念辨析`

---

### 4. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/10-数据结构与算法/01-算法入门与基本分析`
- **双链推荐**：`[[排序概述]]`、`[[基数排序]]`
- **建议标签**：`#学习 #数据结构与算法 #计数排序 #非比较排序 #B类`
""",

    "基数排序.md": """---
title: "基数排序"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "B类：非比较排序算法"
tags:
  - 学习
  - 数据结构与算法
  - 基数排序
  - 非比较排序
upstream:
  - "[[计数排序]]"
downstream:
  - "[[后缀数组]]"
status: learning
topic: "基数排序"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "基数排序"
prerequisites:
  - "[[计数排序]]"
related:
  - "[[计数排序]]"
flow: knowledge
kind: concept
aliases:
  - "Radix Sort"
---

# 基数排序

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🌱 第一阶段：算法入门与基本分析]]  
> **学习定位**：B类：非比较排序算法

---

### 0. 先判断它值不值得深挖

- **类别**：B类：非比较排序算法
- **分类理由**：基数排序（Radix Sort）是一种按位（如个位、十位、百位）分配与收集的非比较排序算法。它解决了计数排序在数据范围 $k$ 过大时的空间爆炸问题，在整数排序、字符串按字典序排序（如后缀数组 SA 构建）中应用广泛。

---

### 1. 核心原理与 C++ 代码（LSD 最低位优先）

```cpp
#include <vector>
#include <algorithm>

using namespace std;

// 对数组按特定位 (exp) 进行稳定计数排序
void countSortByDigit(vector<int>& nums, int exp) {
    int n = nums.size();
    vector<int> output(n);
    int count[10] = {0};

    for (int i = 0; i < n; i++) {
        count[(nums[i] / exp) % 10]++;
    }

    for (int i = 1; i < 10; i++) {
        count[i] += count[i - 1];
    }

    for (int i = n - 1; i >= 0; i--) {
        output[count[(nums[i] / exp) % 10] - 1] = nums[i];
        count[(nums[i] / exp) % 10]--;
    }

    for (int i = 0; i < n; i++) nums[i] = output[i];
}

void radixSort(vector<int>& nums) {
    if (nums.empty()) return;
    int maxVal = *max_element(nums.begin(), nums.end());

    // 从个位开始，逐位向高位进行稳定计数排序
    for (int exp = 1; maxVal / exp > 0; exp *= 10) {
        countSortByDigit(nums, exp);
    }
}
```

---

### 2. 复杂度与稳定性

- **时间复杂度**：$O(d \cdot (n + k))$（$d$ 为最高位数，$k$ 为进制数如 10）
- **空间复杂度**：$O(n + k)$
- **稳定性**：**必须稳定**（按高位排序时依赖低位排序的稳定结果）。

---

### 3. 自测题：1 道

#### 1. [原理运用] 为什么基数排序在按每一位排序时，底层的按位排序算法必须是稳定的？

> [!question]- 答案解析
> **答案**：因为如果按位排序不稳定，在按高位（如十位）排序时就会破坏先前低位（如个位）排好的相对顺序，导致最终结果错误。  
> **Obsidian 标签**：`#自测题 #原理运用`

---

### 4. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/10-数据结构与算法/01-算法入门与基本分析`
- **双链推荐**：`[[计数排序]]`
- **建议标签**：`#学习 #数据结构与算法 #基数排序 #B类`
""",

    "堆排序.md": """---
title: "堆排序"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "A类：核心高级排序"
tags:
  - 学习
  - 数据结构与算法
  - 堆排序
  - 优先队列
  - 排序算法
upstream:
  - "[[排序概述]]"
  - "[[二叉堆]]"
downstream:
  - "[[TopK问题]]"
status: learning
topic: "堆排序"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "堆排序"
prerequisites:
  - "[[二叉堆]]"
related:
  - "[[快速排序]]"
  - "[[归并排序]]"
flow: knowledge
kind: concept
aliases:
  - "Heap Sort"
---

# 堆排序

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🌱 第一阶段：算法入门与基本分析]]  
> **学习定位**：A类：核心高级排序

---

### 0. 先判断它值不值得深挖

- **类别**：A类：核心高级排序
- **分类理由**：堆排序（Heap Sort）是三大选择类排序算法之一，兼具 **$O(n \log n)$ 最坏时间复杂度** 与 **$O(1)$ 原地空间开销**。虽然在内存缓存命中率上略逊于快速排序，但它不存在快排最坏退化为 $O(n^2)$ 的风险，在 C++ `std::sort`（Introsort 恶化兜底）中扮演着安全防线的角色。

---

### 1. 核心 C++ 代码与下沉建堆

```cpp
#include <vector>
#include <algorithm>

using namespace std;

// 维护大根堆的下沉操作 (Sift Down)
void heapify(vector<int>& nums, int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < n && nums[left] > nums[largest]) largest = left;
    if (right < n && nums[right] > nums[largest]) largest = right;

    if (largest != i) {
        swap(nums[i], nums[largest]);
        heapify(nums, n, largest); // 递归下沉
    }
}

void heapSort(vector<int>& nums) {
    int n = nums.size();

    // 1. 自底向上建堆 O(n)
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(nums, n, i);
    }

    // 2. 逐个将堆顶最大值交换至末尾并重新堆化 O(n log n)
    for (int i = n - 1; i > 0; i--) {
        swap(nums[0], nums[i]);
        heapify(nums, i, 0);
    }
}
```

---

### 2. 复杂度与稳定性

- **时间复杂度**：建堆 $O(n)$，排序 $O(n \log n)$，总体为 **$O(n \log n)$**。
- **空间复杂度**：$O(1)$ 严格原地
- **稳定性**：**不稳定**

---

### 3. 自测题：2 道

#### 1. [算法推导] 为什么自底向上线性建堆（Build Heap）的时间复杂度是 $O(n)$ 而不是 $O(n \log n)$？

> [!question]- 答案解析
> **答案**：高度为 $h$ 的节点数为 $\lceil n / 2^{h+1} \rceil$。对所有节点求和得到错位相减级数 $\sum \frac{h}{2^h} = 2$，故总步数为 $O(n)$。  
> **Obsidian 标签**：`#自测题 #算法推导`

#### 2. [工程对比] 为什么虽然堆排序与快排时间同为 $O(n \log n)$，但实际运行中快排更快？

> [!question]- 答案解析
> **答案**：因为堆排序的下沉操作会在数组中跨大步跳跃访问（父节点 $i$ 与子节点 $2i+1$），破坏了 CPU 的 **局部性原理（Locality of Reference）**，导致 CPU 缓存（Cache Miss）失效较多。  
> **Obsidian 标签**：`#自测题 #工程对比`

---

### 4. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/10-数据结构与算法/01-算法入门与基本分析`
- **双链推荐**：`[[排序概述]]`、`[[二叉堆]]`、`[[快速排序]]`
- **建议标签**：`#学习 #数据结构与算法 #堆排序 #A类`
""",

    "二维前缀和.md": """---
title: "二维前缀和"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "A类：常用技巧"
tags:
  - 学习
  - 数据结构与算法
  - 二维前缀和
  - 前缀和
upstream:
  - "[[前缀和]]"
downstream:
  - "[[矩阵应用]]"
status: learning
topic: "二维前缀和"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "二维前缀和"
prerequisites:
  - "[[前缀和]]"
related:
  - "[[差分]]"
flow: knowledge
kind: concept
aliases:
  - "2D Prefix Sum"
---

# 二维前缀和

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🌱 第一阶段：算法入门与基本分析]]  
> **学习定位**：A类：常用技巧

---

### 0. 核心原理解析

二维前缀和将一维前缀和拓展至矩阵空间。通过容斥原理，实现 **$O(1)$ 时间查询任意子矩阵 $[r_1, c_1] \dots [r_2, c_2]$ 的元素之和**。

#### 1. 递推预处理公式 (建表 $O(M \times N)$)
$$P[i][j] = P[i-1][j] + P[i][j-1] - P[i-1][j-1] + grid[i-1][j-1]$$

#### 2. 子矩阵区间和查询公式 (查询 $O(1)$)
$$\text{Sum}(r_1, c_1, r_2, c_2) = P[r_2+1][c_2+1] - P[r_1][c_2+1] - P[r_2+1][c_1] + P[r_1][c_1]$$

---

### 1. 核心 C++ 代码

```cpp
#include <vector>

using namespace std;

class NumMatrix {
private:
    vector<vector<int>> P;

public:
    NumMatrix(vector<vector<int>>& matrix) {
        int m = matrix.size(), n = matrix[0].size();
        P.assign(m + 1, vector<int>(n + 1, 0));

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                P[i][j] = P[i - 1][j] + P[i][j - 1] - P[i - 1][j - 1] + matrix[i - 1][j - 1];
            }
        }
    }

    int sumRegion(int row1, int col1, int row2, int col2) {
        return P[row2 + 1][col2 + 1] - P[row1][col2 + 1] - P[row2 + 1][col1] + P[row1][col1];
    }
};
```

---

### 2. 自测题：1 道

#### 1. [容斥原理] 在二维前缀和预处理公式中，为什么要减去 $P[i-1][j-1]$？

> [!question]- 答案解析
> **答案**：因为在相加左边区域 $P[i][j-1]$ 与上方区域 $P[i-1][j]$ 时，左上角的重叠矩形 $P[i-1][j-1]$ 被重复加了两次，故需减去一次。  
> **Obsidian 标签**：`#自测题 #容斥原理`

---

### 3. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/10-数据结构与算法/01-算法入门与基本分析`
- **双链推荐**：`[[前缀和]]`、`[[差分]]`
- **建议标签**：`#学习 #数据结构与算法 #二维前缀和 #A类`
""",

    "差分.md": """---
title: "差分"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "A类：常用技巧"
tags:
  - 学习
  - 数据结构与算法
  - 差分
  - 算法技巧
upstream:
  - "[[前缀和]]"
downstream:
  - "[[二维前缀和]]"
status: learning
topic: "差分"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "差分"
prerequisites:
  - "[[前缀和]]"
related:
  - "[[前缀和]]"
flow: knowledge
kind: concept
aliases:
  - "Difference Array"
---

# 差分

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🌱 第一阶段：算法入门与基本分析]]  
> **学习定位**：A类：常用技巧

---

### 0. 核心原理解析

差分数组（Difference Array）是前缀和的逆运算。它主要解决 **频繁对区间 $[L, R]$ 里的每个元素同时加上或减去常数 $V$** 的问题。它将区间的批量修改，转化为对差分数组 **端点 2 个元素的 $O(1)$ 修改**！

#### 核心公式
1. **构造差分数组**：$D[i] = A[i] - A[i-1]$
2. **区间 $[L, R]$ 加 $V$**：
   - $D[L] += V$
   - $D[R+1] -= V$
3. **还原原数组**：对 $D$ 求前缀和即可得到最新的 $A$！

---

### 1. 核心 C++ 代码

```cpp
#include <vector>

using namespace std;

class Difference {
private:
    vector<int> diff;

public:
    Difference(const vector<int>& nums) {
        int n = nums.size();
        diff.resize(n);
        diff[0] = nums[0];
        for (int i = 1; i < n; i++) {
            diff[i] = nums[i] - nums[i - 1];
        }
    }

    // 给区间 [i, j] 增加 val
    void increment(int i, int j, int val) {
        diff[i] += val;
        if (j + 1 < diff.size()) {
            diff[j + 1] -= val;
        }
    }

    // 返回还原后的数组
    vector<int> result() {
        vector<int> res(diff.size());
        res[0] = diff[0];
        for (int i = 1; i < diff.size(); i++) {
            res[i] = res[i - 1] + diff[i];
        }
        return res;
    }
};
```

---

### 2. 自测题：1 道

#### 1. [应用场景] 差分数组适合什么操作场景？
A. 频繁查询区间和  
B. 频繁进行区间批量修改，且最终只需要一次性还原全图结果  
C. 单点修改  
D. 矩阵乘法  

> [!question]- 答案解析
> **答案**：B  
> **解析**：差分每次区间修改只需 $O(1)$，修改完成后求一次前缀和 $O(n)$ 即可还原全图，极其高效。  
> **Obsidian 标签**：`#自测题 #应用场景`

---

### 3. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/10-数据结构与算法/01-算法入门与基本分析`
- **双链推荐**：`[[前缀和]]`、`[[二维前缀和]]`
- **建议标签**：`#学习 #数据结构与算法 #差分 #A类`
"""
}

# 批量写入阶段 1 的改写文件
count = 0
for filename, text in stage1_data.items():
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text.strip() + '\n')
    count += 1

print(f"Stage 1 batch 1 refactored successfully: {count} files updated.")
