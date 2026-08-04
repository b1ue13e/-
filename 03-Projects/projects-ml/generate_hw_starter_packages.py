from pathlib import Path


ITEMS = [
    ("hw02_classification", "HW02 Classification", "机器学习 - HW02：Classification 分类阶梯作业.md"),
    ("hw03_cnn", "HW03 CNN", "机器学习 - HW03：CNN 卷积神经网络阶梯作业.md"),
    ("hw04_self_attention", "HW04 Self-Attention", "机器学习 - HW04：Self-Attention 自注意力阶梯作业.md"),
    ("hw05_transformer", "HW05 Transformer", "机器学习 - HW05：Transformer 阶梯作业.md"),
    ("hw06_gan", "HW06 GAN", "机器学习 - HW06：GAN 生成对抗网络阶梯作业.md"),
    ("hw07_bert", "HW07 BERT", "机器学习 - HW07：BERT 自监督表征阶梯作业.md"),
    ("hw08_autoencoder", "HW08 Autoencoder", "机器学习 - HW08：Autoencoder 自编码器阶梯作业.md"),
    ("hw09_explainable_ai", "HW09 Explainable AI", "机器学习 - HW09：Explainable AI 可解释性阶梯作业.md"),
    ("hw10_adversarial_attack", "HW10 Adversarial Attack", "机器学习 - HW10：Adversarial Attack 对抗攻击阶梯作业.md"),
    ("hw11_domain_adaptation", "HW11 Domain Adaptation", "机器学习 - HW11：Domain Adaptation 领域自适应阶梯作业.md"),
    ("hw12_reinforcement_learning", "HW12 Reinforcement Learning", "机器学习 - HW12：Reinforcement Learning 强化学习阶梯作业.md"),
    ("hw13_life_long_learning", "HW13 Life-Long Learning", "机器学习 - HW13：Life-Long Learning 终身学习阶梯作业.md"),
    ("hw14_compression", "HW14 Compression", "机器学习 - HW14：Compression 模型压缩阶梯作业.md"),
    ("hw15_meta_learning", "HW15 Meta Learning", "机器学习 - HW15：Meta Learning 元学习阶梯作业.md"),
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parent
    note_root = Path(r"F:\-\02-Knowledge\🧠 学习系统\17-机器学习")

    for slug, title, note in ITEMS:
        package = root / slug
        for name in ["starter", "baseline", "reports", "tests"]:
            (package / name).mkdir(parents=True, exist_ok=True)

        write(
            package / "README.md",
            f"""# {title} Assignment Starter Package

这是一份给学生自己完成的 `{title}` 作业包骨架。

当前包内提供：

- `starter/`：训练、推理、模型接口骨架
- `baseline/README.md`：记录你的 baseline 目标和结果
- `reports/report_template.md`：学生实验报告模板
- `data_card.md`：数据契约待补区
- `rubric.md`：评分与提交检查清单
- `tests/README.md`：建议你为自己的实现补哪些测试

## 对应笔记页

- `{note_root / note}`

## 说明

1. 这不是教师答案包。
2. 你需要自己完成模型、训练循环、验证和提交。
3. 做题过程建议同步回填到 Obsidian 笔记。
""",
        )

        write(
            package / "data_card.md",
            f"""# {title} Data Card

## 当前状态

- 这份作业包目前只建立了数据契约占位。
- 当你接入官方数据后，请在这里补：
  - 数据来源
  - 文件名
  - 字段结构
  - 标签定义
  - 提交格式

## 最少应补的内容

1. 原始数据文件名
2. 训练 / 验证 / 测试划分方式
3. 标签或目标列含义
4. 提交文件头
5. 已知限制和注意事项
""",
        )

        write(
            package / "rubric.md",
            f"""# {title} Rubric

| 维度 | 权重 | 通过标准 |
|:---|:---:|:---|
| 可运行性 | 25 | 能完成训练、验证、推理 |
| 数据与验证 | 20 | 有清楚的数据契约和验证方式 |
| Baseline 质量 | 20 | 有至少一个可比较 baseline |
| 复现规范 | 15 | README、路径、命令清楚 |
| 分析质量 | 20 | 有实验对照与结果解释 |

## 提交检查清单

- [ ] README 已补全
- [ ] data_card 已补全
- [ ] starter 已实现
- [ ] baseline 结果已记录
- [ ] report 已回填
""",
        )

        write(
            package / "baseline" / "README.md",
            f"""# {title} Baseline Tracker

这页只记录你的 baseline 目标和结果，不保存教师答案。

| 版本 | 指标 | 是否达到目标 | 备注 |
|:---|:---:|:---:|:---|
| Simple | 待填写 | 待填写 | |
| Medium | 待填写 | 待填写 | |
| Strong | 待填写 | 待填写 | |
| Boss | 待填写 | 待填写 | |
""",
        )

        write(
            package / "reports" / "report_template.md",
            f"""# {title} Report Template

> 这份报告由学生自己回填，不预置教师结果。

## 1. 任务目标

- 本次要解决的问题：
- 当前 baseline：

## 2. 数据与设置

- 数据版本：
- 划分方式：
- 指标：

## 3. 实验记录

| 实验编号 | 模型 | 关键配置 | 指标 | 备注 |
|:---:|:---|:---|:---:|:---|
| E1 | | | | |
| E2 | | | | |
| E3 | | | | |

## 4. 最终方案

- 最终模型：
- 最终配置：
- 最终结果：

## 5. 复盘

- 最有效改动：
- 最大问题：
- 下一步：
""",
        )

        write(package / "starter" / "__init__.py", '"""Assignment starter package."""\n')
        write(
            package / "starter" / "model.py",
            f"""from __future__ import annotations


# TODO(student): implement your {title} model here.
""",
        )
        write(
            package / "starter" / "train.py",
            f"""from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="{title} starter training entry.")
    parser.add_argument("--train-data", required=False, help="Path to training data.")
    parser.add_argument("--output-dir", required=True, help="Directory to store checkpoints and logs.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    print("{title} starter is ready.")
    print("Student TODOs:")
    print("1. Load and preprocess the official data")
    print("2. Implement your model in starter/model.py")
    print("3. Add your training loop and validation logic here")
    print("4. Save checkpoints and metrics to the output directory")


if __name__ == "__main__":
    main()
""",
        )
        write(
            package / "starter" / "infer.py",
            f"""from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="{title} starter inference entry.")
    parser.add_argument("--test-data", required=False, help="Path to test data.")
    parser.add_argument("--checkpoint", required=True, help="Path to your checkpoint.")
    parser.add_argument("--output", required=True, help="Path to submission file.")
    return parser.parse_args()


def main() -> None:
    _ = parse_args()
    print("{title} starter inference is ready.")
    print("Student TODOs:")
    print("1. Load your checkpoint")
    print("2. Run inference on the official test split")
    print("3. Save a submission file in the required format")


if __name__ == "__main__":
    main()
""",
        )
        write(
            package / "tests" / "README.md",
            f"""# {title} Tests

建议学生至少补下面几类测试：

1. 数据加载与字段检查
2. 前向传播 shape 检查
3. 提交文件头检查
4. 最小训练 roundtrip 检查
""",
        )


if __name__ == "__main__":
    main()
