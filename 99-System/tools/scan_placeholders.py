import os
import glob

# Find all markdown files under current directory (excluding .git)
all_md = []
for root, dirs, files in os.walk('.'):
    if '.git' in root.split(os.sep):
        continue
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            all_md.append(path)

# Check size and content
empty_files = []
very_small = []  # < 100 bytes
small = []       # < 300 bytes

for path in all_md:
    try:
        size = os.path.getsize(path)
        if size == 0:
            empty_files.append(path)
        elif size < 100:
            very_small.append((path, size))
        elif size < 300:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            small.append((path, size, content))
    except Exception as e:
        pass

print("=== 空文件 (0字节) ===")
for p in empty_files:
    print(p)

print("\n=== 极小文件 (< 100字节) ===")
for p, s in very_small:
    print(f"{s:>5} bytes | {p}")
    try:
        with open(p, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        print(f"  内容: {repr(content[:200])}")
    except:
        pass

print("\n=== 小文件 (100-300字节) ===")
for p, s, content in small:
    print(f"{s:>5} bytes | {p}")
    print(f"  内容前200字: {repr(content[:200])}")

print(f"\n总计: {len(empty_files)} 空文件, {len(very_small)} 极小文件, {len(small)} 小文件")
print(f"总md文件数: {len(all_md)}")
