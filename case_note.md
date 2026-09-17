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