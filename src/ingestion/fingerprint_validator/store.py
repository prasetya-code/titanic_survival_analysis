from pathlib import Path
import json
from typing import Optional


def load_store(store_path: Path) -> dict:
    """
    Load entire fingerprint store.

    Parameters
    ----------
    store_path : Path
        Path to fingerprint JSON file.

    Returns
    -------
    dict
        Stored fingerprint data.

    Notes
    -----
    If the file does not exist, an empty dictionary is returned.
    """

    if not store_path.exists():
        return {}

    with store_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def save_store(
    store_path: Path,
    data: dict,
) -> None:
    """
    Save entire fingerprint store.

    Parameters
    ----------
    store_path : Path
        Path to fingerprint JSON file.

    data : dict
        Data to save.
    """

    store_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with store_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )


def load_dataset(
    store_path: Path,
    dataset_name: str,
) -> Optional[dict]:
    """
    Load fingerprint data for a specific dataset.

    Parameters
    ----------
    store_path : Path
        Path to fingerprint JSON file.

    dataset_name : str
        Dataset identifier.

    Returns
    -------
    dict | None
        Dataset fingerprint data if found.
    """

    store = load_store(store_path)

    return store.get(dataset_name)


def save_dataset(
    store_path: Path,
    dataset_name: str,
    data: dict,
) -> None:
    """
    Save fingerprint data for a specific dataset.

    Existing datasets are preserved.
    """

    store = load_store(store_path)

    store[dataset_name] = data

    save_store(
        store_path=store_path,
        data=store,
    )


def delete_dataset(
    store_path: Path,
    dataset_name: str,
) -> bool:
    """
    Delete a dataset from the fingerprint store.

    Returns
    -------
    bool
        True if dataset existed and was deleted.
        False if dataset was not found.
    """

    store = load_store(store_path)

    if dataset_name not in store:
        return False

    del store[dataset_name]

    save_store(
        store_path=store_path,
        data=store,
    )

    return True