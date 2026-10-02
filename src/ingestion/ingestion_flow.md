# Garis besar

```bash
                    INGESTION
                       │
          ┌────────────┴────────────┐
          │                         │
   TECHNICAL VALIDATION        DATA VALIDATION
          │                         │
   Source                       Schema
   Fingerprint                  Constraint
   Format                       Data Quality
   Structure
```

---

# framework ingestion/validation yang reusable

```bash
ingestion/
│
├── 1. source/
│   │
│   ├── existence/
│   │   ├── path_exists
│   │   ├── file_exists
│   │   └── target_exists
│   │
│   ├── accessibility/
│   │   ├── readable
│   │   ├── writable
│   │   ├── executable
│   │   └── permission
│   │
│   ├── file_type/
│   │   ├── is_file
│   │   ├── is_directory
│   │   ├── is_symlink
│   │   ├── extension
│   │   └── mime_type
│   │
│   ├── metadata/
│   │   ├── file_name
│   │   ├── file_path
│   │   ├── size_bytes
│   │   ├── created_at
│   │   ├── modified_at
│   │   └── accessed_at
│   │
│   └── integrity/
│       ├── non_empty
│       ├── readable_content
│       ├── openable
│       ├── truncated
│       └── corrupted
│
├── 2. fingerprint/
│   │
│   ├── file_hash/
│   │   ├── algorithm
│   │   ├── hash
│   │   └── hash_match
│   │
│   ├── content_hash/
│   │   ├── algorithm
│   │   ├── normalized
│   │   ├── hash
│   │   └── hash_match
│   │
│   ├── schema_hash/
│   │   ├── algorithm
│   │   ├── schema_definition
│   │   ├── hash
│   │   └── hash_match
│   │
│   └── dataset_identity/
│       ├── dataset_name
│       ├── source_name
│       ├── source_version
│       ├── file_hash
│       ├── schema_hash
│       └── identity
│
├── 3. format/
│   │
│   ├── encoding/
│   │   ├── expected
│   │   ├── detected
│   │   ├── confidence
│   │   └── bom
│   │
│   ├── delimiter/
│   │   ├── expected
│   │   ├── detected
│   │   ├── consistent
│   │   └── field_count
│   │
│   ├── quoting/
│   │   ├── quote_char
│   │   ├── quoting_mode
│   │   ├── double_quote
│   │   └── quote_consistent
│   │
│   ├── escaping/
│   │   ├── escape_char
│   │   ├── escape_enabled
│   │   └── escape_consistent
│   │
│   └── parser/
│       ├── parser_type
│       ├── parse_success
│       ├── parse_errors
│       ├── malformed_records
│       └── parser_warnings
│
├── 4. structure/
│   │
│   ├── header/
│   │   ├── has_header
│   │   ├── header_valid
│   │   ├── header_unique
│   │   └── header_count
│   │
│   ├── columns/
│   │   ├── expected_count
│   │   ├── actual_count
│   │   ├── expected_names
│   │   ├── actual_names
│   │   ├── missing_columns
│   │   ├── unexpected_columns
│   │   ├── duplicate_columns
│   │   └── column_order
│   │
│   ├── rows/
│   │   ├── expected_rows
│   │   ├── actual_rows
│   │   ├── row_count
│   │   ├── min_rows
│   │   └── max_rows
│   │
│   ├── empty_rows/
│   │   ├── empty_row_count
│   │   ├── empty_row_ratio
│   │   └── max_allowed_empty_rows
│   │
│   └── malformed_rows/
│       ├── malformed_count
│       ├── malformed_ratio
│       ├── inconsistent_count
│       └── max_allowed_malformed
│
├── 5. schema/
│   │
│   ├── existence/
│   │   ├── required_columns
│   │   ├── missing_columns
│   │   ├── unexpected_columns
│   │   └── column_presence
│   │
│   ├── dtype/
│   │   ├── expected_dtype
│   │   ├── actual_dtype
│   │   ├── dtype_match
│   │   └── conversion_allowed
│   │
│   ├── nullable/
│   │   ├── nullable
│   │   ├── null_count
│   │   ├── null_ratio
│   │   └── null_allowed
│   │
│   ├── required/
│   │   ├── required
│   │   ├── present
│   │   └── requirement_satisfied
│   │
│   ├── semantic_type/
│   │   ├── semantic_type
│   │   ├── detected_type
│   │   └── semantic_match
│   │
│   └── allowed_values/
│       ├── allowed_values
│       ├── actual_values
│       ├── invalid_values
│       ├── invalid_count
│       └── invalid_ratio
│
├── 6. constraint/
│   │
│   ├── primary_key/
│   │   ├── columns
│   │   ├── nullable
│   │   ├── unique
│   │   ├── duplicate_count
│   │   └── violation_count
│   │
│   ├── unique/
│   │   ├── columns
│   │   ├── unique_required
│   │   ├── unique_count
│   │   ├── duplicate_count
│   │   └── duplicate_ratio
│   │
│   ├── not_null/
│   │   ├── columns
│   │   ├── required
│   │   ├── null_count
│   │   ├── null_ratio
│   │   └── violation_count
│   │
│   ├── range/
│   │   ├── column
│   │   ├── min
│   │   ├── max
│   │   ├── inclusive
│   │   ├── actual_min
│   │   ├── actual_max
│   │   └── violation_count
│   │
│   ├── relationship/
│   │   ├── source_column
│   │   ├── reference_dataset
│   │   ├── reference_column
│   │   ├── relationship_type
│   │   ├── orphan_count
│   │   └── violation_count
│   │
│   └── business_rule/
│       ├── rule_id
│       ├── rule_name
│       ├── expression
│       ├── severity
│       ├── violation_count
│       └── violation_ratio
│
└── 7. quality/
   │
   ├── completeness/
   │   ├── null_count
   │   ├── null_ratio
   │   ├── missing_count
   │   ├── missing_ratio
   │   ├── empty_string_count
   │   └── threshold
   │
   ├── validity/
   │   ├── valid_count
   │   ├── invalid_count
   │   ├── valid_ratio
   │   ├── invalid_ratio
   │   ├── format_valid
   │   ├── range_valid
   │   └── threshold
   │
   ├── uniqueness/
   │   ├── total_count
   │   ├── unique_count
   │   ├── duplicate_count
   │   ├── unique_ratio
   │   └── duplicate_ratio
   │
   ├── consistency/
   │   ├── rule_id
   │   ├── comparison_type
   │   ├── consistent_count
   │   ├── inconsistent_count
   │   ├── consistency_ratio
   │   └── threshold
   │
   ├── accuracy/
   │   ├── reference_source
   │   ├── reference_column
   │   ├── matched_count
   │   ├── mismatched_count
   │   └── accuracy_ratio
   │
   ├── timeliness/
   │   ├── timestamp_column
   │   ├── ingestion_time
   │   ├── data_time
   │   ├── data_age
   │   ├── freshness_threshold
   │   └── freshness_status
   │
   └── distribution/
       ├── count
       ├── mean
       ├── median
       ├── std
       ├── min
       ├── max
       ├── percentile
       ├── outlier_count
       ├── outlier_ratio
       └── distribution_drift
```