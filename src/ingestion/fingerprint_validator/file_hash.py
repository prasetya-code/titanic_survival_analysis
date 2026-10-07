from pathlib import Path
import hashlib

from .config import HASH_ALGORITHM
from .result_fingerprint import ValidationResult


def calculate_file(file_path: Path) -> str:

    hash_function  =  hashlib.new(HASH_ALGORITHM)

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            hash_function.update(chunk)

    return hash_function.hexdigest()


def validate_file(file_path: Path, var_calculate_file: str | None = None
) -> ValidationResult:
    """
    Validasi file hash.

    Jika previous_hash tidak tersedia:
        status = NEW_SOURCE

    Jika hash sama:
        status = UNCHANGED

    Jika hash berbeda:
        status = CHANGED
    """

    try:

        current_hash = calculate_file(
            file_path
        )

        if var_calculate_file is None:

            return ValidationResult(
                name = "File Hash",
                status = "NEW_SOURCE",
                actual = current_hash,
                expected = None,
                message = "File hash baru berhasil dibuat",
                details = {
                    "algorithm": HASH_ALGORITHM.upper(),
                    "file": file_path.name,
                }
            )

        hash_match = (
            current_hash == var_calculate_file
        )

        if hash_match:

            return ValidationResult(
                name = "File Hash",
                status = "UNCHANGED",
                actual = current_hash,
                expected = var_calculate_file,
                message = "File hash tidak berubah",
                details = {
                    "algorithm": HASH_ALGORITHM.upper(),
                    "match": True,
                }
            )

        return ValidationResult(
            name = "File Hash",
            status = "CHANGED",
            actual = current_hash,
            expected = var_calculate_file,
            message = "File hash berubah",
            details = {
                "algorithm": HASH_ALGORITHM.upper(),
                "match": False,
            }
        )

    except Exception as e:

        return ValidationResult(
            name = "File Hash",
            status = "ERROR",
            actual = None,
            expected = var_calculate_file,
            message = str(e),
            details = {
                "exception": type(e).__name__
            }
        )