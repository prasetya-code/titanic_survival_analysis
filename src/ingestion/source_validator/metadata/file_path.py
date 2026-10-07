from pathlib import Path

from ..result_source import ValidationResult


def get_file_path(path: Path) -> ValidationResult:
    path = Path(path)

    try:
        absolute_path = path.absolute()

        return ValidationResult(
            name = "file_path",
            status = "INFO",
            actual = str(absolute_path),
            expected = None,
            message = "File path retrieved.",
            details = {
                "path": str(path),
                "absolute_path": str(absolute_path)
            }
        )

    except OSError as error:
        return ValidationResult(
            name = "file_path",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"Failed to get file path: {error}"
        )