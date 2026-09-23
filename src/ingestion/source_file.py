from pathlib import Path
import sys
from datetime import datetime


def _format_size(size_bytes: int) -> str:
    """Memformat ukuran bytes menjadi format yang mudah dibaca."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"

        size_bytes /= 1024.0

    return f"{size_bytes:.2f} TB"


def _format_timestamp(timestamp: float) -> str:
    """Memformat timestamp filesystem menjadi tanggal yang mudah dibaca."""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def check_source_file(
    file_path: Path,
    dataset_name: str = "dataset"
) -> dict:
    """
    Memvalidasi source file CSV.

    Validation:
        1. File Existence
        2. File Type
        3. File Extension
        4. File Integrity / Accessibility
    """

    # ================================================================
    # HEADER
    # ================================================================

    print("\n" + "=" * 70)
    print(f"[INFO] Memulai Pengecekan Dataset: '{dataset_name}'")
    print("=" * 70)

    print()
    print("[DEBUG] Target:")
    print(f"  ├─ Path      : {file_path.resolve()}")
    print(f"  ├─ File      : {file_path.name}")
    print(f"  └─ Dataset   : {dataset_name}")

    # ================================================================
    # 1. FILE EXISTENCE
    # ================================================================

    try:
        print()
        print("[DEBUG] [1/4] File Existence")

        exists = file_path.exists()

        if not exists:
            print("  ├─ Expected  : File exists")
            print("  ├─ Actual    : File not found")
            print("  └─ Result    : FAIL")

            print()
            print(
                f"[FAIL] Tahap 1 Gagal -> "
                f"File '{dataset_name}' tidak ditemukan."
            )

            print("-" * 70)

            return {
                "status": "FAIL",
                "actual": f"{file_path} does not exist",
                "expected": "file exists",
                "message": (
                    f"Source file '{dataset_name}' "
                    f"tidak ditemukan: {file_path}"
                )
            }

        print("  ├─ Expected  : File exists")
        print("  └─ Result    : PASS")

    except Exception as e:
        print("  ├─ Expected  : File exists")
        print(f"  ├─ Actual    : {type(e).__name__}")
        print("  └─ Result    : ERROR")

        print(
            f"[ERROR] Tahap 1 Exception -> "
            f"{str(e)}",
            file=sys.stderr
        )

        return {
            "status": "ERROR",
            "actual": type(e).__name__,
            "expected": "successful path existence check",
            "message": (
                f"Gagal mengecek keberadaan file "
                f"{file_path}: {str(e)}"
            )
        }

    # ================================================================
    # 2. FILE TYPE
    # ================================================================

    try:
        print()
        print("[DEBUG] [2/4] File Type")

        is_file = file_path.is_file()

        if not is_file:
            print("  ├─ Expected  : Regular file")
            print("  ├─ Actual    : Not a regular file")
            print("  └─ Result    : FAIL")

            print()
            print(
                f"[FAIL] Tahap 2 Gagal -> "
                f"Path '{dataset_name}' bukan file reguler."
            )

            print("-" * 70)

            return {
                "status": "FAIL",
                "actual": f"{file_path} is not a regular file",
                "expected": "regular file",
                "message": (
                    f"Path '{dataset_name}' "
                    f"bukan file reguler: {file_path}"
                )
            }

        print("  ├─ Expected  : Regular file")
        print("  └─ Result    : PASS")

    except Exception as e:
        print("  ├─ Expected  : Regular file")
        print(f"  ├─ Actual    : {type(e).__name__}")
        print("  └─ Result    : ERROR")

        print(
            f"[ERROR] Tahap 2 Exception -> "
            f"{str(e)}",
            file=sys.stderr
        )

        return {
            "status": "ERROR",
            "actual": type(e).__name__,
            "expected": "successful file type check",
            "message": (
                f"Gagal mengecek tipe file "
                f"{file_path}: {str(e)}"
            )
        }

    # ================================================================
    # 3. FILE EXTENSION
    # ================================================================

    try:
        print()
        print("[DEBUG] [3/4] File Extension")

        ext = file_path.suffix.lower()

        if ext != ".csv":
            print("  ├─ Expected  : .csv")
            print(f"  ├─ Actual    : {ext or '(none)'}")
            print("  └─ Result    : FAIL")

            print()
            print(
                f"[FAIL] Tahap 3 Gagal -> "
                f"File '{dataset_name}' bukan CSV."
            )

            print("-" * 70)

            return {
                "status": "FAIL",
                "actual": ext,
                "expected": ".csv",
                "message": (
                    f"Source file '{dataset_name}' "
                    f"harus format CSV: {file_path}"
                )
            }

        print("  ├─ Expected  : .csv")
        print(f"  ├─ Actual    : {ext}")
        print("  └─ Result    : PASS")

    except Exception as e:
        print("  ├─ Expected  : .csv")
        print(f"  ├─ Actual    : {type(e).__name__}")
        print("  └─ Result    : ERROR")

        print(
            f"[ERROR] Tahap 3 Exception -> "
            f"{str(e)}",
            file=sys.stderr
        )

        return {
            "status": "ERROR",
            "actual": type(e).__name__,
            "expected": "successful extension check",
            "message": (
                f"Gagal membaca ekstensi file "
                f"{file_path}: {str(e)}"
            )
        }

    # ================================================================
    # 4. FILE INTEGRITY
    # ================================================================

    try:
        print()
        print("[DEBUG] [4/4] File Integrity")

        file_stat = file_path.stat()

        size_bytes = file_stat.st_size
        readable_size = _format_size(size_bytes)
        readable = file_path.stat().st_size > 0

        modified = _format_timestamp(file_stat.st_mtime)

        if size_bytes <= 0:
            print(
                f"  ├─ Size      : "
                f"{size_bytes:,} Bytes ({readable_size})"
            )
            print(f"  ├─ Readable  : {readable}")
            print(f"  ├─ Modified  : {modified}")
            print("  └─ Result    : FAIL")

            print()
            print(
                f"[FAIL] Tahap 4 Gagal -> "
                f"File '{dataset_name}' kosong."
            )

            print("-" * 70)

            return {
                "status": "FAIL",
                "actual": size_bytes,
                "expected": "> 0 bytes",
                "message": (
                    f"Source file '{dataset_name}' "
                    f"kosong: {file_path}"
                )
            }

        print(
            f"  ├─ Size      : "
            f"{size_bytes:,} Bytes ({readable_size})"
        )
        print(f"  ├─ Readable  : {readable}")
        print(f"  ├─ Modified  : {modified}")
        print("  └─ Result    : PASS")

    except Exception as e:
        print("  ├─ Expected  : Valid readable file")
        print(f"  ├─ Actual    : {type(e).__name__}")
        print("  └─ Result    : ERROR")

        print(
            f"[ERROR] Tahap 4 Exception -> "
            f"{str(e)}",
            file=sys.stderr
        )

        return {
            "status": "ERROR",
            "actual": type(e).__name__,
            "expected": "successful file integrity check",
            "message": (
                f"Gagal membaca metadata file "
                f"{file_path}: {str(e)}"
            )
        }

    # ================================================================
    # FINAL RESULT
    # ================================================================

    print()
    print("-" * 70)

    print(
        f"[PASS] VALIDASI SUKSES: "
        f"File '{dataset_name}' memenuhi seluruh kriteria."
    )

    print("-" * 70)

    print()
    print("[DEBUG] Validation Summary:")
    print(f"  ├─ Dataset     : {dataset_name}")
    print(f"  ├─ File        : {file_path.name}")
    print(f"  ├─ Type        : CSV / Regular File")
    print(f"  ├─ Size        : {readable_size}")
    print(f"  ├─ Readable    : {readable}")
    print(f"  └─ Result      : 4/4 PASS")

    print("=" * 70)

    # ================================================================
    # RETURN
    # ================================================================

    return {
        "status": "PASS",
        "actual": {
            "path": str(file_path),
            "file_name": file_path.name,
            "extension": ext,
            "size_bytes": size_bytes,
            "size_human": readable_size,
            "readable": readable,
            "modified_at": modified,
        },
        "expected": "existing, readable, non-empty .csv file",
        "message": f"Source file '{dataset_name}' valid.",
    }