---
type: index
topic: "Knowledge"
created: 2026-08-01
updated: 2026-08-01
status: active
flow: knowledge
kind: moc
tags: [知识, 工作流, 索引]
---

# 🧠 Knowledge

> 跨 33 条学习路径的知识资产总入口。物理位置可以保持不变，`flow: knowledge` 表示当前工作身份。

## 🧭 高频入口

| 任务 | 入口 |
|:--|:--|
| 选学科 | [[🧭 学科分组导航|学科分组导航]] |
| 进具体路径 | [[🎓 学习入口|学习入口]] |
| 按概念查找 | [[🔍 概念自动索引|概念自动索引]] |
| 查前置与依赖 | [[🕸️ 知识依赖图谱|知识依赖图谱]] |
| 按标签筛选 | [[🏷️ 标签云索引|标签云索引]] |
| 找跨路径联系 | [[🔀 知识连接索引|知识连接索引]] |

## 📊 五类知识资产

```dataviewjs
const current = dv.current().file.path;
const labels = {
  moc: "MOC",
  concept: "概念",
  derivation: "推导",
  "problem-type": "题型",
  mistake: "错题"
};
const pages = dv.pages()
  .where(p => p.flow === "knowledge" && !p.template && p.file.path !== current)
  .array();

dv.table(
  ["资产类型", "数量"],
  Object.entries(labels).map(([kind, label]) => [label, pages.filter(p => (p.kind ?? p.note_role) === kind).length])
);

const recent = pages
  .sort((a, b) => (b.file.mtime?.ts ?? 0) - (a.file.mtime?.ts ?? 0))
  .slice(0, 20);

if (recent.length > 0) {
  dv.header(3, "最近更新");
  dv.table(
    ["笔记", "类型", "状态", "更新"],
    recent.map(p => [p.file.link, labels[p.kind ?? p.note_role] ?? p.kind ?? p.note_role ?? "未分类", p.status ?? "-", p.file.mtime])
  );
} else {
  dv.paragraph("尚无标记为 `flow: knowledge` 的知识卡；旧笔记仍可通过上方自动索引访问。");
}
```

## ✍️ 新建规则

- 主题卡优先，不拆分仅有一个小问题的碎片卡。
- `concept` 只填 1–3 个稳定上位概念。
- 独立公式、流程、代码实现、题型或反复引用的内容才单独成卡。
- 模板统一从 [[📇 模板索引|模板索引]] 使用。
