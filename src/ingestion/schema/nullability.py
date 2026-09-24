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


def validate_nullability(
    file_path,
    dataset_name,
    schema,
):
    print("=" * 70)
    print("[INFO] VALIDASI NULLABILITY")
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

    total_rows = len(rows)

    print(f"[DEBUG] CSV columns          : {len(fieldnames)}")
    print(f"[DEBUG] Data rows            : {total_rows}")
    print(f"{'-' * 70}\n")

    details = []
    failed_columns = []

    for column_name, column_schema in schema.items():
        nullable = column_schema.get("nullable")
        max_null_ratio = column_schema.get("max_null_ratio")

        print(f"[DEBUG] Column              : {column_name}")
        print(f"[DEBUG] Nullable            : {nullable}")
        print(f"[DEBUG] Max null ratio      : {max_null_ratio}")

        actual_column = csv_columns.get(
            column_name.strip().casefold()
        )

        if actual_column is None:
            print("[DEBUG] Actual column       : NOT FOUND")
            print("[RESULT] Status             : FAIL")

            failed_columns.append(column_name)

            details.append({
                "column": column_name,
                "status": "FAIL",
                "message": "Kolom tidak ditemukan di CSV.",
            })

            continue

        null_count = sum(
            _is_null(row.get(actual_column))
            for row in rows
        )

        null_ratio = (
            null_count / total_rows
            if total_rows > 0
            else 0
        )

        print(f"[DEBUG] Null count          : {null_count}")
        print(
            f"[DEBUG] Null ratio          : "
            f"{null_ratio:.2f}"
        )

        column_failed = False
        messages = []

        if nullable is False and null_count > 0:
            column_failed = True

            messages.append(
                f"Kolom tidak boleh null, "
                f"tetapi ditemukan {null_count} null."
            )

        if (
            max_null_ratio is not None
            and null_ratio > float(max_null_ratio)
        ):
            column_failed = True

            messages.append(
                f"Null ratio {null_ratio:.4f} "
                f"melebihi batas "
                f"{float(max_null_ratio):.4f}."
            )

        if column_failed:
            print("[RESULT] Status             : FAIL")

            failed_columns.append(column_name)

            details.append({
                "column": column_name,
                "status": "FAIL",
                "message": " ".join(messages),
                "null_count": null_count,
                "null_ratio": null_ratio,
            })

        else:
            print("[RESULT] Status             : PASS")

            details.append({
                "column": column_name,
                "status": "PASS",
                "message": "Nullability sesuai schema.",
                "null_count": null_count,
                "null_ratio": null_ratio,
            })

    status = "FAIL" if failed_columns else "PASS"

    print(f"\n{'=' * 70}")
    print("[RESULT] NULLABILITY VALIDATION")
    print("=" * 70)
    print(f"[RESULT] Dataset             : {dataset_name}")
    print(f"[RESULT] Status              : {status}")

    return {
        "status": status,
        "message": (
            "Nullability validation berhasil."
            if status == "PASS"
            else "Terdapat pelanggaran nullability."
        ),
        "details": details,
    }