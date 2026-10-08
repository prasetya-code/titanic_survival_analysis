from pathlib import Path

from ..result_source import ValidationResult


def check_readable_content(path: Path, encoding: str = "utf-8-sig") -> ValidationResult:
    path = Path(path)

    if not path.exists():
        return ValidationResult(
            name = "readable_content",
            status = "SKIP",
            actual = None,
            expected = True,
            message = "File does not exist."
        )

    if not path.is_file():
        return ValidationResult(
            name = "readable_content",
            status = "SKIP",
            actual = None,
            expected = True,
            message = "Path is not a regular file."
        )

    try:
        with path.open(mode = "r", encoding = encoding, newline = "") as file:
            file.read(4096)

        return ValidationResult(
            name = "readable_content",
            status = "PASS",
            actual = True,
            expected = True,
            message = f"File content is readable using {encoding}.",
            details = {
                "encoding": encoding
            }
        )

    except UnicodeDecodeError as error:
        return ValidationResult(
            name = "readable_content",
            status = "FAIL",
            actual = False,
            expected = True,
            message = (f"File cannot be decoded using {encoding}: {error}"),
            details = {
                "encoding": encoding,
                "error": str(error)
            }
        )

    except (OSError, PermissionError) as error:
        return ValidationResult(
            name = "readable_content",
            status = "FAIL",
            actual = False,
            expected = True,
            message = f"File content cannot be read: {error}",
            details = {
                "encoding": encoding,
                "error": str(error)
            }
        )