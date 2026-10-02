# source_validator/checks/integrity.py

from pathlib import Path

from ..utils import (
    format_size,
    format_timestamp,
)


def _check_readable(file_path: Path) -> bool:
    """
    Test apakah file dapat dibaca.
    """

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8-sig"
        ):
            return True

    except Exception:
        return False


def _check_writable(file_path: Path) -> bool:
    """
    Test apakah file dapat ditulis.

    Catatan:
    mode append dapat menyentuh file metadata.
    """

    try:

        with open(
            file_path,
            "a",
            encoding="utf-8"
        ):
            return True

    except Exception:
        return False


def check_integrity(file_path: Path) -> dict:
    """
    Memvalidasi ukuran, akses, dan timestamp file.
    """

    file_stat = file_path.stat()

    size_bytes = file_stat.st_size

    readable_size = format_size(
        size_bytes
    )

    created = format_timestamp(
        file_stat.st_ctime
    )

    modified = format_timestamp(
        file_stat.st_mtime
    )

    accessed = format_timestamp(
        file_stat.st_atime
    )

    non_empty = size_bytes > 0

    can_read = _check_readable(
        file_path
    )

    can_write = _check_writable(
        file_path
    )

    actual = {
        "size_bytes": size_bytes,
        "size_human": readable_size,
        "non_empty": non_empty,
        "readable": can_read,
        "writable": can_write,
        "created": created,
        "modified": modified,
        "accessed": accessed,
    }

    if not non_empty:

        return {
            "status": "FAIL",
            "actual": actual,
            "expected": "> 0 bytes",
            "message": "File kosong.",
        }

    if not can_read:

        return {
            "status": "FAIL",
            "actual": actual,
            "expected": "readable file",
            "message": "File tidak dapat dibaca.",
        }

    return {
        "status": "PASS",
        "actual": actual,
        "expected": {
            "non_empty": True,
            "readable": True,
        },
        "message": "File valid dan dapat dibaca.",
    }