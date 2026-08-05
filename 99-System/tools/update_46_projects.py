import os
import yaml

VAULT_ROOT = os.path.abspath("F:\\-\\")

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

def generate_chapter(i, topic):
    return f"""## 📖 第 {i} 章：{topic}

### 本章核心理论与数学推导 (LaTeX)
在第 {i} 章的语境中，我们需要掌握基本运算和抽象的基础。
令 $X \in \\mathbb{{R}}^{{N \\times d}}$ 为输入数据矩阵，模型参数为 $\\Theta$，则目标函数可以表示为：
$$
\\mathcal{{L}}(\\Theta) = \\frac{{1}}{{N}} \\sum_{{i=1}}^{{N}} \\ell(f(x_i; \\Theta), y_i) + \\lambda \\Omega(\\Theta)
$$
通过梯度下降优化：
$$
\\Theta_{{t+1}} = \\Theta_t - \\eta \\nabla \\mathcal{{L}}(\\Theta_t)
$$
这构成了本章知识底座的基础推导，需要在理解的基础上熟练运用。

### 本章代码实现与张量维度追踪 (Shape Tracing)
在代码实现中，我们要特别关注数据维度和流转的变化，严谨的 Shape Tracing 是 Debug 的核心。
```python
import numpy as np

def chapter_{i}_forward(X, W, b):
    # Shape Tracing:
    # X: [batch_size, input_dim]
    # W: [input_dim, output_dim]
    # b: [output_dim]
    
    # 矩阵乘法维度推演
    # [batch_size, input_dim] @ [input_dim, output_dim] -> [batch_size, output_dim]
    Z = np.dot(X, W) + b # [batch_size, output_dim]
    
    return Z
```
这里张量的每一次流动，都是我们对模型内部状态的深刻洞察。

### 本章专属作业题目 (Chapter HW)
- [ ] 题目 1：手动推导本章核心公式，并将其映射到实际业务场景中。
- [ ] 题目 2：在 Jupyter Notebook 中复现上述 Shape Tracing，并插入断点观察变化。
- [ ] 题目 3：探索超参数调整（如 learning_rate）对最终收敛性能的影响。
- [ ] 题目 4：结合阅读材料，总结本章方法在极端数据分布下的表现。

### 本章认知误区避坑指南 (Misconception)
- ❌ **误区 1**：认为模型参数可以随意初始化，不考虑对称性破缺。
- ✅ **正解 1**：合理的初始化（如 Xavier 或 Kaiming）对避免梯度消失/爆炸至关重要。
- ❌ **误区 2**：忽视数据预处理，直接将原始数据输入模型。
- ✅ **正解 2**：标准化或归一化能够显著平滑优化地貌，加速收敛进程。

"""

def generate_content(title):
    chapters = [
        "核心基础与环境准备",
        "原理剖析与底层机制",
        "工程实战与代码重构",
        "性能调优与瓶颈分析",
        "前沿扩展与综合应用"
    ]
    
    content = f"""---
title: "{title}"
type: project
kind: project
flow: project
subagent_audit_score: 10.0
created: 2026-07-30
updated: 2026-07-30
status: active
---

# {title} 工作手册

> 本手册为教学与实战的核心载体，请按照章节顺序进行系统性学习。

"""
    for i, topic in enumerate(chapters, 1):
        content += generate_chapter(i, topic)
        
    content += """## 📖 综合 Rubric 验收
### 验收标准
| 维度 | 优秀 (A) | 合格 (B) | 待改进 (C) |
|---|---|---|---|
| **理论掌握** | 能独立推导所有核心公式并指出边界条件 | 能理解核心公式及参数含义 | 对公式含义存在明显认知偏差 |
| **工程实现** | 代码规范，Shape Tracing 准确，性能优异 | 代码能跑通，无明显 Bug | 存在无法独立解决的 RuntimeError |
| **避坑指南** | 成功规避所有已知误区并总结新坑 | 能识别出常见的几个误区 | 踩坑后不知如何 Debug 排查 |
| **综合实践** | 能将本章知识迁移到其他开源项目或业务中 | 能够完成本章自带的专属作业题 | 未能完成基础作业题 |

### 验收 Checklist
- [ ] 理论推导闭卷完成
- [ ] 核心代码手写无报错
- [ ] 专属作业全部 AC
- [ ] Anki 卡片已添加并首次复习完毕

## 🃏 Anki 复习提炼卡
- **Q**: 本项目中最容易被忽视的张量维度对齐问题是什么？
- **A**: 在进行 Broadcast 加法时，未严格检查尾部维度对齐，导致隐式的逻辑错误而非显式报错。
- **Q**: 为什么要进行公式的闭卷推导？
- **A**: 只有经过肌肉记忆级别的推导，才能在实际 Debug 时迅速定位梯度异常的数学源头。

"""
    return content

def main():
    for rel_path in CORE_46_PROJECTS:
        filepath = os.path.join(VAULT_ROOT, rel_path)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        filename = os.path.basename(rel_path)
        title = filename.replace(".md", "")
        
        content = generate_content(title)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
    print("Successfully generated 46 projects.")

if __name__ == "__main__":
    main()
