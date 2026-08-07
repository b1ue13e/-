"""HW03 starter：小型 CNN 与训练工程（PyTorch）

本模块同时服务于两个目的：
1. smoke 流程：`run_smoke()` 被 `run.py` 与 `tests/` 调用，保证最小闭环可运行；
2. 学习骨架：`TinyCNN / train_epoch / evaluate / check_batchnorm_train_eval`
   是本作业 Q2-Q5 的参考实现与验收对象——请先读作业正文的题目规格，
   在理解的基础上扩展（加深网络、加增强、做单因素对照）。

smoke 数据为 4×4 单通道小图（CSV 16 像素）；真实 CIFAR-10 图像到位后，
把 `load_images()` 切换为读取 `cifar10_images.train.npz`（(N,3,32,32) 张量）并归一化到 [0,1]。
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

# 全局随机种子（smoke 可复现）
SEED = 0


def _set_seed(seed: int = SEED) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)


# ---------------------------------------------------------------------------
# Q1 数据加载（smoke：4×4 单通道图；真实：CIFAR-10 张量）
# ---------------------------------------------------------------------------
def load_images(csv_path: Path) -> tuple[torch.Tensor, torch.Tensor]:
    """从 smoke CSV 加载 (X, y)：X (N,1,4,4) float32 归一化到 [0,1]，y (N,) int64。

    CSV 列：id, label, p0..p15（16 像素，值 0-9）。真实数据切换见 data_card.md。
    """
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"空数据文件: {csv_path}")
    X = np.array([[float(row[f"p{i}"]) for i in range(16)] for row in rows], dtype=np.float32)
    y = np.array([int(row["label"]) for row in rows], dtype=np.int64)
    X = X.reshape(-1, 1, 4, 4) / 9.0  # smoke 像素 0-9 → [0,1]；真实图像用 /255.0
    return torch.from_numpy(X), torch.from_numpy(y)


# ---------------------------------------------------------------------------
# Q2 TinyCNN：Conv + BatchNorm + FC
# ---------------------------------------------------------------------------
class TinyCNN(nn.Module):
    """最小可扩展 CNN：Conv2d(3×3, pad=1) + BatchNorm2d + ReLU + 全连接。

    参数化输入通道与图像尺寸，smoke（1 通道 4×4）与真实 CIFAR-10（3 通道 32×32）通用。
    """

    def __init__(self, in_channels: int = 1, img_size: int = 4, num_classes: int = 2, hidden_channels: int = 8):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, hidden_channels, kernel_size=3, padding=1)
        self.bn = nn.BatchNorm2d(hidden_channels)
        self.fc = nn.Linear(hidden_channels * img_size * img_size, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = torch.relu(self.bn(self.conv(x)))
        x = x.flatten(1)
        return self.fc(x)


# ---------------------------------------------------------------------------
# Q3 训练与评估
# ---------------------------------------------------------------------------
def train_epoch(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    X: torch.Tensor,
    y: torch.Tensor,
    batch_size: int = 0,
) -> float:
    """训练一个 epoch（batch_size=0 表示全批量），返回平均损失。"""
    model.train()
    if batch_size <= 0:
        batch_size = X.shape[0]
    losses = []
    idx = torch.randperm(X.shape[0])
    for start in range(0, X.shape[0], batch_size):
        batch_idx = idx[start : start + batch_size]
        optimizer.zero_grad()
        logits = model(X[batch_idx])
        loss = nn.functional.cross_entropy(logits, y[batch_idx])
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
    return float(np.mean(losses))


@torch.no_grad()
def evaluate(model: nn.Module, X: torch.Tensor, y: torch.Tensor) -> float:
    """评估准确率（自动切到 eval 模式，结束后恢复 train 模式）。"""
    was_training = model.training
    model.eval()
    logits = model(X)
    pred = logits.argmax(dim=1)
    acc = float((pred == y).float().mean())
    if was_training:
        model.train()
    return acc


# ---------------------------------------------------------------------------
# Q4 BatchNorm train/eval 模式差异验证
# ---------------------------------------------------------------------------
def check_batchnorm_train_eval(model: nn.Module, X: torch.Tensor) -> dict[str, object]:
    """验证 BatchNorm 的 train/eval 行为差异。

    - train 模式：使用当前 batch 的均值和方差；
    - eval 模式：使用训练阶段累积的 running stats；
    - 返回两种模式下的输出差分（差异 > 0 说明模式切换生效）与说明。
    注意：只有当模型至少训练过若干步（running stats 已更新）后差异才有意义。
    """
    model.train()
    out_train = model(X).detach().clone()
    model.eval()
    out_eval = model(X).detach().clone()
    model.train()
    diff = float((out_train - out_eval).abs().max())
    return {
        "max_output_diff": round(diff, 6),
        "explanation": (
            "train 用 batch 统计、eval 用 running stats；"
            "若 max_output_diff 约 0，说明 BatchNorm 未生效或尚未积累 running stats"
        ),
    }


# ---------------------------------------------------------------------------
# smoke 流程入口（run.py / tests 依赖，勿改签名）
# ---------------------------------------------------------------------------
def run_smoke(train_csv: Path, val_csv: Path) -> dict[str, object]:
    """在 smoke 数据（4×4 二分类图）上训练 TinyCNN，返回可复现的指标。"""
    _set_seed(SEED)
    X_train, y_train = load_images(train_csv)
    X_val, y_val = load_images(val_csv)

    model = TinyCNN(in_channels=1, img_size=4, num_classes=2)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.05, momentum=0.9)

    epoch_losses: list[float] = []
    for _ in range(60):
        loss = train_epoch(model, optimizer, X_train, y_train, batch_size=0)
        epoch_losses.append(round(loss, 6))

    train_acc = evaluate(model, X_train, y_train)
    val_acc = evaluate(model, X_val, y_val)
    bn_check = check_batchnorm_train_eval(model, X_train)

    return {
        "train_size": int(X_train.shape[0]),
        "val_size": int(X_val.shape[0]),
        "epoch_losses_head": epoch_losses[:5],
        "final_train_loss": epoch_losses[-1],
        "train_accuracy": round(train_acc, 4),
        "val_accuracy": round(val_acc, 4),
        "batchnorm_train_eval_diff": bn_check["max_output_diff"],
        "next_step": "把 smoke 图像替换成真实 CIFAR-10 图像张量（3×32×32），再做单因素对照实验（优化器/调度/增强/正则）。",
    }
