# Masalah Umum

Jangan melakukan:

```bash
Database
 ↓
SELECT *
 ↓
seluruh table
 ↓
Polars
```

Jika database memiliki:

```bash
500 juta rows
```

cara tersebut dapat menyebabkan masalah memory dan network.

---

# Filter di Database

Lebih baik:

```sql
SELECT
    id,
    user_id,
    quantity,
    price
FROM transactions
WHERE id > ...
```

Database mengurangi data sebelum dikirim ke Polars.

---

# Select Kolom yang Dibutuhkan

Hindari:

```sql
SELECT *
```

Gunakan:

```sql
SELECT
    id,
    user_id,
    quantity,
    price
```

---

# Batch Processing

Gunakan batch:

```bash
Database
 ↓
1 juta rows
 ↓
Polars
 ↓
process
 ↓
save
 ↓
1 juta rows berikutnya
```

---

# Keyset Pagination

Contoh:

```sql
WHERE id > last_id
ORDER BY id
LIMIT 1000000
```

Biasanya lebih cocok untuk dataset besar daripada OFFSET yang sangat besar.

---

# Pipeline

```bash
Database
   ↓
SQL Filter
   ↓
Batch
   ↓
Polars
   ↓
Transform
   ↓
Parquet
```

---

# Jangan Simpan Semua Batch

Kurang baik:

```python
all_batches = []

while True:
    df = ...
    all_batches.append(df)
```

Karena akhirnya semua batch tetap berada di memory.

Lebih baik:

```python
while True:
    df = ...

    process(df)

    save(df)
```

---

# Database sebagai Source

Database sebaiknya digunakan sebagai source terkontrol:

```bash
Database
   ↓
filter
   ↓
batch
   ↓
Polars
   ↓
Parquet
```

Setelah itu analisis besar dapat dilakukan dari Parquet.