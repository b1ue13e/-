---
type: index
topic: "Review"
created: 2026-08-01
updated: 2026-08-01
status: active
flow: review
kind: moc
tags: [复习, 弱点, Anki, 索引]
---

# 🔁 Review

> FSRS 调度只交给 Anki 26.05。本页负责找到薄弱点、回到原笔记修复，不在 Obsidian 里建第二套调度。

## 🧯 知识质量治理

- 当前修复队列：[[知识质量修复队列]]。
- 修复顺序固定为：结构损坏 → 高入链主卡 → 有正文但缺来源 → 低价值卡退役复核。
- 每轮只处理少量 canonical 主卡；禁止为了提高总分批量灌入模板正文。
- 最新极严审计保存在 `99-System/🗄️ 归档/知识库审计/`，评分明细不作为日常导航页。

## 🧠 薄弱点队列

```dataviewjs
const current = dv.current().file.path;
const pages = dv.pages()
  .where(p => !p.template && p.file.path !== current && (p.flow === "review" || p.weak === true))
  .array()
  .sort((a, b) => {
    const da = a.weak_since ? dv.date(a.weak_since)?.ts ?? 0 : 0;
    const db = b.weak_since ? dv.date(b.weak_since)?.ts ?? 0 : 0;
    return da - db;
  });

if (pages.length === 0) {
  dv.paragraph("✅ 当前没有记录中的薄弱点。");
} else {
  dv.table(
    ["原笔记", "薄弱开始", "状态", "修复动作"],
    pages.map(p => [p.file.link, p.weak_since ?? "未记录", p.status ?? "-", "重讲 → 重做 → 重测"])
  );
}
```

## 🃏 Anki 制卡候选

```dataview
TABLE WITHOUT ID file.link AS "原笔记", anki_deck AS "Deck", anki_tags AS "Tags"
FROM ""
WHERE anki_deck AND !template
SORT file.mtime DESC
LIMIT 30
```

## ✅ Again 后的固定动作

1. 在原笔记设置 `flow: review`、`weak: true`、`weak_since: YYYY-MM-DD`。
2. 补一段“为什么会错”，不只抄正确答案。
3. 完成一次无提示回忆和一次变式练习。
4. 验收通过后改回 `flow: knowledge` 或 `flow: sprint`，并清除 `weak`。

## 🛠️ 工具与模板

- 错题笔记：[[🧯 错题漏洞笔记模板|错题漏洞笔记模板]]
- 制卡区要求：原笔记中保留 `## 🃏 Anki 卡片`
- 导出脚本：`python 99-System/tools/export_anki_cards.py`
- 恢复/审计日志只是系统记录，没有 `flow: review` 时不进入本队列。

## 🔗 相关入口

- [[🚀 Active Sprint|Active Sprint]]
- [[02-🧠 Knowledge|Knowledge]]
- [[03-🛠️ Projects|Projects]]
