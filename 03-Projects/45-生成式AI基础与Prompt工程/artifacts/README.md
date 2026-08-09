# 离线证据清单

生成日期：2026-08-09

## 结果

| 作业 | 文件 | Gate | 证据范围 |
| :---: | :--- | :---: | :--- |
| 00 | `assignment00-offline.json` | pass | Python/JSON/Softmax 前置协议 |
| 01 | `assignment01-offline.json` | pass | 生成循环、causal mask 与解码协议 |
| 02 | `assignment02-offline.json` | pass | 固定数据、adapter、schema 与解析协议 |
| 03 | `assignment03-offline.json` | pass | 单变量 Prompt 实验与多顺序留痕协议 |
| 04 | `assignment04-offline.json` | pass | parse/execute/verify 分解协议 |
| 05 | `assignment05-offline.json` | pass | JSON 校验与 Judge 位置交换协议 |
| 06 | `assignment06-offline.json` | pass | 检索、引用、拒答和不可信文档隔离协议 |
| 07 | `assignment07-offline.json` | pass | 类型化来源/动作安全策略协议 |

八份报告均包含 `evidence_scope: "protocol_only"`。这些结果证明固定离线夹具和验收协议可运行，不证明任何真实 LLM、embedding、reranker、Judge 或生产安全能力。

## 复现

```powershell
python -m unittest discover -s tests -v
0..7 | ForEach-Object {
  $id = $_.ToString("00")
  python scripts/course_lab.py $id --output "artifacts/assignment$id-offline.json"
  if ($LASTEXITCODE -ne 0) { throw "assignment $id gate failed" }
}
```

作业 02/03 使用 `--adapter rule` 明示离线 adapter；README 中提供真实模型命令。当前没有运行真实模型、产生费用或验证外部服务。
