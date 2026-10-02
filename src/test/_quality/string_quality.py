import csv
import re


def _is_null(value):
    if value is None:
        return True

    value = str(value).strip().casefold()

    return value in {
        "",
        "null",
        "none",
        "nan",
        "n/a",
    }


def validate_string_quality(
    file_path,
    dataset_name,
    schema,
):
    print("=" * 70)
    print("[INFO] VALIDASI STRING QUALITY")
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
        print(
            f"[ERROR] Gagal membaca CSV: {error}"
        )

        return {
            "status": "ERROR",
            "message": (
                f"Gagal membaca CSV: {error}"
            ),
            "details": [],
        }

    print(f"[DEBUG] CSV columns          : {len(fieldnames)}")
    print(f"[DEBUG] Data rows            : {len(rows)}")

    csv_columns = {
        column.strip().casefold(): column
        for column in fieldnames
    }

    # ----------------------------------------------------------
    # STRING COLUMNS
    # ----------------------------------------------------------

    string_columns = []

    for column_name, column_schema in schema.items():

        dtype = str(
            column_schema.get(
                "dtype",
                "",
            )
        ).casefold()

        semantic_type = str(
            column_schema.get(
                "semantic_type",
                "",
            )
        ).casefold()

        if (
            dtype in {
                "string",
                "str",
            }
            or semantic_type in {
                "text",
                "string",
            }
        ):
            string_columns.append(
                column_name
            )

    print(
        f"[DEBUG] String columns      : "
        f"{string_columns}"
    )

    if not string_columns:
        print(
            "[DEBUG] Tidak ada string column "
            "dalam schema."
        )
        print("[RESULT] Status            : PASS")

        return {
            "status": "PASS",
            "message": (
                "Tidak ada string column "
                "dalam schema."
            ),
            "details": [],
        }

    details = []
    failed = False

    # ==========================================================
    # VALIDATION PER COLUMN
    # ==========================================================

    for column_name in string_columns:

        print("-" * 70)
        print(
            f"[DEBUG] Column              : "
            f"{column_name}"
        )

        column_schema = schema.get(
            column_name,
            {}
        )

        actual_column = csv_columns.get(
            column_name.strip().casefold()
        )

        if actual_column is None:

            print(
                "[DEBUG] Actual column       : "
                "NOT FOUND"
            )
            print(
                "[RESULT] Column status      : FAIL"
            )

            failed = True

            details.append({
                "column": column_name,
                "status": "FAIL",
                "message": (
                    "String column tidak "
                    "ditemukan di CSV."
                ),
            })

            continue

        print(
            f"[DEBUG] Actual column       : "
            f"{actual_column}"
        )

        # ------------------------------------------------------
        # RULE CONFIGURATION
        # ------------------------------------------------------

        casing_rule = column_schema.get(
            "casing"
        )

        if casing_rule is not None:
            casing_rule = str(
                casing_rule
            ).casefold()

        allowed_values = column_schema.get(
            "allowed_values"
        )

        # ------------------------------------------------------
        # COUNTER
        # ------------------------------------------------------

        leading_trailing_rows = []
        multiple_spaces_rows = []
        empty_string_rows = []
        invalid_character_rows = []
        casing_rows = []
        encoding_rows = []
        missing_like_rows = []
        allowed_value_rows = []

        # ------------------------------------------------------
        # ROW VALIDATION
        # ------------------------------------------------------

        for row_number, row in enumerate(
            rows,
            start=2,
        ):

            value = row.get(
                actual_column
            )

            # ==================================================
            # 1. LEADING / TRAILING WHITESPACE
            # ==================================================

            if value is not None:

                raw_value = str(value)

                if (
                    raw_value != raw_value.strip()
                ):
                    leading_trailing_rows.append(
                        row_number
                    )

            # ==================================================
            # 2. MULTIPLE SPACES
            # ==================================================

            if value is not None:

                raw_value = str(value)

                if re.search(
                    r"[ \t]{2,}",
                    raw_value,
                ):
                    multiple_spaces_rows.append(
                        row_number
                    )

            # ==================================================
            # 3. EMPTY STRING
            # ==================================================

            if value is not None:

                raw_value = str(value)

                if raw_value.strip() == "":
                    empty_string_rows.append(
                        row_number
                    )

            # ==================================================
            # 4. INVALID / UNUSUAL CHARACTERS
            # ==================================================

            if value is not None:

                raw_value = str(value)

                invalid_characters = [
                    character
                    for character in raw_value
                    if not character.isprintable()
                    and character not in {
                        "\t",
                        "\n",
                        "\r",
                    }
                ]

                if invalid_characters:
                    invalid_character_rows.append({
                        "row": row_number,
                        "characters": list(
                            set(
                                invalid_characters
                            )
                        ),
                    })

            # ==================================================
            # 5. CASING CONSISTENCY
            # ==================================================

            if (
                value is not None
                and not _is_null(value)
                and casing_rule
            ):

                raw_value = str(value).strip()

                casing_valid = True

                if casing_rule == "upper":

                    casing_valid = (
                        raw_value == raw_value.upper()
                    )

                elif casing_rule == "lower":

                    casing_valid = (
                        raw_value == raw_value.lower()
                    )

                elif casing_rule == "title":

                    casing_valid = (
                        raw_value == raw_value.title()
                    )

                elif casing_rule == "sentence":

                    casing_valid = (
                        raw_value == raw_value.capitalize()
                    )

                elif casing_rule in {
                    "none",
                    "any",
                }:

                    casing_valid = True

                if not casing_valid:
                    casing_rows.append(
                        row_number
                    )

            # ==================================================
            # 6. ENCODING
            # ==================================================

            if value is not None:

                try:
                    str(value).encode(
                        "utf-8"
                    )

                except UnicodeEncodeError:
                    encoding_rows.append(
                        row_number
                    )

            # ==================================================
            # 7. MISSING-LIKE STRING
            # ==================================================

            if value is not None:

                normalized_value = (
                    str(value)
                    .strip()
                    .casefold()
                )

                if normalized_value in {
                    "null",
                    "none",
                    "nan",
                    "n/a",
                }:
                    missing_like_rows.append(
                        row_number
                    )

            # ==================================================
            # 8. ALLOWED VALUES
            # ==================================================

            if (
                value is not None
                and not _is_null(value)
                and allowed_values is not None
            ):

                raw_value = str(value).strip()

                allowed_values_normalized = {
                    str(allowed_value)
                    .strip()
                    .casefold()
                    for allowed_value
                    in allowed_values
                }

                if (
                    raw_value.casefold()
                    not in allowed_values_normalized
                ):
                    allowed_value_rows.append(
                        row_number
                    )

        # ======================================================
        # RESULT PER PARAMETER
        # ======================================================

        column_failed = False

        # ------------------------------------------------------
        # 1. LEADING / TRAILING WHITESPACE
        # ------------------------------------------------------

        if leading_trailing_rows:

            column_failed = True

            print(
                f"[RESULT] Whitespace         : "
                f"FAIL ({len(leading_trailing_rows)})"
            )

            details.append({
                "column": column_name,
                "parameter": (
                    "leading_trailing_whitespace"
                ),
                "status": "FAIL",
                "message": (
                    "Ditemukan leading atau "
                    "trailing whitespace."
                ),
                "rows": leading_trailing_rows[:50],
            })

        else:

            print(
                "[RESULT] Whitespace         : PASS (0)"
            )

            details.append({
                "column": column_name,
                "parameter": (
                    "leading_trailing_whitespace"
                ),
                "status": "PASS",
                "message": (
                    "Tidak ditemukan leading "
                    "atau trailing whitespace."
                ),
            })

        # ------------------------------------------------------
        # 2. MULTIPLE SPACES
        # ------------------------------------------------------

        if multiple_spaces_rows:

            column_failed = True

            print(
                f"[RESULT] Multiple spaces    : "
                f"FAIL ({len(multiple_spaces_rows)})"
            )

            details.append({
                "column": column_name,
                "parameter": "multiple_spaces",
                "status": "FAIL",
                "message": (
                    "Ditemukan multiple spaces "
                    "di dalam string."
                ),
                "rows": multiple_spaces_rows[:50],
            })

        else:

            print(
                "[RESULT] Multiple spaces    : PASS (0)"
            )

            details.append({
                "column": column_name,
                "parameter": "multiple_spaces",
                "status": "PASS",
                "message": (
                    "Tidak ditemukan multiple "
                    "spaces."
                ),
            })

        # ------------------------------------------------------
        # 3. EMPTY STRING
        # ------------------------------------------------------

        if empty_string_rows:

            column_failed = True

            print(
                f"[RESULT] Empty string       : "
                f"FAIL ({len(empty_string_rows)})"
            )

            details.append({
                "column": column_name,
                "parameter": "empty_string",
                "status": "FAIL",
                "message": (
                    "Ditemukan string kosong "
                    "atau whitespace."
                ),
                "rows": empty_string_rows[:50],
            })

        else:

            print(
                "[RESULT] Empty string       : PASS (0)"
            )

            details.append({
                "column": column_name,
                "parameter": "empty_string",
                "status": "PASS",
                "message": (
                    "Tidak ditemukan empty string."
                ),
            })

        # ------------------------------------------------------
        # 4. INVALID / UNUSUAL CHARACTERS
        # ------------------------------------------------------

        if invalid_character_rows:

            column_failed = True

            print(
                f"[RESULT] Invalid character  : "
                f"FAIL ({len(invalid_character_rows)})"
            )

            details.append({
                "column": column_name,
                "parameter": (
                    "invalid_unusual_characters"
                ),
                "status": "FAIL",
                "message": (
                    "Ditemukan karakter "
                    "non-printable."
                ),
                "rows": invalid_character_rows[:50],
            })

        else:

            print(
                "[RESULT] Invalid character  : PASS (0)"
            )

            details.append({
                "column": column_name,
                "parameter": (
                    "invalid_unusual_characters"
                ),
                "status": "PASS",
                "message": (
                    "Tidak ditemukan karakter "
                    "non-printable."
                ),
            })

        # ------------------------------------------------------
        # 5. CASING CONSISTENCY
        # ------------------------------------------------------

        if casing_rule:

            if casing_rows:

                column_failed = True

                print(
                    f"[RESULT] Casing             : "
                    f"FAIL ({len(casing_rows)})"
                )

                details.append({
                    "column": column_name,
                    "parameter": (
                        "casing_consistency"
                    ),
                    "status": "FAIL",
                    "message": (
                        "Casing tidak sesuai "
                        "dengan rule."
                    ),
                    "rule": casing_rule,
                    "rows": casing_rows[:50],
                })

            else:

                print(
                    "[RESULT] Casing             : PASS (0)"
                )

                details.append({
                    "column": column_name,
                    "parameter": (
                        "casing_consistency"
                    ),
                    "status": "PASS",
                    "message": (
                        "Casing sesuai dengan rule."
                    ),
                    "rule": casing_rule,
                })

        else:

            print(
                "[RESULT] Casing             : SKIP"
            )

            details.append({
                "column": column_name,
                "parameter": (
                    "casing_consistency"
                ),
                "status": "SKIP",
                "message": (
                    "Casing rule tidak "
                    "didefinisikan."
                ),
            })

        # ------------------------------------------------------
        # 6. ENCODING
        # ------------------------------------------------------

        if encoding_rows:

            column_failed = True

            print(
                f"[RESULT] Encoding           : "
                f"FAIL ({len(encoding_rows)})"
            )

            details.append({
                "column": column_name,
                "parameter": "encoding",
                "status": "FAIL",
                "message": (
                    "Ditemukan karakter yang "
                    "tidak dapat di-encode "
                    "sebagai UTF-8."
                ),
                "rows": encoding_rows[:50],
            })

        else:

            print(
                "[RESULT] Encoding           : PASS (0)"
            )

            details.append({
                "column": column_name,
                "parameter": "encoding",
                "status": "PASS",
                "message": (
                    "String dapat di-encode "
                    "sebagai UTF-8."
                ),
            })

        # ------------------------------------------------------
        # 7. MISSING-LIKE STRING
        # ------------------------------------------------------

        if missing_like_rows:

            column_failed = True

            print(
                f"[RESULT] Missing-like       : "
                f"FAIL ({len(missing_like_rows)})"
            )

            details.append({
                "column": column_name,
                "parameter": "missing_like_string",
                "status": "FAIL",
                "message": (
                    "Ditemukan string yang "
                    "dianggap sebagai "
                    "missing value."
                ),
                "rows": missing_like_rows[:50],
            })

        else:

            print(
                "[RESULT] Missing-like       : PASS (0)"
            )

            details.append({
                "column": column_name,
                "parameter": "missing_like_string",
                "status": "PASS",
                "message": (
                    "Tidak ditemukan "
                    "missing-like string."
                ),
            })

        # ------------------------------------------------------
        # 8. ALLOWED VALUES
        # ------------------------------------------------------

        if allowed_values is not None:

            if allowed_value_rows:

                column_failed = True

                print(
                    f"[RESULT] Allowed value      : "
                    f"FAIL ({len(allowed_value_rows)})"
                )

                details.append({
                    "column": column_name,
                    "parameter": "allowed_values",
                    "status": "FAIL",
                    "message": (
                        "Ditemukan nilai yang "
                        "tidak terdapat dalam "
                        "allowed_values."
                    ),
                    "allowed_values": allowed_values,
                    "rows": allowed_value_rows[:50],
                })

            else:

                print(
                    "[RESULT] Allowed value      : PASS (0)"
                )

                details.append({
                    "column": column_name,
                    "parameter": "allowed_values",
                    "status": "PASS",
                    "message": (
                        "Semua nilai sesuai "
                        "dengan allowed_values."
                    ),
                    "allowed_values": allowed_values,
                })

        else:

            print(
                "[RESULT] Allowed value      : SKIP"
            )

            details.append({
                "column": column_name,
                "parameter": "allowed_values",
                "status": "SKIP",
                "message": (
                    "Allowed values tidak "
                    "didefinisikan."
                ),
            })

        # ------------------------------------------------------
        # COLUMN RESULT
        # ------------------------------------------------------

        if column_failed:
            failed = True

        print(
            f"[RESULT] Column status      : "
            f"{'FAIL' if column_failed else 'PASS'}"
        )

    # ==========================================================
    # FINAL RESULT
    # ==========================================================

    status = "FAIL" if failed else "PASS"

    print("=" * 70)
    print("[RESULT] STRING QUALITY VALIDATION")
    print("=" * 70)
    print(
        f"[RESULT] Dataset             : "
        f"{dataset_name}"
    )
    print(
        f"[RESULT] String columns      : "
        f"{string_columns}"
    )
    print(
        f"[RESULT] Status              : "
        f"{status}"
    )

    return {
        "status": status,
        "message": (
            "String quality validation berhasil."
            if status == "PASS"
            else
            "String quality validation gagal."
        ),
        "details": details,
    }
