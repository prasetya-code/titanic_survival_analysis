import polars as pl
import sys


def check_schema(dataframe: pl.DataFrame,
                 dataset_name: str = "dataset",
                 expected_schema: dict | None = None
                 ) -> dict:
    # Memvalidasi schema DataFrame (required columns, column order, data type, dan nullable).
    print("\n" + "=" * 70)
    print(f"[INFO] Memulai Schema Validation Dataset: '{dataset_name}'")
    print("=" * 70)

    # 1. Cek keberadaan expected schema (Schema Contract Check)
    try:
        print("[DEBUG] [1/4] Memeriksa schema contract...")

        if expected_schema is None:
            print("[INFO] Expected schema tidak diberikan.")
            print("[INFO] Pemeriksaan schema dilewati.")
            print("[SUCCESS] Tahap 1 Lolos -> Tidak ada expected schema yang harus dibandingkan. \n")

        else:
            if not isinstance(expected_schema, dict):
                print("[FAIL] Tahap 1 Gagal -> Expected schema harus berupa dictionary.")

                print("  └─ Expected : dict")
                print(f"  └─ Actual   : {type(expected_schema).__name__}")

                return {"status": "FAIL",
                        "actual": type(expected_schema).__name__,
                        "expected": "dict",
                        "message": f"Expected schema '{dataset_name}' harus berupa dictionary."
                        }

            if len(expected_schema) == 0:
                print("[FAIL] Tahap 1 Gagal -> Expected schema kosong.")

                print("  └─ Expected : Schema contract memiliki definisi kolom")
                print("  └─ Actual   : Empty schema")

                return {"status": "FAIL",
                        "actual": {},
                        "expected": "non-empty schema contract",
                        "message": f"Expected schema '{dataset_name}' kosong."
                        }

            print(
                f"[SUCCESS] Tahap 1 Lolos -> Schema contract ditemukan "
                f"({len(expected_schema)} kolom). \n"
            )

    except Exception as e:
        print(f"[ERROR] Tahap 1 Exception -> Gagal memeriksa schema contract: {str(e)}", file=sys.stderr)

        return {"status": "ERROR",
                "actual": type(e).__name__,
                "expected": "successful schema contract check",
                "message": f"Gagal memeriksa schema contract '{dataset_name}': {str(e)}"
                }

    # 2. Cek kesesuaian kolom dengan expected schema (Column Check)
    try:
        print("[DEBUG] [2/4] Memeriksa kesesuaian kolom dengan schema contract...")
        print("  └─ Memeriksa required columns, extra columns, dan urutan kolom.")

        if expected_schema is None:
            print("[INFO] Expected schema tidak diberikan.")
            print("[INFO] Pemeriksaan kolom dilewati.")
            print("[SUCCESS] Tahap 2 Lolos -> Tidak ada expected schema yang harus dibandingkan. \n")

        else:
            # Expected columns mengikuti urutan yang didefinisikan pada schema contract.
            expected_columns = [
                column.strip().lower()
                for column in expected_schema.keys()
            ]

            # Actual columns mengikuti urutan DataFrame.
            actual_columns = dataframe.columns

            # Normalisasi actual columns untuk comparison.
            # strip() mengabaikan spasi awal/akhir.
            # lower() membuat comparison tidak case-sensitive.
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
                print("[FAIL] Tahap 2 Gagal -> Struktur kolom DataFrame tidak sesuai schema contract.")

                print(f"  └─ Expected : {expected_columns}")
                print(f"  └─ Actual   : {actual_columns}")

                if missing_columns:
                    print(f"  └─ Missing  : {missing_columns}")

                if unexpected_columns:
                    print(f"  └─ Extra    : {unexpected_columns}")

                if duplicate_columns:
                    print(f"  └─ Duplicate: {duplicate_columns}")

                if order_mismatch:
                    print("  └─ Order    : Urutan kolom actual berbeda dengan schema contract.")

                return {"status": "FAIL",
                        "actual": actual_columns,
                        "expected": expected_columns,
                        "message": f"Kolom DataFrame '{dataset_name}' tidak sesuai schema contract."
                        }

            print(
                f"[SUCCESS] Tahap 2 Lolos -> "
                f"{len(actual_columns)} kolom sesuai schema contract. \n"
            )

    except Exception as e:
        print(f"[ERROR] Tahap 2 Exception -> Gagal memeriksa struktur kolom schema: {str(e)}", file=sys.stderr)

        return {"status": "ERROR",
                "actual": type(e).__name__,
                "expected": "successful schema column check",
                "message": f"Gagal memeriksa struktur kolom schema '{dataset_name}': {str(e)}"
                }

    # 3. Cek data type setiap kolom (Data Type Check)
    try:
        print("[DEBUG] [3/4] Memeriksa data type setiap kolom...")

        if expected_schema is None:
            print("[INFO] Expected schema tidak diberikan.")
            print("[INFO] Pemeriksaan data type dilewati.")
            print("[SUCCESS] Tahap 3 Lolos -> Tidak ada expected schema yang harus dibandingkan. \n")

        else:
            actual_schema = dataframe.schema
            invalid_dtypes = []

            for column_name, schema_definition in expected_schema.items():
                normalized_column_name = column_name.strip().lower()

                # Cari nama kolom actual berdasarkan comparison yang case-insensitive.
                actual_column_name = next(
                    (
                        column
                        for column in dataframe.columns
                        if column.strip().lower() == normalized_column_name
                    ),
                    None
                )

                # Jika kolom tidak ditemukan, sudah ditangani pada Stage 2.
                if actual_column_name is None:
                    continue

                expected_dtype = schema_definition.get("dtype")
                actual_dtype = actual_schema.get(actual_column_name)

                if expected_dtype is None:
                    print(
                        f"[INFO] Data type expected untuk kolom "
                        f"'{actual_column_name}' tidak diberikan."
                    )

                    continue

                # Normalisasi expected dtype menjadi string untuk comparison.
                expected_dtype_normalized = str(expected_dtype).strip().lower()
                actual_dtype_normalized = str(actual_dtype).strip().lower()

                if expected_dtype_normalized != actual_dtype_normalized:
                    invalid_dtypes.append({
                        "column": actual_column_name,
                        "expected": expected_dtype,
                        "actual": actual_dtype
                    })

            if invalid_dtypes:
                print("[FAIL] Tahap 3 Gagal -> Terdapat kolom dengan data type tidak sesuai.")

                print(f"  └─ Actual   : {len(invalid_dtypes)} kolom bermasalah")

                for invalid_dtype in invalid_dtypes:
                    print(
                        f"  └─ Column '{invalid_dtype['column']}' : "
                        f"expected={invalid_dtype['expected']}, "
                        f"actual={invalid_dtype['actual']}"
                    )

                return {"status": "FAIL",
                        "actual": invalid_dtypes,
                        "expected": "DataFrame data types sesuai schema contract",
                        "message": f"Data type DataFrame '{dataset_name}' tidak sesuai schema contract."
                        }

            print(
                f"[SUCCESS] Tahap 3 Lolos -> "
                f"Seluruh data type sesuai schema contract. \n"
            )

    except Exception as e:
        print(f"[ERROR] Tahap 3 Exception -> Gagal memeriksa data type schema: {str(e)}", file=sys.stderr)

        return {"status": "ERROR",
                "actual": type(e).__name__,
                "expected": "successful schema data type check",
                "message": f"Gagal memeriksa data type schema '{dataset_name}': {str(e)}"
                }

    # 4. Cek nullable / non-nullable setiap kolom (Nullability Check)
    try:
        print("[DEBUG] [4/4] Memeriksa nullable / non-nullable setiap kolom...")
        print("  └─ Memastikan aturan nullability sesuai dengan schema contract.")

        if expected_schema is None:
            print("[INFO] Expected schema tidak diberikan.")
            print("[INFO] Pemeriksaan nullable dilewati.")
            print("[SUCCESS] Tahap 4 Lolos -> Tidak ada expected schema yang harus dibandingkan. \n")

        else:
            invalid_nullability = []

            for column_name, schema_definition in expected_schema.items():
                normalized_column_name = column_name.strip().lower()

                # Cari nama kolom actual berdasarkan comparison yang case-insensitive.
                actual_column_name = next(
                    (
                        column
                        for column in dataframe.columns
                        if column.strip().lower() == normalized_column_name
                    ),
                    None
                )

                # Jika kolom tidak ditemukan, sudah ditangani pada Stage 2.
                if actual_column_name is None:
                    continue

                nullable_expected = schema_definition.get("nullable")

                # Jika nullable tidak didefinisikan,
                # pemeriksaan nullable dilewati.
                if nullable_expected is None:
                    print(
                        f"[INFO] Nullability expected untuk kolom "
                        f"'{actual_column_name}' tidak diberikan."
                    )

                    continue

                # Polars menggunakan null_count untuk mengetahui
                # apakah actual column memiliki nilai null.
                null_count = dataframe.select(
                    pl.col(actual_column_name).null_count()
                ).item()

                has_null = null_count > 0

                # Jika nullable=False tetapi terdapat null,
                # schema contract dilanggar.
                if nullable_expected is False and has_null:
                    invalid_nullability.append({
                        "column": actual_column_name,
                        "expected_nullable": False,
                        "actual_nullable": True,
                        "null_count": null_count
                    })

            if invalid_nullability:
                print("[FAIL] Tahap 4 Gagal -> Terdapat kolom non-nullable yang memiliki null.")

                print(f"  └─ Actual   : {len(invalid_nullability)} kolom bermasalah")

                for invalid_null in invalid_nullability:
                    print(
                        f"  └─ Column '{invalid_null['column']}' : "
                        f"expected_nullable={invalid_null['expected_nullable']}, "
                        f"actual_nullable={invalid_null['actual_nullable']}, "
                        f"null_count={invalid_null['null_count']}"
                    )

                return {"status": "FAIL",
                        "actual": invalid_nullability,
                        "expected": "Non-nullable columns tidak memiliki null",
                        "message": f"Nullability DataFrame '{dataset_name}' tidak sesuai schema contract."
                        }

            print(
                f"[SUCCESS] Tahap 4 Lolos -> "
                f"Seluruh aturan nullable / non-nullable sesuai schema contract. \n"
            )

    except Exception as e:
        print(f"[ERROR] Tahap 4 Exception -> Gagal memeriksa nullable schema: {str(e)}", file=sys.stderr)

        return {"status": "ERROR",
                "actual": type(e).__name__,
                "expected": "successful schema nullability check",
                "message": f"Gagal memeriksa nullable schema '{dataset_name}': {str(e)}"
                }

    # Hasil Akhir Jika Lolos Seluruh Pengecekan
    print("-" * 70)
    print(f"[PASS] VALIDASI SUKSES: Schema '{dataset_name}' valid.")
    print(f"[PROVEN] DataFrame '{dataset_name}' memenuhi seluruh schema criteria.")
    print("-" * 70)

    return {"status": "PASS",
            "actual": {"dataset_name": dataset_name,
                       "column_count": len(dataframe.columns),
                       "columns": dataframe.columns,
                       "schema": {
                           column: str(dtype)
                           for column, dtype in dataframe.schema.items()
                       }
                       },
            "expected": expected_schema,
            "message": f"Schema DataFrame '{dataset_name}' valid."
            }