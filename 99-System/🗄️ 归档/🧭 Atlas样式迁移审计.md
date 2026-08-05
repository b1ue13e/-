---
type: audit
cssclasses:
  - atlas-page
  - atlas-index
topic: "Atlas样式迁移审计"
created: 2026-06-13
updated: 2026-06-13
status: active
up:
  - "[[🏠 Atlas主页]]"
related:
  - "[[🏠 主页]]"
  - "[[📚 书架画廊]]"
tags: [审计, Atlas, 样式治理]
---

# 🧭 Atlas样式迁移审计

> 这页用来检查全库是否已经进入 Atlas 样式体系：看类型分布、样式类覆盖、缺失元数据、主页入口坏链和最近更新。

---

## 样式覆盖总览

```dataviewjs
const pages = dv.pages().where(p => p.file.path !== "AGENTS.md");
const typeOrder = ["study", "index", "stage", "project", "book", "paper", "journal", "question", "prompt", "template", "audit"];

function cssList(p) {
  if (Array.isArray(p.cssclasses)) return p.cssclasses;
  if (typeof p.cssclasses === "string") return [p.cssclasses];
  if (typeof p.cssclass === "string") return [p.cssclass];
  return [];
}

const rows = typeOrder
  .map(type => {
    const group = pages.where(p => p.type === type);
    const covered = group.where(p => cssList(p).includes("atlas-page")).length;
    return [type, group.length, covered, group.length ? Math.round(covered / group.length * 100) + "%" : "-"];
  })
  .filter(row => row[1] > 0);

dv.table(["类型", "页面数", "Atlas覆盖", "覆盖率"], rows);
```

## 剩余未迁移页面

主迁移口径：普通 Markdown 页面需要同时具备 `type` 和 `cssclasses: [atlas-page, ...]`。`AGENTS.md` 是给 AI 助手看的项目说明，不纳入 Atlas 页面迁移。

```dataviewjs
const ignored = new Set(["AGENTS.md"]);

function cssList(p) {
  if (Array.isArray(p.cssclasses)) return p.cssclasses;
  if (typeof p.cssclasses === "string") return [p.cssclasses];
  if (typeof p.cssclass === "string") return [p.cssclass];
  return [];
}

const rows = dv.pages()
  .where(p => !ignored.has(p.file.path))
  .where(p => !p.type || !cssList(p).includes("atlas-page"))
  .sort(p => p.file.mtime, "desc")
  .map(p => [
    p.file.link,
    p.type || "缺 type",
    cssList(p).join(", ") || "缺 cssclasses",
    p.file.mtime.toFormat("yyyy-MM-dd")
  ]);

if (rows.length) {
  dv.table(["页面", "类型", "样式类", "更新时间"], rows.slice(0, 80));
} else {
  dv.paragraph("当前主迁移已完成：除 AGENTS.md 外，未发现缺 type 或缺 atlas-page 的 Markdown 页面。");
}
```

## 类型专属样式缺口

这些页面已经进入 Atlas 主样式，但还缺少与 `type` 对应的细分样式类，例如 `type: study` 应配 `atlas-study`。

```dataviewjs
const expected = {
  study: "atlas-study",
  index: "atlas-index",
  audit: "atlas-index",
  stage: "atlas-stage",
  project: "atlas-project",
  book: "atlas-book",
  paper: "atlas-paper",
  journal: "atlas-journal",
  question: "atlas-question",
  prompt: "atlas-prompt",
  template: "atlas-template"
};

function cssList(p) {
  if (Array.isArray(p.cssclasses)) return p.cssclasses;
  if (typeof p.cssclasses === "string") return [p.cssclasses];
  if (typeof p.cssclass === "string") return [p.cssclass];
  return [];
}

const rows = dv.pages()
  .where(p => p.file.path !== "AGENTS.md" && expected[p.type])
  .where(p => !cssList(p).includes(expected[p.type]))
  .sort(p => p.file.mtime, "desc")
  .map(p => [
    p.file.link,
    p.type,
    expected[p.type],
    cssList(p).join(", ") || "缺 cssclasses"
  ]);

if (rows.length) {
  dv.table(["页面", "类型", "应补样式", "当前样式"], rows.slice(0, 80));
} else {
  dv.paragraph("当前未发现类型专属样式缺口。");
}
```

## Atlas 主页入口检查

```dataviewjs
const source = "🏠 Atlas主页.md";
const text = await dv.io.load(source);
const htmlTargets = [...new Set([...text.matchAll(/data-href="([^"]+)"/g)].map(m => m[1]))];
const brokenHtml = htmlTargets
  .map(target => {
    const dest = app.metadataCache.getFirstLinkpathDest(target, source);
    return [target, dest ? dest.path : ""];
  })
  .filter(row => !row[1]);

if (brokenHtml.length) {
  dv.header(3, "HTML data-href 未解析");
  dv.table(["目标", "解析结果"], brokenHtml.map(row => [row[0], "未找到页面"]));
} else {
  dv.paragraph("🏠 Atlas主页.md 的 HTML data-href 当前全部可解析。");
}

const unresolved = app.metadataCache.unresolvedLinks[source] || {};
const unresolvedRows = Object.entries(unresolved)
  .filter(([target]) => !target.includes("${"))
  .map(([target, count]) => [target, count]);

if (unresolvedRows.length) {
  dv.header(3, "Wiki 链接未解析");
  dv.table(["目标", "引用次数"], unresolvedRows);
} else {
  dv.paragraph("🏠 Atlas主页.md 的普通 wiki 链接当前未发现未解析项。");
}
```

## 待收尾事项

- `🏠 Atlas主页.md` 顶部 HTML 入口已改为具体页面目标，不再指向 `周计划/`、`月计划/` 目录。
- 旧年度规划入口已从 Atlas 主页移除，改为当前仍存在的 `计划系统导航`、`季度学习计划总索引`、`Q1 季度计划`、`2026-W24 周计划` 和 `2026-06 月计划`。
- `AGENTS.md` 仍不迁移为 Atlas 页面；它是仓库协作说明，不属于 Obsidian 导航页。
- 后续新增页面只要出现在上方两个缺口表，就按 `type` 补齐对应 `atlas-*` 样式类。

## 原始缺口查询

```dataview
TABLE type AS "类型", cssclasses AS "样式类", file.mtime AS "更新时间"
WHERE file.name != "AGENTS"
  AND (!type OR !contains(cssclasses, "atlas-page"))
SORT file.mtime DESC
LIMIT 50
```

## 最近更新

```dataview
TABLE type AS "类型", status AS "状态", file.mtime AS "更新时间"
WHERE contains(cssclasses, "atlas-page")
SORT file.mtime DESC
LIMIT 30
```

## 样式规则

- `type: study` 使用 `atlas-study`，适合原子学习卡。
- `type: index` 与 `type: audit` 使用 `atlas-index`，适合导航、索引和看板。
- `type: stage` 使用 `atlas-stage`，适合路径阶段页。
- `type: project` 使用 `atlas-project`，适合项目与实践页。
- `type: book`、`type: paper`、`type: journal` 分别使用对应阅读、论文、周期笔记样式。
