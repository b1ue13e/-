import os
import re

base_dir = r'f:\-\02-Knowledge\🧠 学习系统\10-数据结构与算法'
files_to_process = []

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if '在遇到需要频繁操作或计算' in content or '验证 描述 在标准小规模输入下的基本运算' in content or '在解决实际场景中的数据组织或算法设计时' in content:
                        title = f.replace('.md', '')
                        importance = 'B'
                        m_imp = re.search(r'importance:\s*"?([A-E])', content)
                        if m_imp:
                            importance = m_imp.group(1)
                        rel_path = os.path.relpath(fp, base_dir)
                        files_to_process.append((fp, title, importance, rel_path))
            except Exception as e:
                pass

print(f'Total placeholder files: {len(files_to_process)}')

by_stage = {}
for fp, title, imp, rel in files_to_process:
    stage = rel.split(os.sep)[0] if os.sep in rel else 'Root'
    by_stage.setdefault(stage, []).append((title, imp, rel, fp))

with open(r'f:\-\02-Knowledge\🧠 学习系统\10-数据结构与算法\placeholder_report.txt', 'w', encoding='utf-8') as out:
    out.write(f'Total placeholder files: {len(files_to_process)}\n\n')
    for stage, items in sorted(by_stage.items()):
        out.write(f'=== Stage: {stage} ({len(items)} files) ===\n')
        for title, imp, rel, fp in items:
            out.write(f'[{imp}] {title}  <--  {rel}\n')
        out.write('\n')

print("Report saved to placeholder_report.txt successfully.")
