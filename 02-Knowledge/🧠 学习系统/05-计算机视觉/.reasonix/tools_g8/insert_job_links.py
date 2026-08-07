"""为 61 张 study 卡插入『## 学完后可以完成』主动作业清单（规范 §三）。

在『## 🔗 知识图谱』（或文件末尾）前插入章节：
- 显式列出关联作业（完整路径 wikilink）
- 保留 Dataview 派生查询作为反向事实源
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from job_link_map import get_map, JOBS

KB = "F:" + os.sep + "-"
COURSE = KB + os.sep + "02-Knowledge" + os.sep + "🧠 学习系统" + os.sep + "05-计算机视觉"
SKIP = {'.归档', '.reasonix', '.recovery-hold', '.pytest_cache', '__pycache__', '.git', '.obsidian', '.tmp'}

def build_section(card_name):
    m = get_map()
    if card_name in m['required']:
        job_key, desc = m['required'][card_name]
        job_path = JOBS[job_key]
        job_display = job_key
        return f"""## 学完后可以完成

- [[{job_path}|{job_display}]]：{desc}

> 作业入口由 frontmatter `requires` 维护（唯一事实源），下方 Dataview 反向派生当前卡可完成的全部作业。"""
    for group, title in [('hw06', '开放项目'), ('basic', '检索练习'), ('other', '练习与复现')]:
        if card_name in m[group]:
            desc = m[group][card_name]
            return f"""## 学完后可以完成

- {desc}

> 该卡无直接课后/阶段作业：以卡内自测题与闭卷复现作为形成性验收；如需综合实践，可挂靠 HW06 开放课程项目或 CAP01。"""
    return None

def main():
    applied = skipped = 0
    for root, dirs, files in os.walk(COURSE):
        dirs[:] = [x for x in dirs if x not in SKIP]
        for f in files:
            if not f.endswith('.md'):
                continue
            p = os.path.join(root, f)
            with open(p, encoding='utf-8') as fh:
                content = fh.read()
            if 'type: study' not in content:
                continue
            name = f[:-3]
            section = build_section(name)
            if section is None:
                print(f"[无映射] {name}")
                continue
            if '## 学完后可以完成' in content:
                skipped += 1
                continue
            # 在『## 🔗 知识图谱』前插入；若无则在文件末尾前插入
            anchor = '## 🔗 知识图谱'
            if anchor in content:
                content = content.replace(anchor, section + '\n\n' + anchor, 1)
            else:
                content = content.rstrip() + '\n\n' + section + '\n'
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(content)
            applied += 1
    print(f"插入 {applied} 张，跳过（已有）{skipped} 张")

if __name__ == '__main__':
    main()
