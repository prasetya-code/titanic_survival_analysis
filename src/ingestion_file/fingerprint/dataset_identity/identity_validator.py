from pathlib import Path
import hashlib
import json

from ..config import HASH_ALGORITHM

from ..result_fingerprint import ValidationResult

from ..file_hash.file_validator import get_stored_file_hash
from ..schema_hash.schema_validator import get_stored_schema_hash


# ============================================================
# Configuration
# ============================================================

# Root dir project menggunakan Current Working Directory (CWD)
PROJECT_ROOT = Path.cwd().parent

# Directory
METADATA_DIR = PROJECT_ROOT / "metadata"

# File (IDENTITY_FINGERPRINT_FILE)
IDENTITY_FINGERPRINT_FILE = (
    METADATA_DIR / "identity_fingerprint.json"
)


# ============================================================
# Canonicalize Identity
# ============================================================

def canonicalize_identity(
    identity_data: dict,
) -> str:
    """
    Convert identity data into a deterministic JSON string.

    Dictionary keys are sorted so that the ordering of keys
    does not affect the generated hash.

    Parameters
    ----------
    identity_data : dict
        Identity components (without the 'identity' hash itself).

    Returns
    -------
    str
        Canonical JSON representation of the identity data.
    """

    return json.dumps(
        identity_data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


# ============================================================
# Build Dataset Identity
# ============================================================

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

        Example:
            "train"
            "test"

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

    # --------------------------------------------------------
    # Identity components (used for hashing)
    #
    # file_path is intentionally NOT part of the hash, because
    # an absolute path differs between machines and would make
    # the identity unstable. file_hash already guarantees the
    # content of the file.
    # --------------------------------------------------------

    identity_data = {
        "dataset_name": dataset_name,
        "source_name": source_name,
        "source_version": source_version,
        "file_name": file_path.name,
        "file_hash": file_hash,
        "schema_hash": schema_hash,
    }

    # --------------------------------------------------------
    # Calculate identity hash
    # --------------------------------------------------------

    hash_object = hashlib.new(
        HASH_ALGORITHM
    )

    hash_object.update(
        canonicalize_identity(
            identity_data
        ).encode("utf-8")
    )

    identity_hash = hash_object.hexdigest()

    # --------------------------------------------------------
    # Return identity (file_path is kept as information only)
    # --------------------------------------------------------

    return {
        **identity_data,
        "file_path": str(
            file_path.resolve()
        ),
        "identity": identity_hash,
    }


# ============================================================
# Save Dataset Identity
# ============================================================

def save_dataset_identity(
    identity: dict,
    dataset_name: str,
    fingerprint_file: Path = IDENTITY_FINGERPRINT_FILE,
) -> None:
    """
    Parameters
    ----------
    identity : dict
        Dataset identity returned by build_dataset_identity().

    dataset_name : str
        Logical identifier for the dataset.

    fingerprint_file : Path
        Path to identity fingerprint JSON file.
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

    fingerprints = load_dataset_identity(
        fingerprint_file
    )

    # --------------------------------------------------------
    # Update or create record
    # --------------------------------------------------------

    fingerprints[dataset_name] = identity

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
# Load Dataset Identity
# ============================================================

def load_dataset_identity(
    fingerprint_file: Path = IDENTITY_FINGERPRINT_FILE,
) -> dict:
    """
    Parameters
    ----------
    fingerprint_file : Path
        Path to identity fingerprint JSON file.
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
# Get Stored Dataset Identity
# ============================================================

def get_stored_dataset_identity(
    dataset_name: str,
    fingerprint_file: Path = IDENTITY_FINGERPRINT_FILE,
) -> dict | None:
    """
    Parameters
    ----------
    dataset_name : str
        Logical identifier for the dataset.

    fingerprint_file : Path
        Path to identity fingerprint JSON file.

    Returns
    -------
    dict | None
        Previously stored identity, or None if not found.
    """

    fingerprints = load_dataset_identity(
        fingerprint_file
    )

    identity_data = fingerprints.get(
        dataset_name
    )

    if not isinstance(
        identity_data,
        dict,
    ):
        return None

    return identity_data


# ============================================================
# Calculate Dataset Identity
# ============================================================

def calculate_dataset_identity(
    dataset_name: str,
    source_name: str,
    source_version: str,
    file_path: Path,
    file_hash: str | None = None,
    schema_hash: str | None = None,
    fingerprint_file: Path = IDENTITY_FINGERPRINT_FILE,
) -> ValidationResult:
    """
    Parameters
    ----------
    dataset_name : str
        Logical identifier for the dataset.

    source_name : str
        Name of the source system.

    source_version : str
        Version of the source.

    file_path : Path
        Source file path.

    file_hash : str | None
        File hash.

        If None, the hash stored by file_validator
        (using dataset_name) will be used.

    schema_hash : str | None
        Schema hash.

        If None, the hash stored by schema_validator
        (using dataset_name) will be used.

    fingerprint_file : Path
        Path to identity fingerprint JSON file.
    """

    file_path = Path(file_path)

    # ========================================================
    # Resolve file hash and schema hash
    # ========================================================

    if file_hash is None:

        file_hash = get_stored_file_hash(
            file_key=dataset_name,
        )

    if schema_hash is None:

        schema_hash = get_stored_schema_hash(
            schema_name=dataset_name,
        )

    # ========================================================
    # Build identity
    # ========================================================

    try:

        identity = build_dataset_identity(
            dataset_name=dataset_name,
            source_name=source_name,
            source_version=source_version,
            file_path=file_path,
            file_hash=file_hash,
            schema_hash=schema_hash,
        )

    except Exception as error:

        return ValidationResult(
            name="Dataset Identity Calculation",
            status="ERROR",
            actual=None,
            expected=None,
            message=f"Unexpected error: {error}",
            details={
                "algorithm": HASH_ALGORITHM,
                "dataset": dataset_name,
            },
        )

    # ========================================================
    # Save fingerprint
    # ========================================================

    save_dataset_identity(
        identity=identity,
        dataset_name=dataset_name,
        fingerprint_file=fingerprint_file,
    )

    # ========================================================
    # Return ValidationResult
    # ========================================================

    return ValidationResult(
        name="Dataset Identity Calculation",
        status="PASS",
        actual=identity["identity"],
        expected=None,
        message="Dataset identity successfully calculated.",
        details={
            "algorithm": HASH_ALGORITHM,
            "dataset": dataset_name,
            "fingerprint_file": str(
                Path(fingerprint_file).resolve()
            ),
            "identity": identity,
            "match": None,
        },
    )


# ============================================================
# Validate Dataset Identity
# ============================================================

def validate_dataset_identity(
    dataset_name: str,
    source_name: str,
    source_version: str,
    file_path: Path,
    file_hash: str | None = None,
    schema_hash: str | None = None,
    expected_identity: str | dict | ValidationResult | None = None,
    fingerprint_file: Path = IDENTITY_FINGERPRINT_FILE,
) -> ValidationResult:
    """
    Parameters
    ----------
    dataset_name : str
        Logical identifier for the dataset.

    source_name : str
        Name of the source system.

    source_version : str
        Version of the source.

    file_path : Path
        Source file path.

    file_hash : str | None
        File hash. If None, loaded from file fingerprint JSON.

    schema_hash : str | None
        Schema hash. If None, loaded from schema fingerprint JSON.

    expected_identity : str | dict | ValidationResult | None
        Expected identity.

        Can be provided as:

        1. String identity hash
        2. Identity dict returned by build_dataset_identity()
        3. ValidationResult returned by
           calculate_dataset_identity()
        4. None

        If None, the function will try to load the previous
        identity from the identity fingerprint JSON using
        dataset_name.

    fingerprint_file : Path
        Path to identity fingerprint JSON file.
    """

    file_path = Path(file_path)

    # --------------------------------------------------------
    # Load previous identity (for field-level comparison)
    # --------------------------------------------------------

    previous_identity = get_stored_dataset_identity(
        dataset_name=dataset_name,
        fingerprint_file=fingerprint_file,
    )

    # --------------------------------------------------------
    # Normalize expected identity
    # --------------------------------------------------------

    if isinstance(
        expected_identity,
        ValidationResult,
    ):
        expected_identity = expected_identity.actual

    if isinstance(
        expected_identity,
        dict,
    ):
        expected_identity = expected_identity.get(
            "identity"
        )

    # --------------------------------------------------------
    # Get expected identity from JSON if necessary
    # --------------------------------------------------------

    if expected_identity is None and previous_identity:

        expected_identity = previous_identity.get(
            "identity"
        )

    # --------------------------------------------------------
    # Calculate current identity
    # --------------------------------------------------------

    try:

        actual_result = calculate_dataset_identity(
            dataset_name=dataset_name,
            source_name=source_name,
            source_version=source_version,
            file_path=file_path,
            file_hash=file_hash,
            schema_hash=schema_hash,
            fingerprint_file=fingerprint_file,
        )

        # ----------------------------------------------------
        # Get actual identity from ValidationResult
        # ----------------------------------------------------

        if isinstance(
            actual_result,
            ValidationResult,
        ):

            actual_identity = actual_result.actual

            current_identity = actual_result.details.get(
                "identity"
            )

        else:

            actual_identity = actual_result

            current_identity = None

    except Exception as error:

        return ValidationResult(
            name="Dataset Identity Validation",
            status="ERROR",
            actual=None,
            expected=expected_identity,
            message=f"Unexpected error: {error}",
            details={
                "algorithm": HASH_ALGORITHM,
                "dataset": dataset_name,
            },
        )

    # --------------------------------------------------------
    # Handle calculation error
    # --------------------------------------------------------

    if actual_identity is None:

        return ValidationResult(
            name="Dataset Identity Validation",
            status="ERROR",
            actual=None,
            expected=expected_identity,
            message="Dataset identity calculation failed.",
            details={
                "algorithm": HASH_ALGORITHM,
                "dataset": dataset_name,
                "fingerprint_file": str(
                    Path(fingerprint_file).resolve()
                ),
            },
        )

    # --------------------------------------------------------
    # New source
    # --------------------------------------------------------

    if expected_identity is None:

        return ValidationResult(
            name="Dataset Identity Validation",
            status="NEW_SOURCE",
            actual=actual_identity,
            expected=None,
            message="No previous dataset identity was provided.",
            details={
                "algorithm": HASH_ALGORITHM,
                "dataset": dataset_name,
                "fingerprint_file": str(
                    Path(fingerprint_file).resolve()
                ),
                "match": None,
            },
        )

    # --------------------------------------------------------
    # Compare identity
    # --------------------------------------------------------

    is_match = (
        actual_identity == expected_identity
    )

    # --------------------------------------------------------
    # Detect changed fields
    # --------------------------------------------------------

    changed_fields = {}

    if (
        not is_match
        and previous_identity
        and current_identity
    ):

        for key in current_identity:

            if key in (
                "identity",
                "file_path",
            ):
                continue

            if (
                current_identity.get(key)
                != previous_identity.get(key)
            ):

                changed_fields[key] = {
                    "previous": previous_identity.get(key),
                    "current": current_identity.get(key),
                }

    # --------------------------------------------------------
    # Validation status
    # --------------------------------------------------------

    if is_match:

        status = "PASS"

        message = (
            "Dataset identity matches expected identity."
        )

    else:

        status = "CHANGED"

        message = (
            "Dataset identity does not match expected identity."
        )

    # --------------------------------------------------------
    # Return validation result
    # --------------------------------------------------------

    return ValidationResult(
        name="Dataset Identity Validation",
        status=status,
        actual=actual_identity,
        expected=expected_identity,
        message=message,
        details={
            "algorithm": HASH_ALGORITHM,
            "dataset": dataset_name,
            "fingerprint_file": str(
                Path(fingerprint_file).resolve()
            ),
            "match": is_match,
            "changed_fields": changed_fields,
        },
    )