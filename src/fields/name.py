from ..fields.field import Field


class Name(Field):
    """
    Stores the contact name. Required field.

    Args:
        Field: Base class for all fields.
    """

    def validate(self):
        """
        Validate the name.

        Returns:
            bool: True if the name is valid, False otherwise.
        """
        return isinstance(self.value, str) and self.value != ""
