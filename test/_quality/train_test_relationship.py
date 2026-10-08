import csv
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


def _get_actual_column(
    columns,
    column_name,
):
    column_map = {
        column.strip().casefold(): column
        for column in columns
    }

    return column_map.get(
        column_name.strip().casefold()
    )


def _get_primary_key_columns(schema):
    return [
        column_name
        for column_name, column_schema in schema.items()
        if column_schema.get("semantic_type")
        == "primary_key"
    ]


def _get_target_columns(schema):
    return [
        column_name
        for column_name, column_schema in schema.items()
        if column_schema.get("semantic_type")
        in {
            "binary_target",
            "target",
        }
    ]


def _get_categorical_columns(schema):
    return [
        column_name
        for column_name, column_schema in schema.items()
        if column_schema.get("semantic_type")
        == "categorical"
    ]


def _get_datetime_columns(schema):
    datetime_columns = []

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

        expected_format = str(
            column_schema.get(
                "format",
                "",
            )
        ).casefold()

        if (
            semantic_type
            in {
                "date",
                "datetime",
                "timestamp",
            }
            or dtype
            in {
                "date",
                "datetime",
                "timestamp",
            }
            or expected_format
            in {
                "date",
                "datetime",
            }
        ):
            datetime_columns.append(
                column_name
            )

    return datetime_columns


def _get_feature_columns(
    schema,
    target_columns,
):
    return [
        column_name
        for column_name in schema.keys()
        if column_name not in target_columns
    ]


def _build_row_key(
    row,
    actual_columns,
):
    values = []

    for column in actual_columns:
        value = row.get(column)

        if _is_null(value):
            values.append("")
        else:
            values.append(
                str(value).strip().casefold()
            )

    return tuple(values)


def validate_train_test_relationship(
    train_file_path,
    test_file_path,
    train_dataset_name,
    test_dataset_name,
    schema,
):
    print("=" * 70)
    print("[INFO] VALIDASI TRAIN TEST RELATIONSHIP")
    print("=" * 70)

    print(
        f"[DEBUG] Train dataset        : "
        f"{train_dataset_name}"
    )
    print(
        f"[DEBUG] Train file           : "
        f"{train_file_path}"
    )
    print(
        f"[DEBUG] Test dataset         : "
        f"{test_dataset_name}"
    )
    print(
        f"[DEBUG] Test file            : "
        f"{test_file_path}"
    )
    print(
        f"[DEBUG] Schema columns       : "
        f"{len(schema)}"
    )

    # ==========================================================
    # READ TRAIN CSV
    # ==========================================================

    try:
        train_columns, train_rows = _read_csv(
            train_file_path
        )

    except Exception as error:
        print(
            f"[ERROR] Gagal membaca train CSV: "
            f"{error}"
        )

        return {
            "status": "ERROR",
            "message": (
                f"Gagal membaca train CSV: "
                f"{error}"
            ),
            "details": [],
        }

    # ==========================================================
    # READ TEST CSV
    # ==========================================================

    try:
        test_columns, test_rows = _read_csv(
            test_file_path
        )

    except Exception as error:
        print(
            f"[ERROR] Gagal membaca test CSV: "
            f"{error}"
        )

        return {
            "status": "ERROR",
            "message": (
                f"Gagal membaca test CSV: "
                f"{error}"
            ),
            "details": [],
        }

    print(
        f"[DEBUG] Train columns       : "
        f"{len(train_columns)}"
    )
    print(
        f"[DEBUG] Train rows           : "
        f"{len(train_rows)}"
    )
    print(
        f"[DEBUG] Test columns        : "
        f"{len(test_columns)}"
    )
    print(
        f"[DEBUG] Test rows            : "
        f"{len(test_rows)}"
    )

    train_csv_columns = {
        column.strip().casefold(): column
        for column in train_columns
    }

    test_csv_columns = {
        column.strip().casefold(): column
        for column in test_columns
    }

    details = []
    failed = False

    # ==========================================================
    # 1. PRIMARY KEY RELATIONSHIP
    # ==========================================================

    print("-" * 70)
    print("[DEBUG] 1. Primary Key Relationship")

    primary_key_columns = _get_primary_key_columns(
        schema
    )

    print(
        f"[DEBUG] Primary key columns : "
        f"{primary_key_columns}"
    )

    if not primary_key_columns:

        print(
            "[DEBUG] Primary key tidak "
            "didefinisikan."
        )

        print(
            "[RESULT] PK relationship   : PASS"
        )

        details.append({
            "parameter": "primary_key_relationship",
            "status": "PASS",
            "message": (
                "Primary key tidak didefinisikan."
            ),
        })

    else:

        train_pk_columns = []
        test_pk_columns = []

        pk_failed = False

        for column_name in primary_key_columns:

            train_column = (
                train_csv_columns.get(
                    column_name.strip().casefold()
                )
            )

            test_column = (
                test_csv_columns.get(
                    column_name.strip().casefold()
                )
            )

            print(
                f"[DEBUG] PK column           : "
                f"{column_name}"
            )

            if train_column is None:
                print(
                    "[DEBUG] Train column       : "
                    "NOT FOUND"
                )

                pk_failed = True

            else:
                print(
                    f"[DEBUG] Train column       : "
                    f"{train_column}"
                )

                train_pk_columns.append(
                    train_column
                )

            if test_column is None:
                print(
                    "[DEBUG] Test column        : "
                    "NOT FOUND"
                )

                pk_failed = True

            else:
                print(
                    f"[DEBUG] Test column        : "
                    f"{test_column}"
                )

                test_pk_columns.append(
                    test_column
                )

        if pk_failed:

            failed = True

            print(
                "[RESULT] PK relationship   : FAIL"
            )

            details.append({
                "parameter": (
                    "primary_key_relationship"
                ),
                "status": "FAIL",
                "message": (
                    "Primary key tidak tersedia "
                    "di train atau test."
                ),
            })

        else:

            train_keys = {
                _build_row_key(
                    row,
                    train_pk_columns,
                )
                for row in train_rows
                if not any(
                    _is_null(row.get(column))
                    for column in train_pk_columns
                )
            }

            test_keys = {
                _build_row_key(
                    row,
                    test_pk_columns,
                )
                for row in test_rows
                if not any(
                    _is_null(row.get(column))
                    for column in test_pk_columns
                )
            }

            overlapping_keys = (
                train_keys.intersection(
                    test_keys
                )
            )

            print(
                f"[DEBUG] Train PK keys       : "
                f"{len(train_keys)}"
            )
            print(
                f"[DEBUG] Test PK keys        : "
                f"{len(test_keys)}"
            )
            print(
                f"[DEBUG] Overlapping PK      : "
                f"{len(overlapping_keys)}"
            )

            if overlapping_keys:

                failed = True

                print(
                    "[RESULT] PK relationship   : FAIL"
                )

                details.append({
                    "parameter": (
                        "primary_key_relationship"
                    ),
                    "status": "FAIL",
                    "message": (
                        "Ditemukan primary key "
                        "yang terdapat di train "
                        "dan test."
                    ),
                    "overlap_count": (
                        len(overlapping_keys)
                    ),
                    "sample_overlap": list(
                        overlapping_keys
                    )[:20],
                })

            else:

                print(
                    "[RESULT] PK relationship   : PASS"
                )

                details.append({
                    "parameter": (
                        "primary_key_relationship"
                    ),
                    "status": "PASS",
                    "message": (
                        "Tidak ada primary key "
                        "yang overlap antara "
                        "train dan test."
                    ),
                })

    # ==========================================================
    # 2. RECORD RELATIONSHIP
    # ==========================================================

    print("-" * 70)
    print("[DEBUG] 2. Record Relationship")

    common_columns = sorted(
        train_csv_columns.keys()
        .intersection(
            test_csv_columns.keys()
        )
    )

    target_columns = _get_target_columns(
        schema
    )

    target_column_keys = {
        column.strip().casefold()
        for column in target_columns
    }

    feature_columns = [
        column
        for column in common_columns
        if column not in target_column_keys
    ]

    train_feature_columns = [
        train_csv_columns[column]
        for column in feature_columns
    ]

    test_feature_columns = [
        test_csv_columns[column]
        for column in feature_columns
    ]

    print(
        f"[DEBUG] Feature columns     : "
        f"{len(feature_columns)}"
    )

    train_record_keys = {
        _build_row_key(
            row,
            train_feature_columns,
        )
        for row in train_rows
    }

    test_record_keys = {
        _build_row_key(
            row,
            test_feature_columns,
        )
        for row in test_rows
    }

    overlapping_records = (
        train_record_keys.intersection(
            test_record_keys
        )
    )

    print(
        f"[DEBUG] Train records       : "
        f"{len(train_record_keys)}"
    )
    print(
        f"[DEBUG] Test records        : "
        f"{len(test_record_keys)}"
    )
    print(
        f"[DEBUG] Overlapping records : "
        f"{len(overlapping_records)}"
    )

    if overlapping_records:

        failed = True

        print(
            "[RESULT] Record relationship: FAIL"
        )

        details.append({
            "parameter": "record_relationship",
            "status": "FAIL",
            "message": (
                "Ditemukan record yang sama "
                "antara train dan test."
            ),
            "overlap_count": (
                len(overlapping_records)
            ),
            "sample_overlap": list(
                overlapping_records
            )[:20],
        })

    else:

        print(
            "[RESULT] Record relationship: PASS"
        )

        details.append({
            "parameter": "record_relationship",
            "status": "PASS",
            "message": (
                "Tidak ada record feature "
                "yang overlap antara train "
                "dan test."
            ),
        })

    # ==========================================================
    # 3. SCHEMA RELATIONSHIP
    # ==========================================================

    print("-" * 70)
    print("[DEBUG] 3. Schema Relationship")

    train_schema = set(
        train_csv_columns.keys()
    )

    test_schema = set(
        test_csv_columns.keys()
    )

    train_only_columns = sorted(
        train_schema - test_schema
    )

    test_only_columns = sorted(
        test_schema - train_schema
    )

    print(
        f"[DEBUG] Train only columns   : "
        f"{train_only_columns}"
    )
    print(
        f"[DEBUG] Test only columns    : "
        f"{test_only_columns}"
    )

    print(
        "[RESULT] Schema relationship: "
        "INFO"
    )

    details.append({
        "parameter": "schema_relationship",
        "status": "INFO",
        "message": (
            "Schema train dan test "
            "dibandingkan."
        ),
        "train_only_columns": (
            train_only_columns
        ),
        "test_only_columns": (
            test_only_columns
        ),
    })

    # ==========================================================
    # 4. FEATURE RELATIONSHIP
    # ==========================================================

    print("-" * 70)
    print("[DEBUG] 4. Feature Relationship")

    feature_failed = False
    feature_details = []

    for column_name in schema.keys():

        normalized_column = (
            column_name.strip().casefold()
        )

        if normalized_column in target_column_keys:
            continue

        train_column = train_csv_columns.get(
            normalized_column
        )

        test_column = test_csv_columns.get(
            normalized_column
        )

        if train_column is None:
            feature_failed = True

            print(
                f"[DEBUG] Feature            : "
                f"{column_name}"
            )
            print(
                "[DEBUG] Train              : "
                "NOT FOUND"
            )

            feature_details.append({
                "column": column_name,
                "status": "FAIL",
                "message": (
                    "Feature tidak ditemukan "
                    "di train."
                ),
            })

        elif test_column is None:
            feature_failed = True

            print(
                f"[DEBUG] Feature            : "
                f"{column_name}"
            )
            print(
                "[DEBUG] Test               : "
                "NOT FOUND"
            )

            feature_details.append({
                "column": column_name,
                "status": "FAIL",
                "message": (
                    "Feature tidak ditemukan "
                    "di test."
                ),
            })

        else:
            feature_details.append({
                "column": column_name,
                "status": "PASS",
                "message": (
                    "Feature tersedia "
                    "di train dan test."
                ),
            })

    if feature_failed:

        failed = True

        print(
            "[RESULT] Feature relationship: FAIL"
        )

    else:

        print(
            "[RESULT] Feature relationship: PASS"
        )

    details.append({
        "parameter": "feature_relationship",
        "status": (
            "FAIL"
            if feature_failed
            else "PASS"
        ),
        "message": (
            "Feature train dan test "
            "tidak sesuai."
            if feature_failed
            else
            "Feature train dan test "
            "sesuai."
        ),
        "columns": feature_details,
    })

    # ==========================================================
    # 5. CATEGORY RELATIONSHIP
    # ==========================================================

    print("-" * 70)
    print("[DEBUG] 5. Category Relationship")

    category_failed = False
    category_details = []

    categorical_columns = (
        _get_categorical_columns(schema)
    )

    for column_name in categorical_columns:

        normalized_column = (
            column_name.strip().casefold()
        )

        train_column = (
            train_csv_columns.get(
                normalized_column
            )
        )

        test_column = (
            test_csv_columns.get(
                normalized_column
            )
        )

        if (
            train_column is None
            or test_column is None
        ):
            continue

        train_categories = {
            str(row.get(train_column))
            .strip()
            .casefold()
            for row in train_rows
            if not _is_null(
                row.get(train_column)
            )
        }

        test_categories = {
            str(row.get(test_column))
            .strip()
            .casefold()
            for row in test_rows
            if not _is_null(
                row.get(test_column)
            )
        }

        unseen_test_categories = sorted(
            test_categories
            - train_categories
        )

        print(
            f"[DEBUG] Column              : "
            f"{column_name}"
        )
        print(
            f"[DEBUG] Train categories    : "
            f"{len(train_categories)}"
        )
        print(
            f"[DEBUG] Test categories     : "
            f"{len(test_categories)}"
        )
        print(
            f"[DEBUG] Unseen test values  : "
            f"{unseen_test_categories}"
        )

        if unseen_test_categories:

            category_failed = True

        category_details.append({
            "column": column_name,
            "status": (
                "FAIL"
                if unseen_test_categories
                else "PASS"
            ),
            "train_categories": sorted(
                train_categories
            ),
            "test_categories": sorted(
                test_categories
            ),
            "unseen_test_categories": (
                unseen_test_categories
            ),
        })

    if category_failed:

        failed = True

        print(
            "[RESULT] Category relationship: FAIL"
        )

    else:

        print(
            "[RESULT] Category relationship: PASS"
        )

    details.append({
        "parameter": "category_relationship",
        "status": (
            "FAIL"
            if category_failed
            else "PASS"
        ),
        "message": (
            "Test memiliki kategori "
            "yang tidak ditemukan di train."
            if category_failed
            else
            "Tidak ada kategori baru "
            "di test."
        ),
        "columns": category_details,
    })

    # ==========================================================
    # 6. DISTRIBUTION RELATIONSHIP
    # ==========================================================

    print("-" * 70)
    print("[DEBUG] 6. Distribution Relationship")

    distribution_details = []

    for column_name in schema.keys():

        normalized_column = (
            column_name.strip().casefold()
        )

        train_column = (
            train_csv_columns.get(
                normalized_column
            )
        )

        test_column = (
            test_csv_columns.get(
                normalized_column
            )
        )

        if (
            train_column is None
            or test_column is None
        ):
            continue

        train_values = [
            str(row.get(train_column))
            .strip()
            .casefold()
            for row in train_rows
            if not _is_null(
                row.get(train_column)
            )
        ]

        test_values = [
            str(row.get(test_column))
            .strip()
            .casefold()
            for row in test_rows
            if not _is_null(
                row.get(test_column)
            )
        ]

        train_distribution = Counter(
            train_values
        )

        test_distribution = Counter(
            test_values
        )

        train_total = len(train_values)
        test_total = len(test_values)

        categories = set(
            train_distribution.keys()
        ).union(
            test_distribution.keys()
        )

        distribution_difference = 0.0

        for category in categories:

            train_rate = (
                train_distribution.get(
                    category,
                    0,
                )
                / train_total
                if train_total
                else 0
            )

            test_rate = (
                test_distribution.get(
                    category,
                    0,
                )
                / test_total
                if test_total
                else 0
            )

            distribution_difference += abs(
                train_rate - test_rate
            )

        distribution_difference /= 2

        print(
            f"[DEBUG] Column              : "
            f"{column_name}"
        )
        print(
            f"[DEBUG] Distribution diff   : "
            f"{distribution_difference:.4f}"
        )

        distribution_details.append({
            "column": column_name,
            "distribution_difference": (
                distribution_difference
            ),
        })

    print(
        "[RESULT] Distribution relationship: INFO"
    )

    details.append({
        "parameter": "distribution_relationship",
        "status": "INFO",
        "message": (
            "Distribusi train dan test "
            "dibandingkan."
        ),
        "columns": distribution_details,
    })

    # ==========================================================
    # 7. TARGET RELATIONSHIP
    # ==========================================================

    print("-" * 70)
    print("[DEBUG] 7. Target Relationship")

    target_details = []

    for column_name in target_columns:

        normalized_column = (
            column_name.strip().casefold()
        )

        train_column = (
            train_csv_columns.get(
                normalized_column
            )
        )

        test_column = (
            test_csv_columns.get(
                normalized_column
            )
        )

        print(
            f"[DEBUG] Target column      : "
            f"{column_name}"
        )

        if train_column is None:

            failed = True

            print(
                "[DEBUG] Train              : "
                "NOT FOUND"
            )

            target_details.append({
                "column": column_name,
                "status": "FAIL",
                "message": (
                    "Target tidak ditemukan "
                    "di train."
                ),
            })

        elif test_column is not None:

            print(
                f"[DEBUG] Train              : "
                f"{train_column}"
            )
            print(
                f"[DEBUG] Test               : "
                f"{test_column}"
            )

            target_details.append({
                "column": column_name,
                "status": "INFO",
                "message": (
                    "Target tersedia di "
                    "train dan test."
                ),
            })

        else:

            print(
                f"[DEBUG] Train              : "
                f"{train_column}"
            )
            print(
                "[DEBUG] Test               : "
                "NOT FOUND"
            )

            target_details.append({
                "column": column_name,
                "status": "PASS",
                "message": (
                    "Target tersedia di train "
                    "dan tidak tersedia di test."
                ),
            })

    print(
        "[RESULT] Target relationship : "
        "PASS"
    )

    details.append({
        "parameter": "target_relationship",
        "status": "PASS",
        "message": (
            "Target relationship "
            "berhasil diperiksa."
        ),
        "columns": target_details,
    })

    # ==========================================================
    # 8. TEMPORAL RELATIONSHIP
    # ==========================================================

    print("-" * 70)
    print("[DEBUG] 8. Temporal Relationship")

    datetime_columns = _get_datetime_columns(
        schema
    )

    temporal_details = []

    for column_name in datetime_columns:

        normalized_column = (
            column_name.strip().casefold()
        )

        train_column = (
            train_csv_columns.get(
                normalized_column
            )
        )

        test_column = (
            test_csv_columns.get(
                normalized_column
            )
        )

        if (
            train_column is None
            or test_column is None
        ):
            continue

        train_values = [
            str(row.get(train_column)).strip()
            for row in train_rows
            if not _is_null(
                row.get(train_column)
            )
        ]

        test_values = [
            str(row.get(test_column)).strip()
            for row in test_rows
            if not _is_null(
                row.get(test_column)
            )
        ]

        train_min = (
            min(train_values)
            if train_values
            else None
        )

        train_max = (
            max(train_values)
            if train_values
            else None
        )

        test_min = (
            min(test_values)
            if test_values
            else None
        )

        test_max = (
            max(test_values)
            if test_values
            else None
        )

        print(
            f"[DEBUG] Column              : "
            f"{column_name}"
        )
        print(
            f"[DEBUG] Train min           : "
            f"{train_min}"
        )
        print(
            f"[DEBUG] Train max           : "
            f"{train_max}"
        )
        print(
            f"[DEBUG] Test min            : "
            f"{test_min}"
        )
        print(
            f"[DEBUG] Test max            : "
            f"{test_max}"
        )

        temporal_details.append({
            "column": column_name,
            "train_min": train_min,
            "train_max": train_max,
            "test_min": test_min,
            "test_max": test_max,
        })

    if datetime_columns:

        print(
            "[RESULT] Temporal relationship: INFO"
        )

    else:

        print(
            "[DEBUG] Tidak ada kolom temporal."
        )
        print(
            "[RESULT] Temporal relationship: PASS"
        )

    details.append({
        "parameter": "temporal_relationship",
        "status": "INFO",
        "message": (
            "Temporal relationship "
            "dibandingkan."
            if datetime_columns
            else
            "Tidak ada kolom temporal "
            "dalam schema."
        ),
        "columns": temporal_details,
    })

    # ==========================================================
    # 9. GROUP RELATIONSHIP
    # ==========================================================

    print("-" * 70)
    print("[DEBUG] 9. Group Relationship")

    group_columns = [
        column_name
        for column_name, column_schema in schema.items()
        if column_schema.get("semantic_type")
        in {
            "group",
            "group_key",
        }
    ]

    group_details = []

    if not group_columns:

        print(
            "[DEBUG] Group key tidak "
            "didefinisikan."
        )

        print(
            "[RESULT] Group relationship: PASS"
        )

        details.append({
            "parameter": "group_relationship",
            "status": "PASS",
            "message": (
                "Group key tidak didefinisikan."
            ),
        })

    else:

        group_failed = False

        for column_name in group_columns:

            normalized_column = (
                column_name.strip().casefold()
            )

            train_column = (
                train_csv_columns.get(
                    normalized_column
                )
            )

            test_column = (
                test_csv_columns.get(
                    normalized_column
                )
            )

            if (
                train_column is None
                or test_column is None
            ):
                group_failed = True

                group_details.append({
                    "column": column_name,
                    "status": "FAIL",
                    "message": (
                        "Group key tidak "
                        "ditemukan di train "
                        "atau test."
                    ),
                })

                continue

            train_groups = {
                str(row.get(train_column))
                .strip()
                .casefold()
                for row in train_rows
                if not _is_null(
                    row.get(train_column)
                )
            }

            test_groups = {
                str(row.get(test_column))
                .strip()
                .casefold()
                for row in test_rows
                if not _is_null(
                    row.get(test_column)
                )
            }

            overlapping_groups = (
                train_groups.intersection(
                    test_groups
                )
            )

            print(
                f"[DEBUG] Group column       : "
                f"{column_name}"
            )
            print(
                f"[DEBUG] Train groups       : "
                f"{len(train_groups)}"
            )
            print(
                f"[DEBUG] Test groups        : "
                f"{len(test_groups)}"
            )
            print(
                f"[DEBUG] Overlap groups     : "
                f"{len(overlapping_groups)}"
            )

            if overlapping_groups:

                group_failed = True

                print(
                    "[RESULT] Group relationship: FAIL"
                )

                group_details.append({
                    "column": column_name,
                    "status": "FAIL",
                    "message": (
                        "Ditemukan group yang "
                        "overlap antara train "
                        "dan test."
                    ),
                    "overlap_count": (
                        len(overlapping_groups)
                    ),
                    "sample_overlap": list(
                        overlapping_groups
                    )[:20],
                })

            else:

                print(
                    "[RESULT] Group relationship: PASS"
                )

                group_details.append({
                    "column": column_name,
                    "status": "PASS",
                    "message": (
                        "Tidak ada group overlap "
                        "antara train dan test."
                    ),
                })

        if group_failed:
            failed = True

        details.append({
            "parameter": "group_relationship",
            "status": (
                "FAIL"
                if group_failed
                else "PASS"
            ),
            "message": (
                "Ditemukan group overlap."
                if group_failed
                else
                "Tidak ada group overlap."
            ),
            "columns": group_details,
        })

    # ==========================================================
    # FINAL RESULT
    # ==========================================================

    status = "FAIL" if failed else "PASS"

    print("=" * 70)
    print("[RESULT] TRAIN TEST RELATIONSHIP")
    print("=" * 70)
    print(
        f"[RESULT] Train dataset      : "
        f"{train_dataset_name}"
    )
    print(
        f"[RESULT] Test dataset       : "
        f"{test_dataset_name}"
    )
    print(
        f"[RESULT] Status             : "
        f"{status}"
    )

    return {
        "status": status,
        "message": (
            "Train test relationship "
            "validation berhasil."
            if status == "PASS"
            else
            "Train test relationship "
            "validation gagal."
        ),
        "details": details,
    }