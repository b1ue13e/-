from __future__ import annotations

import csv
import math
from copy import deepcopy
from pathlib import Path


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _dataset(path: Path) -> list[tuple[list[float], int]]:
    return [([float(row["x1"]), float(row["x2"])], int(row["label"])) for row in _read_rows(path)]


def _init_params() -> dict[str, list]:
    return {
        "W1": [[0.20, -0.10, 0.15], [0.05, 0.18, -0.12]],
        "b1": [0.0, 0.0, 0.0],
        "W2": [[0.12, -0.08], [0.10, 0.06], [-0.07, 0.11]],
        "b2": [0.0, 0.0],
    }


def _relu(values: list[float]) -> list[float]:
    return [v if v > 0 else 0.0 for v in values]


def _softmax(logits: list[float]) -> list[float]:
    shift = max(logits)
    exps = [math.exp(v - shift) for v in logits]
    total = sum(exps)
    return [v / total for v in exps]


def _forward(params: dict[str, list], features: list[float]) -> tuple[list[float], list[float], list[float]]:
    hidden_linear = []
    for j in range(3):
        hidden_linear.append(sum(features[i] * params["W1"][i][j] for i in range(2)) + params["b1"][j])
    hidden = _relu(hidden_linear)
    logits = []
    for k in range(2):
        logits.append(sum(hidden[j] * params["W2"][j][k] for j in range(3)) + params["b2"][k])
    return hidden_linear, hidden, logits


def loss_and_grads(params: dict[str, list], batch: list[tuple[list[float], int]]) -> tuple[float, dict[str, list]]:
    grads = {
        "W1": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        "b1": [0.0, 0.0, 0.0],
        "W2": [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]],
        "b2": [0.0, 0.0],
    }
    loss = 0.0
    for features, label in batch:
        hidden_linear, hidden, logits = _forward(params, features)
        probs = _softmax(logits)
        loss += -math.log(max(probs[label], 1e-12))

        dlogits = probs[:]
        dlogits[label] -= 1.0
        for j in range(3):
            for k in range(2):
                grads["W2"][j][k] += hidden[j] * dlogits[k]
        for k in range(2):
            grads["b2"][k] += dlogits[k]

        dhidden = []
        for j in range(3):
            dhidden.append(sum(params["W2"][j][k] * dlogits[k] for k in range(2)))
        dhidden_linear = [dhidden[j] if hidden_linear[j] > 0 else 0.0 for j in range(3)]

        for i in range(2):
            for j in range(3):
                grads["W1"][i][j] += features[i] * dhidden_linear[j]
        for j in range(3):
            grads["b1"][j] += dhidden_linear[j]

    batch_size = float(len(batch))
    for key in ("W1", "W2"):
        for i, row in enumerate(grads[key]):
            for j, value in enumerate(row):
                grads[key][i][j] = value / batch_size
    for key in ("b1", "b2"):
        grads[key] = [value / batch_size for value in grads[key]]
    return loss / batch_size, grads


def _apply_step(params: dict[str, list], grads: dict[str, list], learning_rate: float) -> dict[str, list]:
    updated = deepcopy(params)
    for key in ("W1", "W2"):
        for i, row in enumerate(updated[key]):
            for j, value in enumerate(row):
                updated[key][i][j] = value - learning_rate * grads[key][i][j]
    for key in ("b1", "b2"):
        for i, value in enumerate(updated[key]):
            updated[key][i] = value - learning_rate * grads[key][i]
    return updated


def numeric_gradient_w2_00(params: dict[str, list], batch: list[tuple[list[float], int]], eps: float = 1e-5) -> float:
    plus = deepcopy(params)
    minus = deepcopy(params)
    plus["W2"][0][0] += eps
    minus["W2"][0][0] -= eps
    plus_loss, _ = loss_and_grads(plus, batch)
    minus_loss, _ = loss_and_grads(minus, batch)
    return (plus_loss - minus_loss) / (2 * eps)


def numeric_gradient(
    params: dict[str, list],
    param_name: str,
    index: tuple[int, ...],
    batch: list[tuple[list[float], int]],
    eps: float = 1e-5,
) -> float:
    """通用中心差分：对 params[param_name][index] 扰动后计算数值梯度。

    - param_name: 'W1' / 'b1' / 'W2' / 'b2'（字典键）；
    - index: 标量元素索引，如 (0, 0) 表示 W2[0][0]；向量参数用 (i,) 表示 b1[i]；
    - 返回 (loss(W+e) - loss(W-e)) / (2·eps)。
    """
    if len(index) == 1:
        target = params[param_name][index[0]]
    else:
        target = params[param_name][index[0]][index[1]]

    plus = deepcopy(params)
    minus = deepcopy(params)
    if len(index) == 1:
        plus[param_name][index[0]] = target + eps
        minus[param_name][index[0]] = target - eps
    else:
        plus[param_name][index[0]][index[1]] = target + eps
        minus[param_name][index[0]][index[1]] = target - eps

    plus_loss, _ = loss_and_grads(plus, batch)
    minus_loss, _ = loss_and_grads(minus, batch)
    return (plus_loss - minus_loss) / (2 * eps)


def gradient_check_table(
    params: dict[str, list], batch: list[tuple[list[float], int]], eps: float = 1e-5
) -> list[dict[str, float]]:
    """对全部参数元素做一次梯度检查，返回相对误差表（Q5 验收对象）。

    相对误差：|num - an| / max(1, |num|, |an|)；全部元素应 < 1e-4（eps=1e-5 时）。
    """
    _, an_grads = loss_and_grads(params, batch)
    rows: list[dict[str, float]] = []
    for name in ("W1", "b1", "W2", "b2"):
        param = params[name]
        if isinstance(param[0], list):  # 矩阵参数
            for i in range(len(param)):
                for j in range(len(param[i])):
                    num = numeric_gradient(params, name, (i, j), batch, eps)
                    an = an_grads[name][i][j]
                    denom = max(1.0, abs(num), abs(an))
                    rows.append(
                        {
                            "param": name,
                            "index": f"[{i}][{j}]",
                            "analytic": round(an, 8),
                            "numeric": round(num, 8),
                            "relative_error": round(abs(num - an) / denom, 8),
                        }
                    )
        else:  # 向量参数
            for i in range(len(param)):
                num = numeric_gradient(params, name, (i,), batch, eps)
                an = an_grads[name][i]
                denom = max(1.0, abs(num), abs(an))
                rows.append(
                    {
                        "param": name,
                        "index": f"[{i}]",
                        "analytic": round(an, 8),
                        "numeric": round(num, 8),
                        "relative_error": round(abs(num - an) / denom, 8),
                    }
                )
    return rows


def max_gradient_error(
    params: dict[str, list], batch: list[tuple[list[float], int]], eps: float = 1e-5
) -> float:
    """返回梯度检查表中最大相对误差（smoke 自检用）。"""
    return max(row["relative_error"] for row in gradient_check_table(params, batch, eps))


def run_smoke(tiny_batch_csv: Path, overfit_batch_csv: Path) -> dict[str, object]:
    params = _init_params()
    tiny_batch = _dataset(tiny_batch_csv)
    overfit_batch = _dataset(overfit_batch_csv)

    initial_loss, grads = loss_and_grads(params, tiny_batch)
    numeric = numeric_gradient_w2_00(params, tiny_batch)
    analytic = grads["W2"][0][0]
    updated = _apply_step(params, grads, learning_rate=0.5)
    after_one_step_loss, _ = loss_and_grads(updated, tiny_batch)

    training_params = deepcopy(params)
    history = []
    for _ in range(40):
        current_loss, current_grads = loss_and_grads(training_params, overfit_batch)
        history.append(round(current_loss, 6))
        training_params = _apply_step(training_params, current_grads, learning_rate=0.6)

    return {
        "tiny_batch_size": len(tiny_batch),
        "initial_loss": round(initial_loss, 6),
        "after_one_step_loss": round(after_one_step_loss, 6),
        "numeric_gradient_w2_00": round(numeric, 6),
        "analytic_gradient_w2_00": round(analytic, 6),
        "gradient_diff": round(abs(numeric - analytic), 8),
        "overfit_loss_history_head": history[:5],
        "overfit_final_loss": history[-1],
    }
