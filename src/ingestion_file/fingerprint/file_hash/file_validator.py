from pathlib import Path
import hashlib
import json

from ..config import (
    HASH_ALGORITHM,
    HASH_CHUNK_SIZE,
)

from ..result_fingerprint import ValidationResult


# ============================================================
# Configuration
# ============================================================

# Root dir project menggunakan Current Working Directory (CWD)
PROJECT_ROOT = Path.cwd().parent

# Directory
METADATA_DIR = PROJECT_ROOT / "metadata"

# File (FINGERPRINT_PATH)
FINGERPRINT_FILE = METADATA_DIR / "file_fingerprint.json"


# ============================================================
# Save File Fingerprint
# ============================================================

def save_file_fingerprint(
    file_path: Path,
    file_hash: str,
    file_key: str,
    fingerprint_file: Path = FINGERPRINT_FILE,
) -> None:
    """
    Parameters
    ----------
    file_path : Path
        Path to source file.

    file_hash : str
        Calculated file hash.

    file_key : str
        Logical identifier for the file.

    fingerprint_file : Path
        Path to fingerprint JSON file.
    """

    file_path = Path(file_path)
    fingerprint_file = Path(fingerprint_file)

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

    fingerprints = load_file_fingerprint(
        fingerprint_file
    )

    # --------------------------------------------------------
    # Update or create record
    # --------------------------------------------------------

    fingerprints[file_key] = {
        "file_name": file_path.name,
        "file_path": str(
            file_path.resolve()
        ),
        "file_hash": file_hash,
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
# Load File Fingerprint
# ============================================================

def load_file_fingerprint(
    fingerprint_file: Path = FINGERPRINT_FILE,
) -> dict:
    """
    Parameters
    ----------
    fingerprint_file : Path
        Path to fingerprint JSON file.
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
# Calculate File Hash
# ============================================================

def calculate_file_hash(
    file_path: Path,
    dataset_name: str | None = None,
    fingerprint_file: Path = FINGERPRINT_FILE,
) -> ValidationResult:
    """
    Parameters
    ----------
    file_path : Path
        Path to source file.

    dataset_name : str | None
        Logical identifier for the dataset.

        Example:
            "train"
            "test"

        If None, the file stem will be used.

    fingerprint_file : Path
        Path to fingerprint JSON file.
    """

    file_path = Path(file_path)

    # ========================================================
    # Determine dataset identifier
    # ========================================================

    # ambil nama file tanpa format
    if dataset_name is None:
        dataset_name = file_path.stem

    # ========================================================
    # Validate file existence
    # ========================================================

    if not file_path.exists():
        raise FileNotFoundError(
            f"File tidak ditemukan: {file_path}"
        )

    # ========================================================
    # Validate file type
    # ========================================================

    if not file_path.is_file():
        raise ValueError(
            f"Path bukan regular file: {file_path}"
        )

    # ========================================================
    # Create hash object
    # ========================================================

    hash_object = hashlib.new(
        HASH_ALGORITHM
    )

    # ========================================================
    # Read file in chunks
    # ========================================================

    with file_path.open("rb") as file:

        while True:

            chunk = file.read(
                HASH_CHUNK_SIZE
            )

            if not chunk:
                break

            hash_object.update(
                chunk
            )

    # ========================================================
    # Generate hexadecimal digest
    # ========================================================

    actual_hash = hash_object.hexdigest()

    # ========================================================
    # Save fingerprint
    # ========================================================

    save_file_fingerprint(
        file_path=file_path,
        file_hash=actual_hash,
        file_key=dataset_name,
        fingerprint_file=fingerprint_file,
    )

    # ========================================================
    # Return ValidationResult
    # ========================================================

    return ValidationResult(
        name="File Hash Calculation",
        status="PASS",
        actual=actual_hash,
        expected=None,
        message="File hash successfully calculated.",
        details={
            "algorithm": HASH_ALGORITHM,
            "dataset": dataset_name,
            "file_name": file_path.name,
            "file_path": str(
                file_path.resolve()
            ),
            "fingerprint_file": str(
                fingerprint_file.resolve()
            ),
            "match": None,
        },
    )


# ============================================================
# Get Stored File Hash
# ============================================================

def get_stored_file_hash(
    file_key: str,
    fingerprint_file: Path = FINGERPRINT_FILE,
) -> str | None:
    """
    Parameters
    ----------
    file_key : str
        Logical identifier for the file.

    fingerprint_file : Path
        Path to fingerprint JSON file.
    """

    fingerprints = load_file_fingerprint(
        fingerprint_file
    )

    file_data = fingerprints.get(
        file_key
    )

    if not isinstance(
        file_data,
        dict,
    ):
        return None

    return file_data.get(
        "file_hash"
    )


# ============================================================
# Validate File Hash
# ============================================================

def validate_file_hash(
    file_path: Path,
    expected_hash: str | ValidationResult | None = None,
    dataset_name: str | None = None,
    fingerprint_file: Path = FINGERPRINT_FILE,
) -> ValidationResult:
    """
    Parameters
    ----------
    file_path : Path
        Path to source file.

    expected_hash : str | ValidationResult | None
        Expected hash value.

        Can be provided as:

        1. String hash
        2. ValidationResult returned by
           calculate_file_hash()
        3. None

        If None, the function will try to load the previous
        hash from the fingerprint JSON using dataset_name.

    dataset_name : str | None
        Identifier for the file.

        If None, the file stem will be used.

    fingerprint_file : Path
        Path to fingerprint JSON file.
    """

    file_path = Path(file_path)

    # --------------------------------------------------------
    # Determine file key
    # --------------------------------------------------------

    if dataset_name is None:
        dataset_name = file_path.stem

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

        expected_hash = get_stored_file_hash(
            file_key=dataset_name,
            fingerprint_file=fingerprint_file,
        )

    # --------------------------------------------------------
    # Calculate current hash
    # --------------------------------------------------------

    try:

        actual_result = calculate_file_hash(
            file_path=file_path,
            dataset_name=dataset_name,
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
                "file_key": dataset_name,
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
                "file_key": dataset_name,
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
                "file_key": dataset_name,
            },
        )

    # --------------------------------------------------------
    # New source
    # --------------------------------------------------------

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
                "file_key": dataset_name,
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
    # Validation result
    # --------------------------------------------------------

    if is_match:

        status = "PASS"

        message = (
            "File hash matches expected hash."
        )

    else:

        status = "CHANGED"

        message = (
            "File hash does not match expected hash."
        )

    # --------------------------------------------------------
    # Return validation result
    # --------------------------------------------------------

    return ValidationResult(
        name="File Hash Validation",
        status=status,
        actual=actual_hash,
        expected=expected_hash,
        message=message,
        details={
            "algorithm": HASH_ALGORITHM,
            "file": str(file_path),
            "file_key": dataset_name,
            "match": is_match,
        },
    )