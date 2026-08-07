"""HW01 starter：kNN 与 Softmax 线性分类核心函数（NumPy 实现）

本模块同时服务于两个目的：
1. smoke 流程：`evaluate()` 被 `run.py` 与 `tests/` 调用，保证最小闭环可运行；
2. 学习骨架：`compute_distances / predict_knn / softmax_loss / numeric_gradient /
   train_softmax` 是本作业 Q2-Q6 的参考实现与验收对象——请先读作业正文的题目规格，
   在理解的基础上补全、重写或扩展（例如给 kNN 增加 L1、给 Softmax 增加 mini-batch）。

依赖：仅 NumPy。真实 CIFAR-10 子集到位后，把 `load_data()` 切换为读取
`cifar10.train.npz` / `cifar10.val.npz` / `label_map.json`（见 data_card.md）。
"""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import numpy as np


# ---------------------------------------------------------------------------
# Q1 数据加载与预处理
# ---------------------------------------------------------------------------
def load_data(
    train_csv: Path, val_csv: Path
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """从 smoke CSV 加载数据，返回 (X_train, y_train, X_val, y_val)。

    规格：
    - CSV 列：id, label, f1, f2, f3（smoke）；真实数据切换见 data_card.md。
    - X 形状 (N, D)，float32；y 形状 (N,)，元素为标签字符串（cat/dog/car）。
    - 只保留数值特征列（f1..fD），丢弃 id/label 列。
    """
    def _read(path: Path) -> tuple[np.ndarray, np.ndarray]:
        with path.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            raise ValueError(f"空数据文件: {path}")
        features = [[float(v) for k, v in row.items() if k.startswith("f")] for row in rows]
        labels = [row["label"] for row in rows]
        return np.asarray(features, dtype=np.float32), np.asarray(labels)

    X_train, y_train = _read(train_csv)
    X_val, y_val = _read(val_csv)
    return X_train, y_train, X_val, y_val


# ---------------------------------------------------------------------------
# Q2 kNN 距离矩阵（向量化，禁止 for 循环逐样本）
# ---------------------------------------------------------------------------
def compute_distances(X_train: np.ndarray, X_val: np.ndarray, metric: str = "l2") -> np.ndarray:
    """计算验证集到训练集的成对距离矩阵。

    输入：
    - X_train: (N_train, D) float32
    - X_val:   (N_val, D) float32
    - metric: 'l2'（欧氏）或 'l1'（曼哈顿）
    输出：
    - dists: (N_val, N_train) float32，dists[i, j] = 第 i 个验证样本到第 j 个训练样本的距离

    要求：
    - 使用广播实现，不得写两层 for 循环逐样本计算；
    - L2 用平方展开：||a-b||^2 = ||a||^2 + ||b||^2 - 2 a·b，再开方；
    - 手算校验样例：X_train=[[0,0],[1,1]]，X_val=[[0,1]]，
      l2 结果应为 [[1.0, 1.0]]（√1 与 √1），l1 结果应为 [[1.0, 1.0]]。
    """
    if metric == "l2":
        aa = np.sum(X_val**2, axis=1, keepdims=True)          # (N_val, 1)
        bb = np.sum(X_train**2, axis=1, keepdims=True).T       # (1, N_train)
        ab = X_val @ X_train.T                                  # (N_val, N_train)
        dists = np.sqrt(np.maximum(aa + bb - 2 * ab, 0.0))      # 数值截断防负
    elif metric == "l1":
        # 用广播：|a-b| 求和；大矩阵时可用 np.abs(X_val[:, None, :] - X_train[None, :, :]).sum(axis=2)
        diff = X_val[:, None, :] - X_train[None, :, :]
        dists = np.abs(diff).sum(axis=2)
    else:
        raise ValueError(f"未知 metric: {metric}（支持 'l1' / 'l2'）")
    return dists.astype(np.float32)


# ---------------------------------------------------------------------------
# Q3 kNN 预测（top-k 投票）
# ---------------------------------------------------------------------------
def predict_knn(
    X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, k: int = 3, metric: str = "l2"
) -> np.ndarray:
    """k 近邻投票预测。

    规则：
    - 对每个验证样本，取距离最近的前 k 个训练样本的标签做多数投票；
    - 平局时按标签字典序取第一个（如 ['car','cat','dog'] 中 'cat' 先于 'dog'）；
    - 返回与 y_val 同形状的预测标签数组。
    """
    dists = compute_distances(X_train, X_val, metric=metric)
    preds = []
    for i in range(dists.shape[0]):
        nn_idx = np.argsort(dists[i])[:k]
        votes = Counter(y_train[nn_idx].tolist())
        # 平局按标签字典序取第一个：most_common(1) 已按计数降序，同计数按插入序；
        # 这里显式按 (计数, 标签) 排序保证确定性。
        best = min(votes.items(), key=lambda kv: (-kv[1], kv[0]))
        preds.append(best[0])
    return np.asarray(preds)


# ---------------------------------------------------------------------------
# Q4 Softmax 交叉熵损失与解析梯度（数值稳定）
# ---------------------------------------------------------------------------
def softmax_loss(W: np.ndarray, X: np.ndarray, y: np.ndarray) -> tuple[float, np.ndarray]:
    """Softmax 交叉熵损失与其解析梯度。

    输入：
    - W: (D, C) float32，第 c 列是类别 c 的权重向量
    - X: (N, D) float32（已包含偏置列时 W 为 (D+1, C)，X 末列为 1）
    - y: (N,) 整数类别索引（0..C-1）
    输出：
    - loss: 标量，L = (1/N) Σ_i [ -log p_i[y_i] ]，p_i 为 softmax 概率
    - grad: (D, C)，∂L/∂W = (1/N) X^T (P - Y_onehot)

    数值稳定：softmax 前先减去每行最大 logit（减 max 不改变结果）。
    手算样例：W=[[1,0],[0,1]]，X=[[1,0],[0,1]]，y=[0,1] → loss ≈ 0.3133（softmax 归一化后每行 0.5/0.5）。
    """
    X = X.astype(np.float64)
    W = W.astype(np.float64)
    scores = X @ W                                    # (N, C)
    scores -= scores.max(axis=1, keepdims=True)        # 数值稳定
    exp_scores = np.exp(scores)
    probs = exp_scores / exp_scores.sum(axis=1, keepdims=True)

    n = X.shape[0]
    loss = -np.log(probs[np.arange(n), y] + 1e-12).mean()

    dprobs = probs.copy()
    dprobs[np.arange(n), y] -= 1.0
    grad = X.T @ dprobs / n
    return float(loss), grad.astype(np.float32)


# ---------------------------------------------------------------------------
# Q5 数值梯度验证（中心差分）
# ---------------------------------------------------------------------------
def numeric_gradient(
    loss_fn, W: np.ndarray, X: np.ndarray, y: np.ndarray, eps: float = 1e-6
) -> np.ndarray:
    """用中心差分计算 loss_fn 对 W 的数值梯度。

    对 W 的每个元素 w: (loss(W+eps·e_ij) - loss(W-eps·e_ij)) / (2·eps)。
    与解析梯度比较时用相对误差 |num-an| / max(1, |num|, |an|)，小于 1e-6 量级即通过。
    """
    num_grad = np.zeros_like(W)
    W64 = W.astype(np.float64)  # 用 float64 做扰动，避免 float32 舍入淹没差分
    it = np.nditer(W64, flags=["multi_index"])
    while not it.finished:
        i, j = it.multi_index
        W_plus = W64.copy()
        W_minus = W64.copy()
        W_plus[i, j] += eps
        W_minus[i, j] -= eps
        loss_plus, _ = loss_fn(W_plus, X, y)
        loss_minus, _ = loss_fn(W_minus, X, y)
        num_grad[i, j] = (loss_plus - loss_minus) / (2 * eps)
        it.iternext()
    return num_grad.astype(np.float32)


def check_gradient(rel_tol: float = 1e-6) -> dict[str, float]:
    """在随机小数据上做一次梯度检查，返回最大相对误差（smoke 自检用）。"""
    rng = np.random.default_rng(0)
    D, C, N = 4, 3, 5
    X = rng.normal(size=(N, D)).astype(np.float32)
    W = rng.normal(size=(D, C)).astype(np.float32) * 0.1
    y = rng.integers(0, C, size=N)

    _, an_grad = softmax_loss(W, X, y)
    num_grad = numeric_gradient(softmax_loss, W, X, y)
    denom = np.maximum(1.0, np.maximum(np.abs(an_grad), np.abs(num_grad)))
    rel_err = np.abs(an_grad - num_grad) / denom
    return {"max_relative_error": float(rel_err.max()), "rel_tol": rel_tol}


# ---------------------------------------------------------------------------
# Q6 训练与评估协议（固定种子，SGD 最小实现）
# ---------------------------------------------------------------------------
def train_softmax(
    X_train: np.ndarray,
    y_train: np.ndarray,
    lr: float = 0.5,
    reg: float = 0.0,
    iters: int = 300,
    batch_size: int | None = None,
    seed: int = 0,
) -> tuple[np.ndarray, list[float]]:
    """用批量梯度下降（或 mini-batch）训练 Softmax 线性分类器。

    - 输入 y 为字符串标签时自动映射为整数索引；
    - 权重初始化 W ~ N(0, 0.01)；每步 W -= lr·(grad + reg·W)（L2 正则化梯度）；
    - 返回 (W, loss_history)，loss_history 记录每 10 步的平均损失。
    """
    labels = sorted(set(y_train.tolist()))
    label_to_idx = {lab: i for i, lab in enumerate(labels)}
    y_idx = np.array([label_to_idx[v] for v in y_train.tolist()])

    rng = np.random.default_rng(seed)
    D = X_train.shape[1]
    C = len(labels)
    W = (rng.normal(size=(D, C)) * 0.01).astype(np.float32)

    if batch_size is None:
        batch_size = X_train.shape[0]

    loss_history: list[float] = []
    for step in range(iters):
        idx = rng.choice(X_train.shape[0], size=batch_size, replace=True)
        Xb = X_train[idx]
        yb = y_idx[idx]
        loss, grad = softmax_loss(W, Xb, yb)
        if reg > 0:
            grad = grad + reg * W
        W = W - lr * grad
        if step % 10 == 0 or step == iters - 1:
            loss_history.append(round(loss, 6))
    return W, loss_history


def accuracy(W: np.ndarray, X: np.ndarray, y: np.ndarray) -> float:
    """Softmax 线性分类器准确率（y 可为字符串标签，自动映射）。"""
    labels = sorted(set(y.tolist()))
    label_to_idx = {lab: i for i, lab in enumerate(labels)}
    y_idx = np.array([label_to_idx[v] for v in y.tolist()])
    scores = X @ W
    pred = scores.argmax(axis=1)
    return float((pred == y_idx).mean())


# ---------------------------------------------------------------------------
# smoke 流程入口（run.py / tests 依赖，勿改签名）
# ---------------------------------------------------------------------------
def evaluate(train_csv: Path, val_csv: Path) -> dict[str, object]:
    """组织最小 smoke 流程：kNN(k=3) 与 Softmax(训练 300 步) 的准确率与失败样本。"""
    X_train, y_train, X_val, y_val = load_data(train_csv, val_csv)

    knn_pred = predict_knn(X_train, y_train, X_val, k=3)
    knn_accuracy = float((knn_pred == y_val).mean())

    W, loss_history = train_softmax(X_train, y_train, lr=0.5, reg=0.0, iters=300, seed=0)
    sm_accuracy = accuracy(W, X_val, y_val)

    failures: list[dict[str, str]] = []
    for i in range(len(y_val)):
        if knn_pred[i] != y_val[i] or (X_val[i] @ W).argmax() != 0:  # 占位：由 accuracy 覆盖
            pass
    # 失败样本：kNN 与 Softmax 至少一个预测错误
    softmax_pred_idx = (X_val @ W).argmax(axis=1)
    labels = sorted(set(y_train.tolist()))
    softmax_pred = np.array([labels[i] for i in softmax_pred_idx])
    for i in range(len(y_val)):
        if knn_pred[i] != y_val[i] or softmax_pred[i] != y_val[i]:
            failures.append(
                {
                    "sample_id": f"val{i}",
                    "label": str(y_val[i]),
                    "knn_pred": str(knn_pred[i]),
                    "softmax_pred": str(softmax_pred[i]),
                }
            )

    label_counts = dict(Counter(y_train.tolist()))
    return {
        "train_size": int(X_train.shape[0]),
        "val_size": int(X_val.shape[0]),
        "label_counts": label_counts,
        "knn_accuracy": round(knn_accuracy, 4),
        "softmax_accuracy": round(sm_accuracy, 4),
        "failure_examples": failures[:3],
    }
