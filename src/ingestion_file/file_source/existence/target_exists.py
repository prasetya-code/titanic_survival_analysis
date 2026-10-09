from pathlib import Path

from src.ingestion_file import ValidationResult


def check_target_exists(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa apakah path merupakan symbolic link
        if not path.is_symlink():
            # Jika bukan symlink, validasi dilewati (SKIP)
            return ValidationResult(
                name = "target_exists",
                status = "SKIP",
                actual = None,
                expected = True,
                message = f"Skipped: Path '{path}' is not a symbolic link.",
                details = {
                    "path": str(path)
                },
            )

        # Menganalisis target dari symlink (strict=False agar tidak melempar error jika target tidak ada)
        target = path.resolve(strict = False)
        target_exists = target.exists()

        # Menentukan pesan deskriptif berdasarkan status keberadaan target
        if target_exists:
            message = f"Symbolic link '{path}' points to an existing target: '{target}'."
        else:
            message = f"Symbolic link '{path}' points to a non-existent target: '{target}'."

        # Mengembalikan hasil validasi keberadaan target
        return ValidationResult(
            name = "target_exists",
            status = "PASS" if target_exists else "FAIL",
            actual = target_exists,
            expected = True,
            message = message,
            details = {
                "path": str(path), 
                "target": str(target),
                "is_broken_symlink": not target_exists
            },
        )

    except OSError as error:
        # Menangani kesalahan OS atau I/O (misal: permission error atau siklus symlink)
        return ValidationResult(
            name = "target_exists",
            status = "ERROR",
            actual = None,
            expected = True,
            message = f"Failed to resolve symbolic link '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            },
        )
    except Exception as error:
        # Menangani exception tak terduga lainnya
        return ValidationResult(
            name = "target_exists",
            status = "ERROR",
            actual = None,
            expected = True,
            message = f"An unexpected error occurred while checking path '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            },
        )