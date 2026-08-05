---
type: index
topic: "Inbox"
created: 2026-08-01
updated: 2026-08-01
status: active
flow: inbox
kind: moc
tags: [Inbox, 工作流, 索引]
---

# 📥 Inbox

> 这里只负责快速收集和分流，不长期堆放正式知识卡。

## ⚡ 30 秒处理流程

1. 用 [[99-System/📇 模板/📓 快速笔记模板|快速笔记模板]] 捕捉。
2. 24 小时内补全 `type`、`topic`、`flow`。
3. 按用途改为 `sprint / knowledge / project / review`，或直接删除。
4. 不为了“清空 Inbox”移动源文件；工作身份由 `flow` 决定。

## 📥 待处理收集

```dataviewjs
const current = dv.current().file.path;
const now = dv.luxon.DateTime.now();
const pages = dv.pages()
  .where(p => p.flow === "inbox" && !p.template && p.file.path !== current)
  .array()
  .sort((a, b) => (a.file.ctime?.ts ?? 0) - (b.file.ctime?.ts ?? 0));

if (pages.length === 0) {
  dv.paragraph("✅ 当前没有标记为 `flow: inbox` 的收集项。");
} else {
  dv.table(
    ["收集项", "主题", "已停留", "下一步"],
    pages.map(p => {
      const created = p.created ? dv.date(p.created) : p.file.ctime;
      const hours = created ? Math.max(0, Math.floor((now.toMillis() - created.toMillis()) / 3600000)) : null;
      return [p.file.link, p.topic ?? "未填写", hours === null ? "-" : `${hours}h`, "归区或删除"];
    })
  );
}
```

## 🧯 恢复待确认（隔离区）

> [!warning]
> `恢复待确认/` 是 2026-07-31 重构留下的恢复产物，不等于正常 Inbox。确认内容和去向前不要批量删除。

```dataview
TABLE WITHOUT ID file.link AS "恢复文件", file.mtime AS "最后修改"
FROM "00-Inbox/恢复待确认"
SORT file.name ASC
```

## 🔗 相关入口

- [[01-Active Sprint/🚀 Active Sprint|Active Sprint]]
- [[02-Knowledge/02-🧠 Knowledge|Knowledge]]
- [[03-Projects/03-🛠️ Projects|Projects]]
- [[04-Review/04-🔁 Review|Review]]

