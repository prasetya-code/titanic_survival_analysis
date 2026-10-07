import json
import zipfile
from pathlib import Path

from ..result_source import ValidationResult


def check_corrupted(path: Path) -> ValidationResult:
    path = Path(path)

    if not path.exists():
        return ValidationResult(
            name = "corrupted",
            status = "SKIP",
            actual = None,
            expected = False,
            message = "File does not exist."
        )

    if not path.is_file():
        return ValidationResult(
            name = "corrupted",
            status = "SKIP",
            actual = None,
            expected = False,
            message = "Path is not a regular file."
        )

    extension = path.suffix.lower()

    try:
        if extension == ".json":
            return _check_json(path)

        if extension == ".jsonl":
            return _check_jsonl(path)

        if extension == ".xlsx":
            return _check_xlsx(path)

        if extension == ".parquet":
            return _check_parquet(path)

        if extension in {".csv", ".tsv", ".txt"}:
            return _check_text(path)

        return ValidationResult(
            name = "corrupted",
            status = "SKIP",
            actual = None,
            expected = False,
            message = f"No corruption checker for {extension}."
        )

    except Exception as error:
        return ValidationResult(
            name = "corrupted",
            status = "FAIL",
            actual = True,
            expected = False,
            message = f"File appears corrupted: {error}",
            details = {
                "extension": extension,
                "error": str(error)
            }
        )


def _check_json(path: Path) -> ValidationResult:
    with path.open("r", encoding = "utf-8-sig") as file:
        json.load(file)

    return ValidationResult(
        name = "corrupted",
        status = "PASS",
        actual = False,
        expected = False,
        message = "JSON is valid."
    )


def _check_jsonl(path: Path) -> ValidationResult:
    invalid_lines = []

    with path.open("r", encoding = "utf-8-sig") as file:
        for line_number, line in enumerate(file, start = 1):
            line = line.strip()

            if not line:
                continue

            try:
                json.loads(line)
                
            except json.JSONDecodeError:
                invalid_lines.append(line_number)

    if invalid_lines:
        return ValidationResult(
            name = "corrupted",
            status = "FAIL",
            actual = True,
            expected = False,
            message = (f"Invalid JSONL content at {len(invalid_lines)} line(s)."),
            details = {
                "invalid_lines": invalid_lines
            }
        )

    return ValidationResult(
        name = "corrupted",
        status = "PASS",
        actual = False,
        expected = False,
        message = "JSONL content is valid."
    )


def _check_xlsx(path: Path) -> ValidationResult:
    with zipfile.ZipFile(path, "r") as archive:
        bad_file = archive.testzip()

    if bad_file:
        return ValidationResult(
            name = "corrupted",
            status = "FAIL",
            actual = True,
            expected = False,
            message = f"Corrupted XLSX member: {bad_file}."
        )

    return ValidationResult(
        name = "corrupted",
        status = "PASS",
        actual = False,
        expected = False,
        message = "XLSX archive is valid."
    )


def _check_parquet(path: Path) -> ValidationResult:
    try:
        import pyarrow.parquet as pq
    except ImportError:
        return ValidationResult(
            name = "corrupted",
            status = "SKIP",
            actual = None,
            expected = False,
            message = "pyarrow is not installed."
        )

    pq.ParquetFile(path)

    return ValidationResult(
        name = "corrupted",
        status = "PASS",
        actual = False,
        expected = False,
        message = "Parquet metadata is valid."
    )


def _check_text(path: Path) -> ValidationResult:
    with path.open(mode = "r", encoding = "utf-8-sig", errors = "strict") as file:
        for _ in file:
            pass

    return ValidationResult(
        name = "corrupted",
        status = "INFO",
        actual = False,
        expected = False,
        message = "Text content can be decoded successfully."
    )