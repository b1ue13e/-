---
type: index
cssclasses:
  - atlas-page
  - atlas-index
topic: "学习系统工具集"
created: 2026-04-11
status: active
tags: [工具, 指南]
---

# 学习系统工具集

本目录包含用于维护 Obsidian 学习系统的辅助工具。

## 工具列表

### 1. batch_frontmatter_updater.py

批量更新学习笔记 frontmatter 的工具。

#### 功能
- 自动检测文件类型（阶段文件/主题笔记）
- 为缺失 frontmatter 的文件添加标准模板
- 为已有 frontmatter 的文件补充缺失字段
- 预览模式（dry-run）避免误操作

#### 用法

```bash
# 预览模式（推荐先运行）
python tools/batch_frontmatter_updater.py --dry-run

# 实际更新
python tools/batch_frontmatter_updater.py

# 指定路径
python tools/batch_frontmatter_updater.py --path "02-Knowledge/🧠 学习系统/01-社交网络挖掘"
```

#### 自动检测规则

| 文件类型 | 识别规则 | 使用的模板 |
|:---|:---|:---|
| 阶段文件 | 文件名包含"阶段"或以🗺️开头 | STAGE_TEMPLATE |
| 主题笔记 | 路径包含阶段编号（如01-、02-） | TOPIC_TEMPLATE |
| 其他笔记 | 默认 | NOTE_TEMPLATE |

#### 模板结构

**STAGE_TEMPLATE**（阶段入口文件）:
```yaml
tags: []
created: "2026-04-11"
status: planned
difficulty: intermediate
concept: []
prerequisites: []
related: []
phase: 1  # 自动提取
```

**TOPIC_TEMPLATE**（具体知识点笔记）:
```yaml
topic: "笔记标题"
created: "2026-04-11"
status: ongoing
difficulty: intermediate
concept: []
prerequisites: []
related: []
tags: [学习]
```

---

## 使用建议

1. **首次使用**：先运行 `--dry-run` 查看会修改哪些文件
2. **备份**：在运行前用 Git 提交当前状态
3. **手动调整**：自动添加的 frontmatter 需要根据内容手动补充 concept/prerequisites/related

---

*工具版本: 1.0*
*最后更新: 2026-04-11*
