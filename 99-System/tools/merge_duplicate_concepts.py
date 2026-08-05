import os

vault_dir = r'f:\-\02-Knowledge\🧠 学习系统'

duplicates = [
    ("Cluster-GCN", ["01-社交网络挖掘", "23-图神经网络"]),
    ("GraphSAINT", ["01-社交网络挖掘", "23-图神经网络"]),
    ("Skip-gram", ["08-NLP全栈", "23-图神经网络"]),
    ("Softmax", ["23-图神经网络", "31-属性数据分析", "17-机器学习"]),
    ("AIC", ["14-概率图模型", "31-属性数据分析", "02-时间序列分析", "30-应用回归分析"]),
    ("BIC", ["14-概率图模型", "31-属性数据分析", "02-时间序列分析", "30-应用回归分析"]),
    ("Bagging", ["17-机器学习", "32-非参数统计"]),
    ("度量学习", ["05-计算机视觉", "17-机器学习"]),
    ("策略改进", ["13-强化学习", "29-运筹学"]),
    ("二分图", ["10-数据结构与算法", "29-运筹学", "04-离散数学"]),
    ("滚动优化", ["15-控制与机器人学", "29-运筹学"]),
    ("禁忌搜索", ["14-概率图模型", "29-运筹学", "07-最优化方法"]),
    ("经验分布函数", ["22-概率论与数理统计", "32-非参数统计"]),
    ("矩阵转置", ["06-常微分方程", "09-高等代数"]),
    ("Cramer 法则", ["06-常微分方程", "09-高等代数"]),
    ("Cramer法则", ["06-常微分方程", "09-高等代数"]),
    ("特征值定义", ["06-常微分方程", "09-高等代数"]),
    ("LP 松弛", ["07-最优化方法", "29-运筹学"]),
    ("LP松弛", ["07-最优化方法", "29-运筹学"]),
    ("LU分解", ["09-高等代数"]),
    ("正规方程", ["27-泛函分析", "35-数值分析", "17-机器学习", "30-应用回归分析"]),
    ("卷积定理", ["12-信号与系统", "26-实变函数"]),
    ("测试函数", ["27-泛函分析", "34-偏微分方程"]),
    ("特征函数展开", ["06-常微分方程", "27-泛函分析"]),
    ("自伴算子", ["06-常微分方程", "27-泛函分析"]),
    ("函数项级数", ["26-实变函数", "28-数学分析"]),
    ("分布观点", ["25-测度论", "34-偏微分方程"]),
    ("随机游走", ["02-时间序列分析", "23-图神经网络", "24-随机过程"]),
    ("邻接矩阵", ["10-数据结构与算法", "23-图神经网络", "04-离散数学"]),
    ("多元线性回归模型", ["30-应用回归分析"]),
    ("中国剩余定理", ["04-离散数学", "10-数据结构与算法"]),
    ("最近点对问题", ["10-数据结构与算法"])
]

found_locations = {}

for root, dirs, files in os.walk(vault_dir):
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            name_no_ext = f.replace('.md', '')
            for item in duplicates:
                key = item[0]
                if key in name_no_ext:
                    rel = os.path.relpath(fp, vault_dir)
                    found_locations.setdefault(key, []).append((fp, rel))

print("=== Found Duplicates Locations ===")
with open(r'f:\-\99-System\tools\duplicate_report.txt', 'w', encoding='utf-8') as out:
    for key, locs in sorted(found_locations.items()):
        out.write(f"[{key}] (Found {len(locs)} files):\n")
        for fp, rel in locs:
            out.write(f"  - {rel}\n")
        out.write("\n")

print("Saved duplicate report to duplicate_report.txt successfully.")
