from datetime import datetime
from pathlib import Path

from ..result_source import ValidationResult


def get_created_at(path: Path) -> ValidationResult:
    path = Path(path)

    if not path.exists() and not path.is_symlink():
        return ValidationResult(
            name = "created_at",
            status = "SKIP",
            actual = None,
            expected = None,
            message = "Path does not exist."
        )

    try:
        timestamp = path.stat().st_birthtime
        value = datetime.fromtimestamp(timestamp).isoformat()

        return ValidationResult(
            name = "created_at",
            status = "INFO",
            actual = value,
            expected = None,
            message = f"Created at: {value}.",
            details = {
                "timestamp": timestamp,
                "datetime": value
            }
        )

    except OSError as error:
        return ValidationResult(
            name = "created_at",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"Failed to read creation time: {error}"
        )