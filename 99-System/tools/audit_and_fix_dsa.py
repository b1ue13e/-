import os
import re

base_dir = r'f:\-\02-Knowledge\🧠 学习系统\10-数据结构与算法'

fixed_count = 0
yaml_fixed = 0
callout_fixed = 0
math_fixed = 0

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                original_content = content
                
                # 1. 修复自测题答案 Callout 格式
                # 匹配各种变形如 > 答案解析、> **答案解析**、> 答案： 转化为标准的 > [!question]- 答案解析
                content = re.sub(r'>\s*\*\*答案解析\*\*', r'> [!question]- 答案解析', content)
                content = re.sub(r'>\s*答案解析', r'> [!question]- 答案解析', content)
                if content != original_content:
                    callout_fixed += 1

                # 2. 检查并确保 Frontmatter 字段完备 (flow, kind, course, date)
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        yaml_text = parts[1]
                        body_text = parts[2]
                        
                        modified_yaml = False
                        if 'course:' not in yaml_text:
                            yaml_text += '\ncourse: 数据结构与算法'
                            modified_yaml = True
                        if 'flow:' not in yaml_text:
                            yaml_text += '\nflow: knowledge'
                            modified_yaml = True
                        if 'kind:' not in yaml_text:
                            yaml_text += '\nkind: concept'
                            modified_yaml = True
                        if 'date:' not in yaml_text:
                            yaml_text += '\ndate: 2026-07-28'
                            modified_yaml = True
                            
                        if modified_yaml:
                            content = '---' + yaml_text + '\n---' + body_text
                            yaml_fixed += 1

                # 3. 检查并替换残留的“标准小规模”等泛套话
                if '验证 描述 在标准小规模输入下的基本运算' in content:
                    title = f.replace('.md', '')
                    content = content.replace('验证 描述 在标准小规模输入下的基本运算', f'验证 {title} 在标准小规模输入下的基本运算与边界条件')
                    fixed_count += 1

                # 写回文件
                if content != original_content:
                    with open(fp, 'w', encoding='utf-8') as file:
                        file.write(content)
                    
            except Exception as e:
                print(f"Error processing {fp}: {e}")

print(f"Audit and Fix Complete!")
print(f"YAML fields fixed: {yaml_fixed}")
print(f"Callouts fixed: {callout_fixed}")
print(f"Text cleanups fixed: {fixed_count}")
