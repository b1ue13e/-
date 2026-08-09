from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import yaml


PLACEHOLDER_PROVIDERS = {"", "unknown", "replace-before-qrun"}


def _date_pair(value: object) -> bool:
    if not isinstance(value, list) or len(value) != 2:
        return False
    try:
        return date.fromisoformat(str(value[0])) <= date.fromisoformat(str(value[1]))
    except ValueError:
        return False


def _timeline_is_ordered(handler: dict, segments: dict) -> bool:
    if not all(_date_pair(segments.get(name)) for name in ("train", "valid", "test")):
        return False
    try:
        start = date.fromisoformat(str(handler["start_time"]))
        end = date.fromisoformat(str(handler["end_time"]))
        fit_start = date.fromisoformat(str(handler["fit_start_time"]))
        fit_end = date.fromisoformat(str(handler["fit_end_time"]))
        train_start, train_end = (date.fromisoformat(str(value)) for value in segments["train"])
        valid_start, valid_end = (date.fromisoformat(str(value)) for value in segments["valid"])
        test_start, test_end = (date.fromisoformat(str(value)) for value in segments["test"])
    except (KeyError, ValueError):
        return False
    return (
        start <= fit_start <= fit_end <= train_end
        and start <= train_start <= train_end < valid_start <= valid_end < test_start <= test_end <= end
    )


def build_protocol_summary(
    manifest_path: Path, workflow_path: Path, baseline_path: Path
) -> dict[str, object]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    baselines = json.loads(baseline_path.read_text(encoding="utf-8"))

    task = workflow.get("task", {})
    model = task.get("model", {})
    dataset = task.get("dataset", {})
    dataset_kwargs = dataset.get("kwargs", {})
    handler = dataset_kwargs.get("handler", {})
    handler_kwargs = handler.get("kwargs", {})
    segments = dataset_kwargs.get("segments", {})
    records = {
        record.get("class"): record
        for record in task.get("record", [])
        if isinstance(record, dict)
    }
    signal_record = records.get("SignalRecord", {})
    portfolio_record = records.get("PortAnaRecord", {})
    portfolio_config = portfolio_record.get("kwargs", {}).get("config", {})
    strategy = portfolio_config.get("strategy", {})
    backtest = portfolio_config.get("backtest", {})
    exchange = backtest.get("exchange_kwargs", {})

    manifest_provider = str(manifest.get("provider_uri", "")).strip()
    workflow_provider = str(workflow.get("qlib_init", {}).get("provider_uri", "")).strip()
    provider_is_placeholder = workflow_provider.lower() in PLACEHOLDER_PROVIDERS
    required_handler = {"start_time", "end_time", "fit_start_time", "fit_end_time", "instruments"}
    required_exchange = {"freq", "limit_threshold", "deal_price", "open_cost", "close_cost", "min_cost"}
    checks = {
        "manifest_pins_qlib_version": manifest.get("qlib_version") == "0.9.7",
        "manifest_discloses_unverified_commit": manifest.get("qlib_source_commit") is None,
        "manifest_has_data_release": bool(manifest.get("data_release")),
        "manifest_has_data_license": bool(manifest.get("data_license")),
        "provider_matches_manifest": workflow_provider == manifest_provider,
        "model_is_lightgbm": model.get("class") == "LGBModel"
        and model.get("module_path") == "qlib.contrib.model.gbdt"
        and isinstance(model.get("kwargs"), dict),
        "dataset_is_dataseth": dataset.get("class") == "DatasetH"
        and dataset.get("module_path") == "qlib.data.dataset",
        "handler_is_complete_alpha158": handler.get("class") == "Alpha158"
        and handler.get("module_path") == "qlib.contrib.data.handler"
        and required_handler <= set(handler_kwargs),
        "segments_are_complete": set(segments) == {"train", "valid", "test"},
        "timeline_is_ordered": _timeline_is_ordered(handler_kwargs, segments),
        "signal_record_is_complete": signal_record.get("module_path")
        == "qlib.workflow.record_temp"
        and {"model", "dataset"} <= set(signal_record.get("kwargs", {})),
        "portfolio_record_is_complete": portfolio_record.get("module_path")
        == "qlib.workflow.record_temp"
        and strategy.get("class") == "TopkDropoutStrategy"
        and bool(strategy.get("module_path"))
        and "signal" in strategy.get("kwargs", {})
        and {"start_time", "end_time", "account", "benchmark", "exchange_kwargs"}
        <= set(backtest)
        and required_exchange <= set(exchange),
        "baselines_are_complete": set(baselines) == {"E0", "E1", "E2"},
    }
    template_valid = all(checks.values())
    if not template_valid:
        contract_status = "contract_invalid"
        execution_status = "blocked_on_invalid_template"
        blocked_reasons = [name for name, passed in checks.items() if not passed]
    elif provider_is_placeholder:
        contract_status = "contract_template_ready"
        execution_status = "blocked_on_provider"
        blocked_reasons = ["replace provider_uri and register provider release/license/checksum"]
    else:
        contract_status = "contract_config_declared_unverified"
        execution_status = "not_run"
        blocked_reasons = ["run qrun and preserve stdout/stderr/evidence before claiming execution"]

    return {
        "contract_status": contract_status,
        "contract_checks": checks,
        "provider_status": "placeholder" if provider_is_placeholder else "declared_unverified",
        "blocked_reasons": blocked_reasons,
        "qlib_execution_status": execution_status,
        "qlib_execution_passed": False,
        "manifest": manifest,
        "workflow_config": str(workflow_path),
        "baselines": baselines,
    }
