import json
import zipfile
from pathlib import Path

from src.ingestion_file import ValidationResult


def check_corrupted(path: Path) -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path di filesystem
        if not path.exists():
            # Jika file tidak ada, pengecekan dilewati (SKIP)
            return ValidationResult(
                name = "corrupted",
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
                name = "corrupted",
                status = "SKIP",
                actual = None,
                expected = False,
                message = f"Skipped: Path '{path}' is not a regular file.",
                details = {
                    "path": str(path)
                }
            )

        # Mengambil ekstensi file untuk menentukan fungsi pemeriksa korupsi yang sesuai
        extension = path.suffix.lower()

        if extension == ".json":
            return _check_json(path)

        if extension == ".jsonl":
            return _check_jsonl(path)

        if extension == ".xlsx":
            return _check_xlsx(path)

        if extension == ".parquet":
            return _check_parquet(path)

        if extension in {".csv", ".tsv", ".txt"}:
            return _check_text(path)

        # Jika jenis ekstensi tidak memiliki metode pengecekan korupsi khusus
        return ValidationResult(
            name = "corrupted",
            status = "SKIP",
            actual = None,
            expected = False,
            message = f"Skipped: No corruption checker available for extension '{extension}' on '{path}'.",
            details = {
                "path": str(path),
                "extension": extension
            }
        )

    except Exception as error:
        # Menangani exception tak terduga pada fungsi orchestrator utama
        return ValidationResult(
            name = "corrupted",
            status = "FAIL",
            actual = True,
            expected = False,
            message = f"File '{path}' appears corrupted: {error}",
            details = {
                "path": str(path),
                "extension": path.suffix.lower(),
                "error": str(error)
            }
        )


def _check_json(path: Path) -> ValidationResult:
    """Memeriksa integritas dan sintaksis file JSON."""
    try:
        with path.open("r", encoding = "utf-8-sig") as file:
            json.load(file)

        return ValidationResult(
            name = "corrupted",
            status = "PASS",
            actual = False,
            expected = False,
            message = f"JSON file '{path}' is valid and uncorrupted.",
            details = {
                "path": str(path),
                "extension": ".json",
                "corrupted": False
            }
        )
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as error:
        return ValidationResult(
            name = "corrupted",
            status = "FAIL",
            actual = True,
            expected = False,
            message = f"JSON file '{path}' is corrupted or invalid: {error}",
            details = {
                "path": str(path),
                "extension": ".json",
                "error": str(error),
                "corrupted": True
            }
        )


def _check_jsonl(path: Path) -> ValidationResult:
    """Memeriksa integritas baris demi baris pada file JSONL."""
    try:
        invalid_lines = []

        with path.open("r", encoding = "utf-8-sig") as file:
            for line_number, line in enumerate(file, start = 1):
                line = line.strip()

                if not line:
                    continue

                try:
                    json.loads(line)
                except json.JSONDecodeError:
                    invalid_lines.append(line_number)

        if invalid_lines:
            return ValidationResult(
                name = "corrupted",
                status = "FAIL",
                actual = True,
                expected = False,
                message = f"JSONL file '{path}' contains invalid content at {len(invalid_lines)} line(s).",
                details = {
                    "path": str(path),
                    "extension": ".jsonl",
                    "invalid_lines": invalid_lines,
                    "invalid_count": len(invalid_lines),
                    "corrupted": True
                }
            )

        return ValidationResult(
            name = "corrupted",
            status = "PASS",
            actual = False,
            expected = False,
            message = f"JSONL content in '{path}' is valid.",
            details = {
                "path": str(path),
                "extension": ".jsonl",
                "corrupted": False
            }
        )
    except (UnicodeDecodeError, OSError) as error:
        return ValidationResult(
            name = "corrupted",
            status = "FAIL",
            actual = True,
            expected = False,
            message = f"Failed to read JSONL file '{path}': {error}",
            details = {
                "path": str(path),
                "extension": ".jsonl",
                "error": str(error),
                "corrupted": True
            }
        )


def _check_xlsx(path: Path) -> ValidationResult:
    """Memeriksa integritas fisik arsip XLSX/ZIP."""
    try:
        with zipfile.ZipFile(path, "r") as archive:
            bad_file = archive.testzip()

        if bad_file:
            return ValidationResult(
                name = "corrupted",
                status = "FAIL",
                actual = True,
                expected = False,
                message = f"Corrupted XLSX archive member in '{path}': {bad_file}.",
                details = {
                    "path": str(path),
                    "extension": ".xlsx",
                    "bad_file": bad_file,
                    "corrupted": True
                }
            )

        return ValidationResult(
            name = "corrupted",
            status = "PASS",
            actual = False,
            expected = False,
            message = f"XLSX archive '{path}' is valid and uncorrupted.",
            details = {
                "path": str(path),
                "extension": ".xlsx",
                "corrupted": False
            }
        )
    except (zipfile.BadZipFile, OSError) as error:
        return ValidationResult(
            name = "corrupted",
            status = "FAIL",
            actual = True,
            expected = False,
            message = f"XLSX file '{path}' is corrupted: {error}",
            details = {
                "path": str(path),
                "extension": ".xlsx",
                "error": str(error),
                "corrupted": True
            }
        )


def _check_parquet(path: Path) -> ValidationResult:
    """Memeriksa integritas metadata file Parquet."""
    try:
        try:
            import pyarrow.parquet as pq
        except ImportError:
            return ValidationResult(
                name = "corrupted",
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
            name = "corrupted",
            status = "PASS",
            actual = False,
            expected = False,
            message = f"Parquet metadata in '{path}' is valid.",
            details = {
                "path": str(path),
                "extension": ".parquet",
                "corrupted": False
            }
        )
    except Exception as error:
        return ValidationResult(
            name = "corrupted",
            status = "FAIL",
            actual = True,
            expected = False,
            message = f"Parquet file '{path}' is corrupted: {error}",
            details = {
                "path": str(path),
                "extension": ".parquet",
                "error": str(error),
                "corrupted": True
            }
        )


def _check_text(path: Path) -> ValidationResult:
    """Memeriksa keterbacaan serta keutuhan enkoding file teks."""
    try:
        with path.open(mode = "r", encoding = "utf-8-sig", errors = "strict") as file:
            for _ in file:
                pass

        return ValidationResult(
            name = "corrupted",
            status = "INFO",
            actual = False,
            expected = False,
            message = f"Text file '{path}' decoded successfully without corruption errors.",
            details = {
                "path": str(path),
                "extension": path.suffix.lower(),
                "corrupted": False
            }
        )
    except (UnicodeDecodeError, OSError) as error:
        return ValidationResult(
            name = "corrupted",
            status = "FAIL",
            actual = True,
            expected = False,
            message = f"Text file '{path}' contains decoding/corruption errors: {error}",
            details = {
                "path": str(path),
                "extension": path.suffix.lower(),
                "error": str(error),
                "corrupted": True
            }
        )