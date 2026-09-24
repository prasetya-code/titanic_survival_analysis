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
    print(f"[DEBUG] Schema columns       : {len(schema)}")

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
        semantic_type = column_schema.get("semantic_type")

        actual_column = csv_columns.get(
            column_name.strip().casefold()
        )

        print(f"{'-' * 70} \n")
        print(f"[DEBUG] Expected column     : {column_name}")

        if actual_column is None:
            print("[DEBUG] Actual column       : NOT FOUND")
            print(
                f"[DEBUG] Semantic type       : "
                f"{semantic_type}"
            )
            print(
                f"[DEBUG] Expected dtype      : "
                f"{expected_dtype}"
            )
            print("[DEBUG] Actual dtype        : NOT FOUND")
            print("[RESULT] Status             : FAIL")

            failed_columns.append(column_name)

            details.append({
                "column": column_name,
                "semantic_type": semantic_type,
                "status": "FAIL",
                "message": "Kolom tidak ditemukan di CSV.",
            })

            continue

        print(f"[DEBUG] Actual column       : {actual_column}")
        print(
            f"[DEBUG] Semantic type       : "
            f"{semantic_type}"
        )

        actual_dtype = None

        for row in rows:
            value = row.get(actual_column)

            if _is_null(value):
                continue

            value = str(value).strip()

            if (
                value.casefold() in {
                    "true",
                    "false",
                }
            ):
                actual_dtype = "boolean"

            else:
                try:
                    number = float(value)

                    if number.is_integer():
                        actual_dtype = "Int64"
                    else:
                        actual_dtype = "Float64"

                except (ValueError, TypeError):
                    try:
                        datetime.strptime(
                            value,
                            "%Y-%m-%d",
                        )
                        actual_dtype = "date"

                    except ValueError:
                        try:
                            datetime.fromisoformat(value)
                            actual_dtype = "datetime"

                        except ValueError:
                            actual_dtype = "string"

            break

        if actual_dtype is None:
            actual_dtype = str(expected_dtype)

        print(
            f"[DEBUG] Expected dtype      : "
            f"{expected_dtype}"
        )
        print(
            f"[DEBUG] Actual dtype        : "
            f"{actual_dtype}"
        )

        expected_dtype_normalized = str(
            expected_dtype
        ).strip().casefold()

        actual_dtype_normalized = str(
            actual_dtype
        ).strip().casefold()

        dtype_aliases = {
            "int64": {"int64", "integer", "int", "int32"},
            "float64": {
                "float64",
                "float32",
                "float",
                "double",
            },
            "boolean": {"boolean", "bool"},
            "datetime": {"datetime", "timestamp"},
            "string": {"string"},
            "date": {"date"},
        }

        expected_group = next(
            (
                group
                for group in dtype_aliases.values()
                if expected_dtype_normalized in group
            ),
            {expected_dtype_normalized},
        )

        if actual_dtype_normalized in expected_group:
            print("[RESULT] Status             : PASS")

            details.append({
                "column": column_name,
                "actual_column": actual_column,
                "semantic_type": semantic_type,
                "expected_dtype": expected_dtype,
                "actual_dtype": actual_dtype,
                "status": "PASS",
                "message": (
                    f"Dtype kolom sesuai "
                    f"{expected_dtype}."
                ),
            })

        else:
            print("[RESULT] Status             : FAIL")

            failed_columns.append(column_name)

            details.append({
                "column": column_name,
                "actual_column": actual_column,
                "semantic_type": semantic_type,
                "expected_dtype": expected_dtype,
                "actual_dtype": actual_dtype,
                "status": "FAIL",
                "message": (
                    f"Dtype tidak sesuai. "
                    f"Expected: {expected_dtype}, "
                    f"Actual: {actual_dtype}."
                ),
            })

    status = "FAIL" if failed_columns else "PASS"

    print(f"\n{'=' * 70}")
    print("[RESULT] DATA TYPE VALIDATION")
    print("=" * 70)
    print(f"[RESULT] Dataset             : {dataset_name}")
    print(f"[RESULT] Status              : {status}")

    if failed_columns:
        print(
            f"[RESULT] Failed columns      : "
            f"{failed_columns}"
        )
    else:
        print("[RESULT] Failed columns      : 0")

    return {
        "status": status,
        "message": (
            "Data type validation berhasil."
            if status == "PASS"
            else "Terdapat kolom dengan dtype tidak sesuai."
        ),
        "details": details,
    }