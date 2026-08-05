#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新学习路径文件为交互式大纲格式
"""

import re
import os
from pathlib import Path
from datetime import datetime

# 学习路径配置
ROADMAP_CONFIG = {
    "02-时间序列分析": {
        "emoji": "📈",
        "stages": [
            ("01-基础认知层", "🎯", "基础认知层", [
                ("时间序列概述", "定义、特征、应用场景"),
                ("趋势与季节性", "趋势提取、季节分解"),
                ("周期性分析", "周期检测、谐波分析"),
                ("自相关函数ACF", "自相关、偏自相关"),
                ("时间序列可视化", "可视化方法、工具"),
                ("Python时间序列工具", "Pandas、Statsmodels"),
            ]),
            ("02-统计基础层", "📊", "统计基础层", [
                ("平稳性", "严平稳、宽平稳、检验方法"),
                ("白噪声", "白噪声过程、Ljung-Box检验"),
                ("差分运算", "一阶差分、季节性差分"),
                ("对数变换", "方差稳定化、对数差分"),
                ("描述性统计", "均值、方差、分布特征"),
                ("假设检验", "单位根检验、ADF检验"),
            ]),
            ("03-经典模型层", "📈", "经典模型层", [
                ("AR模型", "自回归模型、参数估计"),
                ("MA模型", "移动平均模型、可逆性"),
                ("ARMA模型", "自回归移动平均、联合建模"),
                ("ARIMA模型", "差分整合、建模流程"),
                ("SARIMA模型", "季节性ARIMA、参数设置"),
                ("ARCH模型", "条件异方差、波动率建模"),
                ("GARCH模型", "广义ARCH、GARCH(1,1)"),
            ]),
            ("04-建模与诊断层", "🔍", "建模与诊断层", [
                ("模型识别", "ACF/PACF分析、模型选择"),
                ("参数估计", "最大似然、最小二乘"),
                ("AIC与BIC", "信息准则、模型比较"),
                ("残差分析", "残差检验、白噪声检验"),
                ("预测与评估", "点预测、区间预测、MAPE"),
                ("模型诊断", "过度拟合、模型改进"),
            ]),
            ("05-机器学习与深度学习进阶", "🤖", "机器学习与深度学习进阶", [
                ("特征工程", "滞后特征、滚动统计、日期特征"),
                ("时间序列交叉验证", "时间序列分割、前向验证"),
                ("XGBoost时序", "梯度提升、特征重要性"),
                ("RNN时序建模", "循环神经网络、序列建模"),
                ("LSTM与GRU", "长短期记忆、门控机制"),
                ("Transformer时序", "注意力机制、Informer"),
                ("N-BEATS", "纯深度学习预测模型"),
            ]),
            ("06-实战项目层", "🚀", "实战项目层", [
                ("股票价格预测", "金融时序、技术分析"),
                ("销售预测", "需求预测、库存优化"),
                ("能源负荷预测", "电力负荷、可再生能源"),
                ("异常检测", "异常点检测、故障预警"),
                ("Prophet实战", "Facebook Prophet工具"),
                ("时序竞赛技巧", "Kaggle、特征工程"),
            ]),
        ]
    },
}

def generate_roadmap_content(path_name, emoji, stages):
    """生成学习路径文件内容"""
    
    # 计算总主题数
    total_topics = sum(len(stage[3]) for stage in stages)
    
    content = f"""---
tags: [学习路径, {path_name.split('-')[1] if '-' in path_name else path_name}]
created: 2026-04-11
description: "{path_name}学习路线图"
---

# {emoji} {path_name.split('-')[1] if '-' in path_name else path_name}学习路径

> 学习路径描述

```dataviewjs
// 学习进度统计
"""
    
    # 添加进度统计代码
    for i, (folder, stage_emoji, stage_name, topics) in enumerate(stages, 1):
        content += f"""const stage{i} = dv.pages('"02-Knowledge/🧠 学习系统/{path_name}/{folder}"').where(p => p.status === "completed").length;
"""
    
    content += f"""
const totalCompleted = {" + ".join(f"stage{i}" for i in range(1, len(stages)+1))};
const totalProgress = Math.round((totalCompleted / {total_topics}) * 100);

dv.paragraph(`**总体进度: ${{totalProgress}}%** | 已完成: ${{totalCompleted}} / {total_topics} 主题`);
```

---

## 📋 学习路线图

| 阶段 | 进度 | 进入阶段 |
|:---:|:---:|:---:|
"""
    
    # 添加路线图表格
    for i, (folder, stage_emoji, stage_name, topics) in enumerate(stages, 1):
        content += f"""| {stage_emoji} **阶段{i}：{stage_name}** | `$= Math.round(dv.pages('"02-Knowledge/🧠 学习系统/{path_name}/{folder}"').where(p => p.status === "completed").length / {len(topics)} * 100) + "%"` | [[{folder}/{stage_emoji} {stage_name}\|进入 →]] |\n"""
    
    # 添加各阶段详细内容
    for i, (folder, stage_emoji, stage_name, topics) in enumerate(stages, 1):
        content += f"""
---

## {stage_emoji} 阶段{i}：{stage_name}

> 阶段描述

| 状态 | 主题 | 核心概念 | 操作 |
|:---:|:---|:---|:---:|
"""
        for topic, concepts in topics:
            file_name = topic.replace(" ", "").replace("/", "")
            safe_path = f"🧠%20学习系统/{path_name.replace('-', '%2D')}/{folder.replace('-', '%2D')}/{file_name}.md"
            content += f"""| ⬜ | [[{topic}]] | {concepts} | [📝 创建](obsidian://new?file={safe_path}) |\n"""
        
        content += f"""
**阶段入口**: [[{stage_emoji} {stage_name}]]
"""
    
    # 添加知识连接索引
    content += """
---

## 🔗 知识连接索引

### 与其他路径的连接

| 本路径概念 | 连接路径 | 相关概念 |
|:---|:---|:---|
"""
    
    # 根据不同路径添加不同的连接
    if "时间序列" in path_name:
        content += """| ACF/PACF | [[02-Knowledge/🧠 学习系统/16-多元统计/🗺️ 多元统计学习路径\|多元统计]] | 自相关、协方差 |
| 平稳性 | [[02-Knowledge/🧠 学习系统/16-多元统计/🗺️ 多元统计学习路径\|多元统计]] | 弱平稳、强平稳 |
| ARIMA | [[02-Knowledge/🧠 学习系统/17-机器学习/🗺️ 机器学习学习路径\|机器学习]] | 预测模型、回归 |
| RNN/LSTM | [[02-Knowledge/🧠 学习系统/17-机器学习/🗺️ 机器学习学习路径\|机器学习]] | 神经网络、深度学习 |
| 金融预测 | [[02-Knowledge/🧠 学习系统/03-量化金融/🗺️ 量化金融学习路径\|量化金融]] | 收益率、波动率建模 |
"""
    
    content += """
---

## 📚 推荐学习资源

| 类型 | 资源 | 说明 |
|:---|:---|:---|
| 📖 书籍 | 推荐书籍 | 说明 |

---

## 🔗 快速导航

- [[🏠 主页|返回主页]]
- [[🎓 学习入口|学习系统入口]]

---

*路线图更新：2026-04-11*
"""
    
    return content

def main():
    """主函数"""
    base_path = Path("02-Knowledge/🧠 学习系统")
    
    for path_name, config in ROADMAP_CONFIG.items():
        file_path = base_path / path_name / f"🗺️ {path_name.split('-')[1] if '-' in path_name else path_name}学习路径.md"
        
        if file_path.exists():
            content = generate_roadmap_content(
                path_name,
                config["emoji"],
                config["stages"]
            )
            file_path.write_text(content, encoding="utf-8")
            print(f"✅ 已更新: {file_path}")
        else:
            print(f"❌ 文件不存在: {file_path}")

if __name__ == "__main__":
    main()
