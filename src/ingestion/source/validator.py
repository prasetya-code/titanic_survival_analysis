from pathlib import Path

from .checks.existence import check_existence
from .checks.data_type import check_data_type
from .checks.extension import check_extension
from .checks.integrity import check_integrity
from .checks.structure import check_structure

from .config import (
    FORMAT_NAMES,
    VALIDATOR_NAMES,
    SUPPORTED_EXTENSIONS,
)

from .output import (
    print_header,
    print_step_header,
    print_result,
    print_error,
    print_failure,
    print_success,
)


def _run_check(
    number: int,
    title: str,
    checker,
    file_path: Path,
    dataset_name: str,
):
    """
    Menjalankan satu tahap validation.
    """

    print_step_header(
        number,
        title
    )

    try:

        result = checker(
            file_path
        )

    except UnicodeDecodeError:

        result = {
            "status": "FAIL",
            "actual": "invalid encoding",
            "expected": "valid data file",
            "message": (
                f"Data file '{dataset_name}' "
                f"tidak menggunakan encoding UTF-8."
            ),
        }

    except Exception as error:

        print_result("ERROR")

        print_error(
            f"Tahap {number} Exception -> "
            f"{error}"
        )

        return {
            "status": "ERROR",
            "actual": type(error).__name__,
            "expected": (
                f"successful {title.lower()}"
            ),
            "message": str(error),
        }

    print_result(
        result["status"]
    )

    if result["status"] != "PASS":

        print_failure(
            f"Tahap {number} Gagal -> "
            f"{result['message']}"
        )

    return result


def check_source_file(
    file_path: Path,
    dataset_name: str = "dataset",
) -> dict:
    """
    Main source file validator.

    Validation:

        1. Existence
        2. Data type
        3. Extension
        4. Integrity
        5. Structure
    """

    file_path = Path(file_path)

    print_header(
        dataset_name,
        file_path
    )

    # ================================================================
    # 1. EXISTENCE
    # ================================================================

    existence = _run_check(
        1,
        "Check Existence",
        check_existence,
        file_path,
        dataset_name,
    )

    if existence["status"] != "PASS":
        return {
            "status": existence["status"],
            **existence,
        }

    # ================================================================
    # 2. DATA TYPE
    # ================================================================

    data_type = _run_check(
        2,
        "Check Data",
        check_data_type,
        file_path,
        dataset_name,
    )

    if data_type["status"] != "PASS":
        return {
            "status": data_type["status"],
            **data_type,
        }

    # ================================================================
    # 3. EXTENSION
    # ================================================================

    extension = _run_check(
        3,
        "Check Extension / Format",
        check_extension,
        file_path,
        dataset_name,
    )

    if extension["status"] != "PASS":
        return {
            "status": extension["status"],
            **extension,
        }

    # ================================================================
    # 4. INTEGRITY
    # ================================================================

    integrity = _run_check(
        4,
        "Check Integrity",
        check_integrity,
        file_path,
        dataset_name,
    )

    if integrity["status"] != "PASS":
        return {
            "status": integrity["status"],
            **integrity,
        }

    # ================================================================
    # 5. STRUCTURE
    # ================================================================

    structure = _run_check(
        5,
        "Check Structure",
        check_structure,
        file_path,
        dataset_name,
    )

    if structure["status"] != "PASS":
        return {
            "status": structure["status"],
            **structure,
        }

    # ================================================================
    # FINAL
    # ================================================================

    print_success(
        dataset_name
    )

    return _build_success_result(
        file_path=file_path,
        dataset_name=dataset_name,
        data_type=data_type,
        extension=extension,
        integrity=integrity,
        structure=structure,
    )


def _build_success_result(
    file_path: Path,
    dataset_name: str,
    data_type: dict,
    extension: dict,
    integrity: dict,
    structure: dict,
) -> dict:
    """
    Membentuk response akhir validator.
    """

    file_actual = data_type["actual"]
    extension_actual = extension["actual"]
    integrity_actual = integrity["actual"]
    metadata = structure["actual"]

    return {
        "status": "PASS",

        "actual": {

            "path": str(
                file_path.resolve()
            ),

            "file_name": file_path.name,

            "extension": (
                extension_actual["extension"]
            ),

            "format": (
                extension_actual["format"]
            ),

            "validator": (
                extension_actual["validator"]
            ),

            "file": file_actual,

            "size": {
                "bytes": integrity_actual[
                    "size_bytes"
                ],
                "human": integrity_actual[
                    "size_human"
                ],
            },

            "timestamp": {
                "created_at": integrity_actual[
                    "created"
                ],
                "modified_at": integrity_actual[
                    "modified"
                ],
                "last_access_at": integrity_actual[
                    "accessed"
                ],
            },

            "data": metadata,
        },

        "expected": {

            "file_exists": True,

            "regular_file": True,

            "extension": sorted(
                SUPPORTED_EXTENSIONS
            ),

            "readable": True,

            "non_empty": True,

            "has_header": True,

            "column_count": "> 0",

            "inconsistent_rows": 0,
        },

        "message": (
            f"Source file '{dataset_name}' "
            f"valid."
        ),
    }