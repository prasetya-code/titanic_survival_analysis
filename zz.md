# 1. String Quality

String Quality digunakan untuk mengecek **kualitas isi data bertipe string**, bukan hanya apakah tipe datanya `String`.

| No | Validation                    | Yang Diperiksa                                                                      |
| -: | ----------------------------- | ----------------------------------------------------------------------------------- |
|  1 | Leading / Trailing Whitespace | Spasi di awal atau akhir string                                                     |
|  2 | Multiple Spaces               | Spasi berulang di dalam string                                                      |
|  3 | Empty String                  | String kosong atau hanya berisi whitespace                                          |
|  4 | Invalid / Unusual Characters  | Karakter aneh, non-printable, atau karakter yang tidak diharapkan                   |
|  5 | Casing Consistency            | Konsistensi `UPPER`, `lower`, `Title Case`, dll.                                    |
|  6 | Encoding                      | Masalah encoding atau karakter yang rusak                                           |
|  7 | Missing-like String           | Nilai seperti `"null"`, `"N/A"`, `"None"`, `"NaN"` yang seharusnya dianggap missing |
|  8 | Allowed Characters            | Karakter yang diperbolehkan berdasarkan rule/regex                                  |

---

# 2. Baseline Drift (distribusi serta persentase data)

Baseline Drift digunakan untuk membandingkan dataset saat ini dengan dataset baseline untuk mengetahui apakah terdapat perubahan karakteristik data.

| No | Parameter                          | Yang Diperiksa                                                         |
| -: | ---------------------------------- | ---------------------------------------------------------------------- |
|  1 | **Schema Drift**                   | Kolom hilang, kolom baru, perubahan `dtype`, perubahan `semantic_type` |
|  2 | **Volume Drift**                   | Perubahan jumlah baris                                                 |
|  3 | **Completeness Drift**             | Perubahan persentase `NULL` / missing value                            |
|  4 | **Numeric Distribution Drift**     | Perubahan mean, median, std, quantile, dan distribusi numerik          |
|  5 | **Categorical Distribution Drift** | Perubahan proporsi kategori, kategori baru, atau kategori yang hilang  |
|  6 | **String Drift**                   | Perubahan distribusi panjang string dan karakteristik text             |
|  7 | **Duplicate Drift**                | Perubahan persentase duplicate                                         |
|  8 | **Outlier Drift**                  | Perubahan jumlah/persentase outlier                                    |

### Contoh

Baseline:

```text
age mean       = 30
NULL rate      = 5%
duplicate rate = 1%
```

Current:

```text
age mean       = 42
NULL rate      = 18%
duplicate rate = 6%
```

Maka validator dapat menghasilkan:

```text
Numeric Distribution Drift → DRIFT
Completeness Drift         → DRIFT
Duplicate Drift            → DRIFT
```

Metode statistik yang dapat digunakan antara lain:

* PSI (Population Stability Index)
* KS Test
* Jensen-Shannon Divergence
* perubahan mean/median
* perubahan quantile
* perubahan category frequency

---

# 3. Train / Test Relationship

Validasi ini digunakan ketika dataset sudah dibagi menjadi `train` dan `test`.

Tujuannya bukan hanya memastikan PK tidak overlap, tetapi juga memastikan tidak terjadi **data leakage atau contamination** antara train dan test.

| No | Parameter                     | Yang Diperiksa                                                        |
| -: | ----------------------------- | --------------------------------------------------------------------- |
|  1 | **PK Relationship**           | Apakah PK train dan test overlap                                      |
|  2 | **Record Relationship**       | Apakah terdapat record/row yang sama di train dan test                |
|  3 | **Schema Relationship**       | Kesamaan struktur kolom train dan test                                |
|  4 | **Feature Relationship**      | Kesesuaian feature train/test dan keberadaan target                   |
|  5 | **Category Relationship**     | Unseen category atau category yang hanya muncul di salah satu dataset |
|  6 | **Distribution Relationship** | Perbedaan distribusi feature train dan test                           |
|  7 | **Target Relationship**       | Distribusi target / class imbalance jika target tersedia              |
|  8 | **Temporal Relationship**     | Potensi temporal leakage berdasarkan timestamp                        |
|  9 | **Group Relationship**        | Overlap group seperti `customer_id`, `patient_id`, dll.               |

---

## 3.1 PK Relationship

Memastikan primary key tidak terdapat pada kedua dataset.

```text
PK(train) ∩ PK(test) = ∅
```

Contoh:

```text
train:
1, 2, 3, 4, 5

test:
6, 7, 8, 9, 10
```

Hasil:

```text
Overlap = 0
Status  = PASS
```

---

## 3.2 Record Relationship

PK berbeda belum tentu berarti record berbeda.

Contoh:

```text
train:
John Doe | 30 | Male

test:
John Doe | 30 | Male
```

Walaupun PK berbeda, record dapat dianggap sama.

Karena itu dapat digunakan:

```text
row_hash(train) ∩ row_hash(test)
```

untuk mendeteksi kemungkinan contamination.

---

## 3.3 Schema Relationship

Memastikan struktur train dan test konsisten.

Contoh:

```text
train:
age       Float64
sex       String
pclass    Int64

test:
age       Float64
sex       String
pclass    Int64
```

Status:

```text
PASS
```

Jika:

```text
train.age = Float64
test.age  = String
```

maka:

```text
FAIL
```

---

## 3.4 Feature Relationship

Memastikan feature train dan test sesuai.

Contoh:

```text
train:
passengerid
survived
pclass
sex
age
fare

test:
passengerid
pclass
sex
age
fare
```

Jika:

```text
target = survived
```

maka:

```text
survived ∉ test
```

merupakan kondisi yang diharapkan untuk test dataset tanpa label.

---

## 3.5 Category Relationship

Memeriksa perbedaan kategori antara train dan test.

Train:

```text
male
female
```

Test:

```text
male
female
unknown
```

Maka:

```text
unknown
```

merupakan **unseen category** pada train.

Hal ini penting terutama untuk model machine learning yang menggunakan categorical encoding.

---

## 3.6 Distribution Relationship

Membandingkan distribusi feature antara train dan test.

Contoh:

```text
             TRAIN     TEST

age mean      30        55
fare mean     32        80
```

Untuk numerical dapat digunakan:

* Mean
* Median
* Standard deviation
* Quantile
* PSI
* KS Test

Untuk categorical:

* Category frequency
* PSI
* Jensen-Shannon Divergence

---

## 3.7 Target Relationship

Jika target tersedia, periksa distribusi target.

Contoh:

```text
survived

0 = 62%
1 = 38%
```

Yang dapat diperiksa:

* jumlah masing-masing class
* persentase masing-masing class
* class imbalance
* perbedaan distribusi target antara train dan test jika label test tersedia

---

## 3.8 Temporal Relationship

Untuk dataset yang mempunyai timestamp.

Contoh:

```text
train:
2026-01 → 2026-09

test:
2026-10 → 2026-12
```

Untuk time-based split, hubungan tersebut dapat dianggap sesuai.

Validator dapat memeriksa:

```text
max(train.timestamp) < min(test.timestamp)
```

Tujuannya mendeteksi **temporal leakage**.

---

## 3.9 Group Relationship

Digunakan jika terdapat group identifier.

Contoh:

```text
customer_id
patient_id
account_id
device_id
```

Misalnya:

```text
train:
customer_id = A
customer_id = B

test:
customer_id = B
customer_id = C
```

Walaupun record ID berbeda, `customer_id = B` muncul pada kedua dataset.

Validator:

```text
group(train) ∩ group(test) = ∅
```

Jika tidak kosong:

```text
Potential Group Leakage
```

---