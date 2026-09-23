```py
MISSING_VALUES = ["", "NA", "N/A", "na", "n/a", "N/a"]
```

```bash
DQ-004
Schema Validation
│
├── Required Columns
├── Optional Columns
├── Column Order
├── Data Types
├── Nullable / Non-nullable
└── Schema Contract


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




### Perubahan utama

Sekarang schema boleh tetap seperti:

```python
TITANIC_SCHEMA = {
    "passengerid": {
        "type": "integer",
        "nullable": False,
        "required": True,
        "unique": True,
        "primary_key": True
    },
    "survived": {
        "type": "integer",
        "nullable": False,
        "required": True,
        "allowed": ["0", "1"]
    }
}
```

sedangkan CSV boleh memiliki:

```text
PassengerId,Survived,Pclass,Name,Sex,...
```

atau bahkan:

```text
PASSENGERID,SURVIVED,PCLASS,NAME,SEX,...
```

atau:

```text
passengerid,survived,pclass,name,sex,...
```

Semuanya akan dianggap cocok karena menggunakan:

```python
.casefold()
```

sebagai normalisasi nama kolom.

Contoh mapping yang akan terlihat pada debug:

```text
[DEBUG] Column Mapping
  ├─ Mode      : CASE-INSENSITIVE
  ├─ CSV Header:
  │  ├─ PassengerId
  │  ├─ Survived
  │  ├─ Pclass
  │  ├─ Name
  │  └─ ...
  └─ Schema Mapping:
     ├─ passengerid → PassengerId
     ├─ survived → Survived
     ├─ pclass → Pclass
     ├─ name → Name
     └─ ...
```

Dengan perubahan ini, kasus sebelumnya:

```text
passengerid → row.get("passengerid") → None
```

sudah tidak terjadi lagi.

Sekarang prosesnya menjadi:

```text
schema
   │
   └── passengerid
           │
           ▼
      casefold()
           │
           ▼
      "passengerid"
           │
           ▼
      column_map
           │
           ▼
      "PassengerId"
           │
           ▼
      row.get("PassengerId")
           │
           ▼
      "1"
```

Jadi **case-insensitive hanya berlaku untuk nama kolom**, bukan untuk isi/value data. Misalnya `Sex` dengan allowed `["male", "female"]` tetap divalidasi sesuai value yang didefinisikan schema.
