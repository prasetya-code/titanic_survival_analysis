import json
import zipfile
from pathlib import Path

from src.ingestion_file import ValidationResult


def check_truncated(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path di filesystem
        if not path.exists():
            # Jika file tidak ada, pengecekan dilewati (SKIP)
            return ValidationResult(
                name = "truncated",
                status = "SKIP",
                actual = None,
                expected = False,
                message = f"Skipped: Path '{path}' does not exist.",
                details = {
                    "path": str(path)
                }
            )

        # Memeriksa apakah path merupakan file biasa (regular file)
        if not path.is_file():
            # Jika path berupa direktori atau objek lain, pengecekan dilewati (SKIP)
            return ValidationResult(
                name = "truncated",
                status = "SKIP",
                actual = None,
                expected = False,
                message = f"Skipped: Path '{path}' is not a regular file.",
                details = {
                    "path": str(path)
                }
            )

        # Mengambil ekstensi file untuk menentukan fungsi pemeriksa yang sesuai
        extension = path.suffix.lower()

        if extension in {".json"}:
            return _check_json(path)

        if extension == ".xlsx":
            return _check_xlsx(path)

        if extension in {".csv", ".tsv", ".txt", ".jsonl"}:
            return _check_text_file(path)

        if extension == ".parquet":
            return _check_parquet(path)

        # Jika jenis ekstensi tidak memiliki metode pengecekan khusus
        return ValidationResult(
            name = "truncated",
            status = "SKIP",
            actual = None,
            expected = False,
            message = f"Skipped: No truncation checker available for extension '{extension}' on '{path}'.",
            details = {
                "path": str(path),
                "extension": extension
            }
        )

    except Exception as error:
        # Menangani exception tak terduga pada fungsi orchestrator utama
        return ValidationResult(
            name = "truncated",
            status = "ERROR",
            actual = None,
            expected = False,
            message = f"Failed to check truncation for '{path}': {error}",
            details = {
                "path": str(path),
                "extension": path.suffix.lower(),
                "error": str(error)
            }
        )


def _check_json(path: Path) -> ValidationResult:
    """Memeriksa kelengkapan struktur JSON."""
    try:
        with path.open("r", encoding = "utf-8-sig") as file:
            json.load(file)

        return ValidationResult(
            name = "truncated",
            status = "PASS",
            actual = False,
            expected = False,
            message = f"JSON structure for '{path}' appears complete.",
            details = {
                "path": str(path),
                "extension": ".json",
                "truncated": False
            }
        )
    except json.JSONDecodeError as error:
        return ValidationResult(
            name = "truncated",
            status = "FAIL",
            actual = True,
            expected = False,
            message = f"JSON file '{path}' is truncated or malformed: {error}",
            details = {
                "path": str(path),
                "extension": ".json",
                "error": str(error),
                "truncated": True
            }
        )


def _check_xlsx(path: Path) -> ValidationResult:
    """Memeriksa integritas arsip ZIP/XLSX."""
    try:
        with zipfile.ZipFile(path, "r") as archive:
            bad_file = archive.testzip()

        if bad_file is not None:
            return ValidationResult(
                name = "truncated",
                status = "FAIL",
                actual = True,
                expected = False,
                message = f"Corrupted ZIP member detected in '{path}': {bad_file}.",
                details = {
                    "path": str(path),
                    "extension": ".xlsx",
                    "bad_file": bad_file,
                    "truncated": True
                }
            )

        return ValidationResult(
            name = "truncated",
            status = "PASS",
            actual = False,
            expected = False,
            message = f"XLSX archive for '{path}' can be read completely.",
            details = {
                "path": str(path),
                "extension": ".xlsx",
                "truncated": False
            }
        )
    except (zipfile.BadZipFile, OSError) as error:
        return ValidationResult(
            name = "truncated",
            status = "FAIL",
            actual = True,
            expected = False,
            message = f"XLSX file '{path}' is truncated or corrupted: {error}",
            details = {
                "path": str(path),
                "extension": ".xlsx",
                "error": str(error),
                "truncated": True
            }
        )


def _check_text_file(path: Path) -> ValidationResult:
    """Membaca file teks hingga EOF untuk memverifikasi keterbacaan."""
    try:
        with path.open(mode = "r", encoding = "utf-8-sig", errors = "strict") as file:
            for _ in file:
                pass

        return ValidationResult(
            name = "truncated",
            status = "INFO",
            actual = False,
            expected = False,
            message = f"Text file '{path}' can be read to EOF; truncation is not conclusively detectable.",
            details = {
                "path": str(path),
                "extension": path.suffix.lower(),
                "truncated": False
            }
        )
    except (UnicodeDecodeError, OSError) as error:
        return ValidationResult(
            name = "truncated",
            status = "FAIL",
            actual = True,
            expected = False,
            message = f"Text file '{path}' cannot be read to EOF (truncated or encoding error): {error}",
            details = {
                "path": str(path),
                "extension": path.suffix.lower(),
                "error": str(error),
                "truncated": True
            }
        )


def _check_parquet(path: Path) -> ValidationResult:
    """Memeriksa keterbacaan metadata/footer file Parquet."""
    try:
        try:
            import pyarrow.parquet as pq
        except ImportError:
            return ValidationResult(
                name = "truncated",
                status = "SKIP",
                actual = None,
                expected = False,
                message = f"Skipped: pyarrow is not installed to check Parquet file '{path}'.",
                details = {
                    "path": str(path),
                    "extension": ".parquet"
                }
            )

        pq.ParquetFile(path)

        return ValidationResult(
            name = "truncated",
            status = "PASS",
            actual = False,
            expected = False,
            message = f"Parquet metadata/footer for '{path}' can be read.",
            details = {
                "path": str(path),
                "extension": ".parquet",
                "truncated": False
            }
        )
    except Exception as error:
        return ValidationResult(
            name = "truncated",
            status = "FAIL",
            actual = True,
            expected = False,
            message = f"Parquet file '{path}' is truncated or corrupted: {error}",
            details = {
                "path": str(path),
                "extension": ".parquet",
                "error": str(error),
                "truncated": True
            }
        )