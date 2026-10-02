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
    print("=" * 70)

    print("\n[DEBUG] Target:")
    print(f"  ├─ Path      : {file_path.resolve()}")
    print(f"  ├─ File      : {file_path.name}")
    print(f"  └─ Dataset   : {dataset_name}")

    # ==================================================================
    # 1. Cek apakah file CSV dapat dibaca
    # ==================================================================
    try:
        print("\n[DEBUG] [1/4] CSV Readability")

        with file_path.open("r", encoding="utf-8-sig", newline="") as f:
            sample = f.read(4096)

        if not sample.strip():
            print("  ├─ Expected  : CSV memiliki isi")
            print("  ├─ Actual    : File kosong")
            print("  └─ Result    : FAIL")

            return {
                "status": "FAIL",
                "actual": "empty file",
                "expected": "non-empty CSV content",
                "message": f"File CSV '{dataset_name}' kosong: {file_path}"
            }

        print("  ├─ Expected  : File CSV dapat dibaca")
        print("  ├─ Actual    : File memiliki isi")
        print("  └─ Result    : PASS")

    except UnicodeDecodeError as e:
        print("  ├─ Expected  : UTF-8 compatible CSV file")
        print(f"  ├─ Actual    : {type(e).__name__}")
        print("  └─ Result    : ERROR")

        print(
            f"[ERROR] Encoding file CSV '{file_path}' tidak kompatibel "
            f"dengan UTF-8: {str(e)}",
            file=sys.stderr
        )

        return {
            "status": "ERROR",
            "actual": type(e).__name__,
            "expected": "UTF-8 compatible CSV file",
            "message": f"Encoding file CSV '{file_path}' tidak kompatibel dengan UTF-8: {str(e)}"
        }

    except Exception as e:
        print("  ├─ Expected  : Successful CSV read")
        print(f"  ├─ Actual    : {type(e).__name__}")
        print("  └─ Result    : ERROR")

        print(
            f"[ERROR] Gagal membaca file CSV: {str(e)}",
            file=sys.stderr
        )

        return {
            "status": "ERROR",
            "actual": type(e).__name__,
            "expected": "successful CSV read",
            "message": f"Gagal membaca file CSV {file_path}: {str(e)}"
        }

    # ==================================================================
    # 2. Cek header CSV
    # ==================================================================
    try:
        print("\n[DEBUG] [2/4] CSV Header")

        with file_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)

        if header is None or len(header) == 0:
            print("  ├─ Expected  : CSV memiliki header")
            print("  ├─ Actual    : Header tidak ditemukan")
            print("  └─ Result    : FAIL")

            return {
                "status": "FAIL",
                "actual": None,
                "expected": "CSV header exists",
                "message": f"Header CSV '{dataset_name}' tidak ditemukan: {file_path}"
            }

        header = [column.strip() for column in header]

        if any(column == "" for column in header):
            print("  ├─ Expected  : Semua kolom memiliki nama")
            print(f"  ├─ Actual    : {header}")
            print("  └─ Result    : FAIL")

            return {
                "status": "FAIL",
                "actual": header,
                "expected": "all columns have names",
                "message": f"Header CSV '{dataset_name}' memiliki nama kolom kosong."
            }

        print("  ├─ Expected  : Header tersedia dan seluruh kolom memiliki nama")
        print(f"  ├─ Actual    : {len(header)} kolom")
        print("  └─ Result    : PASS")

    except csv.Error as e:
        print("  ├─ Expected  : Valid CSV header")
        print(f"  ├─ Actual    : {type(e).__name__}")
        print("  └─ Result    : ERROR")

        print(
            f"[ERROR] Struktur CSV tidak dapat diparse: {str(e)}",
            file=sys.stderr
        )

        return {
            "status": "ERROR",
            "actual": type(e).__name__,
            "expected": "valid CSV header",
            "message": f"Gagal membaca header CSV {file_path}: {str(e)}"
        }

    except Exception as e:
        print("  ├─ Expected  : Successful CSV header check")
        print(f"  ├─ Actual    : {type(e).__name__}")
        print("  └─ Result    : ERROR")

        print(
            f"[ERROR] Gagal memeriksa header CSV: {str(e)}",
            file=sys.stderr
        )

        return {
            "status": "ERROR",
            "actual": type(e).__name__,
            "expected": "successful CSV header check",
            "message": f"Gagal memeriksa header CSV {file_path}: {str(e)}"
        }

    # ==================================================================
    # 3. Cek kesesuaian kolom dengan expected schema
    # ==================================================================
    try:
        print("\n[DEBUG] [3/4] Column Structure")

        if expected_columns is None:
            print("  ├─ Expected  : Expected schema tersedia")
            print("  ├─ Actual    : Tidak diberikan")
            print("  ├─ Check     : Column schema comparison dilewati")
            print("  └─ Result    : PASS")

        else:
            # Normalisasi expected columns untuk comparison.
            # strip() mengabaikan spasi awal/akhir.
            # lower() membuat comparison tidak case-sensitive.
            expected_columns = [
                column.strip().lower()
                for column in expected_columns
            ]

            # Header asli tetap dipertahankan untuk reporting.
            actual_columns = header

            # Normalisasi actual columns untuk comparison.
            actual_columns_normalized = [
                column.strip().lower()
                for column in actual_columns
            ]

            missing_columns = [
                column
                for column in expected_columns
                if column not in actual_columns_normalized
            ]

            unexpected_columns = [
                column
                for column in actual_columns_normalized
                if column not in expected_columns
            ]

            duplicate_columns = [
                column
                for column in set(actual_columns_normalized)
                if actual_columns_normalized.count(column) > 1
            ]

            # Memeriksa apakah urutan kolom actual sesuai dengan expected.
            order_mismatch = (
                expected_columns != actual_columns_normalized
            )

            if (
                missing_columns
                or unexpected_columns
                or duplicate_columns
                or order_mismatch
            ):
                print("  ├─ Expected  : Struktur kolom sesuai expected schema")
                print(f"  ├─ Expected  : {expected_columns}")
                print(f"  ├─ Actual    : {actual_columns}")

                if missing_columns:
                    print(f"  ├─ Missing   : {missing_columns}")

                if unexpected_columns:
                    print(f"  ├─ Extra     : {unexpected_columns}")

                if duplicate_columns:
                    print(f"  ├─ Duplicate : {duplicate_columns}")

                if order_mismatch:
                    print("  ├─ Order     : Tidak sesuai expected")

                print("  └─ Result    : FAIL")

                return {
                    "status": "FAIL",
                    "actual": actual_columns,
                    "expected": expected_columns,
                    "message": f"Kolom CSV '{dataset_name}' tidak sesuai expected schema."
                }

            print("  ├─ Expected  : Struktur kolom sesuai expected schema")
            print(f"  ├─ Actual    : {len(actual_columns)} kolom")
            print("  ├─ Matching  : Name + order + uniqueness")
            print("  └─ Result    : PASS")

    except Exception as e:
        print("  ├─ Expected  : Successful CSV column structure check")
        print(f"  ├─ Actual    : {type(e).__name__}")
        print("  └─ Result    : ERROR")

        print(
            f"[ERROR] Gagal memeriksa struktur kolom CSV: {str(e)}",
            file=sys.stderr
        )

        return {
            "status": "ERROR",
            "actual": type(e).__name__,
            "expected": "successful CSV column structure check",
            "message": f"Gagal memeriksa struktur kolom CSV {file_path}: {str(e)}"
        }

    # ==================================================================
    # 4. Cek jumlah field setiap row
    # ==================================================================
    try:
        print("\n[DEBUG] [4/4] Row Structure")

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
            print(
                f"  ├─ Expected  : {expected_column_count} field per row"
            )
            print(f"  ├─ Actual    : {len(invalid_rows)} row bermasalah")

            for invalid_row in invalid_rows[:10]:
                print(
                    f"  ├─ Row {invalid_row['row']} : "
                    f"expected={invalid_row['expected_fields']}, "
                    f"actual={invalid_row['actual_fields']}"
                )

            if len(invalid_rows) > 10:
                print(
                    f"  ├─ More      : "
                    f"{len(invalid_rows) - 10} row lainnya"
                )

            print("  └─ Result    : FAIL")

            return {
                "status": "FAIL",
                "actual": {
                    "total_rows": total_rows,
                    "invalid_rows": len(invalid_rows),
                    "invalid_row_details": invalid_rows[:10]
                },
                "expected": f"{expected_column_count} fields per row",
                "message": f"Struktur row CSV '{dataset_name}' tidak konsisten."
            }

        print(
            f"  ├─ Expected  : {expected_column_count} field per row"
        )
        print(f"  ├─ Actual    : {total_rows} row diperiksa")
        print("  ├─ Invalid   : 0 row")
        print("  └─ Result    : PASS")

    except csv.Error as e:
        print("  ├─ Expected  : Valid CSV row structure")
        print(f"  ├─ Actual    : {type(e).__name__}")
        print("  └─ Result    : ERROR")

        print(
            f"[ERROR] Struktur CSV tidak dapat diparse: {str(e)}",
            file=sys.stderr
        )

        return {
            "status": "ERROR",
            "actual": type(e).__name__,
            "expected": "valid CSV row structure",
            "message": f"Gagal memeriksa struktur row CSV {file_path}: {str(e)}"
        }

    except Exception as e:
        print("  ├─ Expected  : Successful CSV row structure check")
        print(f"  ├─ Actual    : {type(e).__name__}")
        print("  └─ Result    : ERROR")

        print(
            f"[ERROR] Gagal memeriksa struktur row CSV: {str(e)}",
            file=sys.stderr
        )

        return {
            "status": "ERROR",
            "actual": type(e).__name__,
            "expected": "successful CSV row structure check",
            "message": f"Gagal memeriksa struktur row CSV {file_path}: {str(e)}"
        }

    # ==================================================================
    # Final Result
    # ==================================================================
    print("\n" + "-" * 70)
    print(
        f"[PASS] VALIDASI SUKSES: "
        f"Struktur CSV '{dataset_name}' valid."
    )
    print("-" * 70)

    print("\n[DEBUG] Validation Summary:")
    print(f"  ├─ Dataset     : {dataset_name}")
    print(f"  ├─ File        : {file_path.name}")
    print(f"  ├─ Format      : CSV")
    print(f"  ├─ Columns     : {len(header)}")
    print(f"  ├─ Rows        : {total_rows}")
    print(f"  ├─ Header      : PASS")
    print(f"  ├─ Column      : PASS")
    print(f"  ├─ Row         : PASS")
    print(f"  └─ Result      : 4/4 PASS")

    print("=" * 70)

    return {
        "status": "PASS",
        "actual": {
            "path": str(file_path),
            "file_name": file_path.name,
            "column_count": len(header),
            "columns": header,
            "row_count": total_rows
        },
        "expected": {
            "format": "CSV",
            "header": "exists",
            "columns": expected_columns,
            "fields_per_row": len(header)
        },
        "message": f"Struktur CSV '{dataset_name}' valid."
    }