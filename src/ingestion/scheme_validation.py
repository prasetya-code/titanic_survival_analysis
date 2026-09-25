from pathlib import Path
from datetime import datetime
from typing import Any
import csv
import re
import sys


# ======================================================================
# Helper: Generic Validation Result
# ======================================================================

def _validation_result(status: str, invalid_count: int = 0, details: list[dict] | None = None, message: str = "") -> dict:
    """
    Membuat struktur hasil validation yang konsisten.
    """

    return {
        "status": status,
        "invalid_count": invalid_count,
        "details": details or [],
        "message": message
    }


# ======================================================================
# Helper: Null Check
# ======================================================================

def _is_null(value: Any) -> bool:
    """
    Menentukan apakah value dianggap NULL oleh schema validation.
    """

    if value is None:
        return True

    return str(value).strip().lower() in {
        "",
        "null",
        "none",
        "nan"
    }


# ======================================================================
# Helper: Case-Insensitive Column Mapping
# ======================================================================

def _build_column_map(header: list[str]) -> dict[str, str]:
    """
    Membuat mapping nama kolom secara case-insensitive.

    Contoh:

        CSV Header:
            PassengerId
            Survived
            Pclass

        Hasil mapping:
            {
                "passengerid": "PassengerId",
                "survived": "Survived",
                "pclass": "Pclass"
            }

    Schema tetap boleh menggunakan lowercase.
    """

    column_map = {}

    for column in header:
        normalized_column = column.strip().casefold()
        column_map[normalized_column] = column

    return column_map


# ======================================================================
# Helper: Schema Column Lookup
# ======================================================================

def _get_actual_column(column: str, column_map: dict[str, str]) -> str | None:
    """
    Mencari nama kolom aktual CSV berdasarkan nama schema
    secara case-insensitive.

    Contoh:

        schema:
            passengerid

        CSV:
            PassengerId

        return:
            PassengerId
    """

    normalized_column = column.strip().casefold()

    return column_map.get(normalized_column)


# ======================================================================
# Helper: Type Validation
# ======================================================================

def _is_valid_type(value: Any, expected_type: str) -> bool:
    """
    Memeriksa apakah sebuah value sesuai expected data type.
    """

    if _is_null(value):
        return True

    value = str(value).strip()

    try:

        if expected_type == "string":
            return True

        if expected_type == "integer":
            int(value)
            return True

        if expected_type == "float":
            float(value)
            return True

        if expected_type == "boolean":
            return value.lower() in {
                "true",
                "false",
                "1",
                "0"
            }

        if expected_type == "date":
            datetime.strptime(value, "%Y-%m-%d")
            return True

        if expected_type == "datetime":
            datetime.fromisoformat(value)
            return True

        return False

    except (ValueError, TypeError):
        return False


# ======================================================================
# Helper: Format Validation
# ======================================================================

def _is_valid_format(value: Any, format_rule: str) -> bool:
    """
    Memeriksa format sebuah value.
    """

    if _is_null(value):
        return True

    value = str(value).strip()

    try:

        if format_rule == "email":
            return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value) is not None

        if format_rule == "date":
            datetime.strptime(value, "%Y-%m-%d")
            return True

        if format_rule == "datetime":
            datetime.fromisoformat(value)
            return True

        if format_rule.startswith("regex:"):
            pattern = format_rule[6:]
            return re.fullmatch(pattern, value) is not None

        return False

    except (
        ValueError,
        TypeError,
        re.error
    ):

        return False


# ======================================================================
# 1. Data Type Validation
# ======================================================================

def validate_data_type(rows: list[dict], schema: dict, column_map: dict[str, str]) -> dict:
    """
    Validasi tipe data setiap value terhadap schema.

    Nama kolom bersifat case-insensitive.
    """

    invalid_values = []

    for column, rules in schema.items():
        expected_type = rules.get("type")

        if expected_type is None:
            continue

        actual_column = _get_actual_column(column, column_map)

        # --------------------------------------------------------------
        # Column tidak ditemukan
        # --------------------------------------------------------------

        if actual_column is None:

            invalid_values.append({
                "column": column,
                "actual_column": None,
                "expected_type": expected_type,
                "error": "column_not_found"
            })

            continue

        # --------------------------------------------------------------
        # Validate value
        # --------------------------------------------------------------

        for row_number, row in enumerate(rows, start=2):

            value = row.get(actual_column)

            if not _is_valid_type(value, expected_type):

                invalid_values.append({
                    "row": row_number,
                    "column": column,
                    "actual_column": actual_column,
                    "value": value,
                    "expected_type": expected_type
                })

    status = ("PASS" if not invalid_values else "FAIL")

    return _validation_result(
        status=status,
        invalid_count=len(invalid_values),
        details=invalid_values,
        message="Data type validation selesai."
    )


# ======================================================================
# 2. Nullability Validation
# ======================================================================

def validate_nullability(rows: list[dict], schema: dict, column_map: dict[str, str]) -> dict:
    """
    Validasi apakah NULL diperbolehkan pada setiap kolom.

    Nama kolom bersifat case-insensitive.
    """

    invalid_values = []

    for column, rules in schema.items():
        nullable = rules.get("nullable", False)

        if nullable:
            continue

        actual_column = _get_actual_column(column, column_map)

        # --------------------------------------------------------------
        # Column tidak ditemukan
        # --------------------------------------------------------------

        if actual_column is None:

            invalid_values.append({
                "column": column,
                "actual_column": None,
                "error": "column_not_found"
            })

            continue

        # --------------------------------------------------------------
        # Validate NULL
        # --------------------------------------------------------------

        for row_number, row in enumerate(rows, start=2):

            value = row.get(actual_column)

            if _is_null(value):

                invalid_values.append({
                    "row": row_number,
                    "column": column,
                    "actual_column": actual_column,
                    "value": value
                })

    status = ("PASS" if not invalid_values else "FAIL")

    return _validation_result(
        status=status,
        invalid_count=len(invalid_values),
        details=invalid_values,
        message="Nullability validation selesai."
    )


# ======================================================================
# 3. Required Value Validation
# ======================================================================

def validate_required(rows: list[dict], schema: dict, column_map: dict[str, str]) -> dict:
    """
    Memvalidasi required field agar memiliki value.

    Nama kolom bersifat case-insensitive.
    """

    invalid_values = []

    for column, rules in schema.items():
        required = rules.get("required", False)

        if not required:
            continue

        actual_column = _get_actual_column(column, column_map)

        # --------------------------------------------------------------
        # Column tidak ditemukan
        # --------------------------------------------------------------

        if actual_column is None:

            invalid_values.append({
                "column": column,
                "actual_column": None,
                "error": "column_not_found"
            })

            continue

        # --------------------------------------------------------------
        # Validate required value
        # --------------------------------------------------------------

        for row_number, row in enumerate(rows, start=2):

            value = row.get(actual_column)

            if _is_null(value):

                invalid_values.append({
                    "row": row_number,
                    "column": column,
                    "actual_column": actual_column,
                    "value": value
                })

    status = ("PASS" if not invalid_values else "FAIL")

    return _validation_result(
        status=status,
        invalid_count=len(invalid_values),
        details=invalid_values,
        message="Required value validation selesai."
    )


# ======================================================================
# 4. Format Validation
# ======================================================================

def validate_pattern(rows: list[dict], schema: dict, column_map: dict[str, str]) -> dict:
    """
    Memvalidasi format value berdasarkan format rule.

    Nama kolom bersifat case-insensitive.
    """

    invalid_values = []

    for column, rules in schema.items():
        format_rule = rules.get("format")

        if format_rule is None:
            continue

        actual_column = _get_actual_column(column, column_map)

        # --------------------------------------------------------------
        # Column tidak ditemukan
        # --------------------------------------------------------------

        if actual_column is None:

            invalid_values.append({
                "column": column,
                "actual_column": None,
                "format": format_rule,
                "error": "column_not_found"
            })

            continue

        # --------------------------------------------------------------
        # Validate format
        # --------------------------------------------------------------

        for row_number, row in enumerate(rows, start=2):

            value = row.get(actual_column)

            if not _is_valid_format(value, format_rule):

                invalid_values.append({
                    "row": row_number,
                    "column": column,
                    "actual_column": actual_column,
                    "value": value,
                    "format": format_rule
                })

    status = ("PASS" if not invalid_values else "FAIL")

    return _validation_result(
        status=status,
        invalid_count=len(invalid_values),
        details=invalid_values,
        message="Format validation selesai."
    )


# ======================================================================
# 5. Range / Constraint Validation
# ======================================================================

def validate_constraint(rows: list[dict], schema: dict, column_map: dict[str, str]) -> dict:
    """
    Memvalidasi min/max constraint.

    Nama kolom bersifat case-insensitive.
    """

    invalid_values = []

    for column, rules in schema.items():
        minimum = rules.get("min")
        maximum = rules.get("max")

        if (minimum is None and maximum is None):
            continue

        actual_column = _get_actual_column(column, column_map)

        # --------------------------------------------------------------
        # Column tidak ditemukan
        # --------------------------------------------------------------

        if actual_column is None:

            invalid_values.append({
                "column": column,
                "actual_column": None,
                "constraint": {
                    "min": minimum,
                    "max": maximum
                },
                "error": "column_not_found"
            })

            continue

        # --------------------------------------------------------------
        # Validate constraint
        # --------------------------------------------------------------

        for row_number, row in enumerate(rows, start=2):
            value = row.get(actual_column)

            if _is_null(value):
                continue

            try:
                numeric_value = float(value)

            except (ValueError, TypeError):
                # Type validation menangani masalah tipe.
                continue

            if (minimum is not None and numeric_value < minimum):

                invalid_values.append({
                    "row": row_number,
                    "column": column,
                    "actual_column": actual_column,
                    "value": value,
                    "constraint": f">= {minimum}"
                })

            if (maximum is not None and numeric_value > maximum):

                invalid_values.append({
                    "row": row_number,
                    "column": column,
                    "actual_column": actual_column,
                    "value": value,
                    "constraint": f"<= {maximum}"
                })

    status = ("PASS" if not invalid_values else "FAIL")

    return _validation_result(
        status=status,
        invalid_count=len(invalid_values),
        details=invalid_values,
        message="Constraint validation selesai."
    )


# ======================================================================
# 6. Allowed Value Validation
# ======================================================================

def validate_allowed_value(rows: list[dict], schema: dict, column_map: dict[str, str]) -> dict:
    """
    Memvalidasi apakah value termasuk allowed values.

    Nama kolom bersifat case-insensitive.
    """

    invalid_values = []

    for column, rules in schema.items():
        allowed_values = rules.get("allowed")

        if allowed_values is None:
            continue

        actual_column = _get_actual_column(column, column_map)

        # --------------------------------------------------------------
        # Column tidak ditemukan
        # --------------------------------------------------------------

        if actual_column is None:

            invalid_values.append({
                "column": column,
                "actual_column": None,
                "allowed": allowed_values,
                "error": "column_not_found"
            })

            continue

        # --------------------------------------------------------------
        # Validate allowed values
        # --------------------------------------------------------------

        for row_number, row in enumerate(rows, start=2):
            value = row.get(actual_column)

            if _is_null(value):
                continue

            if value not in allowed_values:

                invalid_values.append({
                    "row": row_number,
                    "column": column,
                    "actual_column": actual_column,
                    "value": value,
                    "allowed": allowed_values
                })

    status = ("PASS" if not invalid_values else "FAIL")

    return _validation_result(
        status=status,
        invalid_count=len(invalid_values),
        details=invalid_values,
        message="Allowed value validation selesai."
    )


# ======================================================================
# 7. Unique Value Validation
# ======================================================================

def validate_unique(rows: list[dict], schema: dict, column_map: dict[str, str]) -> dict:
    """
    Memvalidasi uniqueness pada kolom yang ditandai unique=True.

    Nama kolom bersifat case-insensitive.
    """

    invalid_values = []

    for column, rules in schema.items():
        if not rules.get("unique", False):
            continue

        actual_column = _get_actual_column(column, column_map)

        # --------------------------------------------------------------
        # Column tidak ditemukan
        # --------------------------------------------------------------

        if actual_column is None:

            invalid_values.append({
                "column": column,
                "actual_column": None,
                "error": "column_not_found"
            })

            continue

        # --------------------------------------------------------------
        # Collect values
        # --------------------------------------------------------------

        values = [
            row.get(actual_column)
            for row in rows
            if not _is_null(
                row.get(actual_column)
            )
        ]

        seen = set()

        duplicates = set()

        for value in values:
            if value in seen:
                duplicates.add(value)

            else:
                seen.add(value)

        if duplicates:

            invalid_values.append({
                "column": column,
                "actual_column": actual_column,
                "duplicates": list(duplicates)
            })

    status = ("PASS" if not invalid_values else "FAIL")

    return _validation_result(
        status=status,
        invalid_count=len(invalid_values),
        details=invalid_values,
        message="Unique value validation selesai."
    )


# ======================================================================
# 8. Primary Key Validation
# ======================================================================

def validate_primary_key(rows: list[dict], schema: dict, column_map: dict[str, str]) -> dict:
    """
    Memvalidasi primary key:

    - harus didefinisikan
    - tidak boleh NULL
    - harus UNIQUE

    Nama kolom bersifat case-insensitive.
    """

    primary_key_columns = [
        column
        for column, rules in schema.items()
        if rules.get(
            "primary_key",
            False
        )
    ]

    if not primary_key_columns:

        return _validation_result(
            status="PASS",
            message="Primary key tidak didefinisikan."
        )

    invalid_values = []

    # --------------------------------------------------------------
    # Resolve actual CSV column names
    # --------------------------------------------------------------

    actual_primary_key_columns = []

    for column in primary_key_columns:
        actual_column = _get_actual_column(column, column_map)

        if actual_column is None:

            invalid_values.append({
                "column": column,
                "actual_column": None,
                "error": "column_not_found"
            })

        else:

            actual_primary_key_columns.append(
                actual_column
            )

    # --------------------------------------------------------------
    # Stop jika ada primary key column yang tidak ditemukan
    # --------------------------------------------------------------

    if invalid_values:

        return _validation_result(
            status="FAIL",
            invalid_count=len(invalid_values),
            details=invalid_values,
            message="Primary key column tidak ditemukan."
        )

    # --------------------------------------------------------------
    # Single-column primary key
    # --------------------------------------------------------------

    if len(primary_key_columns) == 1:

        primary_key = primary_key_columns[0]

        actual_primary_key = actual_primary_key_columns[0]

        values = [
            row.get(actual_primary_key)
            for row in rows
        ]

        # ----------------------------------------------------------
        # Check NULL
        # ----------------------------------------------------------

        null_rows = [
            {
                "row": row_number,
                "column": primary_key,
                "actual_column": actual_primary_key,
                "value": value
            }
            for row_number, value in enumerate(
                values,
                start=2
            )
            if _is_null(value)
        ]

        # ----------------------------------------------------------
        # Check duplicate
        # ----------------------------------------------------------

        non_null_values = [
            value
            for value in values
            if not _is_null(value)
        ]

        seen = set()

        duplicate_values = set()

        for value in non_null_values:
            if value in seen:
                duplicate_values.add(value)

            else:
                seen.add(value)

        if null_rows:
            invalid_values.extend(null_rows)

        if duplicate_values:

            invalid_values.append({
                "column": primary_key,
                "actual_column": actual_primary_key,
                "duplicates": list(
                    duplicate_values
                )
            })

    # --------------------------------------------------------------
    # Composite primary key
    # --------------------------------------------------------------

    else:
        key_values = []

        for row_number, row in enumerate(rows, start=2):

            key = tuple(
                row.get(actual_column)
                for actual_column
                in actual_primary_key_columns
            )

            if any(_is_null(value) for value in key):

                invalid_values.append({
                    "row": row_number,
                    "columns": primary_key_columns,
                    "actual_columns": actual_primary_key_columns,
                    "key": key
                })

            key_values.append(key)

        seen = set()

        duplicate_keys = set()

        for key in key_values:
            if key in seen:
                duplicate_keys.add(key)

            else:
                seen.add(key)

        if duplicate_keys:
            invalid_values.append({
                "columns": primary_key_columns,
                "actual_columns": actual_primary_key_columns,
                "duplicates": list(
                    duplicate_keys
                )
            })

    status = ("PASS" if not invalid_values else "FAIL")

    return _validation_result(
        status=status,
        invalid_count=len(invalid_values),
        details=invalid_values,
        message="Primary key validation selesai."
    )


# ======================================================================
# Helper: Validation Reporter
# ======================================================================

def _print_validation_result(validation_name: str, result: dict, expected: str, checked: str | None = None) -> None:
    """
    Menampilkan hasil validation dengan format konsisten.
    """

    print(f"\n[DEBUG] {validation_name}")
    print(f"  ├─ Expected  : {expected}")

    if checked is not None:
        print(f"  ├─ Checked   : {checked}")

    if result["status"] == "PASS":
        print("  ├─ Invalid   : 0")
        print("  └─ Result    : PASS")

    elif result["status"] == "FAIL":

        print(f"  ├─ Invalid   : {result['invalid_count']}")

        for detail in result["details"][:10]:
            if detail.get("error") == "column_not_found":

                print(f"  ├─ Column    : {detail['column']}")
                print(f"  │  └─ Error  : Column tidak ditemukan di CSV")

            elif "row" in detail:

                print(f"  ├─ Row {detail['row']} : {detail}")

            else:
                print(f"  ├─ Detail    : {detail}")

        if result["invalid_count"] > 10:
            print(f"  ├─ More      : {result['invalid_count'] - 10} lainnya")

        print("  └─ Result    : FAIL")

    else:
        print("  ├─ Result    : ERROR")


# ======================================================================
# Main Schema Validation
# ======================================================================

def check_csv_schema(file_path: Path, dataset_name: str = "dataset", schema: dict | None = None) -> dict:
    """
    Schema validation utama.

    Validation:

    1. Data Type
    2. Nullability
    3. Required Value
    4. Format
    5. Range / Constraint
    6. Allowed Value
    7. Unique Value
    8. Primary Key

    Nama kolom schema bersifat CASE-INSENSITIVE
    terhadap nama kolom CSV.
    """

    print("\n" + "=" * 70)
    print(f"[INFO] Memulai Schema Validation Dataset: '{dataset_name}'")
    print("=" * 70)

    print("\n[DEBUG] Target:")
    print(f"  ├─ Path      : {file_path.resolve()}")
    print(f"  ├─ File      : {file_path.name}")
    print(f"  └─ Dataset   : {dataset_name}")

    # ==================================================================
    # Schema Configuration
    # ==================================================================

    if schema is None:

        print("\n[DEBUG] Schema Configuration")
        print("  ├─ Expected  : Schema validation configuration tersedia")
        print("  ├─ Actual    : Schema tidak diberikan")
        print("  └─ Result    : FAIL")

        return {
            "status": "FAIL",
            "actual": None,
            "expected": "schema configuration",
            "message": f"Schema dataset '{dataset_name}' tidak diberikan."
        }

    # ==================================================================
    # Load Dataset
    # ==================================================================

    try:

        print("\n[DEBUG] Loading Dataset")

        with file_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            header = reader.fieldnames or []
            rows = list(reader)

        print(f"  ├─ Columns   : {len(header)}")
        print(f"  ├─ Rows      : {len(rows)}")
        print(f"  └─ Result    : PASS")

    except UnicodeDecodeError as e:

        print(f"  ├─ Expected  : UTF-8 compatible CSV file")
        print(f"  ├─ Actual    : {type(e).__name__}")
        print(f"  └─ Result    : ERROR")

        print(f"[ERROR] Encoding file CSV tidak kompatibel dengan UTF-8: {str(e)}", file=sys.stderr)

        return {
            "status": "ERROR",
            "actual": type(e).__name__,
            "expected": "UTF-8 compatible CSV file",
            "message": str(e)
        }

    except csv.Error as e:

        print(f"  ├─ Expected  : Valid CSV data")
        print(f"  ├─ Actual    : {type(e).__name__}")
        print(f"  └─ Result    : ERROR")

        return {
            "status": "ERROR",
            "actual": type(e).__name__,
            "expected": "valid CSV data",
            "message": str(e)
        }

    except Exception as e:

        print(f"  ├─ Expected  : Successful CSV loading")
        print(f"  ├─ Actual    : {type(e).__name__}")
        print(f"  └─ Result    : ERROR")

        return {
            "status": "ERROR",
            "actual": type(e).__name__,
            "expected": "successful CSV loading",
            "message": str(e)
        }

    # ==================================================================
    # Build Case-Insensitive Column Map
    # ==================================================================

    column_map = _build_column_map(header)

    print(f"\n[DEBUG] Column Mapping")
    print(f"  ├─ Mode      : CASE-INSENSITIVE")
    print(f"  ├─ CSV Header:")

    for column in header:
        print(f"  │  ├─ {column}")

    print(f"  └─ Schema Mapping:")

    for schema_column in schema:
        actual_column = _get_actual_column(schema_column, column_map)

        if actual_column is not None:
            print(f"     ├─ {schema_column} → {actual_column}")

        else:
            print(f"     ├─ {schema_column} → NOT FOUND")

    # ==================================================================
    # Execute 8 Validation Helpers
    # ==================================================================

    validation_results = {}

    validation_results["data_type"] = validate_data_type(
        rows,
        schema,
        column_map
    )

    validation_results["nullability"] = validate_nullability(
        rows,
        schema,
        column_map
    )

    validation_results["required"] = validate_required(
        rows,
        schema,
        column_map
    )

    validation_results["format"] = validate_pattern(
        rows,
        schema,
        column_map
    )

    validation_results["constraint"] = validate_constraint(
        rows,
        schema,
        column_map
    )

    validation_results["allowed_value"] = validate_allowed_value(
        rows,
        schema,
        column_map
    )

    validation_results["unique"] = validate_unique(
        rows,
        schema,
        column_map
    )

    validation_results["primary_key"] = validate_primary_key(
        rows,
        schema,
        column_map
    )

    # ==================================================================
    # Reporting
    # ==================================================================

    _print_validation_result(
        "[1/8] Data Type Validation",
        validation_results["data_type"],
        "Tipe data sesuai expected schema",
        f"{len(schema)} kolom"
    )

    _print_validation_result(
        "[2/8] Nullability Validation",
        validation_results["nullability"],
        "NULL hanya diperbolehkan pada kolom nullable",
        f"{len(schema)} kolom"
    )

    _print_validation_result(
        "[3/8] Required Value Validation",
        validation_results["required"],
        "Required field memiliki value",
        f"{len(schema)} kolom"
    )

    _print_validation_result(
        "[4/8] Format Validation",
        validation_results["format"],
        "Nilai mengikuti format schema"
    )

    _print_validation_result(
        "[5/8] Range / Constraint Validation",
        validation_results["constraint"],
        "Nilai memenuhi range / constraint"
    )

    _print_validation_result(
        "[6/8] Allowed Value Validation",
        validation_results["allowed_value"],
        "Nilai hanya berasal dari allowed values"
    )

    _print_validation_result(
        "[7/8] Unique Value Validation",
        validation_results["unique"],
        "Kolom unique tidak memiliki duplicate"
    )

    _print_validation_result(
        "[8/8] Primary Key Validation",
        validation_results["primary_key"],
        "Primary key valid, NOT NULL dan UNIQUE"
    )

    # ==================================================================
    # Final Status
    # ==================================================================

    total_validation = len(
        validation_results
    )

    passed_validation = sum(
        result["status"] == "PASS"
        for result in validation_results.values()
    )

    failed_validation = sum(
        result["status"] == "FAIL"
        for result in validation_results.values()
    )

    error_validation = sum(
        result["status"] == "ERROR"
        for result in validation_results.values()
    )

    if error_validation > 0:
        final_status = "ERROR"

    elif failed_validation > 0:
        final_status = "FAIL"

    else:
        final_status = "PASS"

    # ==================================================================
    # Final Output
    # ==================================================================

    print("\n" + "-" * 70)

    if final_status == "PASS":

        print(f"[PASS] VALIDASI SUKSES: Schema dataset '{dataset_name}' valid.")

    elif final_status == "FAIL":
        print(f"[FAIL] VALIDASI GAGAL: Schema dataset '{dataset_name}' tidak valid.")

    else:
        print(f"[ERROR] VALIDASI ERROR: Schema dataset '{dataset_name}' tidak dapat divalidasi.")

    print("-" * 70)
    print("\n[DEBUG] Validation Summary:")
    print(f"  ├─ Dataset       : {dataset_name}")
    print(f"  ├─ File          : {file_path.name}")
    print(f"  ├─ Columns       : {len(header)}")
    print(f"  ├─ Rows          : {len(rows)}")
    print(f"  ├─ Data Type     : {validation_results['data_type']['status']}")
    print(f"  ├─ Nullability   : {validation_results['nullability']['status']}")
    print(f"  ├─ Required      : {validation_results['required']['status']}")
    print(f"  ├─ Format        : {validation_results['format']['status']}")
    print(f"  ├─ Constraint    : {validation_results['constraint']['status']}")
    print(f"  ├─ Allowed Value : {validation_results['allowed_value']['status']}")
    print(f"  ├─ Unique        : {validation_results['unique']['status']}")
    print(f"  ├─ Primary Key   : {validation_results['primary_key']['status']}")
    print(f"  └─ Result        : {passed_validation}/{total_validation} PASS")
    print("=" * 70)

    return {
        "status": final_status,
        "actual": {
            "path": str(file_path),
            "file_name": file_path.name,
            "column_count": len(header),
            "row_count": len(rows),
            "validation": validation_results
        },
        "expected": {
            "schema": schema
        },
        "message": (
            f"Schema dataset '{dataset_name}' valid."
            if final_status == "PASS"
            else
            f"Schema dataset '{dataset_name}' tidak valid."
        )
    }
