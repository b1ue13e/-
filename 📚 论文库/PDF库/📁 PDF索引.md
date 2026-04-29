---
tags: [PDF, 论文]
created: 2026-04-11
type: index
topic: "PDF库"
status: active
---

# 📁 PDF库

> 存储所有PDF格式的学术论文

---

## 📊 文件统计

```dataviewjs
const pdfFolder = app.vault.getAbstractFileByPath("📚 论文库/PDF库");
if (pdfFolder && pdfFolder.children) {
    const pdfFiles = pdfFolder.children.filter(f => f.extension === "pdf");
    const totalSize = pdfFiles.reduce((sum, f) => sum + f.stat.size, 0);
    const sizeMB = (totalSize / 1024 / 1024).toFixed(2);
    
    dv.paragraph(`📄 文件数量：**${pdfFiles.length}**`);
    dv.paragraph(`💾 总大小：**${sizeMB}** MB`);
}
```

---

## 📄 文件列表

```dataviewjs
const pdfFolder = app.vault.getAbstractFileByPath("📚 论文库/PDF库");
if (pdfFolder && pdfFolder.children) {
    const pdfFiles = pdfFolder.children
        .filter(f => f.extension === "pdf")
        .sort((a, b) => a.name.localeCompare(b.name));
    
    dv.table(
        ["文件名", "大小(MB)", "链接"],
        pdfFiles.map(f => [
            f.name,
            (f.stat.size / 1024 / 1024).toFixed(2),
            "[[" + f.path + "|打开]]"
        ])
    );
}
```

---

## 📝 如何添加新论文

1. 将PDF文件放入此文件夹
2. 创建论文笔记（使用 [[📄 论文笔记模板]]）
3. 在笔记中链接对应的PDF文件

---

*[[📚 论文库/📄 论文主页|返回论文主页]] | [[🏠 主页|返回主页]]*
