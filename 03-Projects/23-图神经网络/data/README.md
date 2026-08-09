# 数据契约

主线实验使用 `starter/gnn_course/data.py` 生成确定性的 12 节点双社区图，不下载外部数据，不把 toy 结果冒充公开 benchmark 结果。

数据契约：

- 节点特征：`x.shape == (12, 4)`；
- 邻接矩阵：对称、无自环原始矩阵，模型内部显式加自环；
- 标签：两类社区标签；
- split：固定 transductive 节点分类掩码，train/val/test 两两不交；
- manifest：运行时写入 `artifacts/*/split_manifest.json`，包含图哈希、协议和 seed。

外部 OGB/PyG 数据是可选扩展，必须单独记录数据集版本、许可和官方 evaluator。
