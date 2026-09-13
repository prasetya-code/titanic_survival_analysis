`Notebook` sebaiknya digunakan untuk `analisis dan eksperimen`, sedangkan proses `mengambil data` adalah bagian dari `data pipeline/reproducibility -> src`.

```bash
customer-churn-project/
├── .github/                   # Workflow CI/CD (GitHub Actions)
│   └── workflows/
│       └── deploy.yml
├── config/                    # Konfigurasi proyek (file YAML/JSON)
│   └── config.yaml            # Parameter model, path data, hyperparameter
├── data/                      # Direktori data (disimpan lokal, di-ignore git)
│   ├── 01_raw/                # Data mentah awal (immutable / jangan diubah)
│   ├── 02_intermediate/       # Data hasil pembersihan awal (cleaned data)
│   ├── 03_primary/            # Data siap pakai / feature engineered
│   └── 04_model_output/       # Hasil prediksi atau output analitis
├── docs/                      # Dokumentasi proyek (API doc, arsitektur data)
├── logs/                      # Log eksekusi pipeline
├── models/                    # Binary model ML terlaris (.pkl, .joblib, atau .onnx)
├── notebooks/                 # Jupyer Notebook untuk eksplorasi (EDA) saja
│   ├── 1.0-eda.ipynb
│   └── 2.0-feature-experimentation.ipynb
├── src/                       # Source code utama (modular Python package)
│   ├── __init__.py
│   ├── data/                  # Script pengambilan & ETL data
│   │   ├── __init__.py
│   │   ├── ingest.py          # Tari data dari SQL/API
│   │   └── clean.py           # Handling missing value, scaling, dll.
│   ├── features/              # Script pembuatan fitur (Feature Engineering)
│   │   ├── __init__.py
│   │   └── build_features.py
│   ├── models/                # Training dan evaluasi model
│   │   ├── __init__.py
│   │   ├── train.py
│   │   └── evaluate.py
│   └── utils/                 # Functions pendukung (helper, logger)
│       ├── __init__.py
│       └── logger.py
├── tests/                     # Unit test & Data Quality Test (Pytest)
│   ├── test_data.py
│   └── test_models.py
├── .gitignore                 # Mengabaikan file data, log, dan .env
├── main.py                    # Entry point eksekusi seluruh pipeline
├── README.md                  # Panduan proyek
└── requirements.txt           # Dependency pustaka Python
```