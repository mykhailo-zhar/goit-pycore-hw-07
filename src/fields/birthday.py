from datetime import datetime

from src.fields.field import Field


class Birthday(Field):
    DATE_FORMAT = "%d.%m.%Y"
    """
    Stores the contact birthday.

    Args:
        Field: Base class for all fields.
    """

    def validate(self):
        """
        Validate the birthday.
        """

        try:
            datetime.strptime(self.value, self.DATE_FORMAT)
            return True
        except (ValueError, TypeError):
            return False
