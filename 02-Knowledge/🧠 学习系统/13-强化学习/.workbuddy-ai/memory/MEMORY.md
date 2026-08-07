# 强化学习课程仓库 · 长期记忆（可复用约定与坑）

## 仓库路径与工具约定
- 库根实际是 `F:\-`（横杠目录），不是 `F:\`。bash `cd` 带 emoji 路径（如 `🧠 学习系统`）会失败 → 文件读写一律用 Python（managed python 3.13.12），避免 shell + emoji 路径。
- 知识卡目录：`F:\-\02-Knowledge\🧠 学习系统\13-强化学习\<阶段子目录>\`；作业目录：`F:\-\03-Projects\13-强化学习\`。

## 知识卡派生视图（Dataview）规范 — 必记
- 「学完后可以完成」反向查作业（作业 `requires` 指向本卡）：
  `FROM "03-Projects" WHERE contains(requires, this.file.link)`
- 「相关下游知识」反向查卡（其他卡 `upstream` 指向本卡）：
  `FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)`
- **失效写法（必须批量替换）**：`FROM [[]]`（空链接，解析为空，作业挂不上）。历史上 213 张卡曾因此失效，已统一修复。
- 作业 `requires` 字段必须用 `[[wikilink]]` 列表（非纯字符串），Dataview `contains(requires, this.file.link)` 才能匹配 Link 对象。

## Emoji code point 坑（严重）
- 知识库文件夹 emoji `🧠` = **U+1F9E0**（脑）。**不是** U+1F4A0（💠 钻石）。
- 任何脚本写入 `02-Knowledge/🧠 学习系统` 等 emoji 路径时，必须核对 code point；曾误用 U+1F4A0 导致 213 处路径失效，复跑 emoji 计数才发现。同理正文注入数组/矩阵例子用单括号 `A=[...]` 或代码块，绝不用 `[[...]]`（会被当 wikilink 死链）。

## 校验器（C:\Users\DELL\，可迁移 skill《obsidian-course-rl-rebuild》）
- `rl_preflight.py`：兼容校验器（官方 preflight 本环境不可用），扫 type:study 的 PLACEHOLDER/字段缺失/upstream 死链/结构项。
- `rl_critical_audit.py`：严苛诊断（body 死链/孤儿卡/薄卡/手算无数字）。
- 批量生成/修复脚本 `rl_author_b*.py`、`rl_migrate_upstream.py`、`rl_fix_*`。
- 注意：preflight 仅扫 `type: study`；`type: concept/reference` 不被扫。
