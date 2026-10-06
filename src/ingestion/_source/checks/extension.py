# source_validator/checks/extension.py

from pathlib import Path

from ..config import (
    FORMAT_NAMES,
    VALIDATOR_NAMES,
    SUPPORTED_EXTENSIONS,
)


def check_extension(file_path: Path) -> dict:
    """
    Memvalidasi extension file.
    """

    extension = file_path.suffix.lower()

    format_name = FORMAT_NAMES.get(
        extension,
        "Unknown"
    )

    validator_name = VALIDATOR_NAMES.get(
        extension,
        "Unknown Validator"
    )

    if extension not in SUPPORTED_EXTENSIONS:

        return {
            "status": "FAIL",
            "actual": extension,
            "expected": sorted(
                SUPPORTED_EXTENSIONS
            ),
            "message": (
                f"Format file '{extension or '(none)'}' "
                f"tidak didukung."
            ),
        }

    return {
        "status": "PASS",
        "actual": {
            "extension": extension,
            "format": format_name,
            "validator": validator_name,
        },
        "expected": sorted(
            SUPPORTED_EXTENSIONS
        ),
        "message": "Extension didukung.",
    }