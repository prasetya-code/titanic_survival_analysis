import csv


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


def _normalize_value(value):
    if isinstance(value, str):
        return value.strip()

    return value


def _matches_allowed_value(value, allowed_value):
    value = _normalize_value(value)

    if isinstance(allowed_value, bool):
        return str(value).casefold() == str(
            allowed_value
        ).casefold()

    if isinstance(allowed_value, int):
        try:
            numeric_value = float(value)

            return (
                numeric_value.is_integer()
                and int(numeric_value) == allowed_value
            )

        except (ValueError, TypeError):
            return False

    if isinstance(allowed_value, float):
        try:
            return float(value) == allowed_value

        except (ValueError, TypeError):
            return False

    return str(value) == str(allowed_value)


def validate_allowed_value(
    file_path,
    dataset_name,
    schema,
):
    print("=" * 70)
    print("[INFO] VALIDASI ALLOWED VALUE")
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
    validated_columns = 0

    for column_name, column_schema in schema.items():
        allowed_values = column_schema.get(
            "allowed_values"
        )

        if allowed_values is None:
            continue

        validated_columns += 1

        print("-" * 70)
        print(f"[DEBUG] Column              : {column_name}")
        print(
            f"[DEBUG] Allowed values      : "
            f"{allowed_values}"
        )

        actual_column = csv_columns.get(
            column_name.strip().casefold()
        )

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

        invalid_rows = []
        skipped_null = 0

        for row_number, row in enumerate(rows, start=2):
            value = row.get(actual_column)

            if _is_null(value):
                skipped_null += 1
                continue

            is_allowed = any(
                _matches_allowed_value(
                    value,
                    allowed_value,
                )
                for allowed_value in allowed_values
            )

            if not is_allowed:
                invalid_rows.append({
                    "row": row_number,
                    "value": value,
                })

        print(
            f"[DEBUG] Invalid values     : "
            f"{len(invalid_rows)}"
        )
        print(f"[DEBUG] Skipped null        : {skipped_null}")

        if invalid_rows:
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
                    f"{len(invalid_rows)} nilai "
                    f"tidak termasuk allowed_values."
                ),
                "invalid_rows": invalid_rows[:20],
            })

        else:
            print("[RESULT] Status            : PASS")

            details.append({
                "column": column_name,
                "status": "PASS",
                "message": (
                    "Semua nilai termasuk "
                    "allowed_values."
                ),
            })

    if validated_columns == 0:
        print("[DEBUG] Tidak ada allowed_values dalam schema.")

    status = "FAIL" if failed_columns else "PASS"

    print("=" * 70)
    print("[RESULT] ALLOWED VALUE VALIDATION")
    print("=" * 70)
    print(f"[RESULT] Dataset             : {dataset_name}")
    print(f"[RESULT] Status              : {status}")

    return {
        "status": status,
        "message": (
            "Allowed value validation berhasil."
            if status == "PASS"
            else "Terdapat nilai di luar allowed_values."
        ),
        "details": details,
    }