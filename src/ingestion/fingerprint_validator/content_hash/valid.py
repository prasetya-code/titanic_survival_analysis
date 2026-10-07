from pathlib import Path
import hashlib

from ..config import HASH_ALGORITHM
from ..result_fingerprint import ValidationResult


def calculate_content_hash(
    file_path: Path
) -> str:

    hash_function = hashlib.new(
        HASH_ALGORITHM
    )

    with file_path.open("rb") as file:

        content = file.read()

    # Normalisasi sederhana
    content = content.replace(
        b"\r\n",
        b"\n"
    )

    content = content.replace(
        b"\r",
        b"\n"
    )

    hash_function.update(content)

    return hash_function.hexdigest()


def validate_content_hash(
    file_path: Path,
    previous_hash: str | None = None,
) -> ValidationResult:

    try:

        current_hash = calculate_content_hash(
            file_path
        )

        if previous_hash is None:

            return ValidationResult(
                name="Content Hash",
                status="NEW_SOURCE",
                actual=current_hash,
                expected=None,
                message="Content hash baru berhasil dibuat",
                details={
                    "algorithm": HASH_ALGORITHM.upper(),
                    "normalized": True,
                },
            )

        if current_hash == previous_hash:

            return ValidationResult(
                name="Content Hash",
                status="UNCHANGED",
                actual=current_hash,
                expected=previous_hash,
                message="Content tidak berubah",
                details={
                    "algorithm": HASH_ALGORITHM.upper(),
                    "normalized": True,
                },
            )

        return ValidationResult(
            name="Content Hash",
            status="CHANGED",
            actual=current_hash,
            expected=previous_hash,
            message="Content berubah",
            details={
                "algorithm": HASH_ALGORITHM.upper(),
                "normalized": True,
            },
        )

    except Exception as e:

        return ValidationResult(
            name="Content Hash",
            status="ERROR",
            message=str(e),
            details={
                "exception": type(e).__name__
            },
        )