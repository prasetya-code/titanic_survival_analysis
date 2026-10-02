FORMAT_NAMES = {
    ".csv": "CSV",
    ".tsv": "TSV",
    ".txt": "TXT",
    ".json": "JSON",
    ".jsonl": "JSONL",
    ".xlsx": "Excel",
    ".parquet": "Parquet",
}

VALIDATOR_NAMES = {
    ".csv": "CSV Structure Validator",
    ".tsv": "TSV Structure Validator",
    ".txt": "TXT Structure Validator",
    ".json": "JSON Structure Validator",
    ".jsonl": "JSONL Structure Validator",
    ".xlsx": "Excel Structure Validator",
    ".parquet": "Parquet Structure Validator",
}

SUPPORTED_EXTENSIONS = set(FORMAT_NAMES.keys())

DELIMITER_NAMES = {
    ",": "Comma (,)",
    ";": "Semicolon (;)",
    "\t": "Tab (\\t)",
    "|": "Pipe (|)",
}