---
type: study
topic: "TF2坐标变换"
course: "控制与机器人学"
created: 2026-08-09
updated: 2026-08-09
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段11-工程实战]]"
flow: knowledge
kind: concept
concept: ["坐标变换", "TF树"]
prerequisites: ["ROS2工程基础", "齐次变换矩阵"]
related: ["ROS2工程基础", "ROS可视化与调试"]
upstream:
  - "[[ROS2工程基础]]"
  - "[[齐次变换矩阵]]"
source: "ROS 2 tf2 官方文档；Modern Robotics Ch.3 [待验证]"
tags: [学习, 控制与机器人学, 工程实战, ROS]
---

# TF2坐标变换

## 0. 为什么学它

机器人系统里每个传感器都有自己的坐标系：激光在 `laser` 系、相机在 `camera` 系、底盘在 `base_link` 系——**要回答"激光点在地图里在哪"，就必须做坐标变换**。TF2 是 ROS 的坐标变换管理库：维护一棵"TF 树"，按时间查询任意两坐标系之间的变换。本卡是"多传感器融合 + 运动规划"的坐标基础。

## 1. 核心概念

- **坐标系**：每个传感器/部件有自己的 frame（如 `map`、`odom`、`base_link`、`laser`、`camera`）；
- **TF 树**：坐标系间变换按父子关系组织成树（不能有环）；
- **变换查询**：给定源/目标坐标系 + 时间，返回变换矩阵/四元数。

## 2. 最小可运行例子（Python）

```python
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster, Buffer, TransformListener
from geometry_msgs.msg import TransformStamped

class TfEcho(Node):
    def __init__(self):
        super().__init__("tf_echo")
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)
        self.timer = self.create_timer(1.0, self.query)

    def query(self):
        # 查询 laser → base_link 的当前变换
        try:
            t = self.buffer.lookup_transform("base_link", "laser", rclpy.time.Time())
            print("平移:", t.transform.translation)
        except Exception as e:
            print("查询失败:", e)
```

**运行说明**：在已有机器人模型（发布 TF）的环境运行；查询失败通常是 TF 树不完整/时间戳未来——这是最经典的 TF 坑。

## 3. 常见坑

| 坑 | 对策 |
|:---|:---|
| "TF 查询失败：extrapolation" | 目标时间在未来（时钟不同步），用最新时间或等待 |
| 坐标系名拼写错误 | `ros2 run tf2_ros tf2_echo a b` 手动验证 |
| TF 树有环/断链 | 用 `tf2_tools view_frames` 生成 TF 树图检查 |
| 变换在错误时刻使用 | 查询时要带时间戳，传感器数据用其自身时间戳 |

## 4. 与理论的关系

- 底层是齐次变换矩阵链乘（见 [[齐次变换矩阵|齐次变换]]）；
- TF2 只是"管理 + 按时间查询"这些变换的工程化框架；
- 多传感器融合（见 [[导航定位|导航定位]]）要求所有测量先变换到统一坐标系。

## 5. 检索练习（闭卷）

1. 说明 TF 树的结构与约束；
2. 写一个 TF 查询节点并处理失败；
3. 列举三个常见 TF 坑与对策；
4. TF2 与齐次变换矩阵的关系？

## 6. 通过标准

- 能说明 TF 树结构与查询原理；
- 能写 TF 查询代码并调试失败；
- 能理解"传感器测量先变换到统一系"的融合前提；
- 能用 `view_frames` 检查 TF 树。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：为"激光雷达 → 底盘 → 地图"链路画出 TF 树；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；
- 关联：[[ROS2工程基础\|ROS2工程基础]]、[[导航定位\|导航定位]]。
