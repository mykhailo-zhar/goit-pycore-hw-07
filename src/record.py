from src.fields.name import Name
from src.fields.phone import Phone

PHONE_NOT_FOUND_ERROR = "Phone not found"
PHONE_NOT_VALID_ERROR = "Phone is not valid"
PHONE_ALREADY_EXISTS_ERROR = "Phone already exists"


class Record:
    def __init__(self, name: str):
        """
        Initialize the record with a name.

        Args:
            name (str): The name of the record.

        Raises:
            ValueError: If the name is not valid.
        """
        name_obj = Name(name)
        if not name_obj.validate():
            raise ValueError("Name is required")
        self._name = name_obj
        self._phones = []

    def add_phone(self, phone: str):
        """
        Add a phone to the record.

        Args:
            phone (str): The phone number to add.

        Raises:
            ValueError: If the phone number is not valid.
        """
        phone_obj = Phone(phone)
        if not phone_obj.validate():
            raise ValueError(PHONE_NOT_VALID_ERROR)

        if self.find_phone(phone) is not None:
            raise ValueError(PHONE_ALREADY_EXISTS_ERROR)

        self._phones.append(phone_obj)

    def remove_phone(self, phone: str):
        """
        Remove a phone from the record.

        Args:
            phone (str): The phone number to remove.

        Raises:
            ValueError: If the phone number is not found.
        """
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove is None:
            raise ValueError(PHONE_NOT_FOUND_ERROR)
        self._phones.remove(phone_to_remove)

    def find_phone(self, phone: str) -> Phone | None:
        """
        Find a phone in the record.

        Args:
            phone (str): The phone number to find.

        Returns:
            Phone | None: The phone object if found, None otherwise.
        """
        return next((x for x in self._phones if x.value == phone), None)

    def edit_phone(self, old_phone, new_phone):
        """
        Edit a phone in the record.

        Args:
            old_phone (_type_): The old phone number to edit.
            new_phone (_type_): The new phone number to edit.

        Raises:
            ValueError: If the old phone number is not found.
            ValueError: If the new phone number is not valid.
        """
        phone_index = next(
            (i for i, x in enumerate(self._phones) if x.value == old_phone), None
        )
        if phone_index is None:
            raise ValueError(PHONE_NOT_FOUND_ERROR)

        new_phone_obj = Phone(new_phone)
        if not new_phone_obj.validate():
            raise ValueError(PHONE_NOT_VALID_ERROR)

        self._phones[phone_index] = new_phone_obj
