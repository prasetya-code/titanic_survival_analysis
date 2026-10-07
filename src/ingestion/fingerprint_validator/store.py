from pathlib import Path
import json


def load_fingerprint_store(
    fingerprint_path: Path,
) -> dict:
    """
    Membaca seluruh fingerprint yang tersimpan.

    Jika file belum ada, mengembalikan dictionary kosong.
    """

    if not fingerprint_path.exists():
        return {}

    with fingerprint_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def load_dataset_fingerprint(
    fingerprint_path: Path,
    dataset_name: str,
) -> dict | None:
    """
    Mengambil fingerprint untuk dataset tertentu.
    """

    store = load_fingerprint_store(
        fingerprint_path
    )

    return store.get(dataset_name)


def save_dataset_fingerprint(
    fingerprint_path: Path,
    dataset_name: str,
    fingerprint: dict,
) -> None:
    """
    Menyimpan fingerprint dataset.
    """

    fingerprint_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    store = load_fingerprint_store(
        fingerprint_path
    )

    store[dataset_name] = fingerprint

    with fingerprint_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            store,
            file,
            indent=2,
            ensure_ascii=False,
        )