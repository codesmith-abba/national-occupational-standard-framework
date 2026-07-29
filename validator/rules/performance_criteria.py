import re

from validator.models import Issue, Severity
from validator.rules.base import ValidationRule


class PerformanceCriteriaRule(ValidationRule):
    name = "PerformanceCriteriaRule"

    PC_PATTERN = re.compile(r"^(\d+)\.(\d+)$")

    def validate(self, file, data, result):

        units = data.get("units", [])

        for unit_index, unit in enumerate(units, start=1):

            learning_outcomes = unit.get("learning_outcomes", [])

            for lo in learning_outcomes:

                lo_num = lo.get("lo_num")

                try:
                    expected_lo = int(lo_num)
                except (TypeError, ValueError):
                    continue

                performance_criteria = lo.get("performance_criteria", [])

                numbers = []

                for pc in performance_criteria:

                    pc_code = pc.get("pc_code")

                    if not isinstance(pc_code, str):
                        continue

                    match = self.PC_PATTERN.fullmatch(pc_code.strip())

                    if match is None:
                        result.add_issue(
                            Issue(
                                severity=Severity.ERROR,
                                rule=self.name,
                                message=f"Invalid performance criterion code '{pc_code}'.",
                                file=file,
                                location=f"Unit {unit_index}, LO {expected_lo}",
                            )
                        )
                        continue

                    lo_part = int(match.group(1))
                    pc_part = int(match.group(2))

                    if lo_part != expected_lo:
                        result.add_issue(
                            Issue(
                                severity=Severity.ERROR,
                                rule=self.name,
                                message=(
                                    f"Performance criterion '{pc_code}' belongs "
                                    f"to LO {lo_part}, expected LO {expected_lo}."
                                ),
                                file=file,
                                location=f"Unit {unit_index}, LO {expected_lo}",
                            )
                        )
                        continue

                    numbers.append(pc_part)

                if not numbers:
                    continue

                if min(numbers) != 1:
                    result.add_issue(
                        Issue(
                            severity=Severity.ERROR,
                            rule=self.name,
                            message="Performance criteria must start at .1.",
                            file=file,
                            location=f"Unit {unit_index}, LO {expected_lo}",
                        )
                    )

                expected = list(range(1, max(numbers) + 1))

                for expected_num in expected:
                    if expected_num not in numbers:
                        result.add_issue(
                            Issue(
                                severity=Severity.ERROR,
                                rule=self.name,
                                message=(
                                    f"Missing performance criterion "
                                    f"{expected_lo}.{expected_num}."
                                ),
                                file=file,
                                location=f"Unit {unit_index}, LO {expected_lo}",
                            )
                        )