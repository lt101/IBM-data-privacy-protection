from abc import ABC, abstractmethod


class MechanismTemplate(ABC):
    """Abstract class as template for anonymization mechanisms"""

    @abstractmethod
    def create_form(self):
        """
         @brief Creates form for parameters of differential privacy mechanism. This form is used to create a new differential privacy mechanism
        """
        """Creates form for parameters of differential privacy mechanism."""

    @abstractmethod
    def apply_mech(self, col_to_anonymize: list):
        """
         @brief Applies differential privacy mechanism to list of chosen columns. This is a no - op in Panda
         @param col_to_anonymize list of columns to
        """
        """Applies differential privacy mechanism to list of chosen columns."""
