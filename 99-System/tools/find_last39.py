import os

vault_dir = r'f:\-\02-Knowledge\🧠 学习系统'

# 深度捕获剩余 39 篇尚处于轻量规范卡或简单结构卡片的模式
target_patterns = [
    '核心原理解析与代码',
    '是线性表与基本数据结构中的核心组成部分',
    '标准操作逻辑',
    '概念验证',
    '为数据结构与算法的核心标准组件',
    '是体系中的核心组成部分',
    '属于计算机科学中数据结构与算法的核心标准组件'
]

matching_files = []

for root, dirs, files in os.walk(vault_dir):
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # 判断是否包含特定简易标记且无深度展开
                for p in target_patterns:
                    if p in content:
                        title = f.replace('.md', '')
                        rel_path = os.path.relpath(fp, vault_dir)
                        matching_files.append((fp, title, rel_path, p))
                        break
            except Exception as e:
                pass

print(f"Exact matching files found by last39 scanner: {len(matching_files)}")

with open(r'f:\-\99-System\tools\last39_list.txt', 'w', encoding='utf-8') as out:
    out.write(f"Total matching files found: {len(matching_files)}\n\n")
    for fp, title, rel, p in matching_files:
        out.write(f"{title}  <--  {rel}\n")

print("Saved last 39 list to last39_list.txt")
