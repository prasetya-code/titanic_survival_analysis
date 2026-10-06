from dataclasses import dataclass, asdict
from typing import Any, Optional

# Supaya semua validator menghasilkan format yang konsisten.

@dataclass
class ValidationResult:
    name: str
    status: str
    actual: Any = None
    expected: Any = None
    message: str = ""
    details: Optional[dict] = None

    def to_dict(self) -> dict:
        return asdict(self)