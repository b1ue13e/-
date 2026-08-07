#!/usr/bin/env python3
"""Add explicit smoke/real modes and provenance to quant assignment packages."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "03-Projects" / "金融与时序" / "03-量化金融"
PACKAGES = PROJECT / "real_assignment_packages"
SNAPSHOT = ROOT / ".recovery-hold" / "2026-08-06" / "quant-finance-comprehensive"


PROVENANCE = {
    "HW01": ("local_integration_task", "https://python.quantecon.org/", "open online lectures; link-only"),
    "HW02": ("local_integration_task", "https://python.quantecon.org/", "open online lectures; link-only"),
    "HW03": ("local_integration_task", "[待验证]", "[待验证]"),
    "HW04": ("local_integration_task", "[待验证]", "[待验证]"),
    "HW05": ("local_integration_task", "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/pages/assignments/", "CC BY-NC-SA 4.0 for MIT OCW materials"),
    "HW06": ("local_integration_task", "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/pages/assignments/", "CC BY-NC-SA 4.0 for MIT OCW materials"),
    "HW07": ("local_integration_task", "[待验证]", "[待验证]"),
    "HW08": ("local_integration_task", "[待验证]", "[待验证]"),
    "HW09": ("local_integration_task", "[待验证]", "[待验证]"),
    "HW10": ("local_integration_task", "[待验证]", "[待验证]"),
    "HW11": ("local_integration_task", "[待验证]", "[待验证]"),
    "HW12": ("local_integration_task", "[待验证]", "[待验证]"),
    "HW13": ("local_integration_task", "[待验证]", "[待验证]"),
    "HW14": ("local_integration_task", "[待验证]", "[待验证]"),
    "HW15": ("local_integration_task", "[待验证]", "[待验证]"),
    "HW16": ("open_source_project_task", "https://github.com/AI4Finance-Foundation/FinRL", "Apache-2.0; verify fixed commit"),
    "HW17": ("open_source_project_task", "https://github.com/microsoft/qlib", "MIT for Qlib code; data terms source-specific"),
}


def packages() -> list[Path]:
    return sorted(path for path in PACKAGES.glob("hw*_*") if path.is_dir())


def upgrade_manifest(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    source_type, source_url, license_name = PROVENANCE[data["id"]]
    data.update({
        "source_type": source_type,
        "source_url": source_url,
        "license": license_name,
        "accessed": "2026-08-06",
        "random_seed": 42,
        "supported_modes": ["smoke", "real"],
        "solution_visibility": "private",
    })
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def upgrade_run(text: str) -> str:
    if 'parser.add_argument("--mode"' not in text:
        marker = '    parser.add_argument("--input-dir", required=True)\n'
        replacement = (
            '    parser.add_argument("--mode", choices=("smoke", "real"), default="smoke")\n'
            + marker
        )
        text = text.replace(marker, replacement)
    if "manifest = load_manifest()" in text and "selected_files =" not in text:
        text = text.replace(
            "    manifest = load_manifest()\n    input_dir = Path(args.input_dir)\n",
            "    manifest = load_manifest()\n"
            "    selected_files = manifest['smoke_files'] if args.mode == 'smoke' else manifest['real_files']\n"
            "    input_dir = Path(args.input_dir)\n"
            "    missing = [name for name in selected_files if not (input_dir / name).exists()]\n"
            "    if missing:\n"
            "        parser.error(f\"missing {args.mode} input files: {', '.join(missing)}\")\n",
        )
    smoke_names = re.findall(r'input_dir / "([^"]+\.smoke\.csv)"', text)
    for index, name in enumerate(smoke_names):
        text = text.replace(f'input_dir / "{name}"', f"input_dir / selected_files[{index}]", 1)
    text = text.replace('description="Run the ', 'description="Run the ')
    text = text.replace(" Smoke Run", " Run")
    if '"mode": args.mode,' not in text:
        payload_marker = '    payload = {\n'
        text = text.replace(payload_marker, payload_marker + '        "mode": args.mode,\n', 1)
    return text


def append_readme(text: str, manifest: dict) -> str:
    if "## 正式/烟雾双模式" in text:
        return text
    source_type, source_url, license_name = PROVENANCE[manifest["id"]]
    real_files = "、".join(f"`{name}`" for name in manifest["real_files"])
    addition = f'''

## 正式/烟雾双模式

- `--mode smoke`：读取 `*.smoke.csv`，仅验证接口与工程流程。
- `--mode real`：读取 manifest 的正式文件 {real_files}；缺文件时立即失败，不静默回退 smoke。
- 示例：`python starter/run.py --mode real --input-dir <data-dir> --output-dir <output-dir>`。
- 随机算法默认种子为 `42`；提交时记录解释器、依赖版本、硬件和实测运行时间。

## 来源与许可

- `source_type`: `{source_type}`
- `source_url`: `{source_url}`
- `license`: `{license_name}`
- 无法核验的上游材料保持 `[待验证]`；不得将公开访问误写为开放再分发。

## 提交产物

- 环境锁文件、数据 manifest、完成后的 starter/src、测试、`results/summary.json`、失败日志和报告。
- 正式结论必须由 `--mode real` 产生；smoke 输出只能标记为工程自检。
'''
    return text.rstrip() + addition + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.apply and not SNAPSHOT.exists():
        raise SystemExit(f"Missing recovery snapshot: {SNAPSHOT}")
    edits: list[tuple[Path, str]] = []
    for package in packages():
        manifest_path = package / "package_manifest.json"
        old_manifest = manifest_path.read_text(encoding="utf-8-sig")
        new_manifest = upgrade_manifest(manifest_path)
        edits.append((manifest_path, new_manifest))
        manifest = json.loads(new_manifest)
        run_path = package / "starter" / "run.py"
        old_run = run_path.read_text(encoding="utf-8-sig")
        new_run = upgrade_run(old_run)
        edits.append((run_path, new_run))
        readme_path = package / "README.md"
        old_readme = readme_path.read_text(encoding="utf-8-sig")
        edits.append((readme_path, append_readme(old_readme, manifest)))
    changes = [(path, text) for path, text in edits if text != path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")]
    print(f"mode={'apply' if args.apply else 'dry-run'}")
    print(f"packages={len(packages())}")
    print(f"changes={len(changes)}")
    for path, _ in changes:
        print(f"EDIT\t{path.relative_to(ROOT)}")
    if not args.apply:
        return 0
    for path, text in changes:
        path.write_text(text, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
