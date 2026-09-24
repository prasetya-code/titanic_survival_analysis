import csv
from datetime import datetime


def _is_null(value):
    if value is None:
        return True

    value = str(value).strip().casefold()

    return value in {
        "",
        "null",
        "none",
        "nan",
    }


def _is_valid_dtype(value, expected_dtype):
    if _is_null(value):
        return True

    value = str(value).strip()

    dtype = str(expected_dtype).strip().casefold()

    if dtype == "string":
        return True

    if dtype in {"int64", "int32", "integer", "int"}:
        try:
            number = float(value)

            if not number.is_integer():
                return False

            int(number)
            return True

        except (ValueError, TypeError):
            return False

    if dtype in {"float64", "float32", "float", "double"}:
        try:
            float(value)
            return True

        except (ValueError, TypeError):
            return False

    if dtype in {"boolean", "bool"}:
        return value.casefold() in {
            "true",
            "false",
            "1",
            "0",
        }

    if dtype == "date":
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True

        except ValueError:
            return False

    if dtype in {"datetime", "timestamp"}:
        try:
            datetime.fromisoformat(value)
            return True

        except ValueError:
            return False

    return True


def validate_data_type(
    file_path,
    dataset_name,
    schema,
):
    print("=" * 70)
    print("[INFO] VALIDASI DATA TYPE")
    print("=" * 70)

    print(f"[DEBUG] Dataset              : {dataset_name}")
    print(f"[DEBUG] File                 : {file_path}")
    print(f"[DEBUG] Schema columns      : {len(schema)}")

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            reader = csv.DictReader(file)

            fieldnames = reader.fieldnames or []
            rows = list(reader)

    except Exception as error:
        print(f"[ERROR] Gagal membaca CSV: {error}")

        return {
            "status": "ERROR",
            "message": f"Gagal membaca CSV: {error}",
            "details": [],
        }

    csv_columns = {
        column.strip().casefold(): column
        for column in fieldnames
    }

    print(f"[DEBUG] CSV columns          : {len(fieldnames)}")
    print(f"[DEBUG] Data rows            : {len(rows)}")

    details = []
    failed_columns = []

    for column_name, column_schema in schema.items():
        expected_dtype = column_schema.get("dtype")

        actual_column = csv_columns.get(
            column_name.strip().casefold()
        )

        print("-" * 70)
        print(f"[DEBUG] Column              : {column_name}")
        print(f"[DEBUG] Expected dtype      : {expected_dtype}")

        if actual_column is None:
            print("[DEBUG] Actual column       : NOT FOUND")
            print("[RESULT] Status            : FAIL")

            failed_columns.append(column_name)

            details.append({
                "column": column_name,
                "status": "FAIL",
                "message": "Kolom tidak ditemukan di CSV.",
            })

            continue

        print(f"[DEBUG] Actual column       : {actual_column}")

        invalid_rows = []

        for row_number, row in enumerate(rows, start=2):
            value = row.get(actual_column)

            if not _is_valid_dtype(
                value,
                expected_dtype,
            ):
                invalid_rows.append({
                    "row": row_number,
                    "value": value,
                })

        if invalid_rows:
            print(
                f"[DEBUG] Invalid values     : "
                f"{len(invalid_rows)}"
            )
            print(
                f"[DEBUG] Sample rows        : "
                f"{invalid_rows[:5]}"
            )
            print("[RESULT] Status            : FAIL")

            failed_columns.append(column_name)

            details.append({
                "column": column_name,
                "status": "FAIL",
                "message": (
                    f"{len(invalid_rows)} nilai tidak "
                    f"sesuai dtype {expected_dtype}."
                ),
                "invalid_rows": invalid_rows[:20],
            })

        else:
            print("[DEBUG] Invalid values     : 0")
            print("[RESULT] Status            : PASS")

            details.append({
                "column": column_name,
                "status": "PASS",
                "message": (
                    f"Semua nilai sesuai dtype "
                    f"{expected_dtype}."
                ),
            })

    status = "FAIL" if failed_columns else "PASS"

    print("=" * 70)
    print("[RESULT] DATA TYPE VALIDATION")
    print("=" * 70)
    print(f"[RESULT] Dataset             : {dataset_name}")
    print(f"[RESULT] Status              : {status}")

    if failed_columns:
        print(
            f"[RESULT] Failed columns     : "
            f"{failed_columns}"
        )
    else:
        print("[RESULT] Failed columns     : 0")

    return {
        "status": status,
        "message": (
            "Data type validation berhasil."
            if status == "PASS"
            else "Terdapat nilai dengan dtype tidak sesuai."
        ),
        "details": details,
    }