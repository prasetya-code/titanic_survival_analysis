from pathlib import Path
import json
import sys


from .config import (
    HASH_ALGORITHM,
    DEFAULT_FINGERPRINT_PATH,
)

from .file_hash import calculate_file_hash

from .dataset_identity import (
    build_dataset_identity,
    validate_dataset_identity,
)


# ================================================================
# STORAGE
# ================================================================

def _load_previous_fingerprint(
    fingerprint_path: Path,
    dataset_name: str
) -> dict | None:
    """
    Membaca fingerprint dataset dari run sebelumnya.
    """

    if not fingerprint_path.exists():
        return None

    with fingerprint_path.open(
        "r",
        encoding="utf-8"
    ) as f:

        fingerprint_data = json.load(f)

    return fingerprint_data.get(dataset_name)


def _save_fingerprint(
    fingerprint_path: Path,
    dataset_name: str,
    fingerprint_data: dict
) -> None:
    """
    Menyimpan fingerprint dataset terbaru.
    """

    fingerprint_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if fingerprint_path.exists():

        with fingerprint_path.open(
            "r",
            encoding="utf-8"
        ) as f:

            all_fingerprint_data = json.load(f)

    else:

        all_fingerprint_data = {}

    all_fingerprint_data[dataset_name] = fingerprint_data

    with fingerprint_path.open(
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            all_fingerprint_data,
            f,
            indent=2
        )


# ================================================================
# MAIN
# ================================================================

def check_source_fingerprint(
    file_path: Path,
    dataset_name: str = "dataset",
    fingerprint_path: Path = DEFAULT_FINGERPRINT_PATH
) -> dict:
    """
    Memvalidasi fingerprint source file.

    Tahapan:

    1. Check source file
    2. Calculate file hash
    3. Load previous fingerprint
    4. Validate dataset identity
    5. Compare file hash

    Status:

    NEW_SOURCE
    UNCHANGED
    CHANGED
    ERROR
    """

    print("\n" + "=" * 70)
    print(
        f"[INFO] SOURCE FINGERPRINT: '{dataset_name}'"
    )
    print("=" * 70)

    print()
    print("[DEBUG] Target:")
    print(
        f"  ├─ Path        : "
        f"{file_path.resolve()}"
    )
    print(
        f"  ├─ File        : "
        f"{file_path.name}"
    )
    print(
        f"  ├─ Dataset     : "
        f"{dataset_name}"
    )
    print(
        f"  ├─ Algorithm   : "
        f"{HASH_ALGORITHM.upper()}"
    )
    print(
        f"  └─ Fingerprint : "
        f"{fingerprint_path.resolve()}"
    )

    try:

        # ========================================================
        # [1/5] SOURCE FILE
        # ========================================================

        print()
        print("[DEBUG] [1/5] Source File")

        if not file_path.exists():

            print("  ├─ Expected  : Existing file")
            print("  ├─ Actual    : File not found")
            print("  └─ Result    : FAIL")

            return {
                "status": "FAIL",
                "actual": None,
                "expected": str(file_path),
                "message": "Source file tidak ditemukan"
            }

        if not file_path.is_file():

            print("  ├─ Expected  : Regular file")
            print("  ├─ Actual    : Path bukan file")
            print("  └─ Result    : FAIL")

            return {
                "status": "FAIL",
                "actual": str(file_path),
                "expected": "file",
                "message": "Path bukan merupakan file"
            }

        print("  ├─ Expected  : Existing regular file")
        print("  ├─ Actual    : File ditemukan")
        print("  └─ Result    : PASS")

        # ========================================================
        # [2/5] FILE HASH
        # ========================================================

        print()
        print("[DEBUG] [2/5] File Hash")

        print(
            f"  ├─ Algorithm : "
            f"{HASH_ALGORITHM.upper()}"
        )

        print(
            f"  ├─ Source    : "
            f"{file_path.name}"
        )

        current_file_hash = calculate_file_hash(
            file_path
        )

        print(
            f"  ├─ Hash      : "
            f"{current_file_hash}"
        )

        print("  └─ Result    : PASS")

        # ========================================================
        # [3/5] PREVIOUS FINGERPRINT
        # ========================================================

        print()
        print("[DEBUG] [3/5] Previous Fingerprint")

        print(
            f"  ├─ Metadata  : "
            f"{fingerprint_path.resolve()}"
        )

        previous_fingerprint = (
            _load_previous_fingerprint(
                fingerprint_path,
                dataset_name
            )
        )

        # --------------------------------------------------------
        # NEW DATASET
        # --------------------------------------------------------

        if previous_fingerprint is None:

            print("  ├─ Previous  : Not found")
            print("  ├─ Status    : NEW_SOURCE")
            print("  └─ Action    : Create fingerprint")

            current_identity = build_dataset_identity(
                dataset_name=dataset_name,
                file_path=file_path,
                file_hash=current_file_hash
            )

            _save_fingerprint(
                fingerprint_path,
                dataset_name,
                current_identity
            )

            print()
            print(
                "[SUCCESS] Fingerprint baru "
                "berhasil disimpan."
            )

            return {
                "status": "NEW_SOURCE",
                "actual": current_identity,
                "expected": None,
                "message": (
                    "Fingerprint source baru "
                    "berhasil dibuat"
                )
            }

        print("  ├─ Previous  : Found")
        print("  └─ Result    : PASS")

        # ========================================================
        # [4/5] DATASET IDENTITY
        # ========================================================

        print()
        print("[DEBUG] [4/5] Dataset Identity")

        current_identity = build_dataset_identity(
            dataset_name=dataset_name,
            file_path=file_path,
            file_hash=current_file_hash
        )

        identity_match = validate_dataset_identity(
            previous=previous_fingerprint,
            current=current_identity
        )

        print(
            "  ├─ Dataset Match : "
            f"{previous_fingerprint.get('dataset_name') == dataset_name}"
        )

        print(
            "  ├─ File Match    : "
            f"{previous_fingerprint.get('file_name') == file_path.name}"
        )

        print(
            "  ├─ Path Match    : "
            f"{previous_fingerprint.get('file_path') == current_identity['file_path']}"
        )

        print(
            f"  ├─ Identity Match: "
            f"{identity_match}"
        )

        if not identity_match:

            print("  └─ Result        : NEW_SOURCE")

            _save_fingerprint(
                fingerprint_path,
                dataset_name,
                current_identity
            )

            return {
                "status": "NEW_SOURCE",
                "actual": current_identity,
                "expected": previous_fingerprint,
                "message": "Source identity berbeda"
            }

        print("  └─ Result        : PASS")

        # ========================================================
        # [5/5] FILE HASH COMPARISON
        # ========================================================

        print()
        print("[DEBUG] [5/5] File Hash Comparison")

        previous_file_hash = (
            previous_fingerprint.get(
                "file_hash"
            )
        )

        file_hash_match = (
            current_file_hash
            == previous_file_hash
        )

        print(
            f"  ├─ Previous : "
            f"{previous_file_hash}"
        )

        print(
            f"  ├─ Current  : "
            f"{current_file_hash}"
        )

        print(
            f"  ├─ Match    : "
            f"{file_hash_match}"
        )

        # --------------------------------------------------------
        # UNCHANGED
        # --------------------------------------------------------

        if file_hash_match:

            print("  └─ Result   : UNCHANGED")

            return {
                "status": "UNCHANGED",
                "actual": current_identity,
                "expected": {
                    "file_hash": previous_file_hash
                },
                "message": "Source file tidak berubah"
            }

        # --------------------------------------------------------
        # CHANGED
        # --------------------------------------------------------

        print("  └─ Result   : CHANGED")

        _save_fingerprint(
            fingerprint_path,
            dataset_name,
            current_identity
        )

        return {
            "status": "CHANGED",
            "actual": current_identity,
            "expected": {
                "file_hash": previous_file_hash
            },
            "message": "Source file berubah"
        }

    except Exception as e:

        print(
            "\n[ERROR] Proses fingerprint gagal",
            file=sys.stderr
        )

        print(
            f"  ├─ Type    : {type(e).__name__}",
            file=sys.stderr
        )

        print(
            f"  ├─ Message : {e}",
            file=sys.stderr
        )

        print(
            f"  └─ Dataset : {dataset_name}",
            file=sys.stderr
        )

        return {
            "status": "ERROR",
            "actual": None,
            "expected": None,
            "message": str(e)
        }