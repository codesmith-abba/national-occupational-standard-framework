import re

from validator.models import Issue, Severity
from validator.rules.base import ValidationRule


class LevelRule(ValidationRule):
    name = "LevelRule"

    LEVEL_PATTERN = re.compile(r"/L([1-5])(?:/|$)")

    def validate(self, file, data, result):

        document_level = data.get("level")

        if not isinstance(document_level, int):
            result.add_issue(
                Issue(
                    severity=Severity.ERROR,
                    rule=self.name,
                    message="'level' must be an integer.",
                    file=file,
                )
            )
            return

        units = data.get("units", [])

        for unit_index, unit in enumerate(units, start=1):

            code = unit.get("code")

            if not isinstance(code, str):
                continue

            match = self.LEVEL_PATTERN.search(code)

            if match is None:
                continue

            unit_level = int(match.group(1))

            if unit_level != document_level:
                result.add_issue(
                    Issue(
                        severity=Severity.ERROR,
                        rule=self.name,
                        message=(
                            f"Unit level L{unit_level} does not match "
                            f"document level L{document_level}."
                        ),
                        file=file,
                        location=f"Unit {unit_index}",
                    )
                )