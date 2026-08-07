import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

COURSE_DIR = Path(r"F:\-\02-Knowledge\🧠 学习系统\06-常微分方程")

MOC_DATA = [
    {
        "dir": "00-前置知识",
        "file": "🧭 常微分方程-前置知识.md",
        "topic": "常微分方程-前置知识",
        "title": "🔧 前置知识准备",
        "desc": "掌握进入常微分方程课程的必要基础知识与工具能力。",
        "prev": None,
        "next": "[[02-Knowledge/🧠 学习系统/06-常微分方程/01-一阶基石与数值启蒙/🧭 阶段1-一阶基石与数值启蒙|进入第一阶段]]"
    },
    {
        "dir": "01-一阶基石与数值启蒙",
        "file": "🧭 阶段1-一阶基石与数值启蒙.md",
        "topic": "第一阶段：一阶基石与数值启蒙",
        "title": "📘 第一阶段：一阶基石与数值启蒙",
        "desc": "从最基本的概念出发，掌握一阶方程的初等解法及数值启蒙。",
        "prev": "[[02-Knowledge/🧠 学习系统/06-常微分方程/00-前置知识/🧭 常微分方程-前置知识|返回前置]]",
        "next": "[[02-Knowledge/🧠 学习系统/06-常微分方程/02-二阶方程与解析底盘/🧭 阶段2-二阶方程与解析底盘|进入第二阶段]]"
    },
    {
        "dir": "02-二阶方程与解析底盘",
        "file": "🧭 阶段2-二阶方程与解析底盘.md",
        "topic": "第二阶段：二阶方程与解析底盘",
        "title": "📗 第二阶段：二阶方程与解析底盘",
        "desc": "进入线性ODE的核心领域，掌握二阶线性方程的求解与系统性质。",
        "prev": "[[02-Knowledge/🧠 学习系统/06-常微分方程/01-一阶基石与数值启蒙/🧭 阶段1-一阶基石与数值启蒙|返回第一阶段]]",
        "next": "[[02-Knowledge/🧠 学习系统/06-常微分方程/03-多维线性系统与矩阵指数/🧭 阶段3-多维线性系统与矩阵指数|进入第三阶段]]"
    },
    {
        "dir": "03-多维线性系统与矩阵指数",
        "file": "🧭 阶段3-多维线性系统与矩阵指数.md",
        "topic": "第三阶段：多维线性系统与矩阵指数",
        "title": "📙 第三阶段：多维线性系统与矩阵指数",
        "desc": "将一维拓展到高维空间，利用线性代数与矩阵指数解决线性系统。",
        "prev": "[[02-Knowledge/🧠 学习系统/06-常微分方程/02-二阶方程与解析底盘/🧭 阶段2-二阶方程与解析底盘|返回第二阶段]]",
        "next": "[[02-Knowledge/🧠 学习系统/06-常微分方程/04-拉普拉斯与傅里叶频域/🧭 阶段4-拉普拉斯与傅里叶频域|进入第四阶段]]"
    },
    {
        "dir": "04-拉普拉斯与傅里叶频域",
        "file": "🧭 阶段4-拉普拉斯与傅里叶频域.md",
        "topic": "第四阶段：拉普拉斯与傅里叶频域",
        "title": "📕 第四阶段：拉普拉斯与傅里叶频域",
        "desc": "跳出时域，运用积分变换在频域降维打击复杂的线性系统。",
        "prev": "[[02-Knowledge/🧠 学习系统/06-常微分方程/03-多维线性系统与矩阵指数/🧭 阶段3-多维线性系统与矩阵指数|返回第三阶段]]",
        "next": "[[02-Knowledge/🧠 学习系统/06-常微分方程/05-现代非线性动力系统/🧭 阶段5-现代非线性动力系统|进入第五阶段]]"
    },
    {
        "dir": "05-现代非线性动力系统",
        "file": "🧭 阶段5-现代非线性动力系统.md",
        "topic": "第五阶段：现代非线性动力系统",
        "title": "🟣 第五阶段：现代非线性动力系统",
        "desc": "抛开解析解的执念，从全局定性视角俯瞰系统的演化和稳定。",
        "prev": "[[02-Knowledge/🧠 学习系统/06-常微分方程/04-拉普拉斯与傅里叶频域/🧭 阶段4-拉普拉斯与傅里叶频域|返回第四阶段]]",
        "next": "[[02-Knowledge/🧠 学习系统/06-常微分方程/06-PDE桥梁与高级解析/🧭 阶段6-PDE桥梁与高级解析|进入第六阶段]]"
    },
    {
        "dir": "06-PDE桥梁与高级解析",
        "file": "🧭 阶段6-PDE桥梁与高级解析.md",
        "topic": "第六阶段：PDE桥梁与高级解析",
        "title": "🟤 第六阶段：PDE桥梁与高级解析",
        "desc": "通过级数解与特征值问题，搭建通往偏微分方程(PDE)的桥梁。",
        "prev": "[[02-Knowledge/🧠 学习系统/06-常微分方程/05-现代非线性动力系统/🧭 阶段5-现代非线性动力系统|返回第五阶段]]",
        "next": "[[02-Knowledge/🧠 学习系统/06-常微分方程/07-精通与专题/🧭 阶段7-精通与专题|进入第七阶段]]"
    },
    {
        "dir": "07-精通与专题",
        "file": "🧭 阶段7-精通与专题.md",
        "topic": "第七阶段：精通与专题",
        "title": "⚫ 第七阶段：精通与专题",
        "desc": "接触最前沿与最底层的专题：变分方程、伴随灵敏度、随机与神经ODE。",
        "prev": "[[02-Knowledge/🧠 学习系统/06-常微分方程/06-PDE桥梁与高级解析/🧭 阶段6-PDE桥梁与高级解析|返回第六阶段]]",
        "next": "无"
    }
]

TEMPLATE = """---
type: stage
topic: "{topic}"
tags:
- 常微分方程
- 阶段MOC
created: 2026-08-06
status: active
course: 常微分方程
flow: knowledge
kind: moc
---

# {title}

> "{desc}"

---

## 📊 阶段目标与说明

本阶段汇集了相关的核心知识卡片。请按顺序学习以下概念。

## 📚 知识卡片清单

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/06-常微分方程/{dir}"
WHERE stage_moc = this.file.link AND file.name != this.file.name
SORT file.name ASC
```

---

## 🧪 阶段验收与作业

本阶段的所有可用作业清单如下，完成后可开启下一阶段。

```dataview
LIST
FROM "03-Projects/06-常微分方程"
WHERE contains(requires, this.file.link) OR (
  file.folder != null AND 
  contains(file.folder, "03-Projects") AND 
  stage_id != null AND 
  stage_id == "{stage_id}"
)
SORT assignment_level ASC, file.name ASC
```

---

## 🔗 阶段导航

| ⬅️ 上一阶段 | 📋 总览 | 下一阶段 ➡️ |
|:---:|:---:|:---:|
| {prev} | [[02-Knowledge/🧠 学习系统/06-常微分方程/🗺️ 常微分方程学习路径|返回总览]] | {next} |

"""

def main():
    for item in MOC_DATA:
        moc_path = COURSE_DIR / item["dir"] / item["file"]
        stage_id = "".join(filter(str.isdigit, item["dir"].split("-")[0]))
        if not stage_id:
            stage_id = "00"
            
        content = TEMPLATE.format(
            topic=item["topic"],
            title=item["title"],
            desc=item["desc"],
            dir=item["dir"],
            prev=item["prev"] if item["prev"] else "无",
            next=item["next"],
            stage_id=stage_id
        )
        
        # Write to file
        moc_path.parent.mkdir(parents=True, exist_ok=True)
        moc_path.write_text(content, encoding="utf-8")
        print(f"Rebuilt MOC: {item['file']}")

if __name__ == "__main__":
    main()
