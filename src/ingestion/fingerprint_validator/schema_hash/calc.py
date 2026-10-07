import hashlib
import json

from ..config import HASH_ALGORITHM
from ..result_fingerprint import ValidationResult


def calculate_schema_hash(
    schema_definition: dict
) -> str:

    normalized_schema = json.dumps(
        schema_definition,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )

    hash_function = hashlib.new(
        HASH_ALGORITHM
    )

    hash_function.update(
        normalized_schema.encode("utf-8")
    )

    return hash_function.hexdigest()


def validate_schema_hash(
    schema_definition: dict,
    previous_hash: str | None = None,
) -> ValidationResult:

    try:

        current_hash = calculate_schema_hash(
            schema_definition
        )

        if previous_hash is None:

            return ValidationResult(
                name="Schema Hash",
                status="NEW_SOURCE",
                actual=current_hash,
                expected=None,
                message="Schema hash baru berhasil dibuat",
                details={
                    "algorithm": HASH_ALGORITHM.upper(),
                    "schema": schema_definition,
                },
            )

        if current_hash == previous_hash:

            return ValidationResult(
                name="Schema Hash",
                status="UNCHANGED",
                actual=current_hash,
                expected=previous_hash,
                message="Schema tidak berubah",
                details={
                    "algorithm": HASH_ALGORITHM.upper(),
                },
            )

        return ValidationResult(
            name="Schema Hash",
            status="CHANGED",
            actual=current_hash,
            expected=previous_hash,
            message="Schema berubah",
            details={
                "algorithm": HASH_ALGORITHM.upper(),
            },
        )

    except Exception as e:

        return ValidationResult(
            name="Schema Hash",
            status="ERROR",
            message=str(e),
            details={
                "exception": type(e).__name__
            },
        )