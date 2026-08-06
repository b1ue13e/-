"""验证 00-前置知识/ 两张前置卡内的代码示例真实可运行（2026-08-06 新增前置卡配套测试）。"""
import numpy as np


def test_numpy_reshape_and_dtype():
    """前置卡1：创建数组、切片、uint8 溢出防护"""
    gray = np.array([
        [10, 20, 30, 40, 50, 60],
        [15, 25, 35, 45, 55, 65],
        [20, 30, 40, 50, 60, 70],
        [25, 35, 45, 55, 65, 75],
    ], dtype=np.uint8)
    assert gray.shape == (4, 6)
    assert gray[0, 0] == 10
    img = np.zeros((2, 2, 3), dtype=np.uint8)
    img_int = img.astype(np.int16)
    img_int[:, :, 0] = np.clip(img_int[:, :, 0] + 30, 0, 255)
    out = img_int.astype(np.uint8)
    assert out.dtype == np.uint8 and out.shape == (2, 2, 3)


def test_numpy_broadcast_rgb_shift():
    """前置卡1：给所有像素 R 通道加 30（广播）"""
    img = np.random.randint(0, 256, size=(8, 8, 3), dtype=np.uint8)
    img_int = img.astype(np.int16)
    img_int[:, :, 0] = np.clip(img_int[:, :, 0] + 30, 0, 255)
    out = img_int.astype(np.uint8)
    assert out.shape == (8, 8, 3)


def test_numpy_knn_distance_matrix():
    """前置卡1 例子3：kNN 距离矩阵向量化"""
    rng = np.random.default_rng(0)
    X_train = rng.random((500, 3072))
    X_test = rng.random((10, 3072))
    d2 = (X_test[:, None, :] - X_train[None, :, :]) ** 2
    dist = d2.sum(axis=2) ** 0.5
    assert dist.shape == (10, 500)
    expected = np.sqrt(((X_test[0] - X_train[0]) ** 2).sum())
    assert abs(dist[0, 0] - expected) < 1e-9


def test_broadcast_hw3_compat():
    """前置卡1 自测3：A(4,1,6) + B(3,6) 合法且结果为 (4,3,6)"""
    A = np.zeros((4, 1, 6))
    B = np.zeros((3, 6))
    C = A + B
    assert C.shape == (4, 3, 6)


def test_chain_rule_two_layer_net():
    """前置卡2 例子2：链式法则解析梯度 == 数值梯度"""
    def loss_fn(x, w1, w2, t):
        y = w2 * (1 / (1 + np.exp(-w1 * x)))
        return 0.5 * (y - t) ** 2

    x, w1, w2, t = 2.0, 0.5, 1.5, 0.0
    eps = 1e-6
    g_w1_num = (loss_fn(x, w1 + eps, w2, t) - loss_fn(x, w1 - eps, w2, t)) / (2 * eps)
    g_w2_num = (loss_fn(x, w1, w2 + eps, t) - loss_fn(x, w1, w2 - eps, t)) / (2 * eps)

    y = w2 * (1 / (1 + np.exp(-w1 * x)))
    a = w1 * x
    s = 1 / (1 + np.exp(-a))
    g_w1_an = (y - t) * (s * (1 - s) * w2) * x
    g_w2_an = (y - t) * s

    assert abs(g_w1_an - g_w1_num) < 1e-5
    assert abs(g_w2_an - g_w2_num) < 1e-5


def test_sigmoid_derivative_property():
    """前置卡2：sigma'(a) = sigma(a)(1-sigma(a))"""
    a = np.array([-2.0, 0.0, 2.0])
    s = 1 / (1 + np.exp(-a))
    eps = 1e-6
    s_p = 1 / (1 + np.exp(-(a + eps)))
    s_m = 1 / (1 + np.exp(-(a - eps)))
    num = (s_p - s_m) / (2 * eps)
    assert np.allclose(num, s * (1 - s), atol=1e-6)
