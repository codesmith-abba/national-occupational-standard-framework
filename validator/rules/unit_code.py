import re

from validator.models import Issue, Severity
from validator.rules.base import ValidationRule


class UnitCodeRule(ValidationRule):
    name = "UnitCodeRule"

    CODE_PATTERNS = [
        # CON/PD/004/L2
        re.compile(
            r"^[A-Z]{2,5}/[A-Z0-9]{2,6}/\d{2,4}/L[1-5]$"
        ),

        # AGR/AEM/L1/001
        re.compile(
            r"^[A-Z]{2,5}/[A-Z0-9]{2,6}/L[1-5]/\d{2,4}$"
        ),

        # CONCJ/001/L3
        re.compile(
            r"^[A-Z]{4,8}/\d{2,4}/L[1-5]$"
        ),
    ]

    def validate(self, file, data, result):

        units = data.get("units", [])

        for unit_index, unit in enumerate(units, start=1):

            code = unit.get("code")

            if code is None:
                continue

            if not isinstance(code, str):
                result.add_issue(
                    Issue(
                        severity=Severity.ERROR,
                        rule=self.name,
                        message="Unit code must be a string.",
                        file=file,
                        location=f"Unit {unit_index}",
                    )
                )
                continue

            code = code.strip()

            if not code:
                result.add_issue(
                    Issue(
                        severity=Severity.ERROR,
                        rule=self.name,
                        message="Unit code is empty.",
                        file=file,
                        location=f"Unit {unit_index}",
                    )
                )
                continue

            if not any(pattern.fullmatch(code) for pattern in self.CODE_PATTERNS):
                result.add_issue(
                    Issue(
                        severity=Severity.ERROR,
                        rule=self.name,
                        message=f"Invalid unit code format: '{code}'.",
                        file=file,
                        location=f"Unit {unit_index}",
                    )
                )
            
            if re.search(r"/O+\d+/L", code):
                result.add_issue(
                    Issue(
                        severity=Severity.WARNING,
                        rule=self.name,
                        message=(
                            f"Possible OCR error in unit code '{code}' "
                            "(letter 'O' used instead of zero)."
                        ),
                        file=file,
                        location=f"Unit {unit_index}",
                    )
                )