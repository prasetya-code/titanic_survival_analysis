```py
MISSING_VALUES = ["", "NA", "N/A", "na", "n/a", "N/a"]
```

```bash
DQ-005
Data Quality Validation
│
├── Completeness
│   ├── Missing Value Profiling
│   └── Missingness Threshold
│
├── Uniqueness
│   ├── Primary Key
│   ├── Full-Row Duplicate
│   └── Business-Key Duplicate
│
├── Validity
│   ├── String Quality
│   ├── Name Format
│   ├── Numeric Domain
│   └── Categorical Domain
│
├── Integrity
│   └── Row Count / Baseline Drift
│
└── Consistency
    └── Train / Test Relationship


DQ-006
Staged Artifact Validation
│
├── Parquet Read-back
├── Schema Match
└── Artifact Integrity


DQ-007
Provenance & Audit Validation
│
├── Run Metadata
├── Git Commit
├── Environment
└── Validation Report
```




- `validasi nullability`
```bash
[DEBUG] Column              : age
[DEBUG] Nullable            : True
[DEBUG] Max null ratio      : 0.3
[DEBUG] Null count          : 177
[DEBUG] Null ratio          : 0.1987
[RESULT] Status             : PASS

untuk null ratio nya buatkan dua angka dibelakang koma saja
```

- `validasi format` tidak ada di schema BP, maka penerapan di schema berikut seperti apa:
```py
--- ISI TRAIN SCHEMA ---
{
  "passengerid": {
    "dtype": "Int64",
    "semantic_type": "primary_key",
    "nullable": false,
    "required": true
  },
  "survived": {
    "dtype": "Int64",
    "semantic_type": "binary_target",
    "allowed_values": [
      0,
      1
    ],
    "nullable": false,
    "required": true
  },
  "pclass": {
    "dtype": "Int64",
    "semantic_type": "categorical",
    "allowed_values": [
      1,
      2,
      3
    ],
    "nullable": false,
    "required": true
  },
  "name": {
    "dtype": "String",
    "semantic_type": "text",
    "nullable": false,
    "required": true
  },
  "sex": {
    "dtype": "String",
    "semantic_type": "categorical",
    "allowed_values": [
      "male",
      "female"
    ],
    "nullable": false,
    "required": true
  },
  "age": {
    "dtype": "Float64",
    "semantic_type": "numeric",
    "min": 0,
    "max": 100,
    "max_null_ratio": 0.3,
    "nullable": true,
    "required": false
  },
  "sibsp": {
    "dtype": "Int64",
    "semantic_type": "count",
    "min": 0,
    "nullable": false,
    "required": true
  },
  "parch": {
    "dtype": "Int64",
    "semantic_type": "count",
    "min": 0,
    "nullable": false,
    "required": true
  },
  "ticket": {
    "dtype": "String",
    "semantic_type": "identifier",
    "nullable": false,
    "required": true
  },
  "fare": {
    "dtype": "Float64",
    "semantic_type": "numeric",
    "min": 0,
    "max_null_ratio": 0.05,
    "nullable": true,
    "required": false
  },
  "cabin": {
    "dtype": "String",
    "semantic_type": "categorical_text",
    "max_null_ratio": 0.9,
    "nullable": true,
    "required": false
  },
  "embarked": {
    "dtype": "String",
    "semantic_type": "categorical",
    "allowed_values": [
      "C",
      "Q",
      "S"
    ],
    "max_null_ratio": 0.05,
    "nullable": true,
    "required": false
  }
}


# untuk format sebaiknya menggunakan key semantic_type atau buat key baru dengan nama format
```

- `validasi constraint` masih belum paham apa yang di constraint, misal saya mempunyai data berikut:
```py
[DEBUG] Column              : age
[DEBUG] Min                 : 0
[DEBUG] Max                 : 100
[DEBUG] Invalid values      : 0
[DEBUG] Skipped null        : 177
[RESULT] Status             : PASS

# pada [DEBUG] Skipped null sebaiknya dihapus

```

- pada `validasi allowed` value untuk apa step skipped null, berikut contoh datanya:
```py
[DEBUG] Column              : embarked
[DEBUG] Allowed values      : ['C', 'Q', 'S']
[DEBUG] Invalid values      : 0
[DEBUG] Skipped null        : 2
[RESULT] Status             : PASS

# pada [DEBUG] Skipped null sebaiknya dihapus
```

- `validasi unique` seharusnya melakukan cek full row duplication serta business key duplication