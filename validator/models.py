from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"


@dataclass(slots=True)
class Issue:
    severity: Severity
    rule: str
    message: str
    file: str
    location: Optional[str] = None


@dataclass(slots=True)
class ValidationResult:
    file: str
    issues: List[Issue] = field(default_factory=list)

    def add_issue(self, issue: Issue) -> None:
        self.issues.append(issue)

    @property
    def errors(self) -> List[Issue]:
        return [i for i in self.issues if i.severity == Severity.ERROR]

    @property
    def warnings(self) -> List[Issue]:
        return [i for i in self.issues if i.severity == Severity.WARNING]

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0