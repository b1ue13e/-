import os
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

VAULT_ROOT = r"f:\-\02-Knowledge\🧠 学习系统"

TRACK_MAPPING = {
    # 1. 数学底座
    "04-离散数学": "数学底座",
    "06-常微分方程": "数学底座",
    "09-高等代数": "数学底座",
    "25-测度论": "数学底座",
    "26-实变函数": "数学底座",
    "27-泛函分析": "数学底座",
    "28-数学分析": "数学底座",
    "34-偏微分方程": "数学底座",
    "35-数值分析": "数学底座",
    "37-复变函数": "数学底座",
    
    # 2. 概率统计与数据建模
    "16-多元统计": "概率统计与数据建模",
    "22-概率论与数理统计": "概率统计与数据建模",
    "24-随机过程": "概率统计与数据建模",
    "30-应用回归分析": "概率统计与数据建模",
    "31-属性数据分析": "概率统计与数据建模",
    "32-非参数统计": "概率统计与数据建模",
    "33-贝叶斯统计": "概率统计与数据建模",

    # 3. 机器学习与AI应用
    "01-社交网络挖掘": "机器学习与AI应用",
    "05-计算机视觉": "机器学习与AI应用",
    "08-NLP全栈": "机器学习与AI应用",
    "13-强化学习": "机器学习与AI应用",
    "14-概率图模型": "机器学习与AI应用",
    "17-机器学习": "机器学习与AI应用",
    "23-图神经网络": "机器学习与AI应用",
    "36-数据挖掘与信息检索": "机器学习与AI应用",

    # 4. AI Agent工程
    "38-AI Agent设计与工程实践": "AI Agent工程",
    "39-HelloAgents从零构建智能体": "AI Agent工程",
    "40-微软AI-Agents入门与工程实践": "AI Agent工程",
    "41-HuggingFace-Agents开源框架与实战": "AI Agent工程",
    "42-LangGraph复杂工作流与状态机": "AI Agent工程",
    "43-MCP协议与智能体服务编排": "AI Agent工程",
    "44-OpenAI-Agents-SDK架构与设计模式": "AI Agent工程",
    "45-生成式AI基础与Prompt工程": "AI Agent工程",

    # 5. 系统与硬件
    "10-数据结构与算法": "系统与硬件",
    "11-计算机组成原理": "系统与硬件",
    "12-信号与系统": "系统与硬件",
    "15-控制与机器人学": "系统与硬件",

    # 6. 金融与时序
    "02-时间序列分析": "金融与时序",
    "03-量化金融": "金融与时序",
    "07-最优化方法": "金融与时序",
    "29-运筹学": "金融与时序",

    # 辅助目录
    "18-题库学习": "辅助系统",
    "19-习惯追踪": "辅助系统",
    "20-PARA知识管理": "辅助系统",
    "21-周期笔记": "辅助系统",
}

def update_path_index_files():
    updated_count = 0
    missing_count = 0
    
    for dir_name, track in TRACK_MAPPING.items():
        dir_path = os.path.join(VAULT_ROOT, dir_name)
        if not os.path.exists(dir_path):
            print(f"[MISSING DIR] {dir_name}")
            missing_count += 1
            continue
        
        index_files = [f for f in os.listdir(dir_path) if f.startswith("🗺️") and f.endswith(".md")]
        if not index_files:
            index_files = [f for f in os.listdir(dir_path) if "学习路径" in f and f.endswith(".md")]
            
        if not index_files:
            print(f"[MISSING INDEX FILE] in {dir_name}")
            missing_count += 1
            continue
            
        index_file_path = os.path.join(dir_path, index_files[0])
        with open(index_file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        if content.startswith("---"):
            parts = content.split("---", 2)
            frontmatter = parts[1]
            body = parts[2] if len(parts) > 2 else ""
            
            if re.search(r"^track:\s*", frontmatter, re.MULTILINE):
                frontmatter = re.sub(r"^track:\s*.*$", f'track: "{track}"', frontmatter, flags=re.MULTILINE)
            else:
                frontmatter = frontmatter.strip() + f'\ntrack: "{track}"\n'
                
            new_content = f"---{frontmatter}---\n{body.lstrip()}"
        else:
            new_content = f'---\ntrack: "{track}"\n---\n\n' + content
            
        with open(index_file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        print(f"[UPDATED] {dir_name} / {index_files[0]} -> track: '{track}'")
        updated_count += 1

    print(f"\nCompleted: {updated_count} updated, {missing_count} missing.")

if __name__ == "__main__":
    update_path_index_files()
