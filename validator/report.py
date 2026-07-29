from .models import ValidationResult


class ConsoleReport:

    def render(self, result: ValidationResult) -> str:
        lines = []

        lines.append(f"File: {result.file}")
        lines.append("-" * 60)

        if result.is_valid:
            lines.append("Status : PASS")
        else:
            lines.append("Status : FAIL")

        lines.append(f"Errors   : {len(result.errors)}")
        lines.append(f"Warnings : {len(result.warnings)}")
        lines.append("")

        if result.issues:
            lines.append("Issues")
            lines.append("-" * 60)

            for issue in result.issues:
                location = f" [{issue.location}]" if issue.location else ""

                lines.append(
                    f"{issue.severity.value:<7} "
                    f"{issue.rule}{location}: "
                    f"{issue.message}"
                )

        return "\n".join(lines)