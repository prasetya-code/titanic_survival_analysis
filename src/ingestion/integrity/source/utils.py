from datetime import datetime
from pathlib import Path


def format_size(size_bytes: int) -> str:
    
    # Format ukuran bytes menjadi human-readable
   
    size = float(size_bytes)

    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} TB"


def format_timestamp(timestamp: float) -> str:
    
    # Format filesystem timestamp

    return datetime.fromtimestamp(
        timestamp
    ).strftime("%Y-%m-%d %H:%M:%S")


def get_delimiter_display(delimiter):
    
    # Mengubah delimiter menjadi nama yang mudah dibaca.

    names = {
        ",": "Comma (,)",
        ";": "Semicolon (;)",
        "\t": "Tab (\\t)",
        "|": "Pipe (|)",
    }

    return names.get(
        delimiter,
        repr(delimiter)
    )