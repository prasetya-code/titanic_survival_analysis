from pathlib import Path
import sys


def _format_size(size_bytes: int) -> str:
    # Helper untuk memformat ukuran byte ke format yang mudah dibaca.
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        
        size_bytes /= 1024.0

    return f"{size_bytes:.2f} TB"


def check_source_file(file_path: Path, dataset_name: str = "dataset") -> dict:
    # Memvalidasi satu file source (keberadaan, tipe, ekstensi CSV, dan ukuran file).
    print("\n" + "=" * 70)
    print(f"[INFO] Memulai Pengecekan Dataset: '{dataset_name}'")
    print(f"[INFO] Target Path: {file_path.resolve()}")
    print("=" * 70)

    # 1. Cek keberadaan file (Exist Check)
    try:
        print("[DEBUG] [1/4] Memeriksa keberadaan path...")
        exists = file_path.exists()

        if not exists:
            print("[FAIL] Tahap 1 Gagal -> Path tidak ditemukan di sistem file.")

            print("  └─ Expected : File harus ada pada path tersebut")
            print(f"  └─ Actual   : Path '{file_path}' tidak ditemukan")

            return {"status": "FAIL", 
                    "actual": f"{file_path} does not exist", 
                    "expected": "file exists", 
                    "message": f"Source file '{dataset_name}' tidak ditemukan: {file_path}" 
                    }
        
        print("[SUCCESS] Tahap 1 Lolos -> File ditemukan. \n")

    except Exception as e:
        print(f"[ERROR] Tahap 1 Exception -> Gagal memeriksa keberadaan file: {str(e)}", file=sys.stderr)

        return {"status": "ERROR", 
                "actual": type(e).__name__, 
                "expected": "successful path existence check", 
                "message": f"Gagal mengecek keberadaan file {file_path}: {str(e)}" 
                }

    # 2. Cek apakah berupa file reguler (File Type Check)
    try:
        print("[DEBUG] [2/4] Memeriksa tipe path (harus berupa file reguler)...")
        is_file = file_path.is_file()

        if not is_file:
            print("[FAIL] Tahap 2 Gagal -> Path ditemukan, tetapi bukan file reguler (misal: Direktori/Symlink).")

            print("  └─ Expected : Regular file")
            print("  └─ Actual   : Non-regular file/Directory")

            return {"status": "FAIL", 
                    "actual": f"{file_path} is not a regular file", 
                    "expected": "regular file", 
                    "message": f"Path '{dataset_name}' bukan file reguler: {file_path}" 
                    }
        
        print("[SUCCESS] Tahap 2 Lolos -> Path dikonfirmasi sebagai file reguler. \n")

    except Exception as e:
        print(f"[ERROR] Tahap 2 Exception -> Gagal memeriksa tipe file: {str(e)}", file=sys.stderr)

        return {"status": "ERROR", 
                "actual": type(e).__name__, 
                "expected": "successful file type check", 
                "message": f"Gagal mengecek tipe file {file_path}: {str(e)}" 
                }

    # 3. Cek ekstensi file (Extension Check)
    try:
        print("[DEBUG] [3/4] Memeriksa ekstensi file...")
        ext = file_path.suffix.lower()

        if ext != ".csv":
            print("[FAIL] Tahap 3 Gagal -> Ekstensi file tidak sesuai standar.")

            print("  └─ Expected : .csv")
            print(f"  └─ Actual   : {ext}")

            return {"status": "FAIL", 
                    "actual": ext, 
                    "expected": ".csv", 
                    "message": f"Source file '{dataset_name}' harus format CSV: {file_path}" 
                    }

        print("[SUCCESS] Tahap 3 Lolos -> Format file sesuai (.csv). \n")

    except Exception as e:
        print(f"[ERROR] Tahap 3 Exception -> Gagal membaca ekstensi file: {str(e)}", file=sys.stderr)

        return {"status": "ERROR", 
                "actual": type(e).__name__, 
                "expected": "successful extension check", 
                "message": f"Gagal membaca ekstensi file {file_path}: {str(e)}" 
                }

    # 4. Cek ukuran file (File Size Check)
    try:
        print("[DEBUG] [4/4] Memeriksa ukuran file (stat().st_size)...")

        size_bytes = file_path.stat().st_size
        readable_size = _format_size(size_bytes)

        if size_bytes <= 0:
            print("[FAIL] Tahap 4 Gagal -> File terdeteksi kosong (0 Bytes).")

            print("  └─ Expected : Size > 0 Bytes")
            print(f"  └─ Actual   : {size_bytes} Bytes")

            return {"status": "FAIL", 
                    "actual": 0, 
                    "expected": "> 0 bytes", 
                    "message": f"Source file '{dataset_name}' kosong: {file_path}" 
                    }

        print(f"[SUCCESS] Tahap 4 Lolos -> Ukuran file: {size_bytes} Bytes ({readable_size}). \n")

    except Exception as e:
        print(f"[ERROR] Tahap 4 Exception -> Gagal membaca atribut ukuran file (Kemungkinan masalah akses/permission): {str(e)}", file=sys.stderr)

        return {"status": "ERROR", 
                "actual": type(e).__name__, 
                "expected": "successful file size check", 
                "message": f"Gagal membaca ukuran file {file_path}: {str(e)}" 
                }

    # Hasil Akhir Jika Lolos Seluruh Pengecekan
    print("-" * 70)
    print(f"[PASS] VALIDASI SUKSES: File '{dataset_name}' memenuhi seluruh kriteria.")
    print(f"[PROVEN] File '{dataset_name}' memenuhi seluruh kriteria.")
    print("-" * 70)


    return {"status": "PASS", 
            "actual": {"path": str(file_path), 
                       "file_name": file_path.name, 
                       "extension": ext, 
                       "size_bytes": size_bytes, 
                       "size_human": readable_size 
                       }, 
            "expected": "existing, non-empty .csv file", 
            "message": f"Source file '{dataset_name}' valid." 
            }



