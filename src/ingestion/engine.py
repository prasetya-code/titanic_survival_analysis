import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Optional

validation_results = []

class IngestionBlockingError(RuntimeError):
    """Dilempar ketika sebuah rule blocking gagal / error."""
    pass


def serialize_value(value: Any) -> Optional[str]:
    if value is None:
        return None

    if isinstance(value, (dict, list, tuple, set)):
        if isinstance(value, set):
            value = sorted(value)
        elif isinstance(value, tuple):
            value = list(value)
        return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)

    return str(value)


def record(
    rule_id: str,
    check: str,
    dataset: str,
    status: str,
    severity: str,
    actual: Any = None,
    expected: Any = None,
    message: str = ""
) -> Dict[str, Any]:
    entry = {
        "rule_id": str(rule_id),
        "check": str(check),
        "dataset": str(dataset),
        "status": str(status),
        "severity": str(severity),
        "actual": serialize_value(actual),
        "expected": serialize_value(expected),
        "message": str(message),
    }

    validation_results.append(entry)

    marker = {"PASS": "✓", "WARNING": "⚠", "FAIL": "✗", "ERROR": "‼"}.get(status, "?")
    print(f"{marker} [{rule_id}] {check} ({dataset}) -> {status}: {message}")

    return entry


def write_partial_report_on_blocking_failure(
    rule_id: str,
    message: str,
    history_dir: Path,
    context: Optional[Dict[str, Any]] = None
) -> None:
    ctx = context or {}
    run_id = ctx.get("RUN_ID", "unknown")
    
    partial = {
        "run_id": run_id,
        "dataset": ctx.get("DATASET_NAME", "unknown"),
        "pipeline_stage": ctx.get("PIPELINE_STAGE", "ingestion"),
        "timestamp_utc": ctx.get("RUN_TIMESTAMP", datetime.now(timezone.utc)).isoformat()
            if hasattr(ctx.get("RUN_TIMESTAMP"), "isoformat")
            else datetime.now(timezone.utc).isoformat(),
        "overall_status": "FAIL",
        "blocking_rule_id": rule_id,
        "blocking_message": message,
        "rules_recorded_before_failure": validation_results,
    }

    history_path = Path(history_dir)
    history_path.mkdir(parents=True, exist_ok=True)
    failure_path = history_path / f"{run_id}_BLOCKING_FAILURE.json"

    try:
        failure_path.write_text(
            json.dumps(partial, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"‼ Partial audit trail written to: {failure_path}")
    except Exception as exc:
        print(f"‼ Gagal menulis partial audit trail: {exc}")


def run_rule(
    rule_id: str,
    check: str,
    dataset: str,
    severity: str,
    blocking: bool,
    func: Callable[..., Dict[str, Any]],
    *args: Any,
    **kwargs: Any
) -> Dict[str, Any]:
    history_dir = kwargs.pop("history_dir", Path("reports/history"))
    context = kwargs.pop("context", None)

    try:
        result = func(*args, **kwargs)
    except Exception as exc:
        result = {
            "status": "ERROR",
            "actual": repr(exc),
            "expected": "successful execution",
            "message": f"Unexpected error while running {check}: {exc}",
        }

    entry = record(
        rule_id=rule_id,
        check=check,
        dataset=dataset,
        status=result["status"],
        severity=severity,
        actual=result.get("actual"),
        expected=result.get("expected"),
        message=result.get("message", ""),
    )

    if blocking and result["status"] in ("FAIL", "ERROR"):
        write_partial_report_on_blocking_failure(
            rule_id, result.get("message", ""), history_dir=history_dir, context=context
        )
        raise IngestionBlockingError(
            f"[{rule_id}] {check}: BLOCKING FAILURE — {result.get('message', '')}"
        )

    return entry


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()