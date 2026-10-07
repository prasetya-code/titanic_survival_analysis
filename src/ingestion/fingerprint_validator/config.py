from pathlib import Path


# Root dir project menggunakan Current Working Directory (CWD)
PROJECT_ROOT = Path.cwd().parent

# Directory
METADATA_DIR = PROJECT_ROOT / "metadata"

# File (FINGERPRINT_PATH)
DEFAULT_FINGERPRINT_PATH = METADATA_DIR / "source_fingerprint.json"

# Fingerprint algorithm
HASH_ALGORITHM = "sha256"