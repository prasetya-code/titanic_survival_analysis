import os
from pathlib import Path

from src.ingestion_file import ValidationResult


def check_executable(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path di filesystem
        if not path.exists():
            # Jika file tidak ada, validasi eksekusi dilewati (SKIP)
            return ValidationResult(
                name = "executable",
                status = "SKIP",
                actual = None,
                expected = False,
                message = f"Skipped: Path '{path}' does not exist.",
                details = {
                    "path": str(path)
                },
            )

        # Memeriksa apakah path merupakan file biasa (regular file)
        if not path.is_file():
            # Jika path berupa direktori atau objek lain, validasi dilewati (SKIP)
            return ValidationResult(
                name = "executable",
                status = "SKIP",
                actual = None,
                expected = False,
                message = f"Skipped: Path '{path}' is not a regular file.",
                details = {
                    "path": str(path)
                },
            )

        # Memeriksa apakah file memiliki izin eksekusi menggunakan os.access
        executable = os.access(path, os.X_OK)

        # Menentukan pesan deskriptif berdasarkan status ketereksekusian file
        if executable:
            message = f"File '{path}' is executable."
        else:
            message = f"File '{path}' is not executable."

        # Mengembalikan hasil pemeriksaan ketereksekusian (dengan status INFO sesuai format awal)
        return ValidationResult(
            name = "executable",
            status = "INFO",
            actual = executable,
            expected = False,
            message = message,
            details = {
                "path": str(path)
            },
        )

    except OSError as error:
        # Menangani kesalahan akses atau I/O pada filesystem
        return ValidationResult(
            name = "executable",
            status = "FAIL",
            actual = False,
            expected = False,
            message = f"Failed to check executable status for '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            },
        )
    except Exception as error:
        # Menangani exception tak terduga lainnya
        return ValidationResult(
            name = "executable",
            status = "FAIL",
            actual = False,
            expected = False,
            message = f"An unexpected error occurred while checking '{path}': {error}",
            details = {
                "path": str(path),
                "error": str(error)
            },
        )