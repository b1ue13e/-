# AI Agent 工程运行脚本

本目录保存课程原创的离线 worked baseline，不是 Berkeley starter 或 Microsoft/Datawhale 官方实现。

## 入口

- `curriculum_labs.py`：P0–P8 的小型确定性函数与演示。
- `agent_runtime.py`：工具注册、消息 handoff、状态机、trace、checkpoint、沙箱与审批。
- `run_eval.py`：执行 20/10/10 离线评测集并保存逐样本报告。
- `readiness_smoke.py`：验证包导入、审批写入、最小 runtime 与评测 Gate。
- `restaurant_pipeline.py`：餐厅评论本地等价管线。
- `security_harness.py`：基于危险效果的安全策略与指标。
- `autogen02_smoke.py`：历史 AutoGen 0.2 导入、双注册和终止 smoke；需单独安装 `requirements-autogen02.txt`。

## 运行

从项目根目录执行：

```powershell
python -m scripts.readiness_smoke
python -m scripts.run_eval
python -m unittest discover -s tests -v
```

课程核心测试只依赖 Python 3.11+ 标准库。AutoGen smoke 必须在隔离环境安装固定依赖后单独执行；没有依赖或真实模型配置时，不得声称历史官方环境通过。
