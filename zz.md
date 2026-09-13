1. Pembagian File .ipynb dalam Pipeline Data
Untuk proyek skala besar, memisahkan proses ke dalam beberapa file .ipynb bertujuan untuk:

Menghemat penggunaan RAM/GPU.

Memudahkan proses debugging dan isolasi kendala.

Menghindari pengulangan pemrosesan data mentah yang memakan waktu lama.

Memfasilitasi kolaborasi antar anggota tim secara paralel.

Ringkasan Alur Kerja Notebook

```bash
[01_ingestion] ──> [02_cleaning] ──> [03_wrangling] ──> [04_feature_eng] ──> [05_eda] ──> [06_validation]
```

Detail Tugas & Spesifikasi Tiap File Notebook
01_ingestion_and_raw_validation.ipynb
Fokus Utama: Pengambilan data mentah dan validasi awal (Sanity Check).

Tugas Spesifik:

Ekstraksi data dari berbagai sumber (API, Database SQL, Data Lake, S3/GCS, Web Scraping).

Verifikasi skema awal (jumlah kolom, nama kolom, tipe data dasar).

Pengecekan corrupted files atau kelengkapan baris data.

Logging metadata masuk (waktu unduh, versi data).

Output / Artifact: data/1_raw_staged/ (Format: Parquet / Partitioned Parquet).

02_cleaning_and_imputation.ipynb
Fokus Utama: Pembersihan data mendasar (Data Cleaning).

Tugas Spesifik:

Menangani nilai hilang (missing values) menggunakan strategi tertentu (imputasi statistik, KNN, atau model-based).

Identifikasi dan penghapusan duplikasi data (level baris maupun business key).

Standarisasi format string (penanganan karakter khusus, regex, lowercase/uppercase).

Penanganan outliers mendasar (penghapusan data eror ekstrem/logis).

Penyesuaian tipe data agar hemat memori (contoh: downcasting float64 ke float32, string ke category).

Output / Artifact: data/2_bronze_cleaned/ (Format: Parquet).

03_advanced_wrangling.ipynb
Fokus Utama: Restrukturisasi dan penggabungan data (Data Wrangling).

Tugas Spesifik:

Penggabungan data kompleks (joins/merges antar-tabel relasional besar).

Operasi Reshaping data (Pivoting, Unpivoting/Melting).

Pemrosesan data berantai (Window Functions, Agregasi temporal/spasial).

Integrasi data time-series (resampling, lag features awal, rolling window).

Output / Artifact: data/3_silver_processed/ (Format: Parquet / Feather).

04_feature_engineering.ipynb
Fokus Utama: Pembentukan fitur (Feature Construction & Transformation).

Tugas Spesifik:

Pembentukan fitur berbasis domain bisnis (domain-specific features).

Transformasi data kontinu (Log transform, Box-Cox, Binning/Discretization).

Encoding variabel kategorik (One-Hot Encoding, Target Encoding, Ordinal Encoding).

Normalisasi dan Skalasi (StandardScaler, MinMaxScaler, RobustScaler).

Pemrosesan fitur khusus seperti ekstraksi Teks (TF-IDF/Embeddings) atau Gambar.

Output / Artifact: data/4_silver_features/ (Format: Parquet).

05_exploratory_data_analysis.ipynb
Fokus Utama: Eksplorasi visual dan analisis statistik mendalam.

Tugas Spesifik:

Analisis univariat, bivariat, dan multivariat.

Visualisasi matriks korelasi dan deteksi multikolinearitas (VIF).

Analisis Data Drift dan variansi variabel.

Uji hipotesis statistik terkait masalah bisnis.

Penarikan wawasan (insights) bisnis awal.

Output / Artifact: Visualisasi (reports/figures/) & Ringkasan Eksekutif (reports/eda_summary.md).

06_feature_selection_validation.ipynb
Fokus Utama: Seleksi fitur akhir dan validasi kualitas data siap-pakai.

Tugas Spesifik:

Seleksi fitur berkinerja tinggi (Chi-Square, Feature Importance via LightGBM/SHAP, Mutual Information).

Penanganan ketimpangan kelas (Class Imbalance) jika diperlukan (SMOTE, Undersampling).

Validasi kualitas akhir menggunakan pustaka validasi data (misalnya: Great Expectations).

Pemisahan awal dataset (Train-Test Split / Time-Based Split) untuk konsistensi tim.

Output / Artifact: data/5_gold_model_ready/ (Format: Parquet / Delta Lake).

2. Arsitektur Data Pipeline (Medallion Architecture)
Untuk menjaga keandalan data pada proyek kompleks, diterapkan arsitektur 3 lapis utama:

Layer,Nama Layer,Deskripsi & Status Data,Sumber Notebook
Raw / Staged,Landing Zone,Data mentah sesuai bentuk asli dari sumber tanpa modifikasi.,01_ingestion.ipynb
Bronze,Cleaned Data,"Data mentah yang tervalidasi skemanya, bebas karakter rusak, dan terbebas dari duplikat dasar.",02_cleaning.ipynb
Silver,Processed / Engineered Data,"Data yang sudah digabung, diubah strukturnya, dan dilengkapi fitur-fitur baru (Intermediate Stage).",03_wrangling.ipynb04_feature_eng.ipynb
Gold,Analytics / Model Ready,"Data final dengan kualitas teruji, siap dikonsumsi langsung oleh model Machine Learning atau dashboard BI.",06_validation.ipynb

3. Rekomendasi Struktur Folder Proyek
Struktur folder terstandarisasi untuk memisahkan antara source code, data, notebook, dan artifact.

```bash
my_complex_data_project/
│
├── README.md                           <-- Penjelasan umum proyek & panduan setup
├── requirements.txt                    <-- Dependensi pustaka Python (pip)
├── environment.yml                     <-- (Opsional) Setup environment Conda
├── .gitignore                          <-- Mengabaikan file data/sensitif agar tidak masuk Git
│
├── data/                               <-- Menyimpan data (diabaikan oleh Git)
│   ├── 1_raw_staged/                   <-- Output 01 (Data mentah tervalidasi)
│   ├── 2_bronze_cleaned/               <-- Output 02 (Data hasil cleaning)
│   ├── 3_silver_processed/             <-- Output 03 (Data hasil wrangling)
│   ├── 4_silver_features/              <-- Output 04 (Data dengan fitur baru)
│   └── 5_gold_model_ready/             <-- Output 06 (Data siap pakai)
│
├── notebooks/                          <-- Direktori berisi file Jupyter Notebook
│   ├── 01_ingestion_and_raw_validation.ipynb
│   ├── 02_cleaning_and_imputation.ipynb
│   ├── 03_advanced_wrangling.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_exploratory_data_analysis.ipynb
│   └── 06_feature_selection_validation.ipynb
│
├── src/                                <-- Source code Python terstruktur (.py)
│   ├── __init__.py                     <-- Menjadikan src sebagai package Python
│   ├── config.py                       <-- File konfigurasi (path, database credentials, konstanta)
│   ├── utils.py                        <-- Fungsi bantuan umum (logging, timer, I/O)
│   ├── cleaning.py                     <-- Fungsi kustom untuk cleaning & imputasi
│   ├── wrangling.py                    <-- Fungsi kustom untuk transformasi & penggabungan
│   └── features.py                     <-- Fungsi kustom untuk ekstraksi/encoding fitur
│
├── models/                             <-- Tempat menyimpan model (.pkl, .joblib, .onnx)
│
└── reports/                            <-- Output analisis bisnis & visualisasi
    ├── figures/                        <-- Gambar/plot statistik dari EDA
    └── eda_summary.md                  <-- Catatan temuan bisnis mendalam
```

4. Praktik Terbaik (Best Practices) untuk Proyek Kompleks
A. Penggunaan Format Data Intermediate
Gunakan .parquet atau .feather, jangan menggunakan .csv untuk pertukaran data antar-notebook.

Keunggulan Parquet:

Kecepatan baca/tulis jauh lebih tinggi.

Kompresi data efisien (menghemat memori hingga 70-80%).

Menyimpan tipe data secara native (tipe datetime, category, dan float32 tidak akan berubah menjadi string/object saat dibaca ulang).

B. Menerapkan Refactoring Kode ke Modul Python (src/)
Notebook (.ipynb) hanya digunakan untuk eksperimen, pemanggilan fungsi, dan visualisasi.

Logika atau fungsi pembersihan yang berulang harus dipindahkan ke file .py di folder src/.

C. Manajemen Memori & Logging State
Hapus DataFrame Sementara: Gunakan perintah del df_temp dan gc.collect() untuk membersihkan RAM secara manual di dalam notebook jika menangani dataset berukuran gigabyte.

Lakukan Logging State: Catat ringkasan statistik (seperti jumlah baris data sebelum dan sesudah cleaning) di setiap akhir langkah notebook untuk mempermudah proses pemantauan kualitas data (data auditing).