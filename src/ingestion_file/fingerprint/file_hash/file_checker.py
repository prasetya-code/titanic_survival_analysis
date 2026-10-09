from pathlib import Path

from src.config import (
    FINGERPRINT_FILE,
    HASH_ALGORITHM,
    HASH_CHUNK_SIZE,
)
from src.ingestion_file import ValidationResult
from .file_storage import (
    load_file_fingerprint,
    save_file_fingerprint,
)
import hashlib


def calculate_file_hash(
    file_path: Path,
    dataset_name: str | None = None,
) -> ValidationResult:
    """Mengkalkulasi nilai hash aktual dari file fisik."""
    file_path = Path(file_path)

    if dataset_name is None:
        dataset_name = file_path.stem

    try:
        if not file_path.exists():
            return ValidationResult(
                name = "file_hash_calculation",
                status = "SKIP",
                actual = None,
                expected = None,
                message = f"Skipped: Path '{file_path}' does not exist.",
                details = {
                    "file_path": str(file_path),
                    "dataset": dataset_name,
                }
            )

        if not file_path.is_file():
            return ValidationResult(
                name = "file_hash_calculation",
                status = "SKIP",
                actual = None,
                expected = None,
                message = f"Skipped: Path '{file_path}' is not a regular file.",
                details = {
                    "file_path": str(file_path),
                    "dataset": dataset_name,
                }
            )

        hash_object = hashlib.new(HASH_ALGORITHM)

        with file_path.open("rb") as file:
            while chunk := file.read(HASH_CHUNK_SIZE):
                hash_object.update(chunk)

        actual_hash = hash_object.hexdigest()

        return ValidationResult(
            name = "file_hash_calculation",
            status = "PASS",
            actual = actual_hash,
            expected = None,
            message = f"File hash for '{file_path.name}' successfully calculated.",
            details = {
                "algorithm": HASH_ALGORITHM,
                "dataset": dataset_name,
                "file_name": file_path.name,
                "file_path": str(file_path.resolve()),
            }
        )

    except Exception as error:
        return ValidationResult(
            name = "file_hash_calculation",
            status = "FAIL",
            actual = None,
            expected = None,
            message = f"Failed to calculate file hash for '{file_path}': {error}",
            details = {
                "algorithm": HASH_ALGORITHM,
                "file_path": str(file_path),
                "dataset": dataset_name,
                "error": str(error),
            }
        )


def get_or_create_stored_hash(
    file_path: Path,
    actual_hash: str,
    file_key: str,
    fingerprint_file: Path = FINGERPRINT_FILE,
) -> tuple[str | None, int, bool]:
    """
    Mengecek ketersediaan record hash tersimpan.
    - Jika belum ada: buat record v1 baru dan kembalikan (actual_hash, 1, True).
    - Jika sudah ada: kembalikan (stored_hash, current_version, False).
    """
    fingerprints = load_file_fingerprint(fingerprint_file)
    file_data = fingerprints.get(file_key)

    if isinstance(file_data, dict) and "file_hash" in file_data:
        stored_hash = file_data.get("file_hash")
        current_version = file_data.get("version", 1)
        return stored_hash, current_version, False

    # Belum ada record -> buat v1
    save_file_fingerprint(
        file_path = file_path,
        file_hash = actual_hash,
        file_key = file_key,
        fingerprint_file = fingerprint_file,
        version = 1,
    )
    return actual_hash, 1, True