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

# Dataset

Kaggle Titanic Dataset


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

# Models

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting

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

Key engineered features:

- FamilySize
- IsAlone
- Title
- HasCabin
- Deck
- FamilyCategory

---

# Explainability

Model interpretation was performed using:

- Feature Importance
- Permutation Importance

---

Key Findings (insight after all process)

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

# Layer 1 — Data

```text
Raw Data
   ↓
Data Quality
   ↓
Clean Data
```

# Layer 2 — Analytics

```bash
EDA
   ↓
Hypothesis
   ↓
Insight
```

# Layer 3 — Machine Learning

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

# Layer 4 — Business Communication

```bash
Executive Summary
        ↓
Dashboard
        ↓
Recommendation
        ↓
GitHub Portfolio
```


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

# Flow akhir pengerjaan

```bash
┌───────────────────────────────┐
│ 1. BUSINESS PROBLEM           │
│ Objective + Questions         │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 2. DATA UNDERSTANDING         │
│ Schema + Data Dictionary      │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 3. DATA QUALITY               │
│ Missing + Duplicate + Validity│
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 4. EDA                        │
│ Pattern + Relationship        │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 5. HYPOTHESIS                 │
│ Why does survival differ?     │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 6. FEATURE ENGINEERING        │
│ Family + Title + Cabin        │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 7. BASELINE                   │
│ Establish benchmark           │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 8. MODEL BENCHMARK             │
│ LR / DT / RF / GB             │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 9. CROSS VALIDATION            │
│ Stability + Generalization    │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 10. OPTIMIZATION              │
│ Hyperparameter Tuning          │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 11. EXPLAINABILITY             │
│ Importance + Permutation       │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 12. ERROR ANALYSIS             │
│ FP / FN + Segment Analysis    │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 13. KAGGLE VALIDATION          │
│ Final submission               │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 14. BUSINESS INSIGHT           │
│ So What?                       │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 15. EXECUTIVE REPORT           │
│ Decision-oriented summary      │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ 16. DASHBOARD + GITHUB         │
│ Professional Portfolio         │
└───────────────────────────────┘
```