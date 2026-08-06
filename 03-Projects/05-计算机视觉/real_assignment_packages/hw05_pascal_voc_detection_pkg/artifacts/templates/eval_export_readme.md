# HW05 Evaluation Export Guide

这个模板用于把 Pascal VOC 子集评测结果导出成可复核的逐图像记录。

## 字段说明

- `image_id`：图像唯一标识
- `split`：训练 / 验证 / 测试切分
- `class_name`：当前记录的类别
- `gt_count`：该类别在当前图像中的真实框数量
- `pred_count`：该类别在当前图像中的预测框数量
- `tp / fp / fn`：在固定阈值下的真阳、假阳、漏检数量
- `best_iou`：最佳匹配框的 IoU
- `score_threshold`：本次导出采用的分数阈值
- `note`：人工补充说明，例如遮挡、背景混淆、小目标等

## 建议导出时机

- 每次正式评测后导出一次
- 更换阈值或 NMS 策略后重新导出
- 准备写失败案例分析前，先冻结一版导出表
