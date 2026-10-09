from pathlib import Path


# Fingerprint algorithm
HASH_ALGORITHM = "sha256"

# Chunk
HASH_CHUNK_SIZE = 1024 * 1024  # 1 MB

# Root dir project menggunakan Current Working Directory (CWD)
PROJECT_ROOT = Path.cwd().parent

# Directory
METADATA_DIR = PROJECT_ROOT / "metadata"

# File (FINGERPRINT_PATH)
FINGERPRINT_FILE = METADATA_DIR / "file_fingerprint.json"