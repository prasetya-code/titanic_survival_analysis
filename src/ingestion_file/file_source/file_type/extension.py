from pathlib import Path

from ..result_source import ValidationResult


SUPPORTED_EXTENSIONS = {
    ".csv": "CSV",
    ".tsv": "TSV",
    ".txt": "TXT",
    ".json": "JSON",
    ".jsonl": "JSONL",
    ".xlsx": "Excel",
    ".parquet": "Parquet",
}


def check_extension(path: Path) -> ValidationResult:
    path = Path(path)

    extension = path.suffix.lower()

    supported = extension in SUPPORTED_EXTENSIONS

    format_name = SUPPORTED_EXTENSIONS.get(extension)

    return ValidationResult(
        name = "extension",
        status = "PASS" if supported else "FAIL",
        actual = extension or None,
        expected = list(SUPPORTED_EXTENSIONS.keys()),
        message = (f"Supported file extension: {extension}" if supported else f"Unsupported file extension: {extension or '[none]'}"),
        details = {
            "path": str(path),
            "extension": extension,
            "format": format_name,
            "supported": supported
        }
    )