# Project Objective

Develop an analytical and predictive framework to identify the key factors associated with passenger survival and build a classification model capable of predicting survival outcomes.

## Business Questions

1. Faktor apa yang paling berhubungan dengan survival?
2. Bagaimana gender memengaruhi survival?
3. Bagaimana passenger class memengaruhi survival?
4. Bagaimana usia dan ukuran keluarga berhubungan dengan survival?
5. Apakah kombinasi beberapa karakteristik menghasilkan pola survival tertentu?
6. Seberapa akurat model dalam memprediksi survival?
7. Faktor apa yang paling berkontribusi terhadap prediksi model?


# Data Understanding

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


# Data Quality Assessment

contoh:

| Check       | Finding          | Impact | Treatment             |
| ----------- | ---------------- | ------ | --------------------- |
| Age         | Missing values   | Medium | Imputation            |
| Cabin       | High missingness | High   | Feature extraction    |
| Embarked    | Few missing      | Low    | Mode                  |
| PassengerId | Unique           | None   | Identifier only       |
| Fare        | Potential skew   | Medium | Distribution analysis |


# Exploratory Data Analysis

## Analysis Framework

```bash
                         SURVIVAL
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
       PEOPLE             CLASS            FAMILY
          │                 │                 │
     Sex / Age          Pclass / Fare     SibSp / Parch
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
                       SURVIVAL RATE
```

### Overall survival

```bash
Total passengers
Survivors
Non-survivors
Overall survival rate
```

### Survival by Sex

```bash
female
male
```

### Survival by Pclass

```bash
1st
2nd
3rd
```

### Survival by Age

Gunakan:

- distribution
- age bands
- survival rate


### Survival by Family

```bash
FamilySize
IsAlone
SibSp
Parch
```

### Interaction Analysis

cross analysis
```bash
Sex × Pclass
Sex × Age Group
Pclass × Age Group
FamilySize × Pclass
```


# Insight Layer

Saya sarankan pisahkan EDA dan Insights.


## Key Findings

### Finding 01 — Gender is a major survival differentiator

```bash
Evidence
    ↓
Female survival rate
Male survival rate
    ↓
Interpretation
    ↓
Potential explanation
```

### Finding 02 — Passenger class is strongly associated with survival

```bash
Pclass 1
Pclass 2
Pclass 3
```

### Finding 03 — Family structure matters

Misalnya Anda menemukan bahwa:
```bash
Alone
Small family
Large family
```

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


# Kaggle Benchmark

Setelah model selesai:
```bash
Local CV
     ↓
Final Model
     ↓
Test Prediction
     ↓
submission.csv
     ↓
Kaggle
     ↓
Leaderboard Score
```

Dokumentasikan:
```bash
Local CV Accuracy
Kaggle Accuracy
Leaderboard Position
```

Tetapi jangan menjadikan leaderboard sebagai satu-satunya ukuran keberhasilan portfolio. Karena recruiter senior biasanya lebih tertarik pada:
> bagaimana Anda melakukan analysis dan mengambil keputusan.


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


# Buat Dashboard

Untuk meningkatkan portfolio, saya bahkan akan menambahkan dashboard.
```bash
┌─────────────────────────────────────────────┐
│           TITANIC SURVIVAL ANALYSIS         │
├────────────┬────────────┬───────────────────┤
│ Passengers │ Survivors  │ Survival Rate     │
│    891     │    XXX     │      XX%          │
├────────────┴────────────┴───────────────────┤
│                                             │
│ Survival by Gender                          │
│ █████████████                              │
│                                             │
├──────────────────────┬──────────────────────┤
│ Survival by Pclass   │ Survival by Age     │
│                      │                     │
├──────────────────────┴──────────────────────┤
│ Family Size vs Survival                    │
│                                             │
└─────────────────────────────────────────────┘
```

Kemudian dashboard kedua:

Model Insights
```bash
Feature Importance
Confusion Matrix
Prediction Distribution
Error Analysis
```

# Yang membuatnya benar-benar "Senior"

## Junior approach
```bash
Dataset
 ↓
Clean
 ↓
Train model
 ↓
Accuracy
 ↓
Done
```

## Senior approach
```bash
              BUSINESS QUESTION
                      │
                      ▼
               DATA CONTRACT
                      │
                      ▼
               DATA QUALITY
                      │
                      ▼
               EXPLORATION
                      │
                      ▼
               HYPOTHESIS
                      │
                      ▼
             FEATURE ENGINEERING
                      │
                      ▼
             MODEL BENCHMARK
                      │
                      ▼
               VALIDATION
                      │
                      ▼
             EXPLAINABILITY
                      │
                      ▼
              ERROR ANALYSIS
                      │
                      ▼
              RECOMMENDATION
                      │
                      ▼
              COMMUNICATION
```


# Portfolio scoring framework

Saya bahkan akan menilai proyek Titanic Anda dengan framework berikut:
| Area                               |    Bobot |
| ---------------------------------- | -------: |
| Problem Framing                    |      10% |
| Data Understanding                 |      10% |
| Data Quality                       |      10% |
| EDA                                |      15% |
| Insight Quality                    |      15% |
| Feature Engineering                |      10% |
| Modeling                           |      10% |
| Validation                         |       5% |
| Explainability & Error Analysis    |       5% |
| Communication / Dashboard / README |      10% |
| **Total**                          | **100%** |


# Flow final yang saya rekomendasikan

```bash
┌─────────────────────────────────────────────┐
│             BUSINESS PROBLEM                │
│ "What drives passenger survival?"           │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│              DATA UNDERSTANDING             │
│ Source • Schema • Data Dictionary           │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│               DATA QUALITY                  │
│ Missing • Duplicate • Outlier • Validity    │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│                    EDA                      │
│ Demographic • Class • Family • Interaction  │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│                 HYPOTHESIS                  │
│ What factors appear to drive survival?      │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│           FEATURE ENGINEERING               │
│ Raw Data → Analytical Features              │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│             MODEL BENCHMARK                 │
│ Baseline → Logistic → Tree → Ensemble       │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│               VALIDATION                    │
│ Cross Validation • Metrics • Stability      │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│            MODEL EXPLAINABILITY             │
│ Feature Importance • SHAP                   │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│               ERROR ANALYSIS                │
│ False Positive • False Negative             │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│             KAGGLE VALIDATION               │
│ Submission • Benchmark • Iteration          │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│            EXECUTIVE INSIGHTS               │
│ Findings • Limitations • Recommendations    │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│              FINAL PORTFOLIO                │
│ GitHub + Dashboard + Report + Case Study    │
└─────────────────────────────────────────────┘
```

Satu hal lagi yang saya sarankan: jangan menggunakan Titanic sebagai proyek yang berdiri sendiri. Jadikan ini template standar portfolio Anda. Setelah Titanic, workflow yang sama bisa diterapkan ke proyek yang lebih dekat dengan dunia bisnis—misalnya customer churn, sales forecasting, fraud detection, marketing analytics, atau financial analytics.

Dengan begitu, recruiter akan melihat metodologi yang konsisten, bukan kumpulan notebook acak.