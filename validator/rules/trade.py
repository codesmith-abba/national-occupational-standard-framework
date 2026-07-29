import re

from validator.models import Issue, Severity
from validator.rules.base import ValidationRule


class TradeRule(ValidationRule):
    name = "TradeRule"

    _ARTIFACT_PATTERNS = (
        r"\bPAGE\s+\d+\b",
        r"\bNSQ\b",
        r"\bLEVEL\b",
        r"CREDIT\s+VALUE",
        r"//",
    )

    def validate(self, file, data, result):

        trade_name = data.get("trade_name")

        if trade_name is None:
            return

        if not isinstance(trade_name, str):
            result.add_issue(
                Issue(
                    severity=Severity.ERROR,
                    rule=self.name,
                    message="'trade_name' must be a string.",
                    file=file,
                )
            )
            return

        trade_name = trade_name.strip()

        if not trade_name:
            result.add_issue(
                Issue(
                    severity=Severity.ERROR,
                    rule=self.name,
                    message="Trade name is empty.",
                    file=file,
                )
            )
            return

        for pattern in self._ARTIFACT_PATTERNS:
            if re.search(pattern, trade_name, re.IGNORECASE):
                result.add_issue(
                    Issue(
                        severity=Severity.WARNING,
                        rule=self.name,
                        message="Trade name appears to contain PDF extraction artifacts.",
                        file=file,
                    )
                )
                break