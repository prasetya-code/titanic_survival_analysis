# Cara Menentukan Status Kolom

Penentuan sebuah kolom bersifat required atau nullable bukan berdasarkan "tebakan", melainkan berdasarkan logika bisnis dan peran teknis kolom tersebut:


## Kolom Wajib Ada & Tidak Boleh Null (`required: True, nullable: False`)

Ditentukan jika kolom memiliki peran:

1. **Primary Key / Identifier Utama**: Identitas unik tiap baris (contoh: `passengerid, user_id, transaction_id`). Jika `null`, data tidak bisa diidentifikasi.

2. **Target Utama (Label)**: Kolom yang jadi tujuan prediksi (contoh: `survived` pada dataset Titanic, atau `is_fraud` pada data transaksi).

3. **Variabel Kategorikal / Atribut Kunci**: Data dasar yang pasti dimiliki semua entitas (contoh: `sex, created_at`).


## Kolom Boleh Null (`nullable: True`)

Ditentukan jika secara realitas bisnis datanya memang tidak selalu ada:

1. Informasi Opsional: Data yang pengguna/sistem tidak wajib isi (contoh: `cabin, middle_name, phone_number_2`).

2. Kondisional: Nilai baru terisi jika kejadian tertentu terjadi (contoh: `discount_code, cancellation_reason`).

3. Pengukuran yang Hilang: Data sensor atau input manual yang rentan luput (contoh: `age, fare`).


## Cara Menentukannya dalam Praktik

1. Konsultasi Aturan Bisnis (Business Rules): Tanyakan ke Domain Expert / Product Owner: "Apakah seorang penumpang bisa terdaftar tanpa umur?" Jika bisa, maka `nullable = True`.

2. Cek Schema Contract Database Sumber: Jika data diambil dari PostgreSQL/MySQL, lihat definisi tabelnya. Kolom dengan atribut `NOT NULL` otomatis menjadi `nullable = False`.

3. Exploratory Data Analysis (EDA): Cek persentase data kosong pada dataset historis. Jika kolom memiliki null ratio tinggi tetapi tetap berguna, setel sebagai `nullable = True`.

---
# Dupication

## Primary Key Duplicate

## Full-Row Duplicate

## Business-Key Duplicate (`tergantung aturan bisnis`)

misal, Satu customer hanya boleh mempunyai satu transaksi untuk product tertentu pada tanggal tertentu. Maka business key-nya:

```bash
customer + product + date
```

> tidak semua dataset membutuhkan Business-Key Duplicate

---

# library Description

| Library          | Fungsi utama                                     | Contoh penggunaan                              |
| ---------------- | ------------------------------------------------ | ---------------------------------------------- |
| **pandas**       | Mengolah dan menganalisis data berbentuk tabel   | membaca CSV, cleaning, filtering, grouping     |
| **numpy**        | Komputasi numerik dan array                      | operasi matematika, array, missing value       |
| **matplotlib**   | Membuat visualisasi data                         | bar chart, histogram, scatter plot, line chart |
| **scikit-learn** | Machine Learning                                 | preprocessing, training model, evaluasi        |
| **scipy**        | Scientific/statistical computing                 | uji statistik, distribusi, optimasi            |
| **kagglehub**    | Mengambil dataset Kaggle secara programatis      | download dataset Titanic                       |
| **shap**         | Explainable AI / menjelaskan model ML            | mengetahui fitur apa yang memengaruhi prediksi |

---

# Layer Section

## Layer 1 — Data

```bash
Raw Data
   ↓
Data Quality
   ↓
Clean Data
```

## Layer 2 — Analytics

```bash
EDA
   ↓
Hypothesis
   ↓
Insight
```

## Layer 3 — Machine Learning

```bash
Feature Engineering
   ↓
Baseline
   ↓
Benchmark
   ↓
Validation
   ↓
Optimization
   ↓
Explainability
```

## Layer 4 — Business Communication

```bash
Executive Summary
        ↓
Dashboard
        ↓
Recommendation
        ↓
GitHub Portfolio
```

---

# Hal yang Saya Anggap "Senior-Level"

## ketika menemukan missing value

jangan
```bash
Missing value
↓
fillna()
↓
model
```

tetapi
```bash
Missing Value
↓
Why is it missing?
↓
What is the business meaning?
↓
Potential impact
↓
Treatment
↓
Validation
```

## ketika melakukan analisa pada model

jangan
```bash
Random Forest accuracy = 82%
```

tetapi
```bash
Baseline
      ↓
Logistic Regression
      ↓
Decision Tree
      ↓
Random Forest
      ↓
Gradient Boosting
      ↓
Cross Validation
      ↓
Statistical Stability
      ↓
Final Model
```

## Ketika melakukan feature engineering

jangan
```bash
Feature importance
```

tetapi
```bash
Feature Importance
       ↓
Why is it important?
       ↓
Does EDA support it?
       ↓
Is it stable?
       ↓
Does removing it hurt performance?
       ↓
Business interpretation
```

---

# Overview

Data telah dibagi menjadi dua kelompok:

1. **Training set (`train.csv`)**: Digunakan untuk membangun model *machine learning*. Pada file ini, hasil (dikenal juga sebagai *"ground truth"*) untuk setiap penumpang telah disediakan. Model Anda akan dibuat berdasarkan fitur-fitur seperti jenis kelamin dan kelas penumpang. Anda juga dapat menggunakan *feature engineering* untuk membuat fitur baru.

2. **Test set (`test.csv`)**: Digunakan untuk menguji seberapa baik kinerja model Anda pada data baru (*unseen data*). Pada file ini, *ground truth* tidak disediakan. Tugas Anda adalah memprediksi apakah setiap penumpang di *test set* selamat atau tidak dari tenggelamnya kapal Titanic.

3. **`gender_submission.csv`**: Contoh file pengiriman (*submission*) yang mengasumsikan hanya penumpang perempuan yang selamat.


## Data Dictionary

| Variable | Definition | Key |
| :--- | :--- | :--- |
| **survival** | Survival | `0` = No, `1` = Yes |
| **pclass** | Ticket class | `1` = 1st (Upper), `2` = 2nd (Middle), `3` = 3rd (Lower) |
| **sex** | Sex | — |
| **Age** | Age in years | — |
| **sibsp** | # of siblings / spouses aboard the Titanic | — |
| **parch** | # of parents / children aboard the Titanic | — |
| **ticket** | Ticket number | — |
| **fare** | Passenger fare | — |
| **cabin** | Cabin number | — |
| **embarked** | Port of Embarkation | `C` = Cherbourg, `Q` = Queenstown, `S` = Southampton |


## Variable Notes

* **`pclass`**  
  Representasi dari status sosial-ekonomi (*Socio-Economic Status* / SES):
  * `1st` = Kelas Atas (*Upper*)
  * `2nd` = Kelas Menengah (*Middle*)
  * `3rd` = Kelas Bawah (*Lower*)

* **`age`**  
  Umur berbentuk pecahan jika kurang dari 1 tahun. Jika umur merupakan perkiraan, formatnya berupa `xx.5`.

* **`sibsp`**  
  Hubungan keluarga didefinisikan sebagai berikut:
  * **Sibling** = saudara kandung, saudara tiri (laki-laki/perempuan)
  * **Spouse** = suami, istri (tunangan dan kekasih diabaikan)

* **`parch`**  
  Hubungan keluarga didefinisikan sebagai berikut:
  * **Parent** = ibu, ayah
  * **Child** = anak perempuan, anak laki-laki, anak tiri
  * *Catatan:* Beberapa anak hanya bepergian dengan pengasuh, sehingga untuk mereka `parch = 0`.


# NOTEBOOKS

```bash
# not enterprise mode
01_ingestion_and_raw_validation.ipynb
│
├── 1. Import & configuration
├── 2. Expected schema
├── 3. File sanity check
├── 4. SHA256 / source version
├── 5. Load raw CSV
├── 6. Normalize column names
├── 7. Validate column count & names
├── 8. Validate data types
├── 9. Validate row count / empty dataset
├── 10. Missing-value report
├── 11. Basic value sanity check
├── 12. Raw dataset summary
├── 13. Write Parquet
├── 14. Ingestion metadata
├── 15. Validate staged artifacts
└── 16. Final ingestion report
└── 17. Resource cleanup
```

# Another

```bash
DATA QUALITY
│
├── 1. Integrity
│   ├── File existence
│   ├── File type
│   ├── File size
│   ├── CSV structure
│   ├── Encoding
│   └── SHA-256
│
├── 2. Schema
│   ├── Column existence
│   ├── Column order
│   ├── Column name
│   ├── Duplicate column
│   ├── Data type
│   ├── Nullable
│   └── Semantic type
│
├── 3. Completeness
│   ├── Null count
│   ├── Null ratio
│   ├── Required fields
│   ├── Missing threshold
│   └── Missing tokens
│
├── 4. Uniqueness
│   ├── Primary key
│   ├── Full-row duplicate
│   └── Business-key duplicate
│
├── 5. Validity
│   ├── Numeric domain
│   ├── Categorical domain
│   ├── String quality
│   └── Name format
│
├── 6. Consistency
│   ├── Train/Test ID overlap
│   └── Row-count drift
│
├── 7. Artifact Quality
│   ├── Parquet write
│   ├── Read-back
│   ├── Row preservation
│   ├── Column preservation
│   ├── Dtype preservation
│   └── Schema fingerprint
│
└── 8. Governance / Provenance
    ├── Run ID
    ├── Timestamp
    ├── Git
    ├── Environment
    ├── Pipeline version
    ├── Schema version
    ├── DQ rules version
    └── Validation report
```

| Kategori           | Pertanyaan yang dijawab                                     |
| ------------------ | ----------------------------------------------------------- |
| **Completeness**   | Apakah data yang dibutuhkan tersedia?                       |
| **Uniqueness**     | Apakah record/key yang seharusnya unik memang unik?         |
| **Validity**       | Apakah nilai sesuai aturan/domain?                          |
| **Consistency**    | Apakah data konsisten antar kolom/dataset?                  |
| **Accuracy**       | Apakah data merepresentasikan kondisi sebenarnya?           |
| **Timeliness**     | Apakah data cukup terbaru?                                  |
| **Integrity**      | Apakah data/file tidak rusak atau berubah secara tidak sah? |
| **Schema Quality** | Apakah struktur data sesuai kontrak?                        |
| **Provenance**     | Apakah asal-usul dan proses data dapat dilacak?             |
