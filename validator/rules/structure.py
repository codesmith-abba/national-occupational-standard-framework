from validator.models import Issue, Severity
from validator.rules.base import ValidationRule


class StructureRule(ValidationRule):
    name = "StructureRule"

    def validate(self, file, data, result):

        # ---------- Root ----------

        required_root = (
            "trade_name",
            "level",
            "units",
        )

        for key in required_root:
            if key not in data:
                result.add_issue(
                    Issue(
                        severity=Severity.ERROR,
                        rule=self.name,
                        message=f"Missing root key '{key}'.",
                        file=file,
                    )
                )

        if "units" not in data:
            return

        if not isinstance(data["units"], list):
            result.add_issue(
                Issue(
                    severity=Severity.ERROR,
                    rule=self.name,
                    message="'units' must be a list.",
                    file=file,
                )
            )
            return

        # ---------- Units ----------

        for unit_index, unit in enumerate(data["units"], start=1):

            required_unit = (
                "code",
                "title",
                "learning_outcomes",
            )

            for key in required_unit:
                if key not in unit:
                    result.add_issue(
                        Issue(
                            severity=Severity.ERROR,
                            rule=self.name,
                            message=f"Missing unit key '{key}'.",
                            file=file,
                            location=f"Unit {unit_index}",
                        )
                    )

            if "learning_outcomes" not in unit:
                continue

            if not isinstance(unit["learning_outcomes"], list):
                result.add_issue(
                    Issue(
                        severity=Severity.ERROR,
                        rule=self.name,
                        message="'learning_outcomes' must be a list.",
                        file=file,
                        location=f"Unit {unit_index}",
                    )
                )
                continue

            # ---------- Learning Outcomes ----------

            for lo in unit["learning_outcomes"]:

                required_lo = (
                    "lo_num",
                    "description",
                    "performance_criteria",
                )

                for key in required_lo:
                    if key not in lo:
                        result.add_issue(
                            Issue(
                                severity=Severity.ERROR,
                                rule=self.name,
                                message=f"Missing learning outcome key '{key}'.",
                                file=file,
                                location=f"Unit {unit_index}",
                            )
                        )

                if "performance_criteria" not in lo:
                    continue

                if not isinstance(lo["performance_criteria"], list):
                    result.add_issue(
                        Issue(
                            severity=Severity.ERROR,
                            rule=self.name,
                            message="'performance_criteria' must be a list.",
                            file=file,
                            location=f"Unit {unit_index}",
                        )
                    )
                    continue

                # ---------- Performance Criteria ----------

                for pc in lo["performance_criteria"]:

                    required_pc = (
                        "pc_code",
                        "description",
                    )

                    for key in required_pc:
                        if key not in pc:
                            result.add_issue(
                                Issue(
                                    severity=Severity.ERROR,
                                    rule=self.name,
                                    message=f"Missing performance criteria key '{key}'.",
                                    file=file,
                                    location=f"Unit {unit_index}",
                                )
                            )