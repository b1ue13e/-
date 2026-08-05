---
title: "计算机组成原理-题型-Jack语言与高层编程阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "计算机组成原理作业"
course: "11-计算机组成原理"
created: 2026-08-03
updated: 2026-08-03
date: 2026-08-03
status: learning
difficulty: advanced
importance: A
concept: ["Jack语言", "高层编程", "对象与数组"]
prerequisites: ["[[🧭 开源作业体系-计算机组成原理]]", "[[🧠 布尔逻辑门与HDL]]", "[[🧠 ALU算术逻辑单元]]"]
related: ["[[🧠 CPU与取指执行循环]]", "[[02-Knowledge/🧠 学习系统/11-计算机组成原理/汇编编译器(Assembler)|汇编编译器]]"]
upstream: ["[[🧭 开源作业体系-计算机组成原理]]"]
downstream: ["[[计算机组成原理 - HW10：编译器前端词法与语法分析阶梯作业]]"]
tags: [学习, 11-计算机组成原理, 作业, 实战, 阶梯作业]
aliases: ["N2T-Project09-Jack语言作业", "HW09-Jack语言"]
---

# 计算机组成原理 - HW09：Jack 语言与高层编程阶梯作业

> 🎯 **作业目标**：手写一个完整的 Jack 高层语言程序（游戏或应用），掌握类/方法/语句/表达式的写法，用官方 JackAnalyzer 验证语法，并在 CPU Emulator 上实际运行。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`nand2tetris/projects/09/`（官方提供 Pong 完整版源码供参考；自写程序放自建子目录）
- **开源标杆仓库**：[nand2tetris/nand2tetris](https://github.com/nand2tetris/nand2tetris)（官方 Software Suite：JackCompiler、JackAnalyzer、CPU Emulator、TextComparer）
- **语言规范**：*The Elements of Computing Systems* Chapter 9《The Jack Language》——词法元素（关键字/符号/标识符/常量）、类与子程序（constructor / function / method）、语句（let / if / while / do / return）、表达式、数组与字符串、Jack OS API 一览
- **运行链路**：`JackCompiler <目录>` 把 `.jack` 编译为 `.vm`，再在 CPU Emulator（与 OS 库配合）中加载运行；语法检查可单独用 JackAnalyzer
- **Honor Code**：官方 Pong 源码可阅读对照，但自写程序须独立完成，完成后复盘官方实现

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 验收标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | Hello World 与算术程序语法通过 | 写 `HelloWorld.jack`（字符串输出）+ 一个含变量、表达式、`if`、`while` 的算术小程序；JackAnalyzer 零报错，编译后在 CPU Emulator 输出正确结果。 |
| 🟡 **L2 - Medium Baseline** | 简单游戏（弹球）可玩 | 单文件游戏：键盘输入（`Keyboard`）、屏幕移动（`Output`/屏幕映射）、简单碰撞检测（`Math`）；编译运行无崩溃，游戏逻辑可交互。 |
| 🔴 **L3 - Strong Baseline** | Pong 完整版跑通 | 多类组织（`Main` / `Ball` / `Paddle` / `Game`），使用对象、数组与完整游戏循环；编译通过并在 CPU Emulator 配合 OS 完整运行，能计分、判定胜负。 |
| 👑 **L4 - Boss Baseline** | 自创 Jack 程序 | 自选创意程序（必须含数组、字符串、多文件三要素），附一段设计说明；全流程（JackAnalyzer 检查 → JackCompiler 编译 → CPU Emulator 运行）跑通并留档。 |

---

## 3. 🧪 自动化测试 Harness (Validation)

官方 Project 09 为自由作业，无 `.tst` 脚本；验收分两步：**语法检查**（JackAnalyzer 产出 XML 无报错）+ **运行验证**（CPU Emulator 手动/截图留档）。

```python
import subprocess
import pathlib

def validate_jack(prog_dir: str) -> bool:
    """调用官方 JackAnalyzer 做语法检查：能产出 .xml 且无报错即通过"""
    r = subprocess.run(["JackAnalyzer", prog_dir],
                       capture_output=True, text=True)
    xml_files = list(pathlib.Path(prog_dir).glob("*.xml"))
    return r.returncode == 0 and len(xml_files) > 0
```

shell 一键编译 + 模拟运行（macOS/Linux 脚本路径示例）：

```bash
sh nand2tetris/tools/JackCompiler.sh projects/09/MyGame && \
sh nand2tetris/tools/CPUEmulator.sh projects/09/MyGame
```

---

## 🃏 Anki 卡片

- Q: Jack 中 `constructor` / `function` / `method` 三种子程序有何区别？
- A: `constructor` 负责为对象分配内存并初始化（用类名调用，绑定 this）；`function` 是静态过程（类名调用，无 this）；`method` 作用于对象实例（实例调用，隐式携带 this 参数）。
- Q: Jack 中 `if` 与 `while` 语句的语法是什么？
- A: `if (condition) { ... } else { ... }`；`while (condition) { ... }`——条件必须加括号，语句体用花括号包裹。
- Q: Jack 的数组与字符串是如何表示的？
- A: 数组是 `Array` 类对象（本质是内存基址指针，按索引访问连续内存）；字符串是 `String` 类实例，封装长度、容量与底层字符数组。
- Q: 为何 Jack 程序必须配合 Jack OS 才能运行？
- A: 高层语言依赖字符串处理、屏幕输出、键盘输入、内存分配等底层服务，这些由 Jack OS 库提供；编译器把高层调用翻译为对 OS 库的 VM 调用，缺 OS 则程序无法启动。

---

## 📌 待办与验收留档
- [ ] L1：HelloWorld.jack + 算术程序，JackAnalyzer 通过
- [ ] L2：弹球游戏可玩，CPU Emulator 留档
- [ ] L3：Pong 完整版跑通（计分/胜负）
- [ ] L4：自创程序 + 设计说明，截图存入 `03-Projects/11-计算机组成原理/`
- [ ] 口试验收 3 问：这一层向上提供什么接口？向下使用什么接口？测试脚本在验证什么？
