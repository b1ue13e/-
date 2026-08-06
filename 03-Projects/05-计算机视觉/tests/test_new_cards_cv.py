"""验证 03-视觉核心任务/ 新增 5 张卡内代码示例真实可运行（2026-08-06 阶段3 缺口补卡）。"""
import numpy as np
import torch
import torch.nn.functional as F


def focal_loss(logits, targets, alpha=0.25, gamma=2.0):
    ce = F.cross_entropy(logits, targets, reduction="none")
    pt = torch.exp(-ce)
    w = alpha * (1 - pt) ** gamma
    return (w * ce).mean()


def test_focal_loss_focuses_hard_samples():
    """长尾分布卡例2：难分样本损失 > 易分样本损失（调制因子压低易分样本）"""
    torch.manual_seed(0)
    # 易分：logits 在正确类别上很大（pt 高）
    easy_logits = torch.zeros(4, 10); easy_logits[:, 0] = 5.0
    targets = torch.zeros(4, dtype=torch.long)
    # 难分：logits 均匀（pt 低）
    hard_logits = torch.zeros(4, 10)
    targets_h = torch.zeros(4, dtype=torch.long)
    easy = focal_loss(easy_logits, targets)
    hard = focal_loss(hard_logits, targets_h)
    assert hard.item() > easy.item() * 10, (easy.item(), hard.item())


def test_triplet_loss_positive_closer():
    """度量学习卡例2：正样本接近时损失小"""
    torch.manual_seed(0)
    a = F.normalize(torch.randn(4, 128))
    p = F.normalize(a + 0.05 * torch.randn(4, 128))
    n = F.normalize(torch.randn(4, 128))
    d_pos = F.pairwise_distance(a, p, p=2)
    d_neg = F.pairwise_distance(a, n, p=2)
    loss = torch.clamp(d_pos - d_neg + 0.5, min=0.0).mean()
    assert loss.item() >= 0.0
    assert d_pos.mean().item() < d_neg.mean().item()


def test_mask_head_only_gt_class_channel():
    """实例分割卡例2：mask 损失只计算 GT 类别通道（每类 sigmoid）"""
    torch.manual_seed(0)
    N, K = 3, 5
    logits = torch.randn(N, K, 8, 8)
    gt_classes = torch.tensor([1, 3, 0])
    gt_masks = (torch.rand(N, 8, 8) > 0.5).float()
    loss = 0.0
    for i in range(N):
        c = gt_classes[i].item()
        logit = logits[i, c]
        loss = loss + F.binary_cross_entropy_with_logits(logit, gt_masks[i])
    loss = loss / N
    assert loss.item() > 0.0


def test_heatmap_peak_location():
    """姿态估计卡例1：热力图峰值位置 == 关节坐标"""
    h, w = 64, 64
    ys, xs = np.mgrid[0:h, 0:w]
    cx, cy, sigma = 30.0, 40.0, 2.0
    H = np.exp(-((xs - cx) ** 2 + (ys - cy) ** 2) / (2 * sigma ** 2))
    peak = np.unravel_index(H.argmax(), H.shape)
    assert abs(peak[0] - cy) <= 1 and abs(peak[1] - cx) <= 1  # (y, x) 顺序


def test_triplet_hard_mining_proportion():
    """度量学习卡：随机采样三元组大多不激活（损失为 0 比例高）"""
    torch.manual_seed(1)
    a = F.normalize(torch.randn(64, 128))
    p = F.normalize(a + 0.02 * torch.randn(64, 128))   # 正样本很近
    n = F.normalize(torch.randn(64, 128))              # 负样本随机
    d_pos = F.pairwise_distance(a, p, p=2)
    d_neg = F.pairwise_distance(a, n, p=2)
    activated = (d_pos - d_neg + 0.5 > 0).float().mean()
    assert activated.item() < 0.5   # 大部分三元组已满足约束 → 需要 hard mining
