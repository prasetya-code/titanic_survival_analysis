from pathlib import Path
import hashlib
import json

from src.config import HASH_ALGORITHM, CONTENT_FINGERPRINT_FILE

from ..result_fingerprint import ValidationResult


# ============================================================
# Normalize Content
# ============================================================

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


# ============================================================
# Save Content Fingerprint
# ============================================================

def save_content_fingerprint(
    file_path: Path,
    content_hash: str,
    file_key: str,
    normalized: bool,
    fingerprint_file: Path = CONTENT_FINGERPRINT_FILE,
) -> None:
    """
    Parameters
    ----------
    file_path : Path
        Path to source file.

    content_hash : str
        Calculated content hash.

    file_key : str
        Logical identifier for the file.

    normalized : bool
        Whether content was normalized before hashing.

    fingerprint_file : Path
        Path to content fingerprint JSON file.
    """

    file_path = Path(file_path)
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

    fingerprints = load_content_fingerprint(
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
        "content_hash": content_hash,
        "normalized": normalized,
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
# Load Content Fingerprint
# ============================================================

def load_content_fingerprint(
    fingerprint_file: Path = CONTENT_FINGERPRINT_FILE,
) -> dict:
    """
    Parameters
    ----------
    fingerprint_file : Path
        Path to content fingerprint JSON file.
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
# Calculate Content Hash
# ============================================================

def calculate_content_hash(
    file_path: Path,
    dataset_name: str | None = None,
    normalized: bool = True,
    fingerprint_file: Path = CONTENT_FINGERPRINT_FILE,
) -> ValidationResult:
    """
    Parameters
    ----------
    file_path : Path
        Path to text file.

    dataset_name : str | None
        Logical identifier for the dataset.

        Example:
            "train"
            "test"

        If None, the file stem will be used.

    normalized : bool
        Whether content should be normalized before hashing.

    fingerprint_file : Path
        Path to content fingerprint JSON file.
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
    # Read file content
    # ========================================================

    try:

        content = file_path.read_text(
            encoding="utf-8-sig"
        )

    except UnicodeDecodeError as error:

        raise ValueError(
            f"File bukan UTF-8 text: {file_path}"
        ) from error

    # ========================================================
    # Normalize content
    # ========================================================

    if normalized:

        content = normalize_content(
            content
        )

    # ========================================================
    # Create hash object
    # ========================================================

    hash_object = hashlib.new(
        HASH_ALGORITHM
    )

    # ========================================================
    # Generate content hash
    # ========================================================

    hash_object.update(
        content.encode("utf-8")
    )

    actual_hash = hash_object.hexdigest()

    # ========================================================
    # Save fingerprint
    # ========================================================

    save_content_fingerprint(
        file_path=file_path,
        content_hash=actual_hash,
        file_key=dataset_name,
        normalized=normalized,
        fingerprint_file=fingerprint_file,
    )

    # ========================================================
    # Return ValidationResult
    # ========================================================

    return ValidationResult(
        name="Content Hash Calculation",
        status="PASS",
        actual=actual_hash,
        expected=None,
        message="Content hash successfully calculated.",
        details={
            "algorithm": HASH_ALGORITHM,
            "dataset": dataset_name,
            "file_name": file_path.name,
            "file_path": str(
                file_path.resolve()
            ),
            "normalized": normalized,
            "fingerprint_file": str(
                fingerprint_file.resolve()
            ),
            "match": None,
        },
    )


# ============================================================
# Get Stored Content Hash
# ============================================================

def get_stored_content_hash(
    file_key: str,
    fingerprint_file: Path = CONTENT_FINGERPRINT_FILE,
) -> str | None:
    """
    Parameters
    ----------
    file_key : str
        Logical identifier for the file.

    fingerprint_file : Path
        Path to content fingerprint JSON file.
    """

    fingerprints = load_content_fingerprint(
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
        "content_hash"
    )


# ============================================================
# Validate Content Hash
# ============================================================

def validate_content_hash(
    file_path: Path,
    expected_hash: str | ValidationResult | None = None,
    dataset_name: str | None = None,
    normalized: bool = True,
    fingerprint_file: Path = CONTENT_FINGERPRINT_FILE,
) -> ValidationResult:
    """
    Parameters
    ----------
    file_path : Path
        Path to text file.

    expected_hash : str | ValidationResult | None
        Expected content hash.

        Can be provided as:

        1. String hash
        2. ValidationResult returned by
           calculate_content_hash()
        3. None

        If None, the function will try to load the previous
        hash from the content fingerprint JSON using
        dataset_name.

    dataset_name : str | None
        Identifier for the file.

        If None, the file stem will be used.

    normalized : bool
        Whether content should be normalized before hashing.

    fingerprint_file : Path
        Path to content fingerprint JSON file.
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

        expected_hash = get_stored_content_hash(
            file_key=dataset_name,
            fingerprint_file=fingerprint_file,
        )

    # --------------------------------------------------------
    # Calculate current content hash
    # --------------------------------------------------------

    try:

        actual_result = calculate_content_hash(
            file_path=file_path,
            dataset_name=dataset_name,
            normalized=normalized,
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
            name="Content Hash Validation",
            status="ERROR",
            actual=None,
            expected=expected_hash,
            message=str(error),
            details={
                "algorithm": HASH_ALGORITHM,
                "file": str(file_path),
                "file_key": dataset_name,
                "normalized": normalized,
            },
        )

    except ValueError as error:

        return ValidationResult(
            name="Content Hash Validation",
            status="ERROR",
            actual=None,
            expected=expected_hash,
            message=str(error),
            details={
                "algorithm": HASH_ALGORITHM,
                "file": str(file_path),
                "file_key": dataset_name,
                "normalized": normalized,
            },
        )

    except Exception as error:

        return ValidationResult(
            name="Content Hash Validation",
            status="ERROR",
            actual=None,
            expected=expected_hash,
            message=f"Unexpected error: {error}",
            details={
                "algorithm": HASH_ALGORITHM,
                "file": str(file_path),
                "file_key": dataset_name,
                "normalized": normalized,
            },
        )

    # --------------------------------------------------------
    # New source
    # --------------------------------------------------------

    if expected_hash is None:

        return ValidationResult(
            name="Content Hash Validation",
            status="NEW_SOURCE",
            actual=actual_hash,
            expected=None,
            message="No previous content hash was provided.",
            details={
                "algorithm": HASH_ALGORITHM,
                "file": str(
                    file_path.resolve()
                ),
                "file_key": dataset_name,
                "normalized": normalized,
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
    # Validation result
    # --------------------------------------------------------

    if is_match:

        status = "PASS"

        message = (
            "Content hash matches expected hash."
        )

    else:

        status = "CHANGED"

        message = (
            "Content hash does not match expected hash."
        )

    # --------------------------------------------------------
    # Return validation result
    # --------------------------------------------------------

    return ValidationResult(
        name="Content Hash Validation",
        status=status,
        actual=actual_hash,
        expected=expected_hash,
        message=message,
        details={
            "algorithm": HASH_ALGORITHM,
            "file": str(
                file_path.resolve()
            ),
            "file_key": dataset_name,
            "normalized": normalized,
            "fingerprint_file": str(
                fingerprint_file.resolve()
            ),
            "match": is_match,
        },
    )