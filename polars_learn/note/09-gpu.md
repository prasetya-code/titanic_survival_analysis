# Apa itu GPU Engine?

Polars memiliki GPU-accelerated execution engine untuk Python Lazy API menggunakan `RAPIDS cuDF pada NVIDIA GPU`. GPU support masih berkembang, sehingga tidak semua query selalu cocok untuk GPU.

---

# Kapan GPU Digunakan?

GPU dapat membantu ketika:

```bash
dataset besar
+
operasi computationally intensive
+
GPU cukup kuat
+
query cocok dengan GPU engine
```

---

# Install

Umumnya:

```bash
pip install "polars[gpu]"
```

Untuk environment CUDA tertentu, gunakan paket GPU yang sesuai dengan dokumentasi resmi Polars/cuDF, berikut list dokumentasinya:
1. [NVIDIA cuDF - Polars GPU Engine Documentation](https://docs.nvidia.com/cudf/latest/cudf_polars/)
2. [Polars User Guide - GPU Support](https://docs.pola.rs/user-guide/gpu-support/)
3. [NVIDIA cuDF API Reference for Polars](https://docs.nvidia.com/cudf/latest/cudf_polars/api/)

---

# GPU Query

Gunakan LazyFrame:

```python
query = (
    pl.scan_parquet(
        "data.parquet"
    )
    .filter(
        pl.col("age") >= 18
    )
)
```

Kemudian:

```python
result = query.collect(
    engine="gpu"
)
```

---

# GPU Bukan Otomatis Lebih Cepat

Contoh:

```bash
CPU:
read → process → output

GPU:
read
 ↓
transfer
 ↓
GPU process
 ↓
transfer
 ↓
CPU output
```

Transfer data dapat menjadi overhead.

---

# GPU Fallback

Jika operasi tidak didukung GPU, Polars dapat melakukan fallback ke CPU pada kondisi tertentu.

Untuk mendeteksi masalah secara ketat:

```python
df = query.collect(
    engine=pl.GPUEngine(
        raise_on_fail=True
    )
)
```

---

# Verbose

Untuk melihat informasi eksekusi:

```python
with pl.Config() as cfg:
    cfg.set_verbose(True)

    df = query.collect(
        engine="gpu"
    )
```

---

# GPU vs RAM

Perhatikan:

```bash
RAM
≠
VRAM
```

GPU memiliki memory sendiri.

Ukuran DataFrame final juga tidak sama dengan peak VRAM yang digunakan selama query.

---

# Hybrid

Untuk workload besar:

```bash
CPU
 ↓
read
 ↓
filter
 ↓
partition
 ↓
GPU
 ↓
heavy computation
 ↓
CPU
 ↓
output
```

Tujuannya adalah meminimalkan transfer CPU ↔ GPU.

---

# Prioritas Optimasi

Jangan langsung membeli GPU.

Urutan yang lebih baik:

```bash
1. Query benar
2. Lazy
3. Parquet
4. Filter
5. Select
6. Memory
7. Streaming
8. Partitioning
9. Benchmark
10. GPU
```

GPU adalah optimasi, bukan pengganti desain data yang buruk.