from pathlib import Path
import csv
import sys


def check_csv_structure(file_path: Path,
                        dataset_name: str = "dataset",
                        expected_columns: list[str] | None = None
                        ) -> dict:
    # Memvalidasi struktur CSV (readability, header, kolom, dan jumlah field per row).
    print("\n" + "=" * 70)
    print(f"[INFO] Memulai Structural Validation Dataset: '{dataset_name}'")
    print(f"[INFO] Target Path: {file_path.resolve()}")
    print("=" * 70)

    # 1. Cek apakah file CSV dapat dibaca (CSV Readability Check)
    try:
        print("[DEBUG] [1/4] Memeriksa apakah file CSV dapat dibaca...")

        with file_path.open("r", encoding="utf-8-sig", newline="") as f:
            sample = f.read(4096)

        if not sample.strip():
            print("[FAIL] Tahap 1 Gagal -> File CSV kosong atau tidak memiliki isi.")

            print("  └─ Expected : CSV file memiliki isi")
            print("  └─ Actual   : File kosong")

            return {"status": "FAIL",
                    "actual": "empty file",
                    "expected": "non-empty CSV content",
                    "message": f"File CSV '{dataset_name}' kosong: {file_path}"
                    }

        print("[SUCCESS] Tahap 1 Lolos -> File CSV dapat dibaca dan memiliki isi. \n")

    except UnicodeDecodeError as e:
        print(f"[ERROR] Tahap 1 Exception -> Encoding file CSV tidak dapat dibaca sebagai UTF-8: {str(e)}", file=sys.stderr)

        return {"status": "ERROR",
                "actual": type(e).__name__,
                "expected": "UTF-8 compatible CSV file",
                "message": f"Encoding file CSV '{file_path}' tidak kompatibel dengan UTF-8: {str(e)}"
                }

    except Exception as e:
        print(f"[ERROR] Tahap 1 Exception -> Gagal membaca file CSV: {str(e)}", file=sys.stderr)

        return {"status": "ERROR",
                "actual": type(e).__name__,
                "expected": "successful CSV read",
                "message": f"Gagal membaca file CSV {file_path}: {str(e)}"
                }

    # 2. Cek header CSV (Header Check)
    try:
        print("[DEBUG] [2/4] Memeriksa header CSV...")

        with file_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)

            header = next(reader, None)

        if header is None or len(header) == 0:
            print("[FAIL] Tahap 2 Gagal -> Header CSV tidak ditemukan.")

            print("  └─ Expected : CSV memiliki header")
            print("  └─ Actual   : Header tidak ditemukan")

            return {"status": "FAIL",
                    "actual": None,
                    "expected": "CSV header exists",
                    "message": f"Header CSV '{dataset_name}' tidak ditemukan: {file_path}"
                    }

        header = [column.strip() for column in header]

        if any(column == "" for column in header):
            print("[FAIL] Tahap 2 Gagal -> Header CSV memiliki nama kolom kosong.")

            print("  └─ Expected : Semua kolom memiliki nama")
            print(f"  └─ Actual   : {header}")

            return {"status": "FAIL",
                    "actual": header,
                    "expected": "all columns have names",
                    "message": f"Header CSV '{dataset_name}' memiliki nama kolom kosong."
                    }

        print(f"[SUCCESS] Tahap 2 Lolos -> Header ditemukan ({len(header)} kolom). \n")

    except csv.Error as e:
        print(f"[ERROR] Tahap 2 Exception -> Struktur CSV tidak dapat diparse: {str(e)}", file=sys.stderr)

        return {"status": "ERROR",
                "actual": type(e).__name__,
                "expected": "valid CSV header",
                "message": f"Gagal membaca header CSV {file_path}: {str(e)}"
                }

    except Exception as e:
        print(f"[ERROR] Tahap 2 Exception -> Gagal memeriksa header CSV: {str(e)}", file=sys.stderr)

        return {"status": "ERROR",
                "actual": type(e).__name__,
                "expected": "successful CSV header check",
                "message": f"Gagal memeriksa header CSV {file_path}: {str(e)}"
                }

    # 3. Cek kesesuaian kolom dengan expected schema (Column Check)
    try:
        print("[DEBUG] [3/4] Memeriksa kesesuaian kolom CSV...")

        if expected_columns is None:
            print("[INFO] Expected columns tidak diberikan.")
            print("[INFO] Pemeriksaan kolom dilewati.")
            print("[SUCCESS] Tahap 3 Lolos -> Tidak ada expected schema yang harus dibandingkan. \n")

        else:
            expected_columns = [column.strip() for column in expected_columns]

            actual_columns = header

            missing_columns = [
                column
                for column in expected_columns
                if column not in actual_columns
            ]

            unexpected_columns = [
                column
                for column in actual_columns
                if column not in expected_columns
            ]

            duplicate_columns = [
                column
                for column in set(actual_columns)
                if actual_columns.count(column) > 1
            ]

            if (
                missing_columns
                or unexpected_columns
                or duplicate_columns
            ):
                print("[FAIL] Tahap 3 Gagal -> Struktur kolom CSV tidak sesuai expected schema.")

                print(f"  └─ Expected : {expected_columns}")
                print(f"  └─ Actual   : {actual_columns}")

                if missing_columns:
                    print(f"  └─ Missing  : {missing_columns}")

                if unexpected_columns:
                    print(f"  └─ Extra    : {unexpected_columns}")

                if duplicate_columns:
                    print(f"  └─ Duplicate: {duplicate_columns}")

                return {"status": "FAIL",
                        "actual": actual_columns,
                        "expected": expected_columns,
                        "message": f"Kolom CSV '{dataset_name}' tidak sesuai expected schema."
                        }

            print(f"[SUCCESS] Tahap 3 Lolos -> {len(actual_columns)} kolom sesuai expected schema. \n")

    except Exception as e:
        print(f"[ERROR] Tahap 3 Exception -> Gagal memeriksa struktur kolom CSV: {str(e)}", file=sys.stderr)

        return {"status": "ERROR",
                "actual": type(e).__name__,
                "expected": "successful CSV column structure check",
                "message": f"Gagal memeriksa struktur kolom CSV {file_path}: {str(e)}"
                }

    # 4. Cek jumlah field setiap row (Row Structure Check)
    try:
        print("[DEBUG] [4/4] Memeriksa jumlah kolom pada setiap row CSV...")

        expected_column_count = len(header)
        total_rows = 0
        invalid_rows = []

        with file_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)

            # Lewati header
            next(reader, None)

            for row_number, row in enumerate(reader, start=2):
                total_rows += 1

                if len(row) != expected_column_count:
                    invalid_rows.append({
                        "row": row_number,
                        "expected_fields": expected_column_count,
                        "actual_fields": len(row)
                    })

        if invalid_rows:
            print("[FAIL] Tahap 4 Gagal -> Terdapat row dengan jumlah kolom tidak sesuai.")

            print(f"  └─ Expected : {expected_column_count} field per row")
            print(f"  └─ Actual   : {len(invalid_rows)} row bermasalah")

            for invalid_row in invalid_rows[:10]:
                print(
                    f"  └─ Row {invalid_row['row']} : "
                    f"expected={invalid_row['expected_fields']}, "
                    f"actual={invalid_row['actual_fields']}"
                )

            if len(invalid_rows) > 10:
                print(
                    f"  └─ ... dan {len(invalid_rows) - 10} row lainnya"
                )

            return {"status": "FAIL",
                    "actual": {"total_rows": total_rows,
                               "invalid_rows": len(invalid_rows),
                               "invalid_row_details": invalid_rows[:10]
                               },
                    "expected": f"{expected_column_count} fields per row",
                    "message": f"Struktur row CSV '{dataset_name}' tidak konsisten."
                    }

        print(
            f"[SUCCESS] Tahap 4 Lolos -> Seluruh {total_rows} row "
            f"memiliki {expected_column_count} field. \n"
        )

    except csv.Error as e:
        print(f"[ERROR] Tahap 4 Exception -> Struktur CSV tidak dapat diparse: {str(e)}", file=sys.stderr)

        return {"status": "ERROR",
                "actual": type(e).__name__,
                "expected": "valid CSV row structure",
                "message": f"Gagal memeriksa struktur row CSV {file_path}: {str(e)}"
                }

    except Exception as e:
        print(f"[ERROR] Tahap 4 Exception -> Gagal memeriksa struktur row CSV: {str(e)}", file=sys.stderr)

        return {"status": "ERROR",
                "actual": type(e).__name__,
                "expected": "successful CSV row structure check",
                "message": f"Gagal memeriksa struktur row CSV {file_path}: {str(e)}"
                }

    # Hasil Akhir Jika Lolos Seluruh Pengecekan
    print("-" * 70)
    print(f"[PASS] VALIDASI SUKSES: Struktur CSV '{dataset_name}' valid.")
    print(f"[PROVEN] CSV '{dataset_name}' memenuhi seluruh structural criteria.")
    print("-" * 70)

    return {"status": "PASS",
            "actual": {"path": str(file_path),
                       "file_name": file_path.name,
                       "column_count": len(header),
                       "columns": header,
                       "row_count": total_rows
                       },
            "expected": {"format": "CSV",
                         "header": "exists",
                         "columns": expected_columns,
                         "fields_per_row": len(header)
                         },
            "message": f"Struktur CSV '{dataset_name}' valid."
            }