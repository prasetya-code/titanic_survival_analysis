import polars as pl

# Paths
TRAIN_RAW = "data/raw/train.csv"
TEST_RAW = "data/raw/test.csv"
HISTORY_DIR = "reports/history"

# Configurations
MISSING_VALUES = ["", "NA", "N/A", "na", "n/a", "N/a"]

EXPECTED_TRAIN_COLUMNS = [
    "passengerid", "survived", "pclass", "name", "sex",
    "age", "sibsp", "parch", "ticket", "fare", "cabin", "embarked"
]

EXPECTED_TEST_COLUMNS = [
    "passengerid", "pclass", "name", "sex",
    "age", "sibsp", "parch", "ticket", "fare", "cabin", "embarked"
]

EXPECTED_DTYPES = {
    "passengerid": pl.Int64,
    "survived": pl.Int64,
    "pclass": pl.Int64,
    "name": pl.Utf8,
    "sex": pl.Utf8,
    "age": pl.Float64,
    "sibsp": pl.Int64,
    "parch": pl.Int64,
    "ticket": pl.Utf8,
    "fare": pl.Float64,
    "cabin": pl.Utf8,
    "embarked": pl.Utf8,
}

REFERENCE_ROW_COUNTS = {
    "train": 891,
    "test": 418
}

ROW_COUNT_DRIFT_TOLERANCE = 0

REQUIRED_NON_NULL = {
    "train": ["passengerid", "survived", "pclass", "name", "sex"],
    "test": ["passengerid", "pclass", "name", "sex"]
}

MISSINGNESS_THRESHOLDS = {
    "cabin": 0.80,
    "age": 0.25,
    "embarked": 0.05
}

STRING_COLUMNS = ["name", "sex", "ticket", "cabin", "embarked"]

NUMERIC_BOUNDS = {
    "passengerid": {"min": 1},
    "survived": {"min": 0, "max": 1},
    "pclass": {"min": 1, "max": 3},
    "age": {"min": 0, "max": 120},
    "sibsp": {"min": 0},
    "parch": {"min": 0},
    "fare": {"min": 0.0}
}

ALLOWED_VALUES = {
    "sex": {"male", "female"},
    "embarked": {"C", "Q", "S"}
}