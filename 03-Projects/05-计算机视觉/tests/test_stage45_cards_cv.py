"""验证 04/05 阶段新增 5 张卡内代码示例真实可运行（2026-08-06 阶段4/5 缺口补卡）。"""
import numpy as np
import torch
import torch.nn as nn


class DepthwiseSeparable(nn.Module):
    def __init__(self, dim, kernel_size=7):
        super().__init__()
        self.dw = nn.Conv2d(dim, dim, kernel_size, padding=kernel_size // 2, groups=dim, bias=False)
        self.pw = nn.Conv2d(dim, dim, 1, bias=False)

    def forward(self, x):
        return self.pw(self.dw(x))


def test_depthwise_separable():
    """Transformer架构演进卡例2：深度可分离卷积形状与参数"""
    m = DepthwiseSeparable(96, 7)
    x = torch.randn(1, 96, 56, 56)
    out = m(x)
    assert out.shape == (1, 96, 56, 56)
    n_dw = 96 * 7 * 7
    n_pw = 96 * 96
    total = sum(p.numel() for p in m.parameters())
    assert total == n_dw + n_pw


def test_brightness_constancy():
    """光流估计卡例2：正确光流下亮度恒常残差接近 0"""
    rng = np.random.default_rng(0)
    I1 = rng.random((16, 16))
    I2 = np.roll(np.roll(I1, shift=2, axis=1), shift=1, axis=0)  # 右移2、下移1
    H, W = I1.shape
    u, v = 2.0, 1.0
    ys, xs = np.mgrid[0:H, 0:W]
    x2 = np.clip(xs + u, 0, W - 1).astype(int)
    y2 = np.clip(ys + v, 0, H - 1).astype(int)
    res = I2[y2, x2] - I1
    # 忽略 roll 回绕边界（clip 使 u=2/v=1 在右/下边界出错，roll 使左/上边界回绕）
    assert np.abs(res[3:-1, 3:-1]).mean() < 0.05


def test_pointnet_permutation_invariance():
    """点云与3D感知卡例1：PointNet 式 max 池化置换不变"""
    def pointnet_style(x, W1, W2):
        h = np.maximum(x @ W1, 0)
        pooled = h.max(axis=0)
        return pooled @ W2

    rng = np.random.default_rng(0)
    pts = rng.random((100, 3))
    W1 = rng.random((3, 8))
    W2 = rng.random((8, 4))
    perm = rng.permutation(100)
    assert np.allclose(pointnet_style(pts, W1, W2), pointnet_style(pts[perm], W1, W2))


def test_stereo_depth_formula():
    """点云与3D感知卡例2：Z = fB/d，视差越大越近"""
    f, B = 500.0, 0.12
    d = np.array([10, 20, 50, 100], dtype=float)
    Z = f * B / d
    assert Z[0] > Z[1] > Z[2] > Z[3]      # 视差增大 → 深度减小
    assert np.allclose(Z, f * B / d)


def test_pinhole_backprojection():
    """自动驾驶感知卡：像素+深度 → 相机坐标 → 车体坐标"""
    rng = np.random.default_rng(0)
    # 简单相机: K = diag(f, f, 1)，无旋转平移
    f = 500.0
    K_inv = np.diag([1 / f, 1 / f, 1.0])
    R = np.eye(3)
    t = np.zeros(3)
    u, v, d = 250.0, 200.0, 10.0
    ray = np.array([u, v, 1.0])
    x_cam = d * K_inv @ ray                       # (x_c, y_c, z_c) z_c = d
    x_world = R.T @ (x_cam - t)                    # 无变换时等于 x_cam
    assert abs(x_world[2] - d) < 1e-6
    # 深度越深，世界点 x/y 越大（透视）
    x_far = 20.0 * K_inv @ ray
    assert x_far[0] > x_cam[0]
