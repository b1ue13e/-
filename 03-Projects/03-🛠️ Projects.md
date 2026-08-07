---
title: "Projects"
type: index
topic: "Projects"
created: 2026-07-27
updated: 2026-08-01
status: active
flow: project
kind: moc
tags: [项目, 实战, 作业, 索引]
---

# 🛠️ Projects

## 课程作业与验收

- [[33门课程完整作业包索引]]
- [[33门课程正式作业索引]]
- [[33门课程作业来源审计总表]]
- [[33门课程完整作业编目审计-2026-07-28|33门课程完整作业编目审计]]
- [[正式作业包修复审计-2026-07-28|正式作业包修复审计]]
- [[旧项目与作业资产资格审计-2026-07-28|旧项目与作业资产资格审计]]
- [[33门课程开源自学与验收总索引|课程执行总索引]]

## 🎯 活跃项目

```dataview
TABLE WITHOUT ID file.link AS "项目", project_type AS "类型", progress AS "进度", focus AS "焦点", deadline AS "截止"
FROM "03-Projects"
WHERE type = "project" AND !template AND (status = "active" OR status = "ongoing")
SORT choice(focus = "now", 0, choice(focus = "next", 1, 2)) ASC, deadline ASC
LIMIT 20
```

- 新建项目：[[📁 项目模板|项目模板]]
- 当前 Sprint：[[🚀 Active Sprint|Active Sprint]]

## 当前项目目录

- `AI Agent工程/`
- `哲学与人文/`
- `心理与认知/`
- `数学底座/`
- `机器学习与AI应用/`
- `概率统计与数据建模/`
- `系统与硬件/`
- `金融与时序/`
- `通用项目/`

> 项目源文件按领域组织；工作身份仍由 `flow: project` 和 `focus` 决定。
