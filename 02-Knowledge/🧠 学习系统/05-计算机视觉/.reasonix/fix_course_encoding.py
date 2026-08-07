#!/usr/bin/env python3
"""Diagnose and fix the 'course' field encoding issue in knowledge cards.
Inspects raw bytes to understand the exact encoding corruption,
then fixes it by reading as UTF-8, detecting the mojibake pattern,
and rewriting correctly.
"""
import os
import re

BASE = r"F:\-\02-Knowledge\🧠 学习系统\05-计算机视觉"
SKIP_DIRS = {'.归档', '.reasonix', '.pytest_cache', '__pycache__', '.git'}

# The corrupted "05-计算机视觉" appears as "05-璁＄畻鏈鸿�瑙�"
# This is UTF-8 bytes being decoded as if they were Latin-1
# The UTF-8 for "计算机视觉" is: \xe8\xae\xa1 \xe7\xae\x97 \xe6\x9c\xba \xe8\xa7\x86 \xe8\xa7\x89
# When decoded as Latin-1: è®¡ ç® æœº è§† è§‰
# But the rendered mojibake is: "璁＄畻鏈鸿�瑙�"
# This can happen when UTF-8 bytes are decoded with GBK or similar

CORRECT_COURSE = "05-计算机视觉"


def inspect_file(path):
    """Read raw bytes and show the course line."""
    with open(path, 'rb') as f:
        data = f.read()
    # Find the course line
    idx = data.find(b'\ncourse:')
    if idx == -1:
        idx = data.find(b'course:')
    if idx >= 0:
        end = data.find(b'\n', idx + 1)
        if end == -1:
            end = len(data)
        line = data[idx:end]
        print(f"  Raw bytes: {line[:120]}")
        # Try to find the correct "计算机视觉" bytes
        correct_bytes = "计算机视觉".encode('utf-8')
        print(f"  Correct '计算机视觉' UTF-8 bytes: {correct_bytes.hex()}")
        # Check if the file contains the correct bytes
        if correct_bytes in data:
            print(f"  -> File ALREADY has correct UTF-8 bytes!")
            return "already_correct"
        else:
            # Check what we see
            # The mojibake "璁＄畻鏈鸿�瑙�" in UTF-8
            mojibake = "璁＄畻鏈鸿�瑙�".encode('utf-8')
            if mojibake in data:
                print(f"  -> Found mojibake '璁＄畻鏈鸿�瑙�' bytes")
                return "mojibake_utf8"
            print(f"  -> Unknown corruption pattern")
            return "unknown"
    return "no_course_field"


def fix_mojibake_utf8(path):
    """Fix: the file contains '05-璁＄畻鏈鸿�瑙�' as actual UTF-8 text."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old = '05-璁＄畻鏈鸿�瑙�'
    if old in content:
        new_content = content.replace(old, CORRECT_COURSE)
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(new_content)
        return True
    return False


def main():
    all_files = []
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith('.md'):
                all_files.append(os.path.join(root, f))
    
    print(f"Scanning {len(all_files)} markdown files...")
    print()
    
    issues = {}
    for path in all_files:
        rel = os.path.relpath(path, BASE)
        result = inspect_file(path)
        if result not in ("already_correct", "no_course_field"):
            issues[path] = result
            print(f"  ISSUE [{result}]: {rel}")
    
    print(f"\nFound {len(issues)} files with corrupted course field.")
    
    if issues:
        print("\nFixing...")
        fixed = 0
        for path, issue_type in issues.items():
            if issue_type == "mojibake_utf8":
                if fix_mojibake_utf8(path):
                    fixed += 1
                    print(f"  Fixed: {os.path.relpath(path, BASE)}")
        print(f"\nFixed: {fixed} files")
        
        # Re-verify
        print("\nRe-verifying...")
        for path in issues:
            result = inspect_file(path)
            rel = os.path.relpath(path, BASE)
            if result == "already_correct":
                print(f"  OK: {rel}")
            else:
                print(f"  STILL BROKEN [{result}]: {rel}")


if __name__ == '__main__':
    main()
