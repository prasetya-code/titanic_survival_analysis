import json
import zipfile
from pathlib import Path

from ..result_source import ValidationResult


def check_truncated(path: Path) -> ValidationResult:
    path = Path(path)

    if not path.exists():
        return ValidationResult(
            name = "truncated",
            status = "SKIP",
            actual = None,
            expected = False,
            message = "File does not exist."
        )

    if not path.is_file():
        return ValidationResult(
            name = "truncated",
            status = "SKIP",
            actual = None,
            expected = False,
            message = "Path is not a regular file."
        )

    extension = path.suffix.lower()

    try:
        if extension in {".json"}:
            return _check_json(path)

        if extension == ".xlsx":
            return _check_xlsx(path)

        if extension in {".csv", ".tsv", ".txt", ".jsonl"}:
            return _check_text_file(path)

        if extension == ".parquet":
            return _check_parquet(path)

        return ValidationResult(
            name = "truncated",
            status = "SKIP",
            actual = None,
            expected = False,
            message = f"No truncation checker for {extension}."
        )

    except Exception as error:
        return ValidationResult(
            name = "truncated",
            status = "ERROR",
            actual = None,
            expected = False,
            message = f"Failed to check truncation: {error}",
            details = {
                "extension": extension,
                "error": str(error)
            }
        )


def _check_json(path: Path) -> ValidationResult:
    with path.open("r", encoding = "utf-8-sig") as file:
        json.load(file)

    return ValidationResult(
        name = "truncated",
        status = "PASS",
        actual = False,
        expected = False,
        message = "JSON structure appears complete."
    )


def _check_xlsx(path: Path) -> ValidationResult:
    with zipfile.ZipFile(path, "r") as archive:
        bad_file = archive.testzip()

    if bad_file is not None:
        return ValidationResult(
            name = "truncated",
            status = "FAIL",
            actual = True,
            expected = False,
            message = f"Corrupted ZIP member detected: {bad_file}."
        )

    return ValidationResult(
        name = "truncated",
        status = "PASS",
        actual = False,
        expected = False,
        message = "XLSX archive can be read completely."
    )


def _check_text_file(path: Path) -> ValidationResult:
    with path.open(mode = "r", encoding = "utf-8-sig", errors = "strict") as file:
        for _ in file:
            pass

    return ValidationResult(
        name = "truncated",
        status = "INFO",
        actual = False,
        expected = False,
        message = "Text file can be read to EOF; truncation is not conclusively detectable."
    )


def _check_parquet(path: Path) -> ValidationResult:
    try:
        import pyarrow.parquet as pq

    except ImportError:
        return ValidationResult(
            name = "truncated",
            status = "SKIP",
            actual = None,
            expected = False,
            message = "pyarrow is not installed."
        )

    pq.ParquetFile(path)

    return ValidationResult(
        name = "truncated",
        status = "PASS",
        actual = False,
        expected = False,
        message = "Parquet metadata/footer can be read."
    )