# Project Objective

Mengembangkan kerangka kerja analitis dan prediktif untuk mengidentifikasi faktor-faktor utama yang berkaitan dengan kelangsungan hidup penumpang, serta membangun model klasifikasi yang mampu memprediksi hasil kelangsungan hidup tersebut.

---

# Analytical Questions

1. Faktor apa yang paling berhubungan dengan survival?
2. Apakah gender berpengaruh?
3. Apakah kelas penumpang berpengaruh?
4. Apakah umur berpengaruh?
5. Apakah struktur keluarga berpengaruh?
6. Apakah kombinasi gender + class memberikan insight tambahan?
7. Seberapa baik survival dapat diprediksi?
8. Mengapa model menghasilkan prediksi tertentu?
9. Dimana model melakukan kesalahan?

---

# Dataset Layer


## Data Understanding

| Variable    | Description                 | Type        | Role       |
| ----------- | --------------------------- | ----------- | ---------- |
| PassengerId | Unique passenger identifier | Integer     | Identifier |
| Survived    | Survival status             | Binary      | Target     |
| Pclass      | Passenger class             | Categorical | Feature    |
| Name        | Passenger name              | Text        | Feature    |
| Sex         | Passenger gender            | Categorical | Feature    |
| Age         | Passenger age               | Numeric     | Feature    |
| SibSp       | Siblings/spouses aboard     | Numeric     | Feature    |
| Parch       | Parents/children aboard     | Numeric     | Feature    |
| Ticket      | Ticket identifier           | Text        | Feature    |
| Fare        | Passenger fare              | Numeric     | Feature    |
| Cabin       | Cabin information           | Text        | Feature    |
| Embarked    | Port of embarkation         | Categorical | Feature    |


## Data Quality Assessment

contoh:

| Check       | Finding          | Impact | Treatment             |
| ----------- | ---------------- | ------ | --------------------- |
| Age         | Missing values   | Medium | Imputation            |
| Cabin       | High missingness | High   | Feature extraction    |
| Embarked    | Few missing      | Low    | Mode                  |
| PassengerId | Unique           | None   | Identifier only       |
| Fare        | Potential skew   | Medium | Distribution analysis |

---

# Methodology

```bash
Business Problem
        ↓
Data Understanding
        ↓
Data Quality
        ↓
Exploratory Data Analysis
        ↓
Feature Engineering
        ↓
Model Benchmarking
        ↓
Cross Validation
        ↓
Hyperparameter Optimization
        ↓
Explainability
        ↓
Error Analysis
        ↓
Kaggle Submission
```

---

# Modeling Strategy

Buat model benchmark
```bash
                    MODELING
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
     Baseline       Linear         Tree-based
        │              │              │
 DummyClassifier   Logistic       Decision Tree
                    Regression     Random Forest
                                      │
                                      ▼
                                Gradient Boosting
```

| Model               | CV Accuracy | Std | Notes            |
| ------------------- | ----------: | --: | ---------------- |
| Dummy               |         ... | ... | Baseline         |
| Logistic Regression |         ... | ... | Interpretable    |
| Decision Tree       |         ... | ... | Non-linear       |
| Random Forest       |         ... | ... | Ensemble         |
| Gradient Boosting   |         ... | ... | Strong benchmark |


# Validation Strategy

Ini salah satu bagian yang sangat bagus untuk menaikkan kualitas portfolio.

```bash
Train Dataset
      │
      ▼
Stratified Cross Validation
      │
      ├── Fold 1
      ├── Fold 2
      ├── Fold 3
      ├── Fold 4
      └── Fold 5
             │
             ▼
       Mean Performance
             +
       Performance Variance
```

Kemudian bahas:
```bash
accuracy
precision
recall
F1
confusion matrix
```

Walaupun Kaggle menggunakan accuracy, portfolio Anda sebaiknya tidak berhenti di accuracy.


# Model Explainability

Pertanyaan: 
> Why does the model make this prediction?

gunakan:
```bash
Feature Importance
Permutation Importance
SHAP
Partial Dependence
```


Jika menggunakan SHAP, misalnya:
```bash
                MODEL
                  │
                  ▼
             SHAP VALUES
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
      Sex       Pclass      Fare
       │          │          │
       └──────────┼──────────┘
                  ▼
             Prediction
```


Kemudian jelaskan secara bisnis/analitis.


# Error Analysis

Ini bagian yang sering tidak dilakukan oleh pemula. Tanyakan:
> Which passengers did the model get wrong?


Pisahkan:
```bash
True Positive
True Negative
False Positive
False Negative
```


Kemudian cari karakteristik error:
```bash
False Negative
↓
Who were they?
↓
Age?
Sex?
Pclass?
Family?
Fare?
```

Dari sini Anda dapat menemukan:
> “Model memiliki kesulitan mengidentifikasi kelompok penumpang tertentu.”

Itu jauh lebih bernilai daripada sekadar score.

---

# Evaluation

Models were evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- Stratified Cross Validation
- Confusion Matrix

---

# Feature Engineering

Di portfolio senior, tunjukkan reasoning, bukan hanya kode

```bash
RAW DATA
   │
   ├── Name
   │      ↓
   │    Title
   │
   ├── SibSp + Parch
   │      ↓
   │    FamilySize
   │      ↓
   │    IsAlone
   │
   ├── Cabin
   │      ↓
   │    HasCabin
   │
   └── Ticket
          ↓
       Group-related features
```

| Raw Feature   | Engineered Feature | Reason                                 |
| ------------- | ------------------ | -------------------------------------- |
| Name          | Title              | Capture social/demographic information |
| SibSp + Parch | FamilySize         | Represent household group              |
| FamilySize    | IsAlone            | Identify solo travelers                |
| Cabin         | HasCabin           | Preserve cabin availability signal     |
| Fare          | FarePerPerson      | Normalize group ticket cost            |

---

# Insight Layer

Saya sarankan pisahkan EDA dan Insights.


## Key Findings

[]

---

Model Performance (validation result)

[]

---

Limitations

[]

---

Technologies

Python
Pandas
NumPy
Scikit-learn
Matplotlib
Seaborn
SHAP

--- 

# Executive Summary

Buat satu halaman:

## Executive Summary
```bash
Objective
─────────
What are we trying to understand/predict?

Key Findings
─────────────
1. ...
2. ...
3. ...

Model Performance
──────────────────
Best Model: ...
CV Accuracy: ...

Key Drivers
────────────
1. ...
2. ...
3. ...

Limitations
───────────
...

Recommendation
──────────────
...
```

Orang yang membuka GitHub Anda tidak harus membaca 5 notebook untuk memahami hasilnya.