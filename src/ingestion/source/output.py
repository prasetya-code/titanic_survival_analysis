# source_validator/output.py

import sys


def print_header(dataset_name, file_path):
    print("\n" + "=" * 70)

    print(
        f"[INFO] Memulai Pengecekan Dataset: "
        f"'{dataset_name}'"
    )

    print("=" * 70)

    print()

    print("[DEBUG] Target:")

    print(
        f"  ├─ Path      : "
        f"{file_path.resolve()}"
    )

    print(
        f"  ├─ File      : "
        f"{file_path.name}"
    )

    print(
        f"  └─ Dataset   : "
        f"{dataset_name}"
    )


def print_step_header(number, title):
    print()
    print(
        f"[DEBUG] [{number}/5] {title}"
    )


def print_result(status):
    print(
        f"  └─ Result    : "
        f"{status}"
    )


def print_error(message):
    print(
        f"[ERROR] {message}",
        file=sys.stderr
    )


def print_failure(message):
    print()
    print(
        f"[FAIL] {message}"
    )
    print("-" * 70)


def print_success(dataset_name):
    print()
    print("-" * 70)

    print(
        f"[PASS] VALIDASI SUKSES: "
        f"File '{dataset_name}' memenuhi "
        f"seluruh kriteria."
    )

    print("-" * 70)