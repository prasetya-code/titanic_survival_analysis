from pathlib import Path

from ..result_fingerprint import ValidationResult


def build_dataset_identity(
    dataset_name: str,
    file_path: Path,
    source_name: str | None = None,
    source_version: str | None = None,
    file_hash: str | None = None,
    schema_hash: str | None = None,
) -> dict:

    return {
        "dataset_name": dataset_name,
        "source_name": source_name,
        "source_version": source_version,
        "file_name": file_path.name,
        "file_path": str(file_path.resolve()),
        "file_hash": file_hash,
        "schema_hash": schema_hash,
    }


def validate_dataset_identity(
    current: dict,
    previous: dict | None,
) -> ValidationResult:

    if previous is None:

        return ValidationResult(
            name="Dataset Identity",
            status="NEW_SOURCE",
            actual=current,
            expected=None,
            message="Dataset identity belum memiliki referensi",
        )

    checks = {
        "dataset_name": (
            previous.get("dataset_name")
            == current.get("dataset_name")
        ),
        "file_name": (
            previous.get("file_name")
            == current.get("file_name")
        ),
        "file_path": (
            previous.get("file_path")
            == current.get("file_path")
        ),
    }

    identity_match = all(
        checks.values()
    )

    if identity_match:

        return ValidationResult(
            name="Dataset Identity",
            status="MATCH",
            actual=current,
            expected=previous,
            message="Dataset identity sama",
            details={
                "checks": checks
            },
        )

    return ValidationResult(
        name="Dataset Identity",
        status="NEW_SOURCE",
        actual=current,
        expected=previous,
        message="Dataset identity berbeda",
        details={
            "checks": checks
        },
    )