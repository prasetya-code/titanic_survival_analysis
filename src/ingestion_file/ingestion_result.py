from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ValidationResult:
    name: str
    status: str
    actual: Any = None
    expected: Any = None
    message: str = ""
    details: Optional[dict] = None

    def __str__(self) -> str:
        return (
            f"Status     : [{self.status}]\n"
            f"Validation : {self.name}\n"
            f"Expected   : {self.expected}\n"
            f"Actual     : {self.actual}\n"
            f"Messages   : {self.message}\n"
            f"Details    : {self.details}"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "status": self.status,
            "actual": self.actual,
            "expected": self.expected,
            "message": self.message,
            "details": self.details,
        }