# Data Pipeline — Struktur Notebook, Arsitektur Data, dan Best Practices

## `01_ingestion_and_raw_validation.ipynb`

**Fokus utama:** Pengambilan data mentah dan validasi awal (*sanity check*).

### Tugas Spesifik

* Ekstraksi data dari berbagai sumber:
  * API
  * Database SQL
  * Data Lake
  * Amazon S3 / Google Cloud Storage
  * Web Scraping

* Verifikasi skema awal:
  * jumlah kolom
  * nama kolom
  * tipe data dasar

* Pengecekan:
  * file corrupt
  * file kosong
  * jumlah baris
  * kelengkapan data

* Validasi struktur dasar dataset.
* Logging metadata data yang masuk:
  * waktu pengambilan/unduh
  * sumber data
  * versi data
  * ukuran dataset
  * timestamp proses

### Output / Artifact

```bash
data/1_raw_staged/
```

Format yang disarankan:

```bash
Parquet / Partitioned Parquet
```

**Prinsip:** Data pada tahap ini sebaiknya masih mempertahankan bentuk sedekat mungkin dengan sumber aslinya. Jangan melakukan transformasi bisnis yang signifikan pada tahap ingestion.

---

## 1.2 `02_cleaning_and_imputation.ipynb`

**Fokus utama:** Pembersihan data mendasar (*data cleaning*).

### Tugas Spesifik

* Menangani nilai hilang (*missing values*) menggunakan strategi yang sesuai:

  * statistical imputation
  * KNN imputation
  * model-based imputation
* Identifikasi dan penghapusan duplikasi:

  * duplikasi baris
  * duplikasi berdasarkan *business key*
* Standarisasi format string:

  * karakter khusus
  * regex
  * lowercase / uppercase
  * whitespace
* Penanganan outlier mendasar:

  * data error ekstrem
  * nilai yang secara logis tidak mungkin
* Penyesuaian tipe data untuk efisiensi memori:

  * `float64` → `float32`
  * `int64` → tipe integer yang lebih kecil jika memungkinkan
  * `object/string` → `category` jika sesuai

### Output / Artifact

```bash
data/2_bronze_cleaned/
```

Format:

```bash
Parquet
```

**Prinsip:** Tahap Bronze menghasilkan data yang sudah bersih secara teknis, tetapi belum tentu sudah siap digunakan untuk analisis bisnis atau machine learning.

---

## 1.3 `03_advanced_wrangling.ipynb`

**Fokus utama:** Restrukturisasi dan penggabungan data (*data wrangling*).

### Tugas Spesifik

* Penggabungan data kompleks:

  * `join`
  * `merge`
  * relasi antar-tabel
* Reshaping data:

  * pivot
  * unpivot
  * melt
* Pemrosesan data berantai:

  * window functions
  * agregasi
  * agregasi temporal
  * agregasi spasial
* Integrasi data time-series:

  * resampling
  * lag features awal
  * rolling window
* Restrukturisasi dataset agar sesuai dengan kebutuhan analisis berikutnya.

### Output / Artifact

```bash
data/3_silver_processed/
```

Format:

```bash
Parquet / Feather
```

**Prinsip:** Tahap ini menghasilkan dataset yang telah memiliki struktur analitis yang lebih baik dan dapat menjadi input untuk feature engineering.

---

## 1.4 `04_feature_engineering.ipynb`

**Fokus utama:** Pembentukan dan transformasi fitur (*feature construction & transformation*).

### Tugas Spesifik

#### A. Feature Construction

* Membentuk fitur berdasarkan domain bisnis.
* Membuat fitur turunan dari kolom yang sudah tersedia.
* Membentuk fitur agregasi atau kombinasi variabel.

#### B. Transformasi Variabel

* Log transformation
* Box-Cox transformation
* Binning / discretization
* Transformasi kontinu lainnya sesuai kebutuhan model.

#### C. Encoding Variabel Kategorik

* One-Hot Encoding
* Target Encoding
* Ordinal Encoding

#### D. Normalisasi dan Scaling

* `StandardScaler`
* `MinMaxScaler`
* `RobustScaler`

#### E. Fitur Khusus

Untuk tipe data tertentu dapat dilakukan ekstraksi fitur khusus, misalnya:

* **Text**

  * TF-IDF
  * embeddings
* **Image**

  * image embeddings
  * feature extraction menggunakan model computer vision
* **Time-series**

  * lag
  * rolling statistics
  * seasonal features

### Output / Artifact

```bash
data/4_silver_features/
```

Format:

```bash
Parquet
```

**Prinsip:** Feature engineering harus dilakukan secara konsisten antara data training dan data inference agar tidak terjadi perbedaan representasi fitur.

---

## 1.5 `05_exploratory_data_analysis.ipynb`

**Fokus utama:** Eksplorasi visual dan analisis statistik mendalam.

### Tugas Spesifik

#### Analisis Data

* Analisis univariat.
* Analisis bivariat.
* Analisis multivariat.
* Distribusi variabel.
* Analisis hubungan antarvariabel.

#### Analisis Korelasi

* Matriks korelasi.
* Identifikasi hubungan antarvariabel.
* Deteksi multikolinearitas.
* Variance Inflation Factor (VIF).

#### Analisis Distribusi dan Variansi

* Distribusi data.
* Variansi variabel.
* Skewness.
* Potensi data drift.

#### Analisis Statistik

* Uji hipotesis sesuai kebutuhan bisnis.
* Analisis signifikansi statistik.
* Identifikasi pola dan anomali.

#### Business Insight

* Menemukan pola penting.
* Mengidentifikasi hubungan potensial.
* Menghasilkan insight awal yang relevan dengan *business problem*.

### Output / Artifact

Visualisasi:

```bash
reports/figures/
```

Ringkasan analisis:

```bash
reports/eda_summary.md
```

**Catatan:** EDA sebaiknya tidak hanya berisi grafik. Setiap visualisasi idealnya memiliki interpretasi dan kaitan dengan pertanyaan bisnis.

---

## 1.6 `06_feature_selection_validation.ipynb`

**Fokus utama:** Seleksi fitur akhir dan validasi kualitas dataset sebelum digunakan oleh model.

### Tugas Spesifik

#### A. Feature Selection

Metode yang dapat digunakan antara lain:

* Chi-Square
* Mutual Information
* Feature Importance
* LightGBM
* SHAP

Pemilihan metode harus disesuaikan dengan tipe data, algoritma, dan tujuan analisis.

#### B. Class Imbalance

Jika dataset memiliki ketimpangan kelas, dapat diterapkan strategi seperti:

* SMOTE
* Undersampling
* Oversampling
* Class weighting

Penerapan teknik ini harus dilakukan pada data training dan bukan secara sembarangan pada seluruh dataset untuk menghindari *data leakage*.

#### C. Data Quality Validation

Validasi kualitas akhir dapat menggunakan library seperti:

* Great Expectations
* Custom validation rules
* Schema validation

Contoh pemeriksaan:

* jumlah baris
* jumlah kolom
* tipe data
* missing values
* duplicate records
* range nilai
* uniqueness
* validitas kategori

#### D. Dataset Splitting

Pemisahan dataset dapat dilakukan sesuai karakteristik masalah:

* Train-Test Split
* Train-Validation-Test Split
* Time-Based Split

### Output / Artifact

```bash
data/5_gold_model_ready/
```

Format:

```bash
Parquet / Delta Lake
```

**Prinsip:** Gold layer harus menghasilkan dataset yang sudah tervalidasi dan siap dikonsumsi oleh model Machine Learning, dashboard BI, atau sistem analitik lainnya.

---

# 2. Arsitektur Data Pipeline — Medallion Architecture

Untuk menjaga kualitas, keterlacakan, dan keandalan data pada proyek kompleks, pipeline dapat menggunakan pendekatan **Medallion Architecture**.

Secara umum, data melewati beberapa tahap:

```bash
                  DATA SOURCE
                      │
                      ▼
             ┌─────────────────┐
             │ RAW / STAGED     │
             │ Original Data    │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ BRONZE           │
             │ Cleaned Data     │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ SILVER           │
             │ Processed Data   │
             │ + Features       │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ GOLD             │
             │ Model / BI Ready │
             └─────────────────┘
```

## 2.1 Mapping Layer terhadap Notebook

| Layer        | Nama / Status               | Deskripsi                                                                                                         | Notebook                                                       |
| ------------ | --------------------------- | ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Raw / Staged | Landing Zone                | Data mentah yang dipertahankan sedekat mungkin dengan bentuk asli dari sumber.                                    | `01_ingestion_and_raw_validation.ipynb`                        |
| Bronze       | Cleaned Data                | Data yang sudah tervalidasi secara teknis, dibersihkan dari masalah dasar, dan ditangani duplikasinya.            | `02_cleaning_and_imputation.ipynb`                             |
| Silver       | Processed / Engineered Data | Data yang sudah digabung, diubah strukturnya, dan dilengkapi fitur-fitur baru.                                    | `03_advanced_wrangling.ipynb` + `04_feature_engineering.ipynb` |
| Gold         | Analytics / Model Ready     | Data final yang telah melalui validasi kualitas dan siap dikonsumsi model ML, dashboard BI, atau sistem analitik. | `06_feature_selection_validation.ipynb`                        |

### Hubungan Folder dengan Layer

```bash
data/
│
├── 1_raw_staged/          → Raw / Staged
├── 2_bronze_cleaned/      → Bronze
├── 3_silver_processed/    → Silver
├── 4_silver_features/     → Silver
└── 5_gold_model_ready/    → Gold
```

**Catatan:** `05_exploratory_data_analysis.ipynb` berbeda dari notebook transformasi karena output utamanya adalah insight, visualisasi, dan laporan analisis, bukan layer data baru.

---

# 3. Rekomendasi Struktur Folder Proyek

Struktur folder sebaiknya memisahkan:

* source code
* data
* notebook
* model
* laporan
* konfigurasi

Contoh struktur:

```bash
my_complex_data_project/
│
├── README.md
├── requirements.txt
├── environment.yml
├── .gitignore
│
├── data/
│   ├── 1_raw_staged/
│   ├── 2_bronze_cleaned/
│   ├── 3_silver_processed/
│   ├── 4_silver_features/
│   └── 5_gold_model_ready/
│
├── notebooks/
│   ├── 01_ingestion_and_raw_validation.ipynb
│   ├── 02_cleaning_and_imputation.ipynb
│   ├── 03_advanced_wrangling.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_exploratory_data_analysis.ipynb
│   └── 06_feature_selection_validation.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── utils.py
│   ├── cleaning.py
│   ├── wrangling.py
│   └── features.py
│
├── models/
│   ├── trained/
│   └── artifacts/
│
└── reports/
    ├── figures/
    └── eda_summary.md
```

## 3.1 Penjelasan Setiap Direktori

### `data/`

Menyimpan data hasil setiap tahapan pipeline.

Pada proyek nyata, direktori ini biasanya **tidak dimasukkan ke Git**, terutama jika ukurannya besar atau mengandung data sensitif.

### `notebooks/`

Berisi notebook yang digunakan untuk:

* menjalankan pipeline secara interaktif
* eksplorasi
* eksperimen
* visualisasi
* validasi hasil

### `src/`

Berisi source code Python yang reusable.

Tujuannya adalah agar logika yang digunakan berulang kali tidak ditulis ulang di banyak notebook.

### `models/`

Menyimpan model Machine Learning dan artifact terkait.

Contoh:

```bash
.pkl
.joblib
.onnx
```

### `reports/`

Menyimpan hasil analisis dan visualisasi.

Contoh:

```bash
reports/
├── figures/
└── eda_summary.md
```

---

# 4. Praktik Terbaik untuk Proyek Data Kompleks

## 4.1 Gunakan Format Data Intermediate yang Efisien

Untuk pertukaran data antar-notebook, gunakan format seperti:

```bash
Parquet
Feather
```

Hindari penggunaan CSV sebagai format utama untuk intermediate dataset berukuran besar.

### Mengapa Parquet?

Parquet memiliki beberapa keunggulan:

* Pembacaan dan penulisan data umumnya lebih efisien daripada CSV.
* Mendukung kompresi.
* Menyimpan schema dan tipe data.
* Mendukung columnar storage.
* Dapat membaca hanya kolom yang diperlukan (*column pruning*).
* Cocok untuk dataset berukuran besar.

Contoh:

```bash
CSV
↓
Parsing ulang setiap kali dibaca
↓
Inferensi tipe data
↓
Lebih banyak overhead
```

Sedangkan:

```bash
Parquet
↓
Schema tersimpan
↓
Columnar storage
↓
Compression
↓
Effisien untuk analytical workload
```

> Besarnya penghematan storage dan RAM tidak selalu tetap pada angka tertentu seperti 70–80%. Hasilnya sangat bergantung pada struktur data, cardinality, tipe kolom, dan codec kompresi.

---

## 4.2 Pisahkan Eksperimen dan Reusable Code

Notebook (`.ipynb`) sebaiknya digunakan untuk:

* eksperimen
* eksplorasi
* visualisasi
* menjalankan pipeline
* memanggil fungsi

Sedangkan logika yang reusable sebaiknya ditempatkan di:

```bash
src/
```

Contoh:

```bash
src/
├── cleaning.py
├── wrangling.py
├── features.py
└── utils.py
```

### Contoh pembagian tanggung jawab

**Kurang ideal:**

```python
# Notebook
df = df.drop_duplicates()
df["age"] = df["age"].fillna(df["age"].median())
df["name"] = df["name"].str.lower()
...
```

Jika logic tersebut digunakan di banyak notebook, kode akan mudah mengalami duplikasi.

**Lebih baik:**

```python
from src.cleaning import clean_dataset

df = clean_dataset(df)
```

Dengan demikian, notebook berfungsi sebagai **orchestrator/experiment layer**, sedangkan `src/` menjadi tempat utama reusable business/data logic.

---

# 5. Manajemen Memori

Untuk dataset berukuran besar, penggunaan RAM perlu diperhatikan di setiap tahap pipeline.

## 5.1 Hapus DataFrame Sementara

Jika DataFrame sementara sudah tidak diperlukan:

```python
del df_temp
```

Kemudian, jika diperlukan:

```python
import gc

gc.collect()
```

Hal ini dapat membantu melepaskan referensi objek Python yang sudah tidak digunakan.

Namun, penggunaan `del` dan `gc.collect()` bukan pengganti desain pipeline yang efisien. Jika dataset terlalu besar, lebih baik pertimbangkan:

* chunk processing
* column selection
* filtering sebelum load
* Parquet
* partitioning
* streaming
* distributed processing

---

# 6. Logging dan Data Auditing

Setiap notebook sebaiknya mencatat **state dataset** setelah proses selesai.

Informasi yang dapat dicatat antara lain:

* jumlah baris sebelum proses
* jumlah baris setelah proses
* jumlah kolom
* jumlah missing values
* jumlah duplicate
* perubahan schema
* jumlah record yang dibuang
* waktu eksekusi
* nama/version input dataset
* lokasi output dataset

Contoh:

```bash
==================================================
PIPELINE STEP: DATA CLEANING
==================================================

Input rows       : 100,000
Output rows      : 98,450
Rows removed     : 1,550

Input columns    : 12
Output columns   : 12

Missing values   : 4,320 → 0
Duplicates       : 1,200 → 0

Execution time   : 12.43 seconds

Output:
data/2_bronze_cleaned/train.parquet
==================================================
```

Logging seperti ini membantu proses:

* debugging
* monitoring
* reproducibility
* data auditing
* quality control

---

# 7. Prinsip Utama Pipeline

Secara keseluruhan, pipeline dapat diringkas menjadi:

```bash
                    BUSINESS PROBLEM
                          │
                          ▼
                 ┌─────────────────┐
                 │ 01 INGESTION    │
                 │ Raw Validation  │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ 02 CLEANING     │
                 │ Bronze Layer    │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ 03 WRANGLING    │
                 │ Silver Layer    │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ 04 FEATURE ENG. │
                 │ Silver Features │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ 05 EDA          │
                 │ Insights        │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ 06 VALIDATION   │
                 │ Gold Layer      │
                 └────────┬────────┘
                          │
                          ▼
                MODEL / BI / ANALYTICS
```

## Prinsip yang Perlu Dipertahankan

1. **Setiap notebook memiliki satu tanggung jawab utama.**
2. **Input dan output setiap tahap harus jelas.**
3. **Intermediate data menggunakan format yang efisien seperti Parquet.**
4. **Notebook tidak menjadi tempat utama untuk reusable code.**
5. **Logic reusable ditempatkan di `src/`.**
6. **Setiap tahap mencatat perubahan dataset melalui logging.**
7. **Data mentah sebaiknya tidak dimodifikasi secara langsung.**
8. **Setiap layer dapat ditelusuri kembali ke layer sebelumnya.**
9. **Transformasi harus reproducible.**
10. **Train/test separation harus diperhatikan untuk mencegah data leakage.**

Dengan pendekatan ini, pipeline tidak hanya menjadi kumpulan notebook, tetapi menjadi **workflow data yang terstruktur, dapat diaudit, mudah di-debug, dan lebih mudah dikembangkan ketika ukuran maupun kompleksitas proyek meningkat.**
