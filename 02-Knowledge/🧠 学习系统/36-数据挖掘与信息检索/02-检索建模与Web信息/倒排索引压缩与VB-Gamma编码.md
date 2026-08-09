---
type: study
topic: "倒排索引压缩与VB-Gamma编码"
course: "数据挖掘与信息检索"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段2-检索建模与Web信息]]"
flow: knowledge
kind: concept
upstream: ["[[倒排索引系统]]"]
tags: [学习, 数据挖掘与信息检索]
---
## 💡 动机与直觉

海量搜索引擎（如 Google、Baidu）管理着数十亿级网页文档，倒排索引的 Postings List（倒排链）规模极其庞大。

- **差分编码 (d-gaps)**：倒排链中的 DocID 是升序排列的（如 `[100, 105, 108, 120]`）。若直接存储原始 DocID，每个 ID 需占用 32 位（4 字节）。改存相邻 DocID 的差值 `d-gap`（如 `[100, 5, 3, 12]`），数值显著变小。
- **可变长编码 (Variable Byte & Gamma Encoding)**：利用 `d-gap` 中绝大多数数值极小的特点，使用更少的字节（字节对齐）或比特（Bit 级编码）来压缩存储，将索引体积压缩到原有的 15%~25%，大幅提升 CPU Cache 命中率与内存检索吞吐。

---

## 📐 算法原理与规约

### 1. Variable Byte (VB) 字节对齐编码
VB 编码以字节（Byte，8 Bits）为单位。每个字节包含：
- **1 比特延续位 (Continuation Bit $c$)**：若 $c=1$，表示当前字节是该数字的**最后一个字节**；若 $c=0$，表示后续字节仍属于当前数字。
- **7 比特有效数据位 (Payload Bits)**：存放二进制数值。

```
数值 5   (二进制 101):         [10000101] (1 个字节即可表示，首位为 1)
数值 130 (二进制 10000010):    [00000001] [10000010] (拆分为前 7 位与后 7 位)
```

- **特点**：字节对齐，CPU 移位与掩码操作极快，解码吞吐可达 GB/s 级。

### 2. Elias Gamma ($\gamma$) 比特级编码
Elias Gamma 编码适用于数值极小的场景，将正整数 $x$ 编码为两部分：
1. **Length (长度域)**：$N = \lfloor \log_2 x \rfloor$，编码为 $N$ 个 `1` 后接一个 `0`（Unary code）。
2. **Offset (偏移域)**：$x - 2^N$，表示为长度为 $N$ 的二进制数。

$$\text{Gamma}(x) = \underbrace{11\dots10}_{N \text{ 个 1，加上 0}} \,||\, \text{Offset}(x)$$

- **示例**：
  - $x = 1$: $N=0 \Rightarrow$ Length: `0`, Offset:空 $\Rightarrow \mathbf{0}$
  - $x = 9$: $N=3 \Rightarrow$ Length: `1110`, Offset: $9-8 = 1 \Rightarrow \mathbf{001}_2 \Rightarrow \mathbf{1110001}$

---

## 💻 最小 Python 实现

```python
from typing import List

def vb_encode_number(n: int) -> bytearray:
    bytes_list = []
    while True:
        bytes_list.insert(0, n % 128)
        if n < 128:
            break
        n //= 128
    # 最后一个字节的首位置为 1
    bytes_list[-1] += 128
    return bytearray(bytes_list)

def vb_encode(numbers: List[int]) -> bytearray:
    stream = bytearray()
    for num in numbers:
        stream.extend(vb_encode_number(num))
    return stream

def vb_decode(stream: bytearray) -> List[int]:
    numbers = []
    n = 0
    for byte in stream:
        if byte < 128:
            n = 128 * n + byte
        else:
            n = 128 * n + (byte - 128)
            numbers.append(n)
            n = 0
    return numbers

# 倒排链差分压缩与解压测试
if __name__ == "__main__":
    postings_list = [1000, 1005, 1012, 1050, 1200]
    # 1. 转为 d-gaps
    dgaps = [postings_list[0]] + [postings_list[i] - postings_list[i-1] for i in range(1, len(postings_list))]
    print("原始 Postings List:", postings_list)
    print("d-gaps 列表:", dgaps)

    # 2. VB 编码
    encoded_bytes = vb_encode(dgaps)
    print(f"VB 编码字节数: {len(encoded_bytes)} 字节 (原始 32-bit 需要 {len(postings_list)*4} 字节)")

    # 3. VB 解码与还原
    decoded_dgaps = vb_decode(encoded_bytes)
    restored_postings = [decoded_dgaps[0]]
    for gap in decoded_dgaps[1:]:
        restored_postings.append(restored_postings[-1] + gap)
    print("解压还原 Postings List:", restored_postings)
    assert restored_postings == postings_list
```

---

## ⚠️ 常见误区与避坑指南

1. **误区：未做 d-gaps 差分变换直接压缩**
   - 避坑：若未做 `d-gaps` 变换，原始 DocID（如 10,000,000）数值依然很大，Variable Byte 或 Gamma 编码无法节省任何空间，甚至会因标识位增加存储消耗。

---

## 🃏 Anki 卡片

**Q: 什么是倒排链 d-gaps 差分编码？为什么它能提升压缩率？**
**A**:
- **定义**：将单调递增的倒排链 `[d1, d2, d3]` 替换为相邻两项的差值 `[d1, d2-d1, d3-d2]`。
- **原因**：搜索引擎倒排链中文档密居度高，差值数值通常极小（如 1~10），配合 Variable Byte 或 Gamma 可用 1~2 字节完成存储。

---

---

## 🔗 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```