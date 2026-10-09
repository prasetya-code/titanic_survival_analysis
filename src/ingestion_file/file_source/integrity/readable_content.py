from pathlib import Path

from src.ingestion_file import ValidationResult


def check_readable_content(path: Path, encoding: str = "utf-8-sig") -> ValidationResult:
    # Memastikan input dikonversi menjadi objek Path
    path = Path(path)

    try:
        # Memeriksa keberadaan path di filesystem
        if not path.exists():
            # Jika file tidak ada, pembacaan konten dilewati (SKIP)
            return ValidationResult(
                name = "readable_content",
                status = "SKIP",
                actual = None,
                expected = True,
                message = f"Skipped: Path '{path}' does not exist.",
                details = {
                    "path": str(path),
                    "encoding": encoding
                }
            )

        # Memeriksa apakah path merupakan file biasa (regular file)
        if not path.is_file():
            # Jika path berupa direktori atau objek lain, pembacaan konten dilewati (SKIP)
            return ValidationResult(
                name = "readable_content",
                status = "SKIP",
                actual = None,
                expected = True,
                message = f"Skipped: Path '{path}' is not a regular file.",
                details = {
                    "path": str(path),
                    "encoding": encoding
                }
            )

        # Membuka file dan membaca sampel konten (4KB) untuk memverifikasi dekode encoding
        with path.open(mode = "r", encoding = encoding, newline = "") as file:
            file.read(4096)

        # Mengembalikan hasil jika file berhasil dibaca dan didekode
        return ValidationResult(
            name = "readable_content",
            status = "PASS",
            actual = True,
            expected = True,
            message = f"File content for '{path}' is readable using encoding '{encoding}'.",
            details = {
                "path": str(path),
                "encoding": encoding
            }
        )

    except UnicodeDecodeError as error:
        # Menangani kesalahan dekode karakter/encoding pada isi file
        return ValidationResult(
            name = "readable_content",
            status = "FAIL",
            actual = False,
            expected = True,
            message = f"File '{path}' cannot be decoded using '{encoding}': {error}",
            details = {
                "path": str(path),
                "encoding": encoding,
                "error": str(error)
            }
        )

    except (OSError, PermissionError) as error:
        # Menangani kesalahan akses atau I/O pada filesystem
        return ValidationResult(
            name = "readable_content",
            status = "FAIL",
            actual = False,
            expected = True,
            message = f"File content for '{path}' cannot be read: {error}",
            details = {
                "path": str(path),
                "encoding": encoding,
                "error": str(error)
            }
        )

    except Exception as error:
        # Menangani exception tak terduga lainnya
        return ValidationResult(
            name = "readable_content",
            status = "FAIL",
            actual = False,
            expected = True,
            message = f"An unexpected error occurred while reading content for '{path}': {error}",
            details = {
                "path": str(path),
                "encoding": encoding,
                "error": str(error)
            }
        )