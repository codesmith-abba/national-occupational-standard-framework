from abc import ABC, abstractmethod

from validator.models import ValidationResult


class ValidationRule(ABC):
    """
    Base class for all validation rules.
    """

    name: str = "ValidationRule"

    @abstractmethod
    def validate(
        self,
        file: str,
        data: dict,
        result: ValidationResult,
    ) -> None:
        """
        Validate a JSON document.

        Parameters
        ----------
        file:
            Name of the JSON file.

        data:
            Parsed JSON document.

        result:
            ValidationResult object to append issues to.
        """
        raise NotImplementedError