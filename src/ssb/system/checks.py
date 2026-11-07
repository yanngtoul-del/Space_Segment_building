"""Common check results and status definitions for system evaluations."""

from dataclasses import dataclass
from enum import Enum


class CheckStatus(str, Enum):
    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"


@dataclass
class RuleCheckResult:
    rule_id: str
    category: str
    status: CheckStatus
    message: str
    current_value: float | str | None = None
    target_value: float | str | None = None
    unit: str = ""
