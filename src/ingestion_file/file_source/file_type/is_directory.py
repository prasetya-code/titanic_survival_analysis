from pathlib import Path

from ..result_source import ValidationResult


def check_is_directory(path: Path) -> ValidationResult:
    path = Path(path)

    is_directory = path.is_dir()

    return ValidationResult(
        name = "is_directory",
        status = "INFO",
        actual = is_directory,
        expected = False,
        message = ("Path is a directory." if is_directory else "Path is not a directory."),
        details = {
            "path": str(path)
        }
    )