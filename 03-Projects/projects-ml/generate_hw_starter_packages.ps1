$items = @(
  @{Num='02'; Slug='hw02_classification'; Title='HW02 Classification'; Note='机器学习 - HW02：Classification 分类阶梯作业.md'},
  @{Num='03'; Slug='hw03_cnn'; Title='HW03 CNN'; Note='机器学习 - HW03：CNN 卷积神经网络阶梯作业.md'},
  @{Num='04'; Slug='hw04_self_attention'; Title='HW04 Self-Attention'; Note='机器学习 - HW04：Self-Attention 自注意力阶梯作业.md'},
  @{Num='05'; Slug='hw05_transformer'; Title='HW05 Transformer'; Note='机器学习 - HW05：Transformer 阶梯作业.md'},
  @{Num='06'; Slug='hw06_gan'; Title='HW06 GAN'; Note='机器学习 - HW06：GAN 生成对抗网络阶梯作业.md'},
  @{Num='07'; Slug='hw07_bert'; Title='HW07 BERT'; Note='机器学习 - HW07：BERT 自监督表征阶梯作业.md'},
  @{Num='08'; Slug='hw08_autoencoder'; Title='HW08 Autoencoder'; Note='机器学习 - HW08：Autoencoder 自编码器阶梯作业.md'},
  @{Num='09'; Slug='hw09_explainable_ai'; Title='HW09 Explainable AI'; Note='机器学习 - HW09：Explainable AI 可解释性阶梯作业.md'},
  @{Num='10'; Slug='hw10_adversarial_attack'; Title='HW10 Adversarial Attack'; Note='机器学习 - HW10：Adversarial Attack 对抗攻击阶梯作业.md'},
  @{Num='11'; Slug='hw11_domain_adaptation'; Title='HW11 Domain Adaptation'; Note='机器学习 - HW11：Domain Adaptation 领域自适应阶梯作业.md'},
  @{Num='12'; Slug='hw12_reinforcement_learning'; Title='HW12 Reinforcement Learning'; Note='机器学习 - HW12：Reinforcement Learning 强化学习阶梯作业.md'},
  @{Num='13'; Slug='hw13_life_long_learning'; Title='HW13 Life-Long Learning'; Note='机器学习 - HW13：Life-Long Learning 终身学习阶梯作业.md'},
  @{Num='14'; Slug='hw14_compression'; Title='HW14 Compression'; Note='机器学习 - HW14：Compression 模型压缩阶梯作业.md'},
  @{Num='15'; Slug='hw15_meta_learning'; Title='HW15 Meta Learning'; Note='机器学习 - HW15：Meta Learning 元学习阶梯作业.md'}
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path

foreach ($item in $items) {
  $dir = Join-Path $root $item.Slug
  New-Item -ItemType Directory -Force $dir, (Join-Path $dir 'starter'), (Join-Path $dir 'baseline'), (Join-Path $dir 'reports'), (Join-Path $dir 'tests') | Out-Null

  @"
# $($item.Title) Assignment Starter Package

这是一份给学生自己完成的 `$($item.Title)` 作业包骨架。

当前包内提供：

- `starter/`：训练、推理、模型接口骨架
- `baseline/README.md`：记录你的 baseline 目标和结果
- `reports/report_template.md`：学生实验报告模板
- `data_card.md`：数据契约待补区
- `rubric.md`：评分与提交检查清单
- `tests/README.md`：建议你为自己的实现补哪些测试

## 对应笔记页

- `F:\-\02-Knowledge\🧠 学习系统\17-机器学习\$($item.Note)`

## 说明

1. 这不是教师答案包。
2. 你需要自己完成模型、训练循环、验证和提交。
3. 做题过程建议同步回填到 Obsidian 笔记。
"@ | Set-Content -Path (Join-Path $dir 'README.md') -Encoding UTF8

  @"
# $($item.Title) Data Card

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
"@ | Set-Content -Path (Join-Path $dir 'data_card.md') -Encoding UTF8

  @"
# $($item.Title) Rubric

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
"@ | Set-Content -Path (Join-Path $dir 'rubric.md') -Encoding UTF8

  @"
# $($item.Title) Baseline Tracker

这页只记录你的 baseline 目标和结果，不保存教师答案。

| 版本 | 指标 | 是否达到目标 | 备注 |
|:---|:---:|:---:|:---|
| Simple | 待填写 | 待填写 | |
| Medium | 待填写 | 待填写 | |
| Strong | 待填写 | 待填写 | |
| Boss | 待填写 | 待填写 | |
"@ | Set-Content -Path (Join-Path $dir 'baseline\README.md') -Encoding UTF8

  @"
# $($item.Title) Report Template

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
"@ | Set-Content -Path (Join-Path $dir 'reports\report_template.md') -Encoding UTF8

  '"""Assignment starter package."""' | Set-Content -Path (Join-Path $dir 'starter\__init__.py') -Encoding UTF8

  @"
from __future__ import annotations


# TODO(student): implement your $($item.Title) model here.
"@ | Set-Content -Path (Join-Path $dir 'starter\model.py') -Encoding UTF8

  @"
from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='$($item.Title) starter training entry.')
    parser.add_argument('--train-data', required=False, help='Path to training data.')
    parser.add_argument('--output-dir', required=True, help='Directory to store checkpoints and logs.')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    print('$($item.Title) starter is ready.')
    print('Student TODOs:')
    print('1. Load and preprocess the official data')
    print('2. Implement your model in starter/model.py')
    print('3. Add your training loop and validation logic here')
    print('4. Save checkpoints and metrics to the output directory')


if __name__ == '__main__':
    main()
"@ | Set-Content -Path (Join-Path $dir 'starter\train.py') -Encoding UTF8

  @"
from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='$($item.Title) starter inference entry.')
    parser.add_argument('--test-data', required=False, help='Path to test data.')
    parser.add_argument('--checkpoint', required=True, help='Path to your checkpoint.')
    parser.add_argument('--output', required=True, help='Path to submission file.')
    return parser.parse_args()


def main() -> None:
    _ = parse_args()
    print('$($item.Title) starter inference is ready.')
    print('Student TODOs:')
    print('1. Load your checkpoint')
    print('2. Run inference on the official test split')
    print('3. Save a submission file in the required format')


if __name__ == '__main__':
    main()
"@ | Set-Content -Path (Join-Path $dir 'starter\infer.py') -Encoding UTF8

  @"
# $($item.Title) Tests

建议学生至少补下面几类测试：

1. 数据加载与字段检查
2. 前向传播 shape 检查
3. 提交文件头检查
4. 最小训练 roundtrip 检查
"@ | Set-Content -Path (Join-Path $dir 'tests\README.md') -Encoding UTF8
}
