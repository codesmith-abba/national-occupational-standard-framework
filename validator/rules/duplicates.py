from validator.models import Issue, Severity
from validator.rules.base import ValidationRule


class DuplicatesRule(ValidationRule):
    name = "DuplicatesRule"

    def validate(self, file, data, result):

        units = data.get("units", [])

        # ---------- Duplicate Unit Codes ----------

        seen_unit_codes = set()

        for unit_index, unit in enumerate(units, start=1):

            code = unit.get("code")

            if isinstance(code, str):

                if code in seen_unit_codes:
                    result.add_issue(
                        Issue(
                            severity=Severity.ERROR,
                            rule=self.name,
                            message=f"Duplicate unit code '{code}'.",
                            file=file,
                            location=f"Unit {unit_index}",
                        )
                    )
                else:
                    seen_unit_codes.add(code)

        # ---------- Duplicate Learning Outcomes ----------

        for unit_index, unit in enumerate(units, start=1):

            learning_outcomes = unit.get("learning_outcomes", [])

            seen_lo_numbers = set()

            for lo in learning_outcomes:

                lo_num = lo.get("lo_num")

                if lo_num is None:
                    continue

                lo_num = str(lo_num)

                if lo_num in seen_lo_numbers:
                    result.add_issue(
                        Issue(
                            severity=Severity.ERROR,
                            rule=self.name,
                            message=f"Duplicate learning outcome '{lo_num}'.",
                            file=file,
                            location=f"Unit {unit_index}",
                        )
                    )
                else:
                    seen_lo_numbers.add(lo_num)

                # ---------- Duplicate Performance Criteria ----------

                performance_criteria = lo.get("performance_criteria", [])

                seen_pc_codes = set()

                for pc in performance_criteria:

                    pc_code = pc.get("pc_code")

                    if pc_code is None:
                        continue

                    pc_code = str(pc_code)

                    if pc_code in seen_pc_codes:
                        result.add_issue(
                            Issue(
                                severity=Severity.ERROR,
                                rule=self.name,
                                message=f"Duplicate performance criterion '{pc_code}'. Verify against the source PDF.",
                                file=file,
                                location=f"Unit {unit_index}, LO {lo_num}",
                            )
                        )
                    else:
                        seen_pc_codes.add(pc_code)