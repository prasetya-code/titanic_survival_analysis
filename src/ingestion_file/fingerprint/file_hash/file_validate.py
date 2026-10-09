from pathlib import Path

from src.config import (
    FINGERPRINT_FILE,
    HASH_ALGORITHM,
)
from src.ingestion_file import ValidationResult
from .file_checker import (
    calculate_file_hash,
    get_or_create_stored_hash,
)
from .file_storage import save_file_fingerprint


def validate_file_hash(
    file_path: Path,
    dataset_name: str | None = None,
    fingerprint_file: Path = FINGERPRINT_FILE,
    auto_update_version: bool = True,
) -> ValidationResult:
    """Validasi kesesuaian nilai hash file terhadap baseline tersimpan dengan support versioning."""
    file_path = Path(file_path)

    if dataset_name is None:
        dataset_name = file_path.stem

    try:
        # 1. Kalkulasi hash aktual
        actual_result = calculate_file_hash(
            file_path = file_path,
            dataset_name = dataset_name,
        )

        if actual_result.status in {"SKIP", "FAIL"}:
            return ValidationResult(
                name = "file_hash_validation",
                status = actual_result.status,
                actual = None,
                expected = None,
                message = actual_result.message,
                details = {
                    "algorithm": HASH_ALGORITHM,
                    "file_path": str(file_path),
                    "file_key": dataset_name,
                }
            )

        actual_hash = actual_result.actual

        # 2. Cek/buat record hash di storage
        stored_hash, current_version, is_new_record = get_or_create_stored_hash(
            file_path = file_path,
            actual_hash = actual_hash,
            file_key = dataset_name,
            fingerprint_file = fingerprint_file,
        )

        # 3. Record baru (NEW_SOURCE / Version 1)
        if is_new_record:
            return ValidationResult(
                name = "file_hash_validation",
                status = "NEW_SOURCE",
                actual = actual_hash,
                expected = actual_hash,
                message = f"No previous baseline found for '{dataset_name}'. Saved as Version 1.",
                details = {
                    "algorithm": HASH_ALGORITHM,
                    "file_path": str(file_path),
                    "file_key": dataset_name,
                    "version": 1,
                    "match": True,
                }
            )

        # 4. Pencocokan Hash
        is_match = (actual_hash == stored_hash)

        if is_match:
            return ValidationResult(
                name = "file_hash_validation",
                status = "PASS",
                actual = actual_hash,
                expected = stored_hash,
                message = f"File hash for '{file_path.name}' matches stored Version {current_version}.",
                details = {
                    "algorithm": HASH_ALGORITHM,
                    "file_path": str(file_path),
                    "file_key": dataset_name,
                    "version": current_version,
                    "match": True,
                }
            )

        # 5. Jika CHANGED -> naikkan versi jika auto_update_version = True
        new_version = current_version + 1
        if auto_update_version:
            save_file_fingerprint(
                file_path = file_path,
                file_hash = actual_hash,
                file_key = dataset_name,
                fingerprint_file = fingerprint_file,
                version = new_version,
            )

        return ValidationResult(
            name = "file_hash_validation",
            status = "CHANGED",
            actual = actual_hash,
            expected = stored_hash,
            message = f"File hash changed. Updated from Version {current_version} to Version {new_version}.",
            details = {
                "algorithm": HASH_ALGORITHM,
                "file_path": str(file_path),
                "file_key": dataset_name,
                "previous_version": current_version,
                "new_version": new_version,
                "match": False,
            }
        )

    except Exception as error:
        return ValidationResult(
            name = "file_hash_validation",
            status = "ERROR",
            actual = None,
            expected = None,
            message = f"Unexpected error during hash validation for '{file_path}': {error}",
            details = {
                "algorithm": HASH_ALGORITHM,
                "file_path": str(file_path),
                "file_key": dataset_name,
                "error": str(error),
            }
        )