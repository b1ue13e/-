# AI Agent 工程

这是一个可复现的课程工程样例，不是已经接入真实模型、云服务或 MCP/A2A 生产环境的完整产品。项目把稳定控制面拆成可离线验收的 Python 包，并明确区分单元测试、本地 HTTP adapter smoke 与未验证的外部服务。

## 运行

从本目录执行：

```powershell
$env:PYTHONIOENCODING='utf-8'
python -m unittest discover -s tests -v
python -m scripts.readiness_smoke
python -m scripts.run_eval
python -m scripts.audit_course_structure
```

核心没有第三方运行依赖。需要验证可安装性时执行：

```powershell
python -m pip wheel . --no-deps --no-build-isolation --wheel-dir artifacts/wheel
```

从仓库根先 `Set-Location '03-Projects/46-AI Agent工程'`，再运行上述命令。项目的核心通过声明只覆盖离线样例和本机回环 HTTP adapter，不覆盖真实模型、Foundry、AutoGen、MCP/A2A、外部网络、Berkeley starter 或隐藏测试。

## 代码边界

- `scripts/curriculum_labs.py`：课程形成性小实验。
- `scripts/agent_runtime.py`：状态机、工具契约、checkpoint、一次性审批收据、HTTP 决策 adapter 和沙箱边界。
- `scripts/run_eval.py`：运行 20 正常、10 异常、10 对抗样本并生成逐样本报告。
- `scripts/readiness_smoke.py`：检查包导入、runtime、审批写入和评测 Gate。
- `scripts/security_harness.py`：基于动作效果的安全策略与指标。
- `scripts/autogen02_smoke.py`：历史 AutoGen 兼容 smoke，需单独安装固定依赖，失败不得混入核心通过。
- `data/eval_cases.jsonl`：课程原创离线评测集。
- `artifacts/eval/latest.json`：由评测脚本生成的真实运行记录。

## 验收状态

当前为 `full_course` 整改，完成后执行 C 级非独立复评，不等于正式发布。每次修改都应同步 `质量审计/课程重构执行清单.md` 和 `质量审计/课程严苛审计.md`，记录实际命令、版本、失败样本和未验证边界。
