import csv
import math
from collections import Counter


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


def _read_csv(file_path):
    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        fieldnames = reader.fieldnames or []
        rows = list(reader)

    return fieldnames, rows


def _to_number(value):
    if _is_null(value):
        return None

    try:
        return float(str(value).strip())
    except (ValueError, TypeError):
        return None


def _get_column_values(rows, column):
    return [
        row.get(column)
        for row in rows
        if not _is_null(row.get(column))
    ]


def _calculate_mean(values):
    numbers = [
        _to_number(value)
        for value in values
    ]

    numbers = [
        value
        for value in numbers
        if value is not None
    ]

    if not numbers:
        return None

    return sum(numbers) / len(numbers)


def _calculate_std(values):
    numbers = [
        _to_number(value)
        for value in values
    ]

    numbers = [
        value
        for value in numbers
        if value is not None
    ]

    if len(numbers) < 2:
        return None

    mean = sum(numbers) / len(numbers)

    variance = sum(
        (value - mean) ** 2
        for value in numbers
    ) / len(numbers)

    return math.sqrt(variance)


def _calculate_missing_rate(rows, column):
    if not rows:
        return 0.0

    missing = sum(
        1
        for row in rows
        if _is_null(row.get(column))
    )

    return missing / len(rows)


def _calculate_unique_rate(rows, column):
    if not rows:
        return 0.0

    values = [
        str(row.get(column)).strip()
        for row in rows
        if not _is_null(row.get(column))
    ]

    if not values:
        return 0.0

    return len(set(values)) / len(values)


def _calculate_distribution(values):
    cleaned_values = [
        str(value).strip()
        for value in values
        if not _is_null(value)
    ]

    counter = Counter(cleaned_values)

    total = len(cleaned_values)

    if total == 0:
        return {}

    return {
        key: count / total
        for key, count in counter.items()
    }


def _calculate_distribution_difference(
    baseline_distribution,
    current_distribution,
):
    categories = set(
        baseline_distribution.keys()
    ).union(
        current_distribution.keys()
    )

    difference = 0.0

    for category in categories:
        baseline_value = baseline_distribution.get(
            category,
            0.0,
        )

        current_value = current_distribution.get(
            category,
            0.0,
        )

        difference += abs(
            baseline_value - current_value
        )

    return difference / 2


def _calculate_psi(
    baseline_distribution,
    current_distribution,
):
    categories = set(
        baseline_distribution.keys()
    ).union(
        current_distribution.keys()
    )

    psi = 0.0

    for category in categories:
        baseline_value = baseline_distribution.get(
            category,
            0.0,
        )

        current_value = current_distribution.get(
            category,
            0.0,
        )

        baseline_value = max(
            baseline_value,
            0.0001,
        )

        current_value = max(
            current_value,
            0.0001,
        )

        psi += (
            current_value - baseline_value
        ) * math.log(
            current_value / baseline_value
        )

    return psi


def validate_baseline_drift(
    baseline_file_path,
    current_file_path,
    baseline_dataset_name,
    current_dataset_name,
    schema,
):
    print("=" * 70)
    print("[INFO] VALIDASI BASELINE DRIFT")
    print("=" * 70)

    print(
        f"[DEBUG] Baseline dataset     : "
        f"{baseline_dataset_name}"
    )
    print(
        f"[DEBUG] Baseline file        : "
        f"{baseline_file_path}"
    )
    print(
        f"[DEBUG] Current dataset      : "
        f"{current_dataset_name}"
    )
    print(
        f"[DEBUG] Current file         : "
        f"{current_file_path}"
    )
    print(
        f"[DEBUG] Schema columns       : "
        f"{len(schema)}"
    )

    try:
        baseline_columns, baseline_rows = _read_csv(
            baseline_file_path
        )

    except Exception as error:
        print(
            f"[ERROR] Gagal membaca baseline CSV: "
            f"{error}"
        )

        return {
            "status": "ERROR",
            "message": (
                f"Gagal membaca baseline CSV: "
                f"{error}"
            ),
            "details": [],
        }

    try:
        current_columns, current_rows = _read_csv(
            current_file_path
        )

    except Exception as error:
        print(
            f"[ERROR] Gagal membaca current CSV: "
            f"{error}"
        )

        return {
            "status": "ERROR",
            "message": (
                f"Gagal membaca current CSV: "
                f"{error}"
            ),
            "details": [],
        }

    print(
        f"[DEBUG] Baseline columns     : "
        f"{len(baseline_columns)}"
    )
    print(
        f"[DEBUG] Baseline rows        : "
        f"{len(baseline_rows)}"
    )
    print(
        f"[DEBUG] Current columns      : "
        f"{len(current_columns)}"
    )
    print(
        f"[DEBUG] Current rows         : "
        f"{len(current_rows)}"
    )

    baseline_csv_columns = {
        column.strip().casefold(): column
        for column in baseline_columns
    }

    current_csv_columns = {
        column.strip().casefold(): column
        for column in current_columns
    }

    details = []
    failed = False

    # ==========================================================
    # 1. SCHEMA DRIFT
    # ==========================================================

    print("-" * 70)
    print("[DEBUG] 1. Schema Drift")

    baseline_schema = set(
        baseline_csv_columns.keys()
    )

    current_schema = set(
        current_csv_columns.keys()
    )

    added_columns = sorted(
        current_schema - baseline_schema
    )

    removed_columns = sorted(
        baseline_schema - current_schema
    )

    if added_columns or removed_columns:
        failed = True

        print(
            f"[DEBUG] Added columns       : "
            f"{added_columns}"
        )
        print(
            f"[DEBUG] Removed columns     : "
            f"{removed_columns}"
        )
        print("[RESULT] Schema drift      : FAIL")

        details.append({
            "parameter": "schema_drift",
            "status": "FAIL",
            "message": (
                "Ditemukan perubahan schema "
                "antara baseline dan current dataset."
            ),
            "added_columns": added_columns,
            "removed_columns": removed_columns,
        })

    else:
        print("[RESULT] Schema drift      : PASS")

        details.append({
            "parameter": "schema_drift",
            "status": "PASS",
            "message": (
                "Schema baseline dan current "
                "tidak berubah."
            ),
        })

    # ==========================================================
    # 2. VOLUME DRIFT
    # ==========================================================

    print("-" * 70)
    print("[DEBUG] 2. Volume Drift")

    baseline_rows_count = len(
        baseline_rows
    )

    current_rows_count = len(
        current_rows
    )

    if baseline_rows_count == 0:
        volume_change = None
    else:
        volume_change = (
            current_rows_count
            - baseline_rows_count
        ) / baseline_rows_count

    print(
        f"[DEBUG] Baseline rows       : "
        f"{baseline_rows_count}"
    )
    print(
        f"[DEBUG] Current rows        : "
        f"{current_rows_count}"
    )

    if volume_change is None:
        failed = True

        print(
            "[RESULT] Volume drift       : FAIL"
        )

        details.append({
            "parameter": "volume_drift",
            "status": "FAIL",
            "message": (
                "Baseline dataset tidak memiliki "
                "data rows."
            ),
        })

    else:
        print(
            f"[DEBUG] Volume change       : "
            f"{volume_change:.4f}"
        )

        print(
            "[RESULT] Volume drift       : "
            "PASS"
        )

        details.append({
            "parameter": "volume_drift",
            "status": "PASS",
            "message": (
                "Volume comparison berhasil."
            ),
            "baseline_rows": baseline_rows_count,
            "current_rows": current_rows_count,
            "change_rate": volume_change,
        })

    # ==========================================================
    # 3. COMPLETENESS DRIFT
    # ==========================================================

    print("-" * 70)
    print("[DEBUG] 3. Completeness Drift")

    common_columns = sorted(
        baseline_schema.intersection(
            current_schema
        )
    )

    completeness_details = []

    for column_name in common_columns:
        baseline_column = baseline_csv_columns[
            column_name
        ]

        current_column = current_csv_columns[
            column_name
        ]

        baseline_missing_rate = (
            _calculate_missing_rate(
                baseline_rows,
                baseline_column,
            )
        )

        current_missing_rate = (
            _calculate_missing_rate(
                current_rows,
                current_column,
            )
        )

        difference = (
            current_missing_rate
            - baseline_missing_rate
        )

        print(
            f"[DEBUG] Column              : "
            f"{column_name}"
        )
        print(
            f"[DEBUG] Baseline missing    : "
            f"{baseline_missing_rate:.4f}"
        )
        print(
            f"[DEBUG] Current missing     : "
            f"{current_missing_rate:.4f}"
        )
        print(
            f"[DEBUG] Difference          : "
            f"{difference:.4f}"
        )

        completeness_details.append({
            "column": column_name,
            "baseline_missing_rate": (
                baseline_missing_rate
            ),
            "current_missing_rate": (
                current_missing_rate
            ),
            "difference": difference,
        })

    print(
        "[RESULT] Completeness drift : PASS"
    )

    details.append({
        "parameter": "completeness_drift",
        "status": "PASS",
        "message": (
            "Completeness comparison berhasil."
        ),
        "columns": completeness_details,
    })

    # ==========================================================
    # 4. NUMERIC DISTRIBUTION DRIFT
    # ==========================================================

    print("-" * 70)
    print("[DEBUG] 4. Numeric Distribution Drift")

    numeric_details = []

    for column_name, column_schema in schema.items():

        semantic_type = str(
            column_schema.get(
                "semantic_type",
                "",
            )
        ).casefold()

        dtype = str(
            column_schema.get(
                "dtype",
                "",
            )
        ).casefold()

        if (
            semantic_type
            not in {
                "numeric",
                "continuous",
                "integer",
                "float",
            }
            and dtype
            not in {
                "int",
                "int64",
                "float",
                "float64",
                "int64",
                "float64",
            }
        ):
            continue

        actual_baseline_column = (
            baseline_csv_columns.get(
                column_name.strip().casefold()
            )
        )

        actual_current_column = (
            current_csv_columns.get(
                column_name.strip().casefold()
            )
        )

        if (
            actual_baseline_column is None
            or actual_current_column is None
        ):
            continue

        baseline_values = _get_column_values(
            baseline_rows,
            actual_baseline_column,
        )

        current_values = _get_column_values(
            current_rows,
            actual_current_column,
        )

        baseline_mean = _calculate_mean(
            baseline_values
        )

        current_mean = _calculate_mean(
            current_values
        )

        baseline_std = _calculate_std(
            baseline_values
        )

        current_std = _calculate_std(
            current_values
        )

        print(
            f"[DEBUG] Column              : "
            f"{column_name}"
        )
        print(
            f"[DEBUG] Baseline mean       : "
            f"{baseline_mean}"
        )
        print(
            f"[DEBUG] Current mean        : "
            f"{current_mean}"
        )
        print(
            f"[DEBUG] Baseline std        : "
            f"{baseline_std}"
        )
        print(
            f"[DEBUG] Current std         : "
            f"{current_std}"
        )

        numeric_details.append({
            "column": column_name,
            "baseline_mean": baseline_mean,
            "current_mean": current_mean,
            "baseline_std": baseline_std,
            "current_std": current_std,
        })

    print(
        "[RESULT] Numeric drift      : PASS"
    )

    details.append({
        "parameter": "numeric_distribution_drift",
        "status": "PASS",
        "message": (
            "Numeric distribution comparison "
            "berhasil."
        ),
        "columns": numeric_details,
    })

    # ==========================================================
    # 5. CATEGORICAL DISTRIBUTION DRIFT
    # ==========================================================

    print("-" * 70)
    print("[DEBUG] 5. Categorical Distribution Drift")

    categorical_details = []

    for column_name, column_schema in schema.items():

        semantic_type = str(
            column_schema.get(
                "semantic_type",
                "",
            )
        ).casefold()

        if semantic_type != "categorical":
            continue

        actual_baseline_column = (
            baseline_csv_columns.get(
                column_name.strip().casefold()
            )
        )

        actual_current_column = (
            current_csv_columns.get(
                column_name.strip().casefold()
            )
        )

        if (
            actual_baseline_column is None
            or actual_current_column is None
        ):
            continue

        baseline_values = _get_column_values(
            baseline_rows,
            actual_baseline_column,
        )

        current_values = _get_column_values(
            current_rows,
            actual_current_column,
        )

        baseline_distribution = (
            _calculate_distribution(
                baseline_values
            )
        )

        current_distribution = (
            _calculate_distribution(
                current_values
            )
        )

        distribution_difference = (
            _calculate_distribution_difference(
                baseline_distribution,
                current_distribution,
            )
        )

        psi = _calculate_psi(
            baseline_distribution,
            current_distribution,
        )

        print(
            f"[DEBUG] Column              : "
            f"{column_name}"
        )
        print(
            f"[DEBUG] Distribution diff   : "
            f"{distribution_difference:.4f}"
        )
        print(
            f"[DEBUG] PSI                 : "
            f"{psi:.4f}"
        )

        categorical_details.append({
            "column": column_name,
            "distribution_difference": (
                distribution_difference
            ),
            "psi": psi,
            "baseline_distribution": (
                baseline_distribution
            ),
            "current_distribution": (
                current_distribution
            ),
        })

    print(
        "[RESULT] Categorical drift : PASS"
    )

    details.append({
        "parameter": "categorical_distribution_drift",
        "status": "PASS",
        "message": (
            "Categorical distribution "
            "comparison berhasil."
        ),
        "columns": categorical_details,
    })

    # ==========================================================
    # 6. STRING DRIFT
    # ==========================================================

    print("-" * 70)
    print("[DEBUG] 6. String Drift")

    string_details = []

    for column_name, column_schema in schema.items():

        semantic_type = str(
            column_schema.get(
                "semantic_type",
                "",
            )
        ).casefold()

        dtype = str(
            column_schema.get(
                "dtype",
                "",
            )
        ).casefold()

        if (
            semantic_type not in {
                "text",
                "string",
            }
            and dtype not in {
                "string",
                "str",
            }
        ):
            continue

        actual_baseline_column = (
            baseline_csv_columns.get(
                column_name.strip().casefold()
            )
        )

        actual_current_column = (
            current_csv_columns.get(
                column_name.strip().casefold()
            )
        )

        if (
            actual_baseline_column is None
            or actual_current_column is None
        ):
            continue

        baseline_values = _get_column_values(
            baseline_rows,
            actual_baseline_column,
        )

        current_values = _get_column_values(
            current_rows,
            actual_current_column,
        )

        baseline_lengths = [
            len(str(value).strip())
            for value in baseline_values
        ]

        current_lengths = [
            len(str(value).strip())
            for value in current_values
        ]

        baseline_mean_length = (
            sum(baseline_lengths)
            / len(baseline_lengths)
            if baseline_lengths
            else 0
        )

        current_mean_length = (
            sum(current_lengths)
            / len(current_lengths)
            if current_lengths
            else 0
        )

        print(
            f"[DEBUG] Column              : "
            f"{column_name}"
        )
        print(
            f"[DEBUG] Baseline mean len   : "
            f"{baseline_mean_length:.2f}"
        )
        print(
            f"[DEBUG] Current mean len    : "
            f"{current_mean_length:.2f}"
        )

        string_details.append({
            "column": column_name,
            "baseline_mean_length": (
                baseline_mean_length
            ),
            "current_mean_length": (
                current_mean_length
            ),
        })

    print(
        "[RESULT] String drift      : PASS"
    )

    details.append({
        "parameter": "string_drift",
        "status": "PASS",
        "message": (
            "String distribution comparison "
            "berhasil."
        ),
        "columns": string_details,
    })

    # ==========================================================
    # 7. DUPLICATE DRIFT
    # ==========================================================

    print("-" * 70)
    print("[DEBUG] 7. Duplicate Drift")

    def calculate_duplicate_rate(rows):
        if not rows:
            return 0.0

        row_keys = [
            tuple(
                str(value).strip()
                if value is not None
                else ""
                for value in row.values()
            )
            for row in rows
        ]

        duplicate_count = (
            len(row_keys)
            - len(set(row_keys))
        )

        return (
            duplicate_count
            / len(row_keys)
        )

    baseline_duplicate_rate = (
        calculate_duplicate_rate(
            baseline_rows
        )
    )

    current_duplicate_rate = (
        calculate_duplicate_rate(
            current_rows
        )
    )

    duplicate_difference = (
        current_duplicate_rate
        - baseline_duplicate_rate
    )

    print(
        f"[DEBUG] Baseline duplicate  : "
        f"{baseline_duplicate_rate:.4f}"
    )
    print(
        f"[DEBUG] Current duplicate   : "
        f"{current_duplicate_rate:.4f}"
    )
    print(
        f"[DEBUG] Difference          : "
        f"{duplicate_difference:.4f}"
    )

    print(
        "[RESULT] Duplicate drift    : PASS"
    )

    details.append({
        "parameter": "duplicate_drift",
        "status": "PASS",
        "message": (
            "Duplicate comparison berhasil."
        ),
        "baseline_duplicate_rate": (
            baseline_duplicate_rate
        ),
        "current_duplicate_rate": (
            current_duplicate_rate
        ),
        "difference": duplicate_difference,
    })

    # ==========================================================
    # 8. OUTLIER DRIFT
    # ==========================================================

    print("-" * 70)
    print("[DEBUG] 8. Outlier Drift")

    outlier_details = []

    for column_name, column_schema in schema.items():

        semantic_type = str(
            column_schema.get(
                "semantic_type",
                "",
            )
        ).casefold()

        dtype = str(
            column_schema.get(
                "dtype",
                "",
            )
        ).casefold()

        if (
            semantic_type
            not in {
                "numeric",
                "continuous",
                "integer",
                "float",
            }
            and dtype
            not in {
                "int",
                "int64",
                "float",
                "float64",
            }
        ):
            continue

        actual_baseline_column = (
            baseline_csv_columns.get(
                column_name.strip().casefold()
            )
        )

        actual_current_column = (
            current_csv_columns.get(
                column_name.strip().casefold()
            )
        )

        if (
            actual_baseline_column is None
            or actual_current_column is None
        ):
            continue

        baseline_values = [
            _to_number(value)
            for value in _get_column_values(
                baseline_rows,
                actual_baseline_column,
            )
        ]

        current_values = [
            _to_number(value)
            for value in _get_column_values(
                current_rows,
                actual_current_column,
            )
        ]

        baseline_values = [
            value
            for value in baseline_values
            if value is not None
        ]

        current_values = [
            value
            for value in current_values
            if value is not None
        ]

        def calculate_iqr_outlier_rate(values):
            if len(values) < 4:
                return 0.0

            sorted_values = sorted(values)

            middle = len(sorted_values) // 2

            if len(sorted_values) % 2 == 0:
                lower_half = sorted_values[:middle]
                upper_half = sorted_values[middle:]
            else:
                lower_half = sorted_values[:middle]
                upper_half = sorted_values[
                    middle + 1:
                ]

            q1 = (
                lower_half[len(lower_half) // 2]
                if len(lower_half) % 2 == 1
                else (
                    lower_half[
                        len(lower_half) // 2 - 1
                    ]
                    + lower_half[
                        len(lower_half) // 2
                    ]
                ) / 2
            )

            q3 = (
                upper_half[len(upper_half) // 2]
                if len(upper_half) % 2 == 1
                else (
                    upper_half[
                        len(upper_half) // 2 - 1
                    ]
                    + upper_half[
                        len(upper_half) // 2
                    ]
                ) / 2
            )

            iqr = q3 - q1

            lower_bound = (
                q1 - 1.5 * iqr
            )

            upper_bound = (
                q3 + 1.5 * iqr
            )

            outliers = sum(
                1
                for value in values
                if (
                    value < lower_bound
                    or value > upper_bound
                )
            )

            return outliers / len(values)

        baseline_outlier_rate = (
            calculate_iqr_outlier_rate(
                baseline_values
            )
        )

        current_outlier_rate = (
            calculate_iqr_outlier_rate(
                current_values
            )
        )

        print(
            f"[DEBUG] Column              : "
            f"{column_name}"
        )
        print(
            f"[DEBUG] Baseline outlier    : "
            f"{baseline_outlier_rate:.4f}"
        )
        print(
            f"[DEBUG] Current outlier     : "
            f"{current_outlier_rate:.4f}"
        )

        outlier_details.append({
            "column": column_name,
            "baseline_outlier_rate": (
                baseline_outlier_rate
            ),
            "current_outlier_rate": (
                current_outlier_rate
            ),
        })

    print(
        "[RESULT] Outlier drift     : PASS"
    )

    details.append({
        "parameter": "outlier_drift",
        "status": "PASS",
        "message": (
            "Outlier comparison berhasil."
        ),
        "columns": outlier_details,
    })

    # ==========================================================
    # FINAL RESULT
    # ==========================================================

    status = "FAIL" if failed else "PASS"

    print("=" * 70)
    print("[RESULT] BASELINE DRIFT VALIDATION")
    print("=" * 70)
    print(
        f"[RESULT] Baseline dataset   : "
        f"{baseline_dataset_name}"
    )
    print(
        f"[RESULT] Current dataset    : "
        f"{current_dataset_name}"
    )
    print(
        f"[RESULT] Status             : "
        f"{status}"
    )

    return {
        "status": status,
        "message": (
            "Baseline drift validation berhasil."
            if status == "PASS"
            else "Baseline drift validation gagal."
        ),
        "details": details,
    }