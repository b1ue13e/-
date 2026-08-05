#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成学科配图（自评项 4）：落实双重编码。

1. 复变函数：域着色图（domain coloring）示例 —— 用色相编码 arg，亮度编码 |z|，
   演示 f(z)=z^2 的零点、临界点与辐角旋转（对应卡 1 复数运算与复平面 / 卡 14 域着色画廊）。
2. 多元统计：二元正态等高线图 —— 演示马氏距离超椭球、特征向量主轴
   （对应卡 1 多元正态分布与性质）。

输出 PNG 到各课程目录，随后手动嵌入卡中。
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib/numpy 不可用，跳过配图生成")
    sys.exit(0)

VAULT = Path(r"F:\-")


def domain_coloring(f, xlim=(-2, 2), ylim=(-2, 2), n=400, out=None):
    """复函数域着色：色相=arg(f)，亮度=log|f| 归一化。"""
    xs = np.linspace(xlim[0], xlim[1], n)
    ys = np.linspace(ylim[0], ylim[1], n)
    X, Y = np.meshgrid(xs, ys)
    Z = X + 1j * Y
    W = f(Z)
    hue = (np.angle(W) + np.pi) / (2 * np.pi)  # [0,1)
    mag = np.abs(W)
    with np.errstate(divide="ignore"):
        lum = np.clip(0.15 + 0.85 * (np.log1p(mag) / np.log1p(np.max(mag) + 1e-12)), 0, 1)
    hsv = np.stack([hue, np.full_like(hue, 0.85), lum], axis=-1)
    # matplotlib 需要 RGB
    from matplotlib.colors import hsv_to_rgb
    rgb = hsv_to_rgb(hsv)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(rgb, extent=(xlim[0], xlim[1], ylim[0], ylim[1]), origin="lower")
    ax.set_title(r"Domain coloring: $f(z)=z^2$  (hue=arg, brightness=|z|)")
    ax.set_xlabel(r"$\mathrm{Re}\,z$")
    ax.set_ylabel(r"$\mathrm{Im}\,z$")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print(f"已生成: {out}")


def bivariate_normal_contour(out=None):
    """二元正态等高线：演示马氏距离椭球与主轴。"""
    mu = np.array([0.0, 0.0])
    Sigma = np.array([[2.0, 1.2], [1.2, 1.0]])
    # 特征分解求主轴
    vals, vecs = np.linalg.eigh(Sigma)
    xs = np.linspace(-4, 4, 300)
    ys = np.linspace(-4, 4, 300)
    X, Y = np.meshgrid(xs, ys)
    pos = np.stack([X, Y], axis=-1)
    diff = pos - mu
    # 马氏距离平方
    inv = np.linalg.inv(Sigma)
    md2 = np.einsum("...i,ij,...j->...", diff, inv, diff)
    fig, ax = plt.subplots(figsize=(6, 6))
    cf = ax.contourf(X, Y, md2, levels=[0, 1, 2.28, 4, 6, 9], cmap="Blues", alpha=0.8)
    ax.contour(X, Y, md2, levels=[2.28], colors="red", linewidths=2)  # 68% 区域
    # 主轴
    for i in range(2):
        vec = vecs[:, i] * np.sqrt(vals[i]) * 2.2
        ax.arrow(0, 0, vec[0], vec[1], color="black", width=0.05,
                 head_width=0.18, length_includes_head=True)
    ax.set_title(r"Bivariate normal: Mahalanobis contours (red=68%, arrows=principal axes)")
    ax.set_xlabel(r"$X_1$")
    ax.set_ylabel(r"$X_2$")
    ax.set_aspect("equal")
    fig.colorbar(cf, ax=ax, label=r"$(\mathbf{x}-\mu)'\Sigma^{-1}(\mathbf{x}-\mu)$")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print(f"已生成: {out}")


def main():
    complex_dir = VAULT / "02-Knowledge/🧠 学习系统/37-复变函数/04-保角映射与综合项目"
    stats_dir = VAULT / "02-Knowledge/🧠 学习系统/16-多元统计/01-基础矩阵"
    complex_dir.mkdir(parents=True, exist_ok=True)
    stats_dir.mkdir(parents=True, exist_ok=True)

    domain_coloring(lambda z: z**2, out=complex_dir / "域着色示例_z平方.png")
    bivariate_normal_contour(out=stats_dir / "多元正态等高线示例.png")


if __name__ == "__main__":
    main()
