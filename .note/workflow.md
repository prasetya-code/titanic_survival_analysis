# End-to-End Data Analytics & Machine Learning Workflow

```bash
┌─────────────────────────────────────────────┐
│ 1. BUSINESS PROBLEM                         │
│ Objective • Questions • Success Criteria    │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 2. DATA UNDERSTANDING                       │
│ Source • Schema • Data Dictionary           │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 3. DATA QUALITY                             │
│ Missing • Duplicate • Validity • Outlier    │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 4. DATA PREPARATION                         │
│ Types • Cleaning • Encoding • Preprocessing │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 5. EDA                                      │
│ Distribution • Pattern • Relationship       │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 6. HYPOTHESIS                               │
│ What factors appear related to outcome?     │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 7. BASELINE                                 │
│ Establish simple benchmark                  │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 8. FEATURE ENGINEERING                      │
│ Raw Data → Analytical Features              │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 9. LEAKAGE + FEATURE VALIDATION             │
│ Leakage • Redundancy • Stability             │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 10. MODEL BENCHMARK                         │
│ Logistic • Tree • RF • GB • Ensemble        │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 11. MODEL EVALUATION                        │
│ Accuracy • Precision • Recall • F1 • AUC    │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 12. CROSS VALIDATION                        │
│ Generalization • Variance • Stability       │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 13. OPTIMIZATION                            │
│ Hyperparameter Tuning                       │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 14. EXPERIMENT TRACKING                     │
│ Model • Features • Parameters • Metrics     │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 15. EXPLAINABILITY                          │
│ Importance • Permutation • SHAP             │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 16. ERROR ANALYSIS                          │
│ FP • FN • Segment • Failure Pattern         │
└──────────────────────┬──────────────────────┘
                       ↓
                ┌─────────────────┐
                │ NEW HYPOTHESIS  │
                └────────┬────────┘
                         │
                         └──────────→ Feature Engineering
                         ↓
┌─────────────────────────────────────────────┐
│ 17. FINAL MODEL SELECTION                   │
│ Performance • Stability • Interpretability  │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 18. KAGGLE / HOLDOUT VALIDATION             │
│ External Benchmark / Final Evaluation       │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 19. BUSINESS INSIGHT                        │
│ Findings • Drivers • "So What?"             │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 20. LIMITATIONS & RISK                      │
│ Data • Model • Generalization • Bias        │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 21. EXECUTIVE REPORT                        │
│ Decision-Oriented Summary                   │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ 22. DASHBOARD + GITHUB                      │
│ Reproducibility • Documentation • Portfolio │
└─────────────────────────────────────────────┘
```

---

# Layer 1 — Business Framing

## Business Problem

### Tujuan

Menentukan masalah yang sebenarnya ingin dijawab oleh project.

Untuk Titanic:

> What factors are associated with passenger survival, and how accurately can survival be predicted using available passenger information?

### Mengapa harus dilakukan?

Karena `project data seharusnya dimulai dari pertanyaan, bukan dari algoritma`.

Tanpa business problem yang jelas, analisis mudah berubah menjadi:

```bash
Load data
↓
EDA
↓
Train Random Forest
↓
Accuracy
↓
Done
```

Masalahnya adalah kita tidak mengetahui:

* mengapa model dibuat,
* apa yang ingin diketahui,
* apa yang dianggap berhasil,
* dan apa arti hasil model.

Senior Data Specialist harus mampu menjelaskan:

> "Masalah apa yang sedang saya selesaikan?"

sebelum menjelaskan:

> "Model apa yang saya gunakan?"

### Pertanyaan yang harus dijawab

* Apa objective project?
* Siapa stakeholder-nya?
* Apa target/outcome?
* Apa keputusan yang ingin didukung?
* Apa batasan project?
* Apa success criteria?

### Output

```bash
Business Objective
Business Questions
Target Definition
Success Criteria
Scope
Constraints
```

---

# 4. Business Questions

Business problem kemudian diterjemahkan menjadi pertanyaan analitis.

Contoh:

### Descriptive

* Berapa survival rate keseluruhan?
* Bagaimana survival berdasarkan gender?
* Bagaimana survival berdasarkan passenger class?

### Diagnostic

* Mengapa survival rate berbeda antar-class?
* Apakah family size berkaitan dengan survival?
* Apakah age dan passenger class berinteraksi?

### Predictive

* Seberapa akurat survival dapat diprediksi?
* Feature apa yang paling berkontribusi terhadap prediction?

### Business-oriented

* Segmentasi passenger seperti apa yang menunjukkan perbedaan survival?
* Di segment mana model paling sering melakukan kesalahan?

### Mengapa harus dipisahkan?

Karena:

```bash
Business Problem
      ↓
Business Question
      ↓
Analytical Question
      ↓
Modeling Question
```

membuat setiap tahap memiliki tujuan yang jelas.

---

# 5. Success Criteria

Success criteria harus didefinisikan sebelum model dibuat.

Contoh:

```bash
Primary:
- Robust validation performance

Secondary:
- Model stability
- Interpretability
- Reproducibility
- Meaningful business insights
```

Jangan mendefinisikan keberhasilan hanya sebagai:

```bash
Accuracy > X
```

karena model dengan accuracy tinggi belum tentu:

* stabil,
* dapat dijelaskan,
* bebas leakage,
* atau menghasilkan insight yang berguna.

---

# 6. Layer 2 — Data Understanding

## 6.1 Data Source

Identifikasi:

* sumber data,
* file,
* origin,
* periode,
* format,
* unit observasi.

Contoh:

```bash
Source:
Kaggle Titanic Dataset

Unit of Observation:
One row = one passenger
```

### Mengapa harus dilakukan?

Karena kesalahan memahami unit observasi dapat menyebabkan kesalahan analisis.

Misalnya kita mengira:

```bash
1 row = 1 ticket
```

padahal:

```bash
1 row = 1 passenger
```

Interpretasi seluruh analisis kemudian dapat menjadi salah.

---

# 7. Schema

Dokumentasikan:

* column name,
* data type,
* semantic meaning,
* role,
* expected range.

Contoh:

| Column      | Type        | Meaning                 | Role    |
| ----------- | ----------- | ----------------------- | ------- |
| PassengerId | Integer     | Passenger identifier    | ID      |
| Survived    | Integer     | Survival outcome        | Target  |
| Pclass      | Integer     | Passenger class         | Feature |
| Sex         | Categorical | Passenger sex           | Feature |
| Age         | Numeric     | Passenger age           | Feature |
| SibSp       | Integer     | Siblings/spouses aboard | Feature |
| Parch       | Integer     | Parents/children aboard | Feature |
| Fare        | Numeric     | Passenger fare          | Feature |
| Cabin       | Categorical | Cabin information       | Feature |
| Embarked    | Categorical | Port of embarkation     | Feature |

### Mengapa penting?

Karena:

> **Data type secara teknis belum tentu sama dengan semantic type.**

Contoh:

```bash
Pclass = integer
```

secara teknis numeric.

Tetapi secara bisnis:

```bash
Pclass = categorical/ordinal concept
```

Pemahaman ini mempengaruhi EDA dan modeling.

---

# 8. Data Dictionary

Setiap feature sebaiknya mempunyai definisi.

Contoh:

```bash
SibSp:
Number of siblings/spouses aboard the Titanic.

Parch:
Number of parents/children aboard.

Fare:
Passenger fare.
```

### Mengapa harus dilakukan?

Karena feature engineering yang baik membutuhkan pemahaman terhadap **makna data**, bukan hanya nama kolom.

---

# 9. Layer 3 — Data Quality

## 9.1 Missing Values

Periksa:

* jumlah missing,
* persentase missing,
* pattern missing,
* missing berdasarkan segment.

Contoh:

```bash
Age → missing
Cabin → banyak missing
Embarked → sedikit missing
```

### Mengapa?

Karena missing value bukan hanya masalah teknis.

Missing dapat mengandung informasi.

Contohnya:

```bash
Cabin missing
```

mungkin tidak random.

Karena itu jangan langsung:

```python
df.fillna(...)
```

tanpa memahami pola missing terlebih dahulu.

---

# 10. Duplicate

Periksa:

```bash
Exact duplicates
Duplicate passenger ID
Duplicate ticket
```

### Mengapa?

Duplicate dapat menyebabkan:

* bias distribusi,
* inflated sample size,
* data leakage,
* incorrect statistics.

Namun duplicate secara bisnis tidak selalu berarti error.

Contoh:

```bash
Ticket number sama
```

bisa valid karena beberapa passenger menggunakan ticket yang sama.

Jadi:

> **Duplicate harus dianalisis berdasarkan semantic meaning.**

---

# 11. Validity

Periksa apakah nilai masuk akal.

Contoh:

```bash
Age < 0
Fare < 0
Pclass not in expected categories
Invalid Embarked values
Invalid Sex categories
```

### Mengapa?

Karena model tidak mengetahui apakah data masuk akal.

Model hanya melihat angka.

---

# 12. Outlier

Outlier harus diidentifikasi, bukan otomatis dihapus.

Contoh:

```bash
Fare sangat tinggi
FamilySize sangat besar
Age sangat tinggi
```

### Mengapa tidak langsung dihapus?

Karena:

```bash
Outlier ≠ Error
```

Outlier dapat merupakan:

* data entry error,
* rare event,
* legitimate observation.

Keputusan treatment harus berdasarkan konteks.

---

# 13. Data Quality Summary

Output akhir:

```bash
Data Quality Report
├── Missing Values
├── Duplicate
├── Invalid Values
├── Outliers
├── Data Type Issues
└── Quality Decision
```

Setiap masalah harus mempunyai:

```bash
Problem
→ Evidence
→ Decision
→ Reason
```

Ini jauh lebih baik daripada hanya:

```bash
df.isnull().sum()
```

---

# 14. Layer 4 — Data Preparation

Data Quality menjawab:

> "Apa yang salah dengan data?"

Data Preparation menjawab:

> "Bagaimana data dibuat siap digunakan?"

Tahap ini dapat mencakup:

* data type conversion,
* standardisasi kategori,
* missing-value treatment,
* encoding,
* preprocessing,
* train/validation split,
* pipeline preparation.

---

# 15. Mengapa Data Preparation harus terpisah?

Karena:

```bash
Quality Check
```

dan:

```bash
Transformation
```

adalah dua aktivitas berbeda.

Contoh:

```bash
Cabin memiliki missing value
```

adalah **quality finding**.

Sedangkan:

```bash
Cabin → Deck
Deck missing → Unknown
```

adalah **data preparation / feature engineering decision**.

Pemisahan ini membuat audit trail lebih jelas.

---

# 16. Train / Validation / Test Strategy

Sebelum modeling, tentukan bagaimana data akan dibagi.

Contoh konsep:

```bash
Training Data
      ↓
Cross Validation
      ↓
Model Selection
      ↓
Final Holdout / Test
```

### Mengapa?

Karena model tidak boleh dinilai menggunakan data yang telah digunakan secara tidak tepat untuk memilih model.

Tujuannya:

> mengukur kemampuan generalisasi, bukan kemampuan mengingat data.

---

# 17. Layer 5 — Exploratory Data Analysis

EDA bertujuan memahami:

* distribusi,
* relationship,
* pattern,
* segment,
* anomaly,
* interaction.

EDA bukan sekadar membuat banyak grafik.

Pertanyaan utama:

> **Apa yang dapat kita pelajari dari data sebelum modeling?**

---

# 18. Univariate Analysis

Analisis satu variable.

Contoh:

```bash
Age distribution
Fare distribution
Sex distribution
Pclass distribution
```

### Mengapa?

Untuk memahami:

* central tendency,
* spread,
* skewness,
* imbalance,
* category frequency.

---

# 19. Bivariate Analysis

Menganalisis relationship antara feature dan target.

Contoh:

```bash
Survival vs Sex
Survival vs Pclass
Survival vs Age
Survival vs Fare
```

### Mengapa?

Untuk menemukan pattern awal.

Misalnya:

```bash
Survival rate berbeda antar passenger class.
```

Namun:

> Relationship ≠ causation.

Karena itu hasil EDA harus digunakan untuk membangun hypothesis, bukan langsung dianggap sebagai causal conclusion.

---

# 20. Multivariate Analysis

Analisis beberapa feature secara bersamaan.

Contoh:

```bash
Sex × Pclass → Survival
Age × Pclass → Survival
FamilySize × Sex → Survival
```

### Mengapa?

Karena relationship sederhana dapat berubah ketika feature lain diperhitungkan.

Misalnya:

```bash
Sex → Survival
```

belum tentu menjelaskan seluruh pattern.

Bisa terdapat interaction:

```bash
Sex × Pclass
```

---

# 21. Segment Analysis

Analisis survival berdasarkan kelompok.

Contoh:

```bash
Sex
Pclass
Age Group
Family Size
Embarked
Deck
```

Tujuannya:

> menemukan segment yang mempunyai behavior berbeda.

Ini nantinya sangat berguna untuk:

* hypothesis,
* feature engineering,
* error analysis,
* business insight.

---

# 22. EDA Output

EDA sebaiknya menghasilkan:

```bash
EDA Findings
├── Distribution Findings
├── Relationship Findings
├── Segment Findings
├── Interaction Findings
├── Anomalies
└── Candidate Hypotheses
```

Bukan:

```bash
50 charts
```

---

# 23. Layer 6 — Hypothesis

Hypothesis mengubah observation menjadi sesuatu yang dapat diuji.

Contoh:

### Observation

```bash
Female passengers appear to have higher survival rates.
```

### Hypothesis

```bash
H1:
Sex is associated with survival outcome.
```

Contoh lain:

```bash
Passengers in higher classes appear to have different survival rates.
```

menjadi:

```bash
H2:
Passenger class is associated with survival.
```

---

# 24. Mengapa Hypothesis penting?

Karena tanpa hypothesis:

```bash
EDA → Random Feature Engineering
```

Dengan hypothesis:

```bash
EDA
 ↓
Observation
 ↓
Hypothesis
 ↓
Feature
 ↓
Experiment
```

Ini menunjukkan analytical reasoning.

---

# 25. Hypothesis Register

Dokumentasikan:

| ID  | Observation                 | Hypothesis                                    | Test               |
| --- | --------------------------- | --------------------------------------------- | ------------------ |
| H01 | Survival differs by sex     | Sex is associated with survival               | Group comparison   |
| H02 | Survival differs by class   | Pclass is associated with survival            | Segment analysis   |
| H03 | Family structure may matter | Family size may relate to survival            | Feature experiment |
| H04 | Cabin information varies    | Cabin/deck may provide predictive information | Feature experiment |

---

# 26. Layer 7 — Baseline

Baseline adalah model atau rule sederhana yang menjadi benchmark.

Contoh:

```bash
Majority Class Baseline
```

atau:

```bash
Simple Logistic Regression
```

### Mengapa baseline penting?

Karena kita harus mengetahui:

> "Apakah model yang kompleks benar-benar memberikan improvement?"

Misalnya:

```bash
Baseline = 78%
Random Forest = 81%
```

Sekarang kita mengetahui improvement.

Tanpa baseline:

```bash
Random Forest = 81%
```

tidak memiliki konteks.

---

# 27. Layer 8 — Feature Engineering

Feature engineering mengubah:

```bash
Raw Data
```

menjadi:

```bash
Analytical Representation
```

Contoh Titanic:

```bash
SibSp + Parch
        ↓
FamilySize
```

```bash
FamilySize
        ↓
IsAlone
```

```bash
Name
        ↓
Title
```

```bash
Cabin
        ↓
Deck
```

```bash
Fare + Ticket
        ↓
FarePerPerson
```

---

# 28. Mengapa Feature Engineering penting?

Karena raw data belum tentu merepresentasikan konsep yang relevan bagi model.

Contoh:

```bash
SibSp = 2
Parch = 1
```

lebih sulit diinterpretasikan dibanding:

```bash
FamilySize = 4
```

Feature engineering dapat:

* meningkatkan signal,
* mengurangi noise,
* meningkatkan interpretability,
* membantu model menangkap domain pattern.

---

# 29. Feature Engineering harus berbasis reasoning

Jangan membuat feature hanya karena:

> "Feature ini meningkatkan Kaggle score."

Lebih baik:

```bash
Observation
↓
Business/domain reasoning
↓
Hypothesis
↓
Feature
↓
Experiment
```

Dengan demikian feature mempunyai alasan yang dapat dipertanggungjawabkan.

---

# 30. Layer 9 — Leakage & Feature Validation

Ini merupakan salah satu tahap paling penting.

## Data Leakage

Data leakage terjadi ketika informasi yang seharusnya tidak tersedia pada prediction time masuk ke model.

Contoh konsep:

```bash
Information available AFTER outcome
              ↓
        accidentally used
              ↓
             Model
```

Model dapat terlihat sangat bagus tetapi gagal pada data nyata.

---

# 31. Feature Validation

Setiap feature perlu diperiksa:

```bash
Is it available at prediction time?
Is it derived correctly?
Does it contain target information?
Is it redundant?
Is it stable?
Does it make semantic sense?
```

### Mengapa?

Feature engineering bukan hanya soal menghasilkan banyak feature.

Tujuannya adalah menghasilkan:

> **valid analytical features.**

---

# 32. Layer 10 — Model Benchmark

Gunakan beberapa model dengan karakteristik berbeda.

Contoh:

```bash
Logistic Regression
Decision Tree
Random Forest
Gradient Boosting
Ensemble
```

### Mengapa?

Karena setiap model memiliki:

* asumsi,
* bias,
* variance,
* interpretability,
* kemampuan menangkap nonlinear relationship

yang berbeda.

---

# 33. Jangan langsung menggunakan model paling kompleks

Urutan yang lebih sehat:

```bash
Baseline
   ↓
Simple Model
   ↓
Tree Model
   ↓
Ensemble
   ↓
Optimization
```

Tujuannya bukan selalu mendapatkan model paling kompleks.

Tujuannya:

> menemukan trade-off yang sesuai antara performance, stability, dan interpretability.

---

# 34. Layer 11 — Model Evaluation

Gunakan metric yang relevan.

Contoh:

```bash
Accuracy
Precision
Recall
F1
ROC-AUC
Confusion Matrix
```

### Mengapa?

Satu metric tidak selalu memberikan gambaran lengkap.

Contoh:

```bash
Accuracy tinggi
```

belum tentu berarti:

```bash
Recall tinggi
```

atau:

```bash
FP/FN rendah
```

---

# 35. Confusion Matrix

Untuk binary classification:

```bash
                Predicted
              0         1

Actual 0     TN        FP

Actual 1     FN        TP
```

Analisis ini membantu menjawab:

* berapa positive yang terlewat?
* berapa negative yang salah diprediksi?
* jenis kesalahan mana yang lebih sering?

---

# 36. Layer 12 — Cross Validation

Cross-validation digunakan untuk mengukur performa model pada beberapa pembagian data.

Contoh:

```bash
Fold 1
Fold 2
Fold 3
Fold 4
Fold 5
```

Kemudian:

```bash
Mean CV Score
CV Standard Deviation
```

### Mengapa?

Karena satu train/test split dapat memberikan hasil yang kebetulan bagus atau buruk.

Cross-validation memberikan gambaran lebih baik tentang:

> **stability dan generalization.**

---

# 37. Jangan hanya melihat Mean Score

Contoh:

```bash
Model A
Mean = 0.82
Std = 0.01
```

dan:

```bash
Model B
Mean = 0.83
Std = 0.08
```

Kedua model tidak hanya berbeda dalam average performance.

Model juga berbeda dalam stability.

Karena itu dokumentasikan:

```bash
Mean
Std
Min
Max
```

---

# 38. Layer 13 — Optimization

Setelah model benchmark selesai, lakukan hyperparameter tuning.

Contoh:

```bash
Random Forest
├── n_estimators
├── max_depth
├── min_samples_split
└── max_features
```

### Mengapa optimization dilakukan setelah benchmarking?

Karena tuning semua model sejak awal:

* mahal,
* tidak efisien,
* sulit dibandingkan,
* meningkatkan experiment complexity.

Lebih baik:

```bash
Benchmark
 ↓
Identify promising candidates
 ↓
Tune selected models
```

---

# 39. Layer 14 — Experiment Tracking

Setiap eksperimen harus dapat dilacak.

Contoh:

| ID      | Model    | Features   | CV Mean | CV Std | Parameters |
| ------- | -------- | ---------- | ------: | -----: | ---------- |
| EXP-001 | Logistic | Raw        |    0.79 |   0.02 | Default    |
| EXP-002 | Logistic | Engineered |    0.81 |   0.02 | Default    |
| EXP-003 | RF       | Engineered |    0.82 |   0.03 | Default    |
| EXP-004 | RF       | Engineered |    0.83 |   0.02 | Tuned      |

### Mengapa?

Karena tanpa experiment tracking kita mudah kehilangan:

* model mana yang digunakan,
* feature set mana,
* parameter mana,
* hasil eksperimen sebelumnya.

Senior workflow harus reproducible.

---

# 40. Layer 15 — Explainability

Model harus dapat dijelaskan.

Gunakan:

```bash
Global Feature Importance
Permutation Importance
SHAP
```

---

# 41. Global Feature Importance

Menjawab:

> Feature apa yang paling banyak digunakan oleh model?

Namun feature importance model-specific harus diinterpretasikan dengan hati-hati.

---

# 42. Permutation Importance

Menjawab:

> Seberapa besar performa model berubah ketika informasi sebuah feature diacak?

Ini memberikan perspektif yang berbeda terhadap importance.

---

# 43. SHAP

SHAP dapat digunakan untuk memahami:

```bash
Global explanation
Local explanation
```

Pertanyaan yang dapat dijawab:

> Feature apa yang mendorong prediction tertentu?

Namun SHAP bukan bukti causal relationship.

---

# 44. Hubungkan Explainability dengan EDA

Ini bagian yang sangat penting.

Bandingkan:

```bash
EDA Finding
      ↕
Model Explanation
```

Misalnya:

```bash
EDA:
Pclass memiliki relationship dengan survival.

Model:
Pclass memiliki kontribusi besar terhadap prediction.
```

Jika keduanya konsisten, kita mendapatkan analytical narrative yang lebih kuat.

---

# 45. Layer 16 — Error Analysis

Jangan berhenti di:

```bash
Accuracy = X%
```

Tanyakan:

> "Di mana model gagal?"

Analisis:

```bash
False Positive
False Negative
```

Kemudian segmentasikan:

```bash
Sex
Pclass
Age
FamilySize
Fare
Embarked
```

---

# 46. Mengapa Error Analysis penting?

Karena aggregate metric menyembunyikan failure pattern.

Contoh:

```bash
Overall Accuracy = 82%
```

tidak memberitahu:

```bash
Model gagal lebih sering pada:
- passenger tertentu,
- age group tertentu,
- family segment tertentu.
```

Error analysis dapat menghasilkan insight baru.

---

# 47. Iteration Loop

Error analysis dapat menghasilkan:

```bash
New Observation
       ↓
New Hypothesis
       ↓
New Feature
       ↓
New Experiment
       ↓
New Validation
```

Karena itu workflow sebenarnya bukan linear.

Model development bersifat iterative.

```bash
EDA
 ↓
Hypothesis
 ↓
Feature Engineering
 ↓
Model
 ↓
Validation
 ↓
Error Analysis
 ↓
New Hypothesis
 ↓
Feature Engineering
```

Iteration berhenti ketika improvement sudah tidak memberikan manfaat yang berarti atau project telah mencapai success criteria.

---

# 48. Layer 17 — Final Model Selection

Model final tidak seharusnya dipilih hanya berdasarkan score tertinggi.

Pertimbangkan:

```bash
Performance
Stability
Generalization
Interpretability
Complexity
Reproducibility
```

Tujuannya adalah memilih model yang sesuai dengan tujuan project.

Bukan sekadar model dengan satu angka score tertinggi.

---

# 49. Layer 18 — Kaggle / Holdout Validation

Kaggle dapat digunakan sebagai:

```bash
External Benchmark
```

bukan sebagai satu-satunya validasi.

Flow:

```bash
Training
 ↓
Cross Validation
 ↓
Model Selection
 ↓
Final Model
 ↓
Kaggle / Holdout
```

### Mengapa?

Karena leaderboard merupakan benchmark eksternal.

Ia membantu mengetahui apakah model yang dibangun juga bekerja pada hidden evaluation set.

Namun:

> Kaggle score tidak menggantikan analytical validation.

---

# 50. Layer 19 — Business Insight

Setelah modeling selesai, kembali ke business question.

Pertanyaan utama:

> **So What?**

Contoh struktur:

```bash
Finding
↓
Evidence
↓
Interpretation
↓
Business Meaning
```

Jangan hanya menulis:

```bash
Pclass is important.
```

Lebih baik:

```bash
Finding:
Passenger class is strongly associated with survival
in the observed dataset.

Evidence:
Survival rates differ across passenger classes.

Model:
Pclass contributes materially to model prediction.

Implication:
Passenger class appears to capture meaningful
differences in survival patterns within this dataset.
```

---

# 51. Hindari Causal Overclaim

Jika data hanya menunjukkan association:

Jangan mengatakan:

```bash
Pclass caused survival.
```

Lebih tepat:

```bash
Pclass is associated with survival.
```

atau:

```bash
The model uses Pclass as an important predictive feature.
```

Ini menunjukkan statistical discipline.

---

# 52. Layer 20 — Limitations & Risk

Setiap analytical project harus memiliki limitation section.

Contoh:

```bash
Data limitations
Model limitations
Sample limitations
Feature limitations
Generalization limitations
Potential bias
```

---

# 53. Mengapa limitation penting?

Karena hasil model tidak berlaku secara universal.

Contoh:

```bash
Titanic dataset
```

tidak otomatis berarti:

```bash
The same survival patterns apply to every maritime disaster.
```

Kesimpulan harus dibatasi pada:

```bash
population
dataset
time/context
prediction setting
```

yang memang didukung data.

---

# 54. Layer 21 — Executive Report

Executive report harus menjawab:

```bash
1. What happened?
2. What did we find?
3. What drives the prediction?
4. Where does the model fail?
5. What are the limitations?
6. What should stakeholders understand?
```

Report sebaiknya tidak dimulai dari:

```bash
Random Forest parameters
```

Tetapi dari:

```bash
Business question
↓
Key findings
↓
Evidence
↓
Implications
↓
Limitations
```

---

# 55. Layer 22 — Dashboard + GitHub

Final delivery terdiri dari:

```bash
GitHub
Dashboard
Report
Documentation
Model artifacts
```

---

# 56. GitHub Structure

Contoh:

```bash
titanic-survival-analysis/
│
├── README.md
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
│
├── notebooks/
│   ├── 01_business_problem.ipynb
│   ├── 02_data_understanding.ipynb
│   ├── 03_data_quality.ipynb
│   ├── 04_eda.ipynb
│   ├── 05_feature_engineering.ipynb
│   ├── 06_baseline.ipynb
│   ├── 07_model_benchmark.ipynb
│   ├── 08_validation.ipynb
│   ├── 09_optimization.ipynb
│   ├── 10_explainability.ipynb
│   ├── 11_error_analysis.ipynb
│   └── 12_final_insight.ipynb
│
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   └── evaluation/
│
├── reports/
│   ├── executive_report.md
│   └── figures/
│
├── dashboard/
│
├── models/
│
├── requirements.txt
│
└── .gitignore
```

---

# 57. Reproducibility

Project harus dapat dijalankan ulang.

Dokumentasikan:

```bash
Python version
Dependencies
Dataset source
Data preparation
Feature engineering
Model parameters
Random seed
Evaluation methodology
```

Contoh:

```bash
requirements.txt
README.md
configuration files
```

---

# 58. Final Deliverables

Project final sebaiknya menghasilkan:

```bash
1. Clean dataset
2. Data quality report
3. EDA
4. Feature engineering pipeline
5. Baseline
6. Model benchmark
7. Validation report
8. Optimized model
9. Explainability analysis
10. Error analysis
11. Kaggle/holdout result
12. Business insight
13. Limitations
14. Executive report
15. Dashboard
16. GitHub repository
```

---

# 59. Prinsip Senior Data Specialist

Workflow ini dibangun berdasarkan beberapa prinsip utama.

## Principle 1 — Start With Business

```bash
Business Problem
        ↓
Data
        ↓
Model
```

bukan:

```bash
Model
 ↓
Find a problem
```

---

## Principle 2 — Evidence Before Conclusion

Gunakan:

```bash
Observation
↓
Evidence
↓
Hypothesis
↓
Validation
↓
Conclusion
```

bukan:

```bash
Chart
↓
Opinion
```

---

## Principle 3 — Simple Before Complex

Gunakan:

```bash
Baseline
↓
Simple Model
↓
Complex Model
```

sehingga improvement dapat diukur.

---

## Principle 4 — Validation Before Optimization

Jangan tuning model sebelum mengetahui apakah model tersebut memang memiliki generalization yang baik.

```bash
Benchmark
↓
Validation
↓
Optimization
```

---

## Principle 5 — Explain Before Trust

Model yang bagus tetapi tidak dipahami tetap membutuhkan investigation.

```bash
Performance
+
Explainability
+
Error Analysis
```

memberikan gambaran yang jauh lebih lengkap.

---

## Principle 6 — Error Is Information

Kesalahan model bukan hanya kegagalan.

Error dapat digunakan untuk menemukan:

```bash
Hidden Pattern
↓
New Hypothesis
↓
New Feature
↓
New Model
```

---

## Principle 7 — Kaggle Is a Benchmark, Not the Business

Kaggle dapat digunakan untuk external benchmarking.

Namun:

```bash
Kaggle Score ≠ Business Value
```

Model harus tetap dinilai berdasarkan:

```bash
Validation
Stability
Interpretability
Insight
Reproducibility
```

---

# 60. Final Mental Model

Secara sederhana, seluruh workflow dapat dipahami sebagai:

```bash
                    BUSINESS
                       │
                       ↓
                 WHAT & WHY?
                       │
                       ↓
                    DATA
                       │
                       ↓
                 WHAT EXISTS?
                       │
                       ↓
                  DATA QUALITY
                       │
                       ↓
                 CAN WE TRUST IT?
                       │
                       ↓
                     EDA
                       │
                       ↓
               WHAT PATTERNS EXIST?
                       │
                       ↓
                  HYPOTHESIS
                       │
                       ↓
               WHAT CAN WE TEST?
                       │
                       ↓
              FEATURE ENGINEERING
                       │
                       ↓
             HOW CAN WE REPRESENT IT?
                       │
                       ↓
                   BASELINE
                       │
                       ↓
               IS MODELING NEEDED?
                       │
                       ↓
                MODEL BENCHMARK
                       │
                       ↓
               WHAT WORKS BETTER?
                       │
                       ↓
                  VALIDATION
                       │
                       ↓
               DOES IT GENERALIZE?
                       │
                       ↓
                 OPTIMIZATION
                       │
                       ↓
              CAN IT BE IMPROVED?
                       │
                       ↓
                EXPLAINABILITY
                       │
                       ↓
              WHY DOES IT PREDICT?
                       │
                       ↓
                ERROR ANALYSIS
                       │
                       ↓
                 WHE
```
