from validator.models import Issue, Severity
from validator.rules.base import ValidationRule


class LearningOutcomesRule(ValidationRule):
    name = "LearningOutcomesRule"

    def validate(self, file, data, result):

        units = data.get("units", [])

        for unit_index, unit in enumerate(units, start=1):

            learning_outcomes = unit.get("learning_outcomes", [])

            numbers = []

            for lo in learning_outcomes:

                lo_num = lo.get("lo_num")

                if lo_num is None:
                    continue

                try:
                    numbers.append(int(lo_num))
                except (TypeError, ValueError):
                    result.add_issue(
                        Issue(
                            severity=Severity.ERROR,
                            rule=self.name,
                            message=f"Invalid learning outcome number '{lo_num}'.",
                            file=file,
                            location=f"Unit {unit_index}",
                        )
                    )

            if not numbers:
                continue

            expected = list(range(1, max(numbers) + 1))

            if numbers[0] != 1:
                result.add_issue(
                    Issue(
                        severity=Severity.ERROR,
                        rule=self.name,
                        message="Learning outcomes must start at 1.",
                        file=file,
                        location=f"Unit {unit_index}",
                    )
                )

            for expected_num in expected:
                if expected_num not in numbers:
                    result.add_issue(
                        Issue(
                            severity=Severity.ERROR,
                            rule=self.name,
                            message=f"Missing learning outcome number {expected_num}.",
                            file=file,
                            location=f"Unit {unit_index}",
                        )
                    )