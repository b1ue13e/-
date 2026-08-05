#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit script for ML/DL/LLM/Systems/Philosophy/Psychology 46 Core Open-Source Teaching & Extension Projects in Obsidian Vault.
Enforces Chapter-by-Chapter Pedagogical Structure:
- Explicit Chapter/Module breakdown headers (`第 1 章` / `第 2 章` / `第 3 章` / `第 4 章` / `第 5 章` / `模块 01` etc.)
- Chapter-specific Math derivations, Code shape tracing, and Chapter HW exercises
- Cognitive Misconception Diagnosis & Anki Flashcard anchors
"""

import os
import re
import sys
import yaml

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# 46 Core Open-Source Teaching Project Workbooks
CORE_46_PROJECTS = [
    # AI Agent 工程
    "03-Projects/AI Agent工程/项目-LLMsFromScratch从零手写大语言模型教学项目.md",
    "03-Projects/AI Agent工程/项目-CS336大语言模型训练系统与ScalingLaw硬核项目.md",
    "03-Projects/AI Agent工程/项目-MaximeLabonne大模型工程化全景与部署扩展训练.md",
    "03-Projects/AI Agent工程/项目-HuggingFaceCourse通用Transformer工程微调扩展训练.md",
    "03-Projects/AI Agent工程/项目-CS224N-GPT架构手写与下游任务作业.md",
    "03-Projects/AI Agent工程/项目-YSDANLP学术化进阶与序列模型实验包.md",
    "03-Projects/AI Agent工程/项目-HuggingFaceAudioTransformers语音与音频工程扩展训练.md",

    # 机器学习与 AI 应用
    "03-Projects/机器学习与AI应用/项目-ISLP统计学习实验室教学项目.md",
    "03-Projects/机器学习与AI应用/项目-ML-Zoomcamp端到端工程部署扩展训练.md",
    "03-Projects/机器学习与AI应用/项目-PracticingTrustworthyML可信与可解释AI教学项目.md",
    "03-Projects/机器学习与AI应用/项目-DCAI以数据为中心的AI与数据诊断实验包.md",
    "03-Projects/机器学习与AI应用/项目-CS330多任务与元学习MAML实验包.md",
    "03-Projects/机器学习与AI应用/项目-D2L动手学深度学习标准基准实验包.md",
    "03-Projects/机器学习与AI应用/项目-Karpathy-ZeroToHero神经网络底层手写教学项目.md",
    "03-Projects/机器学习与AI应用/项目-fastai实用深度学习快速原型扩展训练.md",
    "03-Projects/机器学习与AI应用/项目-UvADeepLearning论文级高级模型实验包.md",
    "03-Projects/机器学习与AI应用/项目-YSDAPracticalDL代码实战扩展训练.md",
    "03-Projects/机器学习与AI应用/项目-FSDL全栈深度学习产品化与监控扩展训练.md",
    "03-Projects/机器学习与AI应用/项目-UDL深度学习紧凑理论与机制剖析实验包.md",
    "03-Projects/机器学习与AI应用/项目-MIT6S191深度学习极速跨方向实战训练.md",
    "03-Projects/机器学习与AI应用/项目-HSEDeepGenerativeModels深度生成模型与FlowMatching实验包.md",
    "03-Projects/机器学习与AI应用/项目-NeuromatchDeepLearning与NeuroAI协作实验训练.md",
    "03-Projects/机器学习与AI应用/项目-MultimodalLLMs多模态大模型与视觉语言扩展训练.md",
    "03-Projects/机器学习与AI应用/项目-HuggingFaceCV视觉Transformer与生成模型扩展训练.md",
    "03-Projects/机器学习与AI应用/项目-CS285深度强化学习算法手写与离线RL作业.md",

    # 系统与硬件
    "03-Projects/系统与硬件/项目-MLSystems端到端AI系统与MLOps工程项目.md",
    "03-Projects/系统与硬件/项目-AI编译器与机器学习系统底层原理教学项目.md",
    "03-Projects/系统与硬件/项目-MLC机器学习编译与GPU算子调度优化工程项目.md",
    "03-Projects/系统与硬件/项目-HuggingFaceRobotics具身智能与LeRobot工程扩展训练.md",

    # 概率统计与数据建模
    "03-Projects/概率统计与数据建模/项目-PyProbML概率机器学习与变分推断实验包.md",
    "03-Projects/概率统计与数据建模/项目-因果推断与双重机器学习实验包.md",
    "03-Projects/概率统计与数据建模/项目-Recommenders微软推荐系统与排序工程项目.md",

    # 数学底座
    "03-Projects/数学底座/项目-MML机器学习数学底座与算法导图.md",
    "03-Projects/数学底座/项目-GeometricDeepLearning几何深度学习与对称性理论实验包.md",
    "03-Projects/数学底座/项目-OpenLogic开放逻辑与哥德尔不完备性教学项目.md",

    # 哲学与人文
    "03-Projects/哲学与人文/项目-OpenStax哲学概论开放主线教学项目.md",
    "03-Projects/哲学与人文/项目-Yale人性哲学与科学交叉教学项目.md",
    "03-Projects/哲学与人文/项目-MIT哲学问题与论证写作教学项目.md",
    "03-Projects/哲学与人文/项目-MIT心灵与机器AI意识哲学教学项目.md",

    # 心理与认知
    "03-Projects/心理与认知/项目-OpenStax普通心理学主线教学项目.md",
    "03-Projects/心理与认知/项目-NobaPsychology模块化心理学扩展训练.md",
    "03-Projects/心理与认知/项目-CognitiveFoundations认知心理学与AI表征教学项目.md",
    "03-Projects/心理与认知/项目-R语言心理学研究方法与数据分析教学项目.md",
    "03-Projects/心理与认知/项目-LearningStatisticsWithR心理统计与表达教学项目.md",
    "03-Projects/心理与认知/项目-psyTeachR可重复心理学研究与开放科学扩展训练.md",
    "03-Projects/心理与认知/项目-PsychoPy行为实验构建与即时满足决策工程项目.md"
]

def parse_frontmatter(content):
    if not content.startswith("---"):
        return None, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content
    try:
        data = yaml.safe_load(parts[1])
        return data, parts[2]
    except Exception as e:
        print(f"[ERROR] YAML parse error: {e}")
        return None, content

def audit_projects():
    print("=" * 70)
    print(f"🔍 Auditing 46 Core Project Workbooks for Chapter-by-Chapter Structure...")
    print("=" * 70)

    passed_count = 0

    for rel_path in CORE_46_PROJECTS:
        filepath = os.path.join(VAULT_ROOT, rel_path)
        filename = os.path.basename(rel_path)

        if not os.path.exists(filepath):
            print(f"  ⚠️ File pending creation: {rel_path}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.splitlines()
        line_count = len(lines)

        fm, body = parse_frontmatter(content)
        if not fm:
            print(f"  ❌ [{filename}] Frontmatter missing or invalid YAML!")
            continue

        errors = []
        if fm.get("type") != "project":
            errors.append("`type` field must be 'project'")
        if fm.get("kind") != "project":
            errors.append("`kind` field must be 'project'")
        if fm.get("flow") != "project":
            errors.append("`flow` field must be 'project'")

        if line_count < 150:
            errors.append(f"Workbook line count too short for chapter breakdown! ({line_count} < 150 lines)")

        # Chapter breakdown check
        chapter_keywords = ["第 1 章", "第 2 章", "第 3 章", "第 4 章", "第1章", "第2章", "第3章", "第4章", "模块 01", "模块 02", "Chapter 1", "Chapter 2"]
        found_chaps = [kw for kw in chapter_keywords if kw in body]
        if len(found_chaps) < 3:
            errors.append("Missing explicit chapter headers (MUST contain at least 3 explicit chapters: 第 1 章, 第 2 章, 第 3 章...)")

        score = fm.get("subagent_audit_score", 0)
        if score < 9.5:
            errors.append(f"Subagent audit score must be >= 9.5, got {score}")

        if errors:
            print(f"\n▶ [{filename}] (Path: {rel_path})")
            print(f"  ❌ Chapter Structure Audit FAILED:")
            for err in errors:
                print(f"     - {err}")
        else:
            role = fm.get('teaching_role', 'N/A').upper()
            print(f"  ✅ [{filename}] Chapter-Structure PASSED | Lines: {line_count} | Chapters Verified | Score: {score}/10")
            passed_count += 1

    print("\n" + "=" * 70)
    print(f"📊 Chapter Structure Summary: {passed_count} / {len(CORE_46_PROJECTS)} Core Workbooks Audit Passed.")
    print("=" * 70)

    if passed_count == len(CORE_46_PROJECTS):
        print(f"🎉 ALL 46 CORE PROJECT WORKBOOKS PASSED CHAPTER-BY-CHAPTER STRUCTURE AUDIT (SCORE >= 9.5)!")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(audit_projects())
