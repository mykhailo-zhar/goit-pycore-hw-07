class Field:
    """
    Base class for all fields.
    """

    def __init__(self, value):
        """
        Initialize the field with a value.

        Args:
            value: The value to store in the field.
        """
        self.value = value

    def __str__(self):
        """
        Return the string representation of the field.
        """
        return str(self.value)

    def validate(self, value):
        """
        Validate the value

        Args:
            value: Value to validate.

        Returns:
            bool: True if the value is valid, False otherwise.
        """
        return True
