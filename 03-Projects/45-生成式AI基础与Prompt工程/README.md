# 生成式 AI 基础与 Prompt 工程项目包

本目录是课程的唯一作业与可执行证据中心。代码只依赖 Python 3.11+ 标准库；离线 runner 用于验证数据流、schema、受控实验、RAG、Judge 和安全策略协议，不代表真实模型能力。

## 目录

```text
├── 🧭 课程作业总索引.md
├── 课后作业/
├── 阶段作业/
├── 大作业/
├── scripts/course_lab.py
├── tests/test_course_lab.py
├── artifacts/
└── 质量审计/
```

## 一键验证

```powershell
cd "F:\-\03-Projects\45-生成式AI基础与Prompt工程"
python -m unittest discover -s tests -v
0..7 | ForEach-Object {
  $id = $_.ToString("00")
  python scripts/course_lab.py $id --output "artifacts/assignment$id-offline.json"
  if ($LASTEXITCODE -ne 0) { throw "assignment $id gate failed" }
}
```

单项命令：

```powershell
python scripts/course_lab.py 00 --output artifacts/assignment00-offline.json
python scripts/course_lab.py 01 --output artifacts/assignment01-offline.json
python scripts/course_lab.py 02 --adapter rule --output artifacts/assignment02-offline.json
python scripts/course_lab.py 03 --adapter rule --output artifacts/assignment03-offline.json
python scripts/course_lab.py 04 --output artifacts/assignment04-offline.json
python scripts/course_lab.py 05 --output artifacts/assignment05-offline.json
python scripts/course_lab.py 06 --output artifacts/assignment06-offline.json
python scripts/course_lab.py 07 --output artifacts/assignment07-offline.json
```

所有离线报告都包含 `evidence_scope: "protocol_only"`。退出码 0 表示固定 Gate 通过，2 表示 Gate 失败。

## 真实模型

仅作业 02/03 提供 OpenAI-compatible chat-completions adapter：

```powershell
$env:OPENAI_API_KEY="在本机设置，不写入仓库"
$env:OPENAI_BASE_URL="https://api.openai.com/v1"
python scripts/course_lab.py 02 --adapter openai --model "模型ID" --output artifacts/assignment02-live.json
python scripts/course_lab.py 03 --adapter openai --model "模型ID" --output artifacts/assignment03-live.json
```

adapter 保存服务返回的 model/usage 元数据。价格、模型可用性、网络和凭据不在离线测试范围；成本应按运行当日供应商价格另算。服务不兼容时修改 adapter 边界，不修改冻结数据、parser 或评分规则。

## 渐隐支架

| 层次 | 任务 | 完成证据 |
| :--- | :--- | :--- |
| 示范复现 | 跑离线 Gate 并解释正确/失败样本 | 能说明 fixture 不是模型证据 |
| 补全题 | 新建 `ModelAdapter` 实现，保留数据、parser 与测试 | 全部测试通过，非法 JSON 失败关闭 |
| 独立迁移 | 更换任务、标签与冻结数据 | 原始输出、指标、错误分类和回退结论齐全 |

排错顺序固定为：输入 schema → raw output → parser → Prompt → adapter。禁止通过修改测试标签、删除失败样本或只选最佳 seed 提高分数。

## 交付边界

提交代码、JSON 报告、环境信息、Prompt 版本、模型/adapter 标识、逐样本结果和失败复盘。不要提交 API Key、私有 URL、个人数据或未获许可的第三方材料。
