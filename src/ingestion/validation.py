import json
import pathlib
import trace
import sys
from typing import Callable, Any, Dict, Union, Tuple


# ==========================================
# HELPER/RUNNER DATA QUALITY (DQ)
# ==========================================

def run_rule(rule_id: str, 
             category: str, scope: str, 
    severity: str, 
    is_blocking: bool, 
    check_fn: Callable[[], Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Runner untuk mengeksekusi fungsi validasi kualitas data (Data Quality Rule).
    
    Menangani eksekusi aman dengan try-except serta mengolah output serialisasi JSON.
    """
    print(f"[RUNNER] --------------------------------------------------")
    print(f"[RUNNER] Menjalankan Aturan DQ [{rule_id}] | Severity: {severity} | Blocking: {is_blocking}")
    print(f"[RUNNER] Kategori: {category} | Scope: {scope}")
    print(f"[RUNNER] -------------------------------------------------- \n")

    try:
        # Eksekusi fungsi validasi
        result = check_fn()

    except Exception as e:
        # Menangkap error tak terduga saat fungsi pengecekan berjalan
        print(f"[RUNNER ERROR] Terjadi kegagalan sistem saat menjalankan [{rule_id}]: {str(e)}")
        result = {
            "status": "ERROR",
            "actual": f"Unhandled Exception: {type(e).__name__} - {str(e)}",
            "expected": "Execution without exceptions",
            "message": f"Terjadi kesalahan sistem: {str(e)}"
        }

    # Serialisasi hasil 'actual' ke format JSON String
    actual_value = result.get("actual")
    if isinstance(actual_value, (dict, list)):
        actual_serialized = json.dumps(actual_value)
    else:
        actual_serialized = json.dumps({"detail": str(actual_value)})

    status = result.get("status", "FAIL")
    print(f"[RUNNER RESULT] Status Akhir [{rule_id}]: {status}")
    print(f"[RUNNER RESULT] Pesan: {result.get('message')}\n")

    return {
        "rule_id": rule_id,
        "category": category,
        "scope": scope,
        "severity": severity,
        "is_blocking": is_blocking,
        "status": status,
        "actual": actual_serialized,
        "expected": result.get("expected"),
        "message": result.get("message"),
    }


# ==========================================
# DQ-001 — Source File Validation (Blocking)
# ==========================================

def check_source_files(train_path: Union[str, pathlib.Path], 
                       test_path: Union[str, pathlib.Path]
                       ) -> Dict[str, Any]:
    """
    Memeriksa: 

    1. keberadaan 
    2. tipe
    3. ekstensi 
    4. ukuran file
    """
    # Mengelompokkan target validasi
    targets: Tuple[Tuple[str, Union[str, pathlib.Path]], ...] = (
        ("train", train_path), 
        ("test", test_path)
    )
    info = {}

    for name, raw_path in targets:
        print(f"[DQ-001 TRACE] Memeriksa file '{name}' pada path: {raw_path}")
        
        try:
            path = pathlib.Path(raw_path)

            # 1. Cek keberadaan path (existence)
            if not path.exists():
                print(f"[DQ-001 FAIL] File '{name}' tidak ditemukan di lokasi.")
                return {
                    "status": "FAIL",
                    "actual": f"{path} does not exist",
                    "expected": "file exists",
                    "message": f"Source file [{name}] tidak ditemukan: {path}",
                }

            # 2. Cek apakah path merujuk ke file biasa (bukan direktori/symlink rusak)
            if not path.is_file():
                print(f"[DQ-001 FAIL] Path '{name}' merujuk ke direktori/non-file.")
                return {
                    "status": "FAIL",
                    "actual": f"{path} is not a regular file",
                    "expected": "regular file",
                    "message": f"Path [{name}] bukan berupa file: {path}",
                }

            # 3. Cek ekstensi file (harus .csv)
            ext = path.suffix.lower()
            if ext != ".csv":
                print(f"[DQ-001 FAIL] Ekstensi file '{name}' adalah '{ext}', diharapkan '.csv'.")
                return {
                    "status": "FAIL",
                    "actual": ext,
                    "expected": ".csv",
                    "message": f"Source file [{name}] harus berformat CSV: {path}",
                }

            # 4. Cek ukuran file (stat)
            size_bytes = path.stat().st_size
            if size_bytes <= 0:
                print(f"[DQ-001 FAIL] File '{name}' ditemukan namun berukuran 0 bytes.")
                return {
                    "status": "FAIL",
                    "actual": 0,
                    "expected": "> 0 bytes",
                    "message": f"Source file [{name}] kosong (0 bytes): {path}",
                }

            # Mengumpulkan metadata jika lolos seluruh pengecekan
            resolved_path = str(path.resolve())
            info[name] = {
                "path": resolved_path,
                "file_name": path.name,
                "extension": ext,
                "size_bytes": size_bytes,
            }
            print(f"[DQ-001 OK] File '{name}' valid. Ukuran: {size_bytes} bytes.")

        except PermissionError:
            print(f"[DQ-001 ERROR] Izin akses ditolak untuk path: {raw_path}")
            return {
                "status": "FAIL",
                "actual": "PermissionError",
                "expected": "read access permission",
                "message": f"Tidak memiliki izin akses untuk membaca file [{name}]: {raw_path}",
            }
        except Exception as err:
            print(f"[DQ-001 ERROR] Gagal mengakses stat/metadata pada path: {raw_path}. Error: {err}")
            return {
                "status": "FAIL",
                "actual": f"OS/IO Error: {type(err).__name__}",
                "expected": "accessible file system path",
                "message": f"Gagal membaca status file [{name}]: {str(err)}",
            }

    print("[DQ-001 SUCCESS] Seluruh file sumber valid.")
    return {
        "status": "PASS",
        "actual": info,
        "expected": "existing, non-empty .csv files",
        "message": "Source files exist and are valid CSV files.",
    }