---
type: index
topic: "复盘与 Spaced Repetition"
created: 2026-08-02
status: active
flow: knowledge
kind: moc
tags: [方法论, 复盘, Anki, FSRS, SOP]
---

# 04 · 复盘与 Spaced Repetition

> **核心原则**：Anki 26.05 FSRS 唯一负责调度，Obsidian 只做知识主仓库。

## 🎯 调度分工

| 工具 | 角色 | 边界 |
|:---|:---|:---|
| **Anki 26.05 + FSRS** | 唯一调度方 | 生成卡片、安排复习、计算下次间隔 |
| **Obsidian** | 知识主仓库 | 写作、反链、可视化 |
| **导出脚本** | 99-System/tools/export_anki_cards.py | 把 `## 🃏 Anki 卡片` 段批量导出为 TSV |

**为什么不让 Obsidian Spaced Repetition 插件介入**：
- 双调度会冲突（FSRS 与 SM-2 间隔算法不一致）
- Obsidian 关闭时复习中断；Anki 跨设备同步
- Anki 的统计更专业（retention 曲线、卡密度分析）

## 🔁 一张卡片的完整生命周期

```
写新卡 → 标 status: ongoing → 完成学习 → Anki 制卡 → 每日复习
   ↓                                          ↓ Anki Again
[已掌握] 标 status: completed           [薄弱点] 回流到 04-Review
                                              ↓ 修复完成
                                         回流到原卡 + 再次制卡
```

### 阶段 1：写新卡

在 Obsidian 写完一张教师式课程卡，结尾必须有：

```markdown
## 🃏 Anki 卡片

- {{问题 1}} :: {{答案 1}}
- {{问题 2}} :: {{答案 2}}
- {{问题 3}} :: {{答案 3}}
```

**卡片设计原则**：
- 一张卡只考**一个判断点**
- 答案不超过 3 句
- 强制覆盖：定义 / 直觉 / 反例 / 边界

### 阶段 2：导出到 Anki

```bash
# 从所有 flow=knowledge / kind=concept 的笔记导出
python 99-System/tools/export_anki_cards.py \
  --deck "Machine Learning::01 基础概念" \
  --tags "machine-learning 17-机器学习 concept" \
  --output anki_cards.tsv

# 导入 Anki
# File → Import → 选择 TSV → 字段映射：问题,答案,标签
```

卡片格式：
- 正面：问题
- 背面：答案
- 标签：自动从 `tags` + `course` 字段拼接

### 阶段 3：每日复习

在 Anki 26.05 里复习。复习结果分 4 档：

| Anki 操作 | 含义 | 下次间隔（FSRS 算） | Obsidian 动作 |
|:---|:---|:---|:---|
| **Again** | 完全不记得 | 1-3 天 | 回流到 `04-Review/`，原卡标 `weak: true` |
| **Hard** | 吃力 | 5-10 天 | 不动 |
| **Good** | 正常回忆 | 10-60 天 | 不动 |
| **Easy** | 流畅 | 60+ 天 | 不动 |

### 阶段 4：薄弱点回流（Again 时）

```yaml
---
type: study
topic: "假设空间"
status: review
flow: review
weak: true
weak_since: 2026-08-15
anki_status: again
anki_review_count: 3
---
```

**配套动作**：
1. 在 `04-Review/04-🔁 Review.md` 登记
2. 48 小时内**修复**：重做 L1-L4 练习 + 写一段"为什么这里卡住"
3. 修复后改回 `flow: knowledge`，去掉 `weak: true`
4. **重新制卡**（在 Anki 里重置为新卡）

## 📊 复习健康度指标

### Anki 内置指标

- **Retention**（记忆保持率）：目标 ≥ 85%
- **Lapse rate**（失忆率）：目标 < 10%
- **Daily reviews**（每日复习数）：稳定在 30-80 张

### Obsidian 端指标

主页 Dataview 查询：

```dataviewjs
const all = dv.pages().where(p => !p.template);
const weak = all.where(p => p.weak === true).length;
const inReview = all.where(p => p.flow === "review").length;
const completed = all.where(p => p.status === "completed").length;

dv.table(
  ["指标", "数量", "健康"],
  [
    ["薄弱点", weak, weak < 10 ? "✅" : "⚠️"],
    ["Review 流", inReview, "—"],
    ["已完成", completed, "—"]
  ]
);
```

## 🎚️ 复习节奏

| 周期 | 动作 | 工具 |
|:---|:---|:---|
| 每日 | Anki 复习 + 标记 Again | Anki 26.05 |
| 每周 | 整理 04-Review/ 入口、复盘薄弱点 | Obsidian + Anki 统计 |
| 每月 | 卡组审计（哪些题一直 Again） | Anki Browse |
| 每 Sprint | 课程主线 5 张新卡 + 1 个 L3 项目 | Sprint + Anki |
| 每季度 | 卡组合并/拆分、tag 整理 | Anki + Obsidian |

## 🃏 Anki 卡片库结构

```
Collection "WorkBuddy"
├── Machine Learning
│   ├── 01 基础概念
│   ├── 02 线性模型
│   ├── 03 正则优化
│   ├── 04 树与集成
│   └── 05 其他方法
├── Deep Learning
├── Statistics
├── ...
└── Meta
    └── 笔记本身使用问题
```

**deck 命名约定**：`<学科> :: <阶段>`，与 `01-基础概念/...` 路径对应。

## 🛠️ 工具脚本

`99-System/tools/export_anki_cards.py` 用法（计划新建，骨架见 99-System/tools/）：

```python
# 伪代码
import frontmatter
import pathlib

def export_cards(root="02-Knowledge/🧠 学习系统/", deck="Default"):
    cards = []
    for md in pathlib.Path(root).rglob("*.md"):
        post = frontmatter.load(md)
        if post.get("type") != "study":
            continue
        if "Anki 卡片" not in post.content:
            continue
        # 解析 ## 🃏 Anki 卡片 段
        ...
        cards.append((q, a, tags))
    return cards
```

## ⚠️ 常见错误

1. **卡片太多来不及复习** → 每天新增 ≤ 5 张，控制 review 总量
2. **卡片答案太长** → 不超过 3 句，复杂的拆成多张
3. **复制整段笔记到卡片** → 不是背卡片，是**回查卡片**指向笔记
4. **不标记 Again** → FSRS 失效，复习间隔虚高
5. **修复完忘记改 `weak: false`** → 卡片一直留在 review 队列

## 🆘 应急流程：考前突击

| 时间 | 动作 |
|:---|:---|
| 考前 7 天 | 把目标卡组 `tag:expo-mode` 标记，每日 2 倍速复习 |
| 考前 3 天 | 集中过 L1-L2 卡，放弃 L4 卡 |
| 考前 1 天 | 只过最近 3 天**Again** 的卡 |
| 考后 | 解 `tag:expo-mode`，恢复正常节奏 |

---

*创建于：2026-08-02 · 配套文档：[[01-教师式课程卡填法]] [[02-阶梯作业填法]] [[03-Obsidian 嵌入与反向链接]]*
