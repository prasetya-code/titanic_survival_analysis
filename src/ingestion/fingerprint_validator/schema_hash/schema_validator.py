import hashlib
import json
from typing import Any

from ..config import HASH_ALGORITHM
from ..result_fingerprint import ValidationResult


def _canonicalize_schema(
    schema_definition: Any,
) -> str:
    """
    Convert schema definition into a deterministic JSON string.

    sort_keys=True ensures dictionary key ordering
    does not affect the hash.
    """

    return json.dumps(
        schema_definition,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def calculate_schema_hash(
    schema_definition: Any,
) -> str:
    """
    Calculate hash from a schema definition.

    Parameters
    ----------
    schema_definition : Any
        Schema representation.

    Returns
    -------
    str
        Hexadecimal schema hash.
    """

    canonical_schema = _canonicalize_schema(
        schema_definition
    )

    hash_object = hashlib.new(HASH_ALGORITHM)

    hash_object.update(
        canonical_schema.encode("utf-8")
    )

    return hash_object.hexdigest()


def validate_schema_hash(
    schema_definition: Any,
    expected_hash: str | None = None,
) -> ValidationResult:
    """
    Validate schema hash against expected hash.
    """

    try:
        actual_hash = calculate_schema_hash(
            schema_definition
        )

    except Exception as error:
        return ValidationResult(
            name="Schema Hash Validation",
            status="ERROR",
            actual=None,
            expected=expected_hash,
            message=str(error),
            details={
                "algorithm": HASH_ALGORITHM,
            },
        )

    if expected_hash is None:
        return ValidationResult(
            name="Schema Hash Validation",
            status="NEW_SOURCE",
            actual=actual_hash,
            expected=None,
            message="No previous schema hash was provided.",
            details={
                "algorithm": HASH_ALGORITHM,
                "match": None,
            },
        )

    is_match = actual_hash == expected_hash

    if is_match:
        status = "PASS"
        message = "Schema hash matches expected hash."
    else:
        status = "CHANGED"
        message = "Schema hash does not match expected hash."

    return ValidationResult(
        name="Schema Hash Validation",
        status=status,
        actual=actual_hash,
        expected=expected_hash,
        message=message,
        details={
            "algorithm": HASH_ALGORITHM,
            "match": is_match,
        },
    )