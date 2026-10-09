from pathlib import Path
import hashlib
import json

from src.config import HASH_ALGORITHM, SCHEMA_FINGERPRINT_FILE

from ..result_fingerprint import ValidationResult



# ============================================================
# Canonicalize Schema
# ============================================================

def canonicalize_schema(
    schema_definition,
) -> str:
    """
    Convert schema definition into a deterministic JSON string.

    Dictionary keys are sorted so that the ordering of keys
    does not affect the generated hash.

    Parameters
    ----------
    schema_definition : Any
        Schema representation.

    Returns
    -------
    str
        Canonical JSON representation of the schema.
    """

    return json.dumps(
        schema_definition,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


# ============================================================
# Save Schema Fingerprint
# ============================================================

def save_schema_fingerprint(
    schema_hash: str,
    schema_name: str,
    fingerprint_file: Path = SCHEMA_FINGERPRINT_FILE,
) -> None:
    """
    Parameters
    ----------
    schema_hash : str
        Calculated schema hash.

    schema_name : str
        Logical identifier for the schema.

    fingerprint_file : Path
        Path to schema fingerprint JSON file.
    """

    fingerprint_file = Path(
        fingerprint_file
    )

    # --------------------------------------------------------
    # Create parent directory if necessary
    # --------------------------------------------------------

    fingerprint_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Load existing fingerprint data
    # --------------------------------------------------------

    fingerprints = load_schema_fingerprint(
        fingerprint_file
    )

    # --------------------------------------------------------
    # Update or create record
    # --------------------------------------------------------

    fingerprints[schema_name] = {
        "schema_name": schema_name,
        "schema_hash": schema_hash,
    }

    # --------------------------------------------------------
    # Write fingerprint JSON
    # --------------------------------------------------------

    with fingerprint_file.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            fingerprints,
            file,
            indent=4,
            ensure_ascii=False,
        )


# ============================================================
# Load Schema Fingerprint
# ============================================================

def load_schema_fingerprint(
    fingerprint_file: Path = SCHEMA_FINGERPRINT_FILE,
) -> dict:
    """
    Parameters
    ----------
    fingerprint_file : Path
        Path to schema fingerprint JSON file.
    """

    fingerprint_file = Path(
        fingerprint_file
    )

    # --------------------------------------------------------
    # File does not exist
    # --------------------------------------------------------

    if not fingerprint_file.exists():
        return {}

    # --------------------------------------------------------
    # Read JSON
    # --------------------------------------------------------

    try:

        with fingerprint_file.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

    except json.JSONDecodeError:

        return {}

    # --------------------------------------------------------
    # Validate JSON structure
    # --------------------------------------------------------

    if not isinstance(data, dict):
        return {}

    return data


# ============================================================
# Calculate Schema Hash
# ============================================================

def calculate_schema_hash(
    schema_definition,
    schema_name: str,
    fingerprint_file: Path = SCHEMA_FINGERPRINT_FILE,
) -> ValidationResult:
    """
    Parameters
    ----------
    schema_definition : Any
        Schema representation.

    schema_name : str
        Logical identifier for the schema.

        Example:
            "users"
            "orders"
            "products"

    fingerprint_file : Path
        Path to schema fingerprint JSON file.
    """

    # ========================================================
    # Canonicalize schema
    # ========================================================

    try:

        canonical_schema = canonicalize_schema(
            schema_definition
        )

    except Exception as error:

        return ValidationResult(
            name="Schema Hash Calculation",
            status="ERROR",
            actual=None,
            expected=None,
            message=f"Unexpected error: {error}",
            details={
                "algorithm": HASH_ALGORITHM,
                "schema_name": schema_name,
            },
        )

    # ========================================================
    # Create hash object
    # ========================================================

    try:

        hash_object = hashlib.new(
            HASH_ALGORITHM
        )

    except Exception as error:

        return ValidationResult(
            name="Schema Hash Calculation",
            status="ERROR",
            actual=None,
            expected=None,
            message=f"Unexpected error: {error}",
            details={
                "algorithm": HASH_ALGORITHM,
                "schema_name": schema_name,
            },
        )

    # ========================================================
    # Generate schema hash
    # ========================================================

    hash_object.update(
        canonical_schema.encode("utf-8")
    )

    actual_hash = hash_object.hexdigest()

    # ========================================================
    # Save fingerprint
    # ========================================================

    save_schema_fingerprint(
        schema_hash=actual_hash,
        schema_name=schema_name,
        fingerprint_file=fingerprint_file,
    )

    # ========================================================
    # Return ValidationResult
    # ========================================================

    return ValidationResult(
        name="Schema Hash Calculation",
        status="PASS",
        actual=actual_hash,
        expected=None,
        message="Schema hash successfully calculated.",
        details={
            "algorithm": HASH_ALGORITHM,
            "schema_name": schema_name,
            "fingerprint_file": str(
                fingerprint_file.resolve()
            ),
            "match": None,
        },
    )


# ============================================================
# Get Stored Schema Hash
# ============================================================

def get_stored_schema_hash(
    schema_name: str,
    fingerprint_file: Path = SCHEMA_FINGERPRINT_FILE,
) -> str | None:
    """
    Parameters
    ----------
    schema_name : str
        Logical identifier for the schema.

    fingerprint_file : Path
        Path to schema fingerprint JSON file.
    """

    fingerprints = load_schema_fingerprint(
        fingerprint_file
    )

    schema_data = fingerprints.get(
        schema_name
    )

    if not isinstance(
        schema_data,
        dict,
    ):
        return None

    return schema_data.get(
        "schema_hash"
    )


# ============================================================
# Validate Schema Hash
# ============================================================

def validate_schema_hash(
    schema_definition,
    schema_name: str,
    expected_hash: str | ValidationResult | None = None,
    fingerprint_file: Path = SCHEMA_FINGERPRINT_FILE,
) -> ValidationResult:
    """
    Parameters
    ----------
    schema_definition : Any
        Current schema representation.

    schema_name : str
        Logical identifier for the schema.

    expected_hash : str | ValidationResult | None
        Expected schema hash.

        Can be provided as:

        1. String hash
        2. ValidationResult returned by
           calculate_schema_hash()
        3. None

        If None, the function will try to load the previous
        hash from the schema fingerprint JSON using
        schema_name.

    fingerprint_file : Path
        Path to schema fingerprint JSON file.
    """

    # --------------------------------------------------------
    # Normalize expected hash
    # --------------------------------------------------------

    if isinstance(
        expected_hash,
        ValidationResult,
    ):
        expected_hash = expected_hash.actual

    # --------------------------------------------------------
    # Get expected hash from JSON if necessary
    # --------------------------------------------------------

    if expected_hash is None:

        expected_hash = get_stored_schema_hash(
            schema_name=schema_name,
            fingerprint_file=fingerprint_file,
        )

    # --------------------------------------------------------
    # Calculate current schema hash
    # --------------------------------------------------------

    try:

        actual_result = calculate_schema_hash(
            schema_definition=schema_definition,
            schema_name=schema_name,
            fingerprint_file=fingerprint_file,
        )

        # ----------------------------------------------------
        # Get actual hash from ValidationResult
        # ----------------------------------------------------

        if isinstance(
            actual_result,
            ValidationResult,
        ):

            actual_hash = actual_result.actual

        else:

            actual_hash = actual_result

    except Exception as error:

        return ValidationResult(
            name="Schema Hash Validation",
            status="ERROR",
            actual=None,
            expected=expected_hash,
            message=f"Unexpected error: {error}",
            details={
                "algorithm": HASH_ALGORITHM,
                "schema_name": schema_name,
            },
        )

    # --------------------------------------------------------
    # Handle calculation error
    # --------------------------------------------------------

    if actual_hash is None:

        return ValidationResult(
            name="Schema Hash Validation",
            status="ERROR",
            actual=None,
            expected=expected_hash,
            message="Schema hash calculation failed.",
            details={
                "algorithm": HASH_ALGORITHM,
                "schema_name": schema_name,
                "fingerprint_file": str(
                    fingerprint_file.resolve()
                ),
            },
        )

    # --------------------------------------------------------
    # New source
    # --------------------------------------------------------

    if expected_hash is None:

        return ValidationResult(
            name="Schema Hash Validation",
            status="NEW_SOURCE",
            actual=actual_hash,
            expected=None,
            message="No previous schema hash was provided.",
            details={
                "algorithm": HASH_ALGORITHM,
                "schema_name": schema_name,
                "fingerprint_file": str(
                    fingerprint_file.resolve()
                ),
                "match": None,
            },
        )

    # --------------------------------------------------------
    # Compare hash
    # --------------------------------------------------------

    is_match = (
        actual_hash == expected_hash
    )

    # --------------------------------------------------------
    # Validation status
    # --------------------------------------------------------

    if is_match:

        status = "PASS"

        message = (
            "Schema hash matches expected hash."
        )

    else:

        status = "CHANGED"

        message = (
            "Schema hash does not match expected hash."
        )

    # --------------------------------------------------------
    # Return validation result
    # --------------------------------------------------------

    return ValidationResult(
        name="Schema Hash Validation",
        status=status,
        actual=actual_hash,
        expected=expected_hash,
        message=message,
        details={
            "algorithm": HASH_ALGORITHM,
            "schema_name": schema_name,
            "fingerprint_file": str(
                fingerprint_file.resolve()
            ),
            "match": is_match,
        },
    )