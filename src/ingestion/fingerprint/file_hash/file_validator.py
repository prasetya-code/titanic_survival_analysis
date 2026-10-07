from pathlib import Path
import hashlib

from ..config import (
    HASH_ALGORITHM,
    HASH_CHUNK_SIZE,
)

from ..result_fingerprint import ValidationResult


def calculate_file_hash(
    file_path: Path,
) -> str:
    """
    Calculate hash based on the raw bytes of a file.

    Parameters
    ----------
    file_path : Path
        Path to source file.

    Returns
    -------
    str
        Hexadecimal hash digest.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.

    ValueError
        If the path is not a regular file.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File tidak ditemukan: {file_path}"
        )

    if not file_path.is_file():
        raise ValueError(
            f"Path bukan regular file: {file_path}"
        )

    hash_object = hashlib.new(HASH_ALGORITHM)

    with file_path.open("rb") as file:
        while True:
            chunk = file.read(HASH_CHUNK_SIZE)

            if not chunk:
                break

            hash_object.update(chunk)

    return hash_object.hexdigest()


def validate_file_hash(
    file_path: Path,
    expected_hash: str | None = None,
) -> ValidationResult:
    """
    Validate file hash against an expected hash.

    Parameters
    ----------
    file_path : Path
        Path to source file.

    expected_hash : str | None
        Expected hash value.

        If None, the file is considered a new source
        and only the actual hash is calculated.

    Returns
    -------
    ValidationResult
    """

    try:
        actual_hash = calculate_file_hash(file_path)

    except FileNotFoundError as error:
        return ValidationResult(
            name="File Hash Validation",
            status="ERROR",
            actual=None,
            expected=expected_hash,
            message=str(error),
            details={
                "algorithm": HASH_ALGORITHM,
                "file": str(file_path),
            },
        )

    except ValueError as error:
        return ValidationResult(
            name="File Hash Validation",
            status="ERROR",
            actual=None,
            expected=expected_hash,
            message=str(error),
            details={
                "algorithm": HASH_ALGORITHM,
                "file": str(file_path),
            },
        )

    except Exception as error:
        return ValidationResult(
            name="File Hash Validation",
            status="ERROR",
            actual=None,
            expected=expected_hash,
            message=f"Unexpected error: {error}",
            details={
                "algorithm": HASH_ALGORITHM,
                "file": str(file_path),
            },
        )

    if expected_hash is None:
        return ValidationResult(
            name="File Hash Validation",
            status="NEW_SOURCE",
            actual=actual_hash,
            expected=None,
            message="No previous hash was provided.",
            details={
                "algorithm": HASH_ALGORITHM,
                "file": str(file_path),
                "match": None,
            },
        )

    is_match = actual_hash == expected_hash

    if is_match:
        status = "PASS"
        message = "File hash matches expected hash."
    else:
        status = "CHANGED"
        message = "File hash does not match expected hash."

    return ValidationResult(
        name="File Hash Validation",
        status=status,
        actual=actual_hash,
        expected=expected_hash,
        message=message,
        details={
            "algorithm": HASH_ALGORITHM,
            "file": str(file_path),
            "match": is_match,
        },
    )