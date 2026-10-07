from pathlib import Path
import hashlib

from ..config import HASH_ALGORITHM
from ..result_fingerprint import ValidationResult


def normalize_content(
    content: str,
) -> str:
    """
    Normalize text content before hashing.

    Current normalization:
    - CRLF -> LF
    - CR   -> LF
    """

    return (
        content
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )


def calculate_content_hash(
    file_path: Path,
    normalized: bool = True,
) -> str:
    """
    Calculate hash based on file content.

    Parameters
    ----------
    file_path : Path
        Path to text file.

    normalized : bool
        Whether content should be normalized before hashing.

    Returns
    -------
    str
        Hexadecimal content hash.
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

    try:
        content = file_path.read_text(
            encoding="utf-8-sig"
        )

    except UnicodeDecodeError as error:
        raise ValueError(
            f"File bukan UTF-8 text: {file_path}"
        ) from error

    if normalized:
        content = normalize_content(content)

    hash_object = hashlib.new(HASH_ALGORITHM)

    hash_object.update(
        content.encode("utf-8")
    )

    return hash_object.hexdigest()


def validate_content_hash(
    file_path: Path,
    expected_hash: str | None = None,
    normalized: bool = True,
) -> ValidationResult:
    """
    Validate content hash against expected hash.
    """

    try:
        actual_hash = calculate_content_hash(
            file_path=file_path,
            normalized=normalized,
        )

    except Exception as error:
        return ValidationResult(
            name="Content Hash Validation",
            status="ERROR",
            actual=None,
            expected=expected_hash,
            message=str(error),
            details={
                "algorithm": HASH_ALGORITHM,
                "file": str(file_path),
                "normalized": normalized,
            },
        )

    if expected_hash is None:
        return ValidationResult(
            name="Content Hash Validation",
            status="NEW_SOURCE",
            actual=actual_hash,
            expected=None,
            message="No previous content hash was provided.",
            details={
                "algorithm": HASH_ALGORITHM,
                "file": str(file_path),
                "normalized": normalized,
                "match": None,
            },
        )

    is_match = actual_hash == expected_hash

    if is_match:
        status = "PASS"
        message = "Content hash matches expected hash."
    else:
        status = "CHANGED"
        message = "Content hash does not match expected hash."

    return ValidationResult(
        name="Content Hash Validation",
        status=status,
        actual=actual_hash,
        expected=expected_hash,
        message=message,
        details={
            "algorithm": HASH_ALGORITHM,
            "file": str(file_path),
            "normalized": normalized,
            "match": is_match,
        },
    )