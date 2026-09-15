# Model Serialization: Pickle vs. Joblib vs. ONNX

Model serialization adalah proses **menyimpan model machine learning yang sudah dilatih ke dalam sebuah file**, sehingga model tersebut dapat digunakan kembali tanpa harus melakukan training dari awal. Ini sangat penting dalam proses **deployment**, karena model biasanya dilatih sekali kemudian digunakan berkali-kali untuk melakukan inference.


## Why Serialize a Model?

Bayangkan serialization sebagai proses **"membekukan" model yang sudah selesai dilatih**. Misalnya kita memiliki model:

```python
model.fit(X_train, y_train)
```

Setelah training selesai, kita tidak ingin menjalankan proses training setiap kali aplikasi dijalankan.

Dengan serialization:

```bash
Training
   │
   ▼
Trained Model
   │
   ▼
Serialization
   │
   ▼
model.pkl / model.joblib / model.onnx
   │
   ▼
Deployment
   │
   ▼
Load Model → Inference
```

### Keuntungan serialization

* Tidak perlu training ulang.
* Model dapat digunakan dalam aplikasi production.
* Mempercepat startup aplikasi.
* Model dapat dipindahkan ke environment lain.
* Memudahkan versioning model.
* Memisahkan proses **training** dan **inference**.

---

# The Main Contenders

Tiga format yang sering digunakan adalah:

| Format     | Fokus Utama                                  | Python-specific   | Cross-platform    | Cocok untuk                   |
| ---------- | -------------------------------------------- | ----------------- | ----------------- | ----------------------------- |
| **Pickle** | Menyimpan object Python                      | yes               | no                | Python application            |
| **Joblib** | Menyimpan object Python + data numerik besar | yes               | no                | scikit-learn / NumPy          |
| **ONNX**   | Pertukaran dan inference model               | yes               | yes               | Production / interoperability |


## Pickle

`pickle` adalah mekanisme serialization bawaan Python yang dapat menyimpan hampir berbagai macam object Python. Contohnya:

```python
import pickle

# Save the model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

# Load the model
with open("model.pkl", "rb") as f:
    loaded_model = pickle.load(f)
```

Setelah model berhasil dimuat:

```python
prediction = loaded_model.predict(X_test)
```

### Kelebihan Pickle

* Sudah tersedia di Python.
* Sangat mudah digunakan.
* Dapat menyimpan berbagai object Python.
* Cocok untuk aplikasi yang seluruh ecosystem-nya menggunakan Python.

### Kekurangan Pickle

#### 1. Python-specific

Pickle dirancang untuk object Python.

Artinya, file:

```bash
model.pkl
```

tidak dirancang untuk langsung digunakan oleh aplikasi Java, Go, C++, JavaScript, dan sebagainya.

#### 2. Security Risk

**Jangan melakukan `pickle.load()` terhadap file dari sumber yang tidak dipercaya.**

Pickle tidak dirancang sebagai format data yang aman. File pickle berbahaya dapat menyebabkan eksekusi kode ketika di-load.

Contoh yang harus dihindari:

```python
pickle.load(untrusted_file)
```

Gunakan hanya file model yang berasal dari sumber yang benar-benar dipercaya.

#### 3. Compatibility

Pickle dapat bergantung pada:

* versi Python
* versi library
* struktur class
* dependency yang digunakan ketika model dibuat

Contohnya, model yang disimpan dengan versi library tertentu belum tentu dapat di-load dengan baik setelah dependency di-upgrade secara signifikan.


## Joblib

`joblib` merupakan library Python yang banyak digunakan untuk menyimpan model machine learning, terutama model yang menggunakan **NumPy arrays**.

Joblib sangat populer dalam ecosystem **scikit-learn**.

Contoh:

```python
import joblib

# Save the model
joblib.dump(model, "model.joblib")

# Load the model
loaded_model = joblib.load("model.joblib")
```

Kemudian model dapat digunakan:

```python
prediction = loaded_model.predict(X_test)
```

### Kelebihan Joblib

* Sangat nyaman untuk model scikit-learn.
* Dioptimalkan untuk object yang memiliki array numerik besar.
* API sederhana.
* Dapat menggunakan compression.

Contoh:

```python
joblib.dump(model, "model.joblib", compress=3)
```

### Kekurangan Joblib

Joblib **bukan format universal untuk machine learning**.

Seperti Pickle, Joblib tetap sangat terkait dengan Python dan object/library yang digunakan ketika model dibuat.

Selain itu, **Joblib juga tidak boleh dianggap aman untuk membuka file dari sumber yang tidak dipercaya**.

Contoh yang harus dihindari:

```python
joblib.load(untrusted_file)
```


## ONNX

**ONNX (Open Neural Network Exchange)** adalah format terbuka untuk merepresentasikan model machine learning dan deep learning.

Tujuan utamanya berbeda dengan Pickle dan Joblib.

Pickle dan Joblib pada dasarnya menyimpan **Python objects**, sedangkan ONNX berfokus pada representasi model yang dapat digunakan oleh berbagai ecosystem.

Contoh ecosystem yang dapat bekerja dengan ONNX antara lain:

```bash
PyTorch
Scikit-learn
TensorFlow
XGBoost
LightGBM
        │
        ▼
       ONNX
        │
        ▼
 ONNX Runtime
        │
        ├── Python
        ├── C++
        ├── C#
        ├── Java
        └── JavaScript / Web
```

Karena itu ONNX sangat menarik untuk deployment dan interoperability.

### Converting a Model to ONNX

ONNX biasanya membutuhkan proses **conversion/export** dari framework asal.

Misalnya model scikit-learn dapat dikonversi menggunakan library seperti:

```bash
skl2onnx
```

Contoh sederhana:

```python
from skl2onnx import to_onnx

onnx_model = to_onnx(
    model,
    X_train[:1].astype("float32")
)

with open("model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
```

Setelah itu file:

```bash
model.onnx
```

dapat digunakan dengan ONNX Runtime.

### Running an ONNX Model

Untuk melakukan inference:

```python
import numpy as np
import onnxruntime as ort

session = ort.InferenceSession("model.onnx")

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

input_data = X_test.astype(np.float32)

result = session.run(
    [output_name],
    {input_name: input_data}
)

print(result)
```

Perlu diperhatikan bahwa detail input/output dapat berbeda tergantung model yang dikonversi.

Untuk memeriksa input model:

```python
for input_meta in session.get_inputs():
    print(input_meta.name)
    print(input_meta.shape)
    print(input_meta.type)
```

Dan untuk output:

```python
for output_meta in session.get_outputs():
    print(output_meta.name)
    print(output_meta.shape)
    print(output_meta.type)
```

---

# Pickle vs Joblib vs ONNX

## Pickle

Gunakan Pickle ketika:

```bash
Python application
      │
      ▼
Python model
      │
      ▼
Pickle
```

Contoh penggunaan:

* eksperimen lokal
* prototype
* menyimpan object Python
* internal Python application

**Catatan:** hindari Pickle sebagai format pertukaran model lintas bahasa.


## Joblib

Gunakan Joblib ketika:

```bash
scikit-learn
     │
     ▼
NumPy-heavy model
     │
     ▼
Joblib
```

Sangat cocok untuk:

* scikit-learn
* pipeline preprocessing + model
* model dengan array numerik besar
* deployment yang seluruhnya menggunakan Python

Contoh:

```python
from sklearn.pipeline import Pipeline
import joblib

pipeline = Pipeline([
    ("preprocessing", preprocessing),
    ("model", model)
])

pipeline.fit(X_train, y_train)

joblib.dump(
    pipeline,
    "model.joblib"
)
```

Keuntungan pentingnya adalah preprocessing dan model dapat disimpan sebagai satu object.


## ONNX

Gunakan ONNX ketika:

```bash
Training Framework
       │
       ▼
     ONNX
       │
       ▼
ONNX Runtime
       │
       ▼
Production Application
```

ONNX lebih menarik ketika:

* model perlu digunakan di luar Python.
* ingin memisahkan model dari Python runtime.
* membutuhkan interoperability.
* deployment membutuhkan runtime khusus.
* ingin menggunakan model pada berbagai platform.

Namun, **tidak semua model atau seluruh fitur preprocessing dapat dikonversi ke ONNX dengan sempurna**. Compatibility operator dan preprocessing perlu diuji.

---

# Important: Model File ≠ Complete ML Application

Salah satu hal yang sering dilupakan adalah bahwa file model belum tentu berisi seluruh environment yang dibutuhkan untuk menghasilkan prediction yang benar.

Misalnya:

```bash
Raw Data
   │
   ▼
Preprocessing
   │
   ├── Imputation
   ├── Scaling
   ├── Encoding
   └── Feature Selection
   │
   ▼
Model
   │
   ▼
Prediction
```

Jika hanya menyimpan:

```bash
model.pkl
```

tetapi preprocessing tidak disimpan, aplikasi production dapat menghasilkan prediction yang berbeda.

Karena itu, lebih baik menyimpan **pipeline lengkap** jika memungkinkan.

Contoh:

```python
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ("preprocessing", preprocessing),
    ("model", model)
])

pipeline.fit(X_train, y_train)

joblib.dump(
    pipeline,
    "model.joblib"
)
```

Kemudian saat inference:

```python
loaded_pipeline = joblib.load("model.joblib")

prediction = loaded_pipeline.predict(X_test)
```

Dengan pendekatan ini, preprocessing dan model menggunakan konfigurasi yang sama.

---

# Serialization vs Model Format

Penting untuk membedakan:

## Serialization

Tujuannya adalah:

> "Bagaimana saya menyimpan object/model sehingga dapat dimuat kembali?"

Contoh:

```bash
Pickle
Joblib
```

## Model Interchange Format

Tujuannya lebih kepada:

> "Bagaimana saya merepresentasikan model sehingga dapat digunakan oleh ecosystem lain?"

Contoh:

```bash
ONNX
```

Karena itu ketiganya tidak sepenuhnya merupakan alternatif yang identik.

---

# Security Considerations

Ini merupakan bagian yang sangat penting.

## Pickle

```python
pickle.load(file)
```

⚠️ Jangan gunakan pada file yang tidak dipercaya.

## Joblib

```python
joblib.load(file)
```

⚠️ Perlakukan sama seperti Pickle: jangan load file dari sumber yang tidak dipercaya.

## ONNX

ONNX memiliki karakteristik security yang berbeda dari Pickle/Joblib, tetapi file model tetap harus diperlakukan sebagai **untrusted input** jika berasal dari sumber eksternal.

Jangan menganggap format model otomatis aman hanya karena bukan Pickle.

Untuk production:

* gunakan model dari sumber terpercaya.
* validasi artifact sebelum deployment.
* gunakan environment terisolasi jika perlu.
* pin dependency.
* lakukan testing terhadap model sebelum digunakan.

---

# Model Versioning

Jangan hanya memiliki:

```bash
model.pkl
```

Lebih baik gunakan versioning:

```bash
models/
├── model_v1.joblib
├── model_v2.joblib
└── model_v3.joblib
```

Atau:

```bash
models/
└── fraud_detection/
    ├── 1/
    │   └── model.joblib
    ├── 2/
    │   └── model.joblib
    └── 3/
        └── model.joblib
```

Dengan begitu kita dapat mengetahui model mana yang digunakan oleh aplikasi tertentu.

---

# Practical Decision Guide

Gunakan aturan sederhana berikut:

## Pilih Pickle jika:

* hanya menggunakan Python.
* membutuhkan cara paling sederhana untuk serialization.
* sedang melakukan prototype atau eksperimen internal.
* object yang disimpan bukan hanya model ML.

```bash
Python → Pickle
```

## Pilih Joblib jika:

* menggunakan scikit-learn.
* model/pipeline memiliki banyak NumPy arrays.
* inference tetap dilakukan menggunakan Python.

```bash
scikit-learn → Joblib
```

## Pilih ONNX jika:

* membutuhkan interoperability.
* model perlu digunakan di luar Python.
* ingin menggunakan ONNX Runtime.
* deployment membutuhkan runtime yang lebih portable.

```bash
Cross-platform / Interoperability → ONNX
```