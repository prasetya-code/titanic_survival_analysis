from pathlib import Path
import hashlib
import json
import sys

# ================================================================
# HELPER
# ================================================================
def _sha256_file(file_path: Path) -> str:
    # Menghitung SHA-256 dari isi file secara byte-by-byte.
    sha256 = hashlib.sha256()

    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def _load_previous_fingerprint(fingerprint_path: Path,
                               dataset_name: str
                               ) -> dict | None:
    # Membaca fingerprint dataset dari run sebelumnya jika tersedia.
    if not fingerprint_path.exists():
        return None

    with fingerprint_path.open("r", encoding="utf-8") as f:
        fingerprint_data = json.load(f)

    return fingerprint_data.get(dataset_name)


def _save_fingerprint(fingerprint_path: Path,
                      dataset_name: str,
                      fingerprint_data: dict
                      ) -> None:
    # Menyimpan fingerprint dataset terbaru.
    fingerprint_path.parent.mkdir(parents=True, exist_ok=True)

    # Membaca metadata yang sudah ada jika tersedia.
    if fingerprint_path.exists():
        with fingerprint_path.open("r", encoding="utf-8") as f:
            all_fingerprint_data = json.load(f)
    else:
        all_fingerprint_data = {}

    # Menyimpan fingerprint berdasarkan nama dataset.
    all_fingerprint_data[dataset_name] = fingerprint_data

    with fingerprint_path.open("w", encoding="utf-8") as f:
        json.dump(all_fingerprint_data, f, indent=2)


# ================================================================
# MAIN
# ================================================================
def check_source_fingerprint(file_path: Path,
                             dataset_name: str = "dataset",
                             fingerprint_path: Path = Path("../metadata/source_fingerprint.json")
                             ) -> dict:
    """
    Memvalidasi fingerprint SHA-256 source file.

    Pengecekan:
    1. Memastikan file dapat dibaca
    2. Menghitung SHA-256
    3. Mengambil fingerprint dataset sebelumnya
    4. Memastikan source yang dibandingkan adalah file yang sama
    5. Membandingkan SHA-256
    6. Menyimpan fingerprint terbaru

    Status:
    - NEW_SOURCE : Belum ada fingerprint sebelumnya
    - UNCHANGED  : Source sama persis
    - CHANGED    : Isi source berubah
    - ERROR      : Terjadi error saat proses
    """

    print("\n" + "=" * 70)
    print(f"SOURCE FINGERPRINT - {dataset_name.upper()}")
    print("=" * 70)

    try:
        # ------------------------------------------------------------
        # [1/5] CHECK SOURCE FILE
        # ------------------------------------------------------------
        print("[DEBUG] [1/5] Memeriksa source file...")

        if not file_path.exists():
            print("[FAIL] Tahap 1 - Source file tidak ditemukan")
            print(f"  └─ Expected : {file_path}")

            return {
                "status": "FAIL",
                "actual": None,
                "expected": str(file_path),
                "message": "Source file tidak ditemukan"
            }

        if not file_path.is_file():
            print("[FAIL] Tahap 1 - Path bukan merupakan file")
            print(f"  └─ Actual   : {file_path}")

            return {
                "status": "FAIL",
                "actual": str(file_path),
                "expected": "file",
                "message": "Path bukan merupakan file"
            }

        print("[SUCCESS] Tahap 1 - Source file ditemukan \n")

        # ------------------------------------------------------------
        # [2/5] CALCULATE SHA-256
        # ------------------------------------------------------------
        print("[DEBUG] [2/5] Menghitung SHA-256...")

        current_sha256 = _sha256_file(file_path)

        print("[SUCCESS] Tahap 2 - SHA-256 berhasil dihitung")
        print(f"  └─ SHA-256 : {current_sha256} \n")

        # ------------------------------------------------------------
        # [3/5] LOAD PREVIOUS FINGERPRINT
        # ------------------------------------------------------------
        print("[DEBUG] [3/5] Memeriksa fingerprint sebelumnya...")

        previous_fingerprint = _load_previous_fingerprint(
            fingerprint_path=fingerprint_path,
            dataset_name=dataset_name
        )

        if previous_fingerprint is None:
            print("[INFO] Belum terdapat fingerprint sebelumnya")
            print("[INFO] Source dianggap sebagai NEW_SOURCE")

            current_fingerprint = {
                "dataset_name": dataset_name,
                "file_name": file_path.name,
                "file_path": str(file_path.resolve()),
                "sha256": current_sha256
            }

            _save_fingerprint(
                fingerprint_path=fingerprint_path,
                dataset_name=dataset_name,
                fingerprint_data=current_fingerprint
            )

            print("[SUCCESS] Fingerprint baru berhasil disimpan, serta pemeriksaan diberhentikan \n")

            print("-" * 70)
            print("[PASS] NEW_SOURCE")
            print("[PROVEN] Source fingerprint berhasil dibuat")
            print(f"{'-' * 70} \n")

            return {
                "status": "NEW_SOURCE",
                "actual": current_fingerprint,
                "expected": None,
                "message": "Fingerprint source baru berhasil dibuat"
            }

        print("[SUCCESS] Tahap 3 - Fingerprint sebelumnya ditemukan \n")

        # ------------------------------------------------------------
        # [4/5] VALIDATE SOURCE IDENTITY
        # ------------------------------------------------------------
        print("[DEBUG] [4/5] Memvalidasi identitas source...")

        current_file_path = str(file_path.resolve())

        previous_dataset_name = previous_fingerprint.get("dataset_name")
        previous_file_name = previous_fingerprint.get("file_name")
        previous_file_path = previous_fingerprint.get("file_path")
        previous_sha256 = previous_fingerprint.get("sha256")

        dataset_match = (
            previous_dataset_name == dataset_name
        )

        file_name_match = (
            previous_file_name == file_path.name
        )

        file_path_match = (
            previous_file_path == current_file_path
        )

        if not dataset_match:
            print("[WARNING] Dataset name berbeda")
            print(f"  └─ Previous : {previous_dataset_name}")
            print(f"  └─ Current  : {dataset_name}")

        if not file_name_match:
            print("[WARNING] File name berbeda")
            print(f"  └─ Previous : {previous_file_name}")
            print(f"  └─ Current  : {file_path.name}")

        if not file_path_match:
            print("[WARNING] File path berbeda")
            print(f"  └─ Previous : {previous_file_path}")
            print(f"  └─ Current  : {current_file_path}")

        if not (
            dataset_match
            and file_name_match
            and file_path_match
        ):
            print("[INFO] Source identity berbeda")
            print("[INFO] Source dianggap sebagai NEW_SOURCE")

            current_fingerprint = {
                "dataset_name": dataset_name,
                "file_name": file_path.name,
                "file_path": current_file_path,
                "sha256": current_sha256
            }

            _save_fingerprint(
                fingerprint_path=fingerprint_path,
                dataset_name=dataset_name,
                fingerprint_data=current_fingerprint
            )

            print("[SUCCESS] Fingerprint source baru berhasil disimpan \n")

            print("-" * 70)
            print("[PASS] NEW_SOURCE")
            print("[PROVEN] Source identity berubah")
            print("-" * 70)

            return {
                "status": "NEW_SOURCE",
                "actual": current_fingerprint,
                "expected": previous_fingerprint,
                "message": "Source identity berbeda"
            }

        print("[SUCCESS] Tahap 4 - Source identity sesuai \n")

        # ------------------------------------------------------------
        # [5/5] COMPARE SHA-256
        # ------------------------------------------------------------
        print("[DEBUG] [5/5] Membandingkan SHA-256...")

        if current_sha256 == previous_sha256:
            print("[SUCCESS] SHA-256 tidak berubah")
            print(f"  └─ Previous : {previous_sha256}")
            print(f"  └─ Current  : {current_sha256} \n")

            print("-" * 70)
            print("[PASS] UNCHANGED")
            print("[PROVEN] Source file tidak berubah")
            print(f"{'-' * 70} \n")


            return {
                "status": "UNCHANGED",
                "actual": {
                    "dataset_name": dataset_name,
                    "file_name": file_path.name,
                    "file_path": current_file_path,
                    "sha256": current_sha256
                },
                "expected": {
                    "sha256": previous_sha256
                },
                "message": "Source file tidak berubah"
            }

        print("[WARNING] SHA-256 berubah")
        print(f"  └─ Previous : {previous_sha256}")
        print(f"  └─ Current  : {current_sha256}")

        current_fingerprint = {
            "dataset_name": dataset_name,
            "file_name": file_path.name,
            "file_path": current_file_path,
            "sha256": current_sha256
        }

        _save_fingerprint(
            fingerprint_path=fingerprint_path,
            dataset_name=dataset_name,
            fingerprint_data=current_fingerprint
        )

        print("[SUCCESS] Fingerprint terbaru berhasil disimpan \n")

        print("-" * 70)
        print("[WARNING] CHANGED")
        print("[PROVEN] Source file berubah")
        print(f"{'-' * 70} \n")


        return {
            "status": "CHANGED",
            "actual": current_fingerprint,
            "expected": {
                "sha256": previous_sha256
            },
            "message": "Source file berubah"
        }

    except Exception as e:
        print("[ERROR] Tahap fingerprint gagal", file=sys.stderr)
        print(f"  └─ {type(e).__name__}: {e}", file=sys.stderr)

        return {
            "status": "ERROR",
            "actual": None,
            "expected": None,
            "message": str(e)
        }