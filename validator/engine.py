from validator.models import ValidationResult
from validator.rules.base import ValidationRule


class ValidationEngine:
    """
    Executes a collection of validation rules against a JSON document.
    """

    def __init__(self) -> None:
        self._rules: list[ValidationRule] = []

    def register(self, rule: ValidationRule) -> None:
        """
        Register a validation rule.
        """
        self._rules.append(rule)

    def validate(
        self,
        file: str,
        data: dict,
    ) -> ValidationResult:
        """
        Validate a single JSON document.
        """
        result = ValidationResult(file=file)

        for rule in self._rules:
            rule.validate(file, data, result)

        return result