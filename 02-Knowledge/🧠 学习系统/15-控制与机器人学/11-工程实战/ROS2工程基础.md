---
type: study
topic: "ROS2工程基础"
course: "控制与机器人学"
created: 2026-08-09
updated: 2026-08-09
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段11-工程实战]]"
flow: knowledge
kind: concept
concept: ["ROS2", "节点通信", "工程结构"]
prerequisites: ["Python编程基础", "仿真平台"]
related: ["TF2坐标变换", "ROS可视化与调试"]
upstream: ["[[仿真平台]]"]
source: "ROS 2 Documentation (docs.ros.org)；Design of ROS 2 (P. Estefo 等)"
tags: [学习, 控制与机器人学, 工程实战, ROS]
---

# ROS2工程基础

## 0. 为什么学它

机器人软件不是单个程序，而是**一堆节点互相通信的分布式系统**——传感器节点、估计节点、规划节点、控制节点。ROS2 提供这套通信框架：节点/话题/服务/参数/launch + DDS 底层，还引入生命周期节点与实时性支持。本卡是"把控制算法部署成机器人软件"的第一课，覆盖节点通信模型与工程结构。

## 1. 通信模型

| 机制 | 模式 | 用途 |
|:---|:---|:---|
| 话题（Topic） | 发布/订阅，异步流 | 传感器数据、状态广播（高频） |
| 服务（Service） | 请求/响应，同步 | 一次性调用（查询参数、触发动作） |
| 动作（Action） | 目标/反馈/结果，长任务 | 导航、机械臂运动（可取消） |
| 参数（Parameter） | 键值存储 | 动态配置（PID 增益、权重） |

## 2. 工程结构（包）

```
my_pkg/
├── package.xml      # 包元数据与依赖
├── CMakeLists.txt   # 构建配置（或 setup.py）
├── launch/          # launch 文件（启动整套节点）
└── src/             # 节点源码
```

**launch 文件**用 Python/XML 一次性拉起多节点，替代手动逐个 `ros2 run`。

## 3. 最小可运行例子（Python 节点）

```python
# talker.py —— 发布者
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class Talker(Node):
    def __init__(self):
        super().__init__("talker")
        self.pub = self.create_publisher(Float64, "cmd_vel", 10)
        self.timer = self.create_timer(0.1, self.tick)  # 10 Hz
        self.v = 0.0

    def tick(self):
        self.v += 0.1
        self.pub.publish(Float64(data=self.v))
        self.get_logger().info(f"发布速度: {self.v:.2f}")

def main():
    rclpy.init()
    rclpy.spin(Talker())
    rclpy.shutdown()
```

**运行说明**：`colcon build` 后 `ros2 run my_pkg talker`；另开终端 `ros2 topic echo /cmd_vel` 可看到 10 Hz 的速度消息——这就是"控制指令发布"的最小节点。

## 4. DDS 与实时性

- **DDS**（Data Distribution Service）：ROS2 默认底层通信中间件，提供 QoS（可靠性/历史深度/时效性）配置；
- **生命周期节点**：显式管理节点状态（未配置→未激活→激活→关闭），适合需要启动顺序的系统；
- **实时 ROS2**：用实时内核 + 锁内存 + 零拷贝传输，使控制回路延迟确定。

## 5. 常见坑

| 坑 | 对策 |
|:---|:---|
| 话题名拼写不一致 | `ros2 topic list` 核对；用命名空间隔离 |
| QoS 不匹配（发布/订阅协商失败） | 统一 QoS 策略（可靠 vs 尽力、深度） |
| 忘记 `rclpy.spin()` | 节点必须 spin 才能处理消息/回调 |
| 回调里做重活阻塞控制 | 回调只收发数据，计算放独立线程/节点 |

## 6. 检索练习（闭卷）

1. 画出 Topic/Service/Action/Parameter 四种机制对比表；
2. 写出一个发布者节点的最小结构；
3. 为什么控制节点要用独立高频话题而不是服务？
4. DDS 在 ROS2 中的角色与 QoS 的作用？

## 7. 通过标准

- 能区分四种通信机制并选型；
- 能写一个发布/订阅节点并跑通；
- 能用 launch 文件组织多节点；
- 能解释 DDS/QoS 与生命周期节点。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：写一个"订阅 /cmd_vel + 发布 /odom"的节点对；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；
- 关联：[[TF2坐标变换\|TF2坐标变换]]、[[ROS可视化与调试\|ROS可视化与调试]]。
