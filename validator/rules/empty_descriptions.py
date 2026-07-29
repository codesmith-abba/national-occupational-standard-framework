from validator.models import Issue, Severity
from validator.rules.base import ValidationRule


class EmptyDescriptionsRule(ValidationRule):
    name = "EmptyDescriptionsRule"

    def validate(self, file, data, result):

        # ---------- Trade Name ----------

        trade_name = data.get("trade_name")

        if isinstance(trade_name, str) and not trade_name.strip():
            result.add_issue(
                Issue(
                    severity=Severity.WARNING,
                    rule=self.name,
                    message="Trade name is empty.",
                    file=file,
                )
            )

        # ---------- Units ----------

        units = data.get("units", [])

        for unit_index, unit in enumerate(units, start=1):

            title = unit.get("title")

            if isinstance(title, str) and not title.strip():
                result.add_issue(
                    Issue(
                        severity=Severity.WARNING,
                        rule=self.name,
                        message="Unit title is empty.",
                        file=file,
                        location=f"Unit {unit_index}",
                    )
                )

            # ---------- Learning Outcomes ----------

            learning_outcomes = unit.get("learning_outcomes", [])

            for lo in learning_outcomes:

                lo_num = lo.get("lo_num", "?")

                description = lo.get("description")

                if isinstance(description, str) and not description.strip():
                    result.add_issue(
                        Issue(
                            severity=Severity.WARNING,
                            rule=self.name,
                            message="Learning outcome description is empty.",
                            file=file,
                            location=f"Unit {unit_index}, LO {lo_num}",
                        )
                    )

                # ---------- Performance Criteria ----------

                performance_criteria = lo.get("performance_criteria", [])

                for pc in performance_criteria:

                    pc_code = pc.get("pc_code", "?")

                    description = pc.get("description")

                    if isinstance(description, str) and not description.strip():
                        result.add_issue(
                            Issue(
                                severity=Severity.WARNING,
                                rule=self.name,
                                message="Performance criterion description is empty.",
                                file=file,
                                location=f"Unit {unit_index}, PC {pc_code}",
                            )
                        )