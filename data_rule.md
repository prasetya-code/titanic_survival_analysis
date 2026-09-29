# Data Constraint, Validation, Baseline Profiling, dan Model Pipeline

## 1. Overview

Constraint merupakan aturan yang digunakan untuk memastikan data memenuhi kondisi yang diharapkan sebelum digunakan pada proses berikutnya.

Secara umum pipeline:

```text
Raw Data
   │
   ▼
Schema Validation
   │
   ▼
Constraint Validation
   │
   ├── Unique
   ├── Range
   ├── Allowed Values
   ├── Nullability
   ├── Relationship
   ├── Referential Integrity
   ├── Conditional
   ├── Pattern
   ├── Cardinality
   └── Business Rule
   │
   ▼
Validated Data
   │
   ├── Baseline Profiling
   │
   ▼
Feature Engineering
   │
   ▼
Train / Test Split
   │
   ▼
Model
```

---

# 2. Schema vs Constraint

Schema dan constraint sama-sama merupakan bagian dari **data contract**, tetapi memiliki fokus yang berbeda.

### Schema

Schema menjelaskan karakteristik masing-masing kolom.

Contoh:

```yaml
columns:

  age:
    dtype: Int64
    semantic_type: numeric
    min: 0
    max: 100
    nullable: true
    required: false
```

Artinya:

* `age` harus bertipe `Int64`
* `age` merupakan data numerik
* nilai minimum `0`
* nilai maksimum `100`
* nilai `null` diperbolehkan

### Constraint

Constraint menjelaskan aturan yang harus dipenuhi oleh data, terutama hubungan antar kolom atau kondisi tertentu.

Contoh:

```yaml
constraints:

  unique:
    - name: passenger_identity
      columns:
        - name
        - sex
        - age
```

Artinya kombinasi `name + sex + age` diharapkan unik.

---

# 3. Jenis-Jenis Constraint

| Constraint            | Fungsi                                   | Contoh                             |
| --------------------- | ---------------------------------------- | ---------------------------------- |
| Unique                | Memastikan nilai/kombinasi unik          | `passengerid`                      |
| Range                 | Membatasi nilai numerik                  | `age >= 0`                         |
| Allowed Values        | Membatasi nilai kategori                 | `sex = male/female`                |
| Nullability           | Mengontrol nilai kosong                  | `passengerid` tidak boleh null     |
| Relationship          | Memvalidasi hubungan antar kolom         | `ticket` ↔ `pclass`                |
| Referential Integrity | Memastikan referensi ada di dataset lain | `customer_id`                      |
| Conditional           | Aturan berdasarkan kondisi               | Jika `type=adult`, `age` wajib ada |
| Cross-field           | Membandingkan beberapa kolom             | `total = quantity × price`         |
| Pattern               | Memvalidasi pola string                  | `ID-00001`                         |
| Cardinality           | Membatasi jumlah kategori                | `sex` maksimal 2 kategori          |
| Business Rule         | Aturan domain bisnis                     | Aturan transaksi                   |

---

# 4. Unique Constraint

Unique constraint digunakan untuk memastikan suatu kolom atau kombinasi kolom tidak memiliki duplikasi.

### Single Column

```yaml
constraints:

  unique:
    - name: passenger_id_unique
      columns:
        - passengerid
```

Implementasi:

```python
duplicates = df[
    df.duplicated(
        subset=["passengerid"],
        keep=False
    )
]
```

### Composite Unique

```yaml
constraints:

  unique:
    - name: passenger_identity
      columns:
        - name
        - sex
        - age
```

Implementasi:

```python
duplicates = df[
    df.duplicated(
        subset=["name", "sex", "age"],
        keep=False
    )
]
```

---

# 5. Range Constraint

Range digunakan untuk memastikan nilai berada dalam rentang tertentu.

```yaml
constraints:

  range:
    - name: valid_age
      column: age
      min: 0
      max: 100
```

Implementasi:

```python
invalid = df[
    (df["age"] < 0) |
    (df["age"] > 100)
]
```

---

# 6. Allowed Values

Digunakan untuk memastikan nilai hanya berasal dari kategori yang telah ditentukan.

```yaml
columns:

  sex:
    dtype: String
    semantic_type: categorical
    allowed_values:
      - male
      - female
```

Implementasi:

```python
invalid = df[
    ~df["sex"].isin([
        "male",
        "female"
    ])
]
```

---

# 7. Nullability

Nullability menentukan apakah nilai kosong diperbolehkan.

```yaml
columns:

  passengerid:
    nullable: false
```

Implementasi:

```python
invalid = df["passengerid"].isna()
```

Untuk batas jumlah null:

```yaml
columns:

  age:
    nullable: true
    max_null_ratio: 0.3
```

Implementasi:

```python
null_ratio = df["age"].isna().mean()

if null_ratio > 0.3:
    print("FAIL")
```

Perbedaannya:

```text
nullable
    ↓
Apakah null diperbolehkan?

max_null_ratio
    ↓
Berapa banyak null yang masih diperbolehkan?
```

---

# 8. Relationship Constraint

Relationship digunakan untuk memastikan hubungan tertentu antar kolom.

Contoh:

```yaml
constraints:

  relationship:

    - name: ticket_pclass_consistency
      columns:
        - ticket
        - pclass
```

Misalnya:

```text
ticket      pclass
------------------
A/5 21171      3
PC 17599       1
PC 17599       1
```

Valid.

Tetapi:

```text
ticket      pclass
------------------
PC 17599       1
PC 17599       3
```

dapat dianggap violation apabila business rule menetapkan satu `ticket` hanya boleh memiliki satu `pclass`.

Implementasi:

```python
invalid = (
    df.groupby("ticket")["pclass"]
      .nunique()
)

invalid = invalid[invalid > 1]
```

---

# 9. Referential Integrity

Digunakan ketika terdapat beberapa dataset yang saling berhubungan.

Contoh:

```text
customer.csv

customer_id
-----------
001
002
003
```

Kemudian:

```text
transaction.csv

customer_id
-----------
001
002
999
```

`999` tidak ditemukan pada `customer.csv`.

Contract:

```yaml
constraints:

  referential_integrity:

    - name: transaction_customer
      column: customer_id
      reference:
        dataset: customer
        column: customer_id
```

Tujuannya memastikan foreign key memiliki referensi yang valid.

---

# 10. Conditional Constraint

Constraint berdasarkan kondisi tertentu.

Contoh:

```yaml
constraints:

  conditional:

    - name: adult_age_required

      when:
        column: passenger_type
        equals: adult

      then:
        column: age
        required: true
```

Secara logika:

```text
IF passenger_type == "adult"
THEN age != null
```

Implementasi:

```python
invalid = df[
    (df["passenger_type"] == "adult") &
    (df["age"].isna())
]
```

---

# 11. Cross-Field Constraint

Cross-field constraint digunakan untuk memvalidasi hubungan antar beberapa kolom.

Contoh:

```text
quantity
price
total
```

Rule:

```text
total = quantity × price
```

Contract:

```yaml
constraints:

  cross_field:

    - name: total_calculation
      expression: "total == quantity * price"
```

Implementasi:

```python
invalid = df[
    df["total"] !=
    df["quantity"] * df["price"]
]
```

---

# 12. Pattern Constraint

Pattern digunakan untuk memvalidasi format string.

Contoh:

```text
ID-00001
ID-00002
ID-00003
```

Contract:

```yaml
constraints:

  pattern:

    - name: valid_customer_id
      column: customer_id
      regex: "^ID-[0-9]{5}$"
```

Implementasi:

```python
invalid = df[
    ~df["customer_id"].str.match(
        r"^ID-[0-9]{5}$",
        na=False
    )
]
```

---

# 13. Cardinality Constraint

Cardinality digunakan untuk membatasi jumlah kategori unik.

Contoh:

```yaml
constraints:

  cardinality:

    - name: sex_cardinality
      column: sex
      max_unique: 2
```

Misalnya data memiliki:

```text
male
female
unknown
other
```

Maka jumlah kategori telah berubah dari kondisi yang diharapkan.

Cardinality dapat digunakan sebagai salah satu indikator perubahan kualitas data.

---

# 14. Business Rule

Business rule merupakan constraint yang lebih spesifik terhadap domain bisnis.

Contoh:

```yaml
constraints:

  business_rules:

    - name: valid_ticket_class
      expression: "ticket != null AND pclass IN [1,2,3]"
```

Namun sebaiknya YAML tidak digunakan sebagai bahasa pemrograman penuh.

Jika rule sudah kompleks, lebih baik:

```text
constraints.yaml
       │
       ▼
constraint name
       │
       ▼
Python Validator
       │
       ▼
PASS / FAIL
```

Dengan demikian YAML mendefinisikan **apa yang harus divalidasi**, sedangkan Python menangani **bagaimana validasi dilakukan**.

---

# 15. Hard Constraint, Soft Constraint, dan Monitoring

Constraint dapat dikelompokkan berdasarkan konsekuensi ketika terjadi pelanggaran.

## Hard Constraint

Data dianggap tidak valid apabila aturan dilanggar.

Contoh:

```text
Primary Key
Required Column
Data Type
Mandatory Nullability
Referential Integrity
```

Pipeline:

```text
Violation
    ↓
FAIL
    ↓
Data ditolak / dihentikan
```

## Soft Constraint

Data masih dapat diterima, tetapi menghasilkan warning.

Contoh:

```text
Null Ratio
Range tertentu
Cardinality
Data Quality Threshold
```

Pipeline:

```text
Violation
    ↓
WARNING
    ↓
Data tetap dapat diproses
```

## Monitoring

Digunakan untuk mengamati perubahan karakteristik data.

Contoh:

```text
Mean
Median
Standard Deviation
Quantile
Null Ratio
Category Frequency
Distribution
```

Bagian ini lebih tepat masuk ke **baseline profiling dan drift detection**, bukan constraint murni.

---

# 16. Baseline Profiling

Baseline profiling bukan constraint.

Baseline menjawab:

> "Seperti apa kondisi normal dataset?"

Contoh:

```json
{
  "age": {
    "count": 714,
    "null_ratio": 0.1987,
    "mean": 29.699,
    "median": 28.0,
    "std": 14.526,
    "min": 0.42,
    "max": 80.0
  }
}
```

Baseline kemudian digunakan sebagai referensi untuk data berikutnya.

```text
Baseline
   │
   ▼
profile.json
   │
   │ compare
   ▼
Future Data
   │
   ▼
Drift Detection
```

---

# 17. Struktur File yang Direkomendasikan

Untuk project ini:

```text
project/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── metadata/
│   └── schema/
│       └── train.yaml
│
├── baseline/
│   └── train/
│       └── profile.json
│
├── reports/
│   └── drift/
│       └── drift_report.json
│
├── src/
│   ├── validation/
│   ├── profiling/
│   └── drift/
│
└── notebooks/
    └── validation.ipynb
```

---

# 18. Contoh Schema Contract

`train.yaml`:

```yaml
columns:

  passengerid:
    dtype: Int64
    semantic_type: primary_key
    nullable: false
    required: true

  survived:
    dtype: Int64
    semantic_type: binary_target
    allowed_values:
      - 0
      - 1
    nullable: false
    required: true

  pclass:
    dtype: Int64
    semantic_type: categorical
    allowed_values:
      - 1
      - 2
      - 3
    nullable: false
    required: true

  name:
    dtype: String
    semantic_type: text
    nullable: false
    required: true

  sex:
    dtype: String
    semantic_type: categorical
    casing: lower
    allowed_values:
      - male
      - female
    nullable: false
    required: true

  sibsp:
    dtype: Int64
    semantic_type: count
    min: 0
    nullable: false
    required: true

  parch:
    dtype: Int64
    semantic_type: count
    min: 0
    nullable: false
    required: true

  ticket:
    dtype: String
    semantic_type: identifier
    nullable: false
    required: true

  age:
    dtype: Int64
    semantic_type: numeric
    min: 0
    max: 100
    max_null_ratio: 0.3
    nullable: true
    required: false

  fare:
    dtype: Float64
    semantic_type: numeric
    min: 0
    max_null_ratio: 0.05
    nullable: true
    required: false

  cabin:
    dtype: String
    semantic_type: categorical_text
    max_null_ratio: 0.9
    nullable: true
    required: false

  embarked:
    dtype: String
    semantic_type: categorical
    casing: upper
    allowed_values:
      - C
      - Q
      - S
    max_null_ratio: 0.05
    nullable: true
    required: false


constraints:

  unique:

    - name: passenger_identity
      columns:
        - name
        - sex
        - age

    - name: ticket_group
      columns:
        - ticket
        - pclass
```

---

# 19. Hubungan dengan Machine Learning

Constraint validation sebaiknya dilakukan **sebelum data masuk ke proses training**.

```text
                  RAW DATA
                     │
                     ▼
             Schema Validation
                     │
                     ▼
            Constraint Validation
                     │
             ┌───────┴───────┐
             │               │
           FAIL             PASS
             │               │
             ▼               ▼
          Reject          Valid Data
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
        Baseline Profiling        Feature Engineering
                │                         │
                ▼                         ▼
          profile.json              Train / Test
                                          │
                                          ▼
                                       Model
```

Baseline kemudian digunakan untuk monitoring:

```text
                BASELINE
             profile.json
                   │
                   │
                   ▼
             Future Dataset
                   │
                   ▼
            Profiling Future
                   │
                   ▼
            Drift Detection
                   │
                   ▼
           drift_report.json
```

---

# 20. Prinsip Utama

Struktur data contract dapat diringkas menjadi:

```text
Schema
  ↓
"Data harus memiliki bentuk seperti apa?"

Constraint
  ↓
"Aturan apa yang harus dipenuhi data?"

Baseline
  ↓
"Seperti apa kondisi normal data?"

Drift
  ↓
"Apa yang berubah dibandingkan kondisi normal?"

Model
  ↓
"Bagaimana data yang sudah tervalidasi digunakan untuk ML?"
```

Dengan pendekatan ini:

* **YAML** digunakan untuk `schema + constraints`.
* **JSON** digunakan untuk hasil `baseline profiling`.
* **JSON** dapat digunakan untuk hasil `drift report`.
* Constraint divalidasi sebelum data masuk ke training.
* Baseline bukan constraint, melainkan **referensi kondisi data**.
* Feature engineering dilakukan setelah data melewati validasi.
* Model menggunakan data yang telah melewati proses validasi dan preprocessing.
