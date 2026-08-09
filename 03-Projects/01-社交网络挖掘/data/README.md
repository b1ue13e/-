# 数据目录

`generated/` 由下面的命令创建，可以删除后重建：

```powershell
python scripts/generate_course_data.py --output data/generated --seed 42
```

合成 fixture 只用于协议、算法 oracle 和 starter 回归，不是 Capstone 的最终数据证据，也不能支持真实人群结论。每次生成都会写入 `generation_manifest.json`，其中包含种子、行数、SHA-256、文件角色和禁止进入特征的字段。

- `node_features.csv` 只包含 `node` 与 `feature_*`，可进入模型。
- `node_labels.csv` 只用于训练结束后的评价，不得进入无监督表示或结构特征。
- `structure_edges.csv` 是结构、社区和传播任务共用的静态图，不再复制三份同内容边表。
- `temporal_edges.csv` 是时间链接预测的合成预检事件流。

## 必做真实数据轨道

正式 Capstone 使用 SocioPatterns High School 2013 接触网络：

```powershell
python scripts/fetch_public_network.py --output data/external/high-school-2013
python starter/run_baseline.py --events data/external/high-school-2013/temporal_edges.csv --undirected --output artifacts/starter-real
```

下载脚本固定官方 URL 与 SHA-256，并生成 `dataset_manifest.json`。数据采用 `CC BY-NC-SA 3.0`，只能按许可证进行非商业、署名、相同方式共享的使用；课程仓库不镜像上游压缩包。

真实数据不得直接提交到知识卡目录。添加真实数据前，先在作业 manifest 中记录 URL、访问日期、许可、下载哈希、字段语义、脱敏和删除策略。
