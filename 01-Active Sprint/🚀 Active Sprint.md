---
type: index
cssclasses: [atlas-page, atlas-index]
topic: "Active Sprint"
created: 2026-07-27
updated: 2026-08-02
status: active
flow: sprint
kind: moc
tags: [Sprint, 工作流, 索引]
---

# 🚀 Active Sprint

> 全库唯一当前控制面板。日期只是目标节奏，**掌握闸门决定真实进度**。

## 🎯 当前指针

| 项目 | 当前值 |
|:---|:---|
| 主攻学科 | **量化金融** |
| Sprint | [[2026-Sprint1-量化金融冲刺计划]] |
| 本周 | [[2026-W31 周计划]] |
| 今日 | [[2026-08-02 周日 日计划]] |
| 唯一行动入口 | **[[🗺️ 量化金融学习路径|量化金融学习路径]]** |
| 当前知识点 | **[[收益率与对数收益率|K01 收益率与对数收益率]]** |
| 当前阶段作业 | **[[A01-数据协议与无泄漏审计]]** |
| 项目总看板 | [[00-Qlib项目总看板]] |
| PoW | [[Quant-Factor-And-Arbitrage-Engine]] |

> [!important] 今日决策
> 当前路线仍停在 K01。日历已到 Day 7，但不需要追赶；K01 闭卷、手算、代码和证据全部通过后才解锁 K02。

## ✅ 唯一任务源守卫

```dataviewjs
const sources = dv.pages()
  .where(p => p.sprint === "current" && p.source_of_truth === true && !p.template)
  .array();

if (sources.length === 1) {
  dv.paragraph(`✅ 当前唯一任务源：${sources[0].file.link}`);
} else {
  dv.paragraph(`❌ 检测到 ${sources.length} 个 source_of_truth；必须修正为 1 个。`);
  dv.table(["任务源", "Sprint ID", "路径"], sources.map(p => [p.file.link, p.sprint_id ?? "未填写", p.file.folder]));
}
```

## 🧭 执行链

1. 打开 [[🗺️ 量化金融学习路径|量化金融学习路径]]，只看“现在做什么”。
2. 按学习路径中的对应 Week 完成当前 K，不从全栈知识地图随机选题。
3. 把手算、代码、测试或审计证据写入对应 A 作业页。
4. 闭卷验收通过后，在 [[00-Qlib项目总看板]] 更新状态，再解锁下一个 K。
5. `Again` 卡点进入 [[04-🔁 Review]]，但不改变当前主攻学科。

## 📌 当前 Sprint 笔记

```dataview
TABLE WITHOUT ID file.link AS "笔记", kind AS "类型", status AS "状态", file.mtime AS "更新"
FROM ""
WHERE flow = "sprint" AND !template AND file.name != "🚀 Active Sprint"
SORT file.mtime DESC
LIMIT 30
```

## 🔄 切换 Sprint

1. 当前 A 作业必须明确标记完成、移交或放弃。
2. `flow: sprint` 笔记归为 `knowledge / project / review`。
3. 更新本页当前指针和唯一任务源。
4. 运行 `python 99-System/tools/sync_current_sprint.py` 同步派生日/周视图。
