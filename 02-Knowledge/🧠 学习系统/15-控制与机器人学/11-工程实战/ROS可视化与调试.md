---
type: study
topic: "ROS可视化与调试"
course: "控制与机器人学"
created: 2026-08-09
updated: 2026-08-09
status: completed
difficulty: beginner
stage_moc: "[[🧭 阶段11-工程实战]]"
flow: knowledge
kind: concept
concept: ["RViz", "rosbag", "调试工具链"]
prerequisites: ["ROS2工程基础"]
related: ["TF2坐标变换", "ROS2工程基础"]
upstream: ["[[ROS2工程基础]]"]
source: "ROS 2 官方文档（RViz2/rosbag2/rqt）"
tags: [学习, 控制与机器人学, 工程实战, ROS]
---

# ROS可视化与调试

## 0. 为什么学它

机器人系统"看不见摸不着"，出问题全靠工具：**RViz 可视化（模型/传感器/路径）、rqt 监控（曲线/日志）、rosbag 录放（数据回放）**。这三件套是 ROS 开发的"示波器 + 录屏 + 日志系统"——不会用它们，排查问题只能靠猜。本卡是工程实战的调试入门。

## 1. 工具三件套

| 工具 | 作用 | 典型场景 |
|:---|:---|:---|
| RViz2 | 3D 可视化（模型/点云/路径/位姿） | 看机器人状态、传感器数据、TF |
| rqt | 2D 面板（曲线图/日志/话题监控） | 实时看控制量、误差曲线 |
| rosbag2 | 数据录制与回放 | 复现问题、离线调参、回放测试 |

## 2. 最小使用流程

```bash
# 录制所有话题（跑 10 秒）
ros2 bag record -a -o my_bag

# 回放
ros2 bag play my_bag

# RViz 可视化（需可视化配置）
ros2 run rviz2 rviz2

# rqt 看话题曲线
ros2 run rqt_plot rqt_plot /cmd_vel/data
```

**调试工作流**：实车/仿真跑一遍 → `rosbag record` 全量录制 → 离线回放 → RViz/rqt 分析 → 改参 → 复测。**先录后调**，避免"现场复现难"。

## 3. 常见坑

| 坑 | 对策 |
|:---|:---|
| 录制时没开记录（事后想复现） | 养成"每轮实验必录 bag"的习惯 |
| RViz 不显示模型 | 检查 TF 是否发布、Fixed Frame 是否选对 |
| 回放时话题时间戳混乱 | 回放加 `--clock` 与 `use_sim_time` 对齐 |
| rqt 曲线刷太快看不清 | 调采样/降频，或先录 bag 再离线画 |

## 4. 检索练习（闭卷）

1. 说出三件套工具与作用；
2. 写出一条完整的"录制→回放→分析"命令链；
3. RViz 不显示模型的三个排查方向；
4. 为什么推荐"先录后调"？

## 5. 通过标准

- 能录制并回放 rosbag；
- 能在 RViz 查看机器人模型/传感器数据；
- 能用 rqt 查看控制量与误差曲线；
- 能按"录→放→析→改"流程排查问题。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：用 rqt_plot 观察 PID 阶跃响应曲线并分析超调；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；
- 关联：[[ROS2工程基础\|ROS2工程基础]]、[[TF2坐标变换\|TF2坐标变换]]。
