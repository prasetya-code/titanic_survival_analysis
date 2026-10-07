from pathlib import Path
import hashlib
import json

from ..config import HASH_ALGORITHM
from ..result_fingerprint import ValidationResult


def _calculate_identity_hash(
    identity_data: dict,
) -> str:
    """
    Calculate deterministic identity hash.
    """

    canonical_data = json.dumps(
        identity_data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )

    hash_object = hashlib.new(HASH_ALGORITHM)

    hash_object.update(
        canonical_data.encode("utf-8")
    )

    return hash_object.hexdigest()


def build_dataset_identity(
    dataset_name: str,
    source_name: str,
    source_version: str,
    file_path: Path,
    file_hash: str | None = None,
    schema_hash: str | None = None,
) -> dict:
    """
    Build dataset identity information.

    Parameters
    ----------
    dataset_name : str
        Logical dataset name.

    source_name : str
        Name of the source system.

    source_version : str
        Version of the source.

    file_path : Path
        Source file path.

    file_hash : str | None
        File hash.

    schema_hash : str | None
        Schema hash.

    Returns
    -------
    dict
        Dataset identity definition.
    """

    file_path = Path(file_path)

    identity_data = {
        "dataset_name": dataset_name,
        "source_name": source_name,
        "source_version": source_version,
        "file_name": file_path.name,
        "file_path": str(file_path),
        "file_hash": file_hash,
        "schema_hash": schema_hash,
    }

    identity_hash = _calculate_identity_hash(
        identity_data
    )

    return {
        **identity_data,
        "identity": identity_hash,
    }


def validate_dataset_identity(
    current: dict,
    previous: dict | None = None,
) -> ValidationResult:
    """
    Validate current dataset identity against previous identity.

    Parameters
    ----------
    current : dict
        Current dataset identity.

    previous : dict | None
        Previous dataset identity.

    Returns
    -------
    ValidationResult
    """

    if previous is None:
        return ValidationResult(
            name="Dataset Identity Validation",
            status="NEW_SOURCE",
            actual=current,
            expected=None,
            message="No previous dataset identity was found.",
            details={
                "algorithm": HASH_ALGORITHM,
                "match": None,
            },
        )

    current_identity = current.get("identity")
    previous_identity = previous.get("identity")

    if current_identity is None:
        return ValidationResult(
            name="Dataset Identity Validation",
            status="ERROR",
            actual=current,
            expected=previous,
            message="Current dataset identity does not contain 'identity'.",
            details={
                "algorithm": HASH_ALGORITHM,
            },
        )

    if previous_identity is None:
        return ValidationResult(
            name="Dataset Identity Validation",
            status="ERROR",
            actual=current,
            expected=previous,
            message="Previous dataset identity does not contain 'identity'.",
            details={
                "algorithm": HASH_ALGORITHM,
            },
        )

    is_match = (
        current_identity
        == previous_identity
    )

    if is_match:
        status = "PASS"
        message = "Dataset identity matches previous identity."
    else:
        status = "CHANGED"
        message = "Dataset identity has changed."

    return ValidationResult(
        name="Dataset Identity Validation",
        status=status,
        actual=current_identity,
        expected=previous_identity,
        message=message,
        details={
            "algorithm": HASH_ALGORITHM,
            "match": is_match,
            "current": current,
            "previous": previous,
        },
    )