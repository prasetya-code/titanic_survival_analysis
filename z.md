```py
MISSING_VALUES = ["", "NA", "N/A", "na", "n/a", "N/a"]
```

# string validity hanya melakukan:
- cek leading / trailing space
- cek multiple space
- cek casing (Bagaimana bentuk hurufnya)
| Nilai `casing` | Contoh                             | Penjelasan                   |
| -------------- | ---------------------------------- | ---------------------------- |
| `lower`        | `john doe`                         | Semua huruf kecil            |
| `upper`        | `JOHN DOE`                         | Semua huruf besar            |
| `title`        | `John Doe`                         | Awal setiap kata huruf besar |
| `sentence`     | `John doe`                         | Awal kalimat huruf besar     |

- cek invalid character (disesuaikan dengan parameter kolom)
| Nilai         | Karakter bermasalah | Invalid Character  | Penjelasan                                             |
| ------------- | ------------------- | ------------------ | ------------------------------------------------------ |
| `John Doe`    | Tidak ada           | ✅ PASS             | Semua karakter normal                                  |
| `John-Doe`    | `-`                 | ✅ PASS             | `-` masih karakter umum                                |
| `John_Doe`    | `_`                 | ✅ PASS             | `_` masih valid jika aturan mengizinkan                |
| `John@Doe`    | `@`                 | ⚠️ Tergantung rule | Bisa valid untuk email, tetapi bisa invalid untuk nama |
| `John#123`    | `#`                 | ⚠️ Tergantung rule | Harus ditentukan oleh `allowed_pattern`                |
| `John\x00Doe` | `\x00`              | ❌ FAIL             | Karakter kontrol/non-printable                         |
| `John\x01Doe` | `\x01`              | ❌ FAIL             | Karakter kontrol/non-printable                         |
| `John\tDoe`   | Tab                 | ⚠️ Tergantung rule | Bisa dianggap tidak valid                              |
| `John\nDoe`   | Newline             | ⚠️ Tergantung rule | Bisa dianggap tidak valid                              |

- cek encoding violation string
| Teks yang seharusnya         | Teks yang terbaca    | Encoding Violation      | Penjelasan                                                |
| ---------------------------- | -------------------- | ----------------------- | --------------------------------------------------------- |
| `John`                       | `John`               | ✅ PASS                  | ASCII/UTF-8 normal                                        |
| `José`                       | `José`               | ✅ PASS                  | UTF-8 dapat menyimpan `é`                                 |
| `Müller`                     | `Müller`             | ✅ PASS                  | `ü` valid UTF-8                                           |
| `François`                   | `François`           | ✅ PASS                  | `ç` valid UTF-8                                           |
| `東京`                         | `東京`                 | ✅ PASS                  | Karakter Jepang valid UTF-8                               |
| `你好`                         | `你好`                 | ✅ PASS                  | Karakter Mandarin valid UTF-8                             |
| `JosÃ©`                      | `JosÃ©`              | ⚠️ Indikasi masalah     | Kemungkinan **mojibake**, yaitu teks sudah salah didekode |
| `Jos�`                       | `Jos�`               | ❌ FAIL / indikasi rusak | `�` adalah replacement character                          |
| `M�ller`                     | `M�ller`             | ❌ FAIL / indikasi rusak | Karakter asli kemungkinan sudah hilang                    |
| File tidak bisa dibaca UTF-8 | `UnicodeDecodeError` | ❌ FAIL                  | File menggunakan encoding lain/rusak                      |


# NOTE

| Directory   | Fungsi                         | Contoh              |
| ----------- | ------------------------------ | ------------------- |
| `data/`     | Menyimpan data                 | `train.csv`         |
| `metadata/` | Definisi/kontrak data          | `schema.json`       |
| `baseline/` | Profil statistik sebagai acuan | `profile.json`      |
| `reports/`  | Hasil analisis/validasi        | `drift_report.json` |
| `src/`      | Source code                    | `profiling.py`      |
