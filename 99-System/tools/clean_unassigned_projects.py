import os
import shutil
import re

VAULT_ROOT = r"f:\-"
PROJECTS_ROOT = os.path.join(VAULT_ROOT, "03-Projects")
UNKNOWN_DIR = os.path.join(PROJECTS_ROOT, "通用项目")

COURSE_TO_TRACK = {
    "01-社交网络挖掘": "机器学习与AI应用",
    "02-时间序列分析": "金融与时序",
    "03-量化金融": "金融与时序",
    "04-离散数学": "数学底座",
    "05-计算机视觉": "机器学习与AI应用",
    "06-常微分方程": "数学底座",
    "07-最优化方法": "金融与时序",
    "08-NLP全栈": "机器学习与AI应用",
    "09-高等代数": "数学底座",
    "10-数据结构与算法": "系统与硬件",
    "11-计算机组成原理": "系统与硬件",
    "12-信号与系统": "系统与硬件",
    "13-强化学习": "机器学习与AI应用",
    "14-概率图模型": "机器学习与AI应用",
    "15-控制与机器人学": "系统与硬件",
    "16-多元统计": "概率统计与数据建模",
    "17-机器学习": "机器学习与AI应用",
    "22-概率论与数理统计": "概率统计与数据建模",
    "23-图神经网络": "机器学习与AI应用",
    "24-随机过程": "概率统计与数据建模",
    "25-测度论": "数学底座",
    "26-实变函数": "数学底座",
    "27-泛函分析": "数学底座",
    "28-数学分析": "数学底座",
    "29-运筹学": "金融与时序",
    "30-应用回归分析": "概率统计与数据建模",
    "31-属性数据分析": "概率统计与数据建模",
    "32-非参数统计": "概率统计与数据建模",
    "33-贝叶斯统计": "概率统计与数据建模",
    "34-偏微分方程": "数学底座",
    "35-数值分析": "数学底座",
    "36-数据挖掘与信息检索": "机器学习与AI应用",
    "37-复变函数": "数学底座",
    "38-AI Agent设计与工程实践": "AI Agent工程",
    "39-HelloAgents从零构建智能体": "AI Agent工程",
    "40-微软AI-Agents入门与工程实践": "AI Agent工程",
    "41-HuggingFace-Agents开源框架与实战": "AI Agent工程",
    "42-LangGraph复杂工作流与状态机": "AI Agent工程",
    "43-MCP协议与智能体服务编排": "AI Agent工程",
    "44-OpenAI-Agents-SDK架构与设计模式": "AI Agent工程",
    "45-生成式AI基础与Prompt工程": "AI Agent工程"
}

def clean_unassigned():
    if not os.path.exists(UNKNOWN_DIR):
        print("No 通用项目 directory exists.")
        return

    count = 0
    for root, dirs, files in os.walk(UNKNOWN_DIR):
        for f in files:
            if f.endswith(".md"):
                abs_path = os.path.join(root, f)
                if not os.path.exists(abs_path):
                    continue

                with open(abs_path, "r", encoding="utf-8") as file_in:
                    content = file_in.read()

                course = None
                for c in COURSE_TO_TRACK:
                    if c in content or c in abs_path or c[3:] in content:
                        course = c
                        break

                if not course:
                    if any(k in f for k in ["CIFAR", "CNN", "HDR", "Panorama", "分割", "图像", "姿态", "检测", "风格"]):
                        course = "05-计算机视觉"
                    elif any(k in f for k in ["Bert", "Transformer", "NLP", "翻译", "文本"]):
                        course = "08-NLP全栈"
                    elif any(k in f for k in ["PPO", "DQN", "Q-Learning", "强化"]):
                        course = "13-强化学习"
                    else:
                        course = "17-机器学习"

                track = COURSE_TO_TRACK.get(course, "机器学习与AI应用")
                target_dir = os.path.join(PROJECTS_ROOT, track, course)
                os.makedirs(target_dir, exist_ok=True)
                dst_path = os.path.join(target_dir, f)

                if content.startswith("---"):
                    parts = content.split("---", 2)
                    fm = parts[1]
                    body = parts[2] if len(parts) > 2 else ""

                    fm = re.sub(r"^type:\s*.*$", 'type: project', fm, flags=re.MULTILINE) if 'type:' in fm else fm + '\ntype: project'
                    fm = re.sub(r"^flow:\s*.*$", 'flow: project', fm, flags=re.MULTILINE) if 'flow:' in fm else fm + '\nflow: project'
                    fm = re.sub(r"^kind:\s*.*$", 'kind: project', fm, flags=re.MULTILINE) if 'kind:' in fm else fm + '\nkind: project'
                    
                    if 'track:' in fm:
                        fm = re.sub(r"^track:\s*.*$", f'track: "{track}"', fm, flags=re.MULTILINE)
                    else:
                        fm = fm.strip() + f'\ntrack: "{track}"\n'

                    if 'course:' in fm:
                        fm = re.sub(r"^course:\s*.*$", f'course: "{course}"', fm, flags=re.MULTILINE)
                    else:
                        fm = fm.strip() + f'\ncourse: "{course}"\n'

                    if 'status:' not in fm:
                        fm = fm.strip() + '\nstatus: active\n'

                    content = f"---{fm.strip()}\n---\n{body.lstrip()}"

                with open(dst_path, "w", encoding="utf-8") as file_out:
                    file_out.write(content)

                if os.path.exists(abs_path):
                    os.remove(abs_path)
                count += 1

    shutil.rmtree(UNKNOWN_DIR, ignore_errors=True)
    print(f"Cleaned {count} unassigned project files.")

if __name__ == "__main__":
    clean_unassigned()
