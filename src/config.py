from pathlib import Path
from datetime import datetime, timedelta, timezone
import time
import uuid


# Lokasi file saat ini
CONFIG_FILE = Path(__file__).resolve()
# print(f"CONFIG FILE LOCATION: {CONFIG_FILE}")

# Absolute path ke ROOT PROJECT
ROOT_PROJECT = CONFIG_FILE.parent.parent
# print(f"ABSOLUTE ROOT PROJECT DIRECTORY: {ROOT_PROJECT}")

# storage
STORAGE_DIR = ROOT_PROJECT / "storage"

DATA_STORE = STORAGE_DIR / "data"
METADATA_STORE = STORAGE_DIR / "metadata"
BASELINE_STORE = STORAGE_DIR / "baseline"

# Sub Section
RAW_DIR = DATA_STORE / "raw"
STAGE_DIR = DATA_STORE / "stage"

# Pipelien Section
STAGE_PIPELINE = "Ingestion"

# Dataset Section
SOURCE_DATA = "kaggle"
SOURCE_FORMAT = ".csv"

CONTRACT_FORMAT = ".yaml"
BASELINE_FORMAT = FINGERPRINT_FORMAT = ".json"

PROJECT_NAME = "titanic"
STAGE_FORMAT = ".parquet"


# ====================================================
# DATA
# ====================================================

TRAIN_RAW = RAW_DIR / f"train{SOURCE_FORMAT}"
TEST_RAW = RAW_DIR / f"test{SOURCE_FORMAT}"

DATA_CONTRACT = METADATA_STORE / f"data_contract{CONTRACT_FORMAT}"
BASELINE_PROFILE = BASELINE_STORE / f"{PROJECT_NAME}_baseline_profile{BASELINE_FORMAT}"



# ====================================================
# INGESTION PROCESS
# ====================================================

INGESTION_START = time.perf_counter()

WIB = timezone(timedelta(hours = 7))
RUN_TIMESTAMP = datetime.now(WIB)

TIMESTAMP_FORMAT = RUN_TIMESTAMP.strftime("%Y-%m-%d %H:%M:%S WIB")

# Membuat UUID v4 (Random UUID)
rand_UUID = uuid.uuid4()
# print(f"Tipe data: {type(rand_UUID)}, UUID: {rand_UUID}")

rand_UUID_str = str(uuid.uuid4())
# print(f"Tipe data: {type(rand_UUID_str)}, UUID: {rand_UUID_str}")

RUN_ID = f"{PROJECT_NAME}-{rand_UUID_str}"


# ====================================================
# Ingestion Code
# ====================================================

INGESTION_SUPP_EXT = {
    ".csv": "CSV",
    ".tsv": "TSV",
    ".txt": "TXT",
    ".json": "JSON",
    ".jsonl": "JSONL",
    ".xlsx": "Excel",
    ".parquet": "Parquet",
}


# Fingerprint algorithm
HASH_ALGORITHM = "sha256"
HASH_CHUNK_SIZE = 1024 * 1024  # 1 MB

FINGERPRINT_FILE = METADATA_STORE / f"file_fingerprint{FINGERPRINT_FORMAT}"
CONTENT_FINGERPRINT_FILE = METADATA_STORE / f"content_fingerprint{FINGERPRINT_FORMAT}"
SCHEMA_FINGERPRINT_FILE = METADATA_STORE / f"schema_fingerprint{FINGERPRINT_FORMAT}"