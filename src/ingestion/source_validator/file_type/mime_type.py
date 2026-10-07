import mimetypes
from pathlib import Path

from ..result_source import ValidationResult


def check_mime_type(path: Path) -> ValidationResult:
    path = Path(path)

    mime_type, encoding = mimetypes.guess_type(path.name)

    return ValidationResult(
        name = "mime_type",
        status = "INFO",
        actual = mime_type,
        expected = None,
        message = (f"MIME type detected: {mime_type}" if mime_type else "MIME type could not be detected."),
        details = {
            "path": str(path),
            "mime_type": mime_type,
            "encoding": encoding
        }
    )