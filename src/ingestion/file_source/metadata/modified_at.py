from datetime import datetime
from pathlib import Path

from ..result_source import ValidationResult


def get_modified_at(path: Path) -> ValidationResult:
    path = Path(path)

    if not path.exists() and not path.is_symlink():
        return ValidationResult(
            name = "modified_at",
            status = "SKIP",
            actual = None,
            expected = None,
            message = "Path does not exist."
        )

    try:
        timestamp = path.stat().st_mtime
        value = datetime.fromtimestamp(timestamp).isoformat()

        return ValidationResult(
            name = "modified_at",
            status = "INFO",
            actual = value,
            expected = None,
            message = f"Modified at: {value}.",
            details = {
                "timestamp": timestamp,
                "datetime": value
            }
        )

    except OSError as error:
        return ValidationResult(
            name = "modified_at",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"Failed to read modification time: {error}"
        )