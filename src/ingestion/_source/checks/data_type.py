# source_validator/checks/data_type.py

from pathlib import Path


def check_data_type(file_path: Path) -> dict:
    """
    Memastikan path merupakan regular file.

    Menangani symbolic link secara eksplisit.
    """

    is_file = file_path.is_file()
    is_directory = file_path.is_dir()
    is_symlink = file_path.is_symlink()

    path_type = "Unknown"

    symlink_target = None
    symlink_target_exists = None
    symlink_target_is_file = None

    if is_symlink:

        try:

            symlink_target = file_path.resolve(
                strict=False
            )

            symlink_target_exists = (
                symlink_target.exists()
            )

            symlink_target_is_file = (
                symlink_target.is_file()
            )

            if (
                symlink_target_exists
                and symlink_target_is_file
            ):
                path_type = "Symbolic Link → File"

            elif (
                symlink_target_exists
                and symlink_target.is_dir()
            ):
                path_type = "Symbolic Link → Directory"

            else:
                path_type = "Broken Symbolic Link"

        except OSError:

            path_type = (
                "Symbolic Link → Unknown"
            )

    else:

        if is_file:
            path_type = "Regular File"

        elif is_directory:
            path_type = "Directory"

    valid = (
        is_file
        and not is_directory
        and (
            not is_symlink
            or (
                symlink_target_exists
                and symlink_target_is_file
            )
        )
    )

    if valid:

        return {
            "status": "PASS",
            "actual": {
                "is_file": is_file,
                "is_directory": is_directory,
                "is_symlink": is_symlink,
                "path_type": path_type,
                "symlink_target": (
                    str(symlink_target)
                    if symlink_target
                    else None
                ),
                "symlink_target_exists":
                    symlink_target_exists,
                "symlink_target_is_file":
                    symlink_target_is_file,
            },
            "expected": "regular data file",
            "message": "Path merupakan regular file.",
        }

    if is_symlink:

        if not symlink_target_exists:

            message = (
                "Symbolic link merupakan "
                "broken symlink."
            )

        elif symlink_target.is_dir():

            message = (
                "Symbolic link mengarah "
                "ke directory."
            )

        else:

            message = (
                "Symbolic link tidak "
                "mengarah ke regular file."
            )

    elif is_directory:

        message = (
            "Path merupakan directory, "
            "bukan regular file."
        )

    else:

        message = (
            "Path bukan regular file."
        )

    return {
        "status": "FAIL",
        "actual": {
            "is_file": is_file,
            "is_directory": is_directory,
            "is_symlink": is_symlink,
            "path_type": path_type,
            "symlink_target": (
                str(symlink_target)
                if symlink_target
                else None
            ),
            "symlink_target_exists":
                symlink_target_exists,
            "symlink_target_is_file":
                symlink_target_is_file,
        },
        "expected": "regular data file",
        "message": message,
    }