from pathlib import Path

from ..result_source import ValidationResult


def get_file_name(path: Path) -> ValidationResult:
    path = Path(path)

    return ValidationResult(
        name = "file_name",
        status = "INFO",
        actual = path.name,
        expected = None,
        message = "File name retrieved.",
        details = {
            "file_name": path.name
        }
    )