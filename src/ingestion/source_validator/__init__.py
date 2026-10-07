from .result_source import ValidationResult

from .existence import (
    check_path_exists,
    check_file_exists,
    check_target_exists,
)

from .accessibility import (
    check_readable,
    check_writable,
    check_executable,
    check_permission,
)

from .file_type import (
    check_is_file,
    check_is_directory,
    check_is_symlink,
    check_extension,
    check_mime_type,
)

from .metadata import (
    get_file_name,
    get_file_path,
    get_size_bytes,
    get_created_at,
    get_modified_at,
    get_accessed_at,
)

from .integrity import (
    check_non_empty,
    check_readable_content,
    check_openable,
    check_truncated,
    check_corrupted,
)


__all__ = [
    "ValidationResult",

    # existence
    "check_path_exists",
    "check_file_exists",
    "check_target_exists",

    # accessibility
    "check_readable",
    "check_writable",
    "check_executable",
    "check_permission",

    # file type
    "check_is_file",
    "check_is_directory",
    "check_is_symlink",
    "check_extension",
    "check_mime_type",

    # metadata
    "get_file_name",
    "get_file_path",
    "get_size_bytes",
    "get_created_at",
    "get_modified_at",
    "get_accessed_at",

    # integrity
    "check_non_empty",
    "check_readable_content",
    "check_openable",
    "check_truncated",
    "check_corrupted",
]