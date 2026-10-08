from pathlib import Path

from ..result_source import ValidationResult


def _format_size(size_bytes: int) -> str:
    """Convert bytes to a human-readable file size."""
    units = ["B", "KB", "MB", "GB", "TB"]

    size = float(size_bytes)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size_bytes:.2f} B"


def get_size_bytes(path: Path) -> ValidationResult:
    path = Path(path)

    if not path.exists() and not path.is_symlink():
        return ValidationResult(
            name = "size_bytes",
            status = "SKIP",
            actual = None,
            expected = None,
            message = "Path does not exist."
        )

    try:
        size = path.stat().st_size
        human_size = _format_size(size)

        return ValidationResult(
            name = "size_bytes",
            status = "INFO",
            actual = size,
            expected = None,
            message = f"File size: {human_size} ({size:,} bytes).",
            details = {
                "size_bytes": size,
                "size_human": human_size
            },
        )

    except OSError as error:
        return ValidationResult(
            name = "size_bytes",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"Failed to read file size: {error}"
        )