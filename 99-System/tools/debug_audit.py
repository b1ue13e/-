import os

VAULT_ROOT = os.path.abspath("F:\\-\\")

rel_path = "03-Projects/机器学习与AI应用/项目-Karpathy-ZeroToHero神经网络底层手写教学项目.md"
filepath = os.path.join(VAULT_ROOT, rel_path)

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

parts = content.split("---", 2)
if len(parts) >= 3:
    body = parts[2]
else:
    body = content

chapter_keywords = ["第 1 章", "第 2 章", "第 3 章", "第 4 章", "第1章", "第2章", "第3章", "第4章", "模块 01", "模块 02", "Chapter 1", "Chapter 2"]

found_chaps = [kw for kw in chapter_keywords if kw in body]
print(f"File: {filepath}")
print(f"Exists: {os.path.exists(filepath)}")
print(f"Found chaps length: {len(found_chaps)}")
print(f"Found chaps: {found_chaps}")
