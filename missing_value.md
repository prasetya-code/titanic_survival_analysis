# Ringkasan Matriks Missingness

| Persentase Null       | Kategori          | Karakteristik Kolom               | Strategi Penanganan Utama                                 |
| --------------------- | ----------------- | --------------------------------- | --------------------------------------------------------- |
| **`0.0%`**            | **Strict / Zero** | PK, Target (Label), Kolom Krusial | **Reject Row / Fail Pipeline** (No Imputation)            |
| **`< 5.0%`**          | **Low**           | Data operasional rutin            | **Drop Rows** / **Simple Imputation** (Mean/Median/Mode)  |
| **`5.0% – 30.0%`**    | **Moderate**      | Atribut penting rentan kosong     | **Advanced Imputation** (KNN, MICE, Group-based)          |
| **`30.0% – 50.0%`**   | **High**          | Atribut opsional                  | **Missing Indicator Flag** (`is_missing` = 0/1)           |
| **`> 50.0%`**         | **Extreme**       | Data sangat jarang diisi          | **Drop Column** / **Binary Conversion**                   |

---

# Detail Penanganan Berdasarkan Kategori

## A. Strict / Zero Tolerance (`0%`)
* **Kriteria:** Kolom wajib (`nullable: False`) yang berfungsi sebagai identitas utama atau target analisis.
* **Tindakan:**
  * **File Level:** Hentikan pipeline jika rasio `null > 0`
  * **Row Level:** Pisahkan baris bernilai `null` ke `quarantine table` untuk diperiksa tim data.

## B. Low Missingness (`< 1.0%` s.d. `5.0%`)
* **Kriteria:** Kebocoran data akibat kesalahan input ringan atau anomali sistemik sementara.
* **Tindakan:**
  * **Kategorikal:** Isi nilai kosong dengan `Mode (nilai terbanyak)` atau beri label `'Unknown'`.
  * **Numerik:** Isi nilai kosong dengan `Mean (jika distribusi normal)` atau `Median (jika skewed)`.
  * **Row Deletion:** Bisa menerapkan `df.drop_nulls()`, menghapus data yang memiliki null < `5.0%` tidak mengubah distribusi populasi secara signifikan.

## C. Moderate Missingness (`5.0%` s.d. `30.0%`)
* **Kriteria:** Data penting yang tidak bersifat wajib, tetapi masih memiliki bobot informasi tinggi untuk model Machine Learning.
* **Tindakan:**
  * **Group-based Imputation:** `Mengisi data berdasarkan statistik kelompok terkait` (misal: `Impute Age based on Title/Pclass`).
  * **Model-based Imputation:** Menggunakan algoritma `KNN Imputer` atau `Iterative Imputer (MICE)`.

## D. High Missingness (`30.0%` s.d. `50.0%`)
* **Kriteria:** Data opsional di mana ketiadaan data itu sendiri sering kali membawa informasi tersembunyi (*informative missingness*).
* **Tindakan:**
  * **Missing Indicator:** Tambahkan kolom baru (`is_missing`) untuk nilainya biner (`1 = null`, `0 ≠ null`).
  * **Categorical Flag:** `Ubah nilai null` menjadi nilai baru (misal: `Not Specified`).

## E. Extreme Missingness (`> 50.0%`)
* **Kriteria:** Data yang terlalu sedikit diisi sehingga menyuntikkan bias tinggi jika dipaksa di-imputasi.
* **Tindakan:**
  * **Drop Column:** Hapus kolom dari daftar fitur utama jika tidak memiliki urgensi bisnis.
  * **Binary Transformation:** Ubah seluruh kolom menjadi satu fitur penanda sederhana (contoh: `has_cabin` ➡️ `1 = ada data`, `0 = null`).
