import os

vault_dir = r'f:\-\02-Knowledge\🧠 学习系统'

matching_files = []

for root, dirs, files in os.walk(vault_dir):
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # 更通用的模板特征判断：
                # 1. 包含通用占位例题或描述
                # 2. 正文过于简短/属于批量生成的通用内容
                is_template = False
                if '属于计算机科学中数据结构与算法的核心标准组件' in content or '标准操作逻辑' in content or '处理逻辑' in content or '示例转移逻辑' in content or '概念验证' in content or '作为基础工具组件' in content:
                    is_template = True
                
                if is_template:
                    title = f.replace('.md', '')
                    rel_path = os.path.relpath(fp, vault_dir)
                    matching_files.append((fp, title, rel_path))
            except Exception as e:
                pass

print(f"Total template files found by refined scanner: {len(matching_files)}")

with open(r'f:\-\99-System\tools\exact_68_list.txt', 'w', encoding='utf-8') as out:
    out.write(f"Total template files found by refined scanner: {len(matching_files)}\n\n")
    for fp, title, rel in matching_files:
        out.write(f"{title}  <--  {rel}\n")

print("Saved exact list to exact_68_list.txt")
